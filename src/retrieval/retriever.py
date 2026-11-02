"""Simple local evidence retriever for pipeline validation."""


class LocalRetriever:
    """Returns evidence stored inside a validation case."""

    def retrieve(self, case):
        """
        Retrieve the evidence associated with one case.

        Parameters
        ----------
        case : dict
            A validation case containing a search query and evidence.

        Returns
        -------
        dict
            The query, retrieved evidence, and retrieval status.
        """

        query = case.get("search_query", "")
        evidence = case.get("evidence", [])

        # A retrieval is productive when at least one evidence item exists.
        productive = len(evidence) > 0

        return {
            "query": query,
            "evidence": evidence,
            "productive": productive,
            "result_count": len(evidence)
        }


if __name__ == "__main__":
    # Small test to confirm that this file runs independently.
    sample_case = {
        "search_query": "Eiffel Tower location",
        "evidence": [
            {
                "document_id": "eiffel_tower",
                "text": "The Eiffel Tower is located in Paris, France."
            }
        ]
    }

    retriever = LocalRetriever()
    result = retriever.retrieve(sample_case)

    print("Query:", result["query"])
    print("Productive:", result["productive"])
    print("Result count:", result["result_count"])
    print("Evidence:", result["evidence"])