import streamlit as st

st.title("🚀 Live Agent Demo")

col1, col2 = st.columns([1,1])

with col1:

    mode = st.radio(
        "Select Agent",
        [
            "Baseline ReAct",
            "Recovery ReAct"
        ]
    )

with col2:

    sample_claim = st.selectbox(
        "Sample Claim",
        [
            "The Eiffel Tower is located in Berlin.",
            "The Pacific Ocean is larger than the Atlantic Ocean.",
            "The moon is a planet."
        ]
    )

claim = st.text_area(
    "Enter Claim",
    value=sample_claim,
    height=100
)

run = st.button("▶ Run Agent")

st.divider()

left, center, right = st.columns([2,2,1])

with left:

    st.subheader("Reasoning Trajectory")

    trajectory_placeholder = st.empty()

with center:

    st.subheader("Quality Analysis")

    quality_placeholder = st.empty()

with right:

    st.subheader("Prediction")

    prediction_placeholder = st.empty()

if run:

    trajectory_placeholder.markdown("""
    ✅ Thought

    Need evidence related to the claim.

    ✅ Action

    Search(Eiffel Tower)

    ✅ Observation

    The Eiffel Tower is located in Paris.
    """)

    if mode == "Recovery ReAct":

        quality_placeholder.success("""
        Quality Score: 0.82

        Consistency Check: PASS

        Recovery Triggered: NO
        """)

    prediction_placeholder.success("""
    REFUTES

    Confidence: 0.93
    """)