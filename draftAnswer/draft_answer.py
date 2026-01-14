import re
import json
from pathlib import Path
from core.converter import JsonLangChainDocumentMapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

RERANKED_PATH = Path("E:/OneDrive/Documents/GitHub/sourceGroundedAnswer/data/reranked_docs/reranked_docs.json")

converter = JsonLangChainDocumentMapper()

with open(RERANKED_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

candidate_chunks = converter.json_to_documents(data)

def format_chunks_for_llm(chunks):
    formatted = []
    for doc in chunks:
        cid = doc.metadata["chunk_id"]
        text = doc.page_content.strip()
        formatted.append(f"[{cid}]\n{text}")

    return "\n\n".join(formatted)

context = format_chunks_for_llm(candidate_chunks)

template = PromptTemplate(
    template="""You must answer the question using ONLY the information in the chunks below.

Rules:
- Every sentence MUST end with a citation in square brackets, using the chunk_id.
- Use ONLY the provided chunk_ids.
- Do NOT combine multiple facts into one sentence.
- Do NOT add interpretations, summaries, or conclusions.
- Each line must contain EXACTLY ONE claim.
- If the answer is not explicitly stated in the chunks, output exactly: REFUSE




Question:
{question}

Chunks:
{context}

Answer:
""",
input_variables=["quesiton","context"]
)

model = ChatGoogleGenerativeAI(
    model = "models/gemini-flash-latest",
    temperature= 0
)

parser = StrOutputParser()
# query = "explain what CKM syndrome is and what amino acid does"
query = "what is CKM Syndrome. answer in 5 points"

chain = template | model | parser
response = chain.invoke({
    "context": context,
    "question": query
})

CHUNK_PATTERN = re.compile(
    r"(.*?)\s*\[chunk_(\d+)\]",
    re.DOTALL
)

def extract_claims(text: str) -> str:
    claims = []

    matches = CHUNK_PATTERN.findall(text)
    for chunk_text, chunk_id in matches:
        claim = {
            "chunk_text": chunk_text.strip(),
            "chunk_id": f"[chunk_{int(chunk_id)}]",
        }
        claims.append(claim)

    return claims

draft_answer = extract_claims(response)
print(draft_answer)