from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    TextLoader
)

from functools import partial

 
class DocumentLoader:
    """
    Load supported documents from a file or documents. 
    Supported:
    - PDF
    - DOCX
    - PPTX
    - TXT
    """
    
    SUPPORTED_LOADERS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".pptx": UnstructuredPowerPointLoader,
        ".txt": TextLoader
    }
    
    
    def __init__( self, path: Union[str, Path, List[Union[str, Path]]], recursive: bool = True,):
        if isinstance(path, (str, Path)):
            self.paths = [Path(path)]
        else:
            self.paths = [Path(p) for p in path]

        self.recursive = recursive
        
    
    
    def _load_single_file(self, file_path: Path) -> List[Document]:
        extension = file_path.suffix.lower()
        
        if extension not in self.SUPPORTED_LOADERS:
            print(f"Skipping unsupported file: {file_path.name}")
            return []
        print(f"File Loading = {file_path}")
        
        if extension == ".txt":
            docs  = self.load_text(file_path)
        else:
            loader = self.SUPPORTED_LOADERS[extension](str(file_path))
            docs = loader.load()
        
        for doc in docs:
            doc.metadata.setdefault("page", 1)

            doc.metadata.update(
                {
                    "source": file_path.name,
                    "file_path": str(file_path.resolve()),
                    "extension": extension,
                }
            )

        return docs


    def load_text(self,file_path: Path):
            for enc in ["utf-8", "utf-8-sig", "cp1252", "latin-1"]:
                try:
                    return TextLoader(str(file_path), encoding=enc).load()
                except UnicodeDecodeError:
                    continue
    
            raise RuntimeError(f"Cannot decode {file_path}")
    

    # def load(self) -> List[Document]:
    #     documents = []
    #     print("--- Loading Documents ---")

    #     if self.path.is_file():
    #         return self._load_single_file(self.path)

    #     iterator = (
    #         self.path.rglob("*")
    #         if self.recursive
    #         else self.path.glob("*")
    #     )

    #     for file in iterator:
    #         if file.is_file():
    #             print(f"Loading {file}")
    #             documents.extend(self._load_single_file(file))

    #     print(f"Loaded {len(documents)} document chunks.")

    #     return documents
    
    
    def load(self) -> List[Document]:
        documents = []

        print("--- Loading Documents ---")

        for path in self.paths:

            if not path.exists():
                print(f"Path does not exist: {path}")
                continue

            # Single file
            if path.is_file():
                print("Single File")
                documents.extend(
                    self._load_single_file(path)
                )
                continue

            # Directory
            iterator = (
                path.rglob("*")
                if self.recursive
                else path.glob("*")
            )

            for file in iterator:
                if file.is_file():
                    print(f"Loading {file}")
                    documents.extend(
                        self._load_single_file(file)
                    )

        print(f"Loaded {len(documents)} documents.")

        return documents
    
    
    