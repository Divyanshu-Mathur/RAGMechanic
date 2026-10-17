from dataclasses import dataclass
from langchain_core.documents import Document

@dataclass
class CompressionResult:
    original_documents: list[Document]
    compressed_documents: list[Document]
    compression_latency: float
    compression_ratio: float