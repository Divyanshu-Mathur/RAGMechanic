import os

from langchain_qdrant import QdrantVectorStore


class QdrantStore:

    def __init__(
        self,
        embedding,
        persist_directory="./qdrant_db",
        collection_name="rag_collection",
    ):
        self.collection_name = collection_name

        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url:

            self.store = QdrantVectorStore.from_existing_collection(
                embedding=embedding,
                collection_name=collection_name,
                url=qdrant_url,
                api_key=qdrant_api_key,
            )

        else:

            self.store = QdrantVectorStore.from_documents(
                documents=[],
                embedding=embedding,
                collection_name=collection_name,
                path=persist_directory,
            )

    def add_documents(self, docs):
        self.store.add_documents(docs)

    def similarity_search(self, query, k=5):
        return self.store.similarity_search(
            query,
            k=k,
        )

    def similarity_search_with_score(self, query, k=5):
        return self.store.similarity_search_with_score(
            query,
            k=k,
        )

    def max_marginal_relevance_search(self, query, k=5):
        return self.store.max_marginal_relevance_search(
            query,
            k=k,
        )

    def as_retriever(self, k=5):
        return self.store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )