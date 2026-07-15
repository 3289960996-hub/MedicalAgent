import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from langchain_core.documents import Document

from medical_knowledge.knowledge_loader import load_medical_knowledge


ABNORMAL_STATUSES = {"high", "low", "critical", "unknown"}
CATEGORY_HINTS = {
    "肝": "liver_function",
    "血常规": "blood_routine",
    "血细胞": "blood_routine",
    "肾": "kidney_function",
    "尿": "urine",
    "血脂": "lipid_glucose",
    "血糖": "lipid_glucose",
    "糖化": "lipid_glucose",
    "甲状腺": "thyroid",
    "乙肝": "hepatitis",
    "肝炎": "hepatitis",
    "感染": "hepatitis",
    "炎症": "inflammation",
    "凝血": "coagulation",
}


def retrieve_lab_knowledge(
    report_type: str,
    indicators: list[dict[str, Any]],
    *,
    max_documents: int = 8,
    root: str | Path | None = None,
) -> list[Document]:
    """Retrieve at most one deterministic knowledge document per indicator."""
    documents = load_medical_knowledge(root)
    preferred_category = _preferred_category(report_type)
    ordered_indicators = sorted(
        indicators,
        key=lambda item: 0 if str(item.get("status") or "") in ABNORMAL_STATUSES else 1,
    )
    selected: list[Document] = []
    selected_sources: set[str] = set()

    for indicator in ordered_indicators:
        query = str(indicator.get("name") or "").strip()
        if not query:
            continue
        best_document = max(
            documents,
            key=lambda document: _score_document(query, document, preferred_category),
            default=None,
        )
        if best_document is None:
            continue
        score = _score_document(query, best_document, preferred_category)
        relative_source = _relative_source(best_document)
        if score < 55 or relative_source in selected_sources:
            continue
        selected_sources.add(relative_source)
        selected.append(Document(
            page_content=best_document.page_content,
            metadata={
                **best_document.metadata,
                "relative_source": relative_source,
                "retrieval_score": round(score, 2),
                "matched_query": query,
            },
        ))
        if len(selected) >= max_documents:
            break

    return selected


def knowledge_context(documents: list[Document]) -> list[dict[str, str]]:
    return [
        {
            "indicator": str(document.metadata.get("indicator") or ""),
            "category": str(document.metadata.get("category") or ""),
            "source": str(document.metadata.get("relative_source") or _relative_source(document)),
            "content": document.page_content,
        }
        for document in documents
    ]


def knowledge_sources(documents: list[Document]) -> list[dict[str, str]]:
    return [
        {
            "indicator": str(document.metadata.get("indicator") or ""),
            "category": str(document.metadata.get("category") or ""),
            "source": str(document.metadata.get("relative_source") or _relative_source(document)),
        }
        for document in documents
    ]


def _score_document(query: str, document: Document, preferred_category: str) -> float:
    title = str(document.metadata.get("indicator") or "")
    normalized_query = _normalize(query)
    normalized_title = _normalize(title)
    if not normalized_query or not normalized_title:
        return 0.0
    score = 0.0
    if normalized_query in normalized_title or normalized_title in normalized_query:
        score += 100.0
    query_codes = set(re.findall(r"[a-z][a-z0-9]*", query.lower()))
    title_codes = set(re.findall(r"[a-z][a-z0-9]*", title.lower()))
    if query_codes & title_codes:
        score += 120.0
    similarity = SequenceMatcher(None, normalized_query, normalized_title).ratio()
    if similarity >= 0.45:
        score += similarity * 40.0
    if score == 0.0:
        return 0.0
    if preferred_category and document.metadata.get("category") == preferred_category:
        score += 60.0
    return score


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", value.lower())


def _preferred_category(report_type: str) -> str:
    text = str(report_type or "")
    for keyword, category in CATEGORY_HINTS.items():
        if keyword in text:
            return category
    return ""


def _relative_source(document: Document) -> str:
    category = str(document.metadata.get("category") or "lab_items")
    filename = str(document.metadata.get("filename") or "unknown.md")
    return f"medical_knowledge/{category}/{filename}"
