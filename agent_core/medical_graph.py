from agent_core.graph import graph as medical_graph

def run_medical_graph(question: str, client_type: str = "web", session_state: dict | None = None) -> dict:
    initial_state = {
        "question": question,
        "client_type": client_type,
        "answer": "",
        "risk_level": "",
        "recommended_department": "",
        "confidence": "",
        "business_guard": {},
        "triage_analysis": {},
        "llm_intent": {},
        "qwen_followup": {},
        "normalized_symptom": {},
        "location": {},
        "registration_steps": [],
        "handoff": {},
        "rag_context": "",
        "sources": [],
        "source_details": [],
        "need_followup": False,
        "follow_up_questions": [],
        "followup_questions": [],
        "follow_up_items": [],
        "followup_items": [],
        "symptom_summary": "",
        "possible_conditions": [],
        "canonical_department": "",
        "red_flags": [],
        "reason": "",
        "tools_used": [],
        "tool_results": [],
        "decision_path": [],
        "display_text": "",
        "speak_text": "",
    }

    if session_state:
        initial_state["session_state"] = session_state

    result = medical_graph.invoke(initial_state)

    result["type"] = "follow_up" if result.get("need_followup") else "medical"

    llm_intent = result.get("llm_intent", {}) or {}
    followup_info = {
        "missing_info": llm_intent.get("missing_info", []),
        "need_followup": result.get("need_followup", False),
        "follow_up_questions": result.get("follow_up_questions", []),
        "followup_questions": result.get("followup_questions", result.get("follow_up_questions", [])),
        "follow_up_items": result.get("follow_up_items", []),
        "followup_items": result.get("followup_items", result.get("follow_up_items", [])),
    }
    result.setdefault("qwen_followup", followup_info)

    if not result.get("answer") and result.get("display_text"):
        result["answer"] = result["display_text"]
    result.setdefault("answer", "")
    result.setdefault("session_id", "")

    return result
