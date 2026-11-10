# Scientific Experiment Selection

**Project status (2026-11-10): Retrospective measured pilot completed; model-adaptive acquisition is not yet implemented.**

## Research objective

Develop and evaluate cost-aware methods that select a small number of useful experiments to improve or verify ML predictions under laboratory/batch changes. The first testbed is Ce–ARS UV–Vis spectroscopy for PFAS detection. This is an ongoing research project, not a validated autonomous laboratory system.

The approved long-term [research charter](docs/PROJECT_CHARTER.md) includes conventional experiment-selection baselines, Bayesian/active-learning approaches, numerical reinforcement learning, SLM/tool-using scientific agents, and eventual prospective laboratory validation. These later methods are research goals, not completed capabilities.

## What has been implemented

- **Data/provenance and grouped evaluation:** Audited historical Exp3/Exp5 label-to-spectrum joins and a deterministic Exp3 18-fold leave-one-condition-group-out (LOGO) plan. Historical chemical labels remain provisional, and same-solution technical wells are kept together.
- **Experiment-selection engine:** Seeded Random and deterministic nominal factor-level **coverage** (a simple DoE baseline, **not** optimal statistical design), one whole prepared condition per acquisition, explicit unit proxy budget, one-time outcome revelation, disjoint evaluation groups and leakage-checking synthetic tests.
- **Logistic Regression:** A pinned, condition-equal-weighted, training-only-scaled binary TFA vs non-TFA baseline. Four fixed spectral representations: A Raw/Full (176), B Raw/Compact8 (8), C Area/Full (176), D Area/Compact8 (8). No Ce–ARS blank subtraction or 650–700 nm offset correction was performed in the measured pilot.
- **Retrospective measured Exp3 → Exp5 pilot:** 70 Exp3 training wells in 18 conditions, 35 Exp5 acquisition wells in 12 conditions, and 18 Exp5 fixed evaluation wells in six conditions, with the approved D6/D7/B7 exclusions. Four representations × (Random seeds 7/11/19 + coverage) yielded 16 trajectories, 208 fit checkpoints and 624 public aggregate scores. Costs are *proxy condition units*, not measured money or laboratory time.
- **Reproducible reporting:** Condition-aware Balanced Accuracy, TFA sensitivity and specificity at every budget 0–12; 300 dpi PNG/vector PDF plots, complete public aggregate CSV/JSON and figure notes, synthetic tests and CI workflows. The original raw workbooks, per-well predictions, fitted models and other private run artifacts are not published.

## Measured pilot observations (historical, not a new run)

| Representation | Balanced Accuracy, 0 → 12 acquired conditions | TFA sensitivity, 0 → 12 |
| --- | --- | --- |
| A Raw/Full | 0.933333 → 0.833333 | 1.000000 → 0.666667 |
| B Raw/Compact8 | 0.500000 → 0.500000 | 0 throughout |
| C Area/Full | 0.900000 → 0.600000 | 1.000000 → 0.333333 |
| D Area/Compact8 | 0.500000 → 0.500000 | 0 throughout |

Acquiring more conditions did **not** consistently improve fixed Exp5 performance. Exp5 was exposed in historical development and is not a pristine external holdout. The evaluator has only **one positive prepared condition** (TFA 10 ppm, three related technical wells), so sensitivity/BA estimates are fragile. Historical sample chemistry remains provisionally labeled. No selector superiority, causal Compact8 diagnosis, prospective benefit or unseen-batch generalization is established.

Details: [measured pilot results](docs/MEASURED_PILOT_RESULTS.md), [figure/method notes](docs/MEASURED_PILOT_FIGURE_NOTES.md), [figures](docs/figures/measured_pilot/), [aggregate JSON](docs/results/exp3-exp5-nes-2026-11-09-aggregate.json), and merged [PR #37](https://github.com/batuzunoglu/scientific-experiment-selection/pull/37).

## Current research direction and pending decisions

**Recorded researcher direction:** Continue with Logistic Regression as the primary **model family**, defer the Compact8/1-NN comparison originally scoped in [Issue #36](https://github.com/batuzunoglu/scientific-experiment-selection/issues/36), and retain the poor Compact8 results without retroactive tuning. The immediate priority is to understand and plan **model-adaptive next-experiment selection**, not to rerun the exposed Exp5 benchmark.

**Not yet selected or approved:** Fixing A Raw/Full (or any one of A/B/C/D) as the sole primary representation; a new acquisition policy, surrogate/digital twin, information-gain objective, acquisition-time observation/price regime, new measured fits or new wet-lab actions. These require explicit scientific design and authorization. Current Random and coverage selectors see design metadata only; the existing uncertainty selector deliberately rejects execution. No EIG, Bayesian adaptive selector, RL policy or SLM agent has been implemented.

**Protected data:** Exp8 remains locked; neither outcomes nor spectra are available for method selection or tuning. Exp5 is historically exposed and cannot be made pristine by refitting. Any future validation must distinguish held-out group results, genuinely independent preparations and new batches.

## Run available synthetic checks / reproduce public figures

From the repository root after installing the project environment (see `uv.lock` and optional pinned requirements):

```bash
uv sync --locked
uv run python -m scientific_experiment_selection doctor
uv run python -m unittest discover -s tests -v
uv run python -m scientific_experiment_selection.selection_demo --seed 7 --budget 3
```

The synthetic selection demo uses fabricated data and is **not** a real experiment or measured result. To reproduce the existing **public-aggregate-only** figures, install `requirements/figures.txt` and run `scripts/plot_measured_pilot_results.py`; see the [figure/method notes](docs/MEASURED_PILOT_FIGURE_NOTES.md). Do not run a private measured-data fit without a separate approved protocol.

## Project records

- [Research charter](docs/PROJECT_CHARTER.md), [decisions](docs/DECISIONS.md), and the append-only [research notebook](docs/RESEARCH_LAB_NOTEBOOK.md)
- [Handoff checkpoints](docs/HANDOFF.md) and [agent workflow](docs/AGENT_WORKFLOW.md)
- [Dataset reconciliation and limitations](docs/DATASET_RECONCILIATION_REVIEW.md), [Exp3 LOGO protocol](docs/PHASE_B_LOGO_PLAN.md)
- [Synthetic experiment-selection specification](docs/SELECTION_MVP.md) and [Logistic Regression NES protocol](docs/SYNTHETIC_LOGISTIC_NES.md)

## Research integrity

Never present synthetic outputs as laboratory measurements or provisional labels as independently verified chemistry. Never choose a policy by repeatedly tuning against the fixed Exp5 evaluator, and never expose Exp8 to model/selector development. Keep original raw files unchanged and private; document permissions and provenance before publishing. Scientific/methodological changes require a dated notebook entry, researcher review and a scoped PR rather than direct pushes to `main`.
