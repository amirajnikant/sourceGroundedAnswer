import re
import json
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from langchain_ollama import OllamaEmbeddings
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from langchain_community.vectorstores import FAISS
from core.converter import JsonLangChainDocumentMapper
from langchain_community.retrievers import BM25Retriever

CHUNKS_FILE = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/chunks/all_chunks.json"
)
VECTORSTORE_DIR = Path(
    "E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/vectorstore/faiss"
)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

docs_for_embedding = json.loads(Path(CHUNKS_FILE).read_text(encoding="utf-8"))
json_to_doc = JsonLangChainDocumentMapper()
docs_for_embedding = json_to_doc.json_to_documents(docs_for_embedding)


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# vectorstore = FAISS.from_documents(
#     documents=docs_for_embedding,
#     embedding=embeddings
# )

# vectorstore.save_local(VECTORSTORE_DIR)

vectorstore = FAISS.load_local(
    VECTORSTORE_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

bm25_retriever = BM25Retriever.from_documents(docs_for_embedding)

def bm25_query_update(query: str) -> str:
    tokens = re.findall(r"[a-zA-Z0-9\-]+", query.lower())
    keywords = [
        t for t in tokens
        if t not in ENGLISH_STOP_WORDS and len(t) > 2
    ]
    return " ".join(keywords)

query = "Explain the clinical management and diagnostic workflow for acute leukemia in adults"

dense_query = query
bm25_query = bm25_query_update(query)

dense_results = vectorstore.similarity_search(
    query=dense_query,
    k=10
)

bm25_retriever.k = 10
bm25_results = bm25_retriever.invoke(bm25_query)

def merge_deduplicate(bm25_docs, dense_docs, max_candidates):
    candidates = {}
    i = 1
    while i < len(bm25_docs) or i < len(dense_docs):
        if i < len(bm25_docs):
            doc = bm25_docs[i]
            chunk_id = doc.metadata["chunk_id"]
            if chunk_id not in candidates:
                candidates[chunk_id] = doc
            
        if len(candidates) >= max_candidates:
            break

        if i < len(dense_docs):
            doc = dense_docs[i]
            chunk_id = doc.metadata["chunk_id"]
            if chunk_id not in candidates: 
                candidates[chunk_id] = doc

        if len(candidates) >= max_candidates:
            break

        i+=1


    return list(candidates.values())

candidate_chunks = merge_deduplicate(bm25_results, dense_results, 15)

RERANKER = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
)

def rerank_candidate(query: str, docs: List[Document], top_n: int):
    pairs = []
    for doc in docs:
        pairs.append((query,doc.page_content))

    scores = RERANKER.predict(
        pairs, 
        batch_size=16,
        show_progress_bar= False
    )

    indices = list(range(len(scores)))

    indices.sort(key=lambda i: scores[i], reverse=True)

    reranked_docs = []
    for i in indices[:top_n]:
        reranked_docs.append(docs[i])

    return reranked_docs

rerank_docs = rerank_candidate(query,candidate_chunks,10)
print(rerank_docs)

converter = JsonLangChainDocumentMapper()
RERANKED_PATH = Path("E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/reranked_docs/reranked_docs.json")
with open(RERANKED_PATH, "w", encoding="utf-8") as f:
    json.dump(
        converter.documents_to_json(rerank_docs),
        f,
        ensure_ascii=False,
        indent=2
    )