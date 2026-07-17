import base64
import binascii
import json
import re
from typing import Any

from openai import OpenAI

from agent_core.config import LLM_API_KEY, LLM_BASE_URL, LLM_VISION_MODEL, check_config
from agent_core.lab_report_report import build_analysis_result, normalize_report_type
from agent_core.lab_report_rules import apply_indicator_rules
from medical_knowledge.knowledge_retriever import (
    knowledge_context,
    knowledge_sources,
    retrieve_lab_knowledge,
)


MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MIN_TRUSTED_CONFIDENCE = 0.75


EXTRACTION_SAFETY_PROMPT = """
Before extracting any values, classify the uploaded image.
Return these additional top-level JSON fields:
- is_lab_report: boolean; true only when the image visibly contains a medical laboratory test report/table.
- image_quality: one of "clear", "partial", or "unreadable".
- quality_reason: a short Chinese explanation.

Safety rules:
1. A photo, animal, person, scenery, screenshot, or unrelated document is not a lab report.
2. Never infer a common test panel or invent plausible values from layout, context, or prior knowledge.
3. For a stained, covered, blurred, or cropped report, extract only fields that remain directly legible.
4. Omit every indicator whose name or result is uncertain; do not reconstruct obscured digits.
5. If the image is not a lab report, or no indicator name-and-result pair is directly legible, return an empty indicators array.
""".strip()


EXTRACTION_PROMPT = """
你是医学检验报告结构化助手。识别图片并只返回 JSON，不做医学解释、疾病诊断或治疗建议。
要求：
1. 提取报告类型、报告日期、样本信息，以及每项指标的名称、结果原文、可计算数值、单位、参考范围、原报告异常标记和识别置信度。
   report_type 只能填写血常规、肝功能、肾功能、尿常规、血脂血糖、甲状腺功能、乙肝及感染、炎症指标、凝血功能、心肌标志物、肿瘤标志物或化验单；医院名称和“检验报告单”不是检查类型。
2. source_flag 只记录原报告明确出现的 H、L、箭头、偏高、偏低、危急等标记；没有就留空。不要自行判断高低。
3. confidence 为 0 到 1；模糊、遮挡或无法确认的字段必须降低置信度。
4. 不返回姓名、身份证号、手机号、住院号、条码等个人身份信息。
5. 无法识别的字段使用空字符串或 null，不得猜测。
JSON 结构：
{
  "report_type": "",
  "report_date": "",
  "sample_info": "",
  "indicators": [
    {
      "name": "",
      "result": "",
      "value": null,
      "unit": "",
      "reference_range": "",
      "source_flag": "",
      "confidence": 0.0
    }
  ]
}
""".strip()


INTERPRETATION_PROMPT = """
你是谨慎的医学检验报告解释助手。后端已根据报告参考范围判定指标状态，你只能解释，不能修改指标名称、结果、单位、参考范围或状态。
只返回以下 JSON：
{
  "indicator_explanations": [{"name": "", "explanation": ""}],
  "abnormal_summary": "",
  "interpretation": "",
  "possible_factors": [],
  "possible_systems": [],
  "possible_directions": [],
  "suggested_checks": [],
  "recommendations": [],
  "suggested_department": "全科",
  "red_flags": []
}
要求：
1. 优先依据 knowledge_context 中匹配到的本地医学知识解释；知识不足时明确保持谨慎，不得自行补造依据。
2. indicator_explanations 只解释 high、low、critical 等异常项，不逐项复述正常指标；每项最多 2 句，按“结果判断—常见影响—复核建议”的顺序组织。
3. 全文使用谨慎表达，但同一句最多使用一次“可能”；禁止出现“可能可能”“可能提示可能”，也不要在多个相邻分句反复使用“可能提示”。可交替使用“可受……影响”“需关注”“建议复核”等自然表达。
4. abnormal_summary 只概括主要异常及组合关系，控制在 2 句内，不罗列全部正常指标。
5. interpretation 控制在 3 句内：先给报告整体结论，再说明需要关注的项目，最后给复核原则；不得重复 indicator_explanations 和 abnormal_summary 的原句。
6. possible_systems 只填写身体系统或功能名称，例如“肝胆系统”“血液系统”“肾脏功能”“内分泌系统”，不要带“可能涉及”“考虑”等前缀。
7. possible_directions 每项优先用“需要关注……”表述，不直接写疾病诊断，每项只写一个方向。
8. suggested_checks 给出具体的复查项目或就医沟通重点；recommendations 简短、可执行，不给治疗方案。
9. 正常结果用一句整体概括即可；缺少参考范围或状态无法判断的项目应明确写“待复核”，不得把它描述为异常。
10. 风险等级由后端规则生成，你不得自行判断或返回风险等级。
11. 不能修改后端给出的指标状态，也不要在 JSON 中编造知识来源；来源由后端单独生成。
12. 不得确诊疾病、开药、推荐药物、制定治疗方案或预测疾病结果。
""".strip()


def _get_client() -> OpenAI:
    check_config()
    return OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


def analyze_lab_report_image(image_data_url: str) -> dict[str, Any]:
    mime_type, raw = _validate_image_data_url(image_data_url)
    normalized_url = f"data:{mime_type};base64,{base64.b64encode(raw).decode('ascii')}"
    response = _get_client().chat.completions.create(
        model=LLM_VISION_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": f"{EXTRACTION_PROMPT}\n\n{EXTRACTION_SAFETY_PROMPT}"},
                {"type": "image_url", "image_url": {"url": normalized_url}},
            ],
        }],
        temperature=0.1,
    )
    extracted = _parse_json_object(response.choices[0].message.content)
    if extracted.get("is_lab_report") is not True:
        raise ValueError("导入的图片不是化验单，请上传清晰、完整的医学检验报告。")
    image_quality = str(extracted.get("image_quality") or "unreadable").lower()
    if image_quality not in {"clear", "partial"}:
        raise ValueError("化验单内容被严重遮挡或无法辨认，系统不会猜测数据，请重新拍摄后上传。")
    normalized = [_normalize_indicator(item) for item in (extracted.get("indicators") or [])[:100]]
    trusted = [
        item for item in normalized
        if item["name"] and item["result"] and item["confidence"] >= MIN_TRUSTED_CONFIDENCE
    ]
    if not trusted:
        raise ValueError("未识别到可信的检验项目和结果，系统不会补造数据，请上传更清晰的化验单。")
    indicators = apply_indicator_rules(trusted)
    report_type = normalize_report_type(extracted.get("report_type"), indicators)
    result = _normalize_analysis({**extracted, "report_type": report_type, "indicators": indicators})
    result.update({
        "verified": False,
        "requires_review": True,
        "image_quality": image_quality,
        "quality_reason": str(extracted.get("quality_reason") or "")[:300],
    })
    return result


def interpret_confirmed_indicators(report_type: str, indicators: list[dict[str, Any]]) -> dict[str, Any]:
    if not indicators:
        raise ValueError("至少需要一项已确认的检验指标。")
    safe_indicators = apply_indicator_rules(
        [_normalize_indicator(item) for item in indicators[:100]],
        allow_confirmed_status=True,
    )
    report_type = normalize_report_type(report_type, safe_indicators)
    explanation = _request_interpretation(report_type, safe_indicators)
    result = _normalize_analysis({
        **explanation,
        "report_type": report_type,
        "indicators": safe_indicators,
        "verified": True,
    })
    result["requires_review"] = False
    return result


def _request_interpretation(report_type: Any, indicators: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        documents = retrieve_lab_knowledge(str(report_type or "化验单"), indicators)
    except Exception:
        documents = []
    content = json.dumps(
        {
            "report_type": str(report_type or "化验单")[:80],
            "indicators": indicators,
            "knowledge_context": knowledge_context(documents),
        },
        ensure_ascii=False,
    )
    response = _get_client().chat.completions.create(
        model=LLM_VISION_MODEL,
        messages=[
            {"role": "system", "content": INTERPRETATION_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0.1,
    )
    parsed = _parse_json_object(response.choices[0].message.content)
    return {**parsed, "knowledge_sources": knowledge_sources(documents)}


def _validate_image_data_url(value: str) -> tuple[str, bytes]:
    match = re.fullmatch(r"data:([^;,]+);base64,(.+)", str(value or ""), flags=re.DOTALL)
    if not match:
        raise ValueError("图片数据格式不正确。")
    mime_type = match.group(1).lower()
    if mime_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("仅支持 JPG、PNG 或 WebP 图片。")
    try:
        raw = base64.b64decode(match.group(2), validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("图片 Base64 数据无效。") from exc
    if not raw:
        raise ValueError("图片内容为空。")
    if len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("图片不能超过 8MB。")
    signatures = {
        "image/jpeg": (b"\xff\xd8\xff",),
        "image/png": (b"\x89PNG\r\n\x1a\n",),
        "image/webp": (b"RIFF",),
    }
    if not any(raw.startswith(signature) for signature in signatures[mime_type]):
        raise ValueError("图片内容与文件类型不匹配。")
    if mime_type == "image/webp" and raw[8:12] != b"WEBP":
        raise ValueError("WebP 图片格式无效。")
    return mime_type, raw


def _parse_json_object(content: Any) -> dict[str, Any]:
    text = str(content or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("模型未返回可解析的结构化结果。")
        value = json.loads(text[start:end + 1])
    if not isinstance(value, dict):
        raise ValueError("模型返回格式不正确。")
    return value


def _normalize_indicator(item: Any) -> dict[str, Any]:
    source = item if isinstance(item, dict) else {}
    status = str(source.get("status") or "unknown").lower()
    if status not in {"high", "low", "normal", "critical", "unknown"}:
        status = "unknown"
    try:
        confidence = max(0.0, min(1.0, float(source.get("confidence", 0))))
    except (TypeError, ValueError):
        confidence = 0.0
    value = source.get("value")
    if value not in (None, ""):
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = None
    return {
        "name": str(source.get("name") or "").strip()[:100],
        "result": str(source.get("result") or "")[:100],
        "value": value,
        "unit": str(source.get("unit") or "")[:50],
        "reference_range": str(source.get("reference_range") or "")[:100],
        "source_flag": str(source.get("source_flag") or "")[:30],
        "status": status,
        "confidence": confidence,
    }


def _normalize_analysis(payload: dict[str, Any]) -> dict[str, Any]:
    verified = bool(payload.get("verified", False))
    indicators = apply_indicator_rules(
        [_normalize_indicator(item) for item in (payload.get("indicators") or [])[:100]],
        allow_confirmed_status=verified,
    )
    return build_analysis_result(
        payload,
        indicators,
        report_type=str(payload.get("report_type") or "化验单")[:80],
        verified=verified,
    )
