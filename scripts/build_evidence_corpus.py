"""
Build a local evidence corpus from downloaded Wikipedia pages.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

WIKI_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
    / "fever"
    / "wiki-pages"
)

OUTPUT_FILE = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_pilot_evidence.json"
)

REPORT_FILE = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "fever_evidence_resolution_report.json"
)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_page(page_file):

    with open(
        page_file,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    corpus = []
    downloaded_pages = []

    for page_file in WIKI_DIR.glob("*.json"):

        page = load_page(page_file)

        corpus.append(
            {
                "page_title": page.get("title"),
                "page_id": page.get("pageid"),
                "url": page.get("content_urls", {})
                           .get("desktop", {})
                           .get("page"),
                "summary": page.get("extract", "")
            }
        )

        downloaded_pages.append(
            page.get("title")
        )

    report = {
        "pages_loaded": len(corpus),
        "pages_available": downloaded_pages,
        "notes": [
            "Corpus built from Wikipedia summaries.",
            "Not yet aligned to sentence-level FEVER evidence."
        ]
    }

    save_json(corpus, OUTPUT_FILE)
    save_json(report, REPORT_FILE)

    print("=" * 60)
    print("Evidence Corpus Created")
    print("=" * 60)
    print("Pages:", len(corpus))
    print("Corpus:", OUTPUT_FILE)
    print("Report:", REPORT_FILE)


if __name__ == "__main__":
    main()