from typing import List, Dict, Any
from langchain_core.documents import Document

class JsonLangChainDocumentMapper:
    def json_to_documents(self, docs: List[Dict[str,any]]):
        langchain_docs = []
        for doc in docs:
            langchain_docs.append(
                Document(
                    page_content= doc["page_content"],
                    metadata= doc["metadata"]
                )
            )
        return langchain_docs
    
    def documents_to_json(self, docs: List[Document]):
        json_docs = []
        for doc in docs:
            json_docs.append(
                {
                    "metadata": doc.metadata,
                    "page_content" : doc.page_content
                }
            )
        return json_docs
    