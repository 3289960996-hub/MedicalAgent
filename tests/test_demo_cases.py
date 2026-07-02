import json
from pathlib import Path

import pytest

from main import build_rule_demo_result, load_demo_cases, run_case


DEMO_CASES_PATH = Path(__file__).resolve().parents[1] / "examples" / "demo_cases.json"


def test_demo_cases_json_is_valid_list():
    cases = json.loads(DEMO_CASES_PATH.read_text(encoding="utf-8"))

    assert isinstance(cases, list)
    assert {case["risk_level"] for case in cases} == {"low", "medium", "high"}

    for case in cases:
        assert case["id"]
        assert case["title"]
        assert case["input"]
        assert case["expected_output"]["risk_level"] in {"low", "medium", "high"}
        assert case["expected_output"]["recommended_department"]


@pytest.mark.parametrize("case", load_demo_cases())
def test_rule_demo_matches_expected_case(case):
    actual = run_case(case)["actual"]
    expected = case["expected_output"]

    assert actual["risk_level"] == expected["risk_level"]
    assert actual["recommended_department"] == expected["recommended_department"]
    assert actual["need_followup"] is expected["need_followup"]
    assert actual["disclaimer"] == "本项目仅用于学习研究，不能替代医生诊断。"


def test_negated_chest_pain_does_not_hide_breathing_risk():
    result = build_rule_demo_result("没有胸痛，但是呼吸困难")

    assert result["risk_level"] == "high"
    assert result["recommended_department"] == "急诊科"
    assert result["need_followup"] is False


def test_negated_high_risk_symptoms_keep_common_cough_low_risk():
    result = build_rule_demo_result("没有胸痛，也没有呼吸困难，只是咳嗽")

    assert result["risk_level"] == "low"
    assert result["recommended_department"] == "呼吸内科"
    assert result["need_followup"] is True
