import importlib
import sys
from types import ModuleType

import pytest

from agent_core.json_utils import clean_json_text


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ('{"value": 1}', '{"value": 1}'),
        ('  {"value": 1}  ', '{"value": 1}'),
        ('```json\n{"value": 1}\n```', '{"value": 1}'),
        ('```JSON\n{"value": 1}\n```', '{"value": 1}'),
        ('prefix {"value": 1} suffix', 'prefix {"value": 1} suffix'),
        ('```json\n{"value": 1}', '{"value": 1}'),
    ],
)
def test_clean_json_text_preserves_existing_behavior(raw, expected):
    assert clean_json_text(raw) == expected


@pytest.mark.parametrize(
    "module_name",
    [
        "tools.llm_intent_tool",
        "tools.symptom_normalizer_tool",
        "tools.department_llm_classifier_tool",
    ],
)
def test_tool_modules_keep_compatible_cleaner_import(monkeypatch, module_name):
    fake_llm = ModuleType("agent_core.llm")
    fake_llm.call_llm = lambda *_args, **_kwargs: ""
    monkeypatch.setitem(sys.modules, "agent_core.llm", fake_llm)
    monkeypatch.delitem(sys.modules, module_name, raising=False)

    module = importlib.import_module(module_name)

    assert module.clean_json_text is clean_json_text
