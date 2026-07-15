from langchain_core.documents import Document

from medical_knowledge.knowledge_loader import load_medical_knowledge


def test_loads_one_hundred_lab_item_documents():
    documents = load_medical_knowledge()
    assert len(documents) == 100
    assert all(isinstance(item, Document) for item in documents)
    assert all(item.metadata["knowledge_type"] == "lab_item" for item in documents)
    assert all(item.metadata["indicator"] for item in documents)
    assert all("## AI解释规范" in item.page_content for item in documents)
    assert all("直接诊断疾病" in item.page_content for item in documents)
    assert all("推荐药物" in item.page_content for item in documents)
    assert all("制定治疗方案" in item.page_content for item in documents)
