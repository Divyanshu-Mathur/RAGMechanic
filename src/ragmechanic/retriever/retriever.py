from typing import List
from time import perf_counter
from langchain_core.documents import Document


class Retriever:

    def __init__( self,vector_store, search_type: str = "similarity", k: int = 5,):
        self.vector_store = vector_store
        self.search_type = search_type
        self.k = k
        

    def retrieve(self,query: str,):
        start = perf_counter()

        docs = self.vector_store.similarity_search_with_score(
            query,
            k=self.k,
        )

        latency = perf_counter() - start

        retrieved = []

        for rank, (doc, score) in enumerate(docs, start=1):

            doc.metadata.update(
                {
                    "rank": rank,
                    "similarity_score": float(score),
                }
            )

            retrieved.append(doc)
            
        print(f"No. of chunks = {len(retrieved)}")

        return {
            "documents": retrieved,
            "retrieval_latency": latency,
            "num_chunks": len(retrieved),
        }