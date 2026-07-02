from rag.retriever import search_docs


def medical_rag_tool(question: str, top_k: int = 3) -> dict:
    docs = search_docs(question, top_k=top_k)

    context = "\n\n".join([
        f"来源：{doc['source']}\n内容：{doc['content']}"
        for doc in docs
    ])

    sources = list(set([doc["source"] for doc in docs]))

    return {
        "context": context,
        "sources": sources,
        "docs": docs
    }
