import unittest

from scientific_experiment_selection import __version__
from scientific_experiment_selection.__main__ import environment_report


class InfrastructureSmokeTests(unittest.TestCase):
    def test_version(self) -> None:
        self.assertEqual(__version__, "0.1.0")

    def test_diagnostics_have_required_keys(self) -> None:
        report = environment_report()
        for field in ["python_version", "platform", "project_version", "scientific_runs"]:
            self.assertIn(field, report)
        self.assertEqual(report["scientific_runs"], "none")


if __name__ == "__main__":
    unittest.main()
