# from chunking.splitter import DocumentConverter
# from langchain_core.documents import Document
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS

# converter= DocumentConverter()

# docs= converter.json_to_langchainDocs("E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/chunks/all_chunks.json")

# docs_for_embedding = [
#     Document(
#         page_content=chunk["chunk_text"],   # ONLY text is embedded
#         metadata={
#             "chunk_id": chunk["chunk_id"],
#             **chunk["metadata"],
#         },
#     )
#     for chunk in docs
# ]

# embeddings = OllamaEmbeddings(
#     model="nomic-embed-text"
# ) 

# vectorstore = FAISS.from_documents(
#     documents=docs_for_embedding,
#     embedding=embeddings
# )

# results = vectorstore.similarity_search(
#     "acute leukemia diagnosis",
#     k=3
# )

# from pathlib import Path

# VECTORSTORE_DIR = Path(
#     "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/vectorstore"
# )

# VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
# print("before")
# vectorstore.save_local(VECTORSTORE_DIR)
# print("after")




import json
from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# Load chunks AS DICTS (correct)
# --------------------------------------------------

CHUNKS_FILE = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/chunks/all_chunks.json"
)

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)   # <-- list of dicts


# --------------------------------------------------
# Convert dict chunks -> Documents for embedding
# --------------------------------------------------

MAX_CHARS = 2000   # safe for nomic-embed-text

docs_for_embedding = []

for chunk in chunks:
    text = chunk["chunk_text"]

    if not text:
        continue

    if len(text) > MAX_CHARS:
        # split aggressively or truncate
        text = text[:MAX_CHARS]

    docs_for_embedding.append(
        Document(
            page_content=text,
            metadata={
                "chunk_id": chunk["chunk_id"],
                **chunk["metadata"],
            },
        )
    )



# --------------------------------------------------
# Embeddings (Ollama)
# --------------------------------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# --------------------------------------------------
# Create FAISS vector store
# --------------------------------------------------
VECTORSTORE_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/vectorstore/faiss"
)

VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

vectorstore = FAISS.from_documents(
    documents=docs_for_embedding,
    embedding=embeddings
)

# vectorstore = FAISS.load_local(
#     VECTORSTORE_DIR,
#     embeddings,
#     allow_dangerous_deserialization=True
# )



# --------------------------------------------------
# Test search
# --------------------------------------------------

results = vectorstore.similarity_search(
    "acute leukemia diagnosis",
    k=3
)

for r in results:
    print(r.metadata["chunk_id"])
    print(r.page_content[:200])
    print()


# --------------------------------------------------
# Save FAISS index (EXPLICIT PATH)
# --------------------------------------------------


print("before save")
vectorstore.save_local(VECTORSTORE_DIR)
print("after save")
