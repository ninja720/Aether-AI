import streamlit as st
import aether_brain

# --- CONFIGURATION ---
APP_LOGO = "Gemini_Generated_Image_nhfdqjnhfdqjnhfd-removebg-preview.png"

st.set_page_config(page_title="Aether LX", page_icon=APP_LOGO, layout="wide")

# --- LOGIN GATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Aether LX - Login")
    email = st.text_input("Enter your email to connect:")
    if st.button("Connect"):
        if email:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.messages = []
            st.rerun()
    st.stop() # Stops execution if not logged in

# --- MAIN APP INTERFACE ---
st.sidebar.image(APP_LOGO, width=250)
st.sidebar.caption(f"User: {st.session_state.user_email}")

if st.sidebar.button("➕ New Session"):
    st.session_state.messages = []
    st.rerun()

st.title("System Aether")

# Display private chat history
for msg in st.session_state.messages:
    cls = "user" if msg["role"] == "user" else "ai"
    # Using simple markdown for layout instead of raw HTML for stability
    with st.chat_message(cls):
        st.write(msg["content"])

# Input handling
if prompt := st.chat_input("Input system command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Processing
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response = aether_brain.get_ai_response(st.session_state.messages)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
