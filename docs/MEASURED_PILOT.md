# Issue #34 — controlled local measured-data pilot

Owner: Codex. Reviewers: researcher + ChatGPT. Base: `8beacead30c6fd9e33ccaf7454f67fed46ddd0cb`
(main after PR #32). Branch: `feature/measured-exp3-exp5-pilot`.
Authority: [Issue #34](https://github.com/batuzunoglu/scientific-experiment-selection/issues/34)
and [latest Issue #21 approval](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21#issuecomment-6752036077).
Draft review only; no merge permission. This supersedes prior *no measured fitting*
checkpoints only for the explicitly scoped local retrospective pilot.

## Approved design and implementation

The issue already specifies the scientific design. The implementation uses a
separate measured scenario/adapter instead of relaxing synthetic-only guards or
renaming actual batches as synthetic. Importing the module does not read inputs,
fit models, install packages or run experiments. Tests use fabricated data only.
No scientific decision-register edits or new methodological choices.

`measured_pilot.py` loads only the known audited Step4 `Well_Metadata` reference
and two explicitly named raw workbooks. It reuses the prior checksum/join checks
as an execution guard; no new label reconciliation, archaeology or inference from
spectral shape. The canonical private attachment is not required to be downloaded;
the approved existing local Step4 fallback remains the configured source. A supplied
replacement source requires separate agreement/checksum validation; it is not silently
substituted by this loader. Source labels/QC and inherited authorization/verification
assertions are immutable. Issue #34 pilot authorization is recorded separately.

The frozen contract requires 70 Exp3 training wells in 18 groups, 35 Exp5 candidate
wells in 12 groups and 18 Exp5 evaluator wells in six groups. Exactly the existing
three exclusions apply. Duplicate/missing coordinates, wrong groups/components,
binary-label disagreement, invalid source/grid/hash or additional exclusions abort.
All 123 included spectra must transform in all four arms before any fitting. There
is no filtering, imputation, epsilon change or invalid-arm fallback.

Representations reuse `feature_rows` and `spectral.py` without formula changes:

| Arm | Input transformation | Width |
| --- | --- | ---: |
| B, executed first | Raw spectrum → fixed Compact8 | 8 |
| A, control | Raw spectrum | 176 |
| C | Divide full spectrum by positive trapezoidal 380–580 nm area | 176 |
| D | Same area normalization → fixed Compact8 | 8 |

Compact8 retains the approved fixed wavelengths, ratio, centroid/spread, derivative
and slope definitions. No blank subtraction, scalar offset correction, extra
smoothing or feature engineering. Existing numerical guards fail closed.

A small numeric LR helper is shared with the synthetic adapter; that adapter's type
and synthetic-batch checks remain intact. Condition-score arithmetic is similarly
shared behind separate complete-group validators. Model config and five dependency
pins are unchanged from [SYNTHETIC_LOGISTIC_NES.md](SYNTHETIC_LOGISTIC_NES.md).
At each checkpoint, a fresh StandardScaler and L2 LR use identical weights
`N/(G*n_group)` from initial plus already acquired whole conditions only. A warning
about convergence or nonfinite fitted state aborts; no tuning or stale model reuse.

The existing Random selectors (seeds 7/11/19), CoverageSelector and BudgetState are
reused. Measured prospective design objects contain nominal factors/ID/unit cost
only. Selectors receive these, acquired design history and remaining budget; no
spectra, labels, predictions, models or evaluator metrics. DoE factor novelty starts
with empty Exp5 acquisition history, not all Exp3 factors. Uncertainty stays blocked.
Each condition costs one **proxy** unit; checkpoints 0–12 each require a fresh fit.

Evaluation predicts on a deep copy of the model. Correctness is averaged within
each condition, then within each binary class; BA is mean sensitivity/specificity.
Predictions and all three metrics are private and cannot enter the selector view.
All arms share exactly the same partition, seeds, settings, orders and cost schedule.
The implementation checks paired acquisition order, not metric-based method choice.
These are trusted Python interfaces, not a sandbox against malicious introspection.

## Commands and actual local execution

Configure source variables locally, outside Git. No source values are printed:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.measured_pilot \
  --run-measured-pilot --mapping "$MAP" --raw-root "$RAW_ROOT" \
  --raw-checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt \
  --mapping-checksums "$MAPPING_CHECKSUMS" --output "$PRIVATE_OUTPUT"
```

`MAP` is the previously audited Step4 file; `MAPPING_CHECKSUMS` is its existing
source manifest. Only explicit Exp3/Exp5 raw filenames are opened. `PRIVATE_OUTPUT`
must be a new directory beneath this checkout's ignored `data/private/`; symlinked
paths, other locations and overwriting a run are rejected. Directory mode 0700,
artifact files 0600. A failed run retains a private STOP reason and partial artifacts
for review, never a successful summary. The flag records a human-approved local
workflow; it is not an authentication mechanism or new publication authority.

The actual 2026-11-09 execution used a local source-resolution wrapper based on the
two documented roots in WELL_MAP_DISCREPANCIES.md and the exact existing relative
Step4 source location. The wrapper invokes the command above, captures stderr
privately, and prints only the redacted status. Its exact resolved command is in
the private `reproduction.json`; no home-directory search or source recovery ran.

**Observed measured-data execution:** exit 0; 16 completed trajectories, 208 fresh
converged fits (13 per trajectory); all four transformations succeeded for all 123
included wells. Source hashes unchanged after execution. Private artifact checks
confirmed 13 cost checkpoints/run, unique 12-condition acquisitions, paired orders,
70→105 training counts, identical baseline/final aggregate metrics across policies
within each arm, and correct BA arithmetic. These are actual measured-data fitting
and evaluation computations, not the synthetic demo and not new wet-lab measurements.
No measured performance values, predictions, per-well maps or private digests/paths
are published here. No best arm/seed/checkpoint is selected.

The private local review package contains every BA/sensitivity/specificity trajectory,
selected conditions, costs, evaluator predictions, convergence/weight/scaler traces,
208 checkpoint models, complete reproduction metadata (hashes, code hashes, exact
argv, Python/dependency versions) and a redacted aggregate `REVIEW.md` for private
researcher/ChatGPT review. Keep the entire directory off public GitHub.

## Synthetic tests and verification

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_measured_pilot.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
python3 -m venv --without-pip /tmp/issue34-stdlib-env
PYTHONDONTWRITEBYTECODE=1 /tmp/issue34-stdlib-env/bin/python -m unittest discover -s tests -v
git diff --check
# After feature commit, before publication:
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_research_notebook.py
```

Initial test run failed because the new module did not exist. Synthetic fixtures
exercise wrong counts/roles/groups/components/labels/QC, duplicate/missing wells,
all four arms, invalid spectra, exact model/weight/scaler behavior, fresh refits,
convergence failure, forbidden source switches, required authorization and CLI
redaction, private-only output/no overwrite/no symlinks, holdout counterfactual
invariance and predict-state isolation, complete trajectories and artifacts. A
fabricated malformed Exp8 sentinel plus file-open guards checks that it is unopened.
Tests never read private sources or fit actual spectra. Existing public optional-ML
CI runs this suite with exact pins; it never invokes the measured CLI.

Observed results are recorded in the appended notebook/HANDOFF. Full test logs and
local run/validation commands are retained locally. The standard-library run also
caught an ML-dependent assertion in a test; it was guarded on optional dependency
availability. That correction affects tests only, not the measured execution.

## Review limits and stop

Historical labels are researcher-endorsed **provisional analytical references**, not
independent physical verification. There is one positive evaluator condition; its
technical wells are not independent preparations. Exp5 was historically exposed,
so no pristine holdout, confidence or generalization claim is justified. Budget is
a declared proxy, not observed lab cost. No hyperparameter/feature/seed tuning,
LOGO task, uncertainty acquisition, Exp8 access, source-label edits or new physical
experiment. Review every paired trajectory privately; do not use it to select a
winning configuration without a new protocol. Next: ChatGPT + researcher scientific
and code review of the safe Draft and private aggregate report. No merge.

## 2026-11-09 aggregate publication authorization update

The [researcher's latest PR #35 instruction](https://github.com/batuzunoglu/scientific-experiment-selection/pull/35#issuecomment-6753082959)
supersedes the earlier private-only score-reporting boundary **for sanitized aggregate
performance only**. [Complete measured results](MEASURED_PILOT_RESULTS.md) and the
linked aggregate JSON now preserve all predeclared curves for direct GitHub review.
Raw data, well labels/predictions, feature/scaler/model artifacts, local paths and
source hashes remain private. The original private report and run artifacts are
unchanged. Exporting completed results adds no model fit or methodological change.
Scientific numerical review and eventual PR #33/35 notebook reconciliation remain
open; neither PR is authorized to merge. Notebook Entry 035 records this update.
