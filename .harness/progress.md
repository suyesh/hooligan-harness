# Progress Log

## 2026-05-13

- Initialized harness maintenance feature work for installer `update` and `doctor` commands.
- Reviewed `README.md`, installer flow, failure patterns, evolution patterns, and rollback strategy.
- Refactored `install.py` into an explicit command-based CLI with install, uninstall, update, and doctor actions.
- Added updater safety gates for dirty worktrees and non-`main` branches unless forced.
- Added doctor checks for duplicate install directories, missing installation files, orphaned Claude persona files, and duplicate Claude registry entries.
- Narrowed doctor auto-removal to backup/copy-style duplicate directory names to avoid deleting intentional sibling checkouts.
- Added `unittest` coverage for doctor repair behavior and updater guardrails.
- Extended installed skill payloads to include `install.py`, `INSTALL.md`, and `personas/` so Claude/Codex skill invocations can run maintenance commands from the installed skill location.
- Added an install manifest so skill-local `update` can delegate back to the canonical repository checkout.
- Updated skill instructions and docs so `/harness update`, `/harness doctor`, and equivalent Codex requests are treated as maintenance intents instead of feature work.
- Removed maintenance command exposure from `setup.sh` and `setup.bat`; setup now only launches installation.
- Added `questionary`-backed select menus in the Python installer for install target and installed-state actions, with typed fallback only if the dependency is unavailable.
- Removed `update` and `doctor` from the already-installed installer action menu so maintenance stays skill-only.
- Replaced the final install `y/n` confirmation with the same styled selector flow used for other installer choices.
- Verified with `./.venv/bin/python -m unittest discover -s tests`, `./.venv/bin/python install.py --help`, and `python3 -m py_compile install.py tests/test_install.py`.
