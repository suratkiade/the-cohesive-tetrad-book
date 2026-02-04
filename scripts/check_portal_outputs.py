#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
DOCS_DIR = BOOK_DIR / "docs"
SITE_DIR = BOOK_DIR / "site"

REQUIRED_DOCS = {
    "index.md",
    "manuscript.md",
    "cite.md",
    "provenance.md",
    "policy.md",
    "llms.txt",
}


def main() -> None:
    failures: list[str] = []

    for doc in REQUIRED_DOCS:
        path = DOCS_DIR / doc
        if not path.exists():
            failures.append(f"Missing required portal doc: {path}")

    provenance_path = DOCS_DIR / "provenance.md"
    if provenance_path.exists():
        provenance_text = provenance_path.read_text(encoding="utf-8")
        if "unknown" in provenance_text or "unavailable" in provenance_text:
            failures.append("Provenance contains unknown or unavailable values.")
        if "{{" in provenance_text or "}}" in provenance_text:
            failures.append("Provenance contains unresolved template markers.")

    manuscript_path = DOCS_DIR / "manuscript.md"
    if manuscript_path.exists():
        manuscript_text = manuscript_path.read_text(encoding="utf-8")
        if "{{" in manuscript_text or "}}" in manuscript_text:
            failures.append("Manuscript contains unresolved template markers.")

    if SITE_DIR.exists():
        llms_path = SITE_DIR / "llms.txt"
        if not llms_path.exists():
            failures.append("llms.txt not published at site root.")
        sitemap_path = SITE_DIR / "sitemap.xml"
        if not sitemap_path.exists():
            failures.append("sitemap.xml not published at site root.")
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
