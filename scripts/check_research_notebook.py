"""Check that research-changing pull requests append a dated lab-notebook entry.

Run in a checked-out Git repository with full history:
    python3 scripts/check_research_notebook.py

This is a PR quality gate, not an automatic scientific audit. Direct pushes to
unprotected branches can bypass it; branch protection/rulesets must require the
check for hard enforcement.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

NOTEBOOK = "docs/RESEARCH_LAB_NOTEBOOK.md"
RESEARCH_PATH_PREFIXES = (
    "scientific_experiment_selection/",
    "experiments/",
    "notebooks/",
    "configs/",
    "data/",
    "tests/",
    "scripts/",
    "tools/",
)
RESEARCH_FILES = {
    "pyproject.toml",
    "uv.lock",
    "docs/PROJECT_CHARTER.md",
    "docs/DECISIONS.md",
    "docs/EXPERIMENT_TEMPLATE.md",
    "docs/LEARNING_LOG.md",
}
ENTRY_HEADER = re.compile(r"(?m)^## Entry \\d{3} — \\d{4}-\\d{2}-\\d{2}\\b")


def needs_notebook(changed_paths: list[str]) -> bool:
    return any(
        path in RESEARCH_FILES
        or path.startswith(RESEARCH_PATH_PREFIXES)
        for path in changed_paths
    )


def valid_append(old: str, new: str) -> tuple[bool, str]:
    if not new.startswith(old):
        return False, "Existing notebook entries were edited or deleted."
    added = new[len(old):]
    if not added.strip():
        return False, "No new notebook content was appended."
    if not ENTRY_HEADER.search(added):
        return False, "Append a dated '## Entry NNN — YYYY-MM-DD' section."
    return True, ""


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, encoding="utf-8")


def main() -> int:
    base = os.environ.get("GITHUB_BASE_REF") or "main"
    base_ref = "origin/" + base
    try:
        paths = [
            p for p in git("diff", "--name-only", "--diff-filter=ACMR",
                           f"{base_ref}...HEAD").splitlines() if p
        ]
        if not needs_notebook(paths) and NOTEBOOK not in paths:
            print("Notebook gate: no research-code or decision changes.")
            return 0
        if NOTEBOOK not in paths:
            print(f"ERROR: Research changes require an appended {NOTEBOOK} entry.",
                  file=sys.stderr)
            return 1
        old = git("show", f"{base_ref}:{NOTEBOOK}")
        new = Path(NOTEBOOK).read_text(encoding="utf-8")
        valid, message = valid_append(old, new)
        if not valid:
            print("ERROR: " + message, file=sys.stderr)
            return 1
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"ERROR: Notebook gate could not run: {exc}", file=sys.stderr)
        return 2
    print("Notebook gate: dated append-only research entry found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
