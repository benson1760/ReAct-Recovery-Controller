"""
Presentation-only Streamlit demo for the ReAct Recovery Controller.

Live component:
    Claim -> EvidenceRetriever -> Local evidence corpus -> Ranked evidence

Saved experimental component:
    Standard ReAct
    Detection Only
    Enforced Reformulation

Run from the repository root:

    streamlit run .\demo\streamlit_demo.py
"""

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# Repository paths
# =========================================================

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from src.retrieval.evidence_retriever import EvidenceRetriever


PILOT_FILE = (
    REPO_ROOT
    / "data"
    / "samples"
    / "fever_pilot_30.json"
)

STANDARD_RESULTS_FILE = (
    REPO_ROOT
    / "results"
    / "metrics"
    / "standard_react_results.json"
)

DETECTION_RESULTS_FILE = (
    REPO_ROOT
    / "results"
    / "metrics"
    / "detection_only_results.json"
)

REFORMULATION_RESULTS_FILE = (
    REPO_ROOT
    / "results"
    / "metrics"
    / "enforced_reformulation_results.json"
)

DIAGNOSTIC_FILE = (
    REPO_ROOT
    / "results"
    / "metrics"
    / "diagnostic_comparison.json"
)

FAILURE_ANALYSIS_FILE = (
    REPO_ROOT
    / "results"
    / "tables"
    / "failure_analysis.csv"
)


# =========================================================
# Streamlit page configuration
# =========================================================

st.set_page_config(
    page_title="ReAct Recovery Controller Demo",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Styling
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1350px;
        }

        .demo-header {
            padding: 1.2rem 1.4rem;
            border-radius: 14px;
            background:
                linear-gradient(
                    120deg,
                    #072536 0%,
                    #0b4253 55%,
                    #087f7a 100%
                );
            color: white;
            margin-bottom: 1rem;
        }

        .demo-header h1 {
            margin: 0;
            font-size: 2.2rem;
        }

        .demo-header p {
            color: #d7eff0;
            font-size: 1.05rem;
            margin-top: 0.4rem;
            margin-bottom: 0;
        }

        .case-box {
            padding: 1rem 1.1rem;
            border-radius: 12px;
            border: 1px solid #2c6672;
            background-color: #0c2532;
            margin-bottom: 1rem;
        }

        .finding-box {
            padding: 1rem 1.1rem;
            border-left: 5px solid #16c4b8;
            border-radius: 8px;
            background-color: #102d39;
            margin-top: 1rem;
        }

        .warning-box {
            padding: 1rem 1.1rem;
            border-left: 5px solid #e8a43d;
            border-radius: 8px;
            background-color: #322819;
            margin-top: 1rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #335866;
            border-radius: 12px;
            padding: 0.7rem;
            background-color: #0b2532;
        }

        div[data-testid="stExpander"] {
            border-color: #345b68;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Utility functions
# =========================================================

def load_json(path: Path):
    """
    Load JSON data.

    Returns an empty list or dictionary if the file
    does not exist.
    """

    if not path.exists():
        return None

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def normalize_text(value):
    """
    Normalize text for exact claim matching.
    """

    return str(value).strip().lower()


def find_record(records, claim):
    """
    Find the saved experimental record matching a claim.
    """

    if not records:
        return None

    normalized_claim = normalize_text(claim)

    for record in records:
        record_claim = normalize_text(
            record.get("claim", "")
        )

        if record_claim == normalized_claim:
            return record

    return None


def show_condition_card(
    condition_name,
    record,
):
    """
    Display one condition's saved result.
    """

    st.markdown(
        f"### {condition_name}"
    )

    if record is None:
        st.warning(
            "No saved result is available "
            "for this claim."
        )
        return

    prediction = record.get(
        "prediction",
        "Unavailable"
    )

    correct = bool(
        record.get("correct", False)
    )

    st.write(
        f"**Prediction:** `{prediction}`"
    )

    if correct:
        st.success("Correct")
    else:
        st.error("Incorrect")

    controller_action = record.get(
        "controller_action"
    )

    if controller_action:
        st.write(
            "**Controller action:** "
            f"`{controller_action}`"
        )

    reformulated_query = record.get(
        "reformulated_query"
    )

    if reformulated_query:
        st.write(
            "**Reformulated query:**"
        )

        st.code(
            reformulated_query,
            language=None,
        )

    top_page = record.get(
        "top_page"
    )

    if top_page:
        st.caption(
            f"Saved top page: {top_page}"
        )


def show_demo_interpretation(
    selected_name,
    standard_record,
    detection_record,
    reformulation_record,
):
    """
    Display the prepared interpretation for the selected case.
    """

    if selected_name.startswith(
        "Primary demo"
    ):
        st.markdown(
            """
            <div class="warning-box">
                <strong>Evidence-depth failure:</strong>
                the semantic retriever found the correct movie page,
                but the summary did not contain information about
                the Oscar nomination. Correct page retrieval did not
                guarantee sufficient evidence.
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif selected_name.startswith(
        "Detection improvement"
    ):
        standard_correct = (
            standard_record
            and standard_record.get(
                "correct",
                False
            )
        )

        detection_correct = (
            detection_record
            and detection_record.get(
                "correct",
                False
            )
        )

        if (
            not standard_correct
            and detection_correct
        ):
            st.markdown(
                """
                <div class="finding-box">
                    <strong>Detection corrected the baseline:</strong>
                    the warning changed an overconfident
                    <code>REFUTES</code> decision to the correct
                    <code>NOT ENOUGH INFO</code> label.
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif selected_name.startswith(
        "Clear successful"
    ):
        st.markdown(
            """
            <div class="finding-box">
                <strong>Clean success case:</strong>
                the retriever found the correct page and the model
                produced the correct FEVER label.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if (
        reformulation_record
        and reformulation_record.get(
            "controller_action"
        ) == "REFORMULATE"
    ):
        st.caption(
            "The enforced condition generated and used "
            "a reformulated query for this case."
        )


# =========================================================
# Load project data
# =========================================================

pilot_data = load_json(
    PILOT_FILE
) or []

standard_results = load_json(
    STANDARD_RESULTS_FILE
) or []

detection_results = load_json(
    DETECTION_RESULTS_FILE
) or []

reformulation_results = load_json(
    REFORMULATION_RESULTS_FILE
) or []

diagnostic_results = load_json(
    DIAGNOSTIC_FILE
) or {}


# =========================================================
# Cache semantic retriever
# =========================================================

@st.cache_resource(
    show_spinner=(
        "Loading the semantic retriever "
        "and encoding the evidence corpus..."
    )
)
def load_retriever():
    """
    Load the actual project EvidenceRetriever once.
    """

    return EvidenceRetriever()


# =========================================================
# Header
# =========================================================

st.markdown(
    """
    <div class="demo-header">
        <h1>ReAct Recovery Controller</h1>
        <p>
            Live semantic retrieval with saved outcomes from
            Standard ReAct, Detection Only, and Enforced Reformulation
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Prepared demonstration cases
# =========================================================

DEMO_CASES = {
    (
        "Primary demo — correct page, "
        "insufficient evidence"
    ): (
        "A River Runs Through It has been "
        "nominated for an Oscar."
    ),

    (
        "Detection improvement — Hair musical"
    ): (
        "After its revival in 2009 "
        "Hair (musical) won a Tony."
    ),

    (
        "Detection improvement — See.SZA.Run"
    ): (
        "See.SZA.Run is influenced by "
        "Jay-Z and Lil Kim."
    ),

    (
        "Clear successful verification — Libya"
    ): (
        "Libya is a country outside of Africa."
    ),
}


selected_name = st.selectbox(
    "Prepared demonstration case",
    options=list(DEMO_CASES.keys()),
)

default_claim = DEMO_CASES[
    selected_name
]

claim = st.text_area(
    "FEVER claim",
    value=default_claim,
    height=85,
)

control_col1, control_col2 = st.columns(
    [3, 1]
)

with control_col1:
    run_demo = st.button(
        "Run Live Project Pipeline",
        type="primary",
        use_container_width=True,
    )

with control_col2:
    top_k = st.selectbox(
        "Top results",
        options=[1, 3, 5],
        index=1,
    )


# =========================================================
# Results summary always visible
# =========================================================

st.markdown("---")

st.subheader(
    "Completed Experiment Summary"
)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Standard ReAct",
        "63.33%",
        help="19 correct out of 30 claims",
    )

with metric2:
    st.metric(
        "Detection Only",
        "70.00%",
        "+6.67 percentage points",
        help="21 correct out of 30 claims",
    )

with metric3:
    st.metric(
        "Enforced Reformulation",
        "53.33%",
        "-10.00 percentage points",
        delta_color="inverse",
        help="16 correct out of 30 claims",
    )


# =========================================================
# Execute live retrieval
# =========================================================

if run_demo:

    if not claim.strip():
        st.error(
            "Enter a claim before running the demo."
        )
        st.stop()

    try:
        retriever = load_retriever()

        with st.spinner(
            "Running semantic retrieval against "
            "the local evidence corpus..."
        ):
            retrieved = retriever.search(
                claim,
                top_k=top_k,
            )

    except Exception as error:
        st.error(
            "The semantic retriever could not run."
        )

        st.exception(error)
        st.stop()

    st.markdown("---")

    st.subheader(
        "1. Live Semantic Retrieval"
    )

    st.success(
        "The claim was searched using the project's "
        "actual EvidenceRetriever."
    )

    pilot_record = find_record(
        pilot_data,
        claim,
    )

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        if pilot_record:
            st.write(
                "**FEVER ID:**",
                pilot_record.get("fever_id"),
            )
        else:
            st.write(
                "**FEVER ID:** Custom claim"
            )

    with info_col2:
        if pilot_record:
            st.write(
                "**Gold label:**",
                pilot_record.get(
                    "gold_label"
                ),
            )
        else:
            st.write(
                "**Gold label:** Unavailable"
            )

    if not retrieved:
        st.warning(
            "The retriever returned no evidence."
        )

    for index, result in enumerate(
        retrieved,
        start=1,
    ):
        page_title = result.get(
            "page_title",
            "Unknown page",
        )

        score = float(
            result.get("score", 0.0)
        )

        summary = result.get(
            "summary",
            "No evidence summary available.",
        )

        with st.expander(
            (
                f"{index}. {page_title} "
                f"— similarity score {score:.4f}"
            ),
            expanded=(index == 1),
        ):
            st.write(summary)

    st.subheader(
        "2. Saved Experimental Outcomes"
    )

    st.caption(
        "These outcomes were produced by the completed "
        "30-claim experiments using Phi-3 Mini."
    )

    standard_record = find_record(
        standard_results,
        claim,
    )

    detection_record = find_record(
        detection_results,
        claim,
    )

    reformulation_record = find_record(
        reformulation_results,
        claim,
    )

    condition_col1, condition_col2, condition_col3 = (
        st.columns(3)
    )

    with condition_col1:
        show_condition_card(
            "Standard ReAct",
            standard_record,
        )

    with condition_col2:
        show_condition_card(
            "Detection Only",
            detection_record,
        )

    with condition_col3:
        show_condition_card(
            "Enforced Reformulation",
            reformulation_record,
        )

    st.subheader(
        "3. Interpretation"
    )

    show_demo_interpretation(
        selected_name,
        standard_record,
        detection_record,
        reformulation_record,
    )


# =========================================================
# Failure-analysis summary
# =========================================================

st.markdown("---")

with st.expander(
    "Show baseline failure analysis",
    expanded=False,
):
    failures = pd.DataFrame(
        {
            "Failure Type": [
                "Retrieval Failure",
                "Evidence-Depth Failure",
                "Reasoning Failure",
            ],
            "Count": [
                4,
                4,
                3,
            ],
        }
    )

    failure_col1, failure_col2 = (
        st.columns([1, 1.4])
    )

    with failure_col1:
        st.dataframe(
            failures,
            use_container_width=True,
            hide_index=True,
        )

    with failure_col2:
        st.bar_chart(
            failures.set_index(
                "Failure Type"
            ),
            y="Count",
        )

    st.info(
        "Eight of the eleven baseline errors were "
        "retrieval or evidence-quality related. "
        "Only three were categorized as reasoning failures."
    )


# =========================================================
# Footer
# =========================================================

st.markdown("---")

st.caption(
    "Live retrieval uses the actual project corpus and "
    "EvidenceRetriever. Model outcomes are loaded from "
    "the saved, completed experimental runs."
)