import os

from langchain_community.vectorstores import FAISS


class FAISSStore:

    def __init__(
        self,
        embedding,
        persist_directory="./faiss_db",
        collection_name="rag_collection",
    ):
        self.embedding = embedding
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        self.store = None

        # Load existing FAISS index if available
        index_file = os.path.join(
            persist_directory,
            "index.faiss",
        )

        if os.path.exists(index_file):
            self.store = FAISS.load_local(
                persist_directory,
                embeddings=embedding,
                allow_dangerous_deserialization=True,
            )

    def add_documents(self, docs):

        if self.store is None:
            self.store = FAISS.from_documents(
                docs,
                self.embedding,
            )
        else:
            self.store.add_documents(docs)

        os.makedirs(
            self.persist_directory,
            exist_ok=True,
        )

        self.store.save_local(
            self.persist_directory,
        )

    def similarity_search(self, query, k=5):
        if self.store is None:
            return []

        return self.store.similarity_search(
            query,
            k=k,
        )

    def similarity_search_with_score(self, query, k=5):
        if self.store is None:
            return []

        return self.store.similarity_search_with_score(
            query,
            k=k,
        )

    def max_marginal_relevance_search(self, query, k=5):
        if self.store is None:
            return []

        return self.store.max_marginal_relevance_search(
            query,
            k=k,
        )

    def as_retriever(self, k=5):
        if self.store is None:
            raise ValueError(
                "FAISS vector store is empty. "
                "Add documents before creating a retriever."
            )

        return self.store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )