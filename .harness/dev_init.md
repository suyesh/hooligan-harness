# Development Init

## Local workflow

1. Sync Python dependencies:
   `uv sync --python python3`
2. Run the installer interactively:
   `uv run python install.py`
3. Run maintenance commands directly:
   `uv run python install.py update`
   `uv run python install.py doctor`
4. Run the test suite:
   `uv run python -m unittest discover -s tests`

## Notes

- `update` expects this repository checkout to be the canonical source and refreshes it from `origin/main`.
- `doctor` repairs installed files, deduplicates Claude registry entries, and removes duplicate install directories.
