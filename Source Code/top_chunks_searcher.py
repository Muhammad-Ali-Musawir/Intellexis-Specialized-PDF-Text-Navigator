import os
import pickle
import numpy as np
from typing import List, Dict

# Constants
EMBEDDING_FILE = "Assets/embedding_vector_space_chunks.pkl"


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Computes cosine similarity between two vectors.
    """
    v1, v2 = np.array(vec1), np.array(vec2)
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def load_chunks() -> List[Dict]:
    """
    Loads the precomputed vectorized chunks from the pickle file.
    """
    if not os.path.exists(EMBEDDING_FILE):
        raise FileNotFoundError(f"Embedding file '{EMBEDDING_FILE}' not found.")
    
    with open(EMBEDDING_FILE, "rb") as f:
        return pickle.load(f)


def get_top_chunks(query_vector: List[float], top_k: int = 5) -> List[Dict]:
    """
    Returns the top-k most relevant chunks based on cosine similarity to the query vector.
    """
    chunks = load_chunks()
    scored_chunks = []

    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["embedding"])
        scored_chunks.append((score, chunk))

    # Sort by similarity score in descending order
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # Return only the chunk dictionaries
    return [item[1] for item in scored_chunks[:top_k]]

