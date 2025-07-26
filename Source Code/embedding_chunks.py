import os
import json
import pickle
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Constants
CHUNKS_FILE = "Assets\chunks.json"
OUTPUT_FILE = "Assets\embedding_vector_space_chunks.pkl"
MODEL_NAME = "intfloat/e5-base-v2"

# Load model
model = SentenceTransformer(MODEL_NAME)

def embed_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embedded_chunks = []
    print("🔄 Embedding chunks using 'intfloat/e5-base-v2'...")

    for chunk in tqdm(chunks):
        text = chunk.get("content", "").strip()
        if not text:
            continue
        # E5 model expects prefix
        embedding = model.encode("passage: " + text).tolist()
        embedded_chunks.append({
            "section": chunk.get("section", "Unknown"),
            "content": text,
            "page_start": chunk.get("page_start"),
            "page_end": chunk.get("page_end"),
            "embedding": embedding
        })

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(embedded_chunks, f)

    print(f"✅ Embedding completed. Saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    embed_chunks()

