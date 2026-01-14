import re
import ast
import json 
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from core.converter import JsonLangChainDocumentMapper
from core.metadata_loader import Update
from core.document_tools import JsonFileIO, Previewer

SPLITTERS = {
    "pdf": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        ),
        "method": "split_documents"
    },
    "docx": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        ),
        "method": "split_documents"
    },
    "txt": {
        "splitter": RecursiveCharacterTextSplitter(
            chunk_size=500,
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

HTML_SIZE_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def split_documents(docs):
    chunks = []

    for doc in docs:
        fmt = doc.metadata.get("format", "txt")
        config = SPLITTERS.get(fmt, SPLITTERS["txt"])

        splitter = config["splitter"]
        method = config["method"]

        # Case 1: normal document-based splitters (pdf, txt, docx, ppt)
        if method == "split_documents":
            chunks.extend(splitter.split_documents([doc]))

        # Case 2: HTML / URL (header split → size split)
        else:
            sections = splitter.split_text(doc.page_content)

            # convert header sections → Documents
            section_docs = [
                Document(
                    page_content=section.page_content,
                    metadata={**doc.metadata, **section.metadata},
                )
                for section in sections
            ]

            # enforce chunk size AFTER headers
            sized_chunks = HTML_SIZE_SPLITTER.split_documents(section_docs)
            chunks.extend(sized_chunks)

    return chunks

converter = JsonLangChainDocumentMapper()
data = json.loads(Path("E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/processed/all_documents.json").read_text(encoding="utf-8"))
docs= converter.json_to_documents(data)
chunks= split_documents(docs)

assign_chunk = Update()

assign_chunk.update_chunks(chunks)

json = JsonFileIO()

json.save(chunks,"E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/chunks/all_chunks.json")
