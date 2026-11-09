# Learning Journal

## 2026-10-21 — Inventory versus scientific validation

- SHA-256 fingerprints exact file bytes. Matching hashes identify byte duplicates,
  not independent experimental replicates or scientifically interchangeable samples.
- Filename evidence can suggest an experiment ID; it cannot establish a preparation
  batch or plate without supporting records. Conflicting/absent mappings stay unknown.
- Absence of a filename match does not prove a physical experiment is missing.
  A verified expected-batch roster is necessary to assess batch completeness.
- Read-only inventory precedes import: collect paths, sizes and fingerprints first,
  then have the researcher review relevance, mapping, backup and storage choices.
- Eight software tests passed using temporary synthetic byte fixtures; no observed
  or simulated spectra were produced. Commands and limitations are recorded in
  `docs/DATASET_INVENTORY.md` and `data/README.md`.

## Lesson template
- Date / topic:
- What problem does this concept solve?
- Plain-language explanation:
- Definition / assumptions / equations:
- Concrete example in spectroscopy:
- Files and commands involved:
- What I predicted / what actually happened:
- How would I explain it to another researcher?
- Questions to revisit:

## 2026-10-21 — Workflow verification

- The initial uv commands could not run Python because the sandbox prevented writing to the existing uv cache. Approved retries of the same commands passed: the doctor exited 0 and the unittest suite reported 2 tests, OK.
- These observed infrastructure checks verify basic execution, not scientific validity. No scientific measurements were produced or simulated.
- The default `gh issue view` query failed on a deprecated Projects field; requesting explicit JSON fields retrieved Issue #1 successfully.
- Exact commands and observed outputs are recorded in `docs/WORKFLOW_TEST.md`. The researcher approved the local diff and publication; connected-repository review remains untested.


## 2026-10-22 — File recovery is not condition validation

All eight source files were inventoried read-only; Exp8 matches the recovered
attachment's documented SHA-256. Matching bytes confirm the file reference, not
analyte identity, concentration, blank status or QC. Those require independent
lab records keyed to plate/well and source file. No separate mapping file was
found in the source directory; workbook contents were not inspected. Exp numbers
and replicate labels do not prove batch independence. Eight software tests passed
on synthetic bytes/infrastructure; no scientific results or simulations produced.
Exact inventory evidence and commands: `DATASET_INVENTORY.md`, 2026-10-22 entry.

## 2026-10-22 — Separate raw presence, chemistry, QC and historical roles

- A well heading is not a measurement: the eight files each have all 96 headings,
  but only 521 columns have numeric spectra. Empty columns do not imply 0 ppm.
- Matching hashes now link local raw exports to historical `(1)` filename records.
  Matching ML labels establish propagated metadata, not independent physical truth.
- Both All6 alternatives total 10 ppm. Total-concentration checks cannot detect
  the TFA5+five×1 versus TFA2.5+five×1.5 distinction. Reported dilution arithmetic
  favors 5+1 but does not prove what was pipetted into each conflicting well.
- Explicit zero and missing concentration must remain different: 69 Exp7 samples
  have 201 planned zeros missing in the master/draft. No imputation was performed.
- A valid or excluded spectrum and a correct chemical identity are separate
  questions. Historical QC inference was not converted into chemical proof.
- `use_in_model=Yes` includes held-out records. Technical wells and source copies
  are not independent batches or independent validation evidence.
- Eight existing software tests and doctor passed. Report rerun was byte-identical
  for 12 outputs; input checksums stayed unchanged. These observed audit checks
  do not validate physical preparation, model performance or historical leakage.
- Full sources, limitations, proposed review questions and commands:
  [WELL_MAP_DISCREPANCIES.md](WELL_MAP_DISCREPANCIES.md). Stopped for scientific review.

## 2026-11-08 — Approved transforms and the independent-evidence gate

- Raw/full preserves all 176 intensities. Area/full divides them by the same
  per-well 380–580 nm integral, preserving relative shape but removing magnitude
  that could be informative for concentration. Compact8 replaces the full curve
  with eight fixed summaries; using it on Raw versus Area tests a separate factor.
  These comparisons are approved, but no superiority has been observed here.
- All three requested raw-file hashes match in fresh checks. This confirms the
  referenced files, not well chemistry. All 96 Exp5 preparation records remain
  reconstructed; referenced preparation and final-label workbooks were absent
  from the inspected recovered-records directory.
- The latest issue explicitly makes missing independent chemistry evidence a
  stop condition. Consequently no representations or candidate manifest were
  built. See `PHASE_A_PREFLIGHT_REVIEW.md` for exact checks and Notebook Entry 007
  for the reason and pending review. No new measurements, simulations or ML runs.

## 2026-11-08 — Provisional labels can coexist with verified software

Scientific review 6726841885 clarified the previous stop: missing preparation
records prevent calling labels verified, but do not prevent testing functions of
a spectrum. Manifest counts 72/53/18 mean historical claims/presence/QC rules agree;
they do not prove what was dispensed. Every physical-label verification flag is false.

Raw/full keeps amplitude and shape. Area/full removes total magnitude using each
well's own 380–580 nm integral; it may discard concentration information. Compact8
compresses either curve into fixed summaries. Comparing these factors separately
avoids assuming one pipeline helps identity and concentration equally. SG derivatives
use a fixed local polynomial filter, not supervised training. The 15-point impulse
test checks the exact window, whereas polynomial tests alone cannot distinguish
several different derivative methods.

Numerical invalidity is separate from chemical QC: a near-zero denominator yields
a branch error, not a silently repaired curve or a new physical exclusion. Negative
moment weights are flagged rather than clipped. No experimental failure rates or
model performance were computed. 32 software tests passed; new spectra are synthetic
fixtures only. Details and exact commands: `PHASE_A_REVIEW.md`; Notebook Entry 008.

## 2026-11-08 — Numerical execution versus chemical validity

All four fixed representations run successfully on every measured Exp3/5 well,
including excluded and review wells. This shows numeric compatibility, not that
excluded preparations are valid or that normalization improves prediction.
Signed area can be small because positive/negative signals cancel; comparing its
magnitude with integrated absolute signal diagnoses that risk without altering
the method. Here the ratio was 1 for all 168 spectra and no band intensities
were negative. Current denominators exceed numerical epsilon by many orders of
magnitude, but future near-zero/noisy data and thresholds still need review.
Notebook Entry 010 and PHASE_A_REVIEW.md record exact observations/commands.

## 2026-11-09 — Selecting before measuring

Uncertainty based on a not-yet-measured spectrum is unavailable for a true
next-measurement decision unless a separately validated surrogate or explicitly
costed screening step supplies it. Random and nominal factor-level coverage can
work on prospective settings alone. The synthetic MVP therefore blocks uncertainty
execution, keeps hidden outcomes in the oracle, and counts complete shared-solution
conditions rather than individual technical wells as acquisitions. A fixed separate
holdout is evaluator-only; changing its labels must not alter actions. Fake-adapter
curves test information flow and accounting, not chemical accuracy or policy superiority.
