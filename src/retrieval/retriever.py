import streamlit as st
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.utils.logging_setup import setup_logging

logger = setup_logging("retriever")

# Dynamically locate the supportpearlz root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def get_retriever():
    logger.info("Initializing FAISS retriever...")
    
    vector_store_path = BASE_DIR / "data" / "vector_store"
    
    if not vector_store_path.exists():
        logger.error(f"Vector store path {vector_store_path} does not exist.")
        return None

    api_key = st.session_state.get("api_key", "")
    if not api_key:
        logger.error("OpenAI API key missing from session state.")
        return None

    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            openai_api_key=api_key
        )
        
        vector_store = FAISS.load_local(
            folder_path=str(vector_store_path), 
            embeddings=embeddings, 
            allow_dangerous_deserialization=True
        )
        
        retriever = vector_store.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 4}
        )
        
        logger.info("Retriever successfully initialized.")
        return retriever
        
    except Exception as e:
        logger.error(f"Error loading FAISS vector store: {e}")
        return None