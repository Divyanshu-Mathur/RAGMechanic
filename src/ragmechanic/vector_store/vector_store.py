from ..embeddings.embedding import EmbeddingModel
from .chroma_store import ChromaStore
from .faiss_store import FAISSStore
from .qdrant_store import QdrantStore
from .pinecone_store import PineconeStore

class VectorStore:

    def __init__(
        self,
        embedding="BAAI/bge-small-en-v1.5",
        vector_store="chroma",
        collection_name="rag_collection",
    ):

        self.collection_name = collection_name

        self.vector_store = vector_store.lower().strip()

        embedding_model = EmbeddingModel(
            embedding
        ).get()

        if self.vector_store == "chroma":

            self.store = ChromaStore(
                embedding_model,
                collection_name=collection_name,
            )

        elif self.vector_store == "faiss":

            self.store = FAISSStore(
                embedding_model,
                collection_name=collection_name,
            )

        elif self.vector_store == "qdrant":

            self.store = QdrantStore(
                embedding_model,
                collection_name=collection_name,
            )

        elif self.vector_store == "pinecone":

            self.store = PineconeStore(
                embedding_model,
                collection_name=collection_name,
            )

        else:

            supported = [
                "chroma",
                "faiss",
                "qdrant",
                "pinecone",
            ]

            raise ValueError(
                f"Unsupported vector store: '{vector_store}'. "
                f"Supported vector stores: {', '.join(supported)}"
            )



    def add_documents(self, docs):
        print("--- Adding chunks to vector store ---")
        self.store.add_documents(docs)


    def search(self,query,k=5):
        return self.store.similarity_search(
            query,
            k
        )
        
    def as_retriever(self, k=5):
        return self.store.as_retriever(k)