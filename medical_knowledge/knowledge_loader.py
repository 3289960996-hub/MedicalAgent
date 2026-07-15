from pathlib import Path

from langchain_core.documents import Document


KNOWLEDGE_ROOT = Path(__file__).resolve().parent


def load_medical_knowledge(root: str | Path | None = None) -> list[Document]:
    """Load laboratory Markdown files as deterministic LangChain Documents."""
    base_dir = Path(root).resolve() if root else KNOWLEDGE_ROOT
    documents: list[Document] = []

    for path in sorted(base_dir.rglob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        documents.append(Document(
            page_content=content,
            metadata={
                "knowledge_type": "lab_item",
                "indicator": _extract_title(content),
                "category": path.parent.relative_to(base_dir).as_posix(),
                "filename": path.name,
                "source": str(path.resolve()),
            },
        ))

    return documents


def _extract_title(content: str) -> str:
    first_line = content.splitlines()[0].strip()
    return first_line.removeprefix("#").strip() or "未命名指标"
