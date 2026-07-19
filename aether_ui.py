import streamlit as st
import aether_brain
import os
import json
from datetime import datetime

# --- CONFIGURATION ---
APP_LOGO = "Gemini_Generated_Image_nhfdqjnhfdqjnhfd-removebg-preview.png"
CHATS_DIR = "chats"

if not os.path.exists(CHATS_DIR): 
    os.makedirs(CHATS_DIR)

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

# --- FUNCTIONS ---
def save_current_session():
    if st.session_state.messages:
        with open(os.path.join(CHATS_DIR, f"{st.session_state.session_id}.json"), "w") as f:
            json.dump(st.session_state.messages, f)

def load_session(session_file):
    with open(os.path.join(CHATS_DIR, session_file), "r") as f:
        st.session_state.messages = json.load(f)
    st.session_state.session_id = session_file.replace(".json", "")
    st.rerun()

def delete_session(session_file):
    file_path = os.path.join(CHATS_DIR, session_file)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if st.session_state.session_id == session_file.replace(".json", ""):
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.rerun()

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# --- SIDEBAR (HISTORY) ---
with st.sidebar:
    st.image(APP_LOGO, width=250)
    st.caption("Advanced Logic Core by LX.Studio")
    
    if st.button("➕ New Session", use_container_width=True):
        save_current_session()
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()
        
    st.divider()
    st.subheader("Chat History")
    
    sessions = sorted([f for f in os.listdir(CHATS_DIR) if f.endswith('.json')], reverse=True)
    
    if sessions:
        if st.button("🗑️ Clear All History", use_container_width=True):
            for sess in sessions:
                os.remove(os.path.join(CHATS_DIR, sess))
            st.session_state.messages = []
            st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.rerun()
            
        st.write("") 
        
        for sess in sessions:
            col1, col2 = st.columns([4, 1]) 
            
            with col1:
                display_name = sess.replace('chat_', '').replace('.json', '')
                if st.button(f"⏳ {display_name}", key=f"load_{sess}", use_container_width=True):
                    load_session(sess)
            
            with col2:
                if st.button("❌", key=f"del_{sess}"):
                    delete_session(sess)
    else:
        st.caption("No history yet.")

# --- MAIN INTERFACE ---
st.title("System Aether")

for msg in st.session_state.messages:
    cls = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="{cls}-container"><div class="{cls}-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# --- INPUT AND LIVE RE-RUN ---
if prompt := st.chat_input("Input system command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_current_session()
    st.rerun()

# --- PROCESSING ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    status_msg = st.markdown('<div class="loading-pulse">Aether Core Processing...</div>', unsafe_allow_html=True)
    
    # Passing the full chat history to aether_brain
    response = aether_brain.get_ai_response(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_current_session()
    status_msg.empty()
    st.rerun()
