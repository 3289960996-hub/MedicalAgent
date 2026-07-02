GUARD_MESSAGE = "当前系统未接入真实医院业务系统，无法提供该信息，请以医院官方系统或现场工作人员为准。"


def business_guard_tool(question: str) -> dict:
    """
    拦截不能编造的真实医院业务信息，以及诊断、用药、治疗方案问题。
    """
    block_keywords = [
        "今天有号", "还有号", "剩余号源", "张医生", "李医生",
        "主任医师出诊", "医生排班", "什么时候出诊", "多少钱",
        "费用", "报销多少", "医保报销比例", "吃什么药",
        "用药剂量", "治疗方案", "我是不是得了"
    ]

    if any(keyword in question for keyword in block_keywords):
        return {
            "blocked": True,
            "reason": "当前系统未接入真实医院业务系统或问题涉及诊断/用药/治疗方案。",
            "message": GUARD_MESSAGE
        }

    return {
        "blocked": False,
        "reason": "",
        "message": ""
    }
