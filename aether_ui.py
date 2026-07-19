import streamlit as st
import aether_brain
from datetime import datetime

# --- FIRESTORE FUNCTIONS ---
def save_current_session():
    if st.session_state.messages:
        aether_brain.db.collection("chats").document(st.session_state.session_id).set({
            "messages": st.session_state.messages,
            "last_updated": aether_brain.firestore.SERVER_TIMESTAMP
        })

def load_session(session_id):
    doc = aether_brain.db.collection("chats").document(session_id).get()
    if doc.exists:
        st.session_state.messages = doc.to_dict().get("messages", [])
        st.session_state.session_id = session_id
        st.rerun()

# --- SIDEBAR (HISTORY) ---
with st.sidebar:
    # Query Firestore
    chats_query = aether_brain.db.collection("chats").order_by("last_updated", direction="DESCENDING").stream()
    
    if st.button("➕ New Session"):
        save_current_session()
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

    for doc in chats_query:
        if st.button(f"⏳ {doc.id}"):
            load_session(doc.id)

# --- MAIN INTERFACE ---
# (Keep your existing display logic and st.chat_input here)
if prompt := st.chat_input("Input system command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_current_session()
    st.rerun()
