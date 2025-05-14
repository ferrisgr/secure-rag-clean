import streamlit as st
import os
from db_rag import init_db, log_query, get_logs
from backend.rag_utils import load_and_index_docs, ask_question
from backend.file_utils import ensure_doc_folder, handle_file_upload
from backend.chat_utils import initialize_chat, add_chat_entry, display_chat_history, clear_chat, export_chat


# Sidebar for role and PDF
st.set_page_config(page_title="RAG PDF Query", page_icon=":book:", layout="wide")

from PIL import Image

logo_path = "assets/logo.png"
logo = Image.open(logo_path)
st.image(logo, width=200) 



if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("🔒 This app is password protected.")
    password = st.text_input("Enter password:", type="password")
    login_button = st.button("Login")

    if login_button:
        if password == "1234":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Try again.")
    st.stop()


#Initialize the database
init_db()

#safe-load pdf documents
doc_folder = "documents"
available_pdfs = [
    f for f in os.listdir(doc_folder)
    if f.lower().endswith(".pdf") and not f.startswith(".")
]

# Auto-delete macOS junk
ds_store_path = os.path.join(doc_folder, ".DS_Store")
if os.path.exists(ds_store_path):
    os.remove(ds_store_path)


ensure_doc_folder(doc_folder)
handle_file_upload(doc_folder)


st.sidebar.title("User Role & PDF")
role = st.sidebar.selectbox("Select your role", ["Analyst", "Reviewer", "Admin"])
pdf_name = st.sidebar.selectbox("Select PDF", available_pdfs) if available_pdfs else None
load_triggered = st.sidebar.button("📥 Load Selected PDF")



#Only load vectors if a PDF is selected
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if pdf_name and load_triggered:
    pdf_path = os.path.join(doc_folder, pdf_name)
    with st.spinner("🔄 Indexing selected PDF..."):
        st.session_state.vectorstore = load_and_index_docs(pdf_path)
        st.success(f"✅ '{pdf_name}' indexed successfully.")

VECTORSTORE = st.session_state.vectorstore



# Initialize chat
initialize_chat()

if st.sidebar.button("🧹 Clear Chat"):
    clear_chat()

show_chat = st.sidebar.checkbox("🗨️Show Chat History")
show_sources = st.sidebar.checkbox("📚 Show Sources", value=True)

if not VECTORSTORE:
    st.info("📄 Please select and load a PDF before asking a question.")

#main input
question = st.text_area(
    "Ask your question:",
    value="",
    height=100
)

# Run RAG on click
if st.button("Submit") and question and VECTORSTORE:
    answer = ask_question(VECTORSTORE, question, role)

    # Log the query
    retriever = VECTORSTORE.as_retriever()
    docs = retriever.get_relevant_documents(question)
    sources = [doc.page_content[:500] for doc in docs]


    add_chat_entry(question, answer)
    st.session_state["just_submitted"] = True
    st.session_state["last_sources"] = sources
    st.session_state["last_answer"] = answer
    st.rerun()

#Display last answer if just submitted
if st.session_state.get("just_submitted") is not None:
    st.session_state["just_submitted"] = False
    answer = st.session_state.get("last_answer", "")
    sources = st.session_state.get("last_sources", [])

    # Display answer
    st.subheader(f"Answer (Role: {role})")
    st.markdown(answer)

    if show_sources:
        st.subheader("Sources:")
        for src in sources:
            st.code(src[:500])

    
    log_query(role, question, answer, sources)


# Display chat history
if show_chat:
    display_chat_history()


export_chat()