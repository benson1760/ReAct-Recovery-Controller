"""Evaluate saved ReAct trajectories and write summary metrics."""

import json
from collections import Counter
from pathlib import Path


def load_jsonl(input_path):
    """Load trajectory records from a JSONL file."""

    records = []

    with Path(input_path).open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error

    return records


def calculate_metrics(records):
    """Calculate summary metrics from trajectory records."""

    total_cases = len(records)

    if total_cases == 0:
        return {
            "total_cases": 0,
            "correct_cases": 0,
            "accuracy": 0.0,
            "completion_rate": 0.0,
            "average_tool_calls": 0.0,
            "average_trajectory_length": 0.0,
            "average_runtime_seconds": 0.0,
            "predicted_label_counts": {},
            "gold_label_counts": {},
            "failure_type_counts": {}
        }

    correct_cases = sum(record.get("correct", False) for record in records)

    completed_cases = sum(
        record.get("completed", False)
        for record in records
    )

    total_tool_calls = sum(
        record.get("tool_calls", 0)
        for record in records
    )

    total_trajectory_length = sum(
        record.get("trajectory_length", 0)
        for record in records
    )

    total_runtime = sum(
        record.get("runtime_seconds", 0.0)
        for record in records
    )

    predicted_labels = Counter(
        record.get("predicted_label", "UNKNOWN")
        for record in records
    )

    gold_labels = Counter(
        record.get("gold_label", "UNKNOWN")
        for record in records
    )

    failure_types = Counter(
        record["failure_type"]
        for record in records
        if record.get("failure_type")
    )

    return {
        "total_cases": total_cases,
        "correct_cases": correct_cases,
        "accuracy": round(correct_cases / total_cases, 4),
        "completed_cases": completed_cases,
        "completion_rate": round(completed_cases / total_cases, 4),
        "average_tool_calls": round(
            total_tool_calls / total_cases,
            4
        ),
        "average_trajectory_length": round(
            total_trajectory_length / total_cases,
            4
        ),
        "average_runtime_seconds": round(
            total_runtime / total_cases,
            6
        ),
        "predicted_label_counts": dict(predicted_labels),
        "gold_label_counts": dict(gold_labels),
        "failure_type_counts": dict(failure_types),
        "pipeline_mode": records[0].get(
            "pipeline_mode",
            "unknown"
        ),
        "condition": records[0].get(
            "condition",
            "unknown"
        ),
        "interpretation": (
            "Controlled pipeline-validation metrics. "
            "These are not official FEVER benchmark results."
        )
    }


def save_metrics(metrics, output_path):
    """Save metrics as formatted JSON."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)


def evaluate_file(input_path, output_path):
    """Load trajectories, calculate metrics, and save results."""

    records = load_jsonl(input_path)
    metrics = calculate_metrics(records)
    save_metrics(metrics, output_path)

    return metrics


if __name__ == "__main__":
    input_file = "results/logs/baseline_validation.jsonl"
    output_file = (
        "results/metrics/baseline_validation_metrics.json"
    )

    results = evaluate_file(input_file, output_file)

    print("Evaluation completed")
    print("Total cases:", results["total_cases"])
    print("Correct cases:", results["correct_cases"])
    print(f"Accuracy: {results['accuracy']:.2%}")
    print(f"Completion rate: {results['completion_rate']:.2%}")
    print("Metrics saved to:", output_file)