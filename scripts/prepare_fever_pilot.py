"""Create a reproducible 30-case pilot from the official FEVER dataset."""

import json
import random
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


# Find the root directory of the repository.
REPO_ROOT = Path(__file__).resolve().parents[1]

# Official FEVER development file downloaded earlier.
SOURCE_PATH = (
    REPO_ROOT
    / "data"
    / "raw"
    / "fever"
    / "shared_task_dev.jsonl"
)

# Balanced 30-case pilot used for the preliminary experiment.
OUTPUT_PATH = (
    REPO_ROOT
    / "data"
    / "samples"
    / "fever_pilot_30.json"
)

# Metadata describing how the pilot was created.
METADATA_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_pilot_30_metadata.json"
)

TARGET_LABELS = [
    "SUPPORTS",
    "REFUTES",
    "NOT ENOUGH INFO"
]

CASES_PER_LABEL = 10
RANDOM_SEED = 42


def load_jsonl(file_path):
    """Load JSON records from a JSONL file."""

    records = []

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Skip blank lines.
            if not line:
                continue

            try:
                record = json.loads(line)
                records.append(record)

            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {error}"
                ) from error

    return records


def validate_record(record):
    """Check whether a FEVER record contains the required values."""

    required_fields = {
        "id",
        "verifiable",
        "label",
        "claim",
        "evidence"
    }

    fields_exist = required_fields.issubset(record)

    label_is_valid = (
        record.get("label") in TARGET_LABELS
    )

    claim = record.get("claim")

    claim_is_valid = (
        isinstance(claim, str)
        and bool(claim.strip())
    )

    return (
        fields_exist
        and label_is_valid
        and claim_is_valid
    )


def convert_record(record):
    """Convert one official FEVER record into the pilot format."""

    return {
        "fever_id": record["id"],
        "claim": record["claim"],
        "gold_label": record["label"],
        "verifiable": record["verifiable"],
        "source_dataset": "FEVER v1.0",
        "source_split": "shared_task_dev",
        "evidence": record["evidence"],
        "sampling_seed": RANDOM_SEED
    }


def create_balanced_sample(records):
    """Select 10 unique claims from each FEVER label."""

    # Each label gets its own dictionary.
    # The FEVER claim ID is used as the dictionary key
    # to prevent duplicate claims.
    records_by_label = {
        label: {}
        for label in TARGET_LABELS
    }

    for record in records:
        if not validate_record(record):
            continue

        label = record["label"]
        fever_id = record["id"]

        # Keep only one record for each unique claim ID.
        if fever_id not in records_by_label[label]:
            records_by_label[label][fever_id] = record

    random_generator = random.Random(RANDOM_SEED)
    selected_records = []

    for label in TARGET_LABELS:
        available_records = list(
            records_by_label[label].values()
        )

        if len(available_records) < CASES_PER_LABEL:
            raise ValueError(
                f"Not enough {label} records. "
                f"Needed {CASES_PER_LABEL}, "
                f"but found {len(available_records)}."
            )

        label_sample = random_generator.sample(
            available_records,
            CASES_PER_LABEL
        )

        for record in label_sample:
            selected_records.append(
                convert_record(record)
            )

    # Mix the labels instead of storing them in three groups.
    random_generator.shuffle(selected_records)

    return selected_records, records_by_label


def save_json(data, file_path):
    """Save formatted UTF-8 JSON without a byte-order mark."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with file_path.open(
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

        # Add a final newline.
        file.write("\n")


def main():
    """Create and save the balanced FEVER pilot."""

    if not SOURCE_PATH.exists():
        raise FileNotFoundError(
            "The official FEVER source file was not found:\n"
            f"{SOURCE_PATH}\n\n"
            "Download shared_task_dev.jsonl before running "
            "this script."
        )

    print("=" * 60)
    print("Preparing Official FEVER Pilot")
    print("=" * 60)

    source_records = load_jsonl(SOURCE_PATH)

    print("Source records:", len(source_records))

    source_distribution = Counter(
        record.get("label")
        for record in source_records
    )

    print(
        "Source label distribution:",
        dict(source_distribution)
    )

    selected_records, records_by_label = (
        create_balanced_sample(source_records)
    )

    sample_distribution = Counter(
        record["gold_label"]
        for record in selected_records
    )

    selected_ids = [
        record["fever_id"]
        for record in selected_records
    ]

    metadata = {
        "dataset": "FEVER v1.0",
        "source_file": "shared_task_dev.jsonl",
        "source_split": "shared_task_dev",
        "source_url": (
            "https://fever.ai/download/fever/"
            "shared_task_dev.jsonl"
        ),
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "sampling_method": (
            "e of unique FEVER claim IDs"
        ),
        "random_seed": RANDOM_SEED,
        "cases_per_label": CASES_PER_LABEL,
        "total_cases": len(selected_records),
        "target_labels": TARGET_LABELS,
        "source_record_count": len(source_records),
        "source_label_distribution": dict(
            source_distribution
        ),
        "source_unique_claims_by_label": {
            label: len(records_by_label[label])
            for label in TARGET_LABELS
        },
        "sample_label_distribution": dict(
            sample_distribution
        ),
        "selected_fever_ids": selected_ids,
        "notes": [
            (
                "This pilot contains authentic FEVER development "
                "claims selected for preliminary experiments."
            ),
            (
                "The separate fever_validation.json file contains "
                "synthetic software-validation fixtures."
            ),
            (
                "The full raw FEVER source file should not be "
                "committed to the Git repository."
            )
        ]
    }

    save_json(
        selected_records,
        OUTPUT_PATH
    )

    save_json(
        metadata,
        METADATA_PATH
    )

    print()
    print("=" * 60)
    print("Pilot Created Successfully")
    print("=" * 60)
    print("Total cases:", len(selected_records))
    print(
        "Label distribution:",
        dict(sample_distribution)
    )
    print(
        "Unique IDs:",
        len(set(selected_ids))
    )
    print("Pilot file:", OUTPUT_PATH)
    print("Metadata file:", METADATA_PATH)


if __name__ == "__main__":
    main()