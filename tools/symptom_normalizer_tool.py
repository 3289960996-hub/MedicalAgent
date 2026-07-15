import json

from agent_core.json_utils import clean_json_text
from agent_core.llm import call_llm


def symptom_normalizer_tool(question: str) -> dict:
    """
    口语化症状标准化工具。
    把患者口语描述转换成标准症状、身体部位和症状特点。
    不能诊断疾病，不能开药。
    """

    messages = [
        {
            "role": "system",
            "content": (
                "你是医疗导诊系统的症状标准化工具。"
                "你只能提取症状、身体部位、症状特点和风险信号。"
                "不能诊断疾病，不能开药，不能给治疗方案。"
                "必须严格返回 JSON，不要输出额外文字。"
            )
        },
        {
            "role": "user",
            "content": f"""
请将用户的口语化症状描述标准化。

用户原文：
{question}

请严格返回 JSON：
{{
  "original_text": "用户原文",
  "standard_symptoms": [],
  "body_parts": [],
  "symptom_features": [],
  "duration": "",
  "severity": "",
  "possible_department_hint": "",
  "is_vague": false,
  "risk_signals": [],
  "reason": ""
}}

说明：
- standard_symptoms 示例：疼痛、胀痛、麻木、瘙痒、红肿、发热
- body_parts 示例：膝盖、耳朵、眼睛、腹部、胸口
- symptom_features 示例：一阵一阵、里面痛、酸胀、刺痛、活动后加重
- possible_department_hint 只能写科室方向，例如骨科、耳鼻喉科、眼科、消化内科
- 不要诊断疾病
"""
        }
    ]

    result = call_llm(messages)

    try:
        data = json.loads(clean_json_text(result))
        return {
            "original_text": data.get("original_text", question),
            "standard_symptoms": data.get("standard_symptoms", []),
            "body_parts": data.get("body_parts", []),
            "symptom_features": data.get("symptom_features", []),
            "duration": data.get("duration", ""),
            "severity": data.get("severity", ""),
            "possible_department_hint": data.get("possible_department_hint", ""),
            "is_vague": data.get("is_vague", False),
            "risk_signals": data.get("risk_signals", []),
            "reason": data.get("reason", "")
        }
    except Exception:
        return {
            "original_text": question,
            "standard_symptoms": [],
            "body_parts": [],
            "symptom_features": [],
            "duration": "",
            "severity": "",
            "possible_department_hint": "",
            "is_vague": True,
            "risk_signals": [],
            "reason": "症状标准化解析失败。"
        }
