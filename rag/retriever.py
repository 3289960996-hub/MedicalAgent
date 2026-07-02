import chromadb
from sentence_transformers import SentenceTransformer

from agent_core.config import VECTOR_DB_DIR, EMBEDDING_MODEL_NAME

embedding_model = None
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = client.get_or_create_collection(name="medical_docs")


def get_embedding_model():
    """
    懒加载 embedding 模型，避免 FastAPI 启动导入模块时访问 HuggingFace。
    """
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return embedding_model


def search_docs(query: str, top_k: int = 3) -> list[dict]:
    """
    根据用户问题检索最相关的医疗文档片段。
    """

    try:
        query_embedding = get_embedding_model().encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = []

        if not results["documents"] or not results["documents"][0]:
            return docs

        for i in range(len(results["documents"][0])):
            docs.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"]
            })

        return docs

    except Exception:
        return []
