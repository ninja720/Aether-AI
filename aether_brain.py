import streamlit as st
from google import genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firestore
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def get_ai_response(messages_history):
    try:
        # Create chat session with the new SDK
        chat = client.chats.create(model="gemini-2.0-flash")
        
        # Replay history into the chat
        for msg in messages_history[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            chat.send_message(msg["content"]) # Simplified flow
            
        # Send latest message
        response = chat.send_message(messages_history[-1]["content"])
        return response.text
    except Exception as e:
        return f"Error: System core malfunction: {str(e)}"
