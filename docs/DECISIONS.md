# Decision Register

These are **working choices**; technical specifics require explicit review.

| ID | Status | Choice | Why |
| --- | --- | --- | --- |
| D-001 | Working | Use a private GitHub repo as canonical collaboration history | Independent of assistant conversations |
| D-002 | Working | Keep plain Markdown project notes and cross-model checkpoints | Portable between AI tools |
| D-003 | Working | Begin on Ubuntu, defer Mac setup | One validated environment first |
| D-004 | Working | Establish baseline scientific evaluation before RL/SLM claims | Reduce scientific risk |
| D-005 | Proposed | Add MLflow/DVC only when needed for tracked experiments and data sizes | Avoid tooling overhead at day one |
| D-006 | Working; real inventory pending | Issue #3 Phase 1 uses an explicit-root, read-only Python inventory with JSON/Markdown outputs | Preserve raw bytes and make mapping evidence and unknowns reviewable before import |

## D-006 — 2026-10-21 inventory scope

- Authorization: researcher requested Issue #3 Phase 1 and a dedicated branch;
  explicitly prohibited raw upload, commits and pushes pending inventory approval.
- Implemented local tooling with synthetic tests; no actual dataset inventory yet.
- Filename mapping is provisional; batch/plate identities remain `UNKNOWN`.
  Missing expected batches cannot be assessed without a batch roster.
- Backup status is unconfirmed. Source-directory request is pending.
- Issue #3 reports sharing permission for Exp3–Exp8 only. Repository privacy was
  independently checked as true. Existing raw/private ignore rules remain unchanged.
- No research question, evaluation split, physical condition, reward or QC decision changed.
- Researcher approval of inventory/import/publication: **not yet given**.

## New decision template
- ID and date:
- Question / competing options:
- Evidence:
- Chosen option and why:
- Expected trade-offs / risks:
- Researcher approval:


## D-006 update — 2026-10-22 inventory review gate

User and latest Issue #3 comment authorize read-only inventory of Exp1–Exp8 in
`/home/batuhan/research/raw-experiment-results`. Eight files observed; Exp8 checksum
matches recovery reference. See `DATASET_INVENTORY.md` for full evidence. Existing
CLI/code preserved, including Exp1/Exp2 UNKNOWN mapping limitation. No scientific
identities or QC inferred. Independently documented well-to-condition mapping is
required before analysis; backup remains unconfirmed. No research question, split,
physical condition or reward changed. Import/publication approval remains pending;
no commit, push or upload performed. Stop for researcher review.

## D-007 — 2026-10-22 evidence-aware reconciliation review gate

- Authority: researcher request and Issue #3 comment 6344194970. Authorized local
  read-only comparison and reports; not curation, import, training or publication.
- Observed: all eight raw hashes match historical records; all package-manifest
  hashes/sizes match; draft/raw measurement presence agrees. Evidence and exact
  commands: [WELL_MAP_DISCREPANCIES.md](WELL_MAP_DISCREPANCIES.md).
- Preserve 11 All6_QC chemical alternatives and four QC conflicts. Additional
  missing-versus-zero differences affect 201 Exp7 analyte cells in 69 sample wells.
  Exp5 preparation references are reconstructed and original numbered workbooks
  are unavailable. No missing concentrations promoted to zero.
- Evidence precedence follows the issue checkpoint. Old ML agreement is correlated
  lineage, and a historical `Verified` string is not physical validation.
- No new scientific choice made: research question, conditions, rewards, QC actions,
  and training/test assignments unchanged. All resolved_label fields remain empty.
- Proposals pending researcher review: resolve All6 from independent preparation
  evidence; reconcile historical QC records; decide how to represent planned zeros
  separately from unknown physical composition. No approval of these proposals,
  retraining, import or publication has been inferred.

### D-007 review packaging — 2026-10-22

Researcher requested ChatGPT review before commit/push. Consolidated existing
evidence in [DATASET_RECONCILIATION_REVIEW.md](DATASET_RECONCILIATION_REVIEW.md).
No scientific decisions resolved or new approvals inferred; all prior review
gates and source-preservation requirements remain in force.

### D-007 report-level review and PR proposal — 2026-10-22

Issue #3 comment 6345498494 accepts report-level provenance/inventory review only.
It explicitly leaves chemical validation, QC conflicts, incomplete preparation
provenance, and model eligibility unresolved. Researcher requested preparation of
the existing feature branch, with status/diff/file list presented before approval.
Proposed scope is 28 code/test/report/documentation files, excluding raw workbooks.
No uncertain labels promoted to ground truth; no split changes or ML authorized.
Commit, push and PR creation await explicit researcher approval; no staging or
publication performed. No merge authorization.

### D-007 publication authorization

Researcher explicitly replied `approve` to staging/committing/pushing the proposed
28 files and creating the reviewable feature-branch PR. This authorizes publication
of inventory tooling and provisional audit evidence only; it does not validate
chemical labels, resolve conflicts, approve ML, change splits or authorize merge.

### PR #4 housekeeping response — 2026-10-22

Used the documentation-only option in review 5618857967: retain the CLI's original
Exp3–Exp8 interface, explicitly separate Exp1/Exp2 file identity from unknown well
chemistry, and document a recognition-scope follow-up requiring synthetic tests. Refreshed current
status without rewriting historical checkpoints. No scientific decisions changed;
the review's suggested future baseline is not implemented or approved here.

## D-008 — 2026-11-08 approved research roadmap

- **Researcher approval:** the researcher explicitly accepted the six-phase English roadmap in conversation and requested its recording in the project charter and decision register.
- **Scope:** (1) evidence-aware baseline supervised ML; (2) random/DoE/active-learning/Bayesian baselines; (3) numerical RL environment and reward engineering; (4) prompt-only, tool-using, RL-trained SLM and hybrid agent comparisons; (5) prospective wet-lab validation; (6) research publication and portfolio.
- **Required research arms:** numerical RL, reward evaluation, tool-using agents and RL-trained SLM agents are **core experiments to attempt and evaluate**, not conditional extensions. Their relative success is an open empirical question; report non-improvement and feasibility limitations.
- **Initial scientific milestone:** Issue #5 Phase A remains the first technical task. Six-class individual-PFAS classification using Exp3 (development), Exp5 (external evaluation) and Exp8 (locked final batch holdout) is *proposed*. Counts 72/53/18 are candidate historical records, not approved physical preparation identities. No data split, QC resolution, source file, reward formula, or training result was modified by this roadmap decision.
- **Next technical decision gates:** approve verified well inclusion/exclusion and evaluation split before fitting; freeze a leakage-safe evaluation protocol before RL reward design; implement controlled simulation/replay where necessary and prospective wet-lab testing later.
- **Methodological guardrail:** compare RL and agent variants with random, DoE, active learning and Bayesian methods at comparable experiment budgets, with data provenance, reproducibility, error analysis and separate simulated versus observed lab results.

## D-009 — 2026-11-08 repository visibility status

- **Researcher instruction:** make `batuzunoglu/scientific-experiment-selection` public for internship and job applications; researcher confirmed they are comfortable with the current research records being public.
- **Observed GitHub state:** `visibility=public` when checked on 2026-11-08. This is a status observation, not a claim that the assistant changed repository settings.
- Current tracked code includes audit evidence with well compositions and QC information, **but no original Exp1–Exp8 raw XLSX exports**. New raw imports, private lab details, or sensitive materials require a separate publication review; public Git commit history and issue discussions remain accessible.

## D-010 — 2026-11-08 two analytical tasks and honest holdout status

- **Researcher approval:** begin with **individual PFAS identity classification and concentration prediction as separate coequal ML tasks**; do not assume one preprocessing/feature pipeline preserves information for both.
- **Scientific rationale:** transformations that suppress scale/offset may also remove absolute absorbance and concentration information. Keep analysis-specific methods and metrics separate.
- **Historical exposure:** Exp3/Exp5 have already been used for preprocessing and model development in historical records. Training fresh model weights without Exp5 does not erase researcher-level selection based on prior Exp5 outcomes. Exp5 is useful as a **previously explored batch-transfer/development evaluation**, not a pristine unseen final test. Exp8 is the planned locked 10 ppm final test, **conditional on audit of historical exposure**; future prospective experiments are preferred for an additional unexposed test.
- **Open methodological choices:** Raw/full spectrum should serve as a proposed control, but the exact preprocessing × feature-extraction comparison is **not yet approved**. No baseline correction, normalization, Compact8 set, wavelength selection or model family is mandated. Prior experimental outputs are exploratory evidence, not final immutable choices.
- **No change made:** original data, QC labels, source hashes, computational model or proposed physical split were not changed by this note. Do not initiate training until well eligibility, split usage and a fair comparison protocol are reviewed.

## D-011 — 2026-11-08 durable scientific lab notebook

- **Researcher-approved process:** use [RESEARCH_LAB_NOTEBOOK.md](RESEARCH_LAB_NOTEBOOK.md) as the append-only dated reasoning/experiment journal in GitHub for all future research sessions. Capture question, hypotheses, alternatives, evidence, decision status and rationale, parameter/config provenance, actions actually executed, results or failures, limitations and next decision. Differentiate historical, observed and simulated findings.
- **Assistant/Codex workflow:** AGENTS.md requires reading/updating the notebook, with concise settled choices mirrored here and operational checkpoints in HANDOFF.md. Do not retroactively edit old entries to conceal reversals or negative results.

## D-012 — 2026-11-08 approved four-arm spectral representation comparison

- **Researcher-approved:** compare **A Raw/full spectrum, B Raw/Compact8, C Area-normalized/full spectrum, D Area-normalized/Compact8**, in both six-class PFAS identity classification and PFAS concentration regression (known-identity first). Raw remains a required no-preprocessing/no-extraction control. This supersedes the *comparison not approved* language in D-010, while D-010's leakage and physical-QC safeguards remain active.
- **Why:** preprocessing or feature extraction may suppress irrelevant batch effects but also destroy useful PFAS identity or concentration magnitude. Earlier development evidence showed mixed outcomes: Area improved some matching metrics yet did not consistently improve actual classifier results. Compare one design factor at a time using the same within-task model family and grouped evaluation procedure.
- **Exact initial transforms:** Area factor = trapezoidal integral over 380–580 nm, applied to all 176 absorbances; validate area is positive/nonzero. Compact8 follows the historical fixed definitions including Savitzky–Golay first derivative (15 points, polynomial order 2), with denominator and numerical safeguards. Do not silently substitute blank/baseline correction, PQN, SNV, L2 or a supervised-selected feature set.
- **Initial modeling families proposed and accepted for first benchmark:** regularized logistic regression for identity; Ridge for concentration conditional on known PFAS; parameters, preprocessing safety and grouped folds to be documented. No model training is yet authorized by this documentation-only decision, pending Phase A dataset evidence sign-off.
- **Evaluation:** Exp3 development; Exp5 previously exposed batch-transfer assessment, not pristine final test; Exp8 locked final holdout, pending historical exposure verification. No test-derived choices, no random splitting of technical replicates across folds. Report task-specific metrics, not one universal preprocessing winner.
- **Record of rationale:** [RESEARCH_LAB_NOTEBOOK.md Entry 005](RESEARCH_LAB_NOTEBOOK.md). Coding agents must append observed implementation choices and results rather than inventing reasons or backfilling approval.

## D-013 — 2026-11-08 pull-request notebook gate

- **Researcher request:** Ensure reasons, decisions, failed trials and actual execution results are recorded routinely without requiring repeated conversational reminders.
- **Implementation:** A standard-library Python checker and GitHub Actions pull-request workflow require an append-only dated `docs/RESEARCH_LAB_NOTEBOOK.md` entry for research-code/model/tests/config or selected methods-document edits. Synthetic tests cover the gate. Agents must update this notebook within the **same authorized PR**, without rewriting history.
- **Scope:** Documentation/infrastructure enforcement only. A notebook edit does **not** independently authorize new model fitting, raw data publication, QC relabeling or experiment execution; researcher sign-off gates remain.
- **Limitations:** The check confirms the *presence* and append-only structure of an entry, not scientific adequacy. Actions must be enabled, and protecting `main` with a required status check is necessary to prevent bypassing PR checks via direct pushes. No automatic cross-conversation reminder or background monitor is implied.
- **Notebook reference:** [Entry 006](RESEARCH_LAB_NOTEBOOK.md).

## D-014 — 2026-11-08 limited provisional Phase A continuation

- Scientific review: Issue #5 comment 6726841885; researcher explicitly requested
  continuation in the local session. Missing independent preparation evidence blocks
  physical verification, not label-independent manifest/software preparation.
- Authorized: candidate manifest with explicit provisional/reconstructed provenance,
  QC and missing values; four previously approved representations and synthetic tests.
- Not approved: physical labels, final eligibility/folds, ML fitting or evaluation,
  chemistry resolution, public artifacts, commit/push. Numerical implementation details
  and source/grouping limits remain subject to scientific review.
- Observed implementation and tests: Notebook Entry 008 and `PHASE_A_REVIEW.md`.
  Entry 007 and prior conclusions are preserved as historical records.

### D-014 update — 2026-11-08 provisional engineering acceptance

Issue #5 scientific review 6727151818 provisionally accepts the initial spectral
implementation based on source/test review and reported Exp3/5 measured-spectrum
validation. Exact proposed publication scope is in `PHASE_A_PUBLICATION_REVIEW.md`.
No public commit/push is authorized by that comment or this local scope proposal.
Physical labels, eligibility/grouping, CV and training approval remain unresolved.

## D-015 — 2026-11-08 minimal multi-agent collaboration

- **Researcher request:** Prepare Google Antigravity on Ubuntu as an optional assistant to Codex and use accepted, low-complexity best practices so multiple coding agents understand task ownership, handoffs and existing scientific safeguards.
- **Choice:** Reuse the root `AGENTS.md` (supported directly by Antigravity and Codex), the existing GitHub Issue/PR workflow, and the append-only research notebook. Add one short operational reference, `docs/AGENT_WORKFLOW.md`, rather than a custom orchestration service, duplicated `GEMINI.md`, shared mutable state file or new automation.
- **Reason/tradeoff:** Git branches/worktrees isolate writes; single-owner Issue tasks and compact handoffs preserve traceability without model-specific integration. Human review remains required; there is no automatic cross-agent synchronization or authorization.
- **Pilot:** Codex retains core implementation responsibility; Antigravity starts read-only on a bounded review/test task. No GPU or local LLM required for this change.
- **Scope and authorization:** Documentation-only workflow proposal. No training, raw-file access, new chemical approval, experimental execution, and no branch merge without researcher review. Research notebook Entry 015 records the reasoning.

## D-016 — 2026-11-08 Exp3 D6/D7 primary-analysis eligibility

- **Researcher-approved:** Exclude **physical Exp3 D6 and D7** (historical PFHxA_10 `review-retain` preparation concern) from the **primary Phase B model-development/validation pool**; preserve them in source records and use a separate, clearly labeled sensitivity comparison under the frozen primary protocol.
- **Why:** Avoid relying on questioned preparation status for the main benchmark while transparently reporting the effect of including the two uncertain wells.
- **Scope:** Do not rewrite historical QC flags, `candidate_included`, the raw files or the Phase A 72-well candidate manifest. The **provisional** primary pool is 70 of 72 Exp3 individual-PFAS candidates before other eligibility decisions. No well becomes training-authorized by this choice.
- **Still pending:** independent preparation grouping, leakage-aware grouped CV design, remaining labels/eligibility, concentration calibration protocol, and final evaluation holdout approval. Exp5 is historically exposed/reconstructed; Exp8 locked.
- **Evidence:** [Issue #5 comment 6729516343](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6729516343), [Research Lab Notebook Entry 017](RESEARCH_LAB_NOTEBOOK.md). No implementation or model training authorized.
