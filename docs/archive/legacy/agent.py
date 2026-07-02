from langsmith import traceable
from legacy.planner import make_plan
from tools.business_guard_tool import business_guard_tool
from tools.department_llm_classifier_tool import department_llm_classifier_tool
from tools.department_router_tool import department_router_tool
from tools.high_risk_log_tool import high_risk_log_tool
from tools.hospital_map_tool import hospital_map_tool
from tools.human_handoff_tool import human_handoff_tool
from tools.lab_report_tool import lab_report_tool
from tools.llm_intent_tool import llm_intent_tool
from tools.registration_guide_tool import registration_guide_tool
from tools.qwen_followup_tool import qwen_followup_tool
from tools.risk_triage_tool import risk_triage_tool
from tools.robot_response_tool import robot_response_tool
from tools.slot_check_tool import slot_check_tool
from tools.visit_prepare_tool import visit_prepare_tool

from agent_core.langchain_chains import run_final_answer_chain


SAFE_HANDOFF_INTENTS = {
    "medication_question",
    "diagnosis_question",
    "treatment_question"
}


def build_decision_path(
    plan: dict,
    llm_intent: dict,
    risk_level: str,
    extra_steps: list[str] | None = None
) -> list[str]:
    decision_path = [
        f"规则规划：{plan.get('intent', 'unknown')}",
        f"LLM意图识别:{llm_intent.get('intent', 'unknown')}",
        f"风险等级：{risk_level}"
    ]

    if extra_steps:
        decision_path.extend(extra_steps)

    return decision_path


def empty_business_guard() -> dict:
    return {
        "blocked": False,
        "reason": "",
        "message": ""
    }


def empty_handoff() -> dict:
    return {
        "need_handoff": False,
        "reason": "",
        "handoff_message": ""
    }


def normalize_preliminary_department(department: str) -> str:
    known_departments = [
        "急诊科", "眼科", "耳鼻喉科", "口腔科", "儿科", "呼吸内科",
        "发热门诊", "心内科", "神经内科", "内分泌科", "消化内科",
        "骨科", "皮肤科", "泌尿外科", "妇科", "全科医学科或导诊台",
        "导诊台"
    ]
    text = department or ""
    for item in known_departments:
        if item in text:
            return item
    if "足踝" in text:
        return "骨科"
    if "肾内" in text:
        return "泌尿外科"
    return "全科医学科或导诊台"

@traceable(name="run_medical_agent")
def run_medical_agent(
    question: str,
    client_type: str = "web",
    session_state: dict | None = None
) -> dict:
    """
    Medical Agent 主流程。
    client_type 可取 web / robot / mini_program。
    """

    session_state = session_state or {}
    plan = make_plan(question)
    business_guard = business_guard_tool(question)
    tool_results = [
        {
            "tool": "business_guard_tool",
            "result": business_guard
        }
    ]

    if business_guard["blocked"]:
        answer = business_guard["message"]
        handoff = human_handoff_tool(question)
        robot_result = robot_response_tool(answer)

        return {
            "type": "business_guard_blocked",
            "question": question,
            "answer": answer,
            "risk_level": "normal",
            "recommended_department": "",
            "confidence": "",
            "need_followup": False,
            "follow_up_questions": [],
            "tools_used": ["business_guard_tool", "human_handoff_tool"],
            "tool_results": tool_results + [{"tool": "human_handoff_tool", "result": handoff}],
            "sources": [],
            "source_details": [],
            "display_text": robot_result["display_text"],
            "speak_text": robot_result["speak_text"],
            "llm_intent": {},
            "decision_path": [
                f"规则规划：{plan.get('intent', 'unknown')}",
                "业务拦截：blocked"
            ],
            "location": {},
            "registration_steps": {},
            "handoff": handoff,
            "business_guard": business_guard
        }

    recommended_department = ""
    department_confidence = ""
    risk_level = "normal"
    sources = []
    rag_context = ""
    location = {}
    registration_steps = {}
    handoff = empty_handoff()
    decision_steps = []
    risk_checked = False
    slot_checked = False
    qwen_followup_result = {}

    # 高风险优先处理，不进入普通追问或普通 Qwen 导诊。
    if "risk_triage_tool" in plan["tools"]:
        risk_result = risk_triage_tool(question)
        risk_checked = True

        tool_results.append({
            "tool": "risk_triage_tool",
            "result": risk_result
        })

        risk_level = risk_result["risk_level"]

        if risk_level == "emergency":
            recommended_department = "急诊科"
            department_confidence = "high"
            location = hospital_map_tool(recommended_department)
            registration_steps = registration_guide_tool(recommended_department)
            log_result = high_risk_log_tool(
                question=question,
                risk_level=risk_level,
                reason=risk_result.get("reason", ""),
                action=risk_result.get("action", "")
            )
            handoff = human_handoff_tool(question, risk_level, recommended_department, {})

            tool_results.extend([
                {"tool": "hospital_map_tool", "result": location},
                {"tool": "registration_guide_tool", "result": registration_steps},
                {"tool": "high_risk_log_tool", "result": log_result},
                {"tool": "human_handoff_tool", "result": handoff}
            ])
            decision_steps.extend([
                "高风险日志：已记录",
                "人工转接：建议"
            ])

            answer = (
                risk_result["action"]
                + " 本系统仅提供导诊和健康科普参考，不能替代医生诊断。"
            )
            robot_result = robot_response_tool(answer)

            return {
                "type": "emergency",
                "question": question,
                "answer": answer,
                "risk_level": risk_level,
                "recommended_department": recommended_department,
                "confidence": department_confidence,
                "need_followup": False,
                "follow_up_questions": [],
                "tools_used": [
                    "business_guard_tool",
                    "risk_triage_tool",
                    "hospital_map_tool",
                    "registration_guide_tool",
                    "high_risk_log_tool",
                    "human_handoff_tool"
                ],
                "tool_results": tool_results,
                "sources": [],
                "source_details": [],
                "display_text": robot_result["display_text"],
                "speak_text": robot_result["speak_text"],
                "llm_intent": {},
                "decision_path": build_decision_path(plan, {}, risk_level, decision_steps),
                "location": location,
                "registration_steps": registration_steps,
                "handoff": handoff,
                "business_guard": business_guard
            }

    # 非急诊症状先使用 Qwen 动态追问，不使用 RAG 或知识库。
    if plan.get("intent") == "department_recommendation":
        qwen_followup_result = qwen_followup_tool(question, session_state)
        slot_checked = True
        tool_results.append({
            "tool": "qwen_followup_tool",
            "result": qwen_followup_result
        })

        recommended_department = normalize_preliminary_department(
            qwen_followup_result.get("preliminary_department", "")
        )
        department_confidence = "medium" if recommended_department else "low"
        risk_level = qwen_followup_result.get("risk_level") or risk_level
        if risk_level == "emergency":
            risk_level = "high"
        location = hospital_map_tool(recommended_department)
        registration_steps = registration_guide_tool(recommended_department)
        handoff = human_handoff_tool(question, risk_level, recommended_department, {})
        tool_results.extend([
            {"tool": "hospital_map_tool", "result": location},
            {"tool": "registration_guide_tool", "result": registration_steps},
            {"tool": "human_handoff_tool", "result": handoff}
        ])

        if qwen_followup_result.get("need_followup") is True:
            answer = "目前信息还不完整，暂不做疾病判断。请补充以下信息："
            robot_result = robot_response_tool(answer)

            return {
                "type": "follow_up",
                "question": question,
                "answer": answer,
                "risk_level": risk_level,
                "recommended_department": recommended_department,
                "preliminary_department": qwen_followup_result.get("preliminary_department", recommended_department),
                "confidence": department_confidence,
                "need_followup": True,
                "follow_up_questions": qwen_followup_result.get("follow_up_questions", []),
                "tools_used": ["business_guard_tool", "risk_triage_tool", "qwen_followup_tool"],
                "tool_results": tool_results,
                "sources": [],
                "source_details": [],
                "display_text": answer,
                "speak_text": robot_result["speak_text"],
                "llm_intent": {},
                "qwen_followup": qwen_followup_result,
                "decision_path": build_decision_path(plan, {}, risk_level, ["Qwen动态追问：需要补充信息"]),
                "location": location,
                "registration_steps": registration_steps,
                "handoff": handoff,
                "business_guard": business_guard
            }

    llm_intent = llm_intent_tool(question)
    tool_results.append({
        "tool": "llm_intent_tool",
        "result": llm_intent
    })

    # 1. 风险判断
    if "risk_triage_tool" in plan["tools"] and not risk_checked:
        risk_result = risk_triage_tool(question)

        # 兼容旧规则文件的编码问题：规则规划或 LLM 已识别急症时，强制走急诊保护。
        if plan.get("intent") == "emergency_triage" or llm_intent.get("risk_level") == "emergency":
            risk_result = {
                "risk_level": "emergency",
                "reason": "用户描述包含胸痛、呼吸困难或其他高风险症状。",
                "action": "建议立即前往急诊科或拨打 120，并尽快联系现场医护人员。"
            }

        tool_results.append({
            "tool": "risk_triage_tool",
            "result": risk_result
        })

        risk_level = risk_result["risk_level"]

        if risk_level == "emergency":
            recommended_department = "急诊科"
            department_confidence = "high"
            location = hospital_map_tool(recommended_department)
            registration_steps = registration_guide_tool(recommended_department)
            log_result = high_risk_log_tool(
                question=question,
                risk_level=risk_level,
                reason=risk_result.get("reason", ""),
                action=risk_result.get("action", "")
            )
            handoff = human_handoff_tool(question, risk_level, recommended_department, llm_intent)

            tool_results.extend([
                {"tool": "hospital_map_tool", "result": location},
                {"tool": "registration_guide_tool", "result": registration_steps},
                {"tool": "high_risk_log_tool", "result": log_result},
                {"tool": "human_handoff_tool", "result": handoff}
            ])
            decision_steps.extend([
                "高风险日志：已记录",
                "人工转接：建议"
            ])

            answer = (
                risk_result["action"]
                + " 本系统仅提供导诊和健康科普参考，不能替代医生诊断。"
            )
            robot_result = robot_response_tool(answer)

            return {
                "type": "emergency",
                "question": question,
                "answer": answer,
                "risk_level": risk_level,
                "recommended_department": recommended_department,
                "confidence": department_confidence,
                "need_followup": False,
                "follow_up_questions": [],
                "tools_used": [
                    "business_guard_tool",
                    "llm_intent_tool",
                    "risk_triage_tool",
                    "hospital_map_tool",
                    "registration_guide_tool",
                    "high_risk_log_tool",
                    "human_handoff_tool"
                ],
                "tool_results": tool_results,
                "sources": [],
                "source_details": [],
                "display_text": robot_result["display_text"],
                "speak_text": robot_result["speak_text"],
                "llm_intent": llm_intent,
                "decision_path": build_decision_path(plan, llm_intent, risk_level, decision_steps),
                "location": location,
                "registration_steps": registration_steps,
                "handoff": handoff,
                "business_guard": business_guard
            }

    # 2. 诊断、用药、治疗类问题交给医生或导诊台
    if llm_intent.get("intent") in SAFE_HANDOFF_INTENTS:
        answer = "当前系统不能提供诊断、开药或治疗方案，建议咨询医生或医院导诊台。"
        handoff = human_handoff_tool(question, risk_level, "", llm_intent)
        tool_results.append({"tool": "human_handoff_tool", "result": handoff})
        robot_result = robot_response_tool(answer)

        return {
            "type": "safe_handoff",
            "question": question,
            "answer": answer,
            "risk_level": risk_level,
            "recommended_department": "",
            "confidence": "",
            "need_followup": False,
            "follow_up_questions": [],
            "tools_used": ["business_guard_tool", "llm_intent_tool", "human_handoff_tool"],
            "tool_results": tool_results,
            "sources": [],
            "source_details": [],
            "display_text": robot_result["display_text"],
            "speak_text": robot_result["speak_text"],
            "llm_intent": llm_intent,
            "decision_path": build_decision_path(plan, llm_intent, risk_level, ["人工转接：建议"]),
            "location": {},
            "registration_steps": {},
            "handoff": handoff,
            "business_guard": business_guard
        }

    # 3. 科室推荐：规则优先，Qwen 兜底
    if "department_router_tool" in plan["tools"]:
        department_result = department_router_tool(question)
        recommended_department = department_result["department"]
        department_confidence = department_result.get("confidence", "")

        tool_results.append({
            "tool": "department_router_tool",
            "result": department_result
        })

        if (
            department_result.get("matched_type") == "fallback"
            or department_result.get("confidence") == "low"
        ):
            decision_steps.append("规则科室推荐：fallback")

            llm_department_result = department_llm_classifier_tool(
                question,
                llm_intent,
                department_result
            )
            recommended_department = llm_department_result["department"]
            department_confidence = llm_department_result.get("confidence", "low")
            decision_steps.append(f"Qwen兜底科室分类：{recommended_department}")

            tool_results.append({
                "tool": "department_llm_classifier_tool",
                "result": llm_department_result
            })
        else:
            decision_steps.append(f"规则科室推荐：{recommended_department}")

    # 4. 科室位置、挂号流程、人工转接建议
    if recommended_department:
        location = hospital_map_tool(recommended_department)
        registration_steps = registration_guide_tool(recommended_department)
        handoff = human_handoff_tool(question, risk_level, recommended_department, llm_intent)
        decision_steps.extend([
            "科室位置：已查询",
            "挂号流程：已生成",
            f"人工转接：{'建议' if handoff['need_handoff'] else '暂不需要'}"
        ])

        tool_results.extend([
            {"tool": "hospital_map_tool", "result": location},
            {"tool": "registration_guide_tool", "result": registration_steps},
            {"tool": "human_handoff_tool", "result": handoff}
        ])

    # 5. 信息完整性检查
    follow_up_questions = []
    need_followup = False
    if "slot_check_tool" in plan["tools"] and not slot_checked:
        slot_result = slot_check_tool(question)

        tool_results.append({
            "tool": "slot_check_tool",
            "result": slot_result
        })

        if not slot_result["complete"]:
            need_followup = True
            follow_up_questions = slot_result["follow_up_questions"]

    # 6. 体检指标解释
    if "lab_report_tool" in plan["tools"]:
        lab_result = lab_report_tool(question)

        tool_results.append({
            "tool": "lab_report_tool",
            "result": lab_result
        })

    # 7. 就诊准备建议
    if "visit_prepare_tool" in plan["tools"]:
        prepare_result = visit_prepare_tool(recommended_department)

        tool_results.append({
            "tool": "visit_prepare_tool",
            "result": prepare_result
        })

    # 8. RAG 检索
    if "medical_rag_tool" in plan["tools"] and not need_followup:
        from tools.medical_rag_tool import medical_rag_tool

        rag_result = medical_rag_tool(question, top_k=3)

        rag_context = rag_result["context"]
        sources = rag_result["sources"]

        tool_results.append({
            "tool": "medical_rag_tool",
            "result": {
                "sources": sources
            }
        })

    if need_followup:
        answer = "为了更准确地给出导诊参考，请补充以下信息。"
    else:
        answer = run_final_answer_chain(
            question=question,
            plan=plan,
            tool_results=tool_results,
            rag_context=rag_context
        )
        if not answer or not answer.strip():
            answer = (
                f"根据当前信息，建议优先考虑{recommended_department or '全科医学科或导诊台'}就诊。"
                "请按医院现场导诊和医生判断为准。本系统仅提供导诊和健康科普参考，不能替代医生诊断。"
            )

    robot_result = robot_response_tool(answer)

    if client_type == "robot":
        display_text = robot_result["display_text"]
        speak_text = robot_result["speak_text"]
    else:
        display_text = answer
        speak_text = robot_result["speak_text"]

    return {
        "type": "follow_up" if need_followup else "final_answer",
        "question": question,
        "answer": answer,
        "risk_level": risk_level,
        "recommended_department": recommended_department,
        "preliminary_department": qwen_followup_result.get("preliminary_department", ""),
        "confidence": department_confidence,
        "need_followup": need_followup,
        "follow_up_questions": follow_up_questions,
        "tools_used": ["business_guard_tool", "llm_intent_tool"] + plan["tools"],
        "tool_results": tool_results,
        "sources": sources,
        "source_details": sources,
        "display_text": display_text,
        "speak_text": speak_text,
        "llm_intent": llm_intent,
        "qwen_followup": qwen_followup_result,
        "decision_path": build_decision_path(plan, llm_intent, risk_level, decision_steps),
        "location": location,
        "registration_steps": registration_steps,
        "handoff": handoff,
        "business_guard": business_guard
    }
