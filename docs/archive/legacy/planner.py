def make_plan(question: str) -> dict:
    """
    根据用户问题生成 Agent 执行计划。
    """

    intent = "general_medical_question"
    tools = ["medical_rag_tool"]

    emergency_keywords = [
        "胸痛", "胸疼", "呼吸困难", "喘不上气", "意识不清", "大出血",
        "剧烈头痛", "抽搐", "昏迷", "严重外伤", "高烧不退",
        "说话不清", "一侧肢体无力"
    ]

    lab_keywords = [
        "白细胞", "红细胞", "血小板", "血糖", "尿酸", "血压",
        "胆固醇", "甘油三酯", "转氨酶", "肌酐", "尿常规",
        "血常规", "体检指标", "体检报告", "检查结果", "化验单"
    ]

    process_keywords = [
        "挂号", "取号", "缴费", "医保", "报销", "预约",
        "就诊流程", "看病流程", "怎么去医院", "第一次去医院",
        "导诊台", "候诊", "复诊"
    ]

    symptom_keywords = [
        "疼", "痛", "不舒服", "难受", "痒", "肿", "麻", "红",
        "出血", "发烧", "发热", "咳嗽", "咳痰", "流鼻涕",
        "头晕", "头痛", "恶心", "呕吐", "腹泻", "胸闷",
        "耳朵", "耳鸣", "听不清", "眼睛", "牙", "牙疼",
        "尿", "尿痛", "尿频", "月经", "皮肤", "孩子", "宝宝"
    ]

    if any(word in question for word in emergency_keywords):
        intent = "emergency_triage"
        tools = [
            "risk_triage_tool",
            "high_risk_log_tool",
            "human_handoff_tool"
        ]

    elif any(word in question for word in lab_keywords):
        intent = "lab_report_explanation"
        tools = ["lab_report_tool", "medical_rag_tool"]

    elif any(word in question for word in process_keywords) or any(word in question for word in symptom_keywords):
        if any(word in question for word in symptom_keywords):
            intent = "department_recommendation"
        else:
            intent = "hospital_process_question"

        tools = [
            "risk_triage_tool",
            "slot_check_tool",
            "department_router_tool",
            "hospital_map_tool",
            "registration_guide_tool",
            "human_handoff_tool",
            "visit_prepare_tool",
            "medical_rag_tool"
        ]

    return {
        "intent": intent,
        "tools": tools,
        "reason": "根据用户问题类型生成 Agent 工具调用计划。"
    }
