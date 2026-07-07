import json
import re

from agent_core.langchain_chains import run_qwen_followup_chain


DEFAULT_RESULT = {
    "need_followup": False,
    "symptom_type": "未明确症状",
    "known_info": {},
    "missing_info": [],
    "follow_up_questions": [],
    "follow_up_items": [],
    "preliminary_department": "全科医学科或导诊台",
    "risk_level": "normal",
    "reason": "Qwen 追问结果解析失败，建议先补充关键信息。"
}


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return cleaned


def _safe_list(value) -> list:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def _safe_followup_items(value, fallback_questions: list[str]) -> list[dict]:
    items = []
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            question = str(item.get("question") or item.get("text") or "").strip()
            if not question:
                continue
            options = _safe_list(item.get("options"))[:6]
            if len(options) < 2:
                continue
            items.append({
                "question": question,
                "options": options
            })

    return items[:3]


def _safe_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "需要", "是"}
    return bool(value)


def qwen_followup_tool(question: str, session_state: dict | None = None) -> dict:
    """
    使用 Qwen 根据症状动态判断是否需要追问。
    只做导诊信息收集，不使用 RAG，不诊断疾病，不给治疗方案。
    """
    session_state = session_state or {}
    previous_missing = session_state.get("missing_info", [])
    previous_result = session_state.get("last_preliminary_result", {})
    followup_count = session_state.get("followup_count", 0)

    try:
        result_text = run_qwen_followup_chain(
            question=question,
            previous_missing=previous_missing,
            previous_result=previous_result,
            followup_count=followup_count
        )
        data = json.loads(_clean_json_text(result_text))
    except Exception:
        data = DEFAULT_RESULT.copy()

    follow_up_questions = (
        _safe_list(data.get("follow_up_questions"))
        or _safe_list(data.get("followup_questions"))
    )[:3]
    follow_up_items = _safe_followup_items(
        data.get("follow_up_items") or data.get("followup_items"),
        follow_up_questions
    )
    if not follow_up_questions:
        follow_up_questions = [item["question"] for item in follow_up_items]
    missing_info = _safe_list(data.get("missing_info"))
    need_followup = _safe_bool(data.get("need_followup", False))
    if not follow_up_items:
        need_followup = False
        follow_up_questions = []

    if followup_count >= 1:
        need_followup = False
        follow_up_questions = []
        follow_up_items = []

    return {
        "need_followup": need_followup,
        "symptom_type": str(data.get("symptom_type") or "未明确症状"),
        "known_info": data.get("known_info") if isinstance(data.get("known_info"), dict) else {},
        "missing_info": missing_info,
        "follow_up_questions": follow_up_questions,
        "followup_questions": follow_up_questions,
        "follow_up_items": follow_up_items,
        "followup_items": follow_up_items,
        "preliminary_department": str(data.get("preliminary_department") or "全科医学科或导诊台"),
        "risk_level": str(data.get("risk_level") or "normal"),
        "reason": str(data.get("reason") or "")
    }
