import base64
import json
from types import SimpleNamespace

import pytest

import agent_core.lab_report_vision as lab_report_vision
from agent_core.lab_report_vision import (
    _normalize_analysis,
    _parse_json_object,
    _validate_image_data_url,
)


def test_validate_png_data_url():
    raw = b"\x89PNG\r\n\x1a\n" + b"test-image"
    data_url = "data:image/png;base64," + base64.b64encode(raw).decode("ascii")
    mime_type, decoded = _validate_image_data_url(data_url)
    assert mime_type == "image/png"
    assert decoded == raw


def test_rejects_mismatched_image_type():
    raw = b"\xff\xd8\xff" + b"jpeg"
    data_url = "data:image/png;base64," + base64.b64encode(raw).decode("ascii")
    with pytest.raises(ValueError, match="文件类型不匹配"):
        _validate_image_data_url(data_url)


def test_parse_fenced_json():
    parsed = _parse_json_object('```json\n{"report_type":"血常规"}\n```')
    assert parsed["report_type"] == "血常规"


def test_normalize_analysis_counts_abnormal_and_low_confidence():
    result = _normalize_analysis({
        "report_type": "血常规",
        "attention_level": "unsupported",
        "indicators": [
            {"name": "白细胞", "result": "12.6", "value": 12.6, "reference_range": "3.5-9.5", "confidence": 0.9},
            {"name": "血红蛋白", "result": "145", "value": 145, "reference_range": "130-175", "confidence": 0.6},
        ],
    })
    assert result["indicator_count"] == 2
    assert result["abnormal_count"] == 1
    assert result["low_confidence_count"] == 1
    assert result["attention_level"] == "建议复查"
    assert result["disclaimer"] == "本分析仅用于辅助理解报告，不构成医疗诊断或治疗建议。"
    assert result["report"]["overview"]["report_type"] == "血常规"


def test_interpretation_sends_knowledge_context_and_returns_server_sources(monkeypatch):
    captured = {}

    def create(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='{"interpretation":"需结合其他指标判断"}'))])

    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    monkeypatch.setattr(lab_report_vision, "_get_client", lambda: client)

    result = lab_report_vision._request_interpretation(
        "血常规",
        [{"name": "白细胞", "status": "high"}],
    )

    request_payload = json.loads(captured["messages"][1]["content"])
    assert request_payload["knowledge_context"][0]["source"] == "medical_knowledge/blood_routine/wbc.md"
    assert "## AI解释规范" in request_payload["knowledge_context"][0]["content"]
    assert result["knowledge_sources"] == [{
        "indicator": "白细胞计数（WBC）",
        "category": "blood_routine",
        "source": "medical_knowledge/blood_routine/wbc.md",
    }]


def _fake_png_data_url():
    raw = b"\x89PNG\r\n\x1a\n" + b"test-image"
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def _mock_vision_client(payload, calls):
    def create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(content=json.dumps(payload, ensure_ascii=False))
        )])

    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def test_analyze_rejects_non_lab_image(monkeypatch):
    calls = []
    client = _mock_vision_client({
        "is_lab_report": False,
        "image_quality": "clear",
        "quality_reason": "普通照片",
        "indicators": [],
    }, calls)
    monkeypatch.setattr(lab_report_vision, "_get_client", lambda: client)

    with pytest.raises(ValueError, match="不是化验单"):
        lab_report_vision.analyze_lab_report_image(_fake_png_data_url())

    assert len(calls) == 1


def test_analyze_rejects_indicator_without_name_even_when_confidence_is_high(monkeypatch):
    calls = []
    client = _mock_vision_client({
        "is_lab_report": True,
        "image_quality": "clear",
        "quality_reason": "结果可见，但项目名称缺失",
        "indicators": [
            {"name": "", "result": "12.0", "confidence": 0.99},
        ],
    }, calls)
    monkeypatch.setattr(lab_report_vision, "_get_client", lambda: client)

    with pytest.raises(ValueError, match="未识别到可信"):
        lab_report_vision.analyze_lab_report_image(_fake_png_data_url())

    assert len(calls) == 1


def test_analyze_partial_report_keeps_only_trusted_fields_and_waits_for_review(monkeypatch):
    calls = []
    client = _mock_vision_client({
        "is_lab_report": True,
        "image_quality": "partial",
        "quality_reason": "局部污渍，部分字段仍清晰",
        "report_type": "CBC",
        "indicators": [
            {"name": "WBC", "result": "12.0", "value": 12.0, "unit": "10^9/L", "reference_range": "3.5-9.5", "confidence": 0.96},
            {"name": "NEUT%", "result": "72.8", "value": 72.8, "unit": "%", "reference_range": "40-75", "confidence": 0.40},
        ],
    }, calls)
    monkeypatch.setattr(lab_report_vision, "_get_client", lambda: client)

    result = lab_report_vision.analyze_lab_report_image(_fake_png_data_url())

    assert [item["name"] for item in result["indicators"]] == ["WBC"]
    assert result["verified"] is False
    assert result["requires_review"] is True
    assert result["image_quality"] == "partial"
    # Extraction must be the only model call; interpretation happens after confirmation.
    assert len(calls) == 1
