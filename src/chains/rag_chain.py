import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.retrieval.retriever import get_retriever
from src.utils.logging_setup import setup_logging

logger = setup_logging("rag_chain")

def get_rag_chain():
    """Initializes and returns the LCEL RAG chain using session API key."""
    logger.info("Initializing RAG chain...")
    
    # Grab API key securely from Streamlit session state
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        raise ValueError("OpenAI API key is missing in session state. Please authenticate first.")

    retriever = get_retriever()
    if not retriever:
        logger.error("Retriever could not be initialized.")
        return None

    # Use gpt-4o-mini with the user-provided API key
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=api_key
    )

    template = """You are SupportPearlz, an official, professional, and helpful customer support assistant for Pearlz Home Systems. 
    Answer the user's question accurately using ONLY the provided context below. 
    If the answer cannot be found within the context, politely state that you can only answer questions related to Pearlz Home Systems policies, warranties, and product manuals. Do not make up information.

    Context:
    {context}

    User Question: {question}

    Helpful Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logger.info("RAG chain successfully initialized.")
    return rag_chain