# app.py — Streamlit UI for Virtual Chemistry Lab
import streamlit as st
import re
from chemistry import elements
from ai_engine import ask_gemini

st.set_page_config(layout="wide")
st.title("🧪 AI-Powered Virtual Chemistry Lab")

# Initialize session state
if "added" not in st.session_state:
    st.session_state.added = {}

# Sidebar: Periodic Table and Beaker
with st.sidebar:
    st.header("🧬 Periodic Table")
    element_options = [f"{sym} - {data['name']}" for sym, data in elements.items()]
    selected = st.selectbox("Choose element to add:", element_options)
    sym = selected.split(" - ")[0]
    if st.button("Add to Beaker"):
        if sym in st.session_state.added:
            st.session_state.added[sym] += 1
        else:
            st.session_state.added[sym] = 1
        st.rerun()

    st.markdown("---")
    st.subheader("🧫 Beaker Contents")
    if st.session_state.added:
        for sym, count in list(st.session_state.added.items()):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            col1.text(f"{sym} x{count}")
            with col2:
                if st.button("➕", key=f"inc_{sym}"):
                    st.session_state.added[sym] += 1
                    st.rerun()
            with col3:
                if st.button("➖", key=f"dec_{sym}"):
                    if st.session_state.added[sym] > 1:
                        st.session_state.added[sym] -= 1
                    else:
                        del st.session_state.added[sym]
                    st.rerun()
            with col4:
                if st.button("❌", key=f"rem_{sym}"):
                    del st.session_state.added[sym]
                    st.rerun()
    else:
        st.info("No elements added yet.")

# Main Layout
left, center, right = st.columns([1, 3, 1])

# Center Panel: Prediction Output
with center:
    st.subheader("🔮 Prediction Output")
    if st.button("Predict Compound"):
        if st.session_state.added:
            prompt = "Given the following elements and their details:\n"
            for sym, count in st.session_state.added.items():
                prompt += f"- {sym} ({elements[sym]['name']}): {count} atoms\n"

            prompt += (
                "\nPredict the resulting compound (if any) and return only:\n"
                "- Chemical formula\n"
                "- Color\n"
                "- Other name or original name\n"
                "- Reaction\n"
                "- Properties (max 5 points)\n"
                "No tables or markdown formatting. Plain text only."
            )

            try:
                result = ask_gemini(prompt)
                clean_result = re.sub(r'[\*#`|]', '', result)
                clean_result = re.sub(r'\n{2,}', '\n', clean_result).strip()
                st.session_state.prediction = clean_result
            except Exception as e:
                st.session_state.prediction = f"Error: {e}"
        else:
            st.warning("Please add elements to the beaker first.")

    if "prediction" in st.session_state:
        st.text_area("🧪 Result", st.session_state.prediction, height=300)

        # TXT Export
        st.download_button(
            "📄 Export Prediction (TXT)",
            data=st.session_state.prediction.encode('utf-8'),
            file_name="prediction.txt",
            mime="text/plain"
        )

# Right Panel: Clear Button
with right:
    st.subheader("⚙️ Tools")
    if st.button("🧹 Clear Beaker"):
        st.session_state.added = {}
        if "prediction" in st.session_state:
            del st.session_state["prediction"]
        st.rerun()
