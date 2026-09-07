import os
import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader
)
from src.config import settings

logger = logging.getLogger(__name__)

def load_single_document(file_path: str) -> List[Document]:
    """Dispatches a file to the correct loader based on its extension with error handling."""
    ext = os.path.splitext(file_path)[1].lower()
    docs = []
    
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif ext in [".md", ".txt"]:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
        elif ext == ".csv":
            loader = CSVLoader(file_path)
            docs = loader.load()
        else:
            logger.warning(f"Unsupported file extension found: {ext} for file {file_path}")
            return []
            
        file_name = os.path.basename(file_path)
        for doc in docs:
            doc.metadata["source"] = file_name
            doc.metadata["doc_type"] = _infer_doc_type(file_name)
            
        logger.info(f"Successfully loaded: {file_name} ({len(docs)} pages/elements)")
        return docs

    except Exception as e:
        logger.error(f"Error loading file {file_path}: {e}")
        return []

def _infer_doc_type(file_name: str) -> str:
    """Helper to categorize document type based on filename for metadata contract."""
    name_lower = file_name.lower()
    if "manual" in name_lower:
        return "manual"
    elif "policy" in name_lower or "agreement" in name_lower:
        return "policy"
    elif "faq" in name_lower:
        return "faq"
    elif "pricing" in name_lower or "guide" in name_lower:
        return "guide"
    else:
        return "general"

def load_knowledge_base(kb_dir: str) -> List[Document]:
    """Recursively walks the knowledge base directory and loads all supported files."""
    all_documents = []
    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir, exist_ok=True)
        logger.warning(f"Knowledge base directory '{kb_dir}' was missing and has been created.")
        return all_documents

    for root, _, files in os.walk(kb_dir):
        for file in files:
            file_path = os.path.join(root, file)
            docs = load_single_document(file_path)
            all_documents.extend(docs)
            
    logger.info(f"Ingestion complete. Total documents loaded: {len(all_documents)}")
    return all_documents