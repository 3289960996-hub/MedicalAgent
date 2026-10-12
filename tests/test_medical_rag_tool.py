import importlib
from pathlib import Path
import subprocess
import sys
from types import ModuleType


def test_importing_tools_does_not_load_vector_search_dependencies():
    script = """
import importlib
import sys
from types import ModuleType

fake_llm = ModuleType("agent_core.llm")
fake_llm.call_llm = lambda *_args, **_kwargs: ""
sys.modules["agent_core.llm"] = fake_llm

module = importlib.import_module("tools.medical_rag_tool")
assert callable(module.medical_rag_tool)
assert "rag.retriever" not in sys.modules
assert "chromadb" not in sys.modules
assert "sentence_transformers" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_medical_rag_tool_calls_retriever_and_preserves_result(monkeypatch):
    fake_llm = ModuleType("agent_core.llm")
    fake_llm.call_llm = lambda *_args, **_kwargs: ""
    monkeypatch.setitem(sys.modules, "agent_core.llm", fake_llm)

    calls = []
    docs = [
        {"source": "example.md", "content": "first passage"},
        {"source": "example.md", "content": "second passage"},
    ]
    fake_retriever = ModuleType("rag.retriever")

    def search_docs(query, top_k):
        calls.append((query, top_k))
        return docs

    fake_retriever.search_docs = search_docs
    monkeypatch.setitem(sys.modules, "rag.retriever", fake_retriever)
    module = importlib.import_module("tools.medical_rag_tool")

    result = module.medical_rag_tool("example question", top_k=2)

    assert calls == [("example question", 2)]
    assert result == {
        "context": "来源：example.md\n内容：first passage\n\n来源：example.md\n内容：second passage",
        "sources": ["example.md"],
        "docs": docs,
    }
