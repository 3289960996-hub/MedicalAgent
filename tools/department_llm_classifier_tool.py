import json

from agent_core.llm import call_llm


VALID_DEPARTMENTS = [
    "急诊科",
    "全科医学科",
    "呼吸内科",
    "发热门诊",
    "消化内科",
    "心内科",
    "神经内科",
    "骨科",
    "皮肤科",
    "耳鼻喉科",
    "眼科",
    "口腔科",
    "泌尿外科",
    "妇科",
    "儿科",
    "内分泌科",
    "导诊台"
]


def clean_json_text(text: str) -> str:
    """
    清洗 Qwen 可能返回的 ```json 代码块。
    """
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return text


def normalize_confidence(value: str | None) -> str:
    """
    统一置信度，避免 Qwen 返回中文、大小写或空值导致前端看不到。
    """
    text = str(value or "").strip().lower()

    if text in ["high", "高", "较高"]:
        return "high"
    if text in ["medium", "moderate", "中", "中等", "较中"]:
        return "medium"
    if text in ["low", "低", "较低"]:
        return "low"

    return "low"


def normalize_department(value: str | None) -> str:
    department = str(value or "").strip()
    if department in VALID_DEPARTMENTS:
        return department
    if department == "全科医学科或导诊台":
        return department
    return "全科医学科或导诊台"


def department_llm_classifier_tool(
    question: str,
    llm_intent: dict | None = None,
    rule_result: dict | None = None
) -> dict:
    """
    使用 Qwen 做科室分类兜底。
    只从固定科室列表中选择，不诊断疾病，不开药。
    """

    messages = [
        {
            "role": "system",
            "content": (
                "你是医院导诊科室分类助手。"
                "你只能根据用户描述推荐最合适的就诊科室。"
                "不能诊断疾病，不能开药，不能给治疗方案。"
                "必须严格返回 JSON，不要输出任何额外文字。"
            )
        },
        {
            "role": "user",
            "content": f"""
请根据用户描述，从固定科室列表中选择最合适的一个科室。

固定科室列表：
{VALID_DEPARTMENTS}

用户问题：
{question}

LLM 意图识别结果：
{llm_intent or {}}

规则科室推荐结果：
{rule_result or {}}

请严格返回如下 JSON：
{{
  "department": "科室名称",
  "reason": "推荐原因",
  "confidence": "high/medium/low",
  "source": "llm_classifier"
}}
"""
        }
    ]

    result = call_llm(messages)

    try:
        data = json.loads(clean_json_text(result))
        confidence = normalize_confidence(data.get("confidence"))
        department = normalize_department(data.get("department"))

        return {
            "department": department,
            "reason": data.get("reason", ""),
            "confidence": confidence,
            "source": data.get("source", "llm_classifier")
        }
    except Exception:
        return {
            "department": "全科医学科或导诊台",
            "reason": "Qwen 科室分类结果解析失败，建议到导诊台进一步分诊。",
            "confidence": "low",
            "source": "llm_classifier_fallback"
        }
