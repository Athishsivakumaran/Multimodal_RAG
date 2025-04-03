import os
import json
import uuid
from langchain.schema import Document
from frontend_modules.state_manager import st

def add_elements(retriever, elements, elements_summaries, doc_type, id_key="doc_id"):
    doc_ids = [str(uuid.uuid4()) for _ in elements]

    # Create Documents for original elements with metadata
    original_docs = [
        Document(
            page_content=element,
            metadata={id_key: doc_ids[i], "type": doc_type}
        )
        for i, element in enumerate(elements)
    ]

    # Create Documents for summaries with metadata
    summary_docs = [
        Document(
            page_content=summary,
            metadata={id_key: doc_ids[i], "type": doc_type}
        )
        for i, summary in enumerate(elements_summaries)
    ]

    # Store both in the retriever
    retriever.vectorstore.add_documents(summary_docs)
    retriever.docstore.mset(list(zip(doc_ids, original_docs)))  # Store Documents here


    
def add_documents(extracted_path="/Users/athish/Multimodal_RAG/frontend/extracted_data", 
                  summaries_path="/Users/athish/Multimodal_RAG/frontend/summaries"):
    """
    Loads extracted data and corresponding summaries, then stores them in the retriever.
    """

    retriever = st.session_state.retriever
    pdf_folders = [f for f in os.listdir(extracted_path) if os.path.isdir(os.path.join(extracted_path, f))]

    for pdf_folder in pdf_folders:
        extracted_folder = os.path.join(extracted_path, pdf_folder)
        summary_folder = os.path.join(summaries_path, pdf_folder)

        # Ensure summary folder exists
        if not os.path.exists(summary_folder):
            print(f"Warning: No summary folder found for {pdf_folder}, skipping.")
            continue

        # Load extracted text
        with open(os.path.join(extracted_folder, "text.json"), "r", encoding="utf-8") as f:
            texts = json.load(f)
        with open(os.path.join(summary_folder, "summarized_text.json"), "r", encoding="utf-8") as f:
            texts_summaries = json.load(f)

        # Load tables (stored as HTML)
        with open(os.path.join(extracted_folder, "tables.json"), "r", encoding="utf-8") as f:
            tables = json.load(f)
        with open(os.path.join(summary_folder, "summarized_tables.json"), "r", encoding="utf-8") as f:
            tables_summaries = json.load(f)

        # Load images (stored as base64)
        with open(os.path.join(extracted_folder, "images.json"), "r", encoding="utf-8") as f:
            images = json.load(f)
        with open(os.path.join(summary_folder, "summarized_images.json"), "r", encoding="utf-8") as f:
            images_summaries = json.load(f)

        print(f"Adding documents from {pdf_folder}: {len(texts)} texts, {len(tables)} tables, {len(images)} images.")

        # Store all elements in the retriever with type metadata
        add_elements(retriever, texts, texts_summaries, doc_type="text")
        add_elements(retriever, tables, tables_summaries, doc_type="table")
        add_elements(retriever, images, images_summaries, doc_type="image")

        print(f"Successfully added documents from {pdf_folder}.")
