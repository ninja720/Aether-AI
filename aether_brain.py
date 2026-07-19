import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firestore
if not firebase_admin._apps:
    key_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Gemini Config
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def get_ai_response(messages_history):
    formatted_messages = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in messages_history]
    return model.generate_content(formatted_messages).text
