import streamlit as st
import aether_brain

# --- CONFIGURATION ---
APP_LOGO = "Gemini_Generated_Image_nhfdqjnhfdqjnhfd-removebg-preview.png"

st.set_page_config(page_title="Aether LX", page_icon=APP_LOGO, layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #050505; color: #e0e0e0; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }
        .user-container { display: flex; justify-content: flex-end; margin: 5px 0; }
        .ai-container { display: flex; justify-content: flex-start; margin: 5px 0; }
        .user-bubble { background-color: #007bff; color: white; padding: 10px 15px; border-radius: 18px; display: inline-block; max-width: 80%; }
        .ai-bubble { background-color: #333333; color: white; padding: 10px 15px; border-radius: 18px; display: inline-block; max-width: 80%; }
        .loading-pulse { animation: pulse 1.5s infinite; color: #00bcd4; font-weight: bold; margin: 10px 0; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.image(APP_LOGO, width=250)
    st.caption("Advanced Logic Core by LX.Studio")
    
    if st.button("➕ New Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("System Aether")

for msg in st.session_state.messages:
    cls = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="{cls}-container"><div class="{cls}-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# --- INPUT ---
if prompt := st.chat_input("Input system command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- PROCESSING ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    status_msg = st.markdown('<div class="loading-pulse">Aether Core Processing...</div>', unsafe_allow_html=True)
    
    response = aether_brain.get_ai_response(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    status_msg.empty()
    st.rerun()
