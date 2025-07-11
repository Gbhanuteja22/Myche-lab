# 🔬 AI-Powered Virtual Chemistry Lab

An interactive desktop application that simulates a virtual chemistry lab. Users can drag a beaker into the workspace, add elements from the periodic table, and predict the resulting compound with the help of Google's Gemini AI. The lab provides educational insights such as chemical formulas, names, properties, and reactions of combined elements — all without the risk of real-world experiments.

---

## 🧠 Powered by Gemini AI

The app integrates **Google Gemini AI API** to:
- Predict compound results from selected elements.
- Return human-readable details like chemical name, color, formula, properties, and reactions.

---

## 📦 Features

- 🎨 **Graphical Interface** using `tkinter`
- 🧪 Drag-and-drop **Beaker** into the canvas
- 🌈 Select and add elements with optional weights
- 🤖 AI-powered **compound prediction**
- 📄 Displays: 
  - Color  
  - Formula  
  - Alternative/Original Name  
  - Reaction Info  
  - Top 5 Properties  
- 🖼️ Displays compound image (if available)
- 💾 Export results
- 🔄 Reset/Clear tools for repeated usage

---

## 🛠️ Tech Stack

- **Python 3.11+**
- `tkinter`, `Pillow`, `requests` – for UI and HTTP
- `mediapipe`, `opencv-python` – future gesture control features
- `google-generativeai` – Gemini API integration
- `.env` for storing your API key securely

---

## 📥 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/virtual-chem-lab.git
   cd virtual-chem-lab
