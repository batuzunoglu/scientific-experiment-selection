# Dataset reconciliation review

**Date:** 2026-10-22. **Status:** ready for ChatGPT/researcher scientific review;
no approval to curate labels, import data, train, commit, push or merge.

This report summarizes observed local file and metadata checks, not new laboratory
measurements, simulated spectra, or independently reproduced ML results.
Scope follows [Issue #3 decision checkpoint](https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6344194970).
Detailed evidence: [discrepancy report](WELL_MAP_DISCREPANCIES.md) and
[768-row per-well table](audits/2026-10-22-reconciliation/per_well_discrepancies.csv).

## 1. Exact raw files and checksum results

Source directory: `/home/batuhan/research/raw-experiment-results/`.
Eight files, **685147 bytes**; all SHA-256 values match historical provenance
records and the prior local inventory. No raw file is missing from Exp1–Exp8.

| Exact filename | SHA-256 | Comparison | Populated wells |
| --- | --- | --- | ---: |
| Exp1 Plt1.xlsx | f41b973b8b96dd6eaef19bf7adf4b17a4cc89914fd0d3c48480df00c5b581079 | Match | 84 |
| Exp2 Plt2.xlsx | 248c56908c6e8cba5a6d7bb2ddb4861137ea66787057f23bfc873736ecc07d0f | Match | 20 |
| Exp3 Plt3.xlsx | 4e40ee5e4a5056904f783bfc05bb55cea6888104c5fec0517335710143b6915f | Match | 96 |
| Exp4 Plt4.xlsx | 68f1a5672f63f02f97e84aaf20892bd312ed6fc83d974e96e3247ee2a7bedb34 | Match | 84 |
| Exp5 Plt5.xlsx | 0d085b016c2bf4a058d2d8280b68c312654885a035c87eeb9df3f3d7f7a44b84 | Match | 72 |
| Exp6 Plt6.xlsx | d956d53ab6830827f995cc0780bff7c6908ca281785d9ec073415911994affc6 | Match | 66 |
| Exp7 Plt7.xlsx | 9808580f38e0c35f97bff3c3f6d6d63831dec86bc47f2e2b0b17166649c2f32d | Match | 78 |
| Exp8 Plt8.xlsx | 2d41c98a230bd017a13d9bc3e22c2b2812ca1d3efc59772a47a1d4e4631a9f19 | Match | 21 |

Historical anchors: Step0 `File_Provenance` rows 4–9 (Exp1–Exp6); Step1
`File_Provenance` rows 2–7 and uploaded master `RAW_FILE_PROVENANCE` rows 2–7
(Exp3–Exp8); Step2–5 `File_Manifest` rows 4–7 (Exp3–Exp6).
Historical names with `(1)` match current files by recorded digest, not merely
name similarity. This establishes file linkage, not chemical identity.

All **22 manifest-listed evidence files** match their expected sizes and hashes.
All **32 inputs** (eight raw files plus 24 evidence-package files) retained their
starting hashes. The package README and checksum manifest have local hashes but
no external reference digest; the ZIP itself was unavailable for verification.

## 2. Well matches, missing labels and conflicts

- **768 unique coordinates** inspected: eight plates × 96 headings, A1–H12.
- **521 populated well columns**, each with 176 finite numeric values on the
  350–700 wavelength grid at intervals of 2; no partial spectra or duplicate,
  missing or unexpected well headings.
- **576/576 Exp3–Exp8 draft coordinates match raw presence and point counts**:
  417 populated and 159 empty. All 417 populated coordinates have condition-code
  claims, but those claims are not independently verified chemistry.
- **192 Exp1/Exp2 coordinates are outside draft scope**. Their 104 populated
  columns (84 + 20) lack condition-code/composition assignments in the compared
  historical metadata. They remain canceled-pilot/diagnostic records.
- The per-well table has **351 empty condition claims**: 192 outside draft scope
  plus 159 empty Exp3–Exp8 positions. These are not 351 unlabeled measurements.
- **11 conflicting chemical compositions** and **four conflicting QC actions**
  remain unresolved. No additional non-null condition-code disagreement was found
  among the compared per-well metadata tables. Missing concentrations are counted
  separately below. Every `resolved_label` field is intentionally empty.

## 3. Eleven All6_QC conflicts and four QC conflicts

All6_QC alternative A (uploaded master, Step0/Step1): **TFA 2.5 ppm + each of
the other five analytes 1.5 ppm**. Alternative B (operator-reported July 21 recipe,
Step2–5 metadata, Exp5 CSV, draft proposal): **TFA 5 ppm + each other analyte
1 ppm**. Both total 10 ppm; M24 is separately the 2.5+1.5 mixture.

| Experiment | All affected All6_QC wells | Count |
| --- | --- | ---: |
| Exp3 | H9, H10, H11, H12 | 4 |
| Exp5 | D10, D11, D12 | 3 |
| Exp6 | F5, F6, F7, F8 | 4 |

The reported dilution recipe calculates to 5+1, but actual dispensing into each
well remains unverified. Both alternatives are retained; no correction applied.
All 11 are QC samples with `use_in_model=No` in the uploaded master.

| QC conflict | Historical master/Step0/Step1 action | Step2–5 metadata action |
| --- | --- | --- |
| Exp3 G7, water blank | Exclude: elevated baseline | Include |
| Exp3 G12, TFA10 QC | Exclude: abnormal spectrum | Include |
| Exp3 H4, TFA10 QC | Exclude: Ce–ARS-like spectrum | Include |
| Exp4 G7, TFA10 QC | Review: stronger response than companion QC | Include |

All four have `model_partition=qc` in the intermediate ML metadata. These
annotation conflicts do not establish training contamination. Historical spectral
explanations, including “likely missing TFA,” were not treated as chemical proof.

## 4. Additional discrepancies and cautions

- **Exp7 missing versus zero:** 201 component cells across **69 sample wells**
  are blank in the master/draft where the plan explicitly gives zero. This affects
  N01–N20 and N22–N24; N21 has six nonzero components. No values were filled.
  Including six blank wells, 75 populated Exp7 rows have incomplete compositions.
- **Exp8 incomplete components:** all 18 sample rows lack explicit numeric zeros
  for other analytes; all 21 populated rows have at least one missing component.
  F1:F3 remain intended blanks of unresolved chemistry, invalid for Ce–ARS reagent
  baseline. They are not confirmed DI-only. Planned G1:G6 are empty in raw data.
- **Exp5 evidence gap:** all 96 CSV preparation rows say `reconstructed`.
  Referenced numbered preparation/final-label workbooks are absent from the
  supplied package, so their cited rows cannot be independently checked here.
- **Catalog join risk, confirmed:** 91 catalog entries represent 84 unique codes.
  Seven duplicates are CeARS_blank and the six individual PFAS `_10` codes;
  missing-versus-zero differences must not be silently normalized.
- **Inherited validation claims:** master and Step1 agree across all 26 shared
  fields and 576 rows. This is lineage consistency, not independent preparation
  validation. The source word “Verified” was not adopted as our conclusion.
- **Split risk, preserved:** `use_in_model=Yes` includes 46 Exp6 external-test and
  18 Exp8 external-batch-test rows. Exp5 also has task-dependent individual-test
  and M23 mixture-training roles. No split or training eligibility was changed.

Known execution/QC exceptions remain documented: Exp3 D6/D7 review-retain;
Exp4 H row unused and F7:F9 replaced by Exp5 E10:E12; Exp5 B7 excluded historically;
Exp6 physical B12/B06 and D7/B11 excluded historically; Exp7 F8/G4 review-retain.
Physical well B12 is not condition code B12. All raw spectra remain intact.

## 5. Files, tests and limitations

**Reconciliation additions:** `docs/WELL_MAP_DISCREPANCIES.md` and the following
files under `docs/audits/2026-10-22-reconciliation/`:

- Helpers: `inspect_sources.py`, `reconcile.py`, `supplement.py`.
- Tables: `per_well_discrepancies.csv`, `raw_well_columns.csv`,
  `condition_counts.csv`, `source_condition_counts.csv`,
  `plan_composition_comparisons.csv`.
- Evidence/checks: `input_hashes.json`, `raw_verification.json`,
  `reconciliation_checks.json`, `additional_checks.json`,
  `historical_conflicts.json`, `catalog_duplicates.json`, `source_counts.json`,
  `issue3_checkpoint.json`, `raw_sha256sum.txt`.
- Execution logs: `tests.log`, `doctor.log`.

Append-only reconciliation entries were added to `docs/HANDOFF.md`,
`docs/DECISIONS.md`, and `docs/LEARNING_LOG.md`. This review-packaging follow-up
creates **`docs/DATASET_RECONCILIATION_REVIEW.md`** and appends a handoff and decision
note. Existing uncommitted inventory work remains preserved, including
`data/README.md`, `docs/DATASET_INVENTORY.md`,
`scientific_experiment_selection/inventory.py`, and `tests/test_inventory.py`.
No existing package code, dependency, label table or raw workbook was edited.

**Observed checks from the completed reconciliation:** eight existing tests
passed (two infrastructure, six synthetic inventory tests); doctor passed and
reported `scientific_runs: none`; `git diff --check` passed. Twelve report outputs
were byte-identical on rerun. Assertions checked 768 unique coordinates, raw
headings/grid/numeric values, matching source hashes, 11 chemical conflicts,
four QC conflicts, 69 plan-zero differences, and empty resolved-label fields.
These are software/documentary checks, not scientific label validation.
This documentation-only follow-up reads those logs; it does not claim a new
test-suite or reconciliation execution.

Exact runnable commands from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/audits/2026-10-22-reconciliation/supplement.py /home/batuhan/research/raw-experiment-results /home/batuhan/research/recovered-experiment-records/metadata-2026-10-22 /tmp/issue3-review-independent-rerun
git diff --check
```

Use a separate output directory for reports. Python 3.12.14, standard library;
no randomness or dependencies added. Workbook values were read without saving or
recalculating Excel files. The helpers target these inspected schemas rather
than providing a general-purpose importer. Original preparation notebooks and
some cited source workbooks are missing; operator reports are available through
a retrospective issue audit. Backup confirmation, physical label validation,
independent-batch evidence and analysis-specific split approval remain open.
No historical performance claim or absence of leakage was independently validated.

**Review gate:** request scientific review of both All6 alternatives, the four QC
actions, missing-versus-zero handling and preparation provenance before curation.
Branch remains `data/dataset-inventory`; no staging, commit, push, upload, training,
split change or merge was performed. Raw data were not modified.
