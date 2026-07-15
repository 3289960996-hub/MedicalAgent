import re
from typing import Any

from agent_core.lab_report_rules import ABNORMAL_STATUSES


DISCLAIMER = "本分析仅用于辅助理解报告，不构成医疗诊断或治疗建议。"
_FORBIDDEN_MEDICAL_CLAIMS = re.compile(r"确诊为|诊断为|建议服用|建议用药|开药|处方|治疗方案|治愈|预后")
_NUMERIC_RANGE = re.compile(r"^\s*([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*(?:-|~|～|—|–|至)\s*([+-]?(?:\d+(?:\.\d+)?|\.\d+))\s*$")
_REPORT_TYPE_ALIASES = (
    ("血常规", ("血常规", "全血细胞", "血细胞分析", "CBC")),
    ("肝功能", ("肝功能", "肝功")),
    ("肾功能", ("肾功能", "肾功")),
    ("尿常规", ("尿常规", "尿液分析")),
    ("血脂血糖", ("血脂血糖", "血脂", "血糖", "糖化血红蛋白")),
    ("甲状腺功能", ("甲状腺功能", "甲功", "甲状腺")),
    ("乙肝及感染", ("乙肝五项", "乙肝两对半", "感染筛查", "传染病筛查")),
    ("炎症指标", ("炎症指标", "炎症标志物")),
    ("凝血功能", ("凝血功能", "凝血四项", "凝血")),
    ("心肌标志物", ("心肌标志物", "心肌酶", "心功能")),
    ("肿瘤标志物", ("肿瘤标志物", "肿瘤标记物")),
)
_REPORT_TYPE_INDICATORS = (
    ("血常规", ("WBC", "NEUT", "LYMPH", "RBC", "HGB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "MPV", "白细胞", "红细胞", "血红蛋白", "血小板")),
    ("肝功能", ("ALT", "AST", "TBIL", "DBIL", "IBIL", "ALB", "GGT", "ALP", "CHE", "A/G", "总胆红素", "直接胆红素", "白蛋白")),
    ("肾功能", ("CREA", "UREA", "BUN", "EGFR", "CYS-C", "肌酐", "尿素", "尿酸", "胱抑素")),
    ("尿常规", ("尿蛋白", "尿糖", "尿潜血", "尿白细胞", "尿酮体", "尿胆红素", "尿比重")),
    ("血脂血糖", ("HBA1C", "HDL-C", "LDL-C", "LP(A)", "总胆固醇", "甘油三酯", "血糖")),
    ("甲状腺功能", ("TSH", "FT3", "FT4", "TPOAB", "TGAB", "甲状腺")),
    ("乙肝及感染", ("HBSAG", "HBSAB", "HBEAG", "HBEAB", "HBCAB", "HBV-DNA", "HCV-AB", "HIV-AB", "乙肝")),
    ("炎症指标", ("CRP", "HS-CRP", "ESR", "PCT", "降钙素原", "血沉")),
    ("凝血功能", ("APTT", "INR", "D-DIMER", "FIB", "凝血酶原")),
    ("心肌标志物", ("CK-MB", "CTNI", "BNP", "NT-PROBNP", "肌钙蛋白")),
    ("肿瘤标志物", ("AFP", "CEA", "CA125", "CA199", "PSA", "癌胚抗原")),
)


def build_analysis_result(
    payload: dict[str, Any],
    indicators: list[dict[str, Any]],
    *,
    report_type: str = "化验单",
    verified: bool = False,
) -> dict[str, Any]:
    abnormal = [item for item in indicators if item.get("status") in ABNORMAL_STATUSES]
    normalized_report_type = normalize_report_type(report_type or payload.get("report_type"), indicators)
    explanations = _normalize_explanations(payload.get("indicator_explanations"), abnormal)
    explanation_by_name = {item["name"]: item["explanation"] for item in explanations}
    enriched_indicators = [
        {**item, **({"explanation": explanation_by_name[item.get("name")]} if item.get("name") in explanation_by_name else {})}
        for item in indicators
    ]
    abnormal_summary = _safe_text(payload.get("abnormal_summary"), 1000) or _fallback_summary(abnormal)
    interpretation = _safe_text(payload.get("interpretation"), 3000) or abnormal_summary
    recommendations = _safe_list(payload.get("recommendations"), 5, 300)
    if not recommendations:
        recommendations = ["建议结合症状、病史及报告原始参考范围咨询医生，必要时按医生建议复查相关指标。"]
    possible_systems = _safe_list(payload.get("possible_systems"), 5, 80) or _infer_systems(normalized_report_type, abnormal)
    possible_directions = _cautious_directions(payload.get("possible_directions"), 5, 300)
    if not possible_directions:
        possible_directions = (
            ["需要关注上述指标变化与相关身体系统状态的关联，并结合症状及其他检查判断。"]
            if abnormal else
            ["当前报告未见明确异常方向，仍需要结合个人症状、病史和检查目的理解。"]
        )
    suggested_checks = _safe_list(payload.get("suggested_checks"), 5, 300) or recommendations
    risk_level = _risk_level(abnormal)
    attention = "尽快就医" if any(item.get("status") == "critical" for item in indicators) else "建议复查" if abnormal else "常规关注"
    sources = _normalize_knowledge_sources(payload.get("knowledge_sources"))

    result = {
        "report_type": normalized_report_type,
        "report_date": str(payload.get("report_date") or "")[:40],
        "sample_info": _sample_info(payload),
        "indicators": enriched_indicators,
        "indicator_count": len(indicators),
        "abnormal_count": len(abnormal),
        "abnormal_summary": abnormal_summary,
        "indicator_explanations": explanations,
        "interpretation": interpretation,
        "possible_factors": _safe_list(payload.get("possible_factors"), 6, 200),
        "possible_systems": possible_systems,
        "possible_directions": possible_directions,
        "risk_level": risk_level,
        "suggested_checks": suggested_checks,
        "attention_level": attention,
        "recommendations": recommendations,
        "suggested_department": _safe_text(payload.get("suggested_department"), 50) or "全科",
        "red_flags": _safe_list(payload.get("red_flags"), 5, 300),
        "knowledge_sources": sources,
        "low_confidence_count": sum(float(item.get("confidence") or 0) < 0.75 for item in indicators),
        "disclaimer": DISCLAIMER,
        "verified": verified,
    }
    result["report"] = build_fixed_report(result)
    return result


def build_fixed_report(result: dict[str, Any]) -> dict[str, Any]:
    abnormal = [item for item in result.get("indicators", []) if item.get("status") in ABNORMAL_STATUSES]
    return {
        "overview": {
            "report_type": result.get("report_type") or "化验单",
            "sample_info": result.get("sample_info") or "未提供",
        },
        "abnormal_indicators": [
            {
                "name": item.get("name") or "未识别项目",
                "result": item.get("result") or "",
                "unit": item.get("unit") or "",
                "reference_range": item.get("reference_range") or "",
                "direction": item.get("abnormal_direction") or "需要复核",
            }
            for item in abnormal
        ],
        "indicator_explanations": result.get("indicator_explanations") or [],
        "comprehensive_analysis": {
            "main_abnormalities": result.get("abnormal_summary") or "未发现明确异常指标。",
            "possible_systems": result.get("possible_systems") or ["暂无法明确涉及系统"],
            "possible_directions": result.get("possible_directions") or [],
            "risk_level": result.get("risk_level") or "正常",
            "suggested_checks": result.get("suggested_checks") or result.get("recommendations") or [],
            # 保留旧字段，避免已有调用方读取失败。
            "possible_factors": result.get("possible_factors") or [],
            "attention_direction": result.get("interpretation") or "请结合症状、病史及其他检查理解报告。",
        },
        "follow_up_suggestions": result.get("recommendations") or [],
        "knowledge_basis": result.get("knowledge_sources") or [],
        "disclaimer": DISCLAIMER,
    }


def _normalize_explanations(value: Any, abnormal: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_name: dict[str, str] = {}
    if isinstance(value, list):
        for item in value:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "")[:100]
            explanation = _safe_text(item.get("explanation"), 600)
            if name and explanation:
                by_name[name] = explanation if "可能" in explanation else f"该项变化可能提示：{explanation}"
    output = []
    for item in abnormal:
        name = str(item.get("name") or "未识别项目")[:100]
        explanation = by_name.get(name) or "该项变化可能提示相关生理状态发生变化，需结合其他指标、症状和病史综合理解。"
        output.append({"name": name, "explanation": explanation})
    return output


def _fallback_summary(abnormal: list[dict[str, Any]]) -> str:
    if not abnormal:
        return "按报告提供的参考范围，暂未发现明确异常指标。"
    names = "、".join(str(item.get("name") or "未识别项目") for item in abnormal[:8])
    return f"按报告提供的参考范围，{names}存在异常标记，建议结合原报告和临床情况复核。"


def normalize_report_type(value: Any, indicators: list[dict[str, Any]]) -> str:
    """将医院抬头等自由文本收敛为受控的检验类型。"""
    raw = re.sub(r"\s+", "", str(value or "")).upper()
    for canonical, aliases in _REPORT_TYPE_ALIASES:
        if any(alias.upper() in raw for alias in aliases):
            return canonical

    scores = {canonical: 0 for canonical, _ in _REPORT_TYPE_INDICATORS}
    for item in indicators:
        name = re.sub(r"\s+", "", str(item.get("name") or "")).upper()
        if not name:
            continue
        for canonical, keywords in _REPORT_TYPE_INDICATORS:
            if any(keyword.upper() in name for keyword in keywords):
                scores[canonical] += 1

    best_type, best_score = max(scores.items(), key=lambda pair: pair[1], default=("化验单", 0))
    return best_type if best_score else "化验单"


def _cautious_directions(value: Any, limit: int, item_limit: int) -> list[str]:
    directions = _safe_list(value, limit, item_limit)
    return [
        item if ("可能提示" in item or "需要关注" in item) else f"可能提示与{item}相关，需结合其他指标判断。"
        for item in directions
    ]


def _infer_systems(report_type: str, abnormal: list[dict[str, Any]]) -> list[str]:
    if not abnormal:
        return ["暂未发现明确异常涉及系统"]
    text = " ".join([str(report_type or ""), *(str(item.get("name") or "") for item in abnormal)]).upper()
    mappings = [
        (("肝", "ALT", "AST", "TBIL", "DBIL", "GGT", "ALP"), "肝胆系统"),
        (("血常规", "WBC", "RBC", "HGB", "HCT", "PLT", "NEUT", "LYMPH"), "血液系统"),
        (("肾", "CREA", "UREA", "EGFR", "CYS-C", "尿酸"), "肾脏功能"),
        (("尿常规", "尿蛋白", "尿潜血", "尿白细胞"), "泌尿系统"),
        (("甲状腺", "TSH", "FT3", "FT4", "TPOAB", "TGAB"), "内分泌系统"),
        (("血糖", "GLU", "HBA1C"), "内分泌及代谢系统"),
        (("血脂", "HDL", "LDL", "胆固醇", "甘油三酯"), "心血管及代谢系统"),
        (("凝血", "PT", "APTT", "INR", "D-DIMER", "FIB"), "凝血系统"),
        (("心肌", "CTNI", "CK-MB", "BNP", "NT-PROBNP"), "心血管系统"),
        (("炎症", "CRP", "ESR", "PCT"), "免疫与炎症反应"),
        (("乙肝", "HBV", "HBSAG", "HBEAG", "HCV", "HIV"), "感染相关系统"),
    ]
    systems = [label for keywords, label in mappings if any(keyword in text for keyword in keywords)]
    return list(dict.fromkeys(systems))[:5] or ["需要结合具体指标进一步判断涉及系统"]


def _risk_level(abnormal: list[dict[str, Any]]) -> str:
    if not abnormal:
        return "正常"
    if any(item.get("status") == "critical" for item in abnormal):
        return "建议医学评估"
    if all(_is_mild_numeric_deviation(item) for item in abnormal):
        return "轻度异常"
    return "建议关注"


def _is_mild_numeric_deviation(item: dict[str, Any]) -> bool:
    try:
        value = float(item.get("value"))
    except (TypeError, ValueError):
        return False
    match = _NUMERIC_RANGE.match(str(item.get("reference_range") or "").replace(",", ""))
    if not match:
        return False
    lower, upper = sorted((float(match.group(1)), float(match.group(2))))
    status = item.get("status")
    bound = upper if status == "high" else lower if status == "low" else None
    if bound is None:
        return False
    scale = max(abs(bound), abs(upper - lower), 1e-9)
    return abs(value - bound) / scale <= 0.10


def _sample_info(payload: dict[str, Any]) -> str:
    value = payload.get("sample_info") or payload.get("sample_type") or "未提供"
    if isinstance(value, dict):
        value = "；".join(f"{key}：{item}" for key, item in value.items() if item not in (None, ""))
    return str(value or "未提供")[:300]


def _safe_list(value: Any, limit: int, item_limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    return [text for item in value[:limit] if (text := _safe_text(item, item_limit))]


def _normalize_knowledge_sources(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    sources: list[dict[str, str]] = []
    for item in value[:8]:
        if not isinstance(item, dict):
            continue
        indicator = _safe_text(item.get("indicator"), 100)
        category = _safe_text(item.get("category"), 50)
        source = _safe_text(item.get("source"), 200)
        if indicator and source.startswith("medical_knowledge/") and source.endswith(".md"):
            sources.append({"indicator": indicator, "category": category, "source": source})
    return sources


def _safe_text(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text or _FORBIDDEN_MEDICAL_CLAIMS.search(text):
        return ""
    return text[:limit]
