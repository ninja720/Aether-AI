import streamlit as st
import google.generativeai as genai

# API Key configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Personality configuration
system_instruction = (
    "You are Aether, a chill and highly intelligent coding companion created by LX.Studio. "
    "Talk naturally like a real developer—friendly, casual, and energetic. "
    "NEVER use robotic phrases. Just hang out, match the user's vibe, and dive deep "
    "into scripts, logic, game engines, UI configurations, or server optimization."
)

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite", 
    system_instruction=system_instruction
)

def get_ai_response(messages_history):
    try:
        formatted_messages = []
        for msg in messages_history:
            role = "model" if msg["role"] == "assistant" else "user"
            formatted_messages.append({
                "role": role,
                "parts": [msg["content"]]
            })
        response = model.generate_content(formatted_messages)
        return response.text
    except Exception as e:
        return f"Error: System core malfunction: {str(e)}"
