# Provisional Phase A review — 2026-11-08

**Local implementation complete; scientific/data eligibility and split sign-off pending.**
Authority: [scientific review comment 6726841885](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6726841885)
and the researcher's explicit request to continue provisionally. Missing independent
Exp5 preparation records block chemical verification, not label-independent software.
The earlier preflight report and Notebook Entry 007 remain unchanged.

## What was verified

- Exact Exp3/5/8 raw file SHA-256 matches the tracked October manifest (full digests below).
- Each raw workbook has 96 ordered physical wells and exact 350:2:700 nm grid.
  Populated wells have 176 finite numbers; empty columns remain absent measurements.
- 22 evidence-package files match their supplied size/hash manifest. All 28 read inputs
  (3 raw, 22 bundle files, bundle manifest, raw checksum list, reconciliation CSV)
  retained their hashes through each run. Package-manifest authenticity itself is not
  independently established by hashing the manifest.
- All 288 raw coordinates match the versioned reconciliation table's hashes, cell ranges,
  numeric-point counts and presence. That table supplies historical claims, not truth.
- Two final manifest runs produced byte-identical JSON, CSV and summary files.
- **32 tests passed:** 13 existing, 9 spectral synthetic tests, 10 contract/reader tests.
  Python 3.12.14, standard library only; no dependencies added and no randomness.

| Batch / source | Populated wells | Candidate included | Other coordinates | Candidate warnings |
| --- | ---: | ---: | ---: | --- |
| Exp3 Plt3.xlsx | 96 | 72 | 24 | 72 unverified labels/unknown preparations; D6/D7 retain QC review |
| Exp5 Plt5.xlsx | 72 | 53 | 43 | All 53 reconstructed, unverified, historically exposed; original preparation records missing |
| Exp8 Plt8.xlsx | 21 | 18 | 78 | All 18 unverified, missing other-component claims, locked pending exposure audit |

“Other coordinates” includes empty locations, not just excluded measurements.
All 288 rows have `physical_label_verified=false` and `training_authorized=false`.
Preparation status is derived from recorded variants: Exp3/8 unknown, all 96 Exp5
rows reconstructed. Missing/conflicting statuses are explicitly flagged by the code.

Candidate class/concentration counts: Exp3 has four wells per each of six PFAS ×
5/10/20 ppm; Exp5 has three per combination except TFA20 has two (B7 excluded);
Exp8 has three per each of six PFAS, all claimed 10 ppm. These are documentary
consistency checks, not chemically verified concentrations or independent replicates.

Exact physical candidate sets:
- Exp3: A1:F12, retaining D6/D7 review flags.
- Exp5: rows A:F, columns 1:9, except B7; E10:E12 remain mixture repeats outside this task.
- Exp8: A1:A12 and B1:B6. F1:F3 remain unresolved invalid reagent blanks; G1:G6 empty.

All historical variants, conflicting recipes/QC actions, source references, unresolved
questions and blank component fields survive in `source_evidence` in the JSON.
Seven conflict-flagged Exp3 and three conflict-flagged Exp5 coordinates are retained
outside the candidate set; no All6/QC disagreement is adjudicated. Exp4/6 conflicts
remain in the unchanged original audit, outside this three-batch manifest.

All-coordinate QC counts (include / review / exclude / unused): Exp3 91/2/3/0;
Exp5 70/1/1/24; Exp8 18/0/3/75. The summary JSON lists warnings by batch, source,
QC and proposed batch role, and separately for candidates. `proposed_role` is a
batch-level role, including on excluded locations; only `candidate_included`
indicates candidate membership. No actual evaluation folds are created.

## Reviewable local artifacts

Under `data/private/phase-a-2026-11-08-final/` (already Git-ignored):

- `candidate_wells.csv`: compact 288-row review table with provenance references.
- `candidate_wells.json`: same rows plus complete historical reconciliation evidence.
- `summary.json`: input hashes, counts, warnings and run environment.

No artifact contains raw absorbances or derived experimental features. JSON manifest
SHA-256: `619f1e73df3e6bb4930ed77906c0dc17156787ea60f7d3e085ab03ebb13990f3`.
CSV SHA-256: `0ebe9525277ca0f35ca3509efb75bd2fcad022b810ef126fd89464b1f8bee471`.
The earlier `data/private/phase-a-2026-11-08/` is an intermediate implementation
run, superseded by `-final`; retained locally, not a source or final review artifact.

| Raw file | SHA-256 |
| --- | --- |
| Exp3 Plt3.xlsx | `4e40ee5e4a5056904f783bfc05bb55cea6888104c5fec0517335710143b6915f` |
| Exp5 Plt5.xlsx | `0d085b016c2bf4a058d2d8280b68c312654885a035c87eeb9df3f3d7f7a44b84` |
| Exp8 Plt8.xlsx | `2d41c98a230bd017a13d9bc3e22c2b2812ca1d3efc59772a47a1d4e4631a9f19` |

## What each representation means

| Branch | Output | Purpose |
| --- | --- | --- |
| A Raw/full | 176 unchanged numeric intensities | Required intensity-and-shape control |
| B Raw/Compact8 | 8 fixed spectral summaries | Test compression without normalization |
| C Area/full | 176 intensities divided by one per-well area | Test removal of overall magnitude |
| D Area/Compact8 | 8 summaries of the normalized curve | Test normalization plus compression |

Area is the signed trapezoidal integral over **380–580 nm inclusive**, with 2 nm
spacing; every original 350–700 nm value is divided by it. Neither baseline nor
blank subtraction is applied. Area normalization can remove concentration signal;
passing tests does not imply it helps either analytical task.

Compact8, in fixed order:
1. Intensity at 420 nm.
2. Intensity at 518 nm.
3. Ratio of those intensities.
4. Discrete intensity-weighted centroid: `sum(wavelength*y)/sum(y)` over 101 samples,
   380–580 nm inclusive.
5. Square root of the discrete weighted variance around that centroid.
6. Trapezoidal integral of the absolute SG first derivative over 380–580 nm.
7. SG first derivative at 450 nm.
8. Ordinary least-squares slope (with intercept) on the **unsmoothed representation**
   at the 21 points 440–480 nm inclusive.

Derivative: fixed Savitzky–Golay window 15, degree 2, first derivative, spacing 2 nm.
Implemented using symmetric quadratic normal equations, equivalent to fixed filter
weights; first/last seven outputs evaluate the first/last 15-point polynomial
(no padding). This is signal processing, not a trained model. Derivative features
use interior points; the edge convention is documented and synthetically tested.
No smoothing is applied to the intensity, centroid, spread or slope inputs.

Centroid/spread use discrete sums, whereas areas use trapezoids. These exact
numerical conventions are **implementation choices for scientific review**; the
historical named definitions and SG settings are approved, but exact reproduction
of an archived historical feature matrix is not claimed. We did not compare
experimental feature statistics or historical performance to choose conventions.

Guards (`epsilon=1e-12`, configurable in the API): require finite 176-value input,
exact grid, positive area above epsilon, absolute ratio denominator above epsilon,
and positive moment sum above epsilon. Compact8 rejects negative weights within
380–580 nm rather than clipping them or claiming probability-like moments are
physical; Area/full can still succeed on a signed curve with positive area.
Nonfinite/overflowing derived outputs are failures. Epsilon is a numerical guard,
not an instrument detection limit or scientifically validated QC threshold.
The same numeric tolerance applies in each branch's units; sensitivity to it
requires review before real feature use. No experimental rejection rates were computed.

Each branch returns values or an explicit error. Valid Raw/full survives derived
branch failures. Provenance is deep-copied unchanged and carried separately from
features; version `phase-a-v1` and epsilon are recorded. Labels, concentration,
well ID, batch and QC do not enter the transformation arithmetic.

`technical_replicate_group=batch:condition` is a conservative grouping proxy;
`preparation_group=UNKNOWN` and `group_independence_verified=false`. Matching
condition codes are not proof of a single preparation or independent preparations.
No training/split authorization is inferred from grouping or candidate status.

## Exact commands and observed execution

From the repository root, the final manifest run was:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.dataset_contract --raw-root /home/batuhan/research/raw-experiment-results --evidence-csv docs/audits/2026-10-22-reconciliation/per_well_discrepancies.csv --raw-checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt --evidence-root /home/batuhan/research/recovered-experiment-records/metadata-2026-10-22 --output data/private/phase-a-2026-11-08-final
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.dataset_contract --raw-root /home/batuhan/research/raw-experiment-results --evidence-csv docs/audits/2026-10-22-reconciliation/per_well_discrepancies.csv --raw-checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt --evidence-root /home/batuhan/research/recovered-experiment-records/metadata-2026-10-22 --output /tmp/phase-a-2026-11-08-final-rerun
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Both output directories now exist; use a **fresh** output path for another run.
The CLI refuses existing or overlapping input/output directories, hash/schema/
presence mismatches, duplicate evidence coordinates, or unexpected candidate counts.
Contradictory explicit condition/component claims are flagged and withheld from
candidate inclusion, without resolving either claim. Missing components stay missing.

Synthetic API example (no experimental data):

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PY'
from scientific_experiment_selection.spectral import GRID, representations
result = representations(GRID, [2.0]*176, {'data_kind': 'synthetic'})
print({branch: len(result[branch]['values']) for branch in 'ABCD'})
print('Synthetic area:', result['area_factor'])
PY
```

Expected shapes A/B/C/D: 176/8/176/8; constant-2 synthetic area: 400.
The tests exercise those outputs. No experimental A–D feature generation was run.

Tests cover raw preservation, known area/window, normalized scaling, moments,
analytic linear/quadratic derivatives and exact 15-sample impulse response,
invalid grids/values/denominators, independent branch failures and provenance copies;
synthetic XLSX/schema errors, metadata/QC/lock flags, missing values, duplicate keys,
hash/output safety, evidence-driven preparation status, and end-to-end deterministic
288-coordinate exports with count mismatch stopping before output creation.

Negative development outcomes: initial test imports failed because new modules did
not yet exist; two regression assertions exposed missing condition/component warning
and batch-hardcoded preparation status. Both were fixed and the full suite passed.
No failures are being presented as scientific results.

## Files changed and remaining limitations

New code: `scientific_experiment_selection/spectral.py`, `raw_spectra.py`,
`dataset_contract.py`. New tests: `tests/test_spectral.py`, `tests/test_dataset_contract.py`.
New docs: this report and `docs/superpowers/plans/2026-11-08-phase-a.md`.
Appended: `docs/RESEARCH_LAB_NOTEBOOK.md` Entry 008, `docs/HANDOFF.md`,
`docs/LEARNING_LOG.md`, `docs/DECISIONS.md`, `docs/EXPERIMENT_TEMPLATE.md`.
Local ignored artifacts are listed above. Earlier Entry 007/preflight notes are
preserved; `docs/PHASE_A_PREFLIGHT_REVIEW.md` remains an existing untracked file.
No dependency, original evidence table or raw-file edits.

Observed results are software/file checks; synthetic curves are test fixtures,
not simulations calibrated to chemistry or new laboratory measurements. Actual
physical identities, concentrations, preparation independence, eligibility and
split protocol remain unverified/unapproved. Exp5 remains historically exposed;
Exp8 remains locked pending exposure audit. The reader intentionally supports
only the audited raw XLSX schema. Reconciliation evidence is inherited and hashed,
not a new independent audit of every original worksheet claim.

Current checkout and existing local notes were preserved without syncing/stashing;
HEAD stays `9f9089f7832aedaadc877a2bfb8e86af90a4ead9` on local main, all work unstaged.
No model training, predictions, evaluation, chemistry resolution, raw upload,
commit, push or publication. Stop for scientific review of this local result.

Final local documentation checks: `git diff --check` passed; the notebook checker
`valid_append` function passed against the saved pre-continuation notebook,
confirming Entry 007 and all earlier bytes remain intact. Git index is empty and
final artifacts are ignored. The PR-oriented checker CLI compares committed refs,
so its no-change result does not validate an uncommitted diff; the local function
check was used for that purpose. The synthetic API example above was also executed:
176/8/176/8 shapes and area 400.0 observed. All 28 input hashes were rechecked once
more after documentation and remained unchanged.

## Limited measured-spectrum smoke test — 2026-11-08

This new run supersedes earlier **not run** statements only for Exp3/Exp5
transformation smoke testing. Prior implementation and preflight history is retained.
Read [ChatGPT code review 6727098915](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6727098915),
which conditionally accepts the engineering foundation and requests this test before
scientific sign-off. The researcher authorized this limited run. No methods or
numerical thresholds were changed; relative cancellation was measured diagnostically.

| Source | Measured wells | A Raw/full | B Raw/Compact8 | C Area/full | D Area/Compact8 | Branch failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Exp3 | 96 | 96 | 96 | 96 | 96 | 0 |
| Exp5 | 72 | 72 | 72 | 72 | 72 | 0 |

All populated wells were processed without loading labels or QC metadata, including
review/excluded/QC/blank/mixture wells. Exp3 D6/D7 and Exp5 B7/E10:E12 therefore
participated; successful transforms do not change their historical eligibility.
Exp5 G1:H12 (24 locations) have no recorded spectra: skipped as absent, not failed
transforms or zero-valued samples. No failing physical well IDs/reasons exist.
Every successful branch has the expected 176/8/176/8 dimensions and finite values.
Raw/full equals its numeric source spectrum exactly; returned provenance matches.
Only Exp3 and Exp5 raw workbooks were opened. Exp8 was not opened, transformed,
rehashed or otherwise used in this validation. The checksum list was read as text,
selecting only the two authorized filenames. No candidate manifest was loaded.

Numerical diagnostics across all measured wells:

| Diagnostic | Exp3 | Exp5 |
| --- | --- | --- |
| Signed 380–580 nm area range (absorbance·nm) | 5.9882–46.9998 | 25.6058–36.297 |
| `abs(signed area)/integral(abs(signal))` | 1 for all 96 | 1 for all 72 |
| Wells with negative band intensity | 0 | 0 |
| Minimum absolute raw A518 | 0.0289 | 0.0874 |
| Minimum absolute normalized A518 (nm⁻¹) | 0.00339648305 | 0.00341328918 |
| Minimum raw moment sum | 3.0257 | 12.9118 |
| Minimum normalized moment sum | 0.504097089 | 0.504098436 |
| Maximum normalized-area error from 1 | 2.22044605e-16 | 2.22044605e-16 |
| Maximum relative reconstruction error | 1.45469474e-16 | 1.44485037e-16 |
| Max C / D difference after positive ×2 arithmetic rescaling | 0 / 0 | 0 / 0 |

Reconstruction diagnostic is `max(abs(normalized*area - raw))/max(abs(raw))`.
Rescaling is a numerical consistency probe of the same data, not an additional
measurement or concentration experiment. Full-precision diagnostics per well and
aggregate ranges remain in ignored local files. No full spectra or feature vectors
were exported. Area/absolute-area=1 shows no signed cancellation in this band for
these files. A descriptive relative-area threshold of 1e-6 flagged zero wells;
it does not change eligibility and is not a newly approved guard. Both raw and
normalized Compact8 denominators exceed the unchanged absolute epsilon=1e-12
by many orders of magnitude. Strict negative-weight rejection was not triggered.

Limitations: this run cannot establish behavior under sign-changing/noisy/near-zero
future signals, tolerance suitability in different units, physical preparation,
chemical validity, predictive performance, or a preferred representation. The
review's relative guard concern remains open for future scientific policy review;
no guard was added or relaxed to obtain these counts. Exp5 labels remain
reconstructed and historically exposed. Atomic-output reliability, preparation
independence, eligibility and split decisions remain unresolved. No model fit or
prediction, chemistry resolution, blank subtraction, clipping or normalization
policy change occurred. These are observed computations on previously measured
spectra, not new laboratory measurements or chemistry simulations.

Exact commands from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python scripts/smoke_phase_a_exp3_exp5.py --raw-root /home/batuhan/research/raw-experiment-results --checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt --output data/private/phase-a-smoke-exp3-exp5-2026-11-08
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python scripts/smoke_phase_a_exp3_exp5.py --raw-root /home/batuhan/research/raw-experiment-results --checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt --output /tmp/phase-a-smoke-exp3-exp5-rerun-2026-11-08
```

Both exited 0. Existing destinations require a fresh output path on future runs.
The second command's full stdout/stderr/exit code is saved in the first output
folder's `execution.log`; both `summary.json` and `per_well_diagnostics.csv` were
byte-identical between runs. The script asserts branch shapes/finiteness, raw
passthrough, unchanged provenance and before/after raw/module hashes. No new
synthetic unit-test result is claimed for this diagnostic script; prior 32-test
record remains historical. Standard-library Python 3.12.14, no randomness.

Raw hashes before/after match the prior recorded Exp3/5 hashes above. Existing
`spectral.py`, `raw_spectra.py`, `inventory.py` remained unchanged; their hashes are
in the diagnostic summary. Changed this session: new orchestration script
`scripts/smoke_phase_a_exp3_exp5.py`; appended review report, Notebook Entry 010,
handoff, learning and run records. Original spectra and approved implementations
were not edited. Stop for scientific review; no staging, commit or push.
