def registration_guide_tool(department: str) -> dict:
    """
    生成通用挂号流程，不提供真实号源、医生排班或剩余号源。
    """
    return {
        "department": department,
        "steps": [
            "通过医院小程序、自助机或人工窗口进入挂号入口。",
            f"选择推荐科室：{department}。",
            "根据医院官方系统显示的实际号源选择就诊时间段。",
            "完成挂号后，按挂号信息前往对应候诊区。",
            "如不确定科室或流程，请咨询医院导诊台。"
        ],
        "notice": "当前系统不提供真实号源信息，请以医院官方系统为准。"
    }
