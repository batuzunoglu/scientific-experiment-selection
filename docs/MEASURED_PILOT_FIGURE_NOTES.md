# Measured Exp3–Exp5 pilot: figure and reproducibility archive

Owner: Codex. Scientific reviewers: researcher + ChatGPT. Reporting only, 2026-11-10.
PRs [#33](https://github.com/batuzunoglu/scientific-experiment-selection/pull/33) and
[#35](https://github.com/batuzunoglu/scientific-experiment-selection/pull/35) are merged
into main. This branch starts at `cf0084fcc0b6ba4113edaab7e5c157d4db19a5e6`.
No historical result, source label, transformation or fitted model is changed.
No new measured training, refitting, prediction, tuning or Exp8 access is performed.
The existing full test suite still fits **synthetic fixtures only**.

## Public source and exact reproduction

Source: [published aggregate JSON](results/exp3-exp5-nes-2026-11-09-aggregate.json),
also described in [the complete measured-results report](MEASURED_PILOT_RESULTS.md).
Its SHA-256 is:

```text
3d0ebbb13632854b14ee4e97dabdcef305f06dca4ebd1246b621456ff55e767e
```

Validated before plotting: four representations × (Random seeds 7/11/19 + one
DoE) = **16 trajectories**, each with budgets **0–12**, **208 checkpoints**, and
**624 metric values**. Validation rejects extra fields, malformed/incomplete roles,
nonfinite/out-of-range scores, duplicate trajectories and wrong budgets. Only the
public JSON is an input to the main plotting script; private data and learner
modules are never imported by it.

```bash
uv pip install --python .venv/bin/python -r requirements/figures.txt
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python scripts/plot_measured_pilot_results.py
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python -m unittest discover -s tests -v
git diff --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_research_notebook.py
```

The default source/output locations are repository-relative and configurable through
`--source`, `--figure-dir` and `--result-dir`. Optional plotting pins are separate
from ML dependencies. The reporting CI installs them, executes tests and regenerates
figures/tables from **public aggregates only**. It compares all generated tables with
the versioned files and never opens private artifacts or runs measured fitting.

### Public archive contents

| Figure | PNG (300 dpi) | Vector PDF |
| --- | --- | --- |
| 1: Balanced Accuracy | [PNG](figures/measured_pilot/figure_1_balanced_accuracy.png) | [PDF](figures/measured_pilot/figure_1_balanced_accuracy.pdf) |
| 2: TFA Sensitivity | [PNG](figures/measured_pilot/figure_2_tfa_sensitivity.png) | [PDF](figures/measured_pilot/figure_2_tfa_sensitivity.pdf) |
| 3: Specificity | [PNG](figures/measured_pilot/figure_3_specificity.png) | [PDF](figures/measured_pilot/figure_3_specificity.pdf) |

- [Plot data CSV](results/measured_pilot_plot_data.csv): 208 rows, every trajectory,
  condition budget, proxy cost, arm, representation, policy, seed and all three scores.
- [Full endpoint summary CSV](results/measured_pilot_summary.csv): initial, final and
  paired change, Random mean/sample SD and deterministic DoE, for every arm/metric.
- [Concise endpoint summary table](results/measured_pilot_summary.md): same summary,
  rounded to six decimals for display, including changes and descriptive SD.
- [Figure manifest](figures/measured_pilot/manifest.json): public input SHA-256,
  generated-file checksums, dimensions/DPI, Python/Matplotlib/NumPy versions and SD rule.

The JSON already contains six-decimal reporting precision; this archive does not
recover or imply unavailable additional measurement precision. CSV metric strings
are written from Decimal values without rounding, preserving **every numerical
value in that JSON**. Descriptive calculations use 50-digit Decimal arithmetic;
only plotting coordinates are converted to floats. Endpoint changes are paired
within each Random seed before their mean and sample SD are calculated. DoE has no
seed SD. Zero endpoint SD reflects identical scores at those checkpoints, not an
absence of intermediate variation or evaluator uncertainty.

## Plotting and descriptive-statistics conventions

All figures use the same four-panel order A/B/C/D, 10 × 7.8 inch canvas, DejaVu Sans,
embedded TrueType PDF fonts, axes spanning 0–1, integer budgets 0–12 and colorblind-
friendly Okabe–Ito colors. Random seeds are blue circles (7), sky-blue diamonds
(11) and green triangles (19); black squares/error bars show their mean ± sample
SD; orange crosses show deterministic DoE. Concentric markers retain coincident
observations at their exact coordinates, and constant panels are annotated.
No jitter, smoothing, connecting/interpolating segments or checkpoint selection.
All PNGs are 3000 × 2340 pixels at 300 dpi; PDFs contain vector marks and text.

For each arm, metric and budget, with three Random scores $r_s$:

$$\bar r=\frac{1}{3}\sum_s r_s,\qquad
s_r=\sqrt{\frac{\sum_s(r_s-\bar r)^2}{3-1}}.$$

This is **sample SD (ddof=1), descriptive across three fixed seeds**, not a confidence
interval, standard error or measure of independent preparation uncertainty. SD
bars are shown only at observed checkpoints; a descriptive mean ± SD may extend
outside the bounded score range, while metric axes stay at 0–1. No bar endpoints
are treated as additional scores. Three orderings on one fixed evaluator are
insufficient for statistical superiority claims about Random or DoE.

## Figure captions, observations and limitations

### Figure 1 — Balanced Accuracy Learning Curves

**Caption.** Retrospective measured Exp3→Exp5 condition-aware Balanced Accuracy
versus acquired experimental conditions for (a) A Raw/Full, (b) B Raw/Compact8,
(c) C Area/Full and (d) D Area/Compact8. Each marker is an observed checkpoint from
the frozen pilot: three Random acquisition seeds, their descriptive mean ± sample
SD (n=3, ddof=1), and deterministic nominal-coverage DoE. One proxy cost unit
acquires a complete condition; every run retains budgets 0–12. No interpolation,
smoothing or favorable-run selection is applied. Error bars are not confidence
intervals. The same fixed, historically exposed Exp5 evaluator and provisional
labels are used throughout; these results do not establish policy superiority.

**Observed.** A and C have different trajectories and order-dependent intermediate
scores; their common initial→final BA values are 0.933333→0.833333 and
0.900000→0.600000, respectively. B and D remain at BA 0.500000 for every strategy
and checkpoint. Acquisition does not yield consistent monotonic improvement.

**Limits.** BA gives equal class weight, but sensitivity is based on only one
TFA-positive prepared condition. Correlated technical wells and prior Exp5 exposure
prevent interpreting these curves as independent-batch generalization or chemistry
truth; the seed SD is not a confidence statement.

### Figure 2 — TFA Sensitivity Learning Curves

**Caption.** TFA sensitivity on the fixed Exp5 evaluator across the same complete
acquisition trajectories, panel order, markers, proxy costs and descriptive Random
mean ± sample SD as Figure 1. No new model calculations are performed for this
figure; it displays the recorded checkpoint sensitivities. Compact8 zero-sensitivity
panels retain the zero-valued markers and an explicit coincidence annotation.
The evaluator contains one positive prepared condition with three technical wells,
so these values provide limited independent positive-condition evidence.

**Observed.** B and D have zero TFA sensitivity throughout all recorded trajectories,
despite the increasing acquisition budget. A ends at 0.666667 and C at 0.333333,
both starting at 1.000000; C in particular shows substantial intermediate changes
across the three Random orderings and DoE. No cause of these changes is established
by this figure, and no arm, seed or budget is selected from the exposed evaluator.

**Limits.** The three positive technical wells are not independent positive
preparations. Sensitivity fluctuations on this single historically exposed
condition do not demonstrate chemical identity, generalization or statistical
superiority; the Compact8 failure mechanism remains unverified.

### Figure 3 — Specificity Learning Curves

**Caption.** Non-TFA specificity on the same five fixed negative Exp5 condition
groups across all 16 acquisition trajectories, with the same panels and plotting
conventions as Figures 1–2. Within-condition technical-well correctness is averaged
first, followed by the mean across negative conditions. Markers retain every
budget; black error bars describe variation among three Random seeds and are not
confidence intervals. DoE is deterministic nominal coverage, not active learning.

**Observed.** B and D retain specificity 1.000000 at every checkpoint; Figure 2
shows that this coexists with zero TFA sensitivity. A increases from 0.866667 to
1.000000, while C changes from 0.800000 to 0.866667, with intermediate order-dependent
variation. Specificity alone therefore does not summarize binary detection behavior.

**Limits.** These are five historically exposed negative conditions, not a new
independent batch; their technical replicates are not independent preparations.
High specificity does not establish useful positive detection or certified physical
labels, and no policy-superiority inference is warranted.

## Source-verified model and spectral configuration

Verified against [measured_pilot.py](../scientific_experiment_selection/measured_pilot.py),
[_logistic_core.py](../scientific_experiment_selection/_logistic_core.py),
[logistic.py](../scientific_experiment_selection/logistic.py),
[nes_protocol.py](../scientific_experiment_selection/nes_protocol.py),
[spectral.py](../scientific_experiment_selection/spectral.py) and
[selection.py](../scientific_experiment_selection/selection.py). This section
records existing behavior; it introduces no transformation or learner change.

- **Task:** binary TFA=1 vs other single PFAS=0, with researcher-endorsed provisional
  historical analytical labels; no independent physical label certification.
- **Fixed inputs:** 70 Exp3 training wells / 18 conditions; 35 Exp5 acquirable wells /
  12 conditions; 18 Exp5 evaluator wells / six conditions. Three approved exclusions:
  Exp3 D6/D7 and Exp5 B7. No further exclusions. Technical wells from a condition
  stay together; 12 acquisitions yield 105 training wells, not 12 new independent batches.
- **Evaluator conditions:** PFPA_5, PFOA_5, TFA_10, PFHxA_10, PFBA_20, PFNA_20;
  TFA_10 is the only positive condition-level evaluation unit.
- **Learner:** scikit-learn 1.7.2 LogisticRegression, penalty `l2`, C=1.0,
  class_weight=None, solver `lbfgs`, max_iter=5000, tol=1e-4, fit_intercept=True,
  random_state=0, warm_start=False. Native fitting threads limited to one.
  Existing ML pins remain NumPy 2.2.6, SciPy 1.15.3, joblib 1.5.2 and
  threadpoolctl 3.6.0, in addition to scikit-learn.
- **Condition-equal fitting weights:** for N currently acquired training wells and
  G training conditions, each well in condition g with $n_g$ wells gets
  $w_i=N/(G n_g)$. Total condition weight is N/G; total weight is N. These are
  not equal per-well weights or class-balanced weights.
- **Feature standardization:** a new StandardScaler(with_mean=True, with_std=True)
  fits **only current training features** with those same weights. Nondegenerate
  feature means/variances are the weighted mean and weighted population variance
  (ddof=0); scikit-learn handles constant features. The fitted scaler then transforms
  current training features for LR and held-out features for evaluation only.
  LR receives the identical weight vector. Held-out data never fit the scaler.
- **Fresh fits:** the existing pilot created new scaler and LR instances at k=0
  and after each whole-condition acquisition: 13 fits × 16 runs = 208. Failed
  transforms or convergence abort; no stale classifier or automatic retuning.
  This reporting task does **not** repeat those fits.
- **Policies:** Python seeded Random(7/11/19) chooses uniformly among the sorted
  remaining design objects. Deterministic CoverageSelector counts unseen nominal
  analyte/concentration factor levels within **acquisition history only**, breaking
  ties by group ID. It starts with empty acquisition history, not Exp3 factor
  coverage. Unit cost is a declared whole-condition proxy. Neither selector sees
  outcomes, fitted models, predictions or evaluator metrics; no uncertainty selector.
- **Metrics:** correctness is averaged within each evaluator condition. TFA sensitivity
  is the mean positive-condition correctness, specificity the mean negative-condition
  correctness, and BA their arithmetic mean. Evaluating a deep copy prevents
  predict-state feedback to the learner. No confidence intervals are estimated.

### Representations and baseline correction distinction

Let $y_i$ be the measured absorbance at $\lambda_i=350+2i$ nm for $i=0,\ldots,175$.
The exact full grid is 350–700 nm in 2 nm steps, 176 channels. Let $B=\{15,\ldots,115\}$
be the inclusive 380–580 nm band and $h=2$ nm. Area is

$$S=\sum_{i=15}^{114}\frac{h}{2}(y_i+y_{i+1}).$$

S must be finite and greater than the frozen epsilon $10^{-12}$; area-normalized
input is $u_i=y_i/S$ on **all 176** channels, not just the integration band.

| Arm | Spectral input to learner features | Feature count |
| --- | --- | ---: |
| A Raw/Full | All measured $y_i$, no spectral normalization | 176 |
| B Raw/Compact8 | Compact8 of measured $y_i$ | 8 |
| C Area/Full | All $u_i=y_i/S$ | 176 |
| D Area/Compact8 | Compact8 of $u_i$ | 8 |

**Feature standardization is distinct from spectral baseline correction.** The
train-only StandardScaler operates across training examples, independently for
176 wavelength features or eight engineered features. It does not subtract a
physical blank or estimate a per-spectrum baseline. Source code shows **no Ce–ARS
blank subtraction**, no 650–700 nm scalar offset correction and no other spectral
baseline correction in this pilot. Area normalization is the only spectral
normalization. SG is used only inside the approved Compact8 derivative features;
full-spectrum A/C and the other Compact8 features are not additionally smoothed.

### Exact Compact8 definitions and order

For either selected input vector $v=y$ (B) or $v=u$ (D), define
$W=\sum_{i\in B}v_i$, $p_i=v_i/W$ and $\mu=\sum_{i\in B}\lambda_i p_i$.
The band weights must be nonnegative and W finite and greater than $10^{-12}$;
$|v_{84}|$ must exceed $10^{-12}$ for the ratio. There is no extra per-spectrum
normalization before these formulas. Moment weights are **discrete point weights**,
not trapezoidal endpoint weights.

| Position / code name | Exact formula | Unit relative to input |
| --- | --- | --- |
| 1 `A420` | $v_{35}$, exact 420 nm channel | input magnitude |
| 2 `A518` | $v_{84}$, exact 518 nm channel | input magnitude |
| 3 `A420_over_A518` | $v_{35}/v_{84}$ | ratio |
| 4 `centroid_380_580` | $\mu=\sum_{i=15}^{115}\lambda_i p_i$ | nm |
| 5 `spread_380_580` | $\sqrt{\sum_{i=15}^{115}p_i(\lambda_i-\mu)^2}$ | nm |
| 6 `absolute_derivative_area_380_580` | $\sum_{i=15}^{114}\frac{h}{2}(|d_i|+|d_{i+1}|)$ | input magnitude |
| 7 `derivative_450` | $d_{50}$, exact 450 nm channel | input magnitude/nm |
| 8 `slope_440_480` | $\frac{\sum_{i=45}^{65}(\lambda_i-460)v_i}{\sum_{i=45}^{65}(\lambda_i-460)^2}$ | input magnitude/nm |

Here $d_i$ is the Savitzky–Golay first derivative: window length **15**, polynomial
order **2**, derivative order **1**, wavelength spacing/delta **2 nm**, and
polynomial-interpolated boundary windows (`interp` convention). At each interior
point the quadratic fits offsets $t_j=2j$ nm, $j=-7,\ldots,7$; if its coefficients
are a,b,c, the derivative is $b+2ct$. The first/last seven outputs use the first/last
complete 15-point quadratic evaluated at their corresponding edge offsets. The
implementation derives these fixed coefficients from quadratic normal equations;
it does not call a learned transform or fit a classifier. Feature 8 uses an
unsmoothed ordinary least-squares line over 440–480 nm inclusive (21 points), with
an intercept implicit in the centered wavelength formula. Feature 6 integrates
the **absolute** derivative; it is not the absolute signed derivative integral.

## Existing private supplementary diagnostics

The authorized inspection found saved grouped Exp5 holdout predictions at **208
checkpoints** and existing LR coefficient arrays in **208 model checkpoints**.
It prepared private-only figures of held-out condition correctness (all 16
trajectories, no new predictions) and saved coefficient L2 norms (all checkpoints).
Coefficient norms are descriptive of each fitted standardized feature space, not
causal chemical effects or a cross-representation feature-importance comparison.
No private diagnostic values, models, predictions or matrices are published here.

The trusted checkpoint pickles recorded the CLI adapter under `__main__`, so ordinary
loading failed. A tested compatibility Unpickler resolves only that known adapter
name to the existing implementation before restoring saved state; it performs no
fit, predict, transform or spectral computation and does not rewrite the source
pickle. Pickles must be the user-trusted original local artifacts; this is not a
safe loader for arbitrary untrusted files. The optional inspector is never run in CI.

No saved Compact8 training/holdout feature-matrix files were present in the known
run directory. The reproduction record stores raw scenario inputs, not saved
Compact8 matrices; it was not used to generate substitute features. **Compact8
matrix diagnostics are unavailable and were not reconstructed.** No missing
predictions, coefficients or feature matrices were fabricated.

Optional exact command, with variables configured privately and never logged:

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python -m scripts.inspect_measured_pilot_artifacts --source "$PRIVATE_RUN" --output "$PRIVATE_DIAGNOSTICS" --inspect-trusted-pickles
```

Outputs must be a new directory below ignored private storage; public output,
existing output directories and symlinked destinations are rejected. Only the
known run's exact checkpoint filenames are opened; no Exp8 workbook, model or
label artifact is requested. Original private input bytes are checked unchanged.

## Review boundary

This archive preserves observed retrospective results, including unfavorable ones.
It is not proof of physical chemical identity, performance on unseen batches,
model-adaptive experiment selection or superiority over another policy. The current
researcher's reporting instruction supersedes the earlier pause only for these
figures/documentation and bounded saved-artifact inspection. It does not start a
new research phase. Stop at a Draft PR for ChatGPT scientific and code review;
no merge, tuning, retraining, alternate classifier or Exp8 use is authorized.
