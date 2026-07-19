import streamlit as st
import json
from google import genai
import firebase_admin
from firebase_admin import credentials, firestore

# --- INITIALIZATION ---
# Initialize Firestore
if not firebase_admin._apps:
    # Ensure your secret is named FIREBASE_SERVICE_ACCOUNT and is a stringified JSON
    key_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- GEMINI FALLBACK LOGIC ---
def get_ai_response(messages_history):
    # Load the list of keys from Streamlit secrets
    keys = json.loads(st.secrets["GEMINI_KEYS"])
    
    for api_key in keys:
        try:
            # Initialize client with current key
            client = genai.Client(api_key=api_key)
            
            # Create chat session
            chat = client.chats.create(model="gemini-2.0-flash")
            
            # Replay history (excluding the very last message)
            for msg in messages_history[:-1]:
                chat.send_message(msg["content"])
                
            # Send latest message
            response = chat.send_message(messages_history[-1]["content"])
            return response.text
            
        except Exception as e:
            # If a 429 (Resource Exhausted) occurs, the loop continues to the next key
            if "429" in str(e):
                continue
            else:
                return f"Error: {str(e)}"
                
    return "Error: All API keys have exceeded their daily quota."
