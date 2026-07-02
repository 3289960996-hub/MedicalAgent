from agent_core.graph import (
    build_visit_guide,
    canonicalize_department,
    doctors_by_department,
    get_department_location,
    normalize_confidence,
    normalize_risk_level,
)


CHAT_SCHEMA_DEFAULTS = {
    "type": "medical",
    "answer": "",
    "display_text": "",
    "speak_text": "",
    "analysis": "",
    "guide": "",
    "visit_guide": "",
    "risk_level": "low",
    "department": "全科",
    "recommended_department": "全科",
    "canonical_department": "全科",
    "confidence": 0.45,
    "symptom_summary": "",
    "possible_conditions": [],
    "red_flags": [],
    "reason": "",
    "department_location": {},
    "location": {},
    "registration_steps": [],
    "followup_items": [],
    "follow_up_items": [],
    "followup_questions": [],
    "follow_up_questions": [],
    "doctors": [],
    "recommended_doctors": [],
    "sources": [],
    "source_details": [],
    "handoff": {},
    "business_guard": {},
    "tools_used": [],
    "decision_path": [],
}


def ensure_chat_schema(result: dict) -> dict:
    for key, value in CHAT_SCHEMA_DEFAULTS.items():
        if key not in result or result[key] is None:
            result[key] = value.copy() if isinstance(value, (dict, list)) else value
    return result


def normalize_chat_result(
    result: dict,
    question: str = "",
    initial_department: str = "",
    followup_done: bool = False
) -> dict:
    followup_questions = (
        result.get("followup_questions")
        or result.get("follow_up_questions")
        or []
    )
    result["followup_questions"] = followup_questions
    result["follow_up_questions"] = followup_questions

    followup_items = (
        result.get("followup_items")
        or result.get("follow_up_items")
        or []
    )
    if not followup_items and followup_questions:
        followup_items = [
            {
                "question": question,
                "options": []
            }
            for question in followup_questions
        ]
    result["followup_items"] = followup_items
    result["follow_up_items"] = followup_items

    risk_level = normalize_risk_level(result.get("risk_level", "low"))
    result["risk_level"] = risk_level

    raw_department = (
        result.get("canonical_department")
        or result.get("department")
        or result.get("recommended_department")
        or ""
    )

    if followup_done and initial_department and risk_level != "high" and not raw_department:
        raw_department = initial_department

    department = canonicalize_department(
        raw_department or ("全科/急诊" if risk_level == "high" else "全科"),
        question,
        risk_level,
    )

    result["department"] = department
    result["recommended_department"] = department
    result["canonical_department"] = department
    result["confidence"] = normalize_confidence(result.get("confidence", 0.45))
    result["symptom_summary"] = result.get("symptom_summary") or ""
    result["possible_conditions"] = result.get("possible_conditions") or []
    result["red_flags"] = result.get("red_flags") or []
    result["reason"] = result.get("reason") or ""

    department_location = get_department_location(department)
    result["department_location"] = department_location
    result["location"] = department_location

    if result.get("need_followup") is True:
        result.setdefault("analysis", "")
        result.setdefault("guide", "")
        result["doctors"] = []
        result["recommended_doctors"] = []
        return ensure_chat_schema(result)

    result["analysis"] = (
        result.get("analysis")
        or result.get("answer")
        or result.get("display_text")
        or ""
    )

    registration_steps = result.get("registration_steps") or []
    result["guide"] = result.get("guide") or "\n".join(
        f"{index + 1}. {step}"
        for index, step in enumerate(registration_steps)
    )
    result["visit_guide"] = result.get("visit_guide") or build_visit_guide(department, risk_level)

    doctors = result.get("doctors") or result.get("recommended_doctors") or []
    if not doctors:
        doctors = doctors_by_department(department)

    result["doctors"] = doctors
    result["recommended_doctors"] = result.get("recommended_doctors") or doctors
    result.setdefault("sources", [])

    return ensure_chat_schema(result)
