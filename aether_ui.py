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

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# --- SIDEBAR (HISTORY) ---
with st.sidebar:
    st.subheader("Chat History")
    if st.button("➕ New Session"):
        save_current_session()
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

    chats_query = aether_brain.db.collection("chats").order_by("last_updated", direction="DESCENDING").stream()
    for doc in chats_query:
        if st.button(f"⏳ {doc.id}"):
            load_session(doc.id)

# --- RENDER MESSAGES ---
# Render history first so it's always visible above the input
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- SINGLE INPUT AREA ---
# This is the only place st.chat_input should appear
if prompt := st.chat_input("Input system command..."):
    # 1. Update UI immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Append to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. Get AI response
    response = aether_brain.get_ai_response(st.session_state.messages)
    
    # 4. Append AI response to state
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 5. Save everything to Firestore
    save_current_session()
    
    # 6. Rerun to refresh the display
    st.rerun()
