import json
from pathlib import Path
from typing import Callable, Dict, List, Optional
from langchain_community.document_loaders import (DirectoryLoader,PyPDFLoader,TextLoader,UnstructuredHTMLLoader,UnstructuredWordDocumentLoader,UnstructuredPowerPointLoader,WebBaseLoader,)
from langchain_core.documents import Document
from core.metadata_loader import Update
from core.document_tools import JsonFileIO, Previewer

RAW_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
)
PROCESSED_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/"
)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = PROCESSED_DIR / "all_documents.json"

def make_directory_loader(glob_pattern: str, loader_cls) -> Callable[[], List[Document]]:
    def load():
        return DirectoryLoader(
            path=str(RAW_DIR),
            glob=glob_pattern,
            loader_cls=loader_cls,
        ).load()
    return load

def make_url_loader(urls: List[str]) -> Callable[[], List[Document]]:
    def load():
        return WebBaseLoader(urls).load()
    return load

SOURCE_LOADERS: Dict[str, Callable[[], List[Document]]] = {
    "pdf": make_directory_loader("**/*.pdf", PyPDFLoader),
    "pptx": make_directory_loader("**/*.pptx", UnstructuredPowerPointLoader),
    "txt": make_directory_loader("**/*.txt", TextLoader),
    "html": make_directory_loader("**/*.html", UnstructuredHTMLLoader),
    "docx": make_directory_loader("**/*.docx", UnstructuredWordDocumentLoader),
    "url": make_url_loader(
        [
            "https://www.sciencenews.org/",
            "https://www.sciencedaily.com/",
        ]
    ),
}

def all_source_loader(sources: Optional[List[str]] = None) -> List[Document]:
    all_docs: List[Document] = []

    if sources is None:
        sources = list(SOURCE_LOADERS.keys())

    for source in sources:
        if source not in SOURCE_LOADERS:
            raise ValueError(f"Unknown source type: {source}")

        loader_fn = SOURCE_LOADERS[source]
        docs = loader_fn()
        all_docs.extend(docs)

    return all_docs


output = all_source_loader()

assign_metadata = Update()
final_output = assign_metadata.update_metadata(output)

obj = JsonFileIO()
obj.save(final_output,"E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/all_documents.json")