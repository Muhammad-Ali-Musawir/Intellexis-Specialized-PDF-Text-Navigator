# QueryLens (general)
import streamlit as st
from embedding_question import embed_question
from top_chunks_searcher import get_top_chunks
from prompt_builder import build_prompt
from llm_handler import ask_llm
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set Streamlit page config
st.set_page_config(
    page_title="Intellexis: Specialized PDF Text Navigator",
    layout="centered",
    page_icon="Source Code/Assets/icon.ico"
)

# Encode logo to base64
logo_base64 = get_base64_image("Source Code/Assets/logo.png")

# Inline logo + single-line title
st.markdown(
    f"""
    <div style="display: flex; align-items: center; white-space: nowrap; overflow: hidden;">
        <img src="data:image/png;base64,{logo_base64}" width="110" style="margin-right: 10px;">
        <span style="font-size: 2em; font-weight: bold;">Intellexis: Specialized PDF Text Navigator</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Ask any question based on the uploaded PDF knowledge base.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display full conversation in order
for item in st.session_state.history:
    with st.chat_message("user", avatar="🧠"):
        st.markdown(item["question"])
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(item["answer"])

# Chat input (bottom, with Enter or Send button)
question = st.chat_input("Type your question here...")

if question:
    # Display user message immediately
    with st.chat_message("user", avatar="🧠"):
        st.markdown(question)

    try:
        with st.spinner("🔎 Embedding your question..."):
            question_vector = embed_question(question)

        with st.spinner("📚 Finding relevant chunks..."):
            top_chunks = get_top_chunks(question_vector, top_k=5)

        with st.spinner("🧩 Building prompt..."):
            prompt = build_prompt(question, top_chunks, st.session_state.history)

        with st.spinner("💬 Asking the LLM..."):
            answer = ask_llm(prompt)

        # Display assistant message
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)

        # Save to history
        st.session_state.history.append({
            "question": question,
            "chunks": top_chunks,
            "answer": answer
        })

    except Exception as e:
        st.error(f"❌ Error: {e}")

