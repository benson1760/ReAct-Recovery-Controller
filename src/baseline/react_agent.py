"""Controlled ReAct baseline used to validate the experiment pipeline."""

import time


class BaselineReActAgent:
    """Run a simple Thought-Action-Observation validation trajectory."""

    def __init__(self, retriever, condition="standard_react"):
        self.retriever = retriever
        self.condition = condition

    def predict_label(self, evidence):
        """
        Produce a FEVER label from controlled evidence annotations.

        This validates the pipeline mechanics.
        It is not the final language-model classifier.
        """

        if not evidence:
            return "NOT ENOUGH INFO"

        stances = {
            item.get("stance", "NOT ENOUGH INFO").upper()
            for item in evidence
        }

        if "REFUTES" in stances:
            return "REFUTES"

        if "SUPPORTS" in stances:
            return "SUPPORTS"

        return "NOT ENOUGH INFO"

    def run(self, case):
        """Run one controlled ReAct trajectory."""

        start_time = time.perf_counter()

        # Thought
        thought = (
            "I need to retrieve evidence relevant to the claim "
            "before selecting a FEVER label."
        )

        # Action
        action = {
            "step": 1,
            "type": "search",
            "query": case.get("search_query", "")
        }

        # Observation
        retrieval_result = self.retriever.retrieve(case)
        evidence = retrieval_result["evidence"]

        observation = {
            "step": 1,
            "productive": retrieval_result["productive"],
            "result_count": retrieval_result["result_count"],
            "evidence": evidence
        }

        # Final answer
        predicted_label = self.predict_label(evidence)
        gold_label = case["gold_label"]
        correct = predicted_label == gold_label

        runtime_seconds = time.perf_counter() - start_time

        return {
            "case_id": case["case_id"],
            "claim": case["claim"],
            "gold_label": gold_label,
            "condition": self.condition,
            "thoughts": [thought],
            "actions": [action],
            "observations": [observation],
            "predicted_label": predicted_label,
            "correct": correct,
            "completed": True,
            "tool_calls": 1,
            "trajectory_length": 1,
            "runtime_seconds": round(runtime_seconds, 6),
            "failure_type": (
                None if correct else "incorrect_classification"
            ),
            "pipeline_mode": "controlled_validation"
        }