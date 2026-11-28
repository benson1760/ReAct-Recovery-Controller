@"
# ReAct Recovery Controller Demo

This presentation-specific Streamlit application demonstrates the
semantic retrieval component of the ReAct Recovery Controller project.

## Live Component

- FEVER claim input
- SentenceTransformer semantic retrieval
- Local 22-page evidence corpus
- Ranked evidence pages and similarity scores

## Saved Experimental Outcomes

- Standard ReAct: 63.33%
- Detection Only: 70.00%
- Enforced Reformulation: 53.33%

## Run Locally

```powershell
streamlit run .\demo\streamlit_demo.py