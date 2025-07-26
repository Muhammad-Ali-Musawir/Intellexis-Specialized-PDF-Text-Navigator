# 🧠 Intellexis - Specialized PDF Text Navigator

Intellexis is a streamlined and intelligent **static PDF-based research assistant**. It allows you to interact with PDF documents conversationally, returning highly **accurate, concise, and strictly in-document** responses — all with proper section references.

---

## 🚀 Purpose

This tool enables fast and precise exploration of long PDF documents by allowing you to ask natural language questions and receive context-aware answers **only from the uploaded PDF**.

---

## 📄 Starting with Desired PDF

To start using the chatbot with your desired PDF, follow these steps:

1. 📂 **Place Your File**: Move your target PDF into the `Assets` folder and rename it as `document.pdf`.
2. ⚙️ **Run Setup**: Do the setup that is told below in the `Setup Instructions` section.
3. 💬 **Ask Away**: Begin interacting with the assistant to extract insights or ask questions from the document.

> _Note: Ensure your PDF is text-based for accurate results._

---

## 🖥️ Live Preview

> 💡 **Try it instantly**:  
A ready-to-use version of the web application is included. Navigate to the  
📁 `website Application` folder and double-click  
🔹 **Intellexis - Specialized PDF Text Navigator.exe**  
to run the app — **no installation required!**

---

## 🎯 Key Features

- ✅ **PDF-only answers** – no hallucinations, no off-topic replies  
- 📌 **Cites exact section** or location within the PDF  
- ✍️ Supports casual/natural questions as well  
- 🚫 Clearly states if a topic is not found in the document  
- ⚡ Fast and accurate with high precision chunk retrieval  
- 🧠 Embedded vector similarity-based search for top relevant sections

---

## ⚙️ Technologies Used

- `Python 3.10+`
- `streamlit`
- `requests`
- `python-dotenv`
- `PyMuPDF`
- `tiktoken`
- `numpy`
- `scikit-learn`
- `tqdm`
- `sentence-transformers`
- `pickle-mixin`
- `typing-extensions`

---

## 🗂️ Project Structure

```
Intellexis - Specialized PDF Text Navigator/
├── Source Code/
│ ├── .streamlit/
│ │ └── config.toml
│ ├── pycache/
│ │ └── *.pyc
│ ├── Assets/
│ │ ├── extracted_images/
│ │ ├── .env
│ │ ├── chunks.json
│ │ ├── document.pdf
│ │ ├── embedding_vector_space_chunks.pkl
│ │ ├── icon.ico
│ │ ├── logo.png
│ │ ├── raw_extraction.json
│ │ └── requirements.txt
│ ├── VirtualEnvironment/           (you can make your own virtual environment)
│ ├── embedding_chunks.py
│ ├── embedding_question.py
│ ├── extract_and_chunk.py
│ ├── launcher.py
│ ├── llm_handler.py
│ ├── main.py
│ ├── prompt_builder.py
│ └── top_chunks_searcher.py
├── website Application/
│ └── Intellexis - Specialized PDF Text Navigator.exe
├── LICENSE
└── README.md                       (you are here)
```

---

## 🛠️ Setup Instructions

1. **Install dependencies**  
   Run:
   ```
   pip install -r Assets/requirements.txt
   ```

2. **Configure API keys**  
   Inside `Assets`, create a `.env` file with the following contents:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=model_name_that_you_want_to_use
   ```

3. **Extract and chunk the PDF
   Run:
   ```
   python extract_and_chunk.py
   ```

4. **Vectorize the chunks**  
   Run:
   ```
   python embedding_chunks.py
   ```

5. **Launch the App**  
   Option 1:
   ```
   streamlit run main.py
   ```
   Option 2:
   ```
   python launcher.py
   ```

---

## 👨‍💻 Author

**Muhammad Ali Musawir**
Feel free to connect or fork this project to build your own PDF-specific assistants!

---

## 📌 Disclaimer

- This assistant is designed only for **static PDFs** bundled inside the `Assets` folder.

- External PDF upload support will be part of future dynamic versions.

- Ensure API key usage complies with OpenRouter’s fair-use policies.

---

**✨ Built with precision and purpose. No hallucinations. Just accurate PDF knowledge.**

Let me know if you want:

- 🏷️ Badges (e.g., Python version, license, dependencies)

- 📸 Screenshot section

- 🌐 GitHub Pages / Hugging Face / Streamlit Cloud deployment guide