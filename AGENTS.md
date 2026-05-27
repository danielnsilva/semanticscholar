# AGENTS.md

Unofficial Python client library for Semantic Scholar APIs
(async-first, typed, paginated).

## Build and Test

```bash
pip install -r requirements.txt \
  && pip install -r test-requirements.txt \
  && pip install -e .
python -m unittest
```

Tests use vcrpy cassettes (recorded HTTP fixtures). No live API calls needed.

## Definition of Done

A task is complete when:

1. `python -m unittest` exits 0
2. New/changed API methods have corresponding VCR cassettes in `tests/data/`
3. Commit message follows conventional format: `type(scope): description`

## Escalation Rules

- If tests fail after 2 attempts: stop and report the failure with full output
- If a VCR cassette is missing: stop and ask (do not make live API requests)
- Never: delete test cassettes, skip tests, or modify recorded fixtures

## When Writing Code

- Properties use **camelCase** matching API JSON keys
  (`paperId`, `citationCount`), not snake_case
- Each model declares `FIELDS` / `SEARCH_FIELDS` constants for valid API fields
- Async client (`AsyncSemanticScholar`) is the primary implementation;
  sync client wraps it

## When Releasing

- Update version in `setup.py` and move `[Unreleased]` entries in `CHANGELOG.md`
- Tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
- Push tag triggers CI publish to PyPI

## References

- [README.md](README.md) — Usage for end users
- [CHANGELOG.md](CHANGELOG.md) — Version history
- [CONTRIBUTING.md](.github/CONTRIBUTING.md) — Contribution guidelines
- [docs/](docs/) — Sphinx documentation (RST)
