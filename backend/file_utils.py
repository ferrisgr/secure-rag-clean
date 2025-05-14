import os
import streamlit as st

# Ensure documents folder exists
def ensure_doc_folder(doc_folder: str = "documents"):
    os.makedirs(doc_folder, exist_ok=True)

# Upload PDF via drag-and-drop
def handle_file_upload(doc_folder: str = "documents"):
    uploaded_file = st.sidebar.file_uploader("📄 Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        save_path = os.path.join(doc_folder, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded: {uploaded_file.name}")
        st.rerun()

