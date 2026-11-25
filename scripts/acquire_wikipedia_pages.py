"""
Download only the Wikipedia pages needed by the FEVER pilot.
"""

import json
import requests
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PAGES_FILE = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "required_wikipedia_pages.txt"
)

OUTPUT_DIR = (
    REPO_ROOT
    / "data"
    / "raw"
    / "fever"
    / "wiki-pages"
)

REPORT_FILE = (
    REPO_ROOT
    / "data"
    / "processed"
    / "fever"
    / "wikipedia_page_acquisition_report.json"
)


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_pages():
    with open(PAGES_FILE, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pages = load_pages()

    downloaded = []
    failed = []

    for page in pages:
        wiki_title = (
    page
    .replace("-LRB-", "(")
    .replace("-RRB-", ")")
)

        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + wiki_title
        )

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=15
            )

            if response.status_code == 200:

                data = response.json()

                output_path = (
                    OUTPUT_DIR / f"{page}.json"
                )

                with open(
                    output_path,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        data,
                        file,
                        indent=2,
                        ensure_ascii=False
                    )

                downloaded.append(page)

                print("Downloaded:", page)

            else:

                failed.append(
                    {
                        "page": page,
                        "status_code": response.status_code
                    }
                )

                print(
                    "Failed:",
                    page,
                    response.status_code
                )

        except Exception as error:

            failed.append(
                {
                    "page": page,
                    "error": str(error)
                }
            )

            print("Error:", page)

    report = {
        "pages_requested": len(pages),
        "pages_downloaded": len(downloaded),
        "pages_failed": len(failed),
        "downloaded_pages": downloaded,
        "failed_pages": failed
    }

    save_json(report, REPORT_FILE)

    print()
    print("=" * 60)
    print("Wikipedia Download Complete")
    print("=" * 60)
    print("Requested:", len(pages))
    print("Downloaded:", len(downloaded))
    print("Failed:", len(failed))


if __name__ == "__main__":
    main()