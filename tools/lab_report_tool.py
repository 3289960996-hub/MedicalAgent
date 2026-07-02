def lab_report_tool(question: str) -> dict:
    """
    体检指标解释工具。
    只做健康科普解释，不做疾病诊断。
    """

    if "白细胞" in question:
        return {
            "indicator": "白细胞",
            "explanation": "白细胞升高可能与感染、炎症、应激反应等因素有关。",
            "warning": "不能仅凭白细胞一项指标判断疾病，需要结合症状、体征和医生判断。"
        }

    if "血糖" in question:
        return {
            "indicator": "血糖",
            "explanation": "血糖升高可能与饮食、糖尿病、应激状态等因素有关。",
            "warning": "建议结合空腹血糖、餐后血糖和糖化血红蛋白综合判断。"
        }

    if "尿酸" in question:
        return {
            "indicator": "尿酸",
            "explanation": "尿酸升高可能与饮食、代谢异常、肾脏排泄功能等因素有关。",
            "warning": "长期尿酸升高可能增加痛风风险，建议咨询医生。"
        }

    if "血压" in question:
        return {
            "indicator": "血压",
            "explanation": "血压长期升高可能提示高血压风险。",
            "warning": "建议多次测量并咨询医生，不能凭一次测量结果直接判断。"
        }

    if "转氨酶" in question:
        return {
            "indicator": "转氨酶",
            "explanation": "转氨酶升高可能与肝脏损伤、饮酒、药物影响、脂肪肝等因素有关。",
            "warning": "需要结合其他肝功能指标和医生判断。"
        }

    return {
        "indicator": "未知指标",
        "explanation": "暂未匹配到该体检指标解释。",
        "warning": "建议携带完整体检报告咨询医生。"
    }
