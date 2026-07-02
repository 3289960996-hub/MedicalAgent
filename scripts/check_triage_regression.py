import contextlib
import io
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.department_router_tool import department_router_tool
from tools.risk_triage_tool import risk_triage_tool


with contextlib.redirect_stdout(io.StringIO()):
    from graph import canonicalize_department
    from chat_schema import CHAT_SCHEMA_DEFAULTS, normalize_chat_result


DEPARTMENT_CASES = [
    ("我牙疼，应该挂什么科？", "口腔科"),
    ("牙龈肿了两天", "口腔科"),
    ("我牙不舒服", "口腔科"),
    ("智齿疼", "口腔科"),
    ("我眼睛不舒服", "眼科"),
    ("眼红还流泪", "眼科"),
    ("看东西有点看不清", "眼科"),
    ("我皮肤痒痒", "皮肤科"),
    ("身上痒还起红疹", "皮肤科"),
    ("皮疹反复发作", "皮肤科"),
    ("嗓子不舒服", "耳鼻喉科"),
    ("喉咙疼声音嘶哑", "耳鼻喉科"),
    ("咳嗽发烧", "呼吸内科或发热门诊"),
    ("胃疼恶心", "消化内科"),
    ("尿尿疼", "泌尿外科"),
    ("膝盖疼", "骨科"),
]


RISK_CASES = [
    ("我牙疼，应该挂什么科？", "low"),
    ("牙龈肿持续三天", "medium"),
    ("我牙疼，脸肿得厉害还发烧", "high"),
    ("胸痛喘不上气", "high"),
    ("皮疹反复发作", "medium"),
    ("眼睛疼持续三天", "medium"),
    ("我没有高热也没有呼吸困难，只是嗓子不舒服", "low"),
]


CANONICAL_CASES = [
    ("皮肤科", "面部、口唇、眼睑可能肿胀", "皮肤科"),
    ("口腔科", "眼睑安全提示", "口腔科"),
    ("", "我皮肤痒痒还起红疹", "皮肤科"),
    ("", "我牙疼，应该挂什么科？", "口腔科"),
]


SCHEMA_CASES = [
    (
        {"need_followup": True, "follow_up_questions": ["持续多久了？"]},
        "我皮肤痒痒",
        True,
        "全科",
    ),
    (
        {"need_followup": False, "department": "口腔科", "risk_level": "low", "answer": "建议口腔科就诊。"},
        "我牙疼，应该挂什么科？",
        False,
        "口腔科",
    ),
]


def main() -> None:
    failures = []

    for question, expected in DEPARTMENT_CASES:
        actual = department_router_tool(question).get("department")
        if actual != expected:
            failures.append(f"department: {question!r} expected {expected!r}, got {actual!r}")

    for question, expected in RISK_CASES:
        actual = risk_triage_tool(question).get("risk_level")
        if actual != expected:
            failures.append(f"risk: {question!r} expected {expected!r}, got {actual!r}")

    for department, question, expected in CANONICAL_CASES:
        actual = canonicalize_department(department, question, "low")
        if actual != expected:
            failures.append(
                f"canonical: dept={department!r}, question={question!r} "
                f"expected {expected!r}, got {actual!r}"
            )

    for payload, question, is_followup, expected_department in SCHEMA_CASES:
        normalized = normalize_chat_result(payload.copy(), question)
        missing = [key for key in CHAT_SCHEMA_DEFAULTS if key not in normalized]
        if missing:
            failures.append(f"schema missing keys for {question!r}: {missing}")
        if normalized.get("need_followup") is not is_followup:
            failures.append(f"schema followup mismatch for {question!r}")
        if normalized.get("canonical_department") != expected_department:
            failures.append(
                f"schema department for {question!r} expected {expected_department!r}, "
                f"got {normalized.get('canonical_department')!r}"
            )

    if failures:
        raise SystemExit("\n".join(failures))

    print("triage regression ok")


if __name__ == "__main__":
    main()
