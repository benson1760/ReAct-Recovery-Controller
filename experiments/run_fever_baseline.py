"""
Run the model-based ReAct baseline on the FEVER pilot.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.baseline.model_react_agent import ModelReActAgent
from src.retrieval.evidence_retriever import EvidenceRetriever

PILOT_FILE = (
    REPO_ROOT
    / "data"
    / "samples"
    / "fever_pilot_30.json"
)

RESULTS_FILE = (
    REPO_ROOT
    / "results"
    / "metrics"
    / "standard_react_results.json"
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():

    pilot = load_json(PILOT_FILE)

    retriever = EvidenceRetriever()

    agent = ModelReActAgent()

    results = []

    print("=" * 80)
    print("RUNNING STANDARD REACT BASELINE")
    print("=" * 80)

    for sample in pilot:

        claim = sample["claim"]

        retrieved = retriever.search(
            claim,
            top_k=3
        )

        evidence_text = "\n\n".join(
            item["summary"]
            for item in retrieved
        )

        result = agent.predict(
            claim,
            evidence_text
        )

        record = {
            "fever_id": sample["fever_id"],
            "claim": claim,
            "top_page": (
                retrieved[0]["page_title"]
                if retrieved
                else None
            ),
            "top_score": (
                float(retrieved[0]["score"])
                if retrieved
                else None
            ),
            "gold_label":
                sample["gold_label"],
            "prediction":
                result["prediction"],
            "correct":
                (
                    result["prediction"]
                    == sample["gold_label"]
                )
        }

        results.append(record)

        print("=" * 80)

        print("CLAIM:")
        print(claim)

        print()

        print(
            "TOP PAGE:",
            record["top_page"]
        )

        print(
            "TOP SCORE:",
            record["top_score"]
        )

        print()

        print(
            "GOLD LABEL:",
            record["gold_label"]
        )

        print(
            "PREDICTION:",
            record["prediction"]
        )

        if record["correct"]:
            print("RESULT: CORRECT")
        else:
            print("RESULT: INCORRECT")

        print("=" * 80)
        print()

    correct = sum(
        item["correct"]
        for item in results
    )

    accuracy = correct / len(results)

    print("\n")
    print("=" * 80)
    print("BASELINE SUMMARY")
    print("=" * 80)

    print(
        "Total Cases:",
        len(results)
    )

    print(
        "Correct:",
        correct
    )

    print(
        "Accuracy:",
        round(accuracy, 4)
    )

    save_json(
        results,
        RESULTS_FILE
    )

    print()
    print(
        "Results saved to:",
        RESULTS_FILE
    )


if __name__ == "__main__":
    main()