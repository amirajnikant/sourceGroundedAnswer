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




from typing import Callable, Dict, List

RAW_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/raw/"
)

PROCESSED_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/chunks/"
)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "all_chunks.json"

class MetadataStage2:
    """
    Stage 2:
    - Convert LangChain Documents into final chunk dictionaries
    - Add chunk_id (outside metadata)
    - Normalize metadata
    - Save / load / preview chunks
    """

    # ---------- normalize ----------

    def normalize(self, docs: List[Document]) -> List[Dict]:
        chunks: List[Dict] = []

        for idx, d in enumerate(docs):
            source = d.metadata.get("source")
            doc_name = Path(source).name if source else None

            page = d.metadata.get("page", idx + 1)

            chunk = {
                "chunk_id": idx,
                "chunk_text": d.page_content,
                "metadata": {
                    **d.metadata,
                    "doc_name": doc_name,
                    "page": page,
                },
            }

            chunks.append(chunk)

        return chunks

    # ---------- save ----------

    def save_all(self, chunks: List[Dict]) -> None:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(
                chunks,
                f,
                indent=2,
                ensure_ascii=False,
            )

    # ---------- load ----------

    def load_all(self) -> List[Dict]:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------- preview ----------

    def preview(self, chunks: List[Dict], chars: int = 200) -> None:
        print(f"\nTotal chunks: {len(chunks)}\n")

        for i, c in enumerate(chunks):
            text = (c.get("chunk_text") or "")[:chars].replace("\n", " ")
            print(f"[{i}] {text}...")
            print(f"    chunk_id: {c.get('chunk_id')}")
            print(f"    metadata: {c.get('metadata')}\n")


# -------------------------------------------------------------------
# Example usage (THIS is how you call it)
# -------------------------------------------------------------------

# docs = DocumentConverter().json_to_langchainDocs("path/to/all_documents.json")
# chunks = split_documents(docs)

stage2 = MetadataStage2()
chunks = stage2.normalize(chunks)
stage2.save_all(chunks)
stage2.preview(chunks)