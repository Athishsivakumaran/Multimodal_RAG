# app.py - Main application entry point

from frontend_modules.ui import apply_custom_css, render_header, display_empty_state, render_chat_messages
from frontend_modules.file_handler import display_file_upload_section
from frontend_modules.chat_handler import display_chat_input
from frontend_modules.state_manager import initialize_session_state,st



st.set_page_config(
    page_title="Document Intelligence RAG Chat",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Apply custom styling
apply_custom_css()

# Render header
render_header()

# Create two-column layout
main_column, _ = st.columns([6, 1])

# Sidebar - File Upload Section
with st.sidebar:
    st.markdown("<h2>📄 Document Upload</h2>", unsafe_allow_html=True)
    
    # Display file upload interface
    display_file_upload_section()
    
    # About section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <h4>ℹ️ About</h4>
        <p>This RAG (Retrieval Augmented Generation) system helps you extract insights from your documents using advanced AI.</p>
        <p class="metadata">Built with Streamlit & AI</p>
    </div>
    """, unsafe_allow_html=True)

# Main chat interface
with main_column:
    # Display chat messages
    

    render_chat_messages()
    
    # Display empty state if no messages
    if not st.session_state.chat_history and not st.session_state.processing_complete:
        display_empty_state()
    
    # Display chat input if documents have been processed
    if st.session_state.processing_complete:
        display_chat_input()
