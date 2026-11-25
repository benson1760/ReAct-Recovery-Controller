"""
Recovery Controller

Purpose:
Detect potentially unproductive retrieval results and
generate a reformulated query.

This is the project's primary intervention.

Baseline:
Claim
    ↓
Retriever
    ↓
Evidence
    ↓
Prediction

Controlled:
Claim
    ↓
Retriever
    ↓
Recovery Controller
    ↓
Reformulated Query
    ↓
Retriever
    ↓
Prediction
"""

import re


class RecoveryController:

    def __init__(
        self,
        min_similarity_score=0.30
    ):
        """
        Parameters
        ----------
        min_similarity_score : float

        Retrieval results below this threshold
        are considered potentially unproductive.
        """
        self.min_similarity_score = (
            min_similarity_score
        )

    def is_unproductive(
        self,
        claim,
        retrieved_results
    ):
        """
        Determine whether retrieval appears
        unproductive.
        """

        if not retrieved_results:
            return True

        top_score = retrieved_results[0].get(
            "score",
            0
        )

        if top_score < self.min_similarity_score:
            return True

        return False

    def reformulate(
        self,
        claim
    ):
        """
        Generate a meaningfully different query.

        Current implementation:
        remove stop words
        preserve key entities
        shorten query

        More advanced reformulation can be
        implemented later.
        """

        stop_words = {
            "a",
            "an",
            "the",
            "is",
            "was",
            "were",
            "are",
            "of",
            "to",
            "in",
            "for",
            "has",
            "have",
            "had",
            "been"
        }

        tokens = re.findall(
            r"\w+",
            claim
        )

        filtered = [
            token
            for token in tokens
            if token.lower()
            not in stop_words
        ]

        return " ".join(filtered)

    def process(
        self,
        claim,
        retrieved_results
    ):
        """
        Main controller entry point.
        """

        unproductive = self.is_unproductive(
            claim,
            retrieved_results
        )

        if unproductive:

            return {
                "action":
                    "REFORMULATE",

                "original_query":
                    claim,

                "reformulated_query":
                    self.reformulate(claim),

                "reason":
                    "Low retrieval quality"
            }

        return {
            "action":
                "ACCEPT",

            "original_query":
                claim,

            "reformulated_query":
                None,

            "reason":
                "Retrieval accepted"
        }


if __name__ == "__main__":

    controller = RecoveryController()

    example_claim = (
        "A River Runs Through It "
        "has been nominated for an Oscar."
    )

    poor_results = [
        {
            "page_title":
                "Ted Cruz",
            "score":
                0.12
        }
    ]

    decision = controller.process(
        example_claim,
        poor_results
    )

    print("\nController Decision\n")
    print(decision)
