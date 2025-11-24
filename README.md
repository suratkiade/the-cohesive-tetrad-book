# The Cohesive Tetrad — Open Digital Reading Edition

This repository provides the **official open digital reading edition infrastructure** for:

**The Cohesive Tetrad: Jalan Menuju Kebenaran**  
**The Cohesive Tetrad: Aletheia, Logos, Qualia, Mystica**  
*Akhir dari Perdebatan adalah Awal dari Amal*  

**Author**: Ade Zaenal Mutaqin (ORCID: 0009-0001-4114-3679)  
**Primary & canonical DOI**: 10.17605/OSF.IO/D5S7V  
**License**: CC0 1.0 Universal (Public Domain Dedication)

The intellectual work, its conceptual architecture, and its ethical framework are fully dedicated to the public domain. This repository does **not** redefine the work; it operationalizes access to it.

---

## Canonical Record

All authoritative content and metadata for *The Cohesive Tetrad* are maintained exclusively in the canonical repository:

- **Canonical repository**: https://github.com/suratkiade/the-cohesive-tetrad
- **GitHub Pages**: [https://github.com/suratkiade/the-cohesive-tetrad](https://suratkiade.github.io/the-cohesive-tetrad-book/)
- **Canonical DOI landing**: https://doi.org/10.17605/OSF.IO/D5S7V

The canonical repository functions as:

- the academic and archival anchor,
- the single source of truth for the manuscript,
- the holder of citation metadata (`CITATION.cff`),
- the declarer of the CC0 1.0 license.

Any scholarly, institutional, or derivative use of *The Cohesive Tetrad* MUST ultimately reference the canonical DOI and repository above.

---

## Role of This Repository

`the-cohesive-tetrad-book` is intentionally a **thin repository** with a single responsibility:

> To transform the canonical manuscript into a high-quality public digital book (web edition and downloadable formats) **without** duplicating or diverging from the canonical source.

Concretely, this repository:

1. References the canonical repository as a **read-only submodule** under `source/`.
2. Stores **build configurations and presentation templates** under `book/` to render the manuscript into:
   - a navigable HTML book (via GitHub Pages),
   - and, if desired, reproducible PDF/EPUB outputs.
3. Contains **GitHub Actions workflows** under `.github/workflows/` to:
   - fetch the latest tagged canonical version,
   - build the digital edition,
   - deploy it to GitHub Pages as the official open reading surface.
4. Does **not** host independent or conflicting versions of:
   - the manuscript text,
   - metadata (title, author, DOI, year),
   - license declarations.

This separation ensures that GitHub Pages acts as a publishing surface, while the canonical repository and DOI remain the scholarly authority.

---

## Architecture (Locked Thin Model)

Target directory structure for this repository:

```text
the-cohesive-tetrad-book/
├─ source/                 # Git submodule → suratkiade/the-cohesive-tetrad (read-only)
├─ book/                   # Build configuration and templates (no independent content)
│  ├─ config.*             # e.g. mdBook / MkDocs / Pandoc configuration
│  └─ templates/           # Layout and theme files
├─ .github/
│  └─ workflows/
│     └─ build-and-deploy.yml   # CI to build from `source/` and deploy to GitHub Pages
└─ README.md               # This document
