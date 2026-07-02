from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from db import SessionLocal, init_db
from models import (
    Department,
    DepartmentLocation,
    DiseaseKnowledge,
    Doctor,
    InspectionSuggestion,
    SymptomDepartmentRule,
)
from agent_core.graph import (
    FALLBACK_DEPARTMENT_LOCATION_MAP,
    fallback_doctors_by_department,
)


SYMPTOM_RULES = [
    {
        "department": "骨科",
        "keywords": ["脚趾", "脚趾头", "脚踝", "足踝", "膝盖", "膝关节", "关节", "腰", "腿", "肩膀", "脖子", "扭伤", "摔伤", "骨折"],
        "reason": "用户描述涉及足踝、膝关节、骨骼关节或运动损伤相关问题，建议优先考虑骨科；如医院设有足踝外科，可按导诊进一步分诊。",
        "priority": 10,
    },
    {"department": "肛肠科", "keywords": ["痔疮", "肛门疼", "肛门痛", "肛门瘙痒", "便血", "肛裂", "肛周肿痛"], "reason": "用户描述涉及痔疮、便血或肛门相关不适，建议优先考虑肛肠科。", "priority": 15},
    {"department": "眼科", "keywords": ["眼睛", "眼疼", "眼痛", "眼红", "眼部", "眼不舒服", "眼睛不舒服", "视力下降", "看不清", "流泪", "眼干", "眼痒"], "reason": "用户描述涉及眼部不适或视力相关问题，建议优先考虑眼科。", "priority": 20},
    {"department": "耳鼻喉科", "keywords": ["耳朵", "耳疼", "耳痛", "耳鸣", "听不清", "听力下降", "鼻塞", "流鼻涕", "鼻出血", "咽喉痛", "嗓子疼", "嗓子", "喉咙", "咽喉", "声音嘶哑"], "reason": "用户描述涉及耳、鼻、咽喉相关不适，建议优先考虑耳鼻喉科。", "priority": 30},
    {"department": "口腔科", "keywords": ["牙疼", "牙痛", "牙龈", "牙齿", "牙不舒服", "牙龈肿", "口腔", "嘴巴疼", "口腔溃疡", "拔牙", "智齿", "脸肿", "面部肿胀"], "reason": "用户描述涉及牙齿、牙龈或口腔相关问题，建议优先考虑口腔科。", "priority": 40},
    {"department": "呼吸内科", "keywords": ["咳嗽", "发烧", "发热", "气短", "咳痰", "胸闷", "喘", "咽痛", "呼吸"], "reason": "用户描述包含发热、咳嗽、气短等呼吸系统或发热相关症状。", "priority": 50},
    {"department": "消化内科", "keywords": ["胃痛", "胃疼", "腹痛", "肚子疼", "腹泻", "拉肚子", "恶心", "呕吐", "反酸", "消化不良"], "reason": "用户描述包含胃痛、腹痛、腹泻、恶心等消化系统相关症状。", "priority": 60},
    {"department": "心内科", "keywords": ["胸痛", "胸疼", "心悸", "高血压", "胸闷", "心慌", "心跳快"], "reason": "用户描述涉及胸痛、胸闷、心悸或血压相关问题，建议优先考虑心内科；明显急症应优先急诊。", "priority": 70},
    {"department": "神经内科", "keywords": ["头痛", "头疼", "头晕", "眩晕", "麻木", "肢体无力", "手麻", "脚麻", "说话不清"], "reason": "用户描述涉及头痛、头晕、麻木或肢体无力等神经系统相关症状。", "priority": 80},
    {"department": "皮肤科", "keywords": ["皮疹", "瘙痒", "皮肤痒", "痒痒", "身上痒", "过敏", "湿疹", "红疹", "起疹", "起红疹", "脱皮", "长痘", "荨麻疹"], "reason": "用户描述涉及皮疹、瘙痒、过敏或其他皮肤相关问题。", "priority": 90},
    {"department": "泌尿外科", "keywords": ["尿频", "尿急", "尿痛", "血尿", "小便疼", "尿尿", "尿尿疼", "排尿困难", "肾结石"], "reason": "用户描述涉及排尿不适或泌尿系统相关问题。", "priority": 100},
    {"department": "妇科", "keywords": ["月经", "痛经", "白带", "阴道", "妇科", "下腹痛", "经期", "怀孕"], "reason": "用户描述涉及女性生殖健康或妇科相关问题。", "priority": 110},
    {"department": "儿科", "keywords": ["孩子", "小孩", "儿童", "宝宝", "婴儿", "幼儿"], "reason": "用户描述对象为儿童，建议优先考虑儿科。", "priority": 120},
    {"department": "内分泌科", "keywords": ["血糖", "糖尿病", "甲状腺", "肥胖", "多饮", "多尿"], "reason": "用户描述涉及血糖、甲状腺、肥胖或内分泌相关问题。", "priority": 130},
]


DISEASE_KNOWLEDGE = [
    {"name": "视力下降", "department": "眼科", "summary": "看不清、视力下降、眼痛或眼红等眼部问题建议先到眼科评估。", "red_flags": "突然视力明显下降、剧烈眼痛、外伤后视物异常"},
    {"name": "痔疮便血", "department": "肛肠科", "summary": "痔疮、便血、肛门疼痛或肛裂等情况建议先到肛肠科评估。", "red_flags": "大量便血、头晕乏力、黑便或持续加重"},
    {"name": "关节疼痛", "department": "骨科", "summary": "摔伤、扭伤、骨折、关节痛和活动受限等建议先到骨科评估。", "red_flags": "明显畸形、无法行走、严重外伤"},
    {"name": "咳嗽发热", "department": "呼吸内科", "summary": "咳嗽、发热、咳痰、胸闷等呼吸相关症状可先到呼吸内科或发热门诊评估。", "red_flags": "呼吸困难、持续高热、意识异常"},
]


INSPECTION_SUGGESTIONS = [
    {"name": "眼部基础检查", "department": "眼科", "suggestion": "可由医生根据情况安排视力、裂隙灯或眼底相关检查。", "risk_level": "low", "confidence": 0.6},
    {"name": "肛肠专科评估", "department": "肛肠科", "suggestion": "可由医生根据便血和疼痛情况安排肛肠专科查体。", "risk_level": "low", "confidence": 0.6},
    {"name": "骨关节评估", "department": "骨科", "suggestion": "外伤、疼痛或活动受限时，可由医生判断是否需要影像学检查。", "risk_level": "low", "confidence": 0.6},
    {"name": "呼吸系统评估", "department": "呼吸内科", "suggestion": "咳嗽发热或胸闷时，可由医生判断是否需要血常规、胸部影像等检查。", "risk_level": "low", "confidence": 0.6},
]


def get_or_create(db, model, defaults=None, **filters):
    row = db.query(model).filter_by(**filters).first()
    if row:
        return row, False
    row = model(**filters, **(defaults or {}))
    db.add(row)
    return row, True


def seed_departments(db) -> int:
    created = 0
    names = set(FALLBACK_DEPARTMENT_LOCATION_MAP)
    names.update(rule["department"] for rule in SYMPTOM_RULES)
    for name in sorted(names):
        _, was_created = get_or_create(db, Department, name=name, defaults={"description": f"{name}基础科室数据"})
        created += int(was_created)
    return created


def seed_department_locations(db) -> int:
    created = 0
    for department, location in FALLBACK_DEPARTMENT_LOCATION_MAP.items():
        _, was_created = get_or_create(
            db,
            DepartmentLocation,
            department=department,
            defaults={
                "floor": location.get("floor", ""),
                "area": location.get("area", ""),
                "room": location.get("room", ""),
                "description": location.get("description", ""),
            },
        )
        created += int(was_created)
    return created


def seed_doctors(db) -> int:
    created = 0
    for department in sorted(FALLBACK_DEPARTMENT_LOCATION_MAP):
        for doctor in fallback_doctors_by_department(department):
            _, was_created = get_or_create(
                db,
                Doctor,
                name=doctor.get("name", ""),
                department=doctor.get("department", department),
                defaults={
                    "title": doctor.get("title", ""),
                    "specialty": doctor.get("specialty", ""),
                    "available": bool(doctor.get("available", True)),
                    "time": doctor.get("time", ""),
                    "fee": doctor.get("fee", ""),
                    "slots": int(doctor.get("slots") or 0),
                },
            )
            created += int(was_created)
    return created


def seed_symptom_rules(db) -> int:
    created = 0
    for rule in SYMPTOM_RULES:
        keywords = ",".join(rule["keywords"])
        _, was_created = get_or_create(
            db,
            SymptomDepartmentRule,
            department=rule["department"],
            keywords=keywords,
            defaults={
                "reason": rule["reason"],
                "matched_type": "rule",
                "confidence": "medium",
                "priority": rule["priority"],
            },
        )
        created += int(was_created)
    return created


def seed_disease_knowledge(db) -> int:
    created = 0
    for item in DISEASE_KNOWLEDGE:
        defaults = {key: value for key, value in item.items() if key != "name"}
        _, was_created = get_or_create(db, DiseaseKnowledge, name=item["name"], defaults=defaults)
        created += int(was_created)
    return created


def seed_inspection_suggestions(db) -> int:
    created = 0
    for item in INSPECTION_SUGGESTIONS:
        defaults = {
            key: value
            for key, value in item.items()
            if key not in {"name", "department"}
        }
        _, was_created = get_or_create(
            db,
            InspectionSuggestion,
            name=item["name"],
            department=item["department"],
            defaults=defaults,
        )
        created += int(was_created)
    return created


def main() -> None:
    init_db()
    with SessionLocal() as db:
        counts = {
            "departments": seed_departments(db),
            "department_locations": seed_department_locations(db),
            "doctors": seed_doctors(db),
            "symptom_department_rules": seed_symptom_rules(db),
            "disease_knowledge": seed_disease_knowledge(db),
            "inspection_suggestions": seed_inspection_suggestions(db),
        }
        db.commit()
    print("MySQL seed complete:", counts)


if __name__ == "__main__":
    main()
