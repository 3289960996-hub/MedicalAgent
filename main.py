import argparse
import json
from pathlib import Path


DEMO_CASES_PATH = Path(__file__).resolve().parent / "examples" / "demo_cases.json"


def has_unnegated_keyword(question: str, keyword: str, negations: list[str]) -> bool:
    if keyword not in question:
        return False
    return not any(phrase in question for phrase in negations)


def build_rule_demo_result(question: str) -> dict:
    """Return a lightweight demo result without calling external services."""
    high_risk_rules = {
        "胸痛": ["没有胸痛", "无胸痛"],
        "呼吸困难": ["没有呼吸困难", "无呼吸困难"],
        "意识不清": ["没有意识不清", "无意识不清"],
        "大量出血": ["没有大量出血", "无大量出血"],
        "严重外伤": ["没有严重外伤", "无严重外伤"],
    }
    risk_level = "low"
    if any(
        has_unnegated_keyword(question, keyword, negations)
        for keyword, negations in high_risk_rules.items()
    ):
        risk_level = "high"
    elif any(keyword in question for keyword in ["持续", "加重", "高烧", "三天", "多天"]):
        risk_level = "medium"

    if risk_level == "high":
        department = "急诊科"
    elif any(keyword in question for keyword in ["胃痛", "胃疼", "肚子疼", "腹痛", "恶心", "呕吐", "腹泻"]):
        department = "消化内科"
    elif any(keyword in question for keyword in ["咳嗽", "发烧", "发热", "嗓子疼", "呼吸"]):
        department = "呼吸内科"
    elif any(keyword in question for keyword in ["牙疼", "牙痛", "牙龈"]):
        department = "口腔科"
    elif any(keyword in question for keyword in ["头痛", "头晕", "手麻", "脚麻"]):
        department = "神经内科"
    else:
        department = "全科医学科"

    need_followup = risk_level != "high"
    followups = []
    if need_followup:
        followups = ["症状持续多久了？是否伴随发热、胸闷、呼吸困难或基础疾病？"]

    return {
        "question": question,
        "risk_level": risk_level,
        "recommended_department": department,
        "need_followup": need_followup,
        "follow_up_questions": followups,
        "answer": f"根据当前描述，建议优先考虑 {department}。该结果仅作为导诊参考。",
        "visit_guide": "建议携带身份证、医保卡和既往检查资料，按医院挂号流程前往对应科室；如症状明显加重，请及时前往急诊。",
        "disclaimer": "本项目仅用于学习研究，不能替代医生诊断。",
    }


def build_demo_result(question: str) -> dict:
    """Run one minimal triage demo through the existing LangGraph flow."""
    from agent_core.medical_graph import run_medical_graph

    result = run_medical_graph(question=question, client_type="cli")
    return {
        "question": question,
        "risk_level": result.get("risk_level", ""),
        "recommended_department": (
            result.get("canonical_department")
            or result.get("recommended_department")
            or result.get("department", "")
        ),
        "need_followup": result.get("need_followup", False),
        "follow_up_questions": (
            result.get("follow_up_questions")
            or result.get("followup_questions")
            or []
        ),
        "answer": result.get("answer") or result.get("display_text", ""),
        "visit_guide": result.get("visit_guide", ""),
        "sources": result.get("sources", []),
        "source_details": result.get("source_details", []),
        "disclaimer": "本项目仅用于学习研究，不能替代医生诊断。",
    }


def load_demo_cases(path: Path = DEMO_CASES_PATH) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("examples/demo_cases.json must contain a JSON array.")
    return cases


def run_case(case: dict, full_agent: bool = False) -> dict:
    question = case.get("input", "")
    result = build_demo_result(question) if full_agent else build_rule_demo_result(question)
    return {
        "case_id": case.get("id", ""),
        "title": case.get("title", ""),
        "input": question,
        "expected": case.get("expected_output", {}),
        "actual": result,
    }


def main():
    parser = argparse.ArgumentParser(
        description="MedicalAgent command-line demo"
    )
    parser.add_argument(
        "question",
        nargs="?",
        default="我发烧咳嗽两天了，没有呼吸困难，应该挂什么科？",
        help="用户症状描述",
    )
    parser.add_argument(
        "--full-agent",
        action="store_true",
        help="调用现有 LangGraph Agent 全流程，需要完整依赖和大模型配置。",
    )
    parser.add_argument(
        "--case",
        choices=["low", "medium", "high", "all"],
        help="从 examples/demo_cases.json 读取并运行指定示例。",
    )
    args = parser.parse_args()

    try:
        if args.case:
            cases = load_demo_cases()
            selected_cases = cases if args.case == "all" else [
                case for case in cases if case.get("risk_level") == args.case
            ]
            result = [run_case(case, args.full_agent) for case in selected_cases]
        elif args.full_agent:
            result = build_demo_result(args.question)
        else:
            result = build_rule_demo_result(args.question)
    except Exception as exc:
        result = {
            "question": args.question,
            "error": str(exc),
            "hint": "请确认已安装 requirements.txt，并按需配置 project_config/.env 中的 LLM_API_KEY。",
            "disclaimer": "本项目仅用于学习研究，不能替代医生诊断。",
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
