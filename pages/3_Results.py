import streamlit as st
import pandas as pd

st.title("📊 Experimental Results")

results = pd.DataFrame(
    {
        "Method": [
            "Baseline ReAct",
            "Recovery ReAct"
        ],
        "Accuracy": [
            70,
            78
        ]
    }
)

st.dataframe(results)

st.bar_chart(
    results.set_index("Method")
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Claims Evaluated",
    "30"
)

col2.metric(
    "Recovery Triggers",
    "8"
)

col3.metric(
    "Errors Corrected",
    "5"
)

col4.metric(
    "Improvement",
    "+8%"
)

st.markdown("---")

st.subheader("Discussion")

st.write("""
Recovery was most useful when the initial retrieval
produced incomplete or misleading evidence.
""")