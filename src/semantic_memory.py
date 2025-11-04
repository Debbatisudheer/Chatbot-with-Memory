import chromadb
from openai import OpenAI
import os

# ✅ Load OpenAI key (make sure OPENAI_API_KEY is set in environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Initialize ChromaDB (local persistent vector DB)
chroma_client = chromadb.PersistentClient(path="./chroma-db")

collection = chroma_client.get_or_create_collection(
    name="chatbot_memory",
    metadata={"hnsw:space": "cosine"}  # cosine = similarity search
)


def add_semantic_memory(text: str):
    """Store memory sentence into Vector DB"""
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

    collection.add(
        ids=[text],             # we use the sentence itself as the ID
        documents=[text],       # stored text
        embeddings=[embedding]  # vector of the text
    )


def search_semantic_memory(query: str):
    """Search meaning-based memory"""
    embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    result = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )

    if result and result["documents"] and result["documents"][0]:
        return result["documents"][0][0]   # return best match

    return None
