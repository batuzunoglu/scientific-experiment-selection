# Experiment and Computational Run Template

- Run ID and timestamp:
- Research question and hypothesis:
- Performed by / equipment:
- Real laboratory observation OR retrospective replay OR synthetic simulation? (choose one):
- Data source filenames, checksums and batch metadata:
- Plate, replicate, blank, standard, QC information:
- Protocol, experimental concentrations and units:
- Action candidate set and budget/cost:
- Git commit / locked software environment / hardware:
- Exact command and config / seed:
- Training/validation/test partition and leakage prevention:
- Observed outputs, metrics, uncertainty and figures:
- Interpretation, limitations and alternative explanations:
- Paper-ready observation and evidence link:
- Next action:

## Run record — phase-a-provisional-2026-11-08

- Question: can provisional evidence be represented reproducibly while testing the
  approved label-independent A–D functions without asserting verified chemistry?
- Kind: observed file/metadata audit plus artificial synthetic unit tests; no physical
  experiment, calibrated simulation, training or evaluation.
- Code base: HEAD `9f9089f7832aedaadc877a2bfb8e86af90a4ead9` plus uncommitted local
  Phase A modules; Python 3.12.14, standard library, deterministic/no random seed.
- Exact commands, source/output SHA-256 values and numerical configuration:
  [PHASE_A_REVIEW.md](PHASE_A_REVIEW.md). Output directory must be fresh.
- Outputs: local ignored `data/private/phase-a-2026-11-08-final/` candidate JSON/CSV
  and summary. Three files byte-identical to the final `/tmp` rerun. 72/53/18
  candidate counts; all 288 physical-label flags false; 32 software tests passed.
- Split/leakage: no folds or models; Exp5 historically exposed, Exp8 locked; no
  experimental A–D outputs or feature statistics computed. Technical grouping is a
  condition proxy, with preparation independence unknown.
- Limitation: consistency and numerical tests do not validate physical preparation,
  historical labels or predictive performance. Next: scientific review only.

## Run record — phase-a-exp3-exp5-smoke-2026-11-08

- Authority: Issue #5 comment 6727098915 plus explicit researcher instruction.
- Kind: observed numerical validation on historical measured Exp3/5 spectra;
  no new measurements, simulations, supervised fitting or label validation.
- Exact commands/config/source hashes: appended `PHASE_A_REVIEW.md` smoke section.
- Python 3.12.14, unchanged phase-a-v1 methods/epsilon 1e-12, no randomness.
- A/B/C/D successes: Exp3 96 each; Exp5 72 each. Failures 0. Empty Exp5 columns 24.
- Diagnostics: no signed cancellation or negative band values; normalized-area
  errors <=2.22044605e-16. Both artifacts byte-identical on repeat, input hashes
  unchanged. Exp8 excluded from run entirely.
- Artifacts: `data/private/phase-a-smoke-exp3-exp5-2026-11-08/` (ignored, local only).
- Next: scientific review; no method-policy changes or scientific sign-off inferred.
