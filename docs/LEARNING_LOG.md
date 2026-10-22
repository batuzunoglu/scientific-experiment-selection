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
