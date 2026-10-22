# Cross-LLM Research Handoff

**Checkpoint date:** 2026-10-22
**Phase:** Actual Exp1–Exp8 inventory and evidence reconciliation completed; scientific conflicts remain open.
**Status:** Sources found at `/home/batuhan/research/raw-experiment-results/`; inventory code, tests and provisional reports committed as `4a83e74` and pushed on `data/dataset-inventory`. [PR #4](https://github.com/batuzunoglu/scientific-experiment-selection/pull/4) is open and unmerged. Eight software tests and doctor passed; no model training or raw-workbook import performed. Backup confirmation remains pending. Housekeeping follow-up awaits approval before further push or merge.

The dated checkpoints below are historical records; their earlier pending-source
and publication-hold statements describe the state at those checkpoints.

## Stable goals
Reproducible ECE PhD research, paper/proposal, and a publicly presentable portfolio for 2027 internship applications. Core task: sequential physical experiment selection to adapt/verify predictive scientific models under shift, using PFAS spectroscopy first.

## Checkpoint 002 — Phase 1 tooling; awaiting sources

- Date: 2026-10-21; Ubuntu/Linux; Python 3.12.14.
- Branch: `data/dataset-inventory`, created from freshly fetched `origin/main` at
  `7996a8bfa743f65b6d9589d98419d726c2bccefb`; initial tree clean.
- Read Issue #3 through the connected GitHub integration and all required project guidance.
- Added read-only inventory CLI, six synthetic integration tests, metadata guidance
  and review record. See `docs/DATASET_INVENTORY.md` for changed files, exact commands,
  observed outcomes and limitations; `data/README.md` for the executable usage template.
- Verification: baseline 2 tests; test-first 6 inventory failures before implementation;
  final 8 tests passed; doctor exit 0; whitespace check exit 0.
- GitHub repository independently verified private. `.gitignore` unchanged.
- Actual data manifests/checksums: none. Source paths, separate backup confirmation,
  authoritative mappings and expected batch roster still needed.
- Synthetic fixtures are arbitrary bytes, not spectra. No scientific conclusions.
- Changes remain local and unstaged. Do not commit, push, open a PR or upload raw files
  until the researcher reviews the inventory and explicitly approves.
- Next single task: obtain exact source directories and backup confirmation, run the
  inventory there, and present actual file list/sizes/mapping uncertainties for review.

## What currently exists
- Markdown operating protocol and scientific charter.
- A minimal Python package with a `doctor` diagnostic.
- Standard-library smoke tests and locked baseline environment (no third-party runtime dependencies).
- No raw PFAS data have been copied into the project.

## Initial Ubuntu verification checklist (completed, see Checkpoints 000–001)
1. Git repo clone and correct private remote.
2. `uv sync --locked` succeeds.
3. `uv run python -m scientific_experiment_selection doctor` succeeds.
4. `uv run python -m unittest discover -s tests -v` passes.
5. Commit hash saved below.

## Checkpoint for next session
- Researcher / machine:
- Git branch / commit SHA:
- Data manifests / checksums:
- Actions and exact commands run:
- Observed outputs:
- Tests passed / failed:
- Scientific conclusions (only if supported):
- Issues / warnings:
- Next single task:

## Checkpoint 000 — Ubuntu Setup

Date: 2026-10-20
Status: Environment verified

Completed:
- GitHub repository cloned to Ubuntu.
- Project scaffold installed.
- Python environment created using uv.
- Package diagnostic successful.
- 2 infrastructure tests passed.

Scientific results:
- None yet.

Known issues:
- No scientific datasets imported.
- No ML models trained.
- No experiment-selection methods implemented.

Next milestone:
- PFAS Dataset Inventory and Data Validation.

## Checkpoint 001 — Local workflow verification (review approved)

Date: 2026-10-21
Branch: `test/workflow-issue-1`
Base commit: `843946995a497adbd7710cb8eaf5f62aae77e4ae`
Starting working tree: clean.

- Issue #1 was read using `gh issue view 1 --repo batuzunoglu/scientific-experiment-selection --json number,title,body,url,state`.
- `uv run python --version`: Python 3.12.14, exit 0.
- `uv run python -m scientific_experiment_selection doctor`: exit 0.
- `uv run python -m unittest discover -s tests -v`: 2 tests passed, exit 0.
- Initial sandboxed uv attempts exited 2 because the existing cache was read-only; approved retries succeeded.
- Researcher reviewed the local diff and replied `approve`; [local workflow test record](WORKFLOW_TEST.md) linked after review per Issue #1.
- Observed infrastructure results only; no scientific results or simulated measurements.
- No scientific data, analysis code, evaluation rules, or dependencies changed.
- Approved next actions: commit the documentation, push this branch, and open a PR for review. Publication results will be reported in the session; connected-repository review remains to be verified. Merge requires separate approval.

## 2026-10-21 — Remote review follow-up

- GitHub PR [#2](https://github.com/batuzunoglu/scientific-experiment-selection/pull/2) was read using the connected GitHub integration; the patch and `docs/WORKFLOW_TEST.md` on the feature branch were accessible without manual copying.
- Review comment submitted on PR #2. Confirmed the documentation records two passed Ubuntu infrastructure tests; no independent rerun of those tests or GitHub Actions result was observed by the reviewer.
- This verifies the ChatGPT ↔ GitHub report visibility path, not any ML/scientific claim.
- Next research milestone: dataset inventory, publication-permission assessment, and data manifest design.


## Checkpoint 003 — 2026-10-22 actual inventory; review stop

Supersedes pending-source status above. Retained branch `data/dataset-inventory`
and HEAD `7996a8bfa743f65b6d9589d98419d726c2bccefb`; preserved existing changes.
Read Issue #3 and latest comment. Source `/home/batuhan/research/raw-experiment-results`
contains eight regular XLSX files, Exp1–Exp8, totaling 685147 bytes. No duplicates
or excluded entries. Exp8 is present and matches the issue's recovered-file hash.
Full filenames, sizes, hashes, commands and limitations: `docs/DATASET_INVENTORY.md`
2026-10-22 checkpoint; JSON at `/tmp/issue-3-inventory-2026-10-22/manifest.json`.
Existing CLI labels Exp1/Exp2 UNKNOWN due to its narrower mapper; all bytes inventoried.
Eight software tests passed; independent sha256sum matched all files. No workbook
parsing or scientific inference. No code edits, raw changes/copies, commits, pushes
or uploads. Only local report/log additions. Independent backup unconfirmed.
Next: researcher review, independent well-to-condition mapping and provenance/QC
records; confirm backups and Exp1–Exp2 sharing scope before any controlled import.
Stopped for review as requested; no scientific analysis authorized/performed.

## Checkpoint 004 — 2026-10-22 evidence reconciliation; scientific review stop

Supersedes the earlier no-workbook-parsing checkpoint. Read all Issue #3 comments,
including decision checkpoint 6344194970, and all required project guidance.
Retained `data/dataset-inventory` at
`7996a8bfa743f65b6d9589d98419d726c2bccefb`. All seven pre-existing changed/untracked
files verified unchanged before append-only updates to the three session logs.

- Sources: raw files in `/home/batuhan/research/raw-experiment-results/`; evidence
  in `/home/batuhan/research/recovered-experiment-records/metadata-2026-10-22/`.
- All eight raw hashes match historical provenance, including `(1)` filename
  variants. All 22 manifest-listed package files match hash and size. All 32
  input files (eight raw + 24 evidence) unchanged on final hash recheck.
- Raw: 96 headings per workbook; 521 populated well columns total, including
  417 Exp3–8. All populated columns have 176 finite numeric points. No partial
  spectra. Draft presence/point-count claims agree for all 576 coordinates.
- Unresolved: 11 All6_QC composition conflicts; four QC action conflicts.
  Additional finding: 201 explicit planned zero cells are missing in master/draft
  across 69 Exp7 sample wells. No missing value filled or conflict resolved.
- Exp5 CSV's 96 preparation rows are all reconstructed; referenced numbered
  preparation/final-label workbooks are absent. Exp1/2 mapping remains incomplete.
- Detailed report: [WELL_MAP_DISCREPANCIES.md](WELL_MAP_DISCREPANCIES.md).
  Per-well CSV covers all 768 coordinates, with separate original/proposed
  composition, historical variants, source references, QC, confidence and roles.
  Helpers, input hashes, counts, checks and execution logs under
  `docs/audits/2026-10-22-reconciliation/`. Exact runnable commands are in report.
- Verification: eight existing tests passed; doctor exit 0, scientific_runs none;
  git diff --check exit 0. Independent rerun produced 12 byte-identical report
  outputs. Assertions verified 768 unique keys, 11 chemical/4 QC conflicts,
  69 plan-zero differences, and every resolved_label empty.
- Observed file/metadata audit only; no new measured or simulated scientific
  result. No source workbook writes, package-code changes, automatic exclusions,
  split changes, model training, staging, commits, pushes, uploads or merge.

Next single task: researcher scientific review of the discrepancy report and
source alternatives before any curation/import/training. Exp6/Exp8 test roles
remain intact; use_in_model is not a training selector. Independent preparation
evidence and backup confirmation remain open. Do not continue automatically.

## Checkpoint 005 — 2026-10-22 review report prepared

At the researcher's request, consolidated the completed audit into
[DATASET_RECONCILIATION_REVIEW.md](DATASET_RECONCILIATION_REVIEW.md) for ChatGPT and
scientific review before any commit/push. It lists exact raw hashes, match and
missing-label counts, all 11 chemistry/four QC conflicts, additional discrepancies,
files, prior observed test results, commands and limitations. Recounted saved
per-well records: 351 empty condition claims comprise 192 pilot/diagnostic
coordinates plus 159 empty Exp3–8 positions; only 104 are populated unlabeled
pilot/diagnostic columns. No new reconciliation or test-suite execution claimed.
Documentation-only follow-up; raw data, evidence tables, labels and splits untouched.
Next action remains scientific review. No staging, commit, push, upload or merge.

## Checkpoint 006 — 2026-10-22 proposed PR scope; awaiting approval

Read latest Issue #3 scientific review, comment 6345498494:
https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6345498494
Report-level review passed; this does not verify chemical labels or authorize ML.
Researcher requested a proposed commit scope before commit/push/PR creation.
Presented git status and tracked diff stat; enumerated all 28 proposed files
(inventory code/tests, documentation, and 19 audit supporting files). No raw XLSX,
unrelated file, canonical curated labels or model artifacts proposed. Largest file:
per_well_discrepancies.csv, 3257194 bytes; preserve its contradictory evidence.

Fresh checks: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
passed eight tests; `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor`
passed, scientific_runs none; `git diff --check` passed. Git index empty.
Branch retained; pre-existing work preserved. Only handoff/decision checkpoint
additions during preparation; no code or evidence-table changes.
All chemical conflicts, missing-versus-zero distinctions and external-test roles
remain unchanged. Next: researcher approval of the exact proposed 28-file scope
before staging/commit/push/PR. No merge authorized.

## Checkpoint 007 — researcher approved publication workflow

Researcher replied `approve` to the exact 28-file proposal and authorization to
stage, commit, push `data/dataset-inventory` and open a reviewable PR against main.
This supersedes the prior publication hold only for that scope. Raw workbooks,
canonical label curation, model training, split changes and merge remain outside
authorization. Fresh eight-test suite and doctor passed before publication.
Next action after opening the PR: review the code and discrepancy evidence on
GitHub; no automatic merge or chemical-conflict resolution. Publication outcome
and PR URL will be reported in the session and recorded in GitHub's PR history.

## Checkpoint 008 — PR #4 housekeeping follow-up; approval pending

Addressed review 5618857967 with current status text and explicit documentation
of the CLI's retained Exp3–Exp8 recognition limit and Exp1/Exp2 follow-up.
Historical checkpoints and all scientific records remain unchanged. No code edits.
Observed: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
passed all eight tests; `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor`
passed with scientific_runs none. Next: researcher approval of the local diff.
No staging, commit, push or merge performed for this follow-up.
