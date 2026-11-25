"""
Enforced Reformulation Condition

If retrieval quality is poor, force the controller
to generate a reformulated query and retrieve again.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.baseline.model_react_agent import ModelReActAgent
from src.retrieval.evidence_retriever import EvidenceRetriever
from src.controller.recovery_controller import RecoveryController

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
    / "enforced_reformulation_results.json"
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

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

    controller = RecoveryController()

    results = []

    for sample in pilot:

        claim = sample["claim"]

        retrieved = retriever.search(
            claim,
            top_k=3
        )

        decision = controller.process(
            claim,
            retrieved
        )

        final_results = retrieved

        # Enforce reformulation if controller requests it
        if decision["action"] == "REFORMULATE":

            reformulated_query = (
                decision[
                    "reformulated_query"
                ]
            )

            final_results = retriever.search(
                reformulated_query,
                top_k=3
            )

        evidence_text = "\n\n".join(
            item["summary"]
            for item in final_results
        )

        prediction = agent.predict(
            claim,
            evidence_text
        )

        record = {
            "condition":
                "ENFORCED_REFORMULATION",

            "fever_id":
                sample["fever_id"],

            "claim":
                claim,

            "controller_action":
                decision["action"],

            "original_query":
                decision["original_query"],

            "reformulated_query":
                decision[
                    "reformulated_query"
                ],

            "top_page":
                (
                    final_results[0]["page_title"]
                    if final_results
                    else None
                ),

            "gold_label":
                sample["gold_label"],

            "prediction":
                prediction["prediction"],

            "correct":
                (
                    prediction["prediction"]
                    == sample["gold_label"]
                )
        }

        results.append(record)

    correct = sum(
        item["correct"]
        for item in results
    )

    accuracy = correct / len(results)

    print("=" * 60)
    print(
        "ENFORCED REFORMULATION RESULTS"
    )
    print("=" * 60)

    print("Cases:", len(results))
    print("Correct:", correct)

    print(
        "Accuracy:",
        round(
            accuracy,
            4
        )
    )

    save_json(
        results,
        RESULTS_FILE
    )

    print()
    print(
        "Saved:",
        RESULTS_FILE
    )


if __name__ == "__main__":
    main()