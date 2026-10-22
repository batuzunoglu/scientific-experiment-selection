# Exp1–Exp8 evidence reconciliation — scientific review required

Date: 2026-10-22. Local, read-only source audit. No chemical labels, exclusions,
training/test assignments, or source workbooks were changed. No model was trained.
These are observed file/metadata comparisons, not new laboratory results or
simulated measurements. Historical spectral-QC statements are quoted evidence,
not independently rerun QC.

Authority: [Issue #3 latest decision checkpoint](https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6344194970),
with the [retrospective execution/QC audit](https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6342506517).
The checkpoint permits reconciliation and explicitly requires stopping for review.
All four issue comments were read; their text is retained locally in
[issue3_checkpoint.json](audits/2026-10-22-reconciliation/issue3_checkpoint.json).

## Review findings

1. All eight current raw SHA-256 digests match historical workbook provenance.
   All 22 manifest-listed evidence files match their supplied sizes and hashes.
2. Every raw workbook has 96 distinct physical well headings, A1–H12. Only 521
   columns across Exp1–Exp8 contain spectra: 104 pilot/diagnostic and 417 Exp3–Exp8.
   Empty columns remain present and are not interpreted as observed measurements.
3. All 576 draft Exp3–Exp8 coordinates agree with raw spectrum presence and point
   counts. All 11 All6_QC composition conflicts and four historical QC conflicts
   remain unresolved. No additional non-null condition-code disagreements were
   found in the compared per-well metadata sources.
4. Additional discrepancy: Exp7 plan zeros are missing in the uploaded master and
   draft: 201 analyte cells across 69 sample wells, covering N01–N20 and N22–N24.
   N21 has all six nonzero components. This is a missing-versus-explicit-zero
   discrepancy, not evidence of a different preparation. No zero was filled in.
5. All 96 Exp5 controlled metadata rows have `preparation_status=reconstructed`.
   The referenced preparation/final-label workbooks are absent from this package.
   Those references support a historical documentary chain, not independently
   inspected preparation records.
6. `use_in_model=Yes` is not a training split: it includes 46 Exp6 external-test
   and 18 Exp8 external-batch-test wells. No rows are approved for retraining.

## Deliverables and interpretation

- [Per-well discrepancy table](audits/2026-10-22-reconciliation/per_well_discrepancies.csv):
  **768 rows**, all eight plates × 96 coordinates. Includes raw header/range and
  checksum, point counts, planned/analytical layout cell, original master and
  proposed chemistry, replicate claims, each historical variant with workbook
  sheet/row reference, QC reasons, reported execution, source roles, partitions,
  identity status, and unresolved questions. `resolved_label` is deliberately
  empty for every row. JSON-valued CSV columns preserve multiple alternatives.
- [Raw verification](audits/2026-10-22-reconciliation/raw_verification.json) and
  [raw columns](audits/2026-10-22-reconciliation/raw_well_columns.csv) contain every
  hash provenance reference and physical column check.
- [Condition counts](audits/2026-10-22-reconciliation/condition_counts.csv) and
  [counts by historical source/condition](audits/2026-10-22-reconciliation/source_condition_counts.csv)
  distinguish plate coordinates from populated raw columns and source subsets.
- [Plan composition comparisons](audits/2026-10-22-reconciliation/plan_composition_comparisons.csv)
  give 321 exact nonempty condition-code joins to the Exp3–Exp6 historical
  definitions and Exp7 plan. These do not cover absent QC definitions or Exp8
  recipe-only definitions. No ambiguous catalog join was used.
- [Input hashes](audits/2026-10-22-reconciliation/input_hashes.json),
  [comparison checks](audits/2026-10-22-reconciliation/reconciliation_checks.json),
  [additional checks](audits/2026-10-22-reconciliation/additional_checks.json),
  [historical conflicts](audits/2026-10-22-reconciliation/historical_conflicts.json),
  and [catalog duplicates](audits/2026-10-22-reconciliation/catalog_duplicates.json)
  retain the comparison evidence.

Source paths in tables are relative to
`/home/batuhan/research/recovered-experiment-records/metadata-2026-10-22/`.
Workbook references identify original sheet and Excel row/cell; CSV references
identify records including the header (not physical text lines when quoted fields
contain newlines). All source values remain claims. Agreement between inherited
ML labels does not increase the number of independent preparation observations.
Operator statements are available here through the retrospective issue audit,
not a newly inspected original notebook or original conversation transcript.

## Raw integrity and well columns — verified first

Raw root: `/home/batuhan/research/raw-experiment-results/`. Eight files total
685147 bytes. SHA-256 values also match the prior local inventory in
[DATASET_INVENTORY.md](DATASET_INVENTORY.md).

| Raw filename | SHA-256 | Populated | Empty |
| --- | --- | ---: | ---: |
| Exp1 Plt1.xlsx | f41b973b8b96dd6eaef19bf7adf4b17a4cc89914fd0d3c48480df00c5b581079 | 84 | 12 |
| Exp2 Plt2.xlsx | 248c56908c6e8cba5a6d7bb2ddb4861137ea66787057f23bfc873736ecc07d0f | 20 | 76 |
| Exp3 Plt3.xlsx | 4e40ee5e4a5056904f783bfc05bb55cea6888104c5fec0517335710143b6915f | 96 | 0 |
| Exp4 Plt4.xlsx | 68f1a5672f63f02f97e84aaf20892bd312ed6fc83d974e96e3247ee2a7bedb34 | 84 | 12 |
| Exp5 Plt5.xlsx | 0d085b016c2bf4a058d2d8280b68c312654885a035c87eeb9df3f3d7f7a44b84 | 72 | 24 |
| Exp6 Plt6.xlsx | d956d53ab6830827f995cc0780bff7c6908ca281785d9ec073415911994affc6 | 66 | 30 |
| Exp7 Plt7.xlsx | 9808580f38e0c35f97bff3c3f6d6d63831dec86bc47f2e2b0b17166649c2f32d | 78 | 18 |
| Exp8 Plt8.xlsx | 2d41c98a230bd017a13d9bc3e22c2b2812ca1d3efc59772a47a1d4e4631a9f19 | 21 | 75 |

Each workbook has `Sheet1`, headers A1:B1 for wavelength/temperature and C1:CT1
for A1:H12, and 176 wavelength rows, 350–700 at intervals of 2. All populated
well columns contain 176 finite numeric values; no partial spectrum or unexpected,
missing, or duplicate well heading was found. The raw wavelength header itself
does not specify units; historical provenance calls these nm. The temperature
header has the source encoding `Temperature(¡C)`, preserved as-is.

Historical hash anchors: Step0 `File_Provenance` rows 4–9 cover Exp1–Exp6;
Step1 `File_Provenance` rows 2–7 and uploaded master `RAW_FILE_PROVENANCE` rows 2–7
cover Exp3–Exp8; Step2–5 `File_Manifest` rows 4–7 cover Exp3–Exp6.
Thus the older `(1)` filenames can now be linked to the local files by matching
recorded byte digests, not by filename similarity. The historical originals were
not separately present for a second direct byte comparison. Digest equality does
not validate a chemical label or instrument provenance.

The extracted package has 24 files: 22 listed in SHA256SUMS.csv, plus the manifest
and README. The latter two were hashed locally but have no external expected
digest in that manifest. The ZIP itself was not supplied in the scoped directory;
its issue-posted ZIP digest was not checked. Before/after input hashes agree.

## Chemical conflicts — no resolution applied

All6_QC master/Step0/Step1 composition: **TFA 2.5 ppm, other five 1.5 ppm each**.
Alternative in Step2–5 metadata, Exp5 CSV, and draft proposed columns:
**TFA 5 ppm, other five 1 ppm each**. Both total 10 ppm. M24 is separately
documented as the 2.5+1.5 mixture, including Exp4 F10:F12.

| Experiment | Every affected well | Count | Status |
| --- | --- | ---: | --- |
| Exp3 | H9, H10, H11, H12 | 4 | CONFLICT; both recipes retained |
| Exp5 | D10, D11, D12 | 3 | CONFLICT; both recipes retained |
| Exp6 | F5, F6, F7, F8 | 4 | CONFLICT; both recipes retained |

The reported July 21 recipe (50 µL of 100-ppm TFA and 10 µL of each other
100-ppm stock in a 100-µL mixture; 20 µL mixture in a 200-µL final well) calculates
to TFA `100 × 50/100 × 20/200 = 5` ppm and each other analyte
`100 × 10/100 × 20/200 = 1` ppm. This checks the stated dilution arithmetic;
it does not prove that any physical well received those volumes. All 11 remain
QC rather than model-eligible rows in the uploaded master.

Exp5 CSV D10:D12 refers to preparation/final-label worksheet rows 49–51 and
records the generic recipe `10 µL master + 170 µL water + 20 µL prepared PFAS
mixture (All6_QC)`. That per-well text alone does not specify the mixture's internal
recipe. Its component fields favor 5+1, but all preparation statuses are
`reconstructed`. `02_Exp5_Plate_Preparation.xlsx`,
`05_Exp5_Final_Sample_Labels.xlsx`, and the other numbered files named in
`DATA_SCHEMA.md` are not among the supplied files. No independent execution
confirmation was inferred from these unavailable references.

## Four QC disagreements — distinct from chemical identity

| Well | Master/Step0/Step1 and historical QC log | Step2–5 Well_Metadata | Model partition there |
| --- | --- | --- | --- |
| Exp3 G7 | exclude; elevated water-blank baseline | include | qc |
| Exp3 G12 | exclude; abnormal TFA-QC spectrum | include | qc |
| Exp3 H4 | exclude; Ce–ARS-like spectrum | include | qc |
| Exp4 G7 | review; stronger response than companion QC | include | qc |

Master experiment record `QC_Exclusion_Log` rows 8–10 and 13 supply the
corresponding reasons. Four disagreements persist after only comparison-time
alias normalization (`accepted`→`include`, `review_include`→`review`). Original
strings are retained. The claim “likely missing TFA” for Exp3 H4 is historical
spectral inference, not a confirmed chemical identity. These `qc` partitions
do not demonstrate training contamination, nor does this audit establish that
all historical model executions were leakage-free.

## Execution changes and special wells

| Scope | Evidence comparison and retained interpretation |
| --- | --- |
| Exp1 | 84 populated columns A1:G12; H row empty. Step0 has 96 coordinate rows but no condition codes/compositions. Canceled pilot remains excluded historically; no physical labels inferred. |
| Exp2 | 20 populated columns A1:A4, B1:B4, C1:C4, D1:D4, E1:E4. Historical 24-hour delay, diagnostic-only role, A3 spectral-QC exclusion; physical chemical mapping remains incomplete. |
| Exp3 D6/D7 | Historical PFHxA10 preparation concern and review-retain; raw spectra present. No automatic exclusion. |
| Exp3 B4/B5/C9 | July 22 retrospective report says retain for sensitivity analysis; no extra hard exclusions. |
| Exp4 H1:H12 | Reported deliberately unused; raw columns all empty. Absence of data supports the location record, not a chemical concentration of zero. |
| Exp4 F7:F9 | M23 historical exclusion/replacement retained. F7/F8 were suspected; F9 was included in the conservative condition-wide exclusion. All three raw spectra preserved. |
| Exp5 E10:E12 | Historical M23 replacement; TFA/PFPA/PFBA 0, PFHxA3/PFOA3/PFNA4 ppm. They are not ordinary individual-analyte replicates. |
| Exp5 A:F rows | A PFHxA; B TFA; C PFNA; D PFBA; E PFOA; F PFPA. Columns 1–3/4–6/7–9 are 5/10/20 ppm. This differs from Exp3 and is preserved. |
| Exp5 B7/B8/B9, F12 | B7 TFA20 historically excluded; B8/B9 retained; F12 blank retained with review. No current spectra removed. |
| Exp6 physical B12 | B06 replicate, 5-ppm pure TFA, historically excluded. Distinct from condition B12, 15-ppm pure TFA in physical D9:D12. |
| Exp6 D7, E9/E10 | D7 is B11 replicate, historically excluded; E9/E10 are TFA10 QC review wells. Other blind assignments remain unchanged. |
| Exp7 G/H | Original plan reserves all 24 G/H positions as “QC / Blank,” without exact chemistry. Operator report specifies G1:G6 blanks, remaining 18 reserved positions empty. Raw populated/empty columns agree. |
| Exp7 F8/G4 | Historical review-include, not proven preparation errors. N23 is the F8 condition; G4 is a blank location. |
| Exp8 | Plan has 18 A/B samples and G1:G6 blanks. Operator report retains the 18 samples and relocates intended blanks to F1:F3. Raw has exactly those 21 populated columns; G1:G6 empty. F1:F3 remain chemically unresolved and invalid for Ce–ARS reagent baseline, not confirmed DI-only. |

Exp8 sample recipe references: `Exp8_Bridge_Experiment_Plan.xlsx`,
`Bridge Experiment Plan` rows 11–16 (six 10-ppm individual PFAS, three wells each).
Blank recipes in rows 17–18 are planned, not evidence of actual F1:F3 contents.
All 18 Exp8 sample rows lack explicit numeric zeros for other analytes in the
master/draft; all 21 populated Exp8 rows have at least one missing component.
Missing entries remain missing. The six Exp7 blank rows also have incomplete
six-component fields; total populated Exp7 rows with incomplete composition is
75 (69 samples + six blanks). These are distinct from the 11 numeric All6 conflicts.

## Documentary lineage, counts, and split safeguards

The draft CSV and workbook agree after numeric representation normalization.
The uploaded master and Step1 audit agree on all 26 shared metadata fields for
all 576 coordinates. This reproduces the claimed lineage, not independent
verification. The uploaded master's word “Verified” is retained only as source
metadata; this audit certifies no physical chemical label.

| Draft status (unchanged) | Coordinates |
| --- | ---: |
| PROVISIONAL | 381 |
| QC_REVIEW | 12 |
| QC_CONFLICT | 4 |
| CONFLICT | 11 |
| UNUSED_LOCATION_REPORTED | 18 |
| UNUSED_UNCONFIRMED | 141 |
| AS_EXECUTED_LOCATION_REPORTED | 9 |
| Total | 576 |

The 159 unused coordinates are not 159 measured zero-concentration samples.
Exp1/Exp2 add 192 coordinates outside draft scope, including 104 populated columns.
Draft confidence categories describe source claims; reported blank location does
not confirm chemistry. The per-well table keeps identity confidence separate from
raw presence and QC action, with no new training approval.

| Source | Coordinate/record coverage |
| --- | --- |
| Step0 Well_Metadata | 576: 96 each Exp1–Exp6 |
| Each Step2–5 Well_Metadata | 384: 96 each Exp3–Exp6 |
| Step3_Well_Features inherited in Step3/4/5 | 318 each: Exp3 96, Exp4 84, Exp5 72, Exp6 66; includes controls |
| Later Development_Features | 197: Exp3 72, Exp4 69, Exp5 56 |
| External_Exp6_LOCKED | 46, separate external sheet |
| Step1 / uploaded master / draft | 576 each: 96 each Exp3–Exp8 |
| Exp5 controlled CSV | 96, all reconstructed |

Historical roles must be interpreted by analysis task. Step4/5 `Locked_Partitions`
rows 4–7 specify Exp3 individual training (72), Exp5 individual external test (53),
Exp4 mixture training (69) plus Exp5 M23 replacement (3), and Exp6 external mixture
test (46). A later feature workbook groups 197 Exp3–5 rows as development; this
does not authorize treating the older individual-test rows as training. Exp7's
72 `mixture_development_extension` rows and Exp8's 18
`individual_external_batch_test` rows are separate later metadata roles.
The earlier master analysis plan also describes two-direction leave-one-plate-out
validation, whereas the old prediction tables document a specific train/test
direction. Preserve both as distinct historical analysis contexts; choose no new
evaluation design here. Technical replicate wells are not independent batches.

The uploaded condition catalog contains 91 rows and 84 unique codes. Duplicate
codes: CeARS_blank, PFBA_10, PFHxA_10, PFNA_10, PFOA_10, PFPA_10, TFA_10.
Some duplicates differ by missing versus explicit zero fields. Do not join
solely on condition code and multiply records or silently normalize chemistry.

## Reproduction, verification, and preservation

Branch retained: `data/dataset-inventory`; HEAD retained:
`7996a8bfa743f65b6d9589d98419d726c2bccefb`.
Python 3.12.14, standard library only; no dependencies added, no randomness/seeds.
Audit helpers read XLSX ZIP/XML values without saving or recalculating workbooks.
Their limited schema is for these inspected evidence records, not a production
ingestion pipeline. Cached formula values, where present, are historical values;
no Excel recalculation, image/format verification, or validation of historical
model scores was performed. Spectral shape was never used to assign chemistry.

Exact commands from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.inventory --source raw_exports=/home/batuhan/research/raw-experiment-results --output /tmp/issue3-reconciliation/inventory --data-kind researcher-provided
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python docs/audits/2026-10-22-reconciliation/supplement.py /home/batuhan/research/raw-experiment-results /home/batuhan/research/recovered-experiment-records/metadata-2026-10-22 /tmp/issue3-reconciliation-rerun
sha256sum /home/batuhan/research/raw-experiment-results/*.xlsx
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor
git diff --check
git status --short --branch
```

The inventory's output directory must be fresh for another invocation. The final
audit was also run with `docs/audits/2026-10-22-reconciliation` as output; a fresh
`/tmp` destination above is preferred for independent reproduction. The helper
does not alter any input. It writes reports and may replace existing reports in
the explicitly supplied output directory; keep that directory separate from inputs.

Observed: existing **eight tests passed**, doctor exited successfully and reported
`scientific_runs: none`. Logs: [tests](audits/2026-10-22-reconciliation/tests.log),
[doctor](audits/2026-10-22-reconciliation/doctor.log). These tests cover existing
infrastructure and synthetic inventory fixtures, not the scientific correctness
of mappings. The audit separately asserts unique coordinate keys, exact raw
headings/wavelength grid, finite numeric populated cells, historical hash matches,
and unchanged input hashes. No new general-purpose test suite was introduced.
An independent invocation to the stated `/tmp/issue3-reconciliation-rerun` path
produced 12 byte-identical report outputs. Final checks confirmed 768 unique
coordinates, 11 chemical conflicts, four QC conflicts, 69 plan-zero differences,
and no filled resolved labels. All 32 source files retained their starting hashes.
`git diff --check` passed; the Git index remained empty.

Session additions: this report and `docs/audits/2026-10-22-reconciliation/`
(three read-only Python report helpers, source-comment snapshot, CSV/JSON evidence,
raw checksum output and verification logs). Append-only session entries in
`docs/HANDOFF.md`, `docs/DECISIONS.md`, `docs/LEARNING_LOG.md`. Existing inventory
code, tests, data README and inventory report are preserved. No package code,
dependency file, raw workbook, draft map, original master, Git index, branch,
or commit was changed. No stage, commit, push, upload, training or merge occurred.

## Questions for scientific review — no action applied

- What independent preparation evidence can resolve the 11 All6_QC wells? Keep
  both recipes and the 5+1 proposal until reviewed.
- Confirm disposition of the four QC annotation conflicts while preserving the
  accepted QC reasons and alternate historical metadata.
- Should the explicit Exp7 planned zeros be represented as provisional planned
  values in a future curated table? Current missing fields were not replaced.
- Can the actual Exp5 numbered preparation/final-label files and original execution
  evidence be supplied? They are referenced but unavailable here.
- Confirm the intended analysis-specific splits, any future training authorization,
  independent-batch evidence, and a separate backup before controlled import.
  No retraining, split change, or publication approval is assumed.

Stop here for researcher review. No conflicting label has been resolved.
