import os
import json,shutil
from unstructured.partition.pdf import partition_pdf

def extract_chunks(file_path):
    chunks = partition_pdf(
        filename=file_path,
        infer_table_structure=True,            
        strategy="hi_res",                     
        extract_image_block_types=["Image"],   
        extract_image_block_to_payload=True,   
        chunking_strategy="by_title",          
        max_characters=10000,                  
        combine_text_under_n_chars=2000,       
        new_after_n_chars=6000,                
    )

    images, tables, texts = [], [], []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk.text)  # Extract raw text
            chunk_els = chunk.metadata.orig_elements
            for el in chunk_els:
                if "Image" in str(type(el)) and el.metadata.image_base64:
                    images.append(el.metadata.image_base64)
                if 'Table' in str(type(el)):
                    tables.append(el.metadata.text_as_html)  # ✅ Store as HTML
            
    return images, tables, texts

def save_extracted_data(pdf_name, images, tables, texts,extracted_data_path="/Users/athish/Multimodal_RAG/frontend/extracted_data"):
    if os.path.exists(extracted_data_path):
        shutil.rmtree(extracted_data_path)  # Deletes the folder and its contents
    os.makedirs(extracted_data_path)  # Recreate the empty folder
    extracted_path = os.path.join(extracted_data_path ,pdf_name)
    os.makedirs(extracted_path, exist_ok=True)

    # Save extracted text
    with open(os.path.join(extracted_path, "text.json"), "w") as f:
        json.dump(texts, f, indent=4)

    # Save extracted tables as HTML
    with open(os.path.join(extracted_path, "tables.json"), "w") as f:
        json.dump(tables, f, indent=4)

    # Save extracted images as a list of base64 strings in a JSON file
    with open(os.path.join(extracted_path, "images.json"), "w", encoding="utf-8") as f:
        json.dump(images, f, indent=4, ensure_ascii=False)


def extract_from_files(folder_path="/Users/athish/Multimodal_RAG/frontend/backend_modules/data"):
    """Checks for PDFs in a folder, extracts data, and saves it in structured format."""
    
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    for pdf in pdf_files:
        file_path = os.path.join(folder_path, pdf)
        print(f"Processing: {file_path}")
        images, tables, texts = extract_chunks(file_path)
        save_extracted_data(pdf, images, tables, texts)

# Run the function


