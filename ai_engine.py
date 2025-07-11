# ai_engine.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

def ask_gemini(question: str):
    data = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    response = requests.post(GEMINI_URL, json=data)
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]
