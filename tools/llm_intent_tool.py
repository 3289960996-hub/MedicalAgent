import json

from agent_core.json_utils import clean_json_text
from agent_core.llm import call_llm


FALLBACK_RESULT = {
    "intent": "unknown",
    "symptoms": [],
    "body_parts": [],
    "risk_level": "unknown",
    "need_handoff": True,
    "need_followup": False,
    "missing_info": [],
    "reason": "LLM意图识别解析失败，建议人工确认。"
}


def llm_intent_tool(question: str) -> dict:
    """
    使用 Qwen 识别用户真实意图。
    只做意图、症状、部位、风险和交接判断，不诊断疾病，不提供用药或治疗方案。
    """
    messages = [
        {
            "role": "system",
            "content": (
                "你是医疗导诊系统的意图识别工具。"
                "你只能识别意图、症状、身体部位、风险等级和缺失信息。"
                "不能诊断疾病，不能开药，不能给用药剂量，不能提供治疗方案。"
                "必须严格返回 JSON，不要输出任何额外文字。"
            )
        },
        {
            "role": "user",
            "content": f"""
请识别下面用户问题的医疗导诊意图。

可选 intent：
- department_recommendation
- lab_report_explanation
- hospital_process_question
- medication_question
- diagnosis_question
- treatment_question
- emergency_triage
- general_medical_question
- unknown

规则：
1. 用户问吃什么药、用药剂量、药物选择，intent=medication_question，need_handoff=true。
2. 用户问治疗方案、怎么治，intent=treatment_question，need_handoff=true。
3. 用户问“我是不是得了某病”“是不是某疾病”，intent=diagnosis_question，need_handoff=true。
4. 胸痛、呼吸困难、喘不上气、意识不清、大出血、剧烈头痛等急危重症，intent=emergency_triage，risk_level=emergency。
5. 只描述身体不适并询问挂什么科，intent=department_recommendation。
6. 检验检查指标含义，intent=lab_report_explanation。
7. 挂号、取号、缴费、医保、就医流程，intent=hospital_process_question。

用户问题：
{question}

请严格返回如下 JSON 结构：
{{
  "intent": "department_recommendation / lab_report_explanation / hospital_process_question / medication_question / diagnosis_question / treatment_question / emergency_triage / general_medical_question / unknown",
  "symptoms": [],
  "body_parts": [],
  "risk_level": "normal / emergency / unknown",
  "need_handoff": false,
  "need_followup": false,
  "missing_info": [],
  "reason": ""
}}
"""
        }
    ]

    result = call_llm(messages)

    try:
        data = json.loads(clean_json_text(result))
    except Exception:
        return FALLBACK_RESULT.copy()

    return {
        "intent": data.get("intent", "unknown"),
        "symptoms": data.get("symptoms", []),
        "body_parts": data.get("body_parts", []),
        "risk_level": data.get("risk_level", "unknown"),
        "need_handoff": data.get("need_handoff", False),
        "need_followup": data.get("need_followup", False),
        "missing_info": data.get("missing_info", []),
        "reason": data.get("reason", "")
    }
