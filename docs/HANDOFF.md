# Cross-LLM Research Handoff

**Checkpoint date:** 2026-10-20
**Phase:** Repository scaffold and Ubuntu smoke testing (NOT YET EXECUTED ON USER'S UBUNTU MACHINE).
**Status:** Starter files prepared and locally testable. No scientific models trained, no laboratory results analyzed in this repository.

## Stable goals
Reproducible ECE PhD research, paper/proposal, and a publicly presentable portfolio for 2027 internship applications. Core task: sequential physical experiment selection to adapt/verify predictive scientific models under shift, using PFAS spectroscopy first.

## What currently exists
- Markdown operating protocol and scientific charter.
- A minimal Python package with a `doctor` diagnostic.
- Standard-library smoke tests and locked baseline environment (no third-party runtime dependencies).
- No raw PFAS data have been copied into the project.

## Must verify next on Ubuntu
1. Git repo clone and correct private remote.
2. `uv sync --locked` succeeds.
3. `uv run python -m scientific_experiment_selection doctor` succeeds.
4. `uv run python -m unittest discover -s tests -v` passes.
5. Commit hash saved below.

## Checkpoint for next session
- Researcher / machine:
- Git branch / commit SHA:
- Data manifests / checksums:
- Actions and exact commands run:
- Observed outputs:
- Tests passed / failed:
- Scientific conclusions (only if supported):
- Issues / warnings:
- Next single task:

## Checkpoint 000 — Ubuntu Setup

Date: 2026-10-20
Status: Environment verified

Completed:
- GitHub repository cloned to Ubuntu.
- Project scaffold installed.
- Python environment created using uv.
- Package diagnostic successful.
- 2 infrastructure tests passed.

Scientific results:
- None yet.

Known issues:
- No scientific datasets imported.
- No ML models trained.
- No experiment-selection methods implemented.

Next milestone:
- PFAS Dataset Inventory and Data Validation.
