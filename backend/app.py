from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / "project_config" / ".env")
import traceback
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_core.chat_schema import normalize_chat_result
from agent_core.medical_graph import run_medical_graph
from agent_core.lab_report_vision import analyze_lab_report_image, interpret_confirmed_indicators

app = FastAPI(title="医疗导诊 Agent 系统")
followup_sessions = {}
SESSION_STORE = followup_sessions
LOCAL_FRONTEND_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=LOCAL_FRONTEND_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    client_type: str = "web"
    session_id: str | None = None
    original_query: str = ""
    followup_answer: str = ""
    initial_department: str = ""
    followup_done: bool = False


class RobotChatRequest(BaseModel):
    text: str
    terminal_id: str = "robot_001"
    location: str = "门诊大厅"


class LabReportAnalyzeRequest(BaseModel):
    image_data_url: str


class LabReportInterpretRequest(BaseModel):
    report_type: str = "化验单"
    indicators: list[dict]


@app.get("/")
def home():
    return {
        "message": "医疗导诊 Agent 系统启动成功"
    }


@app.post("/build")
def build():
    """
    构建医疗知识库。
    第一次运行项目，或修改 data/docs 文档后调用。
    """
    from rag.build_vector_db import build_vector_db

    result = build_vector_db()

    return {
        "message": result
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())

        session = SESSION_STORE.get(session_id, {
            "history": [],
            "pending_followup": False,
            "last_medical_question": "",
            "missing_info": [],
            "followup_count": 0,
            "initial_department": "",
            "last_preliminary_result": {}
        })

        pending_followup = session.get("pending_followup") is True
        last_question = session.get("last_medical_question", "")

        followup_done = request.followup_done or pending_followup
        original_query = request.original_query or last_question or request.question

        followup_answer = request.followup_answer
        if followup_done and not followup_answer:
            followup_answer = request.question

        initial_department = (
            request.initial_department
            or session.get("initial_department", "")
            or session.get("last_preliminary_result", {}).get("canonical_department", "")
            or session.get("last_preliminary_result", {}).get("recommended_department", "")
            or session.get("last_preliminary_result", {}).get("department", "")
        )

        if followup_done and original_query:
            full_question = f"{original_query}\n补充信息：{followup_answer or request.question}"
        else:
            full_question = request.question

        session_state = {
            **session,
            "session_id": session_id,
            "current_question": request.question,
            "full_question": full_question,
            "original_query": original_query,
            "followup_answer": followup_answer,
            "initial_department": initial_department,
            "followup_done": followup_done,
        }

        result = run_medical_graph(
            question=full_question,
            client_type=request.client_type,
            session_state=session_state
        )

        result["session_id"] = session_id

        if followup_done or session.get("followup_count", 0) >= 1:
            result["need_followup"] = False
            result["follow_up_questions"] = []
            result["followup_questions"] = []
            result["follow_up_items"] = []
            result["followup_items"] = []
            result["type"] = "medical"

        result = normalize_chat_result(
            result,
            full_question,
            initial_department=initial_department,
            followup_done=followup_done,
        )
        result.setdefault("symptom_summary", "")
        result.setdefault("possible_conditions", [])
        result.setdefault("canonical_department", result.get("department", ""))
        result.setdefault("risk_level", "low")
        result.setdefault("confidence", 0.45)
        result.setdefault("red_flags", [])
        result.setdefault("reason", "")
        result.setdefault("analysis", result.get("answer", ""))
        result.setdefault("follow_up_items", result.get("followup_items", []))
        result.setdefault("department_location", result.get("location", {}))
        result.setdefault("doctors", result.get("recommended_doctors", []))
        result["explain_chain"] = result.get("explain_chain") or result.get("decision_path", [])

        history = session.get("history", [])
        history.append({
            "question": request.question,
            "full_question": full_question,
            "type": result.get("type", "")
        })

        if result.get("need_followup") is True:
            first_department = (
                result.get("canonical_department")
                or result.get("recommended_department")
                or result.get("department")
                or initial_department
            )

            SESSION_STORE[session_id] = {
                "history": history,
                "pending_followup": True,
                "last_medical_question": original_query or full_question,
                "missing_info": result.get("qwen_followup", {}).get("missing_info", []),
                "followup_count": session.get("followup_count", 0) + 1,
                "initial_department": first_department,
                "last_preliminary_result": {
                    **(result.get("qwen_followup", {}) or {}),
                    "canonical_department": first_department,
                    "recommended_department": first_department,
                    "department": first_department,
                }
            }
        else:
            result["final_answer"] = result.get("answer") or result.get("display_text") or ""

            SESSION_STORE[session_id] = {
                "history": history,
                "pending_followup": False,
                "last_medical_question": full_question,
                "missing_info": [],
                "followup_count": 0,
                "initial_department": result.get("canonical_department") or result.get("department") or initial_department,
                "last_preliminary_result": result.get("qwen_followup", {})
            }

        return result

    except Exception as e:
        traceback.print_exc()
        return {
            "error": "服务暂时不可用，请稍后重试。",
            "traceback": ""
        }


@app.post("/lab-report/analyze")
def analyze_lab_report(request: LabReportAnalyzeRequest):
    try:
        return analyze_lab_report_image(request.image_data_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=502, detail="化验单识别服务暂时不可用，请稍后重试。") from exc


@app.post("/lab-report/interpret")
def interpret_lab_report(request: LabReportInterpretRequest):
    try:
        return interpret_confirmed_indicators(request.report_type, request.indicators)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=502, detail="化验单解读服务暂时不可用，请稍后重试。") from exc


@app.post("/robot/chat")
def robot_chat(request: RobotChatRequest):
    try:
        result = run_medical_graph(
            question=request.text,
            client_type="robot"
        )

        return {
            "terminal_id": request.terminal_id,
            "location": request.location,
            "risk_level": result["risk_level"],
            "recommended_department": result["recommended_department"],
            "need_followup": result["need_followup"],
            "follow_up_questions": result["follow_up_questions"],
            "speak_text": result["speak_text"],
            "display_text": result["display_text"],
            "tools_used": result["tools_used"],
            "sources": result["sources"]
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "error": "服务暂时不可用，请稍后重试。",
            "traceback": ""
        }


@app.get("/tools")
def get_tools():
    return {
        "tools": [
            "risk_triage_tool",
            "slot_check_tool",
            "department_router_tool",
            "lab_report_tool",
            "visit_prepare_tool",
            "robot_response_tool",
            "medical_rag_tool",
            "llm_intent_tool",
            "department_llm_classifier_tool",
            "hospital_map_tool",
            "registration_guide_tool",
            "human_handoff_tool",
            "high_risk_log_tool",
            "business_guard_tool",
            "qwen_followup_tool",
            "langchain_chains",
            "langgraph_medical_graph"
        ]
    }
