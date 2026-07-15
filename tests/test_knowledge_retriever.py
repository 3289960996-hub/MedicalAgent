from pathlib import Path

from medical_knowledge.knowledge_retriever import (
    knowledge_context,
    knowledge_sources,
    retrieve_lab_knowledge,
)


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1] / "medical_knowledge"


def test_retrieves_wbc_by_chinese_name():
    documents = retrieve_lab_knowledge(
        "血常规",
        [{"name": "白细胞", "status": "high"}],
        root=KNOWLEDGE_ROOT,
    )
    assert len(documents) == 1
    assert documents[0].metadata["category"] == "blood_routine"
    assert documents[0].metadata["filename"] == "wbc.md"


def test_report_type_disambiguates_glu():
    documents = retrieve_lab_knowledge(
        "尿常规",
        [{"name": "GLU", "status": "high"}],
        root=KNOWLEDGE_ROOT,
    )
    assert len(documents) == 1
    assert documents[0].metadata["category"] == "urine"
    assert documents[0].metadata["filename"] == "glu.md"


def test_context_contains_content_but_sources_do_not():
    documents = retrieve_lab_knowledge(
        "肝功能",
        [{"name": "ALT", "status": "high"}],
        root=KNOWLEDGE_ROOT,
    )
    assert "content" in knowledge_context(documents)[0]
    assert knowledge_sources(documents) == [{
        "indicator": "丙氨酸氨基转移酶（ALT）",
        "category": "liver_function",
        "source": "medical_knowledge/liver_function/alt.md",
    }]


def test_unknown_indicator_does_not_match_by_category_alone():
    documents = retrieve_lab_knowledge(
        "血常规",
        [{"name": "完全未知项目XYZ", "status": "unknown"}],
        root=KNOWLEDGE_ROOT,
    )
    assert documents == []
