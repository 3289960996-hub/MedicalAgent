from agent_core.lab_report_report import DISCLAIMER, build_analysis_result, normalize_report_type
from agent_core.lab_report_rules import apply_indicator_rule


def test_numeric_range_rules_cover_high_low_and_normal():
    common = {"reference_range": "3.5-9.5", "result": ""}
    assert apply_indicator_rule({**common, "value": 10.2})["status"] == "high"
    assert apply_indicator_rule({**common, "value": 3.0})["status"] == "low"
    assert apply_indicator_rule({**common, "value": 5.0})["status"] == "normal"


def test_limit_and_qualitative_rules():
    assert apply_indicator_rule({"value": 5.7, "reference_range": "< 6.1"})["status"] == "normal"
    assert apply_indicator_rule({"value": 6.1, "reference_range": "< 6.1"})["status"] == "high"
    positive = apply_indicator_rule({"result": "阳性", "reference_range": "阴性"})
    assert positive["status"] == "high"
    assert positive["abnormal_direction"] == "阳性"


def test_source_flag_has_priority_and_keeps_provenance():
    result = apply_indicator_rule({"result": "4.2", "source_flag": "L", "reference_range": "3-5", "value": 4.2})
    assert result["status"] == "low"
    assert result["status_source"] == "source_flag"


def test_model_status_cannot_override_reference_rule():
    result = apply_indicator_rule({"status": "high", "value": 4.2, "reference_range": "3-5"})
    assert result["status"] == "normal"
    assert result["status_source"] == "reference_range"


def test_confirmed_status_is_used_only_when_rule_is_unresolved():
    result = apply_indicator_rule({"status": "low", "result": "模糊"}, allow_confirmed_status=True)
    assert result["status"] == "low"
    assert result["status_source"] == "manual_review"


def test_fixed_report_and_safety_constraints():
    indicators = [apply_indicator_rule({
        "name": "白细胞",
        "result": "12.6",
        "value": 12.6,
        "unit": "10^9/L",
        "reference_range": "3.5-9.5",
        "confidence": 0.95,
    })]
    result = build_analysis_result(
        {
            "sample_info": "静脉血",
            "indicator_explanations": [{"name": "白细胞", "explanation": "与多种生理或炎症反应有关"}],
            "interpretation": "诊断为感染",
            "possible_systems": ["血液系统"],
            "possible_directions": ["炎症反应相关变化"],
            "suggested_checks": ["复查血常规并关注分类计数"],
            "recommendations": ["建议用药"],
            "knowledge_sources": [{
                "indicator": "白细胞计数（WBC）",
                "category": "blood_routine",
                "source": "medical_knowledge/blood_routine/wbc.md",
            }],
        },
        indicators,
        report_type="血常规",
    )
    assert result["disclaimer"] == DISCLAIMER
    assert result["report"]["disclaimer"] == DISCLAIMER
    assert result["report"]["overview"] == {"report_type": "血常规", "sample_info": "静脉血"}
    assert result["report"]["abnormal_indicators"][0]["direction"] == "升高"
    assert "可能" in result["indicator_explanations"][0]["explanation"]
    assert result["indicators"][0]["explanation"] == result["indicator_explanations"][0]["explanation"]
    assert "诊断为" not in result["interpretation"]
    assert all("建议用药" not in item for item in result["recommendations"])
    assert result["knowledge_sources"][0]["source"] == "medical_knowledge/blood_routine/wbc.md"
    assert result["report"]["knowledge_basis"] == result["knowledge_sources"]
    comprehensive = result["report"]["comprehensive_analysis"]
    assert comprehensive["possible_systems"] == ["血液系统"]
    assert comprehensive["possible_directions"][0].startswith("可能提示")
    assert comprehensive["risk_level"] == "建议关注"
    assert comprehensive["suggested_checks"] == ["复查血常规并关注分类计数"]


def test_comprehensive_risk_level_is_rule_controlled():
    normal = build_analysis_result({}, [], report_type="血常规")
    assert normal["risk_level"] == "正常"

    mild = build_analysis_result({}, [apply_indicator_rule({
        "name": "白细胞", "value": 9.6, "result": "9.6", "reference_range": "3.5-9.5"
    })], report_type="血常规")
    assert mild["risk_level"] == "轻度异常"

    critical = build_analysis_result({}, [apply_indicator_rule({
        "name": "白细胞", "result": "20.0 危急", "source_flag": "危急", "reference_range": "3.5-9.5"
    })], report_type="血常规")
    assert critical["risk_level"] == "建议医学评估"


def test_report_type_filters_hospital_title_and_infers_panel():
    indicators = [
        {"name": "白细胞计数（WBC）"},
        {"name": "红细胞计数（RBC）"},
        {"name": "血红蛋白（HGB）"},
    ]
    assert normalize_report_type("成都市第二人民医院检验报告单", indicators) == "血常规"
    assert normalize_report_type("成都市第二人民医院血常规检验报告", indicators) == "血常规"
    assert normalize_report_type("成都市第二人民医院检验报告单", []) == "化验单"
