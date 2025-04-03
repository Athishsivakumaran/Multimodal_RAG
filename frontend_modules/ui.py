# modules/ui.py - UI components and styling

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the application"""
    st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Main background and text */
        .stApp {
            background: linear-gradient(to bottom right, #f8f9fa, #f1f3f9);
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e6e9ef;
            padding: 1rem;
        }
        
        /* Custom containers */
        .chat-container {
            border-radius: 10px;
            margin-bottom: 10px;
            padding: 10px 15px;
            position: relative;
            width: 90%;
        }
        
        .user-container {
            background-color: #4361ee;
            color: white;
            margin-left: auto;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 10px;
        }
        
        .bot-container {
            background-color: #ffffff;
            border: 1px solid #e6e9ef;
            margin-right: auto;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Custom header */
        .custom-header {
            background: linear-gradient(90deg, #4361ee, #3f37c9);
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* File uploader */
        .uploadedFile {
            border: 1px solid #e6e9ef;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 8px;
            background-color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* Custom button */
        .custom-button {
            background-color: #4361ee;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .custom-button:hover {
            background-color: #3f37c9;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Input text area */
        .stTextInput>div>div>input {
            border-radius: 8px;
            background-color: white;
            border: 1px solid #e6e9ef;
            color: #1f2937;
            padding: 12px 15px;
            font-size: 16px;
        }
        
        /* Typing animation */
        .typing-animation {
            display: flex;
            align-items: center;
            column-gap: 6px;
            padding: 10px 15px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            background-color: #4361ee;
            border-radius: 50%;
            animation: typing-dot-animation 1.4s infinite ease-in-out;
            display: inline-block;
        }
        
        .typing-dot:nth-child(1) { animation-delay: 0s; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing-dot-animation {
            0%, 100% {
                transform: scale(0.75);
                opacity: 0.5;
            }
            50% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: #4361ee;
        }
        
        /* Cards */
        .info-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        
        /* Divider */
        hr {
            margin: 1.5rem 0;
            border: 0;
            height: 1px;
            background: #e6e9ef;
        }
        
        /* File badges */
        .file-badge {
            background-color: #e0e7ff;
            color: #4361ee;
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 12px;
            margin-right: 5px;
        }
        
        /* Response metadata */
        .metadata {
            font-size: 12px;
            color: #9ca3af;
            margin-top: 5px;
        }
        
        /* Placeholder styling */
        .placeholder {
            color: #9ca3af;
            font-style: italic;
        }

        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            .chat-container {
                width: 100%;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header"""
    st.markdown("""
    <div class="custom-header">
        <h1>📚 Document Intelligence RAG Chat</h1>
        <p>Upload your documents, presentations, and PDFs for an intelligent conversation about their content.</p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_messages():
    """Render all chat messages"""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-container user-container">
                <p>{message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-container bot-container">
                <p>{message["content"]}</p>
                <p class="metadata">RAG AI Assistant</p>
            </div>
            """, unsafe_allow_html=True)
    


def display_empty_state():
    """Display empty state message when no chat history exists"""
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #9ca3af;">
        <i class="fas fa-comments" style="font-size: 48px; margin-bottom: 20px; color: #e0e7ff;"></i>
        <h3>Upload documents to start chatting</h3>
        <p>Process your files from the sidebar to begin the conversation</p>
    </div>
    """, unsafe_allow_html=True)

def render_file_card(file, index):
    """Render a single file card"""
    file_extension = file.name.split('.')[-1].upper()
    return f"""
    <div class="uploadedFile">
        <div>
            <span class="file-badge">{file_extension}</span>
            {file.name}
        </div>
    </div>
    """

def render_supported_formats_info():
    """Render information about supported file formats"""
    return """
    <div class="info-card">
        <h4>📋 Supported Formats</h4>
        <span class="file-badge">PPT</span>
        <span class="file-badge">PPTX</span>
        <span class="file-badge">PDF</span>
        <span class="file-badge">DOC</span>
        <span class="file-badge">DOCX</span>
        <p class="placeholder">Upload your documents to begin analysis</p>
    </div>
    """