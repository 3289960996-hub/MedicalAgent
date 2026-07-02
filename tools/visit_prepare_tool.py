def visit_prepare_tool(department: str) -> dict:
    """
    就诊准备建议工具。
    根据推荐科室生成就诊准备清单。
    """

    prepare_list = [
        "携带身份证、医保卡或就诊卡。",
        "记录症状开始时间、持续时间和变化情况。",
        "如有体温、血压、血糖等数据，建议提前记录。",
        "携带既往检查报告、体检报告或用药记录。",
        "如症状严重或持续加重，应及时前往急诊。"
    ]

    return {
        "department": department,
        "prepare_list": prepare_list
    }
