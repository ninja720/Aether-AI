import streamlit as st
import aether_brain
from datetime import datetime

# --- FUNCTIONS ---
def save_current_session():
    if st.session_state.messages:
        aether_brain.db.collection("chats").document(st.session_state.session_id).set({
            "messages": st.session_state.messages,
            "last_updated": aether_brain.firestore.SERVER_TIMESTAMP
        })

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# --- RENDER MESSAGES ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- SINGLE DEFINITIVE INPUT ---
# This specific line must only appear ONCE in the entire file
prompt = st.chat_input("Input system command...")

if prompt:
    # 1. Update UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. AI Logic
    response = aether_brain.get_ai_response(st.session_state.messages)
    
    # 4. Save
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_current_session()
    
    # 5. Rerun
    st.rerun()
