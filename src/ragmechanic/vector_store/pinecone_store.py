import os

from langchain_pinecone import PineconeVectorStore


class PineconeStore:

    def __init__(
        self,
        embedding,
        persist_directory="./pinecone_db",
        collection_name="rag_collection",
    ):
        self.collection_name = collection_name

        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv(
            "PINECONE_INDEX_NAME",
            collection_name,
        )

        if not api_key:
            raise ValueError(
                "PINECONE_API_KEY environment variable is required."
            )

        if not index_name:
            raise ValueError(
                "PINECONE_INDEX_NAME environment variable is required."
            )

        self.store = PineconeVectorStore(
            index_name=index_name,
            embedding=embedding,
            pinecone_api_key=api_key,
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