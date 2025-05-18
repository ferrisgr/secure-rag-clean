# PDF Insight 🔍

A lightweight PDF-based RAG assistant that lets users upload PDFs and ask questions in natural language. Built with Streamlit and deployed on Render.

## 🚀 Features
- Drag-and-drop PDF upload
- Role-based prompts (Analyst, Reviewer, Admin)
- Chat history + source toggle
- Export chat to CSV
- Fully containerized with Docker
- Deployed on Render

## ⚙️ Tech Stack
- **Frontend:** Streamlit
- **RAG Logic:** LangChain, FAISS, OpenAI
- **PDF Parsing:** PyMuPDF
- **Embedding:** OpenAI Embeddings
- **Backend:** Python
- **Deployment:** Docker + Render

## 🧠 How it Works
1. Upload a PDF file (e.g. 10-K, reports)
2. It gets parsed and chunked using PyMuPDF
3. Chunks are embedded into FAISS vector store
4. User queries are matched with top chunks
5. LangChain chain generates a response based on role

## 🛠️ Local Setup

```bash
git clone https://github.com/ferrisgr/secure-rag-clean
cd pdf-insight
pip install -r requirements.txt
streamlit run app.py

OPENAI_API_KEY=your_key_here
