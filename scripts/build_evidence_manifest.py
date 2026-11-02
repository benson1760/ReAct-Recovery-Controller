"""Build an evidence-reference manifest for the 30-case FEVER pilot."""

import json
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PILOT_PATH = (
    REPO_ROOT
    / "data"
    / "samples"
    / "fever_pilot_30.json"
)

MANIFEST_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_evidence_manifest.json"
)

COVERAGE_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_evidence_coverage.json"
)


def load_json(file_path):
    """Load a JSON file."""

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, file_path):
    """Save formatted UTF-8 JSON."""

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

        file.write("\n")


def extract_evidence_references(record):
    """
    Extract usable Wikipedia page and sentence references
    from one FEVER record.
    """

    references = []

    for evidence_group in record.get("evidence", []):
        if not evidence_group:
            continue

        for evidence_item in evidence_group:
            if len(evidence_item) < 4:
                continue

            annotation_id = evidence_item[0]
            evidence_id = evidence_item[1]
            wiki_page = evidence_item[2]
            sentence_id = evidence_item[3]

            if wiki_page is None or sentence_id is None:
                continue

            references.append(
                {
                    "annotation_id": annotation_id,
                    "evidence_id": evidence_id,
                    "wiki_page": wiki_page,
                    "sentence_id": sentence_id
                }
            )

    return references


def build_manifest(records):
    """Build a deduplicated evidence-reference manifest."""

    reference_map = {}
    claims_by_page = defaultdict(set)

    cases_with_references = 0
    cases_without_references = 0

    coverage_by_label = {
        "SUPPORTS": {
            "total": 0,
            "with_reference": 0,
            "without_reference": 0
        },
        "REFUTES": {
            "total": 0,
            "with_reference": 0,
            "without_reference": 0
        },
        "NOT ENOUGH INFO": {
            "total": 0,
            "with_reference": 0,
            "without_reference": 0
        }
    }

    for record in records:
        fever_id = record["fever_id"]
        label = record["gold_label"]
        claim = record["claim"]

        coverage_by_label[label]["total"] += 1

        references = extract_evidence_references(record)

        if references:
            cases_with_references += 1
            coverage_by_label[label]["with_reference"] += 1
        else:
            cases_without_references += 1
            coverage_by_label[label]["without_reference"] += 1

        for reference in references:
            wiki_page = reference["wiki_page"]
            sentence_id = reference["sentence_id"]

            # Page and sentence together identify one evidence sentence.
            reference_key = f"{wiki_page}::{sentence_id}"

            if reference_key not in reference_map:
                reference_map[reference_key] = {
                    "reference_key": reference_key,
                    "wiki_page": wiki_page,
                    "sentence_id": sentence_id,
                    "fever_cases": [],
                    "resolved": False,
                    "evidence_text": None
                }

            case_entry = {
                "fever_id": fever_id,
                "claim": claim,
                "gold_label": label,
                "annotation_id": reference["annotation_id"],
                "evidence_id": reference["evidence_id"]
            }

            existing_case_ids = {
                case["fever_id"]
                for case in reference_map[
                    reference_key
                ]["fever_cases"]
            }

            if fever_id not in existing_case_ids:
                reference_map[
                    reference_key
                ]["fever_cases"].append(case_entry)

            claims_by_page[wiki_page].add(fever_id)

    manifest = sorted(
        reference_map.values(),
        key=lambda item: (
            item["wiki_page"],
            item["sentence_id"]
        )
    )

    unique_pages = sorted(
        {
            item["wiki_page"]
            for item in manifest
        }
    )

    page_summary = []

    for page in unique_pages:
        sentence_ids = sorted(
            {
                item["sentence_id"]
                for item in manifest
                if item["wiki_page"] == page
            }
        )

        page_summary.append(
            {
                "wiki_page": page,
                "required_sentence_ids": sentence_ids,
                "fever_case_ids": sorted(
                    claims_by_page[page]
                )
            }
        )

    coverage = {
        "total_pilot_cases": len(records),
        "cases_with_evidence_references": (
            cases_with_references
        ),
        "cases_without_evidence_references": (
            cases_without_references
        ),
        "unique_evidence_references": len(manifest),
        "unique_wikipedia_pages": len(unique_pages),
        "coverage_by_label": coverage_by_label,
        "pilot_label_distribution": dict(
            Counter(
                record["gold_label"]
                for record in records
            )
        ),
        "notes": [
            (
                "SUPPORTS and REFUTES cases are expected to "
                "contain evidence references."
            ),
            (
                "NOT ENOUGH INFO cases normally do not contain "
                "gold evidence references."
            ),
            (
                "The manifest records required evidence only; "
                "actual evidence text has not yet been resolved."
            )
        ]
    }

    output = {
        "source_file": "data/samples/fever_pilot_30.json",
        "manifest_type": "FEVER evidence-reference manifest",
        "unique_pages": unique_pages,
        "page_summary": page_summary,
        "evidence_references": manifest
    }

    return output, coverage


def main():
    """Build and save the evidence manifest."""

    if not PILOT_PATH.exists():
        raise FileNotFoundError(
            "The FEVER pilot file was not found:\n"
            f"{PILOT_PATH}"
        )

    records = load_json(PILOT_PATH)

    manifest, coverage = build_manifest(records)

    save_json(
        manifest,
        MANIFEST_PATH
    )

    save_json(
        coverage,
        COVERAGE_PATH
    )

    print("=" * 60)
    print("FEVER Evidence Manifest Created")
    print("=" * 60)
    print(
        "Pilot cases:",
        coverage["total_pilot_cases"]
    )
    print(
        "Cases with references:",
        coverage["cases_with_evidence_references"]
    )
    print(
        "Cases without references:",
        coverage["cases_without_evidence_references"]
    )
    print(
        "Unique evidence references:",
        coverage["unique_evidence_references"]
    )
    print(
        "Unique Wikipedia pages:",
        coverage["unique_wikipedia_pages"]
    )
    print("Manifest:", MANIFEST_PATH)
    print("Coverage summary:", COVERAGE_PATH)


if __name__ == "__main__":
    main()