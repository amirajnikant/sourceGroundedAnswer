import re
import ast
import json 
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter

class DocumentConverter:
    def json_to_langchainDocs(self, path):
        with open(Path(path), "r", encoding="utf-8") as f:
            raw_data= json.load(f)
        docs= []
        for item in raw_data:
            docs.append(
                Document(
                    page_content=item["page_content"],
                    metadata= item["metadata"]
                )
            )
        return docs

    def langchainDocs_to_json(self, path):
        with open(Path(path), "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
        json_output = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and node.func.id == "Document":
                metadata = {}
                page_content = ""
                for kw in node.keywords:
                    if kw.arg == "metadata":
                        metadata = ast.literal_eval(kw.value)
                    elif kw.arg == "page_content":
                        page_content = kw.value.value
                json_output.append(
                    {
                        "metadata": metadata,
                        "page_content": page_content
                    }
                )
        return json_output
    

SPLITTERS = {
    "pdf": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        ),
        "method": "split_documents"
    },
    "docx": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        ),
        "method": "split_documents"
    },
    "txt": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        ),
        "method": "split_documents"
    },
    "ppt": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        ),
        "method": "split_documents"
    },
    "html": {
        "splitter": HTMLHeaderTextSplitter(
            headers_to_split_on=[
                ("h1", "header_1"),
                ("h2", "header_2"),
                ("h3", "header_3"),
            ]
        ),
        "method": "split_text"
    },
    "url": {
        "splitter": HTMLHeaderTextSplitter(
            headers_to_split_on=[
                ("h1", "header_1"),
                ("h2", "header_2"),
            ]
        ),
        "method": "split_text"
    },
}

def split_documents(docs):
    chunks = []

    for doc in docs:
        fmt = doc.metadata.get("format", "txt")
        config = SPLITTERS.get(fmt, SPLITTERS["txt"])

        splitter = config["splitter"]
        method = config["method"]

        if method == "split_documents":
            chunks.extend(splitter.split_documents([doc]))

        else:  # split_text
            sections = splitter.split_text(doc.page_content)
            for section in sections:
                chunks.append(
                    Document(
                        page_content = section.page_content,
                        metadata = section.metadata
                    )
                )

    return chunks

docs= DocumentConverter().json_to_langchainDocs("E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/all_documents.json")
chunks= split_documents(docs)
