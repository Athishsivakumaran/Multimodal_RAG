import chromadb
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever

def create_vector_store():
    PERSIST_DIRECTORY = "./chroma_db"
    
    # Initialize embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    try:
        # Create the client
        chroma_client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
        
        # Check if collection exists and delete it
        try:
            collection = chroma_client.get_collection("multi_modal_rag")
            if collection:
                # Delete the collection if it exists
                chroma_client.delete_collection("multi_modal_rag")
                print("Deleted existing collection")
        except Exception as e:
            # Collection doesn't exist or other error
            print(f"Collection doesn't exist or error: {e}")
        
        # Create a fresh collection
        collection = chroma_client.create_collection("multi_modal_rag")
        print("Created new collection")
        
    except Exception as e:
        print(f"Error with ChromaDB setup: {e}")
        raise
    
    # Initialize Chroma vector store
    vectorstore = Chroma(
        client=chroma_client, 
        collection_name="multi_modal_rag", 
        embedding_function=embeddings
    )
    
    # Initialize an in-memory store
    store = InMemoryStore()
    id_key = "doc_id"
    
    # Create a retriever
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )
    return retriever