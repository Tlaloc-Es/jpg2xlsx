# Contributing

Thanks for contributing to jpg2xlsx.

## Development setup

1. Install `uv`.
2. Clone the repository.
3. Run `uv sync --all-groups`.

## Local checks

Run the full local validation suite before opening a pull request:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Pull requests

1. Create a focused branch.
2. Add or update tests when behavior changes.
3. Use conventional commit messages when possible. The release workflows rely on them.
4. Update `README.md` or `CHANGELOG.md` when user-facing behavior changes.

## Pre-commit

To enable the local git hooks:

```bash
uv run pre-commit install
```
