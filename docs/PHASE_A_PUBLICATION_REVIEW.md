# Phase A final publication scope — 2026-11-08

**Proposed only; nothing staged, committed or pushed.** Latest scientific review:
[Issue #5 comment 6727151818](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6727151818).
Phase A spectral implementation is provisionally accepted as engineering-complete,
conditional on the reported evidence matching local files. This review proposes
publication of exactly these 15 files; explicit publication approval remains pending.

## Exact proposed file list

```text
scientific_experiment_selection/dataset_contract.py
scientific_experiment_selection/raw_spectra.py
scientific_experiment_selection/spectral.py
scripts/smoke_phase_a_exp3_exp5.py
tests/test_dataset_contract.py
tests/test_spectral.py
docs/PHASE_A_PREFLIGHT_REVIEW.md
docs/PHASE_A_REVIEW.md
docs/PHASE_A_PUBLICATION_REVIEW.md
docs/RESEARCH_LAB_NOTEBOOK.md
docs/DECISIONS.md
docs/HANDOFF.md
docs/LEARNING_LOG.md
docs/EXPERIMENT_TEMPLATE.md
docs/superpowers/plans/2026-11-08-phase-a.md
```

Notebook includes unchanged local Entries 007–010 and a new Entry 011 recording
this publication preparation. Existing committed Entries 001–006 remain intact.
Reports contain methods, provenance identifiers and limited aggregate review
results; they do not embed raw spectra, private manifests or per-well diagnostics.
References to local private artifact paths do not include those artifact files.

**Excluded:** every `data/private/**` file; raw XLSX and other raw-data copies;
private candidate manifests (CSV/JSON), local summary/per-well numerical outputs,
logs containing private outputs, `/tmp` review ZIPs/snapshots, caches and environments.
No additional evidence table or historical source data is proposed for publication.
Existing tracked historical audits are dependencies, not newly changed files.

## Final diff / evidence review

Reviewed all three new modules, smoke script, two tests and documentation diffs
relative to HEAD `9f9089f7832aedaadc877a2bfb8e86af90a4ead9`. New files require
`git diff --no-index /dev/null PATH` for review; ordinary `git diff` omits them.
A final complete patch, file list and per-file SHA-256 are retained locally in
`/tmp/phase-a-publication-review-2026-11-08/`. They are not additional commit files.

- Four fixed representations match documented grid, windows and indices; feature
  arithmetic consumes no labels. Errors are branch-specific; Raw/full is preserved.
- Manifest joins on experiment/well and checks hashes/cell ranges/presence. It
  retains missing values, evidence, review/exclusion flags and provisional status.
  No model fitting API or automatic physical-label verification is introduced.
- Synthetic tests cover SG stencil, moments, scaling, guards, provenance, strict
  reader schema, provisional claims/QC, deterministic exports and count-stop behavior.
- Smoke script explicitly selects only Exp3/Exp5 and includes all measured wells.
  It records failures and numerical diagnostics without changing the methods.
  Exp8 was not used for the smoke test or any representation/model choice.

Fresh command:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Observed **32 tests passed**, exit 0 (13 existing, 19 new). These are synthetic/
software tests, including synthetic Exp8 metadata/fixtures, not actual Exp8 access.
Full fresh stdout/stderr is retained with the local publication review evidence.
`git diff --check` and direct notebook append validation are part of final local
verification. No CI execution or model performance is claimed.

Prior observed Exp3/Exp5 smoke evidence was checked against its saved diagnostic
summary/log and module hashes: each of A/B/C/D succeeds for 96/96 and 72/72 measured
wells respectively, failures 0, Exp5 absent locations 24. No signed cancellation
or negative band values; maximum normalized-area error 2.220446049250313e-16.
Exact run commands and limits remain in PHASE_A_REVIEW.md and Entry 010. This
publication preparation does not rerun transformations or open any raw workbook.

## Remaining blockers and follow-ups

**Publication gate:** researcher approval of this precise file scope and final diff.
Work currently remains uncommitted on local main; after approval, use a dedicated
feature branch and the reviewed explicit file allowlist for a PR. Do not directly
push research changes to main. No branch/sync/stage operation was performed here.

No additional implementation failure was observed that blocks a scoped provisional
engineering PR. Known limits should remain visible in its description:
- Signed-area relative cancellation and unit-dependent epsilon policy remain open
  for future signals. Current measured Exp3/5 evidence does not validate all domains.
- Compact8 negative-weight rejection is strict; no clipping policy is approved.
- Manifest/diagnostic output writes are non-atomic; interrupted output directories
  must be preserved/inspected, then a fresh output path used for a retry.
- The smoke script is supported for populated audited Exp3/5 files; it has run
  assertions/repeatability evidence, but no separate synthetic unit-test module.
- Reader supports the audited single-Sheet1 schema; preparation grouping is unknown.

**Separate training gate:** label/well eligibility with uncertainty, preparation
and replicate grouping, CV scheme, concentration task applicability and locked
holdout protocol require scientific sign-off. Exp5 remains reconstructed and
historically exposed. No identities or concentrations are newly verified, and
no method superiority or predictive accuracy is asserted.
