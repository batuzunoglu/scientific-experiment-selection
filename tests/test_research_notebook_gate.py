"""Synthetic checks for the PR notebook quality gate; no raw lab files needed."""
from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.check_research_notebook import (
    NOTEBOOK,
    check_repo,
    needs_notebook,
    resolve_base_commit,
    valid_append,
)

INITIAL_NOTEBOOK = "# Research Lab Notebook\n\n## Entry 001 — 2026-11-08\nEarlier.\n"
VALID_APPEND_ENTRY = "\n## Entry 002 — 2026-11-08 | Synthetic CI gate test\nQuestion, decision and evidence.\n"


def _git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def _write(repo: Path, rel_path: str, content: str) -> None:
    target = repo / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def _init_synthetic_repo(repo: Path) -> str:
    """Create a synthetic Git repo with a baseline commit on main and origin/main."""
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Synthetic Test")
    _git(repo, "config", "user.email", "synthetic@example.com")
    _git(repo, "config", "commit.gpgsign", "false")
    _write(repo, "README.md", "# Synthetic Repo\n")
    _write(repo, NOTEBOOK, INITIAL_NOTEBOOK)
    _git(repo, "add", "README.md", NOTEBOOK)
    _git(repo, "commit", "-m", "Initial baseline")
    base_sha = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", "refs/remotes/origin/main", base_sha)
    return base_sha


def _create_pr_merge_ref(repo: Path, base_sha: str, feature_sha: str, pr_num: int = 1) -> str:
    """Create a synthetic GitHub refs/pull/<N>/merge commit with parents (base_sha, feature_sha)."""
    _git(repo, "checkout", "--detach", base_sha)
    _git(repo, "merge", "--no-ff", "-m", f"Merge {feature_sha} into {base_sha}", feature_sha)
    merge_sha = _git(repo, "rev-parse", "HEAD")
    _git(repo, "update-ref", f"refs/pull/{pr_num}/merge", merge_sha)
    return merge_sha


class NotebookGateTests(unittest.TestCase):
    def test_code_and_methodology_changes_require_entry(self):
        self.assertTrue(needs_notebook(["scientific_experiment_selection/model.py"]))
        self.assertTrue(needs_notebook(["docs/DECISIONS.md"]))
        self.assertTrue(needs_notebook(["tests/test_features.py"]))
        self.assertTrue(needs_notebook(["experiments/exp1.py"]))

    def test_plain_readme_change_does_not_require_entry(self):
        self.assertFalse(needs_notebook(["README.md"]))

    def test_valid_dated_append(self):
        old = INITIAL_NOTEBOOK
        new = old + VALID_APPEND_ENTRY
        self.assertEqual(valid_append(old, new), (True, ""))

    def test_editing_history_is_rejected(self):
        old = "# Research Lab Notebook\n\n## Entry 001 — 2026-11-08\nObserved.\n"
        new = old.replace("Observed.", "Edited.") + "\n## Entry 002 — 2026-11-08\nNext.\n"
        ok, _ = valid_append(old, new)
        self.assertFalse(ok)

    def test_undated_append_is_rejected(self):
        old = "# Research Lab Notebook\n"
        ok, _ = valid_append(old, old + "\nThis was a useful step.\n")
        self.assertFalse(ok)

    def test_git_unmerged_pr_with_genuine_dated_append_passes(self):
        """Scenario 1: Genuine appended, dated entry in an unmerged PR passes."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/test", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 1\n")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + VALID_APPEND_ENTRY)
            _git(repo, "add", "scientific_experiment_selection/module.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Add research module and notebook entry")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            # Direct feature-branch checkout passes
            self.assertEqual(resolve_base_commit(cwd=repo, env={}), base_sha)
            code, msg = check_repo(cwd=repo, env={})
            self.assertEqual(code, 0, msg)

            # GitHub Actions refs/pull/1/merge synthetic merge checkout passes
            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)
            self.assertEqual(resolve_base_commit(cwd=repo, env={}), base_sha)
            code, msg = check_repo(cwd=repo, env={})
            self.assertEqual(code, 0, msg)

    def test_git_pr_merge_ref_passes_after_base_advances_from_squash_merge(self):
        """Scenario 2: Same PR's refs/pull/N/merge checkout passes after base advances from squash merge."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/squash-race", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 1\n")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + VALID_APPEND_ENTRY)
            _git(repo, "add", "scientific_experiment_selection/module.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Add module and Entry 002")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            # Construct PR synthetic merge commit before main moves
            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)

            # Simulate squash merge on main advancing origin/main to include Entry 002
            _git(repo, "checkout", "main")
            _git(repo, "merge", "--squash", feature_sha)
            _git(repo, "commit", "-m", "Squash merge PR #1")
            squash_main_sha = _git(repo, "rev-parse", "HEAD")
            _git(repo, "update-ref", "refs/remotes/origin/main", squash_main_sha)

            # Check out the PR synthetic merge ref (as ready_for_review CI does)
            _git(repo, "checkout", "--detach", pr_merge_sha)

            # Passes both without GITHUB_BASE_SHA and with GITHUB_BASE_SHA
            for env in ({}, {"GITHUB_BASE_SHA": base_sha}):
                self.assertEqual(resolve_base_commit(cwd=repo, env=env), base_sha)
                code, msg = check_repo(cwd=repo, env=env)
                self.assertEqual(code, 0, msg)

    def test_git_pr_merge_ref_passes_after_base_advances_from_normal_merge_commit(self):
        """Scenario 3: Same PR's refs/pull/N/merge checkout passes after base advances from normal merge commit."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/normal-merge-race", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 1\n")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + VALID_APPEND_ENTRY)
            _git(repo, "add", "scientific_experiment_selection/module.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Add module and Entry 002")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            # Construct PR synthetic merge commit before main moves
            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)

            # Simulate normal (--no-ff) merge commit on main advancing origin/main
            _git(repo, "checkout", "main")
            _git(repo, "merge", "--no-ff", "-m", "Merge pull request #1", feature_sha)
            normal_main_sha = _git(repo, "rev-parse", "HEAD")
            _git(repo, "update-ref", "refs/remotes/origin/main", normal_main_sha)

            # Note: naive `git merge-base origin/main pr_merge_sha` would return feature_sha here!
            naive_mb = _git(repo, "merge-base", "origin/main", pr_merge_sha)
            self.assertEqual(naive_mb, feature_sha)

            # Check out the PR synthetic merge ref
            _git(repo, "checkout", "--detach", pr_merge_sha)

            # Both without and with GITHUB_BASE_SHA, resolve_base_commit resolves to base_sha (not feature_sha)
            for env in ({}, {"GITHUB_BASE_SHA": base_sha}):
                self.assertEqual(resolve_base_commit(cwd=repo, env=env), base_sha)
                code, msg = check_repo(cwd=repo, env=env)
                self.assertEqual(code, 0, msg)

    def test_git_research_change_without_notebook_entry_fails(self):
        """Scenario 4: Research change without a new notebook entry fails."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/missing-entry", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 2\n")
            _git(repo, "add", "scientific_experiment_selection/module.py")
            _git(repo, "commit", "-m", "Research change without notebook entry")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            code, msg = check_repo(cwd=repo, env={})
            self.assertEqual(code, 1)
            self.assertIn("require an appended", msg)

            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)
            code, msg = check_repo(cwd=repo, env={"GITHUB_BASE_SHA": base_sha})
            self.assertEqual(code, 1)
            self.assertIn("require an appended", msg)

    def test_git_existing_notebook_content_modified_or_deleted_fails(self):
        """Scenario 5: Existing notebook content modified/deleted fails."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/rewrite-history", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 3\n")
            rewritten = INITIAL_NOTEBOOK.replace("Earlier.", "Rewritten.") + VALID_APPEND_ENTRY
            _write(repo, NOTEBOOK, rewritten)
            _git(repo, "add", "scientific_experiment_selection/module.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Rewrite earlier entry")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)
            code, msg = check_repo(cwd=repo, env={"GITHUB_BASE_SHA": base_sha})
            self.assertEqual(code, 1)
            self.assertIn("Existing notebook entries were edited or deleted", msg)

    def test_git_invalid_or_undated_appended_entry_fails(self):
        """Scenario 6: Invalid/undated appended entry fails."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "feature/undated-entry", base_sha)
            _write(repo, "scientific_experiment_selection/module.py", "X = 4\n")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + "\n## Entry 002 — undated\nNotes.\n")
            _git(repo, "add", "scientific_experiment_selection/module.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Add undated entry")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)
            code, msg = check_repo(cwd=repo, env={"GITHUB_BASE_SHA": base_sha})
            self.assertEqual(code, 1)
            self.assertIn("Append a dated", msg)

    def test_git_plain_non_research_docs_change_passes_without_entry(self):
        """Scenario 7: Plain non-research docs change needs no notebook entry."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)
            _git(repo, "checkout", "-b", "docs/readme-update", base_sha)
            _write(repo, "README.md", "# Synthetic Repo\n\nUpdated plain docs.\n")
            _write(repo, "docs/HANDOFF.md", "# Handoff\n")
            _git(repo, "add", "README.md", "docs/HANDOFF.md")
            _git(repo, "commit", "-m", "Update plain docs")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            pr_merge_sha = _create_pr_merge_ref(repo, base_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)
            code, msg = check_repo(cwd=repo, env={"GITHUB_BASE_SHA": base_sha})
            self.assertEqual(code, 0)
            self.assertIn("no research-code or decision changes", msg)

    def test_git_missing_or_identical_base_fails_closed(self):
        """Missing/invalid base SHA or identical HEAD/base fails closed with exit code 2."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)

            # Invalid GITHUB_BASE_SHA fails closed
            code, msg = check_repo(cwd=repo, env={"GITHUB_BASE_SHA": "0" * 40})
            self.assertEqual(code, 2)
            self.assertIn("Notebook gate could not run", msg)

            # Invalid GITHUB_HEAD_SHA fails closed
            code, msg = check_repo(
                cwd=repo,
                env={"GITHUB_BASE_SHA": base_sha, "GITHUB_HEAD_SHA": "0" * 40},
            )
            self.assertEqual(code, 2)
            self.assertIn("Notebook gate could not run", msg)

            # Running directly on base_sha where base_commit == HEAD fails closed instead of bypassing
            code, msg = check_repo(cwd=repo, env={})
            self.assertEqual(code, 2)
            self.assertIn("Baseline commit resolves to HEAD", msg)

    def test_git_pr_merge_ref_rejects_missing_entry_when_main_advances_after_event_base(self):
        """Scenario 9: When main advances B -> N (with an unrelated notebook entry) after GITHUB_BASE_SHA=B
        and before refs/pull/N/merge checkout M=(N, F), a feature branch F with research code but NO
        notebook entry must compare against P1=N and fail (exit code 1), never borrowing N's entry."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)

            # Feature branch F branched from B adds research code without any notebook entry
            _git(repo, "checkout", "-b", "feature/missing-entry-stale-event-base", base_sha)
            _write(repo, "scientific_experiment_selection/model.py", "MODEL = 'synthetic'\n")
            _git(repo, "add", "scientific_experiment_selection/model.py")
            _git(repo, "commit", "-m", "Add research code without notebook entry")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            # Another PR updates main B -> N with a legitimate unrelated Notebook Entry 002
            _git(repo, "checkout", "main")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + VALID_APPEND_ENTRY)
            _git(repo, "add", NOTEBOOK)
            _git(repo, "commit", "-m", "Unrelated PR on main appends Entry 002")
            new_main_sha = _git(repo, "rev-parse", "HEAD")
            _git(repo, "update-ref", "refs/remotes/origin/main", new_main_sha)

            # GitHub regenerates synthetic PR merge M with parents (N, F), while workflow has GITHUB_BASE_SHA=B
            pr_merge_sha = _create_pr_merge_ref(repo, new_main_sha, feature_sha)
            _git(repo, "checkout", "--detach", pr_merge_sha)

            for env in (
                {"GITHUB_BASE_SHA": base_sha},
                {"GITHUB_BASE_SHA": base_sha, "GITHUB_HEAD_SHA": feature_sha},
                {},
            ):
                self.assertEqual(resolve_base_commit(cwd=repo, env=env), new_main_sha)
                code, msg = check_repo(cwd=repo, env=env)
                self.assertEqual(code, 1, f"Expected failure for env={env}, got {code}: {msg}")
                self.assertIn("require an appended", msg)

    def test_git_pr_merge_ref_passes_when_main_advances_after_event_base_and_pr_appends_own_entry(self):
        """Scenario 10: Positive counterpart to Scenario 9 — when main advances B -> N (with Entry 002)
        after GITHUB_BASE_SHA=B and feature F (branched from B) genuinely appends its own dated Entry 003,
        M=(N, F) compares against P1=N and passes."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            base_sha = _init_synthetic_repo(repo)

            # Feature branch F (branched from B) adds research code and its own dated Entry 003
            _git(repo, "checkout", "-b", "feature/genuine-entry-stale-event-base", base_sha)
            pr_entry = "\n## Entry 003 — 2026-11-09 | Feature PR dated entry\nGenuine PR notebook append.\n"
            _write(repo, "scientific_experiment_selection/model.py", "MODEL = 'synthetic'\n")
            _write(repo, NOTEBOOK, INITIAL_NOTEBOOK + pr_entry)
            _git(repo, "add", "scientific_experiment_selection/model.py", NOTEBOOK)
            _git(repo, "commit", "-m", "Add research code and Entry 003")
            feature_sha = _git(repo, "rev-parse", "HEAD")

            # Another PR updates main B -> N with Entry 002
            _git(repo, "checkout", "main")
            main_notebook = INITIAL_NOTEBOOK + VALID_APPEND_ENTRY
            _write(repo, NOTEBOOK, main_notebook)
            _git(repo, "add", NOTEBOOK)
            _git(repo, "commit", "-m", "Unrelated PR on main appends Entry 002")
            new_main_sha = _git(repo, "rev-parse", "HEAD")
            _git(repo, "update-ref", "refs/remotes/origin/main", new_main_sha)

            # Construct synthetic PR merge M with parents (N, F) containing N's notebook + F's Entry 003
            _git(repo, "checkout", "--detach", new_main_sha)
            subprocess.run(
                ["git", "merge", "--no-ff", "--no-commit", feature_sha],
                cwd=repo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            _write(repo, NOTEBOOK, main_notebook + pr_entry)
            _git(repo, "add", "scientific_experiment_selection/model.py", NOTEBOOK)
            _git(repo, "commit", "-m", f"Merge {feature_sha} into {new_main_sha}")
            pr_merge_sha = _git(repo, "rev-parse", "HEAD")
            _git(repo, "update-ref", "refs/pull/1/merge", pr_merge_sha)

            for env in (
                {"GITHUB_BASE_SHA": base_sha},
                {"GITHUB_BASE_SHA": base_sha, "GITHUB_HEAD_SHA": feature_sha},
                {},
            ):
                self.assertEqual(resolve_base_commit(cwd=repo, env=env), new_main_sha)
                code, msg = check_repo(cwd=repo, env=env)
                self.assertEqual(code, 0, f"Expected pass for env={env}, got {code}: {msg}")
                self.assertIn("dated append-only research entry found", msg)


if __name__ == "__main__":
    unittest.main()
