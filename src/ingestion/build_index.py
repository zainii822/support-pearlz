import os
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils.logging_setup import setup_logging

logger = setup_logging("build_index")

# Dynamically locate the supportpearlz root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def build_vector_store():
    kb_path = BASE_DIR / "data" / "knowledge_base"
    vector_store_path = BASE_DIR / "data" / "vector_store"

    if not kb_path.exists() or not any(kb_path.iterdir()):
        logger.warning(f"Knowledge base directory is empty or missing at {kb_path}")
        raise FileNotFoundError(f"Knowledge base directory is empty or missing at {kb_path}")

    logger.info("Loading documents from knowledge base...")
    loader = DirectoryLoader(
        str(kb_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(docs)} text chunks.")

    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please authenticate in the UI.")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=api_key
    )

    logger.info("Building FAISS vector index...")
    vector_store = FAISS.from_documents(docs, embeddings)
    
    vector_store_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(vector_store_path))
    logger.info(f"Vector index successfully built and persisted to '{vector_store_path}'.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build FAISS vector store from knowledge base.")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild the vector store.")
    args = parser.parse_args()
    build_vector_store()