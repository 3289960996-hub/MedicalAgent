import json
import re
from typing import TypedDict, Any
from importlib import import_module

from langgraph.graph import StateGraph, START, END


class MedicalAgentState(TypedDict, total=False):
    question: str
    client_type: str

    answer: str
    risk_level: str
    recommended_department: str
    confidence: str
    canonical_department: str

    business_guard: dict
    llm_intent: dict
    qwen_followup: dict
    triage_analysis: dict
    normalized_symptom: dict
    location: dict
    registration_steps: list
    handoff: dict

    rag_context: str
    sources: list
    source_details: list

    need_followup: bool
    follow_up_questions: list
    follow_up_items: list

    tools_used: list
    tool_results: list
    decision_path: list

    display_text: str
    speak_text: str
    analysis: str
    guide: str
    visit_guide: str
    department_location: dict
    doctors: list
    recommended_doctors: list
    department: str
    followup_questions: list
    followup_items: list
    symptom_summary: str
    possible_conditions: list
    red_flags: list
    reason: str


def get_func(module_path: str, func_name: str):
    try:
        module = import_module(module_path)
        return getattr(module, func_name)
    except Exception as e:
        print(f"[工具加载失败] {module_path}.{func_name}: {e}")
        return None


business_guard_tool = get_func("tools.business_guard_tool", "business_guard_tool")
risk_triage_tool = get_func("tools.risk_triage_tool", "risk_triage_tool")
department_router_tool = get_func("tools.department_router_tool", "department_router_tool")
registration_guide_tool = get_func("tools.registration_guide_tool", "registration_guide_tool")
medical_rag_tool = get_func("tools.medical_rag_tool", "medical_rag_tool")
human_handoff_tool = get_func("tools.human_handoff_tool", "human_handoff_tool")
robot_response_tool = get_func("tools.robot_response_tool", "robot_response_tool")
high_risk_log_tool = get_func("tools.high_risk_log_tool", "high_risk_log_tool")
run_triage_analysis_chain = get_func("agent_core.langchain_chains", "run_triage_analysis_chain")


FALLBACK_DEPARTMENT_LOCATION_MAP = {
    "急诊科": {"floor": "1F", "area": "急诊分诊区", "room": "急诊楼 1F", "description": "急诊楼 1F 急诊分诊区"},
    "发热门诊": {"floor": "1F", "area": "发热门诊区", "room": "门诊楼 1F", "description": "门诊楼 1F 发热门诊区"},
    "全科医学科": {"floor": "2F", "area": "A区", "room": "201-205 诊室", "description": "门诊楼 2F A区 201-205 诊室"},
    "儿科": {"floor": "2F", "area": "儿童诊区", "room": "206-210 诊室", "description": "门诊楼 2F 儿童诊区 206-210 诊室"},
    "口腔科": {"floor": "2F", "area": "D区", "room": "211-216 诊室", "description": "门诊楼 2F D区 211-216 诊室"},
    "肛肠科": {"floor": "2F", "area": "E区", "room": "217-220 诊室", "description": "门诊楼 2F E区 217-220 诊室"},
    "普外科": {"floor": "2F", "area": "F区", "room": "221-224 诊室", "description": "门诊楼 2F F区 221-224 诊室"},
    "呼吸内科": {"floor": "3F", "area": "B区", "room": "301-306 诊室", "description": "门诊楼 3F B区 301-306 诊室"},
    "消化内科": {"floor": "3F", "area": "C区", "room": "307-312 诊室", "description": "门诊楼 3F C区 307-312 诊室"},
    "耳鼻喉科": {"floor": "3F", "area": "D区", "room": "313-318 诊室", "description": "门诊楼 3F D区 313-318 诊室"},
    "眼科": {"floor": "3F", "area": "E区", "room": "319-324 诊室", "description": "门诊楼 3F E区 319-324 诊室"},
    "感染科/发热门诊": {"floor": "1F", "area": "发热门诊区", "room": "门诊楼 1F 感染科/发热门诊", "description": "门诊楼 1F 发热门诊区 感染科/发热门诊"},
    "感染科": {"floor": "1F", "area": "发热门诊区", "room": "门诊楼 1F 感染科/发热门诊", "description": "门诊楼 1F 发热门诊区 感染科/发热门诊"},
    "心内科": {"floor": "4F", "area": "A区", "room": "401-406 诊室", "description": "门诊楼 4F A区 401-406 诊室"},
    "神经内科": {"floor": "4F", "area": "B区", "room": "407-412 诊室", "description": "门诊楼 4F B区 407-412 诊室"},
    "内分泌科": {"floor": "4F", "area": "C区", "room": "413-418 诊室", "description": "门诊楼 4F C区 413-418 诊室"},
    "泌尿外科": {"floor": "4F", "area": "D区", "room": "419-424 诊室", "description": "门诊楼 4F D区 419-424 诊室"},
    "妇科": {"floor": "4F", "area": "E区", "room": "425-430 诊室", "description": "门诊楼 4F E区 425-430 诊室"},
    "乳腺外科": {"floor": "4F", "area": "F区", "room": "431-434 诊室", "description": "门诊楼 4F F区 431-434 诊室"},
    "骨科": {"floor": "5F", "area": "A区", "room": "501-506 诊室", "description": "门诊楼 5F A区 501-506 诊室"},
    "皮肤科": {"floor": "5F", "area": "C区", "room": "507-512 诊室", "description": "门诊楼 5F C区 507-512 诊室"},
    "风湿免疫科": {"floor": "5F", "area": "D区", "room": "513-516 诊室", "description": "门诊楼 5F D区 513-516 诊室"},
    "康复医学科": {"floor": "5F", "area": "康复治疗区", "room": "517-520 诊室", "description": "门诊楼 5F 康复治疗区 517-520 诊室"},
    "精神心理科": {"floor": "5F", "area": "E区", "room": "521-524 诊室", "description": "门诊楼 5F E区 521-524 诊室"},
    "导诊台": {"floor": "1F", "area": "门诊大厅", "room": "门诊大厅", "description": "门诊楼 1F 门诊大厅导诊台"},
    "全科/急诊": {"floor": "1F", "area": "急诊分诊区", "room": "急诊楼 1F", "description": "急诊楼 1F 急诊分诊区"},
    "急诊科/转人工": {"floor": "1F", "area": "急诊分诊区", "room": "急诊楼 1F", "description": "急诊楼 1F 急诊分诊区"},
    "全科": {"floor": "2F", "area": "A区", "room": "201-205 诊室", "description": "门诊楼 2F A区 201-205 诊室"},
    "全科医学科或导诊台": {"floor": "2F", "area": "A区", "room": "201-205 诊室", "description": "门诊楼 2F A区 201-205 诊室"},
}

RED_FLAG_KEYWORDS = [
    "呼吸困难", "喘不上气", "意识异常", "意识模糊", "大量出血", "大量便血",
    "剧烈胸痛", "胸口剧烈疼", "胸口剧烈痛", "胸部剧烈疼", "胸部剧烈痛",
    "严重外伤", "持续高热", "迅速加重", "无法行走", "明显畸形"
]


def canonicalize_department(
    department: str,
    question: str = "",
    risk_level: str = "",
    allow_question_fallback: bool = False
) -> str:
    dept = str(department or "").strip()
    if "感染科" in dept or "发热门诊" in dept:
        return "感染科/发热门诊"
    standard_departments = [
        "口腔科", "眼科", "皮肤科", "呼吸内科", "消化内科", "泌尿外科",
        "耳鼻喉科", "骨科", "神经内科", "心内科", "儿科", "妇科", "内分泌科",
        "肛肠科", "普外科", "风湿免疫科", "康复医学科", "精神心理科",
        "感染科/发热门诊", "乳腺外科", "急诊科"
    ]
    for standard in standard_departments:
        if standard in dept:
            return standard
    if "急诊" in dept and risk_level == "high":
        return "急诊科"
    text = str(question or "")
    if any(keyword in text for keyword in RED_FLAG_KEYWORDS):
        return "急诊科"
    if not allow_question_fallback:
        if dept in {"全科", "全科医学科", "导诊台", "全科医学科或导诊台"}:
            return "全科"
        return "全科"
    if any(keyword in text for keyword in ["痔疮", "肛门疼", "肛门痛", "肛门瘙痒", "便血", "肛裂", "肛周肿痛"]):
        return "肛肠科"
    if any(keyword in text for keyword in ["伤口", "体表包块", "疝气", "脓肿", "皮下肿块", "外科换药"]):
        return "普外科"
    if any(keyword in text for keyword in ["尿痛", "尿频", "尿急", "血尿", "排尿困难", "尿不尽"]):
        return "泌尿外科"
    if any(keyword in text for keyword in ["月经不调", "痛经", "白带异常", "阴道出血", "外阴瘙痒"]):
        return "妇科"
    if any(keyword in text for keyword in ["儿童", "孩子", "小孩", "宝宝", "婴儿", "幼儿"]):
        return "儿科"
    if any(keyword in text for keyword in ["头痛", "头晕", "眩晕", "手脚麻木", "手麻", "脚麻", "肢体无力", "说话不清", "面瘫", "抽搐"]):
        return "神经内科"
    if any(keyword in text for keyword in ["胸痛", "胸闷", "心慌", "心悸", "心跳快", "血压高"]):
        return "心内科"
    if any(keyword in text for keyword in ["糖尿病", "血糖高", "甲亢", "甲减", "甲状腺", "肥胖", "多饮多尿"]):
        return "内分泌科"
    if any(keyword in text for keyword in ["关节肿痛", "多关节痛", "晨僵", "风湿", "类风湿", "痛风", "尿酸高"]):
        return "风湿免疫科"
    if any(keyword in text for keyword in ["术后康复", "运动康复", "腰腿康复", "偏瘫康复", "功能恢复"]):
        return "康复医学科"
    if any(keyword in text for keyword in ["焦虑", "抑郁", "失眠", "情绪低落", "压力大", "睡不着"]):
        return "精神心理科"
    if any(keyword in text for keyword in ["持续高热", "发热伴皮疹", "疑似传染病", "近期接触感染患者"]):
        return "感染科/发热门诊"
    if any(keyword in text for keyword in ["乳房疼", "乳房痛", "乳房肿块", "乳头溢液", "乳腺结节", "乳房红肿"]):
        return "乳腺外科"
    if any(keyword in text for keyword in ["牙疼", "牙痛", "牙龈", "口腔", "面部肿胀", "脸肿"]):
        return "口腔科"
    if "眼" in text:
        return "眼科"
    if any(keyword in text for keyword in ["皮肤", "皮疹", "红疹", "瘙痒", "皮肤痒", "痒痒", "起疹", "起红疹", "过敏"]):
        return "皮肤科"
    if any(keyword in text for keyword in ["呼吸", "咳嗽", "发热", "发烧", "咽痛"]):
        return "呼吸内科"
    if any(keyword in text for keyword in ["胃", "腹", "肚子", "腹泻", "恶心", "呕吐"]):
        return "消化内科"
    if any(keyword in text for keyword in ["尿", "小便", "泌尿"]):
        return "泌尿外科"
    if dept in {"全科", "全科医学科", "导诊台", "全科医学科或导诊台"}:
        return "全科"
    return "全科"


def normalize_risk_level(value: str | None) -> str:
    text = str(value or "").strip().lower()
    if text in {"high", "emergency", "urgent", "急诊", "高"}:
        return "high"
    if text in {"medium", "moderate", "中", "尽快"}:
        return "medium"
    return "low"


def normalize_confidence(value, matched_type: str = "") -> float:
    text = str(value or "").strip().lower()
    try:
        numeric = float(text)
        if numeric <= 1:
            return round(numeric, 2)
    except Exception:
        pass
    if text in {"high", "高", "较高"} or matched_type == "rule":
        return 0.85
    if text in {"medium", "moderate", "中", "中等"}:
        return 0.65
    return 0.45


def is_low_confidence(confidence) -> bool:
    if confidence is None:
        return True
    if isinstance(confidence, (int, float)):
        return confidence <= 0.5

    text = str(confidence).strip().lower()
    if not text:
        return True
    if text in {"low", "低"}:
        return True
    if text in {"high", "medium", "moderate"}:
        return False

    try:
        return float(text) <= 0.5
    except Exception:
        return True


def fallback_department_location(department: str) -> dict:
    department = canonicalize_department(department)
    department = (department or "").strip()
    if department in FALLBACK_DEPARTMENT_LOCATION_MAP:
        return FALLBACK_DEPARTMENT_LOCATION_MAP[department]
    for key, value in FALLBACK_DEPARTMENT_LOCATION_MAP.items():
        if key in department:
            return value
    return FALLBACK_DEPARTMENT_LOCATION_MAP["全科/急诊"]


def query_department_location_from_db(department: str) -> dict | None:
    try:
        from db import SessionLocal
        from models import DepartmentLocation

        canonical = canonicalize_department(department)
        with SessionLocal() as db:
            location = (
                db.query(DepartmentLocation)
                .filter(DepartmentLocation.department == canonical)
                .first()
            )
            if not location:
                location = (
                    db.query(DepartmentLocation)
                    .filter(DepartmentLocation.department.like(f"%{canonical}%"))
                    .first()
                )
            if not location:
                return None
            return {
                "floor": location.floor or "",
                "area": location.area or "",
                "room": location.room or "",
                "description": location.description or "",
            }
    except Exception:
        return None


def get_department_location(department: str) -> dict:
    return query_department_location_from_db(department) or fallback_department_location(department)


def build_visit_guide(department: str, risk_level: str = "") -> str:
    risk_level = normalize_risk_level(risk_level)
    location = get_department_location(department)
    soon = "建议急诊/转人工" if risk_level == "high" else "建议尽快就诊" if risk_level == "medium" else "普通门诊"
    return (
        f"科室位置：{location.get('description', '暂无科室位置信息')}\n"
        "挂号流程：导诊台确认 → 挂号/缴费 → 前往对应楼层 → 等候叫号\n"
        f"是否建议尽快就诊：{soon}"
    )


def add_path(state: MedicalAgentState, text: str) -> list:
    return state.get("decision_path", []) + [text]


def add_tool(state: MedicalAgentState, tool_name: str, result: Any) -> tuple[list, list]:
    tools_used = state.get("tools_used", []) + [tool_name]
    tool_results = state.get("tool_results", []) + [
        {
             "tool": tool_name,
            "result": result
        }
    ]
    return tools_used, tool_results


def clean_json_text(text: str) -> str:
    cleaned = str(text or "").strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start:end + 1]
    return cleaned


def safe_str_list(value) -> list:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def safe_followup_items(value) -> list:
    items = []
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            question = str(item.get("question") or item.get("text") or "").strip()
            if not question:
                continue
            options = safe_str_list(item.get("options"))[:6]
            if len(options) < 2:
                continue
            items.append({"question": question, "options": options})
    return items[:3]


def is_vague_or_no_symptom(question: str) -> bool:
    text = re.sub(r"\s+", "", str(question or ""))
    if not text:
        return True
    vague_phrases = {
        "我没事",
        "没事",
        "没有不舒服",
        "无不适",
        "没不舒服",
        "不知道",
        "随便看看",
        "咨询一下",
    }
    if text in vague_phrases:
        return True
    symptom_hints = [
        "痛", "疼", "痒", "咳", "烧", "热", "吐", "泻", "晕", "麻", "肿", "血",
        "胸闷", "气短", "恶心", "鼻塞", "流涕", "皮疹", "红疹", "腹", "头", "嗓子",
        "发热", "乏力", "心慌", "失眠", "外伤", "摔", "扭"
    ]
    return len(text) < 4 and not any(hint in text for hint in symptom_hints)


def has_red_flag(question: str) -> bool:
    return any(keyword in str(question or "") for keyword in RED_FLAG_KEYWORDS)



def fallback_doctors_by_department(department: str) -> list:
    """Return fallback doctors list for a given department."""
    department = (department or "").strip() or "全科/急诊"
    doc_db = {
        "耳鼻喉科": [
            {"name": "张伟华", "title": "主任医师", "department": "耳鼻喉科", "specialty": "耳科常见疾病", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 5},
            {"name": "李敏", "title": "副主任医师", "department": "耳鼻喉科", "specialty": "鼻科疾病", "available": True, "time": "周一/三/五 14:00-17:00", "fee": "30元", "slots": 8},
            {"name": "王磊", "title": "主治医师", "department": "耳鼻喉科", "specialty": "喉哑症", "available": True, "time": "周二/四 14:00-17:00", "fee": "20元", "slots": 12},
        ],
        "眼科": [
            {"name": "赵明", "title": "主任医师", "department": "眼科", "specialty": "白内障手术", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 3},
            {"name": "孙丽", "title": "副主任医师", "department": "眼科", "specialty": "视网膜疾病", "available": True, "time": "周一/三/五 14:00-17:00", "fee": "30元", "slots": 6},
        ],
        "急诊科": [
            {"name": "急诊值班医生", "title": "24小时急诊", "department": "急诊科", "specialty": "急性療法", "available": True, "time": "全天24小时", "fee": "—", "slots": 99},
        ],
        "口腔科": [
            {"name": "周宁", "title": "副主任医师", "department": "口腔科", "specialty": "牙痛、牙龈肿痛", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 6},
            {"name": "何洁", "title": "主治医师", "department": "口腔科", "specialty": "口腔常见病", "available": True, "time": "周一/三/五 14:00-17:00", "fee": "20元", "slots": 9},
        ],
        "内科": [
            {"name": "赵国强", "title": "主任医师", "department": "内科", "specialty": "消化系统疾病", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 4},
            {"name": "黄文华", "title": "副主任医师", "department": "内科", "specialty": "呼吸系统疾病", "available": True, "time": "周一/三/五 14:00-17:00", "fee": "30元", "slots": 7},
        ],
        "骨科": [
            {"name": "张明辉", "title": "主任医师", "department": "骨科", "specialty": "骨关节扭伤", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 4},
        ],
        "皮肤科": [
            {"name": "沈红", "title": "主任医师", "department": "皮肤科", "specialty": "湿疹瘙痒", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 5},
        ],
        "肛肠科": [
            {"name": "郑肛宁", "title": "副主任医师", "department": "肛肠科", "specialty": "痔疮、便血、肛裂", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 8},
        ],
        "普外科": [
            {"name": "刘建平", "title": "主任医师", "department": "普外科", "specialty": "伤口、包块、疝气", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 6},
        ],
        "泌尿外科": [
            {"name": "吴泌", "title": "副主任医师", "department": "泌尿外科", "specialty": "尿频尿痛、血尿", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 7},
        ],
        "妇科": [
            {"name": "林芳", "title": "副主任医师", "department": "妇科", "specialty": "月经不调、白带异常", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 9},
        ],
        "儿科": [
            {"name": "周童", "title": "主任医师", "department": "儿科", "specialty": "儿童发热、咳嗽", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 10},
        ],
        "神经内科": [
            {"name": "陈明远", "title": "副主任医师", "department": "神经内科", "specialty": "头晕头痛、肢体麻木", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 7},
        ],
        "心内科": [
            {"name": "胡心安", "title": "主任医师", "department": "心内科", "specialty": "胸闷心慌、高血压", "available": True, "time": "周一至周五 08:00-12:00", "fee": "50元", "slots": 6},
        ],
        "内分泌科": [
            {"name": "唐泌", "title": "副主任医师", "department": "内分泌科", "specialty": "血糖、甲状腺", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 8},
        ],
        "风湿免疫科": [
            {"name": "高免", "title": "副主任医师", "department": "风湿免疫科", "specialty": "痛风、关节肿痛", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 7},
        ],
        "康复医学科": [
            {"name": "梁康复", "title": "主治医师", "department": "康复医学科", "specialty": "术后康复、功能恢复", "available": True, "time": "周一至周五 08:00-12:00", "fee": "20元", "slots": 8},
        ],
        "精神心理科": [
            {"name": "许安然", "title": "副主任医师", "department": "精神心理科", "specialty": "焦虑、抑郁、失眠", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 6},
        ],
        "感染科/发热门诊": [
            {"name": "韩感染", "title": "副主任医师", "department": "感染科/发热门诊", "specialty": "发热、感染相关症状", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 12},
        ],
        "乳腺外科": [
            {"name": "秦乳宁", "title": "副主任医师", "department": "乳腺外科", "specialty": "乳房肿块、乳腺结节", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 6},
        ],
    }
    if department in doc_db:
        return doc_db[department]
    for key, doctors in doc_db.items():
        if key in department:
            return doctors
    return [
        {"name": "刘医生", "title": "副主任医师", "department": department, "specialty": "常见疾病诊治", "available": True, "time": "周一至周五 08:00-12:00", "fee": "30元", "slots": 8},
        {"name": "陈医生", "title": "主治医师", "department": department, "specialty": "全科诊疗", "available": True, "time": "周一/三/五 14:00-17:00", "fee": "20元", "slots": 10},
    ]


def query_doctors_from_db(department: str) -> list:
    try:
        from db import SessionLocal
        from models import Doctor

        canonical = canonicalize_department(department)
        with SessionLocal() as db:
            doctors = (
                db.query(Doctor)
                .filter(Doctor.department == canonical)
                .order_by(Doctor.id.asc())
                .limit(3)
                .all()
            )
            if not doctors:
                doctors = (
                    db.query(Doctor)
                    .filter(Doctor.department.like(f"%{canonical}%"))
                    .order_by(Doctor.id.asc())
                    .limit(3)
                    .all()
                )
            return [
                {
                    "name": doctor.name,
                    "title": doctor.title,
                    "department": doctor.department,
                    "specialty": doctor.specialty,
                    "available": bool(doctor.available),
                    "time": doctor.time,
                    "fee": doctor.fee,
                    "slots": doctor.slots,
                }
                for doctor in doctors
            ]
    except Exception:
        return []


def doctors_by_department(department: str) -> list:
    return query_doctors_from_db(department) or fallback_doctors_by_department(department)


mock_doctors_by_department = fallback_doctors_by_department


def query_symptom_department_rule_from_db(question: str) -> dict | None:
    try:
        from db import SessionLocal
        from models import SymptomDepartmentRule

        with SessionLocal() as db:
            rules = (
                db.query(SymptomDepartmentRule)
                .filter(SymptomDepartmentRule.is_active.is_(True))
                .order_by(SymptomDepartmentRule.priority.asc(), SymptomDepartmentRule.id.asc())
                .all()
            )
            for rule in rules:
                keywords = [
                    keyword.strip()
                    for keyword in str(rule.keywords or "").split(",")
                    if keyword.strip()
                ]
                if any(keyword in question for keyword in keywords):
                    return {
                        "department": rule.department,
                        "reason": rule.reason,
                        "matched_type": rule.matched_type or "rule",
                        "confidence": rule.confidence or "medium",
                    }
    except Exception:
        return None
    return None

def business_guard_node(state: MedicalAgentState) -> MedicalAgentState:
    question = state.get("question", "")

    if business_guard_tool:
        result = business_guard_tool(question)
    else:
        result = {
            "blocked": False,
            "reason": "",
            "message": ""
        }

    tools_used, tool_results = add_tool(state, "business_guard_tool", result)

    return {
        "business_guard": result,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "业务拦截检查完成")
    }


def risk_triage_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "risk_level": "low",
            "decision_path": add_path(state, "业务已拦截，跳过风险分级")
        }

    question = state.get("question", "")

    if risk_triage_tool:
        result = risk_triage_tool(question)
    else:
        result = {
            "risk_level": "low",
            "reason": "未加载风险分级工具",
            "action": ""
        }

    risk_level = "high" if has_red_flag(question) else normalize_risk_level(result.get("risk_level", "low"))

    tools_used, tool_results = add_tool(state, "risk_triage_tool", result)

    update: MedicalAgentState = {
        "risk_level": risk_level,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, f"风险分级完成：{risk_level}")
    }

    if risk_level == "high":
        update["recommended_department"] = "急诊科"
        update["canonical_department"] = "急诊科"

        if high_risk_log_tool:
            log_result = high_risk_log_tool(
                question=question,
                risk_level=risk_level,
                reason=result.get("reason", ""),
                action=result.get("action", "")
            )
            tools_used, tool_results = add_tool(update, "high_risk_log_tool", log_result)
            update["tools_used"] = tools_used
            update["tool_results"] = tool_results

    return update


def triage_analysis_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "triage_analysis": {},
            "decision_path": add_path(state, "业务已拦截，跳过LLM病情分析")
        }

    question = state.get("question", "")
    session_state = state.get("session_state", {}) or {}
    followup_count = session_state.get("followup_count", 0)
    previous_result = session_state.get("last_preliminary_result", {})

    data = {}
    if run_triage_analysis_chain:
        try:
            result_text = run_triage_analysis_chain(question, followup_count, previous_result)
            data = json.loads(clean_json_text(result_text))
        except Exception as exc:
            data = {
                "_internal_error": f"LLM病情分析解析失败：{exc}",
                "reason": ""
            }
    else:
        data = {
            "_internal_error": "未加载LLM病情分析链",
            "reason": ""
        }

    llm_department = data.get("canonical_department") or data.get("recommended_department") or ""
    risk_level = normalize_risk_level(data.get("risk_level") or state.get("risk_level") or "low")
    red_flags = safe_str_list(data.get("red_flags"))

    if has_red_flag(question):
        risk_level = "high"
        llm_department = "急诊科"
        red_flags = red_flags or [keyword for keyword in RED_FLAG_KEYWORDS if keyword in question]

    department = canonicalize_department(llm_department, question, risk_level) if llm_department else ""
    follow_up_items = safe_followup_items(data.get("follow_up_items") or data.get("followup_items"))
    need_followup = bool(data.get("need_followup")) and bool(follow_up_items) and followup_count < 1 and risk_level != "high"
    follow_up_questions = [item["question"] for item in follow_up_items]

    internal_error = str(data.get("_internal_error") or "").strip()

    analysis = {
        "symptom_summary": str(data.get("symptom_summary") or "").strip(),
        "possible_conditions": safe_str_list(data.get("possible_conditions")),
        "recommended_department": department or str(data.get("recommended_department") or "").strip(),
        "canonical_department": department,
        "risk_level": risk_level,
        "confidence": normalize_confidence(data.get("confidence", 0.45)),
        "red_flags": red_flags,
        "reason": str(data.get("reason") or "").strip(),
        "department_reason": str(data.get("department_reason") or "").strip(),
        "patient_explanation": str(data.get("patient_explanation") or "").strip(),
        "urgency_advice": str(data.get("urgency_advice") or "").strip(),
        "doctor_questions": safe_str_list(data.get("doctor_questions")),
        "visit_preparation": safe_str_list(data.get("visit_preparation")),
        "need_followup": need_followup,
        "follow_up_items": follow_up_items,
    }
    if internal_error:
        analysis["internal_error"] = internal_error

    tools_used, tool_results = add_tool(state, "triage_analysis_chain", analysis)

    update: MedicalAgentState = {
        "triage_analysis": analysis,
        "symptom_summary": analysis["symptom_summary"],
        "possible_conditions": analysis["possible_conditions"],
        "risk_level": risk_level,
        "confidence": analysis["confidence"],
        "red_flags": red_flags,
        "reason": analysis["reason"],
        "department_reason": analysis["department_reason"],
        "patient_explanation": analysis["patient_explanation"],
        "urgency_advice": analysis["urgency_advice"],
        "doctor_questions": analysis["doctor_questions"],
        "visit_preparation": analysis["visit_preparation"],
        "need_followup": need_followup,
        "follow_up_questions": follow_up_questions,
        "followup_questions": follow_up_questions,
        "follow_up_items": follow_up_items,
        "followup_items": follow_up_items,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "LLM病情分析完成")
    }

    if department:
        update["department"] = department
        update["recommended_department"] = department
        update["canonical_department"] = department

    return update


def department_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "recommended_department": "",
            "confidence": "",
            "decision_path": add_path(state, "业务已拦截，跳过科室推荐")
        }

    if state.get("risk_level") == "high":
        return {
            "recommended_department": "急诊科",
            "department": "急诊科",
            "canonical_department": "急诊科",
            "confidence": 0.85,
            "decision_path": add_path(state, "高风险情况，推荐急诊科")
        }

    question = state.get("question", "")
    triage_analysis = state.get("triage_analysis", {}) or {}
    llm_department = triage_analysis.get("canonical_department") or triage_analysis.get("recommended_department")
    if llm_department:
        department = canonicalize_department(llm_department, question, state.get("risk_level", "low"))
        return {
            "department": department,
            "recommended_department": department,
            "canonical_department": department,
            "confidence": normalize_confidence(triage_analysis.get("confidence", state.get("confidence", 0.45))),
            "decision_path": add_path(state, f"LLM病情分析推荐科室：{department}")
        }

    rule_result = query_symptom_department_rule_from_db(question)
    if not rule_result:
        if department_router_tool:
            rule_result = department_router_tool(question)
        else:
            rule_result = {
                "department": "全科",
                "reason": "未加载规则科室推荐工具",
                "matched_type": "fallback",
                "confidence": "low"
            }

    tools_used, tool_results = add_tool(state, "department_router_tool", rule_result)

    raw_department = rule_result.get("department", "全科")
    department = canonicalize_department(
        raw_department,
        question,
        state.get("risk_level", "low"),
        allow_question_fallback=True
    )
    raw_confidence = rule_result.get("confidence")
    confidence = normalize_confidence(raw_confidence, rule_result.get("matched_type", ""))

    decision_path = state.get("decision_path", [])

    if rule_result.get("matched_type") == "fallback" or is_low_confidence(raw_confidence):
        decision_path.append(f"LLM未返回科室，规则兜底推荐：{department}")
    else:
        decision_path.append(f"规则科室推荐：{department}")

    return {
        "department": department,
        "recommended_department": department,
        "canonical_department": department,
        "confidence": confidence,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": decision_path
    }


def hospital_map_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "location": {},
            "decision_path": add_path(state, "业务已拦截，跳过楼层位置查询")
        }

    department = canonicalize_department(
        state.get("canonical_department") or state.get("recommended_department", "") or state.get("department", ""),
        state.get("question", ""),
        state.get("risk_level", "")
    )

    result = {
        "department": department,
        **get_department_location(department)
    }

    tools_used, tool_results = add_tool(state, "hospital_map_tool", result)

    return {
        "location": result,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "楼层位置查询完成")
    }


def registration_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "registration_steps": [],
            "decision_path": add_path(state, "业务已拦截，跳过挂号流程")
        }

    department = state.get("recommended_department", "") or state.get("department", "")

    if registration_guide_tool and department:
        result = registration_guide_tool(department)
    else:
        result = {
            "department": department,
            "steps": [],
            "notice": "当前系统不提供真实号源信息，请以医院官方系统为准。"
        }

    tools_used, tool_results = add_tool(state, "registration_guide_tool", result)

    return {
        "registration_steps": result.get("steps", []),
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "挂号流程生成完成")
    }


def rag_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        return {
            "rag_context": "",
            "sources": [],
            "source_details": [],
            "decision_path": add_path(state, "业务已拦截，跳过RAG检索")
        }

    question = state.get("question", "")

    if medical_rag_tool:
        result = medical_rag_tool(question, top_k=3)
    else:
        result = {
            "context": "",
            "sources": [],
            "docs": []
        }

    docs = result.get("docs", [])
    source_details = result.get("source_details")

    if not source_details:
        source_details = [
            {
                "source": doc.get("source", ""),
                "content": doc.get("content", "")
            }
            for doc in docs
        ]

    tools_used, tool_results = add_tool(
        state,
        "medical_rag_tool",
        {
            "sources": result.get("sources", [])
        }
    )

    return {
        "rag_context": result.get("context", ""),
        "sources": result.get("sources", []),
        "source_details": source_details,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "RAG检索完成")
    }


def handoff_node(state: MedicalAgentState) -> MedicalAgentState:
    question = state.get("question", "")

    if human_handoff_tool:
        result = human_handoff_tool(
            question=question,
            risk_level=state.get("risk_level", "low"),
            recommended_department=state.get("recommended_department", ""),
            llm_intent=state.get("llm_intent", {})
        )
    else:
        result = {
            "need_handoff": False,
            "reason": "",
            "handoff_message": ""
        }

    tools_used, tool_results = add_tool(state, "human_handoff_tool", result)

    return {
        "handoff": result,
        "tools_used": tools_used,
        "tool_results": tool_results,
        "decision_path": add_path(state, "人工转接判断完成")
    }


def answer_node(state: MedicalAgentState) -> MedicalAgentState:
    question = state.get("question", "")
    guard = state.get("business_guard", {})

    risk_level = normalize_risk_level(state.get("risk_level", "low"))
    department = canonicalize_department(
        state.get("canonical_department") or state.get("recommended_department", "") or state.get("department", ""),
        question,
        risk_level
    )
    confidence = normalize_confidence(state.get("confidence", 0.45))
    location = state.get("location", {}) or {}
    registration_steps = state.get("registration_steps", []) or []
    handoff = state.get("handoff", {}) or {}
    triage_analysis = state.get("triage_analysis", {}) or {}
    symptom_summary = state.get("symptom_summary") or triage_analysis.get("symptom_summary") or ""
    possible_conditions = state.get("possible_conditions") or triage_analysis.get("possible_conditions") or []
    red_flags = state.get("red_flags") or triage_analysis.get("red_flags") or []
    reason = state.get("reason") or triage_analysis.get("reason") or ""

    # 1. 业务拦截：真实号源、医生排班、药物、诊断等，不让大模型乱答
    if guard.get("blocked") is True:
        answer = guard.get(
            "message",
            "当前系统未接入真实医院业务系统，无法提供该信息，请以医院官方系统或现场工作人员为准。"
        )

    # 2. 高风险：急诊优先
    elif risk_level == "high":
        department = canonicalize_department(department, question, risk_level)
        answer = (
            f"根据你补充的信息，系统建议优先到 {department} 就诊，并尽快由医护人员进一步评估。\n\n"
            "该判断仅作导诊参考，不代表诊断结论。"
        )

    # 3. 普通导诊：按症状推荐对应科室，语气保持参考性
    else:
        if not department:
            department = "全科"

        answer_parts = []

        answer_parts.append(
            f"根据你补充的信息，建议优先考虑到 {department} 就诊。"
        )

        if confidence:
            answer_parts.append(f"系统参考置信度：{confidence}。")

        if location:
            building = location.get("building", "")
            floor = location.get("floor", "")
            area = location.get("area", "")
            route = location.get("route", "")

            location_text = "科室位置："
            detail_list = []

            if building:
                detail_list.append(building)
            if floor:
                detail_list.append(floor)
            if area:
                detail_list.append(area)

            if detail_list:
                location_text += "，".join(detail_list) + "。"
                answer_parts.append(location_text)

            if route:
                answer_parts.append(f"路线：{route}")

        if registration_steps:
            steps_text = "\n".join([
                f"{index + 1}. {step}"
                for index, step in enumerate(registration_steps)
            ])
            answer_parts.append(f"挂号流程：\n{steps_text}")

        if handoff.get("need_handoff") is True:
            answer_parts.append(
                handoff.get(
                    "handoff_message",
                    "建议咨询医院导诊台或现场医护人员。"
                )
            )

        answer_parts.append(
            "以上病情分析仅作导诊参考，不代表诊断结论；具体判断以医生面诊为准。"
        )

        answer = "\n\n".join(answer_parts)

    analysis_parts = []
    if symptom_summary:
        analysis_parts.append(f"症状概括：{symptom_summary}")
    if possible_conditions:
        analysis_parts.append("可能方向：" + "、".join(possible_conditions[:5]))
    if reason:
        analysis_parts.append(f"推荐依据：{reason}")
    if red_flags:
        analysis_parts.append("风险信号：" + "、".join(red_flags[:5]))
    analysis_text = "\n".join(analysis_parts) or answer

    if robot_response_tool:
        robot_result = robot_response_tool(answer)
    else:
        robot_result = {
            "display_text": answer,
            "speak_text": answer[:120]
        }

    need_followup = state.get("need_followup", False)
    follow_up_questions = state.get("follow_up_questions", [])
    follow_up_items = state.get("follow_up_items", [])
    doctors = (
        state.get("doctors")
        or state.get("recommended_doctors")
        or doctors_by_department(department)
    )
    department_location = get_department_location(department)
    guide = "\n".join(
        f"{index + 1}. {step}"
        for index, step in enumerate(registration_steps)
    )
    visit_guide = build_visit_guide(department, risk_level)

    return {
        "doctors": doctors,
        "recommended_doctors": doctors,
        "department": department,
        "recommended_department": department,
        "canonical_department": department,
        "department_location": department_location,
        "location": department_location,
        "answer": answer,
        "analysis": analysis_text,
        "symptom_summary": symptom_summary,
        "possible_conditions": possible_conditions,
        "red_flags": red_flags,
        "reason": reason,
        "guide": guide,
        "visit_guide": visit_guide,
        "display_text": robot_result.get("display_text", answer),
        "speak_text": robot_result.get("speak_text", answer[:120]),
        "need_followup": need_followup,
        "follow_up_questions": follow_up_questions,
        "followup_questions": follow_up_questions,
        "follow_up_items": follow_up_items,
        "followup_items": follow_up_items,
        "decision_path": add_path(state, "最终回答生成完成")
    }


def qwen_followup_node(state: MedicalAgentState) -> MedicalAgentState:
    fol_state = state.get("session_state", {})
    triage_analysis = state.get("triage_analysis", {}) or {}
    triage_items = safe_followup_items(triage_analysis.get("follow_up_items") or triage_analysis.get("followup_items"))
    triage_need_followup = bool(triage_analysis.get("need_followup")) and (fol_state.get("followup_count", 0) < 1)

    if triage_items or triage_analysis.get("canonical_department") or triage_analysis.get("recommended_department"):
        if state.get("risk_level") == "high":
            triage_need_followup = False
            triage_items = []
        follow_up_questions = [item["question"] for item in triage_items]
        result = {
            "need_followup": triage_need_followup,
            "follow_up_questions": follow_up_questions,
            "followup_questions": follow_up_questions,
            "follow_up_items": triage_items,
            "followup_items": triage_items,
            "missing_info": [],
            "preliminary_department": state.get("canonical_department", ""),
            "risk_level": state.get("risk_level", "low"),
            "reason": triage_analysis.get("reason", "")
        }
        tools_used, tool_results = add_tool(state, "triage_analysis_followup", result)
        return {
            "need_followup": result["need_followup"],
            "follow_up_questions": follow_up_questions,
            "followup_questions": follow_up_questions,
            "follow_up_items": triage_items,
            "followup_items": triage_items,
            "qwen_followup": result,
            "tools_used": tools_used,
            "tool_results": tool_results,
            "decision_path": add_path(state, "使用LLM病情分析追问")
        }


    return {
        "need_followup": False,
        "follow_up_questions": [],
        "followup_questions": [],
        "follow_up_items": [],
        "followup_items": [],
        "qwen_followup": {},
        "decision_path": add_path(state, "LLM未返回追问，跳过旧追问兜底")
    }


def preliminary_answer_node(state: MedicalAgentState) -> MedicalAgentState:
    guard = state.get("business_guard", {})
    if guard.get("blocked") is True:
        ans = guard.get("message", "\u5f53\u524d\u65e0\u6cd5\u5904\u7406\u8be5\u95ee\u9898\u3002")
        return {"answer": ans, "display_text": ans, "speak_text": ans[:120], "doctors": []}

    triage_analysis = state.get("triage_analysis", {}) or {}
    department = canonicalize_department(
        state.get("canonical_department") or state.get("recommended_department", "") or state.get("department", ""),
        state.get("question", ""),
        state.get("risk_level", "")
    )
    department_location = get_department_location(department)

    fi = safe_followup_items(state.get("follow_up_items", []))
    fq = [item["question"] for item in fi]

    if not fi:
        if is_vague_or_no_symptom(state.get("question", "")):
            ans = (
                "当前还没有描述明确的不适症状，系统暂时无法生成有针对性的追问。"
                "请补充患者具体哪里不舒服、持续多久、是否加重，以及是否伴随发热、疼痛、咳嗽、恶心、皮疹等表现。"
            )
            path_text = "主诉过于笼统，提示用户补充具体症状"
        else:
            ans = (
                "当前没有生成可选择的追问项。请换一种方式补充主诉，例如说明不适部位、持续时间、严重程度和伴随症状，"
                "系统会再根据补充信息生成追问或导诊建议。"
            )
            path_text = "未返回有效追问选项，提示用户补充主诉"
        return {
            "doctors": [],
            "recommended_doctors": [],
            "department": department,
            "recommended_department": department,
            "canonical_department": department,
            "department_location": department_location,
            "risk_level": state.get("risk_level", ""),
            "confidence": state.get("confidence", ""),
            "symptom_summary": state.get("symptom_summary") or triage_analysis.get("symptom_summary", ""),
            "possible_conditions": state.get("possible_conditions") or triage_analysis.get("possible_conditions", []),
            "red_flags": state.get("red_flags") or triage_analysis.get("red_flags", []),
            "reason": state.get("reason") or triage_analysis.get("reason", ""),
            "analysis": state.get("reason") or triage_analysis.get("reason", ""),
            "location": department_location,
            "registration_steps": [],
            "handoff": {},
            "sources": [],
            "source_details": [],
            "answer": ans,
            "display_text": ans,
            "speak_text": ans[:120],
            "need_followup": False,
            "follow_up_questions": [],
            "followup_questions": [],
            "follow_up_items": [],
            "followup_items": [],
            "decision_path": add_path(state, path_text)
        }

    parts = ["目前信息还不完整，暂不做疾病判断，请选择以下补充信息：\n"]

    if fq:
        for i, q in enumerate(fq, 1):
            parts.append(f"  {i}. {q}")

    parts.append("\n\u672c\u7cfb\u7edf\u4ec5\u63d0\u4f9b\u5bfc\u8bca\u53c2\u8003\uff0c\u4e0d\u80fd\u4ee3\u66ff\u533b\u751f\u8bca\u65ad\u3002")
    ans = "\n\n".join(parts)

    return {
        "doctors": [],
        "recommended_doctors": [],
        "department": department,
        "recommended_department": department,
        "canonical_department": department,
        "department_location": department_location,
        "risk_level": state.get("risk_level", ""),
        "confidence": state.get("confidence", ""),
        "symptom_summary": state.get("symptom_summary") or triage_analysis.get("symptom_summary", ""),
        "possible_conditions": state.get("possible_conditions") or triage_analysis.get("possible_conditions", []),
        "red_flags": state.get("red_flags") or triage_analysis.get("red_flags", []),
        "reason": state.get("reason") or triage_analysis.get("reason", ""),
        "analysis": state.get("reason") or triage_analysis.get("reason", ""),
        "location": department_location,
        "registration_steps": [],
        "handoff": {},
        "sources": [],
        "source_details": [],
        "answer": ans,
        "display_text": ans,
        "speak_text": ans[:120],
        "need_followup": True,
        "follow_up_questions": fq,
        "followup_questions": fq,
        "follow_up_items": fi,
        "followup_items": fi,
        "decision_path": add_path(state, "\u521d\u6b65\u56de\u7b54\u751f\u6210\u5b8c\u6210\uff08\u8ffd\u95ee\u6a21\u5f0f\uff09")
    }


def followup_router(state: MedicalAgentState) -> str:
    guard = state.get("business_guard", {})
    risk_level = state.get("risk_level", "")
    session_state = state.get("session_state", {}) or {}
    followup_count = session_state.get("followup_count", 0)

    # Blocked questions -> go straight to RAG/answer
    if guard.get("blocked") is True:
        return "rag"

    # Emergency questions -> go straight to RAG/answer
    if risk_level == "high":
        return "rag"

    # Only ask one follow-up round per session. After the user answers it,
    # continue to RAG/final analysis even if Qwen still reports missing info.
    if followup_count >= 1:
        return "rag"

    # First normal round: ask exactly one follow-up before final analysis.
    return "preliminary_answer"

builder = StateGraph(MedicalAgentState)

builder.add_node("business_guard_node", business_guard_node)
builder.add_node("risk_triage_node", risk_triage_node)
builder.add_node("triage_analysis_node", triage_analysis_node)
builder.add_node("department_node", department_node)
builder.add_node("hospital_map_node", hospital_map_node)
builder.add_node("registration_node", registration_node)
builder.add_node("rag_node", rag_node)
builder.add_node("handoff_node", handoff_node)
builder.add_node("answer_node", answer_node)
builder.add_node("qwen_followup_node", qwen_followup_node)
builder.add_node("preliminary_answer_node", preliminary_answer_node)


# qwen_followup conditional routing
builder.add_conditional_edges(
    "qwen_followup_node",
    followup_router,
    {
        "preliminary_answer": "preliminary_answer_node",
        "rag": "rag_node"
    }
)

builder.add_edge("preliminary_answer_node", END)
builder.add_edge("answer_node", END)

builder.add_edge(START, "business_guard_node")
builder.add_edge("business_guard_node", "risk_triage_node")
builder.add_edge("risk_triage_node", "triage_analysis_node")
builder.add_edge("triage_analysis_node", "department_node")
builder.add_edge("department_node", "hospital_map_node")
builder.add_edge("hospital_map_node", "registration_node")
builder.add_edge("registration_node", "qwen_followup_node")
builder.add_edge("rag_node", "handoff_node")
builder.add_edge("handoff_node", "answer_node")


graph = builder.compile()
