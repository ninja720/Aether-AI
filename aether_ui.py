import streamlit as st
import aether_brain
from datetime import datetime

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# --- SIDEBAR (HISTORY) ---
with st.sidebar:
    st.subheader("Chat History")
    if st.button("➕ New Session"):
        st.session_state.messages = []
        st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        st.rerun()

    # Query Firestore for previous sessions
    chats_query = aether_brain.db.collection("chats").order_by("last_updated", direction="DESCENDING").stream()
    for doc in chats_query:
        if st.button(f"⏳ {doc.id}"):
            # Load function
            chat_doc = aether_brain.db.collection("chats").document(doc.id).get()
            if chat_doc.exists:
                st.session_state.messages = chat_doc.to_dict().get("messages", [])
                st.session_state.session_id = doc.id
                st.rerun()

# --- RENDER MESSAGES ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- SINGLE INPUT ---
if prompt := st.chat_input("Input system command..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI Response
    response = aether_brain.get_ai_response(st.session_state.messages)
    
    # Append Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save to Firestore
    aether_brain.db.collection("chats").document(st.session_state.session_id).set({
        "messages": st.session_state.messages,
        "last_updated": aether_brain.firestore.SERVER_TIMESTAMP
    })
    st.rerun()
