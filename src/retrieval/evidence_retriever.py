"""
Semantic retrieval for FEVER evidence corpus.
"""

import json

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class EvidenceRetriever:

    def __init__(
        self,
        corpus_path=(
            "data/processed/fever/"
            "fever_pilot_evidence.json"
        )
    ):

        with open(
            corpus_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.corpus = json.load(file)

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.texts = [
            page["summary"]
            for page in self.corpus
        ]

        print("Encoding corpus...")

        self.embeddings = self.model.encode(
            self.texts,
            convert_to_tensor=True
        )

    def search(
        self,
        claim,
        top_k=3
    ):

        claim_embedding = self.model.encode(
            claim,
            convert_to_tensor=True
        )

        similarities = cos_sim(
            claim_embedding,
            self.embeddings
        )[0]

        top = similarities.topk(
            min(top_k, len(self.corpus))
        )

        results = []

        for score, idx in zip(
            top.values,
            top.indices
        ):

            page = self.corpus[int(idx)]

            results.append(
                {
                    "page_title":
                        page["page_title"],
                    "summary":
                        page["summary"],
                    "score":
                        float(score)
                }
            )

        return results


if __name__ == "__main__":

    retriever = EvidenceRetriever()

    query = (
        "A River Runs Through It "
        "has been nominated for an Oscar."
    )

    results = retriever.search(query)

    print("\nResults:\n")

    for result in results:

        print(
            result["page_title"],
            result["score"]
        )