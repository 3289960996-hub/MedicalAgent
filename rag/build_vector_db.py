import os
import uuid

import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_core.config import DOCS_DIR, VECTOR_DB_DIR, EMBEDDING_MODEL_NAME
from rag.splitter import split_text

embedding_model = None
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)


def get_embedding_model():
    """
    懒加载 embedding 模型，避免 FastAPI 启动导入模块时访问 HuggingFace。
    """
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return embedding_model


def get_clean_collection():
    """
    每次重新构建知识库时，先删除旧 collection，避免重复写入。
    """
    try:
        client.delete_collection(name="medical_docs")
    except Exception:
        pass

    return client.get_or_create_collection(name="medical_docs")


def build_vector_db() -> str:
    """
    构建医疗知识库。
    读取 data/docs 目录下的 txt 文件，切分后写入 Chroma。
    """

    if not os.path.exists(DOCS_DIR):
        return "文档目录不存在，请先创建 data/docs"

    model = get_embedding_model()
    collection = get_clean_collection()
    count = 0

    for filename in os.listdir(DOCS_DIR):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(DOCS_DIR, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = split_text(text)

        for chunk in chunks:
            doc_id = str(uuid.uuid4())
            embedding = model.encode(chunk).tolist()

            collection.add(
                ids=[doc_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{"source": filename}]
            )

            count += 1

    return f"知识库构建完成，共写入 {count} 个文本片段。"
