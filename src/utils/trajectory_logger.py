"""Save ReAct experiment trajectories as JSONL records."""

import json
from datetime import datetime, timezone
from pathlib import Path


class TrajectoryLogger:
    """Save complete experiment trajectories in JSON Lines format."""

    def __init__(self, output_path):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, trajectory):
        """Save one experiment trajectory."""

        record = dict(trajectory)
        record["logged_at_utc"] = datetime.now(timezone.utc).isoformat()

        with self.output_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def clear(self):
        """Delete an existing log before starting a new experiment."""

        if self.output_path.exists():
            self.output_path.unlink()


if __name__ == "__main__":
    logger = TrajectoryLogger("results/logs/logger_test.jsonl")
    logger.clear()

    sample_trajectory = {
        "case_id": "fever_001",
        "claim": "The Eiffel Tower is located in Paris.",
        "gold_label": "SUPPORTS",
        "condition": "standard_react",
        "actions": [
            {
                "step": 1,
                "type": "search",
                "query": "Eiffel Tower location"
            }
        ],
        "observations": [
            {
                "step": 1,
                "productive": True,
                "text": "The Eiffel Tower is located in Paris, France."
            }
        ],
        "predicted_label": "SUPPORTS",
        "correct": True,
        "completed": True
    }

    logger.save(sample_trajectory)

    print("Test trajectory saved to:", logger.output_path)