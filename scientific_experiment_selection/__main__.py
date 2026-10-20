"""Minimal diagnostics: infrastructure only, no scientific computation."""

import argparse
import platform
from pathlib import Path

from scientific_experiment_selection import __version__


def environment_report() -> dict[str, str]:
    return {
        "project_version": __version__,
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "project_directory": str(Path.cwd()),
        "scientific_runs": "none",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Research repository diagnostics")
    parser.add_argument("command", choices=["doctor"])
    args = parser.parse_args()
    if args.command == "doctor":
        for key, value in environment_report().items():
            print(f"{key}: {value}")
        print("OK: package imports and Python executes (not a scientific validation).")


if __name__ == "__main__":
    main()
