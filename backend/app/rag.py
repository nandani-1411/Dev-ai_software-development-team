from typing import Self


class RAGManager:
    def __init__(self: Self) -> None:
        self.documents = []

    def add_document(self: Self, doc_id: str, content: str) -> None:
        self.documents.append({"id": doc_id, "content": content})

    def search(self: Self, query: str) -> list[str]:
        return [doc["content"] for doc in self.documents if query.lower() in doc["content"].lower()]
