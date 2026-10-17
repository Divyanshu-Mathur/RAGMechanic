from time import perf_counter

from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_core.prompts import PromptTemplate

from ..compression.result import CompressionResult


class Compressor:

    def __init__(self, llm):

        prompt = PromptTemplate(
            input_variables=["question", "context"],
            template="""
You are a document compression system for a RAG pipeline.

Extract information relevant to answering the question.

IMPORTANT:
- Preserve names, entities, IDs, registration numbers, dates,
  headings, and other identifying information when they establish
  the relationship to the answer.
- Never return an isolated value if its associated entity is needed
  to understand that value.
- The compressed text must be self-contained.
- Do not invent information.
- Remove only irrelevant information.

Example:

Question:
What is the registration number of Divyanshu Mathur?

Document:
Submitted By
Divyanshu Mathur
Reg. No.:22BDS0100
B.Tech. Computer Science

Correct:
Divyanshu Mathur — Reg. No.:22BDS0100

Incorrect:
Reg. No.:22BDS0100

Question:
{question}

Document:
{context}

Relevant information:
"""
        )

        self.compressor = LLMChainExtractor.from_llm(
            llm,
            prompt=prompt,
        )

    def compress(self, query: str, retrieved_documents):

        start = perf_counter()

        docs = self.compressor.compress_documents(
            retrieved_documents,
            query,
        )

        latency = perf_counter() - start

        ratio = (
            1 - len(docs) / len(retrieved_documents)
            if retrieved_documents
            else 0
        )

        return CompressionResult(
            original_documents=retrieved_documents,
            compressed_documents=docs,
            compression_latency=latency,
            compression_ratio=ratio,
        )