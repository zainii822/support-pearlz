# SupportPearlz RAG Assistant

An advanced, production-grade Retrieval-Augmented Generation (RAG) customer support assistant built for Pearlz Home Systems using LangChain, OpenAI (`gpt-4o-mini`), FAISS, and Streamlit.

---

## Project Structure
- `data/knowledge_base/`: Contains markdown documents detailing warranties, manuals, and policies.
- `data/vector_store/`: Local persistent FAISS vector index storage.
- `src/config.py`: Centralized configuration management using Pydantic Settings.
- `src/ingestion/`: Document loaders and index building scripts.
- `src/retrieval/`: Configurable FAISS vector retriever.
- `src/chains/`: LCEL RAG generation chains and prompt templates.
- `app.py`: Streamlit web chat frontend interface.

---

## Setup & Installation Instructions

### 1. Clone or Open Project Directory
Open your terminal in the root project folder (`supportpearlz/supportpearlz/`).

### 2. Create and Activate Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate