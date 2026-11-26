import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="ReAct Recovery Controller",
    layout="wide"
)

st.title("ReAct Recovery Controller")

st.markdown(
    """
    Research Question:

    Can enforced query reformulation improve recovery
    after poor retrieval compared with standard ReAct?
    """
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Retrieval Demo",
        "Results",
        "Failure Analysis"
    ]
)

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

with tab1:

    st.header("Project Overview")

    st.markdown(
        """
        Conditions:

        - Standard ReAct
        - Detection Only
        - Enforced Reformulation

        FEVER Pilot:

        - 30 Claims
        - 10 SUPPORTS
        - 10 REFUTES
        - 10 NOT ENOUGH INFO
        """
    )

# --------------------------------------------------
# RETRIEVAL DEMO
# --------------------------------------------------

with tab2:

    st.header("Retrieval Improvement Demo")

    st.subheader(
        "Claim"
    )

    st.code(
        "A River Runs Through It has been nominated for an Oscar."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### Before Semantic Retrieval"
        )

        st.code(
            """
Ted Cruz
Melilla
Guns N' Roses
            """
        )

    with col2:

        st.markdown(
            "### After Semantic Retrieval"
        )

        st.code(
            """
A River Runs Through It (film)
Easy A
The Little Prince (2015 film)
            """
        )

    st.success(
        "Semantic retrieval fixed a major retrieval bottleneck."
    )

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

with tab3:

    st.header(
        "Experimental Results"
    )

    comparison = pd.DataFrame(
        {
            "Condition": [
                "Standard ReAct",
                "Detection Only",
                "Enforced Reformulation"
            ],
            "Accuracy": [
                63.33,
                70.00,
                53.33
            ]
        }
    )

    st.table(comparison)

    st.markdown(
        """
        Key Findings

        ✅ Detection improved performance.

        ✅ Detection Only achieved the highest accuracy.

        ❌ Forced Reformulation reduced performance.
        """
    )

# --------------------------------------------------
# FAILURE ANALYSIS
# --------------------------------------------------

with tab4:

    st.header("Failure Analysis")

    failures = pd.DataFrame(
        {
            "Failure Type": [
                "Retrieval Failure",
                "Evidence Depth Failure",
                "Reasoning Failure"
            ],
            "Count": [
                4,
                4,
                3
            ]
        }
    )

    st.table(failures)

    st.markdown(
        """
        Interpretation

        Most failures occurred before the reasoning stage.

        Retrieval and evidence quality were larger bottlenecks
        than model reasoning for this pilot dataset.
        """
    )