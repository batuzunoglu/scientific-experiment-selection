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
from typing import Mapping

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
ENTRY_HEADER = re.compile(r"(?m)^## Entry \d{3} — \d{4}-\d{2}-\d{2}\b")


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


def git(*args: str, cwd: Path | str | None = None) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    )


def is_ancestor(ancestor: str, descendant: str, cwd: Path | str | None = None) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def resolve_base_commit(
    cwd: Path | str | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    """Resolve the immutable pre-merge base commit for comparing HEAD.

    Uses a single consistent commit SHA for both changed-file detection and
    baseline notebook retrieval, eliminating the race when a `ready_for_review`
    workflow run overlaps a squash or normal merge of the same PR:
    1. If `GITHUB_BASE_SHA` is provided (e.g. `github.event.pull_request.base.sha`),
       verify it resolves to a valid commit object and use it as the target base ref;
       otherwise resolve `origin/<GITHUB_BASE_REF or main>`.
    2. Inspect `HEAD` parents (`git rev-list --parents -n 1 HEAD`). When `HEAD` is a
       two-parent PR synthetic merge commit `(P1, P2)` (`refs/pull/<N>/merge`) where
       `P1` (`HEAD^1`) is on the base branch history (`is_ancestor(P1, target_ref)`)
       and `P2` (`HEAD^2`) is the PR head (`not is_ancestor(P2, P1)`), `P1` is the
       exact pre-merge base commit merged into `HEAD`. Using `P1` avoids the
       `git merge-base origin/main HEAD` ambiguity after a normal merge commit (where
       both `P1` and `P2` are ancestors of post-merge `origin/main` and `merge-base`
       would return the feature tip `P2`).
    3. For single-parent branch checkouts (or feature branches that merged base into
       themselves), compute `git merge-base <target_ref> HEAD`.
    4. Fail closed if the resolved base commit equals `HEAD` so an already-merged ref
       without a distinct pre-merge base never produces an empty diff.
    """
    environ = os.environ if env is None else env
    base_sha = (environ.get("GITHUB_BASE_SHA") or "").strip()
    if base_sha:
        target_ref = git("rev-parse", "--verify", f"{base_sha}^{{commit}}", cwd=cwd).strip()
    else:
        base_name = (environ.get("GITHUB_BASE_REF") or "main").strip() or "main"
        base_ref = f"origin/{base_name}"
        target_ref = git("rev-parse", "--verify", f"{base_ref}^{{commit}}", cwd=cwd).strip()

    rev_tokens = git("rev-list", "--parents", "-n", "1", "HEAD", cwd=cwd).strip().split()
    if not rev_tokens:
        raise ValueError("Could not resolve HEAD commit.")
    head_sha = rev_tokens[0]
    parents = rev_tokens[1:]

    if (
        len(parents) == 2
        and is_ancestor(parents[0], target_ref, cwd=cwd)
        and not is_ancestor(parents[1], parents[0], cwd=cwd)
    ):
        base_commit = parents[0]
    else:
        base_commit = git("merge-base", target_ref, head_sha, cwd=cwd).strip()

    if not base_commit:
        raise ValueError("Could not resolve merge-base commit.")
    if base_commit == head_sha:
        raise ValueError(
            "Baseline commit resolves to HEAD; cannot evaluate PR diff without a distinct pre-merge base."
        )
    return base_commit


def check_repo(
    cwd: Path | str | None = None,
    env: Mapping[str, str] | None = None,
) -> tuple[int, str]:
    """Check that research changes between the resolved base commit and HEAD append a dated entry."""
    repo_root = Path(cwd) if cwd is not None else Path(".")
    try:
        base_commit = resolve_base_commit(cwd=repo_root, env=env)
        paths = [
            p for p in git(
                "diff", "--name-only", "--diff-filter=ACMR", base_commit, "HEAD",
                cwd=repo_root,
            ).splitlines() if p
        ]
        if not needs_notebook(paths) and NOTEBOOK not in paths:
            return 0, "Notebook gate: no research-code or decision changes."
        if NOTEBOOK not in paths:
            return 1, f"ERROR: Research changes require an appended {NOTEBOOK} entry."
        old = git("show", f"{base_commit}:{NOTEBOOK}", cwd=repo_root)
        new = (repo_root / NOTEBOOK).read_text(encoding="utf-8")
        valid, message = valid_append(old, new)
        if not valid:
            return 1, "ERROR: " + message
    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
        return 2, f"ERROR: Notebook gate could not run: {exc}"
    return 0, "Notebook gate: dated append-only research entry found."


def main() -> int:
    code, message = check_repo()
    stream = sys.stderr if code != 0 else sys.stdout
    print(message, file=stream)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
