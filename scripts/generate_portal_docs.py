#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
TEMPLATE_DIR = BOOK_DIR / "templates"
DOCS_DIR = BOOK_DIR / "docs"
SOURCE_DIR = ROOT / "source"
SITE_DIR = BOOK_DIR / "site"


def run_git(args: list[str], cwd: Path) -> str:
    return subprocess.check_output(["git", "-C", str(cwd), *args], text=True).strip()


def get_submodule_commit() -> str:
    try:
        return run_git(["rev-parse", "HEAD"], SOURCE_DIR)
    except Exception:
        try:
            tree_line = run_git(["ls-tree", "HEAD", "source"], ROOT)
            return tree_line.split()[2]
        except Exception:
            return "unknown"


def get_submodule_tag() -> str:
    try:
        return run_git(["describe", "--tags", "--abbrev=0"], SOURCE_DIR)
    except Exception:
        return ""


def get_submodule_short_commit() -> str:
    try:
        return run_git(["rev-parse", "--short", "HEAD"], SOURCE_DIR)
    except Exception:
        return ""


def get_submodule_commit_date() -> str:
    try:
        return run_git(["show", "-s", "--format=%cs", "HEAD"], SOURCE_DIR)
    except Exception:
        return "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_directory(path: Path, exclude_paths: set[Path]) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        relative = file_path.relative_to(path)
        if any(relative == ex or relative.is_relative_to(ex) for ex in exclude_paths):
            continue
        digest.update(str(relative).encode("utf-8"))
        digest.update(b"\0")
        with file_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(8192), b""):
                digest.update(chunk)
    return digest.hexdigest()


def render_template(template_path: Path, output_path: Path, replacements: dict[str, str]) -> None:
    text = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(f"{{{{ {key} }}}}", value)
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    canonical_commit = get_submodule_commit()
    canonical_tag = get_submodule_tag()
    if not canonical_tag:
        canonical_tag = get_submodule_short_commit() or "unknown"
    canonical_commit_date = get_submodule_commit_date()

    pdf_path = SOURCE_DIR / "manuscript" / "TCT_v1.0_canonical.pdf"
    if pdf_path.exists():
        pdf_sha256 = sha256_file(pdf_path)
    else:
        pdf_sha256 = "unavailable"

    html_bundle_sha256 = "unavailable"
    if SITE_DIR.exists():
        html_bundle_sha256 = sha256_directory(
            SITE_DIR,
            exclude_paths={Path("provenance")},
        )

    if canonical_tag == "unknown":
        canonical_tag_link = "unavailable"
    elif canonical_tag == get_submodule_short_commit():
        canonical_tag_link = (
            "[commit](https://github.com/suratkiade/the-cohesive-tetrad/commit/"
            f"{canonical_commit})"
        )
    else:
        canonical_tag_link = (
            "[release](https://github.com/suratkiade/the-cohesive-tetrad/releases/tag/"
            f"{canonical_tag})"
        )

    replacements = {
        "canonical_tag": canonical_tag,
        "canonical_commit": canonical_commit,
        "canonical_commit_date": canonical_commit_date,
        "build_date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pdf_sha256": pdf_sha256,
        "html_bundle_sha256": html_bundle_sha256,
        "canonical_tag_link": canonical_tag_link,
    }

    render_template(
        TEMPLATE_DIR / "manuscript.md.tmpl",
        DOCS_DIR / "manuscript.md",
        replacements,
    )
    render_template(
        TEMPLATE_DIR / "provenance.md.tmpl",
        DOCS_DIR / "provenance.md",
        replacements,
    )


if __name__ == "__main__":
    main()
