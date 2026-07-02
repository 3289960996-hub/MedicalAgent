def slot_check_tool(question: str) -> dict:
    """
    信息完整性检查工具。
    导诊类问题尽量收集年龄、持续时间、体温、伴随症状等信息。
    """

    missing_slots = []

    if not any(word in question for word in ["岁", "年龄", "男", "女", "孩子", "宝宝", "老人"]):
        missing_slots.append("年龄或基本信息")

    if not any(word in question for word in ["天", "小时", "分钟", "周", "月", "刚刚", "今天", "昨天"]):
        missing_slots.append("症状持续时间")

    if "发烧" in question or "发热" in question:
        if not any(word in question for word in ["度", "℃", "体温"]):
            missing_slots.append("最高体温")

    if any(word in question for word in ["咳嗽", "发烧", "发热", "胸痛", "胸疼", "腹痛"]):
        if not any(word in question for word in ["没有", "无", "伴有", "同时", "呼吸困难", "胸痛", "胸疼"]):
            missing_slots.append("是否有胸痛、呼吸困难等伴随症状")

    if missing_slots:
        return {
            "complete": False,
            "missing_slots": missing_slots,
            "follow_up_questions": [
                f"请补充：{slot}" for slot in missing_slots
            ]
        }

    return {
        "complete": True,
        "missing_slots": [],
        "follow_up_questions": []
    }
