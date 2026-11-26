import streamlit as st

st.title("📖 Project Overview")

st.markdown("""
## Research Question

Can observation quality monitoring improve the robustness
of ReAct-based reasoning agents?

---

## Base Model

microsoft/Phi-3-mini-4k-instruct

## Framework

ReAct (Reason + Act)

## Enhancement

- Observation Quality Control
- Adaptive Recovery

---
""")

st.subheader("Architecture")

st.code("""
Claim
   ↓
Retriever
   ↓
ReAct Agent
   ↓
Quality Checker
   ↓
Recovery Controller
   ↓
Prediction
""")

st.markdown("""
### Hypothesis

Low-quality observations lead to reasoning failures.

By detecting poor observations and triggering recovery
strategies, prediction accuracy can improve.
""")