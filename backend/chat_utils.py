import streamlit as st
import pandas as pd
import io

def initialize_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def add_chat_entry(question, answer):
    st.session_state.chat_history.append((question, answer))

# Display chat history
def display_chat_history():
    for q, a in st.session_state.chat_history[::-1]:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**RAG:** {a}")
        st.markdown("---")

def clear_chat():
    st.session_state.chat_history = []
    st.session_state["last_answer"] = ""
    st.session_state["last_sources"] = []
    st.session_state["just_submitted"] = False
    st.success("Chat history cleared.")
    st.rerun()

def export_chat():
    if not st.session_state.get("chat_history"):
        st.warning("No chat history to export")
        return
    
    # format the chat history
    format = pd.DataFrame(st.session_state.chat_history, columns=["Question", "Answer"])

    #convert to CSV
    csv_file = io.StringIO()
    format.to_csv(csv_file, index=False)

    # create a download button
    st.download_button(
        label = "⬇️ Download Chat History as CSV",
        data=csv_file.getvalue(),
        file_name="RAG_chat_history.csv",
        mime="text/csv"
    )

