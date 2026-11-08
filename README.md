# Scientific Experiment Selection

**Status: Project infrastructure / zero empirical results.**

## Purpose
Study reliable, cost-aware selection of physical experiments to improve or verify ML predictions when experimental conditions change. The first candidate testbed is Ce–ARS/PFAS spectroscopy. We will compare well-established experiment design, active learning and Bayesian baselines before testing RL policies and small-language agents.

## First-time setup (Ubuntu)
1. Clone your **private** GitHub repository.
2. Copy the scaffold contents into its root (do not overwrite existing files without reviewing changes).
3. Run `uv sync --locked` in the repository root. If `uv` is not installed, see https://docs.astral.sh/uv/getting-started/installation/.
4. Run `uv run python -m scientific_experiment_selection doctor`.
5. Run `uv run python -m unittest discover -s tests -v`.
6. Review `git status` and commit only after verifying what changed.

## What the first tests prove
The Python environment can run a tiny local program and a standard-library test suite. They do **not** establish scientific validity or perform an ML training run.

## Directory map
- `AGENTS.md`: instructions for AI coding/research assistants.
- `docs/PROJECT_CHARTER.md`: goals and boundaries.
- `docs/DECISIONS.md`: decision record.
- `docs/RESEARCH_LAB_NOTEBOOK.md`: dated scientific reasoning and experiment log; read before making modeling decisions.
- `docs/HANDOFF.md`: session and cross-model checkpoint.
- `docs/LEARNING_LOG.md`: teach-first notes.
- `docs/EXPERIMENT_TEMPLATE.md`: laboratory/computational experiment record.
- `data/`: metadata and documented datasets (private raw files excluded from Git).
- `scientific_experiment_selection/`: initial runnable package stub.
- `tests/`: fast deterministic smoke tests.
- `results/`, `proposal/`, `paper/`: later verified research outputs.

## Research integrity and safety
Do not record simulated values as observed experimental results; avoid using target held-out outcomes for acquisition decisions. Preserve raw exports unchanged. No public release of lab data before verifying rights and permissions. No model or dataset has been created/processed in this scaffold.

## Current ML methodology checkpoint

We will study **PFAS identity and concentration as two separate tasks**. Source processing and model choices must preserve the Raw/full-spectrum comparison and explicitly evaluate possible loss of chemical information. Historical Exp3/Exp5 model development prevents calling Exp5 a fully untouched final test. Exp8 is an intended locked 10-ppm holdout pending historical-exposure review. Current preprocessing, feature set and split decisions remain proposed until researcher sign-off. See `docs/RESEARCH_LAB_NOTEBOOK.md` and Issue #5 before training.
