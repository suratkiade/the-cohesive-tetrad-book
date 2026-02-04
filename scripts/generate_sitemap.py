#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "book" / "site"
SITE_URL = "https://suratkiade.github.io/the-cohesive-tetrad-book/"


def build_sitemap() -> None:
    if not SITE_DIR.exists():
        raise SystemExit("Site directory does not exist. Run mkdocs build first.")

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = date.today().isoformat()

    for file_path in sorted(p for p in SITE_DIR.rglob("*") if p.is_file()):
        if file_path.name in {"sitemap.xml"}:
            continue
        if file_path.suffix not in {".html", ".txt"}:
            continue
        relative = file_path.relative_to(SITE_DIR)
        url = SITE_URL + str(relative).replace("index.html", "").replace("\\", "/")

        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = url
        lastmod_el = ET.SubElement(url_el, "lastmod")
        lastmod_el.text = today

    sitemap_path = SITE_DIR / "sitemap.xml"
    sitemap_path.write_text(
        ET.tostring(urlset, encoding="unicode"),
        encoding="utf-8",
    )


if __name__ == "__main__":
    build_sitemap()
