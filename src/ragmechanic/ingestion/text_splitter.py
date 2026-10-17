from typing import List
from tqdm import tqdm
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    def __init__(self,chunk_size: int = 800,chunk_overlap: int = 150,separators: list[str] | None = None,):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if separators is None:
            separators = ["\n\n","\n",". "," ","",]

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=separators,
        )
        

    def split( self, documents: List[Document],) -> List[Document]:

        chunks = self.splitter.split_documents(documents)
        print("--- Splitting Documents ---")
        for idx, chunk in enumerate(tqdm(chunks, desc="Processing chunks", unit="chunk"),start=1,):
            chunk.metadata["chunk_id"] = idx + 1
            chunk.metadata["chunk_size"] = len(chunk.page_content)

        return chunks