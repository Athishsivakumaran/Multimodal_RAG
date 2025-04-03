
import streamlit as st
from backend_modules.config  import create_vector_store
from backend_modules.response_chain import generate_response


def initialize_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        print("Debug: Initialized chat_history")

    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
        print("Debug: Initialized uploaded_files")

    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
        print("Debug: Initialized processing_complete")

    if 'retriever' not in st.session_state:
        st.session_state.retriever = create_vector_store()  # Ensure this function is defined
        print("Debug: Initialized retriever")
    else:
        print("Debug: Retriever already exists in session state")

    if "chain" not in st.session_state:
        # Pass retriever to generate_response
        st.session_state.chain = generate_response(st.session_state.retriever)



def add_message(role, content):
    """Add a message to the chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })

def get_last_user_message():
    """Get the most recent user message"""
    for message in reversed(st.session_state.chat_history):
        if message["role"] == "user":
            return message["content"]
    return None

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []

def add_file(file):
    """Add a file to the uploaded files list"""
    # Check if file already exists
    for existing_file in st.session_state.uploaded_files:
        if existing_file.name == file.name:
            return False
    
    # Add file if it doesn't exist
    st.session_state.uploaded_files.append(file)
    return True

def remove_file(index):
    """Remove a file from the uploaded files list"""
    if 0 <= index < len(st.session_state.uploaded_files):
        st.session_state.uploaded_files.pop(index)
        return True
    return False

def set_processing_complete(status=True):
    """Set the processing complete status"""
    st.session_state.processing_complete = status

