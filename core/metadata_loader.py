import json
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.documents import Document

LANGCHAINDOCS_DIR = Path("")

class Update:
    def update_metadata(self, docs: List[Document]):
        for i,doc in enumerate(docs):
            source= Path(doc.metadata.get("source",""))
            doc.metadata["file_name"] = source.name
            doc.metadata["format"] = source.suffix.lstrip(".").lower()
        return docs
    
    def update_chunks(self, docs: List[Document]):
        for i,doc in enumerate(docs):
            doc.metadata["chunk_no"] = i
            file_name = Path(doc.metadata.get("source","unknown")).name
            doc.metadata["chunk_id"] = f"chunk_{i}::{file_name}"
        return docs
    

