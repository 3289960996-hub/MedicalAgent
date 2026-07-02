def human_handoff_tool(
    question: str,
    risk_level: str = "normal",
    recommended_department: str = "",
    llm_intent: dict | None = None
) -> dict:
    """
    判断是否建议转人工导诊或现场医护。
    """
    llm_intent = llm_intent or {}
    handoff_keywords = [
        "吃什么药", "用药剂量", "治疗方案", "怎么治", "是不是得了",
        "诊断", "说不清哪里不舒服", "不知道哪里难受"
    ]

    need_handoff = False
    reasons = []

    if risk_level in ["high", "emergency", "高风险"]:
        need_handoff = True
        reasons.append("存在急危重症风险")

    if any(keyword in question for keyword in handoff_keywords):
        need_handoff = True
        reasons.append("问题涉及诊断、用药、治疗或描述不清")

    if "导诊台" in recommended_department:
        need_handoff = True
        reasons.append("推荐科室需要现场进一步分诊")

    if llm_intent.get("need_handoff") is True:
        need_handoff = True
        reasons.append("LLM意图识别建议人工确认")

    return {
        "need_handoff": need_handoff,
        "handoff_required": need_handoff,
        "reason": "；".join(reasons),
        "handoff_message": "建议咨询医院导诊台或现场医护人员。"
    }
