from sentence_transformers import SentenceTransformer

# Load the same model used for chunks
MODEL_NAME = "intfloat/e5-base-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_question(question: str):
    """
    Embeds a user question into a vector using the same embedding model.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # E5 model expects prefix for questions
    return model.encode("query: " + question).tolist()

