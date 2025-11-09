# semantic_memory.py
import os
import sys
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

EMBED_DIM = 1536


def six_words(text: str) -> str:
    return " ".join(text.split()[:6]) if text else ""


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding


def add_semantic_memory(text: str):
    text = text.lower().strip()

    if "what" in text:
        sys.stderr.write(f"Skipped storing question: {text}\n")
        return

    metadata = {"type": "note", "value": text}

    if "my name is" in text:
        metadata = {"type": "name", "value": text.replace("my name is", "").strip()}

    elif "i love" in text:
        metadata = {"type": "love", "value": text.replace("i love", "").strip()}

    elif "my role is" in text or "i am a" in text:
        metadata = {"type": "role", "value": text.replace("my role is", "").replace("i am a", "").strip()}

    embedding = get_embedding(text)

    index.upsert(
        vectors=[
            {"id": text, "values": embedding, "metadata": metadata}
        ]
    )

    sys.stderr.write(f"Stored semantic memory: {metadata}\n")   # ✅ not stdout


def search_semantic_memory(query: str):
    embedding = get_embedding(query)
    result = index.query(vector=embedding, top_k=15, include_metadata=True)

    loves, roles, names = [], [], []

    for match in result.matches:
        meta = match.metadata or {}
        if meta.get("type") == "love":
            loves.append(meta.get("value"))
        elif meta.get("type") == "role":
            roles.append(meta.get("value"))
        elif meta.get("type") == "name":
            names.append(meta.get("value"))

    q = query.lower()

    if "love" in q and loves:
        return six_words(f"You love {', '.join(set(loves))}")

    if "role" in q and roles:
        return six_words(f"Your role is {roles[-1]}")

    if ("name" in q or "who am i" in q) and names:
        return six_words(f"Your name is {names[-1]}")

    return None


def list_memories():
    stats = index.describe_index_stats()
    total = stats.get("total_vector_count", 0)

    if total == 0:
        return []

    result = index.query(vector=[0] * EMBED_DIM, top_k=total, include_metadata=True)

    return [
        {"id": match.id, "type": match.metadata.get("type"), "value": match.metadata.get("value")}
        for match in result.matches if match.metadata
    ]


def delete_memory(memory_id: str):
    index.delete(ids=[memory_id])
    return True
