import streamlit as st
import os
from db_rag import init_db, log_query, get_logs
from rag_utils import load_and_index_docs, ask_question

#Initialize the database
init_db()
VECTORSTORE = load_and_index_docs("documents")

# Sidebar for role and PDF
st.set_page_config(page_title="RAG PDF Query", page_icon=":book:", layout="wide")
st.sidebar.title("User Role & PDF")
role = st.sidebar.selectbox("Select your role", ["Analyst", "Reviewer", "Admin"])
pdf_name = st.sidebar.selectbox("Select PDF", os.listdir("documents"))

#main input
st.title("RAG PDF Query")
question = st.text_input("Ask your question about the selected PDF: ")

# Run RAG on click
if st.button("Submit") and question:
    answer = ask_question(VECTORSTORE, question, role)

    # Display answer
    st.subheader(f"Answer (Role: {role})")
    try:
        st.markdown(answer)
    except:
        st.write(answer)

    # Log the query
    retriever = VECTORSTORE.as_retriever()
    docs = retriever.get_relevant_documents(question)
    sources = [doc.page_content[:500] for doc in docs]
    st.subheader("Sources:")
    for src in sources:
        st.code(src[:500])
    
    log_query(role, question, answer, sources)

