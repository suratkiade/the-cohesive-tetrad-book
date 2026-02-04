#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python "$ROOT_DIR/scripts/generate_portal_docs.py"
python "$ROOT_DIR/scripts/validate_structured_files.py"

mkdocs build --strict --config-file "$ROOT_DIR/book/mkdocs.yml" --site-dir "$ROOT_DIR/book/site"
python "$ROOT_DIR/scripts/generate_sitemap.py"

python "$ROOT_DIR/scripts/generate_portal_docs.py"
mkdocs build --strict --config-file "$ROOT_DIR/book/mkdocs.yml" --site-dir "$ROOT_DIR/book/site"
python "$ROOT_DIR/scripts/generate_sitemap.py"
python "$ROOT_DIR/scripts/generate_portal_docs.py"
mkdocs build --strict --config-file "$ROOT_DIR/book/mkdocs.yml" --site-dir "$ROOT_DIR/book/site"
python "$ROOT_DIR/scripts/check_portal_outputs.py"
