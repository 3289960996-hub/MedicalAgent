from pathlib import Path

from scripts.evaluate_demo_cases import evaluate_cases, load_eval_cases


EVAL_CASES_PATH = Path(__file__).resolve().parents[1] / "eval" / "triage_eval_cases.json"


def test_eval_cases_pass_current_lightweight_demo():
    report = evaluate_cases(load_eval_cases(EVAL_CASES_PATH))

    assert report["metrics"]["total"] >= 10
    assert report["metrics"]["exact_match_rate"] == 1.0
    assert report["metrics"]["risk_level_accuracy"] == 1.0
    assert report["metrics"]["department_accuracy"] == 1.0
    assert report["metrics"]["followup_accuracy"] == 1.0
