import json
from pathlib import Path


MAP_PATH = Path(__file__).resolve().parents[1] / "data" / "hospital" / "hospital_map.json"


def _department_candidates(department: str) -> list[str]:
    if department == "呼吸内科或发热门诊":
        return ["呼吸内科", "发热门诊"]
    if department == "全科医学科或导诊台":
        return ["导诊台", "全科医学科"]
    if department == "心内科或急诊科":
        return ["心内科", "急诊科"]
    return [department]


def hospital_map_tool(department: str) -> dict:
    """
    查询模拟医院科室位置。
    """
    try:
        hospital_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    except Exception:
        hospital_map = {}

    for candidate in _department_candidates(department):
        if candidate in hospital_map:
            info = hospital_map[candidate]
            return {
                "department": candidate,
                "building": info.get("building", ""),
                "floor": info.get("floor", ""),
                "area": info.get("area", ""),
                "route": info.get("route", "")
            }

    return {
        "department": department,
        "building": "",
        "floor": "",
        "area": "",
        "route": "暂未查询到该科室位置，请咨询医院导诊台。"
    }
