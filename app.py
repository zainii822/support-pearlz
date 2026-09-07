import streamlit as st
from openai import OpenAI
from src.chains.rag_chain import get_rag_chain
from pathlib import Path
from src.ingestion.build_index import build_vector_store

# Dynamically locate the base directory for app.py to prevent path errors on cloud
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="SupportPearlz AI | Enterprise Assistant",
    page_icon="🛡️",
    layout="wide"
)

# --- Advanced Professional CSS Styling ---
st.markdown("""
    <style>
    .main-header { font-size: 2.8rem; color: #0F172A; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0px; }
    .sub-header { font-size: 1.15rem; color: #475569; margin-bottom: 25px; }
    .stButton>button { background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; border-radius: 10px; font-weight: 600; border: none; padding: 0.6rem 1.2rem; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2); transition: all 0.3s ease; }
    .stButton>button:hover { background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%); box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3); transform: translateY(-1px); }
    .auth-card { background: #FFFFFF; padding: 35px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05); border: 1px solid #E2E8F0; }
    .metric-container { background: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "api_key" not in st.session_state: st.session_state.api_key = ""
if "prefilled_prompt" not in st.session_state: st.session_state.prefilled_prompt = None

# --- SCREEN 1: Secure Enterprise Login Gate ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br><div style='text-align: center;'><span style='font-size: 3.5rem;'>🛡️</span></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 2.2rem;'>SupportPearlz Secure Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Enter your OpenAI API credentials to unlock the enterprise customer intelligence engine.</p><br>", unsafe_allow_html=True)
        
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        user_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...", help="Your key is validated securely and kept only for your session.")
        
        if st.button("Unlock Dashboard", use_container_width=True):
            if not user_api_key.strip():
                st.error("⚠️ Please provide a valid API key.")
            else:
                with st.spinner("🔐 Authenticating with OpenAI API..."):
                    try:
                        client = OpenAI(api_key=user_api_key.strip())
                        client.models.list()
                        st.session_state.authenticated = True
                        st.session_state.api_key = user_api_key.strip()
                        st.success("✅ Authentication successful! Loading dashboard...")
                        st.rerun()
                    except Exception:
                        st.error("❌ Invalid API Key. Please verify your credentials and try again.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- SCREEN 2: Pro Dashboard & Chat Interface ---
with st.sidebar:
    st.markdown("### 🎛️ Control Center\n---\n**System Status:** <span style='color: #10B981; font-weight: 600;'>● Operational</span>\n**LLM Engine:** `gpt-4o-mini`\n**Vector Index:** `FAISS (Local)`\n**Knowledge Scope:** `10 Documents`\n---", unsafe_allow_html=True)
    
    st.markdown("#### 🚀 Quick Topics")
    if st.button("AquaPearl 500 Warranty", use_container_width=True): st.session_state.prefilled_prompt = "What does the warranty cover for the AquaPearl 500 Pro?"
    if st.button("Shipping & Delivery Info", use_container_width=True): st.session_state.prefilled_prompt = "What are the standard shipping timelines and policies?"
    if st.button("Return & Refund Rules", use_container_width=True): st.session_state.prefilled_prompt = "What is the return and refund policy for hardware products?"
    if st.button("AirPearl Pro Specs", use_container_width=True): st.session_state.prefilled_prompt = "What are the core specifications of the AirPearl Pro Air Purifier?"

    st.markdown("---")
    if st.button("🔒 End Session (Lock)", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown("<h1 class='main-header'>🛡️ SupportPearlz Assistant</h1><p class='sub-header'>Instant, accurate, and grounded answers sourced directly from Pearlz Home Systems knowledge repositories.</p>", unsafe_allow_html=True)
with col_badge:
    st.markdown("<br><div class='metric-container'><b>Mode:</b> Production RAG<br><span style='color: #2563EB; font-size: 0.85rem;'>Strictly Grounded</span></div>", unsafe_allow_html=True)
st.markdown("---")

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

# Initialize RAG chain dynamically using the robust BASE_DIR path
def load_chain():
    vector_store_path = BASE_DIR / "data" / "vector_store"
    if not vector_store_path.exists() or not any(vector_store_path.iterdir()):
        try:
            with st.spinner("Building vector index for the first time..."):
                build_vector_store()
        except Exception as e:
            st.sidebar.error(f"Vector Build Error: {e}")
    return get_rag_chain()

rag_chain = load_chain()

prompt = st.chat_input("Ask about warranties, manuals, shipping, or troubleshooting...")
if st.session_state.prefilled_prompt:
    prompt = st.session_state.prefilled_prompt
    st.session_state.prefilled_prompt = None  

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        if not rag_chain:
            response = "Error: RAG chain initialization failed. Check your data/knowledge_base folder."
            st.markdown(response)
        else:
            with st.spinner("🔍 Querying vector store & synthesizing response..."):
                try:
                    response = rag_chain.invoke(prompt)
                except Exception as e:
                    response = f"An error occurred during retrieval: {e}"
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})