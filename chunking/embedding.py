from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(
    model="nomic-embed-text"
)

vector = emb.embed_query("I forgot my password")

print(vector)
print(len(vector))