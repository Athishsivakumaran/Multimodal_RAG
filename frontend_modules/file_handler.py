from frontend_modules.state_manager import st
import os, sys, time, shutil
from frontend_modules.state_manager import add_file, remove_file, add_message, set_processing_complete
from frontend_modules.ui import render_supported_formats_info, render_file_card
from backend_modules.extract_elements import extract_from_files
from backend_modules.summarize_elements.summarize import summarize
from backend_modules.store_documents import add_documents

sys.path.append("/Users/athish/Multimodal_RAG/frontend")
UPLOAD_DIR = "data"

def clean_upload_directory():
    """Delete all existing files in the upload directory before saving new ones."""
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)  # Remove the entire directory
    os.makedirs(UPLOAD_DIR)  # Recreate an empty directory

def save_uploaded_files():
    """Save uploaded files to the 'data/' directory after cleaning existing files."""
    clean_upload_directory()  # Ensure the directory is clean before saving new files
    
    saved_files = []
    for uploaded_file in st.session_state.uploaded_files:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        
        # Write file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        saved_files.append(file_path)

    return saved_files

def display_file_upload_section():
    """Display the file upload section in the sidebar"""
    st.markdown(render_supported_formats_info(), unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drag and drop your files here",
        type=["pdf", "ppt", "pptx", "doc", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    # Ensure files are only added once and displayed properly
    if uploaded_files:
        for uploaded_file in uploaded_files:
            add_file(uploaded_file)

    if st.session_state.uploaded_files:
        st.markdown("<h4>Uploaded Documents</h4>", unsafe_allow_html=True)

        for i, file in enumerate(st.session_state.uploaded_files):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(render_file_card(file, i), unsafe_allow_html=True)
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    remove_file(i)
                    st.rerun()
    
    # Call buttons once to avoid duplication
    display_process_button()
    display_clear_chat_button()

def process_documents():
    """Process the uploaded documents and prepare them for RAG"""
    saved_files = save_uploaded_files()  # Save files after cleaning previous uploads

    with st.spinner("Processing your documents..."):
        progress_bar = st.progress(0)

        for i in range(101):
            progress_bar.progress(i)
            time.sleep(0.02)
            
            if i == 30:
                st.info("Extracting information from documents...")
                extract_from_files()
            elif i == 60:
                st.info("Analyzing images and tables")
                summarize()
            elif i == 90:
                st.info("Readying the RAG")
                add_documents()
        
        set_processing_complete(True)

        add_message(
            "assistant", 
            f"I've processed {len(saved_files)} document(s). You can now ask me questions about their content."
        )

        progress_bar.progress(100)
        st.success("Documents processed successfully!")
        st.rerun()

def display_process_button():
    """Display the process documents button"""
    if st.session_state.uploaded_files and not st.session_state.processing_complete:
        if st.button("Process Documents", key="process_docs"):
            process_documents()

def display_clear_chat_button():
    """Display button to clear chat history"""
    if st.session_state.chat_history:
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
