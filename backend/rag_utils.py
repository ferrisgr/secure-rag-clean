from dotenv import load_dotenv
load_dotenv()
import os

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA 
from langchain.prompts import PromptTemplate
import streamlit as st

openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

@st.cache_resource(show_spinner=True)
def load_and_index_docs(file_path):
    if not file_path.endswith(".pdf"):
        raise ValueError("The provided file path does not point to a PDF file.")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()

    if not docs:
        raise ValueError("No PDF documents found in the specified folder.")

    splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

def ask_question(vectorstore, query, role):
    llm = OpenAI(openai_api_key=openai_key)

    if role == "Analyst":
        tone = "You are an experienced investment banking analyst. " \
        "Given the context below, answer the question at the end. " \
        "If you don't know the answer, say 'I don't know'. " \
        "If the data allows it, respond using a markdown table. " \
        "If a table is not appropriate, respond in bullet points. " \
        "You must answer in a concise, professional tone — as if you're sending a summary slide to Goldman Sachs MD."
    
    elif role == "Reviewer":
        tone = "You are an experienced financial reviewer. Answer the question below based on the context provided."
    
    elif role == "Admin":
        tone = "You are an experienced financial admin. Answer the question below based on the context provided. " \
        "You have worked in top tier financial institutions. "
    
    else:
        tone = "Respond as a professional assistant."


   
    question_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template = f"""Given the context below, answer the question at the end. {tone}
                 If you don't know the answer, say "I don't know". Be concise and avoid assumptions
                 
                 Context: 
                 {{context}}
                 
                 Question:
                 {{question}}
                 
                 Answer:""" 
        )

    combine_prompt = PromptTemplate(
        input_variables=["summaries", "question"],
        template = f"""
        {tone}
        Summaries:
        {{summaries}}
        Question:
        {{question}}
        
        Final Answer:"""
        )
    
    # Define the chain type and its arguments
    chain_type_kwargs = {
         "question_prompt": question_prompt,
         "combine_prompt": combine_prompt
    }

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="map_reduce",
        chain_type_kwargs=chain_type_kwargs
    )

    result = qa.run(query)
    return result
