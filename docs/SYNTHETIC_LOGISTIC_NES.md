# Issue #29 — synthetic Logistic Regression NES integration

Owner: Codex. Reviewers: ChatGPT + researcher. Draft/code review only; no real-data
access/fitting or merge approval. Base is main after PR #28 (`861e07e`). Binding
Issue #21 approvals: [fixed split](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21#issuecomment-6749253141),
[B-first/four-arm plan](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21#issuecomment-6749392851),
[weights and metrics](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21#issuecomment-6749605069).

## Install and run synthetic examples

The standard-library scaffold/fake demo remains dependency-free. ML integration
is optional and isolated in `requirements/logistic.txt`, pinning all five runtime
packages: numpy 2.2.6, scipy 1.15.3, scikit-learn 1.7.2, joblib 1.5.2,
threadpoolctl 3.6.0. The adapter fails if installed versions differ from these pins.
No automatic package install occurs in library code. Python tested: 3.12.14.
These are reproducibility pins, not a claim to use the newest releases.

```bash
uv pip install --python .venv/bin/python -r requirements/logistic.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.logistic_demo --arm B --budget 12 --seeds 7 11 19
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_logistic_nes.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.selection_demo --seed 7 --budget 3
```

Observed: 16 new tests passed; full optional-ML suite **102/102 passed** (86 existing
plus 16 new). In a separate clean standard-library venv created with
`venv.EnvBuilder(with_pip=False)`, the same `-m unittest discover -s tests -v`
command ran 102 tests successfully with the 10 ML-dependent methods skipped.
Six new protocol/isolation tests and all prior tests run without ML packages.
Dedicated CI installs/verifies exact pins and executes the entire suite plus the
full B-arm demo, so the real Logistic Regression integration is not silently skipped.
The existing notebook/standard-library CI job remains unchanged.

API references: [StandardScaler.fit sample weights](https://scikit-learn.org/1.7/modules/generated/sklearn.preprocessing.StandardScaler.html),
[LogisticRegression](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.LogisticRegression.html),
[scikit-learn 1.7.2 release dependencies](https://pypi.org/project/scikit-learn/1.7.2/).

## Fixed recipe and training boundary

Synthetic binary labels: TFA=1, other PFAS=0. Default B = **Raw/Compact8**.
The adapter uses the existing spectral functions unchanged; it adds no blank,
scalar-offset or other baseline correction. All four arms are selectable:
A raw/full 176, B raw/Compact8 8, C area/full 176, D area/Compact8 8. All use the
same scenario, group eligibility, fixed roles, selector rules and unit costs.
Only B is used for the reported budget demonstration; no representation is chosen
by inspecting these curves. Unit tests fit/predict all four dimensional contracts.

Approved constraints are L2, C=1.0, class_weight=None, condition-equal sample weights
and training-only StandardScaler. Fixed numerical implementation details (not a
hyperparameter search): lbfgs, max_iter=5000, random_state=0, tol=1e-4,
fit_intercept=True, warm_start=False. Native thread count is limited to one for
repeatability. No pipeline-routing assumptions: identical explicit sample-weight
arrays are passed to `StandardScaler.fit` and `LogisticRegression.fit`.

Every fit is from scratch on initial plus already acquired **whole groups**:
`w_i=N/(G*n_group)`; each condition total is N/G and total sample weight N.
Weights are recomputed and validated at every update. No class-balanced multiplier
is applied. This preserves group equality even when a group has two technical
replicates and others have three/four; it does not make the binary classes equally
weighted. Both training classes are required. Failed feature transforms or
convergence warnings stop the run without dropping a well, changing C or reusing
a stale classifier. New scaler/estimator instances are created every time.

The adapter implements existing fit(groups)/predict(spectra), with lazy ML imports.
Fit traces record synthetic training group IDs, counts/weights, feature width,
scaler means and convergence/iteration status. These are synthetic diagnostic
values only. Prediction transforms with the fitted scaler; it never fits it.

## Synthetic partition and decision-time information

A public metadata specification encodes the exact approved nominal Exp5 partition:

| ppm | Evaluator-only conditions | Acquirable conditions |
| --- | --- | --- |
| 5 | PFPA, PFOA | TFA, PFBA, PFHxA, PFNA |
| 10 | TFA, PFHxA | PFPA, PFBA, PFOA, PFNA |
| 20 | PFBA, PFNA | TFA, PFPA, PFHxA, PFOA |

Validation rejects missing/reassigned conditions, wrong nominal settings/labels,
batches or dimensions. The fixture has 18 initial synthetic condition groups,
12 acquisition groups and 6 fixed evaluation groups. Synthetic replicate counts
illustrate 70 initial, 35 acquirable and 18 evaluator rows, including the two-replicate
special groups. These are fabricated examples of already public design counts,
not copied from manifests and not a new well-level eligibility audit. No actual
excluded well is loaded or reinstated; any future real loader must separately
preserve the historical exclusion rules and obtain authorization.

The analytic generator uses positive baseline plus two Gaussian peaks, with a
predeclared synthetic target baseline/peak-strength shift and deterministic replicate
variation. Constants were fixed before the first model run and not adjusted after
seeing results. It is not a calibrated chemical simulator. All batches have explicit
`synthetic-` prefixes; group IDs identify whole conditions. No data-loading interface.

Existing Random/DoE selectors and oracle/budget guards remain. Selectors receive
only nominal prospective design settings, acquisition-design history and remaining
budget, never candidate spectra, scaler/model state, outcomes or evaluator results.
One valid unselected affordable action reveals an entire synthetic group, then the
scaler and LR are refitted on the expanded training pool. The fixed evaluator alone
predicts on a deep copy of the model, preserving holdout isolation. Uncertainty
selection remains blocked. Python interface separation is not a malicious-code
sandbox; adapters and truthful preparation IDs are still trusted assumptions.

## Correct metrics and observed synthetic curves

At every fixed cost checkpoint (including k=0), average correctness **within each
condition**, then average same-class condition recalls. Primary balanced accuracy
is `(TFA sensitivity + non-TFA specificity)/2`. Sensitivity and specificity are
reported separately. Missing either evaluation class raises an error; invalid or
incomplete predictions fail. Extra technical replicates do not add condition weight.
Legacy `CurvePoint.accuracy` retains condition-equal accuracy and is explicitly
separate from new balanced_accuracy/sensitivity/specificity fields.

The full default demonstration was executed at all cost checkpoints 0–12, with
three predeclared Random seeds and one deterministic DoE run. Each costs one
synthetic unit per full group, giving 13 scaler/estimator refits per run. The
printed JSON includes every checkpoint, selected synthetic condition, actual cost,
fit provenance, versions and fixed model config. No best seed/iteration is selected.

| Acquired conditions / cost | Random 7 BA | Random 11 BA | Random 19 BA | DoE BA |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.5 | 0.5 | 0.5 | 0.5 |
| 1 | 0.5 | 0.5 | 1.0 | 0.5 |
| 2 | 0.5 | 0.5 | 1.0 | 0.5 |
| 3 | 0.5 | 0.5 | 1.0 | 0.5 |
| 4 | 0.5 | 1.0 | 1.0 | 0.5 |
| 5 | 0.5 | 1.0 | 1.0 | 0.5 |
| 6 | 1.0 | 1.0 | 1.0 | 1.0 |
| 7 | 1.0 | 1.0 | 1.0 | 1.0 |
| 8 | 1.0 | 1.0 | 1.0 | 1.0 |
| 9 | 1.0 | 1.0 | 1.0 | 1.0 |
| 10 | 1.0 | 1.0 | 1.0 | 1.0 |
| 11 | 1.0 | 1.0 | 1.0 | 1.0 |
| 12 | 1.0 | 1.0 | 1.0 | 1.0 |

For all runs, specificity is 1.0 throughout; sensitivity is 0 where BA=0.5 and 1
where BA=1.0. These are observed synthetic computations, **not measured chemical
results or evidence that Random/DoE is superior**. In particular, the fixed evaluator
has only **one positive condition** (and five negative conditions). Technical wells
do not provide independent positive preparations, and this simple synthetic fixture
cannot validate robustness, confidence or generalization. No smoothing, interpolation,
seed selection or tuning was used to obtain this table.

## Tests, privacy and handoff

New tests exercise exact roles and dimensions, wrong partitions/metadata/labels,
unequal-replicate group/class metric math, missing classes/invalid predictions,
all four unchanged spectral paths, exact recipe/no class balancing, equal-total
sample weights and estimator/scaler weight identity, weighted scaler statistics,
new scaler/model at each step, fit group IDs limited to initial+acquired groups,
holdout/unselected extreme-value isolation, failed transforms/convergence rejection,
selectors unchanged by counterfactual hidden labels, repeated paired curves and
independence of the stdlib demo from ML imports. Initial missing-module test failure
preceded implementation. No actual data or historical outcomes were accessed.

Scientific decisions register, existing spectral math and source labels/flags are
unchanged. This is not the separate Exp3 D-019 LOGO model-development evaluation.
Real Exp3/Exp5 data access, eligibility/physical-claims checks and fitting need separate
permission. Exp5 is historically exposed/reconstructed and cannot be described as
a pristine test. Exp8 remains unopened/locked. No surrogate, RL or actual model on
measured spectra. Next owner: ChatGPT + researcher reviews this Draft, synthetic
boundaries and numerical choices before any independent real-data authorization.
