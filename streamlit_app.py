import streamlit as st

st.set_page_config(
    page_title="Robust ReAct Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Robust ReAct with Observation Quality Control")
st.markdown("---")

st.markdown("""
### Welcome

This application demonstrates:

- ReAct reasoning
- Observation Quality Control
- Adaptive Recovery
- FEVER-style Fact Verification
- Microsoft Phi-3-mini-4k-instruct

Use the navigation menu on the left to explore:

1. Overview
2. Live Demo
3. Results
4. Failure Analysis
""")

st.info(
    "Navigate using the Streamlit sidebar to access each section."
)