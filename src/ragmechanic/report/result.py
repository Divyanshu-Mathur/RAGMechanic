from dataclasses import dataclass
from langchain_core.documents import Document
from ..evaluation.result import EvaluationResult


@dataclass
class RAGResult:
    id: int | None
    question: str

    answer: str

    retrieved_documents: list[Document]

    compressed_documents: list[Document]

    retrieval_latency: float

    compression_latency: float

    generation_latency: float

    evaluation: EvaluationResult | None = None
    
    @property
    def total_latency(self):
        return (
            self.retrieval_latency
            + self.compression_latency
            + self.generation_latency
        )
        
    @property
    def retrieved_count(self):
        return len(self.retrieved_documents)
    

    @property
    def compressed_count(self):
        return len(self.compressed_documents)


    @property
    def compression_ratio(self):

        if self.retrieved_count == 0:
            return 0.0

        return (
            1
            - self.compressed_count / self.retrieved_count
        ) * 100


    @property
    def similarity_scores(self):

        return [
            doc.metadata.get("similarity_score")
            for doc in self.retrieved_documents
        ]


    @property
    def sources(self):

        return list(
            dict.fromkeys(
                doc.metadata.get("source", "Unknown")
                for doc in self.retrieved_documents
            )
        )
        