# test_gemini_final.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "contents": [
        {
            "parts": [
                {"text": "What is the formula and state of water at room temperature?"}
            ]
        }
    ]
}

response = requests.post(f"{url}?key={API_KEY}", headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Full Response:")
print(response.text)
