from typing import List, Dict

def build_prompt(question: str, top_chunks: List[Dict], history: List[Dict] = None) -> str:
    """
    Builds a clean, safe, and precise prompt to be sent to the LLM.
    """

    if not top_chunks:
        raise ValueError("No context chunks provided for prompt building.")

    context = "\n\n---\n\n".join(
        f"Section: {chunk['section']} (Pages {chunk['page_start']}-{chunk['page_end']})\n{chunk['content']}"
        for chunk in top_chunks
    )

    # Format chat history (last 3 exchanges only)
    formatted_history = ""
    if history:
        for exchange in history[-3:]:
            formatted_history += f"\nUser: {exchange['question']}\nAssistant: {exchange['answer']}\n"

    prompt = f"""You are a helpful PDF research assistant. You are only allowed to answer using the following context.

Your response must be:
- Shortest and accurate.
- Only based on the PDF context.
- Clearly mention the section and page number where the answer is found.
- If the answer is not in the context, say: "The answer is not in the provided document."
- Praise the history. may the question that the user asking is related to the previous conversation.
- If the user greets you or ask a casual question, respond politely and conversationally.
- If the user asks something unrelated to the PDF, tell them politely that this document does not contain anytopic like that.

Conversation so far:
{formatted_history}

Context:
{context}

User Question: {question}

Your Answer:"""

    return prompt

