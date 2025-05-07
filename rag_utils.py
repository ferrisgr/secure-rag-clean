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

def load_and_index_docs(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = PyMuPDFLoader(os.path.join(folder_path, filename))
            docs.extend(loader.load())

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def ask_question(vectorstore, query, role):
    openai_key = os.getenv("OPENAI_API_KEY")
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
        tone = "Respond as a professiona assistant."


   
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
        template = f"""Given the context below, answer the question at the end. {tone}
                 If you don't know the answer, say "I don't know". Be concise and avoid assumptions
                 
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
