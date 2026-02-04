# Book build configuration

This folder contains the MkDocs configuration, templates, and portal pages used to publish the reading edition portal. It does not contain canonical manuscript content.

## Key paths

- `mkdocs.yml` for site configuration
- `docs/` for portal pages and static assets
- `overrides/` for theme overrides
- `templates/` for generated portal documents

## Canonical sources

The manuscript lives in the `source/` submodule and remains the single source of truth. This portal only builds a reading edition from those canonical sources.
