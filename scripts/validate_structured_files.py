#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    ROOT / ".git",
    ROOT / "book" / "site",
    ROOT / "source",
}


def is_excluded(path: Path) -> bool:
    return any(excluded in path.parents for excluded in EXCLUDED_DIRS)


def validate_yaml(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def main() -> None:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or is_excluded(path):
            continue
        if path.suffix in {".yml", ".yaml"}:
            try:
                validate_yaml(path)
            except Exception as exc:  # pragma: no cover - diagnostics
                failures.append(f"YAML invalid: {path}: {exc}")
        if path.suffix in {".json", ".jsonld"}:
            try:
                validate_json(path)
            except Exception as exc:  # pragma: no cover - diagnostics
                failures.append(f"JSON invalid: {path}: {exc}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
