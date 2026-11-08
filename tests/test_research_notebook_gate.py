"""Synthetic checks for the PR notebook quality gate; no raw lab files needed."""
import unittest

from scripts.check_research_notebook import needs_notebook, valid_append


class NotebookGateTests(unittest.TestCase):
    def test_code_and_methodology_changes_require_entry(self):
        self.assertTrue(needs_notebook(["scientific_experiment_selection/model.py"]))
        self.assertTrue(needs_notebook(["docs/DECISIONS.md"]))
        self.assertTrue(needs_notebook(["tests/test_features.py"]))
        self.assertTrue(needs_notebook(["experiments/exp1.py"]))

    def test_plain_readme_change_does_not_require_entry(self):
        self.assertFalse(needs_notebook(["README.md"]))

    def test_valid_dated_append(self):
        old = "# Research Lab Notebook\n\n## Entry 001 — 2026-11-08\nEarlier.\n"
        new = old + "\n## Entry 002 — 2026-11-08\nQuestion, decision and evidence.\n"
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


if __name__ == "__main__":
    unittest.main()
