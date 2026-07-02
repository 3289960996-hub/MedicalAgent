def risk_triage_tool(question: str) -> dict:
    """
    风险分级工具。
    如果用户描述包含高风险症状，优先提醒急诊。
    简单处理“没有胸痛”“无呼吸困难”这类否定表达。
    """

    negative_patterns = [
        "没有胸痛",
        "无胸痛",
        "没有呼吸困难",
        "无呼吸困难",
        "没有喘不上气",
        "无喘不上气",
        "没有意识不清",
        "无意识不清",
        "没有高热",
        "无高热",
        "没有大量出血",
        "无大量出血",
        "没有严重外伤",
        "无严重外伤",
        "没有吞咽困难",
        "无吞咽困难",
    ]

    high_keywords = [
        "高热", "呼吸困难", "喘不上气", "意识模糊", "意识不清",
        "大量出血", "大出血", "剧烈胸痛", "严重外伤", "昏迷",
        "面部肿胀迅速加重", "吞咽困难"
    ]

    dental_keywords = ["牙疼", "牙痛", "牙龈肿", "牙龈", "面部肿胀", "脸肿"]
    has_dental = any(keyword in question for keyword in dental_keywords)
    has_fever = "发烧" in question or "发热" in question or "高热" in question
    has_face_swelling = "面部肿胀" in question or "脸肿" in question
    has_breath_or_swallow_issue = "呼吸困难" in question or "吞咽困难" in question or "影响呼吸" in question or "影响吞咽" in question

    if has_dental and ((has_face_swelling and has_fever) or has_breath_or_swallow_issue or "面部肿胀迅速加重" in question):
        return {
            "risk_level": "high",
            "reason": "牙痛伴面部肿胀、发热或呼吸/吞咽相关风险信号。",
            "action": "建议尽快就医，必要时走急诊/转人工评估。"
        }

    for keyword in high_keywords:
        has_keyword = keyword in question
        is_negated = any(pattern in question for pattern in negative_patterns if keyword in pattern)

        if has_keyword and not is_negated:
            return {
                "risk_level": "high",
                "reason": f"用户描述中包含高风险症状：{keyword}",
                "action": "建议急诊/立即就医，并尽快联系现场医护人员。"
            }

    medium_keywords = [
        "持续三天", "持续多天", "反复发作", "越来越严重", "明显加重",
        "疼得厉害", "痛得厉害", "肿得厉害"
    ]

    if has_dental and any(keyword in question for keyword in ["肿", "持续", "多天", "三天", "两天", "局部肿胀"]):
        return {
            "risk_level": "medium",
            "reason": "牙痛伴局部肿胀或持续多天，建议尽快到口腔科就诊。",
            "action": "建议尽快就诊。"
        }

    if any(keyword in question for keyword in medium_keywords):
        return {
            "risk_level": "medium",
            "reason": "症状持续、反复或加重，建议尽快到相应门诊就诊。",
            "action": "建议尽快就诊。"
        }

    return {
        "risk_level": "low",
        "reason": "暂未识别到明显高风险症状。",
        "action": "可按普通门诊流程就诊。"
    }
