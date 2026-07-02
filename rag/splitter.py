def split_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    文本切分。
    chunk_size：每个文本块长度。
    overlap：相邻文本块重叠长度，避免上下文断裂。
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks