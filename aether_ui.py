import streamlit as st
import aether_brain
from datetime import datetime

# --- FIRESTORE FUNCTIONS ---
def save_current_session():
    """Saves session messages to Firestore."""
    if st.session_state.messages:
        aether_brain.db.collection("chats").document(st.session_state.session_id).set({
            "messages": st.session_state.messages,
            "last_updated": aether_brain.firestore.SERVER_TIMESTAMP
        })

def load_session(session_id):
    """Loads session from Firestore."""
    doc = aether_brain.db.collection("chats").document(session_id).get()
    if doc.exists:
        st.session_state.messages = doc.to_dict().get("messages", [])
        st.session_state.session_id = session_id
        st.rerun()

def delete_session(session_id):
    """Deletes session from Firestore."""
    aether_brain.db.collection("chats").document(session_id).delete()
    if st.session_state.session_id == session_id:
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.rerun()

# --- SIDEBAR HISTORY ---
with st.sidebar:
    # Query database for history instead of local files
    chats_query = aether_brain.db.collection("chats").order_by("last_updated", direction="DESCENDING").stream()
    sessions = [doc.id for doc in chats_query]

    if st.button("➕ New Session"):
        save_current_session()
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

    for sess in sessions:
        col1, col2 = st.columns([4, 1])
        if col1.button(f"⏳ {sess}", key=f"load_{sess}"):
            load_session(sess)
        if col2.button("❌", key=f"del_{sess}"):
            delete_session(sess)

# --- MAIN LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# [Keep your existing chat display code here]

if prompt := st.chat_input("Input system command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_current_session() # Save to cloud
    st.rerun()
