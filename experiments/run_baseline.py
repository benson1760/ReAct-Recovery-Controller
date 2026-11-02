"""Run the controlled three-case baseline validation."""

import json
import sys
from pathlib import Path


# Add the repository root to Python's import path.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.baseline.react_agent import BaselineReActAgent
from src.retrieval.retriever import LocalRetriever
from src.utils.trajectory_logger import TrajectoryLogger


def load_json(file_path):
    """Load and return a JSON file."""

    with Path(file_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """Run all controlled validation cases."""

    config_path = REPO_ROOT / "configs" / "baseline_config.json"
    config = load_json(config_path)

    dataset_path = REPO_ROOT / config["dataset_path"]
    results_path = REPO_ROOT / config["results_path"]

    cases = load_json(dataset_path)

    retriever = LocalRetriever()

    agent = BaselineReActAgent(
        retriever=retriever,
        condition=config["agent"]["condition"]
    )

    logger = TrajectoryLogger(results_path)

    # Begin with a fresh log for every validation run.
    logger.clear()

    results = []

    print("=" * 60)
    print("Controlled ReAct Baseline Validation")
    print("=" * 60)
    print("Cases:", len(cases))
    print("Condition:", config["agent"]["condition"])
    print("Pipeline mode: controlled_validation")
    print()

    for case in cases:
        trajectory = agent.run(case)
        logger.save(trajectory)
        results.append(trajectory)

        result_text = "PASS" if trajectory["correct"] else "FAIL"

        print(
            f"{trajectory['case_id']}: "
            f"predicted={trajectory['predicted_label']} | "
            f"gold={trajectory['gold_label']} | "
            f"{result_text}"
        )

    total_cases = len(results)
    correct_cases = sum(result["correct"] for result in results)
    accuracy = correct_cases / total_cases if total_cases else 0.0
    completed_cases = sum(result["completed"] for result in results)
    completion_rate = (
        completed_cases / total_cases if total_cases else 0.0
    )
    average_tool_calls = (
        sum(result["tool_calls"] for result in results) / total_cases
        if total_cases
        else 0.0
    )
    average_runtime = (
        sum(result["runtime_seconds"] for result in results) / total_cases
        if total_cases
        else 0.0
    )

    print()
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Total cases: {total_cases}")
    print(f"Correct cases: {correct_cases}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Completion rate: {completion_rate:.2%}")
    print(f"Average tool calls: {average_tool_calls:.2f}")
    print(f"Average runtime: {average_runtime:.6f} seconds")
    print(f"Trajectory log: {results_path}")
    print()
    print(
        "Note: These results validate the pipeline mechanics. "
        "They are not official FEVER benchmark results."
    )


if __name__ == "__main__":
    main()