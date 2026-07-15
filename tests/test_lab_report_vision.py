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
