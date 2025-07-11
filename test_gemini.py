from ai_engine import ask_gemini

try:
    result = ask_gemini("Say hello from Gemini!")
    print("✅ Gemini API Response:\n", result)
except Exception as e:
    print("❌ Error:", e)
