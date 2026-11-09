# Synthetic next-experiment selection MVP — Issue #27

Owner: Codex. Scientific reviewers: ChatGPT + researcher. This is a standard-library
engineering scaffold with fabricated data only. It does not load real data, fit a
real classifier, choose a scientific winner or amend an approved decision.

## Run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.selection_demo --seed 7 --budget 3
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_selection.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

The demonstration prints paired synthetic Random/coverage action logs and curves.
Every result is marked `synthetic-only`. It has four nominal toy candidate conditions,
variable technical-replicate counts, a separate initial pool and fixed separate
holdout. Label 1 denotes the fabricated TFA standard and 0 the other standard.
These constants are not derived from any private laboratory records.

## Boundaries and flow

```text
prospective designs + acquisition-only history + remaining budget
                         |
                      selector
                         |
      validate unselected affordable condition ID
                         |
              oracle.reveal(condition ID) once
                         |
       charge one group cost; reveal ALL technical replicates
                         |
      synthetic model.fit(initial + acquired groups only)
                         |
  evaluator predicts on a copy of fitted adapter and fixed holdout
                         |
     append evaluator-only curve point; continue selection
```

`CandidateExperiment` is frozen, with opaque group ID, synthetic batch, immutable
nominal factor-level string pairs and positive integer cost. There is no spectrum,
feature array, observed response, label, model error or holdout score field. Known
nominal standard identity/concentration may be design settings; they are not an
observed experimental outcome. Obvious observed/predictive setting keys are rejected.
The caller is responsible for truthful prospective metadata; naming checks cannot
establish its origin. Batch names must explicitly start with `synthetic-`.

`Selector.choose(available_designs, observed_history, budget_state)` sees only an
immutable affordable subset and previously acquired **design metadata**, plus frozen
budget state. History deliberately excludes even the acquired spectra/labels and all
evaluation outputs. It starts empty: this MVP's initial training groups do not carry
prospective settings for coverage. The selector is not given a model or oracle.

`SyntheticOracle` holds immutable full-group outcomes, rejects unknown/repeated
reveal calls, and is never passed to a selector. The engine validates the action
before revelation. Initial, acquisition and holdout group IDs must be unique and
disjoint, widths agree, and each condition group has one consistent binary label.
A group denotes an indivisible prepared condition, not one well. Caller-supplied
canonical group IDs must identify shared preparations honestly: aliasing the same
preparation under different IDs cannot be discovered from this metadata alone.

Selectors operate as follows:
- **Random:** uniform choice over affordable unselected IDs sorted canonically,
  using a private local RNG and explicit integer seed. Same seed/scenario gives
  deterministic runs, independent of input ordering. Use a fresh instance per run.
- **DoE/coverage:** greedily maximize the number of unseen nominal `(factor, level)`
  pairs relative to acquired designs; break ties by opaque ID. This is an elementary
  condition-space coverage baseline, not statistical D-optimality, a predictive
  spectrum method or a proven optimal design. Numeric levels are nominal strings;
  no scaling/distance/geometry is inferred or fitted. Costs constrain feasibility
  but do not divide the novelty score. Duplicate settings across distinct genuine
  conditions are allowed; no new preparation independence is inferred.
- **Uncertainty stub:** rejects every execution attempt, including caller strings
  claiming screening or surrogate access. No scientific capability/access/cost
  regime has been approved. A future implementation must separately validate and
  budget permitted predictive inputs; ordinary hidden candidate-spectra entropy
  is not a free next-measurement policy. Zero-acquisition runs need no selection.

`BudgetState` uses exact integer synthetic cost units. Charges are per selected
condition, irrespective of replicate count. A zero budget yields the starting-model
curve point without acquisition. Stop when the pool is exhausted, remaining budget
is zero, or no remaining condition is affordable. Invalid/duplicate/holdout actions
fail rather than silently substituting an experiment. A failed fit/evaluation aborts
the run; no retry/refund or external laboratory transaction is implemented.

`ModelAdapter` hooks accept immutable grouped training data and explicit per-well
weights giving each condition equal total weight: `N / (G*n_group)`. This normalization
is an engineering fixture; no real estimator/scaling/sample-weight protocol is
scientifically frozen here. The fake `SyntheticMeanModel` ignores spectra and uses
only a weighted synthetic label mean with a 0.5 threshold. It is intentionally not
an ML baseline to adopt on real data. No dependency or real-model fitting is added.

The evaluator alone owns the fixed holdout and labels. It predicts on a deep copy
of the trained adapter, preventing ordinary predict-time mutations from returning
holdout data to the live learner; it never calls fit on evaluation data. Its toy
score is mean condition accuracy (each group equal regardless of technical wells).
This is a synthetic diagnostic, not a frozen real metric or generalization claim.
RunResult exposes curves only after completion; they are never selector inputs.
Adapters must support deepcopy and be trusted side-effect-free code.

Action logs record group ID, cost, cumulative spend and the names of available
information sources. Curves start at zero acquisitions and log acquired **conditions**,
actual cumulative cost and evaluator accuracy. Random seed and budget are included.
`compare_selectors` creates fresh policies/adapters on the identical immutable
scenario and cost schedule. Equal-cost fixtures have paired cost checkpoints;
variable-cost choices may have different interior checkpoints. No interpolation,
post-hoc budget matching, tuning or claim of one policy's superiority is performed.

## Verification and limits

Synthetic tests check immutability and invalid input, group identity separation,
reveal-after-valid-action order, one-shot/whole-group revelation, no duplicate or
unaffordable action, zero/exact/insufficient budgets, equal condition weights,
determinism, seeded ordering, DoE novelty, identical-scenario comparisons, holdout
isolation and blocked uncertainty regimes. Changing hidden candidate outcomes or
holdout labels must not change action sequences; evaluator predict side effects
must not reach the training adapter. Test/demo arrays are fabricated constants.

These are in-process API boundaries, not a security sandbox against malicious
Python introspection, captured oracle references, global state, callbacks or an
external user tuning against returned holdout curves. No cryptographic oracle,
process isolation, filesystem/network sandbox or data-origin verification is claimed.
The real benchmark requires a frozen acquisition/evaluation protocol and trustworthy
adapters/metadata. Synthetic success cannot demonstrate laboratory cost savings,
TFA recognition, Exp5 adaptation or Exp8 generalization.

Remaining scientific gates under Issue #21: real classifier/preprocessing (including
any separately reviewed scalar-offset sensitivity), metrics/weights, Exp5 pool vs
fixed evaluation groups and eligibility, screening/surrogate information costs,
real-data access/fitting approval and future Exp8 exposure/holdout audit. Existing
A/B/C/D formulas, D-012/D-019 and all source flags remain unchanged.
