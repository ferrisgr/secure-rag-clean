from rag_utils import load_and_index_docs, ask_question

VECTORSTORE = load_and_index_docs("documents")

def query_rag(question, pdf_name):
    """
    Handles full RAG pipeline: retrieve + generate + return answer + chunks.
    Currently ignores `pdf_name` because vectorstore is built from all PDFs.
    """

    # Run LangChain chain
    answer = ask_question(VECTORSTORE, question)

    # Get the top K retrieved chunks (extract manually if needed)
    retriever = VECTORSTORE.as_retriever()
    docs = retriever.get_relevant_documents(question)
    sources = [doc.page_content[:500] for doc in docs]

    return {
        "answer": answer,
        "sources": sources,
    }