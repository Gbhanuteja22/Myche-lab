# # ai_engine.py — Handles interaction with Gemini API
# import os
# import google.generativeai as genai

# # Load API key from environment variable
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     raise EnvironmentError("GOOGLE_API_KEY not set in environment.")

# genai.configure(api_key=GOOGLE_API_KEY)

# # Use valid available model (as per your list_models output)
# MODEL_NAME = "models/gemini-2.5-pro"

# model = genai.GenerativeModel(model_name=MODEL_NAME)

# def ask_gemini(question: str) -> str:
#     try:
#         response = model.generate_content(question)
#         return response.text.strip() if hasattr(response, "text") else str(response)
#     except Exception as e:
#         return f"Error communicating with Gemini API: {e}"











# ai_engine.py
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-2.5-pro"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"

headers = {
    "Content-Type": "application/json"
}

def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        raise EnvironmentError("GEMINI_API_KEY not set in environment.")

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        raise Exception(f"Gemini API Error {response.status_code}: {response.text}")

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
