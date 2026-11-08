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
