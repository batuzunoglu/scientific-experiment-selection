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

## Checkpoint 009 — 2026-11-08 approved methodology and notebook enforcement

- PR #6 approved and merged the English six-phase roadmap: baseline ML, traditional selection, RL/reward engineering, tool-using/RL-trained SLM agents, prospective lab validation, publication.
- PR #7 created the append-only `docs/RESEARCH_LAB_NOTEBOOK.md`, clarified two separate individual-PFAS tasks (identity and concentration), and documented Exp5's historical development exposure. Exp8 remains intended locked 10 ppm holdout pending historical-use audit.
- PR #8 approved the initial representation experiment: A Raw/full 176-point spectrum; B Raw/Compact8; C Area-normalized/full; D Area-normalized/Compact8, for both tasks. No preprocessing winner claimed. Exact transformation details are in Notebook Entry 005 and D-012.
- Notebook PR gate being added in a separate PR: every research-affecting PR should append a dated entry. Scientific accuracy and actual runtime outcomes still need human review.
- **Next single technical task:** Issue #5 Phase A on clean Ubuntu clone: verify raw checksums and per-well identity/QC provenance for Exp3/5/8; generate reviewable candidate manifest and deterministic non-fitting A–D feature representations with synthetic tests. **No ML training, Exp8 evaluation, arbitrary relabeling, raw Git upload or feature-branch commit/push before researcher reviews Phase A results.**
- Current GitHub work here is limited to docs and notebook process tooling; the Ubuntu raw laboratory data are not accessible through this connector, and no new ML scientific run is claimed.

## Checkpoint 010 — 2026-11-08 Phase A preflight evidence stop

Local Ubuntu checks supersede the previous connector-only access limitation.
Initially clean main at `9f9089f7832aedaadc877a2bfb8e86af90a4ead9`.
Exp3/5/8 raw hashes freshly match the tracked manifest. Exp5 CSV still has
96 reconstructed preparation rows; referenced original preparation/final-label
workbooks were not found under the recovered-records root. Latest Issue #5
comment 6726670028 explicitly requires stopping for missing independent chemistry
evidence. See `PHASE_A_PREFLIGHT_REVIEW.md` and Notebook Entry 007.
Only four documentation files changed locally. No source/code changes, manifest,
features, new tests, training, upload, staging, commit, push or branch creation.
No fetch/sync performed. Next: researcher review of the evidence gap and explicit
clarification or additional source evidence before resuming Phase A. Prior
72/53/18 counts are not newly verified. Exp8 remains locked.

## Checkpoint 011 — 2026-11-08 provisional Phase A implemented; review stop

User accepted Issue #5 scientific review 6726841885. Entry 007/preflight report
preserved; Entry 008 records continuation rationale and observed results. New
manifest CLI/raw reader/four representations and synthetic tests implemented.
Final artifacts: `data/private/phase-a-2026-11-08-final/` (ignored metadata-only
CSV/JSON/summary). 288 rows, 72/53/18 candidate counts; all physical labels unverified,
all Exp5 preparation statuses reconstructed, all Exp8 rows locked. Raw hashes and
22 evidence-package checks pass; 28 inputs unchanged; final rerun byte-identical.
32 tests passed. No actual experimental features or ML models generated.
Full commands/conventions/limitations/file list: `PHASE_A_REVIEW.md`.
Current main checkout and prior notes retained without sync/stash/branch change;
all work local/unstaged, no commit/push/upload. Next: scientific review of eligibility,
provisional chemistry, numerical details, preparation groups and split protocol.

## Checkpoint 012 — 2026-11-08 local ChatGPT review package

Read Issue #5 comment 6726971791. Package at
`/tmp/phase-a-chatgpt-review-2026-11-08` with ZIP/combined Markdown, complete reports,
code/test snapshots, full diffs including new files, fresh 32-test log and metadata
checks. Code/tests unchanged; Entries 007–008 retained; Entry 009 records packaging.
Scientific sign-off pending; next step ChatGPT review. No models, experimental
feature smoke test, commits, push or upload performed.

## Checkpoint 013 — 2026-11-08 Exp3/Exp5 measured-spectrum smoke test

Issue #5 review 6727098915 and researcher authorize limited validation. Entry 010
and appended PHASE_A_REVIEW report exact commands/results. Unchanged A–D functions
succeed for all 96 Exp3/72 Exp5 measured wells, no failures. Exp5 24 empty columns
reported absent. No negative band values or signed-area cancellation; normalized
area/reconstruction errors ~machine precision. Both raw hashes and existing module
hashes unchanged. Ignored diagnostics in `data/private/phase-a-smoke-exp3-exp5-2026-11-08`;
repeat byte-identical. Exp8 untouched; no labels/models/method changes or publication.
New script only orchestrates validation. Next: scientific review, no automatic sign-off.

## Checkpoint 014 — 2026-11-08 final publication proposal

Latest review 6727151818 provisionally accepts Phase A engineering. Exact proposed
15-file allowlist: `PHASE_A_PUBLICATION_REVIEW.md`; includes Entries 007–010 plus
publication-preparation Entry 011. Raw/private files explicitly excluded. Fresh
32-test suite passed; source/tests unchanged. Local patch/hashes/test log at
`/tmp/phase-a-publication-review-2026-11-08`. Await explicit approval of scope/diff
before branch/stage/commit/push/PR. Training gate remains separate.

## Checkpoint 015 — 2026-11-08 exact publication authorized

Researcher explicitly approved the 15-file scope and feature-branch commit/push/PR
against main, with no merge/training/label changes. Feature branch created from
`9f9089f7832aedaadc877a2bfb8e86af90a4ead9`; fresh 32-test suite passed. Reviewed
snapshot matched all 15 files before append-only authorization notes. Notebook
007–011 preserved; Entry 012 records authorization. No extra files added to scope.
Next: staged audit then authorized publication; observe/report PR link and CI.

## Checkpoint 016 — 2026-11-08 multi-agent coordination preparation

Researcher wants Antigravity available on Ubuntu to supplement Codex without
increasing project complexity or risking dual-agent edits. Preparing documentation
PR with shared root AGENTS.md rules, one short docs/AGENT_WORKFLOW.md,
explicit Issue ownership, Git worktree isolation, short handoffs and append-only
notebook Entry 015. No additional runtime, agent server or GPU requirement.
Antigravity is not yet installed or authorized for code-writing tasks.
Next: researcher reviews docs PR and installs official agy CLI, then tries one
read-only pilot. Phase B model training, preparation provenance and split approval
remain pending.

## Checkpoint 017 — 2026-11-08 Antigravity read-only pilot reviewed

Google Antigravity CLI 1.5.3 was installed by the researcher on Ubuntu with their
Google account. Shared multi-agent instructions were merged via PR #12.
The researcher relayed the first read-only audit of Issue #13 from clean `main`
at `a1ff18e` (agent-reported; no file modifications). ChatGPT checked the
source references against published code and posted its assessment in Issue #13
comment 6729448802, with the full rationale in Notebook Entry 016.
Findings: QC review wells are candidates but not training-authorized; physical
preparation groups are UNKNOWN and grouped-split leakage risks remain; Exp5 is
historically exposed/reconstructed and Exp8 remains locked. No defects fixed,
data uploaded, ML models trained, or new scientific approval given.
Next: researcher-led Phase B eligibility and grouped-CV decision; Antigravity
may continue as a bounded read-only reviewer, Codex remains main implementer.

## Checkpoint 018 — 2026-11-08 researcher approved Exp3 D6/D7 primary exclusion

Researcher agreed to exclude physical Exp3 D6/D7 from primary Phase B ML
analysis, while preserving these historically review-retain PFHxA_10
measurements for a future frozen-protocol sensitivity analysis.
Decision and scientific reasoning: Issue #5 comment 6729516343, Notebook
Entry 017 and D-016. Existing 72 candidate rows/QC/source files unchanged;
the provisional primary subset would have 70 rows before any other eligibility
decisions. No code or model training, no label promotion and no split changed.
Next scientific review: preparation-group/replicate evidence and grouped CV,
then separate identity and known-identity concentration task protocols.

## Checkpoint 019 — 2026-11-08 Exp3 shared-solution technical repeats confirmed

Researcher stated that the four technical replicate wells for each Exp3
PFAS × concentration condition all came from the same prepared solution and
approved keeping them together in any Phase B train/validation split.
Documented as scientific provenance (researcher first-hand report, not
independently audited preparation record): Issue #5 comment 6729570912,
Notebook Entry 018, Decision D-017. Existing technical_replicate_group is
a suitable proposed Exp3 shared-solution identifier; original
preparation_group=UNKNOWN and group_independence_verified=False remain
conservative and unchanged. No assumption of independence between conditions
or reuse for Exp5/8; no code, raw data, model training or CV implementation.
Next: select scientific CV schemes for identity and known-identity regression,
while recognizing at most 18 nominal shared-solution groups and D6/D7 primary
exclusion.

## Checkpoint 020 — 2026-11-08 chosen Phase B balanced grouped CV

Researcher requested the best grouped evaluation design after confirming shared
Exp3 condition solutions. We selected a fixed 3-fold, class- and concentration-
balanced group split: 18 nominal PFAS×concentration shared-solution groups,
6 per held-out fold (1/PFAS and 2/concentration). Initial deterministic proposal:
fold=(class_index+concentration_index)%3 with documented class/concentration order.
No well shares prepared solution between train/validation. Existing D6/D7
exclusions yield provisional 70 primary wells; no source eligibility/status
changed. See Notebook Entry 019, Decision D-018, Issue #5 comment 6729701226.
Before supervised fitting, review metadata-only group→fold manifest,
model/metric and label eligibility protocols; Exp5/Exp8 gates unchanged.
No code or model run in this documentation step.

## Checkpoint 021 — 2026-11-08 approved LOGO primary validation choice

Researcher explicitly preferred Leave-One-Group-Out and approved LOGO as
primary Phase B Exp3 cross-validation after comparing it with fixed balanced
three-fold grouped CV. The former D-018 three-fold primary method is
**superseded** (not removed); shared-solution grouping D-017 and Exp3 D6/D7
primary exclusion D-016 still apply. Nominally 18 shared-solution groups:
each entire group held out in turn, remaining 17 for training. No model fits
or code changes performed. A single held-out group has one PFAS true class,
so metrics must be predefined and aggregated over held-out predictions
across folds; condition/group-balanced evaluation needed. Known-identity
concentration regression has only two other concentrations per PFAS in
each fit and is exploratory. See Notebook Entry 020, Decision D-019 and
Issue #5 comment 6729822449.
Next: metadata-only 18-fold LOGO manifest and leakage review before
scientific eligibility/metric protocol sign-off and separate training approval.
