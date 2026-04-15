# Repository instructions

## Scope

- Keep the project as a small, dependency-light Python CLI and library.
- Preserve the public CLI name `jpg2xlsx` and the `src/` package layout.
- Prefer focused changes over large refactors.

## Tooling

- Use `uv sync --all-groups` to install dependencies.
- Run `uv run ruff check .`, `uv run ruff format .`, and `uv run pytest` before finishing substantial changes.
- Keep development dependencies in `[dependency-groups].dev` inside `pyproject.toml`.

## Code guidelines

- Maintain compatibility with Python 3.10+.
- Avoid adding heavy CLI frameworks unless there is a clear need.
- Add tests for behavior changes, especially around output path handling and workbook generation.

## Packaging and release

- Keep package metadata in `pyproject.toml`.
- Prefer updating GitHub Actions with `uv`-based commands.
- Do not add docs-site tooling unless the repo actually ships documentation pages.
