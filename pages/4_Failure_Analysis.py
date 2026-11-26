import streamlit as st

st.title("🔍 Failure Analysis")

case = st.selectbox(
    "Select Case",
    [
        "Case 1",
        "Case 2",
        "Case 3"
    ]
)

left, right = st.columns(2)

with left:

    st.subheader("Baseline ReAct")

    st.error("""
    Observation:

    Incomplete evidence

    Prediction:

    Incorrect
    """)

with right:

    st.subheader("Recovery ReAct")

    st.success("""
    Additional retrieval performed

    New evidence collected

    Prediction:

    Correct
    """)

st.markdown("---")

st.subheader("Interpretation")

st.write("""
The recovery mechanism detected poor evidence quality,
performed additional retrieval, and improved the final
prediction.
""")