"""
Resolve FEVER evidence references into actual evidence text.
Inital version: inventory and reporting framework.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_evidence_manifest.json"
)

OUTPUT_REPORT = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_evidence_resolution_report.json"
)

def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def main():

    manifest = load_json(MANIFEST_PATH)

    unique_pages = manifest["unique_pages"]
    references = manifest["evidence_references"]

    report = {
        "total_pages_needed": len(unique_pages),
        "total_references": len(references),
        "pages_available": 0,
        "pages_missing": len(unique_pages),
        "references_resolved": 0,
        "references_unresolved": len(references),
        "required_pages": unique_pages,
        "notes": [
            "Initial inventory stage.",
            "Wikipedia evidence source has not yet been acquired."
        ]
    }

    save_json(
        report,
        OUTPUT_REPORT
    )

    print("=" * 60)
    print("FEVER Evidence Resolution Inventory")
    print("=" * 60)
    print("Pages needed:", len(unique_pages))
    print("Evidence references:", len(references))
    print("Report saved:", OUTPUT_REPORT)


if __name__ == "__main__":
    main()