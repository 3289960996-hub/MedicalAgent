import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from main import build_rule_demo_result


DEFAULT_CASES_PATH = ROOT_DIR / "eval" / "triage_eval_cases.json"


def load_eval_cases(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list):
        raise ValueError("Evaluation file must contain a JSON array.")
    return cases


def evaluate_cases(cases: list[dict]) -> dict:
    rows = []
    correct = {
        "risk_level": 0,
        "recommended_department": 0,
        "need_followup": 0,
    }

    for case in cases:
        actual = build_rule_demo_result(case["input"])
        expected = case["expected"]
        checks = {
            "risk_level": actual["risk_level"] == expected["risk_level"],
            "recommended_department": actual["recommended_department"] == expected["recommended_department"],
            "need_followup": actual["need_followup"] is expected["need_followup"],
        }
        for key, passed in checks.items():
            correct[key] += int(passed)

        rows.append(
            {
                "id": case["id"],
                "input": case["input"],
                "expected": expected,
                "actual": {
                    "risk_level": actual["risk_level"],
                    "recommended_department": actual["recommended_department"],
                    "need_followup": actual["need_followup"],
                },
                "passed": all(checks.values()),
                "checks": checks,
            }
        )

    total = len(cases)
    exact_match = sum(1 for row in rows if row["passed"])
    metrics = {
        "total": total,
        "exact_match": exact_match,
        "exact_match_rate": round(exact_match / total, 4) if total else 0,
        "risk_level_accuracy": round(correct["risk_level"] / total, 4) if total else 0,
        "department_accuracy": round(correct["recommended_department"] / total, 4) if total else 0,
        "followup_accuracy": round(correct["need_followup"] / total, 4) if total else 0,
    }
    return {"metrics": metrics, "results": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate lightweight triage demo cases.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--fail-under", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = evaluate_cases(load_eval_cases(args.cases))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(json.dumps(report["metrics"], ensure_ascii=False, indent=2))

    if report["metrics"]["exact_match_rate"] < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
