# Research Lab Notebook

**Purpose:** Chronological, append-only record of how we reason about, choose, implement, test and revise scientific methods. This notebook is the research narrative. Use [DECISIONS.md](DECISIONS.md) for brief durable decisions, [HANDOFF.md](HANDOFF.md) for operational session state, and [EXPERIMENT_TEMPLATE.md](EXPERIMENT_TEMPLATE.md) for individual reproducible physical/computational runs.

**Every future research session:** Read the latest entry before work; record date, question, evidence, alternative choices, decision status, rationale, risks, actions actually performed, exact result artifacts, and next step. Explicitly label **researcher-approved**, **working proposal**, **observed**, **historical**, **simulated**, or **not run**. Do not turn a proposed method into a tested/approved method. Record negative results and changes to prior decisions rather than rewriting them.

**Public-repository rule:** Document technical rationale without uploading original experimental spectra or nonpublic source workbooks. Any public data release requires a separate review.

---

## Entry 001 — 2026-11-08 | Distinguishing new models from independent tests

**Question.** If we retrain a model from scratch, can Exp5 become a completely untouched test batch, despite prior Exp3/Exp5 modeling?

**Evidence.** Past Ce–ARS development records (`Preprocessing_Worklog.md` and `CeARS_Feature_Strategy_Model_Development_Guide.md`, historical local/Library records not yet versioned here) explicitly compare preprocessing, wavelength/feature choices and model performance across Exp3 and Exp5. The repo's [Issue #3](https://github.com/batuzunoglu/scientific-experiment-selection/issues/3) and [reconciliation report](DATASET_RECONCILIATION_REVIEW.md) establish source-file matches but not definitive physical label validity. Background references: [Dwork et al., Science 2015, DOI 10.1126/science.aaa9375](https://doi.org/10.1126/science.aaa9375); [Avoiding common machine learning pitfalls, Patterns 2024, DOI 10.1016/j.patter.2024.101046](https://doi.org/10.1016/j.patter.2024.101046).

**Explanation.** New model weights do not erase earlier researcher-level model-selection feedback. Even if Exp5 is omitted from the new model's fitting, previous Exp5 results may already have influenced choices of pipeline/algorithm. This is *historical exposure and adaptive test reuse*, distinct from direct train/test feature leakage.

**Current working safeguards, subject to split sign-off:**
- Exp3: model development / training candidates.
- Exp5: **previously exposed** batch-transfer / development evaluation; do not market as a pristine independent final test. It is still valuable for explicit cross-batch analysis.
- Exp8: intended **locked** 10-ppm final independent batch evaluation, *provided historical exposure is checked*. Do not open Exp8 outcomes for preprocessing/model/reward decisions; its limited concentration coverage must be disclosed.
- Prefer newly prepared independent batches for later prospective and RL/agent generalization validation. If existing held-out outcomes are viewed, report the resulting exposure and preserve a new future lockbox.

**Status:** Methodological safeguard documented and explained; final split approval remains pending. No labels or actual data partitions changed. No model trained.

## Entry 002 — 2026-11-08 | Two supervised tasks from the beginning

**Researcher-approved decision:** Model **PFAS identity** and **PFAS concentration** as **two distinct, coequal analytical tasks from the start**. Do not describe concentration as merely an optional future extension.

| Task | Proposed target | Evaluation focus |
| --- | --- | --- |
| Individual PFAS identity | six-class label: TFA, PFPA, PFBA, PFHxA, PFOA, PFNA | grouped balanced accuracy, macro-F1, confusion matrices, transfer to another batch |
| Individual PFAS concentration | measured target concentration (ppm); initial method may be conditional on known identity | grouped MAE/RMSE, error by PFAS, concentration and batch, unseen-concentration tests |

**Reason:** Amplitude may encode concentration, whereas normalized shape may distinguish compound identity. A preprocessing choice that improves one task could harm the other. Testing both guards against overclaiming a universal optimum.

**Important qualification:** The first concentration model is a *known-identity / oracle-identity* calibration benchmark, not an end-to-end device that knows the correct analyte. Later, compare a cascaded pipeline using **predicted identity** and propagate identification errors. No concentration, PFAS identity, condition code, batch ID or well ID may enter as a predictive input unless the explicitly defined deployment scenario would genuinely supply it; these values are targets/metadata otherwise.

**Status:** Researcher-approved high-level task choice. Exact algorithms, calibration design, candidate wells and final splits are not yet selected. No model fit.

## Entry 003 — 2026-11-08 | Preprocessing and feature extraction: review before coding

**Question.** Should UV–Vis preprocessing and engineered spectral features be mandatory?

**Rationale.** Each transform can suppress baseline/batch noise but can also remove PFAS identity or concentration information. A transformation that preserves chemical identity may destroy absolute intensity and distort concentration calibration. Historically, Raw, offset correction, Area, L2, SNV, PQN, derivatives and legacy Compact8 were explored; those exploratory comparisons do not establish a universal winner.

**Working comparison proposal — not yet approved as a fixed experiment matrix:**
- Always preserve original raw spectra and maintain a **Raw/full-spectrum reference**.
- Separately examine preprocessing effect while holding the feature set/model fixed; examine feature-extraction effect while holding the underlying representation/model fixed.
- Candidate initial transparent factorial comparison: Raw/full, Raw/Compact8, Area/full, Area/Compact8. Consider PQN separately as justified; record its training-only reference construction. Neither Area nor PQN is chosen as the winner.
- Baseline/blank subtraction, SNV, derivative and any engineered feature need explicit rationale, numerical safety checks, and task-specific validation before activation. Exp8 has no confirmed valid same-run Ce–ARS blank and must not be used to estimate blank correction.
- The historical Compact8 is a **baseline candidate**, not a mandatory representation; be careful with ratios near zero and with centroid/spread after mean-centered SNV (not physically valid under the original definitions).
- For any fold, fit scaling, supervised feature selection, PCA/PLS and PQN reference (if learned) from **training data only**; never use Exp8 or a nominal external test batch to choose a method. Preserve the unchanged raw spectrum and the versioned derivation of every feature.

**Status:** No preprocessing or feature-extraction scheme has been approved as the default. The researcher requested a methodological discussion before implementation. **Codex Issue #5 Phase A should prepare verified candidate well mappings and a method-comparison protocol first, not silently lock or run a preprocessing pipeline.** Existing issue instructions requiring immediate implementation are superseded by this note pending a review.

## Entry 004 — 2026-11-08 | Ongoing research-record convention

**Researcher-approved process:** Use this file like a dated laboratory notebook for every substantive research decision and experiment. Record the *why* as well as the *what*. Keep decisions separate from evidence, observed results separate from expectations, and negative results available for review. Prompt coding assistants to do the same in [AGENTS.md](../AGENTS.md).

**Change-management rule:** Any future decision that changes a prior model, preprocessing, holdout, reward or laboratory protocol gets a new entry referencing the superseded entry; no retrospective rewriting of the historical record. A change is not “approved” merely because code ran.

**This entry:** Documentation only. No new spectra, QC adjudication, model training or experimental measurement. No claims of new empirical results.

**Next single decision gate:** Agree on the first fair preprocessing × representation comparison and on how calibration/identity folds will be grouped. Then implement a read-only, evidence-aware dataset builder under [Issue #5](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5).

## Entry 005 — 2026-11-08 | Approved initial preprocessing × feature-extraction comparison

**Researcher approval:** The researcher explicitly approved the four-branch comparison after reviewing Area Normalization's mathematical meaning and the mixed historical results. This supersedes the *unapproved method matrix* status in Entry 003, **not** its warnings or the distinction between identity and concentration.

**Scientific question:** Does removing overall absorbance magnitude or compressing a 176-point spectrum into eight interpretable features help PFAS identity classification, and does either operation destroy information needed to predict PFAS concentration?

**Initial controlled 2 × 2 design:**

| Branch | Spectral preprocessing | Model input representation |
| --- | --- | --- |
| A — Raw / Full | No spectral preprocessing | 176 raw absorbances (350–700 nm) |
| B — Raw / Compact8 | No spectral preprocessing | Eight prespecified Compact8 features |
| C — Area / Full | Area normalization | 176 normalized absorbances (350–700 nm) |
| D — Area / Compact8 | Area normalization | Eight Compact8 features from normalized spectra |

**Area Normalization definition:** Compute the trapezoidal integral of the original spectrum over 380–580 nm and divide *every* original wavelength intensity (350–700 nm) by that same positive, nonzero factor. Validate finite signals and nonzero/nonpathological area; record failures rather than silently changing spectra. No blank subtraction or baseline correction is part of these four branches. This is per-well processing; no test-derived reference is fitted.

**Compact8 definitions, from the historical method:** point intensity at 420 and 518 nm, A420/A518 (guard denominator), spectral centroid and spread over 380–580 nm, integrated absolute first derivative over 380–580 nm, first derivative at 450 nm, and fitted slope over 440–480 nm. Use the historical Savitzky–Golay derivative convention: window 15 points, polynomial order 2, 2 nm grid, first derivative; specify boundary behavior and numerical integration conventions in implementation. Do not add or select extra features using Exp5/Exp8 results. Interpret normalized signals as normalized coordinates, not original absorbances.

**Two separate tasks for every branch:**
- Identity: six-class single-PFAS classification; initial reference model family **regularized logistic regression**; macro-F1 and balanced accuracy, confusion and per-class recall.
- Concentration: single-PFAS concentration regression in ppm; initial reference family **Ridge regression** conditional on *known analyte identity*. Report MAE/RMSE and by-PFAS/concentration errors. This conditional setting is an oracle identity benchmark; later evaluate cascading predicted identity into concentration.
- Exact hyperparameters, normalization of ML features, grouping/folds, model fit and evaluation must be reproducible; **fit any learned scaling/selection on training folds only**. Technical replicates do not constitute independent preparation batches. Historical Exp3/Exp5 exposure must be disclosed; Exp8 remains locked pending audit of past exposure.

**Why approved:** Holding the model family and sample assignments fixed within each task lets us compare (A vs B) extraction, (A vs C) normalization, and (B vs D) the effect of normalization on engineered features. The raw/full control is essential because intensity differences may encode both chemical identity and concentration. Earlier cross-batch spectral matching sometimes favored Area, while some Compact8/model-level analyses favored Raw; neither method has earned universal preference. See historical `Preprocessing_Worklog.md` and `CeARS_Feature_Strategy_Model_Development_Guide.md` for prior exploratory observations.

**Limitations and status:** This is an **approved experiment design, not an observed result**. No model was trained, no preprocessing run, no raw Excel written, no QC label or split altered by this documentation update. PQN/SNV/L2/blank correction are **outside this initial four-branch comparison**, though they may be considered later through a new logged decision. Only the *choice of comparison* is approved; exact well eligibility and grouping require audit and explicit review before model fitting.

**Notebook responsibility:** ChatGPT records researcher-approved research questions, alternatives, reasons and scope promptly from the discussion; Codex reads the notebook and appends exact implementation, scripts, parameters, runs, checks, results/negative outcomes and limitations. Neither actor may claim researcher approval for unapproved changes. Every update is reviewed with the researcher via a GitHub diff/PR.

**Next action:** Proceed with Issue #5 Phase A: build and verify a read-only spectral dataset contract and candidate well inclusion manifest, then implement the **four explicitly approved feature representations** with synthetic tests and scientific explanation, subject to source availability. Stop for review **before model training or a new data publication**.

## Entry 006 — 2026-11-08 | Make notebook updates enforceable during coding

**Researcher instruction and approval:** Consistent, structured research documentation is required throughout the project without repeated reminders. The researcher asks ChatGPT and Codex to take necessary action so later publication work can rely on the experiment narrative.

**Problem:** Written agent instructions alone are easy to overlook; a new code commit might introduce methodology or results without recording the rationale, executed commands, parameter values, provenance and failures. An assistant cannot guarantee automatic updates when nobody is running it.

**Decision / implementation:** Add a small Python `scripts/check_research_notebook.py` quality gate and a GitHub Actions `research-notebook` pull-request check. For research-code, analysis, experiment, modeling, tests, config and selected methodological-document changes, the same PR must append a new dated entry to this file. Historical notebook content must remain byte-for-byte intact. New lightweight synthetic unit tests exercise the checking logic. Update `AGENTS.md` so assistants log discussions and implementation at their respective steps; no direct research pushes to `main`.

**Why:** The code and the contemporaneous explanation of its purpose and limits should be reviewed as one versioned change. This creates a repeatable reminder whenever someone opens or updates a PR, while preserving earlier research decisions and failures.

**Limitations:** This is a workflow/process check, **not** an audit of whether a scientific entry is correct or sufficiently complete. It runs on PRs only while GitHub Actions is enabled; without a required branch-protection status check, a direct push could bypass it. It cannot recover unrecorded conversations or run on the user's Ubuntu machine without a local action. Notebook ownership: ChatGPT records the researcher's stated decisions and reasoning; Codex records exact observed implementation/tests/results, and both need researcher review.

**Current observations:** Workflow/checker/tests and this entry were authored in a new GitHub branch. No raw experiment files were loaded, no ML dataset was constructed, no models fitted, and no chemistry outputs produced. Test/workflow execution remains to be verified, and should not be marked passed unless observed.

**Next action:** Review/merge the process PR, then start Issue #5 Phase A with the approved Raw vs Area and Full vs Compact8 2×2 design, local evidence-aware well manifest, deterministic feature extraction, and synthetic unit tests. Stop before model fitting and before publishing raw spectra.

## Entry 007 — 2026-11-08 | Phase A preflight: raw hashes match; evidence stop

**Question.** Are the prerequisites in Issue #5's latest implementation comment
satisfied on this Ubuntu checkout?

**Authority/status.** Researcher requested Phase A only, no training, uploads,
commits or pushes. Read AGENTS.md, README, charter, decisions, handoff, Entries
001–006, full Issue #5 and all four comments, plus both reconciliation reports.
Comment 6726670028 explicitly requires stopping if independent chemistry evidence
is missing. The four-arm design stays approved; this is an observed preflight
discrepancy, not a new scientific decision or completed implementation.

**Evidence and actual runs.** Initial tree clean on main at
`9f9089f7832aedaadc877a2bfb8e86af90a4ead9`. Fresh SHA-256 calculations for Exp3,
Exp5 and Exp8 matched the tracked raw manifest; independent `sha256sum` agreed.
Fresh CSV inspection counted 96 Exp5 rows, all `reconstructed`. Recursive search
of the recovered-records root found neither `02_Exp5_Plate_Preparation.xlsx` nor
`05_Exp5_Final_Sample_Labels.xlsx`, both referenced in its DATA_SCHEMA.md.
Exact runnable checks, full hashes, paths and limitations are recorded in
[PHASE_A_PREFLIGHT_REVIEW.md](PHASE_A_PREFLIGHT_REVIEW.md).

**Alternatives and why.** Proceeding with provisional claims could support
software preparation, but would disregard the latest issue's explicit stop
condition. Stopped and documented the gap instead of treating inherited labels
as independent chemistry evidence. No labels, zeros, QC actions, splits or
representation definitions were changed. No additional methodological approval
is inferred.

**Implementation/testing status.** Documentation only: new preflight report and
append-only notebook/handoff/learning notes. No candidate manifest or A–D code
implemented, no synthetic tests added or run, no models fitted, no raw spectra
parsed/transformed/uploaded. Candidate counts 72/53/18 were not freshly verified.
No new observed or simulated laboratory result. No fetch/sync, new branch,
staging, commit or push performed. Local notes await review.

**Limitations / next decision.** Missing within the inspected directory does not
prove the source files do not exist elsewhere. Hash agreement establishes bytes,
not physical labels. Supply independent preparation evidence or clarify whether
provisional Phase A implementation may proceed despite that stop condition.
Exp5 exposure and Exp8 lock remain unchanged. Phase A remains incomplete.


## Entry 008 — 2026-11-08 | Provisional Phase A implementation after scientific review

**Question and review.** Can we prepare auditable software while independent Exp5
preparation evidence remains missing? Read the latest Issue #5 scientific review,
[comment 6726841885](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6726841885).
It distinguishes physical-label verification from label-independent preparation.
The researcher explicitly accepted limited provisional continuation in this session.
Entry 007 and its local preflight report are preserved, not rewritten or renumbered.

**Approval status.** Provisional manifest and the previously approved four
representations plus synthetic tests are authorized. Physical labels, sample
eligibility, evaluation folds and numerical implementation sign-off remain pending.
No authorization for ML fitting, chemistry adjudication, publication, commit or push.

**Alternatives and rationale.** Continuing the blanket stop would conflate missing
chemical validation with ability to test deterministic software. Promoting inherited
labels to truth would be unsupported. Implemented provisional claims with explicit
`physical_label_verified=false`, complete source evidence and unresolved warnings,
while making transformations independent of labels. Raw/full remains the required
control; neither normalization nor compression is designated a winner.

**Implementation.** Added `spectral.py`, `raw_spectra.py`, `dataset_contract.py` and
two test modules. Manifest covers all 288 coordinates, including excluded/empty
locations, source hash/cells, QC, original references, preparation/replicate claims,
proposed batch role, both future target tasks and lock status. No missing component
is imputed. Preparation status derives from source variants, not batch identity.
Actual preparation groups remain unknown; batch:condition is only a conservative
technical-group proxy, with no independence claim and no folds constructed.

A/C produce 176 values; B/D eight. Area uses the inclusive 380–580 trapezoid and
scales all original channels. Compact8 uses the approved points, ratio, moments,
derivative area/450 derivative and 440–480 slope. Implementation conventions:
discrete intensity-weighted centroid/spread; trapezoidal areas; fixed SG 15/poly2/
delta2/deriv1 with polynomial-interpolated boundaries; unsmoothed slope inputs;
configurable numerical epsilon 1e-12. Negative moment weights are flagged invalid,
not clipped. Branch errors preserve valid Raw/full. These conventions/limits are
reviewable implementation choices, not validated instrument QC or proof of exact
archived feature-matrix reproduction. No experimental feature statistics informed them.

**Observed runs/results.** Exact runnable commands, full source/output hashes,
counts, artifact paths, files and numerical details are in
[PHASE_A_REVIEW.md](PHASE_A_REVIEW.md). Fresh raw SHA-256 matches for Exp3/5/8;
22 evidence-package size/hash matches; all 28 input hashes retained. Raw populated
well counts 96/72/21; candidate counts **72/53/18** match historical expectations.
All candidates remain chemically unverified. Exp3 D6/D7 review flags retained;
Exp5 B7 excluded; E10:E12 mixtures outside this task; Exp8 F1:F3 invalid reagent
blanks and absent G1:G6 preserved. All Exp8 rows locked. All 96 Exp5 rows retain
reconstructed status. Missing Exp8 components remain missing.

Final local outputs: `data/private/phase-a-2026-11-08-final/{candidate_wells.json,
candidate_wells.csv,summary.json}` (Git-ignored, no spectra). Independent rerun at
`/tmp/phase-a-2026-11-08-final-rerun` produced three byte-identical files. Manifest
JSON SHA-256 `619f1e73df3e6bb4930ed77906c0dc17156787ea60f7d3e085ab03ebb13990f3`.
An earlier intermediate output directory was retained and superseded by `-final`.

**Tests and negative outcomes.** Baseline 13 tests passed. Initial new-test imports
failed for missing modules before implementation. Later regression tests exposed
missing explicit-claim disagreement detection and hardcoded preparation status;
both fixed from the source of the defect. Fresh code review prompted evidence-based
status and exact 15-sample impulse coverage; end-to-end synthetic export/count-stop
coverage added. Final `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover
-s tests -v`: **32 tests passed** (19 new). Python 3.12.14; standard library only;
no random seed needed. Tests are artificial fixtures, not observed chemical behavior.

**Not run / limitations.** No experimental feature extraction/export, training,
predictions, performance evaluation or model-selection statistics. Raw workbooks
were read only for structure/presence checks, not chemical inference. No uncertainty
resolved; prior All6/QC alternatives preserved. Package hashes and inherited audit
agreement are not independent chemistry evidence. Exp5 remains historically exposed;
Exp8 lock remains conditional on historical-use audit. Source reader is schema-specific.
Current checkout/local notes preserved without sync, stash, staging, commits or push.

**Next decision.** Researcher review of the local manifest, numerical conventions,
source limitations, candidate eligibility and eventual grouped split protocol.
Implementation is locally complete; scientific/data sign-off remains pending.

**Final local verification.** `git diff --check` passed; direct `valid_append` check
against the saved notebook through Entry 007 passed, preserving all prior bytes.
Synthetic API example produced shapes 176/8/176/8 and area 400.0. All 28 input
hashes rechecked after documentation unchanged. Index empty; final local artifacts
ignored. The PR checker CLI only compares committed refs and therefore did not
exercise this uncommitted diff; no CI execution or publication is claimed.

## Entry 009 — 2026-11-08 | Local review package prepared; no implementation change

Read Issue #5 scientific review comment 6726971791. It acknowledges engineering
progress provisionally and requests exact local reports/diffs before final sign-off.
Researcher requested a local ChatGPT review package, explicitly withholding code
changes, training, commits and pushes. Packaged complete preflight/Phase A reports,
source/test snapshots, tracked and untracked diffs, manifest metadata and fresh test
logs at `/tmp/phase-a-chatgpt-review-2026-11-08`; ZIP and combined Markdown accompany it.

Fresh exact test command: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest
discover -s tests -v`: 32 tests passed, exit 0. Full stdout/stderr and command in
package `tests.txt`. Read-only checks confirmed candidate counts 72/53/18; Exp3
D6/D7 review inclusion, Exp5 B7 exclusion/E10:E12 mixture exclusion; all 96 Exp5
statuses reconstructed; all physical-label flags false; Exp8 lock/missing values
preserved; all 28 recorded input hashes match; prior notebook through Entry 007
preserved. Code/test SHA-256 snapshots before/after match; index empty.

No source/tests changed and no real-spectrum transformation, model, prediction,
chemistry adjudication or publication performed. Synthetic tests and documentary
checks remain software evidence only. Scientific risks and numerical implementation
choices remain pending independent review. Suggested real-spectrum smoke test from
the review was not run: the comment places it after code review. Next action is
ChatGPT review of the local package, then researcher decision; no final sign-off.

## Entry 010 — 2026-11-08 | Label-independent measured Exp3/Exp5 transformation smoke test

**Question/authority.** Read ChatGPT scientific code review Issue #5 comment
6727098915. It independently reviewed the uploaded package, reported 19 new tests
passing and SG agreement with SciPy on synthetic data, and requested real-data
numerical validation before sign-off. Those independent results are attributed to
that review, not rerun here. Researcher authorized only the read-only Exp3/Exp5
smoke test and stability diagnostics. Prior Entries 007–009 remain intact.

**Alternatives/why.** Retaining synthetic-only evidence leaves actual signal-domain
compatibility unknown. Silently changing signed-area or negative-intensity policy
would alter the approved methods. Ran the unchanged branches on every populated
Exp3/5 column and reported stability metrics instead. No labels/QC metadata used
for transformations or well filtering; no method preference or model selection.
Relative-area threshold 1e-6 is descriptive only, not an added rejection rule.

**Exact runs/artifacts.** New standard-library orchestration script
`scripts/smoke_phase_a_exp3_exp5.py`; exact two commands, definitions, full diagnostic
ranges and limitations appended to `docs/PHASE_A_REVIEW.md`. First output:
`data/private/phase-a-smoke-exp3-exp5-2026-11-08/{summary.json,per_well_diagnostics.csv}`;
repeat output `/tmp/phase-a-smoke-exp3-exp5-rerun-2026-11-08`. Both commands exit 0;
two artifacts byte-identical. Repeat stdout/stderr/command/exit captured in first
folder's `execution.log`. Python 3.12.14; no randomness, ML or new dependencies.

**Observed results.** Exp3: all A/B/C/D succeed for 96/96 measured wells. Exp5:
all A/B/C/D succeed for 72/72. No failing well IDs/reasons. Exp5 G1:H12 are 24
absent spectra, not transform failures. All populated review/excluded/QC/mixture
wells included; numerical success does not change eligibility. Dimensions and
finiteness checked; exact Raw/full passthrough and provenance equality asserted.

Area ranges: Exp3 5.9882–46.9998; Exp5 25.6058–36.297 absorbance·nm.
Relative signed/absolute area=1 in every well; zero negative band values and zero
relative-cancellation flags. Minimum raw A518: 0.0289/0.0874; minimum normalized
A518: 0.00339648305/0.00341328918 (Exp3/5). Minimum raw moment sums 3.0257/12.9118,
normalized 0.504097089/0.504098436. All well above unchanged epsilon 1e-12.
Maximum normalized-area error 2.22044605e-16 both batches; maximum relative raw
reconstruction error 1.45469474e-16/1.44485037e-16. ×2 arithmetic rescaling leaves
C/D unchanged to recorded precision (max absolute differences 0). This is a
consistency probe, not a new physical concentration observation.

**Preservation/limitations.** Exp3/5 hashes match prior records before and after;
existing transform/reader/inventory module hashes unchanged. Only the two selected
raw workbooks were opened; Exp8 not used, rehashed or transformed. No spectra/full
feature vectors exported. No new measurements or chemistry simulations; results
are observed computations on historical measured spectra. No threshold, formula,
QC/label, missing value, split or preprocessing change. Exp5 remains reconstructed
and historically exposed. All physical-label/eligibility decisions remain provisional.
No independent real-data feature truth, tolerance sensitivity under future noise,
near-cancellation policy or method superiority established. New script validated
by run assertions/repeatability; no new unit-test pass count claimed. Original
source methods preserved, no models, staging, commits, push or upload.

**Next decision.** Scientific review of real-spectrum diagnostics and remaining
numerical/domain risks before final Phase A sign-off or any future scoped PR.

## Entry 011 — 2026-11-08 | Final publication scope prepared; approval pending

Read scientific review Issue #5 comment 6727151818, which provisionally accepts
Phase A engineering conditional on matching final evidence and requests exact
publication scope. Researcher requested preparation only, no models/commit/push.
Reviewed final source/test/docs diff and proposed a 15-file explicit allowlist in
`docs/PHASE_A_PUBLICATION_REVIEW.md`, excluding all raw files, private candidate
manifests and `data/private/**`. Entries 007–010 and committed history preserved.

Fresh exact command `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover
-s tests -v` passed 32 tests, exit 0. Prior saved Exp3/5 smoke results/log and method
hashes checked; no raw spectra or Exp8 opened in this preparation. No implementation
changes or new methodological choices. Known numerical-domain/non-atomic-output
limitations remain documented; physical labels, eligibility, grouping and training
protocol approval remain separate. Local full patch/file hashes/test log accompany
the scope review under `/tmp/phase-a-publication-review-2026-11-08`.

Next: researcher review and explicit approval of precise public code/docs scope.
No staging, commit, push, PR creation, model fitting or publication performed.

## Entry 012 — 2026-11-08 | Researcher authorized the exact Phase A publication scope

Researcher explicitly approved publishing exactly the 15 files in
PHASE_A_PUBLICATION_REVIEW.md, committing/pushing only the Phase A feature branch
and opening a PR against main. No merge, training or scientific-label changes
are authorized. All 15 contents matched the reviewed snapshot before appending
this authorization and handoff note within the same approved file scope.
Entries 007–011 and all preceding notebook bytes are preserved.

Fresh `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
passed all 32 tests, exit 0. No raw workbooks were opened for this publication
step. Branch `feature/ml-dataset-contract` created from main at
`9f9089f7832aedaadc877a2bfb8e86af90a4ead9`; sandbox initially blocked ref creation,
then the approved elevated retry succeeded. Next: verify the exact staged allowlist,
append-only notebook, secret/private-content exclusions and whitespace; commit,
push feature branch and create reviewable PR. Final PR URL/CI outcomes will be
reported after observation in the session/PR, not predicted here. Scientific
uncertainty, prior negative results, label/QC claims and method limits unchanged.

## Entry 013 — 2026-11-08 | ChatGPT review of GitHub PR #10

**Question:** Does the published Phase A engineering pull request match the approved scope and preserve scientific safeguards, and can it be considered ready for a separate merge decision?

**Evidence inspected directly on GitHub:** [PR #10](https://github.com/batuzunoglu/scientific-experiment-selection/pull/10) at original reviewed commit `0429de91a024585481e948ad557f64b3301ebcdb`. Confirmed exactly 15 changed paths: three implementation modules, one measured-spectrum smoke script, two test files, and nine methods/review/notebook documentation files. PR patches include no raw workbook, `data/private/**` file, per-well output or private candidate manifest. Documentation refers to local paths but does not embed their contents. No obvious credential/token patterns appeared in the changed text. Read the full Python source and relevant review/decision/notebook content.

**CI observed:** [GitHub Actions run 42537656978](https://github.com/batuzunoglu/scientific-experiment-selection/actions/runs/42537656978) passed the append-only notebook check and unit test step; the job log explicitly reports `Ran 32 tests ... OK`. This checks the repository's software behavior using synthetic fixtures; it does not independently reproduce the historical laboratory measurements or certify reconstruction of Exp5 preparations.

**Review finding:** The implementation is appropriately scoped as **provisional, label-independent Phase A infrastructure**: 176-channel raw reader, deterministic raw/area/Compact8 branches, evidence-preserving candidate manifest and explicit training-authorization false flags. The Exp3/Exp5 measured-spectra smoke success and hashes are supported by prior local execution reports; the reviewer did not rerun those raw-file operations in GitHub. Exp8 is still a locked candidate holdout; no ML model training, performance estimate, automatic chemical-label adjudication or superiority claim is included.

**Known limitations remain visible:** strict Compact8 negative-weight and ratio thresholds; absolute epsilon and signed-area near-cancellation policy not established for future spectra; non-atomic output files; provisional identity/concentration claims and unknown independent preparation groups; Exp5 reconstructed and historically exposed. These do not block publishing this **versioned engineering research baseline**, but they block a claim of validated chemistry or automatic permission to train predictive models. The versioned notebook and PR reviews are the audit trail for later research reporting.

**Decision/status:** ChatGPT's scientific/code **review supports merging this scoped Phase A PR after the researcher's separate approval**, contingent on final PR CI passing after this documentation entry. This is **not** an authorization to perform the merge, train models, change labels, expose Exp8, or publish private data. No computation, model training or experimental run was performed as part of this entry.

**Next decision:** merge approval, then an independent scientific review of candidate well eligibility, chemistry provenance, preparation-group-aware CV and a prospective untouched evaluation protocol before any supervised ML fitting.

## Entry 014 — 2026-11-08 | Phase A engineering PR merged to main

**Researcher approval:** The researcher explicitly approved merging [PR #10](https://github.com/batuzunoglu/scientific-experiment-selection/pull/10) after scientific/code review.

**Observed GitHub action:** PR #10 was squash-merged to `main` with commit `8922ee3783db97c4f67084671375982daa93a2f4`. Its final reviewed head was `3cb699735a76c169416dcb674c3dcbd616c0c037`; the corresponding [CI run](https://github.com/batuzunoglu/scientific-experiment-selection/actions/runs/42537955788) completed successfully (32 unit tests and the research-notebook gate). Only the agreed 15 implementation/test/documentation files were included; no raw workbooks or private candidate manifests were committed. The merge itself did not retrain models, decide any chemical identities, or evaluate Exp8.

**Why this milestone matters:** The approved Raw/full, Raw/Compact8, Area/full and Area/Compact8 representations, audited source reader, provisional well manifest builder and documented Exp3/Exp5 smoke-test procedure are now a versioned, reproducible engineering foundation for *future* supervised experiments. The existing notebook preserves why preprocessing was compared rather than assumed helpful.

**Scientific status:** **Phase A engineering published, but physical chemistry labels, QC inclusion, preparation independence, grouped CV design and authorization to train remain unresolved.** Previous reports of 168/168 Exp3/Exp5 measured spectra successfully transforming are from the historical local smoke run, not a new experiment performed during merge. Exp5 historical exposure remains explicit; Exp8 remains locked.

**Next decision gate:** Scientifically review the proposed training eligibility, concentration target, replicate/preparation-group definitions and evaluation split. Do not train a model or inspect Exp8 outcomes until those decisions are explicitly approved.

## Entry 015 — 2026-11-08 | Lightweight collaboration between Codex and Antigravity

**Researcher request:** Codex's short-window usage allowance is limited, while the researcher also has a Gemini account and an Ubuntu workstation. They asked for a practical Antigravity installation and a simple, generally accepted way for different agents to know their responsibilities and hand off work without creating unnecessary complexity.

**Question and alternatives:** Introduce a custom multi-agent orchestrator/server, duplicate tool-specific instructions, or reuse existing project conventions. A full orchestrator adds unnecessary infrastructure, concurrency and security concerns for the current research stage. Antigravity officially recognizes root `AGENTS.md` instructions, so a second `GEMINI.md` would introduce divergence risk.

**Decision/proposal implemented on a documentation feature branch:** Retain the root `AGENTS.md` as the shared coding-agent rulebook; add one short `docs/AGENT_WORKFLOW.md` for explicit one-owner-per-issue responsibility, isolated branches/worktrees, read-only reviewer by default, GitHub Issue/PR handoffs and a compact status template. ChatGPT/researcher coordinate scientific decisions, Codex owns main implementation, Antigravity is initially a bounded independent reviewer/tester. No concurrent writes to the same tree, no overlapping undocumented notebook edits, and no independent agent approval of chemistry, training, raw release or merge.

**Why:** Shared file-based instructions, Git branches/PRs and auditable Issue updates are simple, portable across model providers and already familiar to the project. The current notebook gate continues to ensure dated records in authorized research PRs, with human checking scientific completeness.

**What was done:** Authored the workflow guide and updated `AGENTS.md`, `docs/DECISIONS.md`, the notebook and handoff in a new GitHub branch. The user requested Ubuntu setup guidance; **Antigravity was not installed on the researcher's machine by ChatGPT** and no model execution/test results or physical experimental measurements are claimed.

**Limitations and next step:** This is human-directed task coordination, not automatic agent-to-agent messaging. Start with a safe Antigravity CLI installation verified from Google's official docs, then run a small read-only pilot. PR must be reviewed before merge. Phase B scientific eligibility, grouping, holdout and model-training approval remain entirely separate and unresolved.

## Entry 016 — 2026-11-08 | First Antigravity read-only Phase B risk-audit pilot

**Question.** Can Antigravity use the same scientific repo instructions and provide a useful second-agent review without interfering with Codex's work or spending Codex's short-window allowance?

**Delegation and evidence.** Following merged PR #12's `AGENTS.md` and `docs/AGENT_WORKFLOW.md`, Antigravity was assigned a read-only, explicitly scoped [Issue #13](https://github.com/batuzunoglu/scientific-experiment-selection/issues/13) audit on the Ubuntu checkout. The researcher supplied the agent's structured handoff: clean `main` at `a1ff18e`, `git status --short` clean, no modified files, and reading project decisions/notebook/reports plus `dataset_contract.py` and its tests. The assistant did not itself witness Antigravity's local session; these execution details are **agent-reported**. No ML model or additional lab test was run.

**Findings independently cross-checked in published code.**
1. `dataset_contract.py:44` allows a historical `qc='review'` well to remain a candidate, with explicit `qc_review` warning at line 56. Exp3 D6/D7 require a **separate future eligibility review**. Crucially, candidates are *not* approved training rows: line 96 sets `training_authorized=False`.
2. `dataset_contract.py:89–91` sets `preparation_group='UNKNOWN'` and uses the `experiment:condition` technical-replicate **proxy**, explicitly marking preparation independence unverified. Random well-wise CV risks leakage/overconfidence if wells share their physical preparation; the available evidence **does not prove** the independent preparation structure.
3. The code preserves `physical_label_verified=False`, Exp5's reconstructed/historically exposed warning and proposed Exp8 locked holdout (lines 54–55, 86–96). No chemical ground truth is established by these flags.

**Review outcome and rationale.** The pilot is **useful and accepted as an independent read-only risk review**, not a new verified scientific experiment and not a defect-fix request. This demonstrates a practical, minimal handoff via an Issue and shared Markdown rules, without multi-agent orchestration or simultaneous writes. It does not establish comparative model quality, token cost, or performance improvement.

**Open scientific gate.** Before Phase B model fitting, researcher and ChatGPT must agree how to treat Exp3 D6/D7, which preparation/replicate groups and leakage-safe CV are defensible, how to handle provisional labels and which concentration task evaluations are legitimate. Exp5 remains a historically explored transfer/development batch; Exp8 stays locked pending historical exposure audit. **No training approval or experiment design change is inferred from the audit.**

**Actions actually taken.** Posted the reviewed findings and qualifications in [Issue #13 comment 6729448802](https://github.com/batuzunoglu/scientific-experiment-selection/issues/13#issuecomment-6729448802); this entry documents the rationale. No code, raw workbooks, private manifests, model artifacts or data splits were changed.

**Next:** Resume Phase B *scientific protocol discussion* with the researcher; only after sign-off delegate a bounded implementation issue to a named coding agent.

## Entry 017 — 2026-11-08 | Exp3 D6/D7 primary analysis exclusion with sensitivity follow-up

**Researcher-approved decision.** The researcher explicitly accepted the recommendation to **exclude physical Exp3 wells D6 and D7 from the primary supervised ML analysis** and preserve them for a separate sensitivity analysis. Approval followed Antigravity's read-only Issue #13 audit and ChatGPT's scientific discussion. The decision is also recorded in [Issue #5 comment 6729516343](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6729516343).

**Evidence and alternatives.** `docs/WELL_MAP_DISCREPANCIES.md` identifies D6/D7 as historical `review-retain` PFHxA_10 wells with a preparation concern and available raw spectra. Options considered: include them in primary fitting despite uncertainty, delete/exclude entirely, or exclude from the primary analysis while preserving them for a transparent controlled sensitivity analysis. The third approach was approved because it reduces dependence on disputed preparation while showing whether their inclusion materially changes conclusions.

**Interpretation and boundaries.** These are **physical well identifiers, not condition codes**. The Phase A manifest's 72 Exp3 individual-PFAS candidate wells remain historical candidate records; excluding these two would give a **provisional primary subset of 70** if no other exclusion applies. This decision **does not rewrite** source QC labels, candidate manifest, source hashes or raw data; does not verify remaining chemistry; and does **not** set `training_authorized=True` for any sample. Keep D6/D7 traceable and use a *frozen* primary procedure in the later +D6/D7 sensitivity comparison rather than tuning on them.

**What was actually done.** Documented researcher approval and rationale in the Issue, notebook, decision register and handoff. **No code, source workbooks, split implementation, test result, new experimental measurement or model fit** was produced by this decision.

**Next unresolved scientific decision.** Establish defensible grouping for technical replicates and any shared sample preparations before selecting grouped validation/CV. Current `experiment:condition` grouping is a proxy, not proof of physically independent preparations. Later decide full eligible-well list, task-specific six-class identity and known-identity concentration evaluation, Exp5's historically exposed status and Exp8's lock. No training authorization yet.

## Entry 018 — 2026-11-08 | Exp3 technical replicates share one prepared solution

**Scientific question.** Should the four measured Exp3 technical replicates per PFAS × concentration condition be treated as independent samples for train/validation splits?

**New researcher-provided experimental fact.** The researcher confirmed directly: all four replicates under each Exp3 condition were aliquots from **the same prepared solution**. The researcher approved keeping every such group together. This is a first-hand experimental statement, **not** a newly supplied or independently audited original preparation record; do not retroactively rewrite source evidence or assert independence across different conditions, dilutions or stock batches.

**Approved constraint.** In future Exp3 Phase B evaluations, an individual `Exp3:PFAS_concentration` condition (shared-solution group) is **indivisible across train/validation**. A random well-wise train/validation split is disallowed because replicate wells from the same solution could leak shared preparation signatures. The existing software's `technical_replicate_group=f'{exp}:{condition}'` matches this reporting convention for Exp3, but the manifest's `preparation_group='UNKNOWN'` and `group_independence_verified=False` remain scientifically conservative until provenance is documented. Do **not** infer that the convention is valid for Exp5 or Exp8.

**Design consequences.** Exp3 has nominally 6 PFAS × 3 concentrations = 18 shared-solution condition groups, four technical wells each in the historical candidate design. Previous Entry 017 approval excludes Exp3 D6/D7 from primary ML analyses while retaining them for a separate frozen-protocol sensitivity analysis; their reported parent PFHxA_10 group remains one indivisible group with its remaining candidate wells. This grouping may assess predictions for held-out condition combinations, **not** generalization to new independent preparations of the same condition. Additional shared-stock dependencies between different conditions are unknown.

**Alternatives and reasoning.** Random well splitting would treat aliquots as independent and invite optimistic leakage. Grouped splitting with preparation provenance avoids this specific within-condition leakage; defining exact folds requires a separate task-specific decision because leaving out whole concentrations changes the generalization question. This entry approves the grouping constraint, **not** a specific CV algorithm or reported model result.

**Observed actions and limits.** Recorded the researcher's statement and decision in [Issue #5 comment 6729570912](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6729570912) and the decision/handoff records. No ML model trained, no simulation or new physical experiment performed, no raw XLSX, dataset-contract code, provisional labels, eligibility flags, source hashes or Exp8 outcomes changed. Exp5 remains reconstructed and historically exposed. Next: independently review grouped-CV design for six-class identity and known-identity concentration prediction.

## Entry 019 — 2026-11-08 | Choose balanced three-fold grouped CV for Exp3 Phase B

**Question.** After agreeing to keep all four technical wells from one prepared Exp3 solution together, which CV procedure best suits the small 6-PFAS × 3-concentration experiment? The researcher asked why the previous “grouped CV” and “grouped K-fold” suggestions differed and requested the most suitable choice. Grouped CV is the general principle; grouped K-fold is a concrete implementation. There was no reversal of the leakage-prevention decision.

**Alternatives.** Random well-level K-fold can split aliquots of the same solution and overestimate validation accuracy. Off-the-shelf GroupKFold prevents that leakage but does not guarantee every PFAS is represented in each fold. StratifiedGroupKFold attempts class balance, but its greedy procedure does not guarantee exact balance. Leave-one-group-out has just one held-out condition group per validation pass, omitting most PFAS classes from that pass and complicating per-fold classifier metrics. With the designed 18 condition groups, an explicit **balanced three-fold grouped protocol** achieves both group separation and complete PFAS class coverage.

**Selected scientific protocol.** Use **three fixed folds**, each holding out six whole PFAS × concentration groups: one group per each of six PFAS identity classes and two groups at each nominal concentration (5, 10 and 20 ppm). A simple deterministic assignment is `fold=(class_index+concentration_index)%3`, where class order is `TFA, PFPA, PFBA, PFHxA, PFOA, PFNA` and concentration order `5, 10, 20`; publish and validate the explicit group-to-fold map before any ML training. Each group appears in validation exactly once and never concurrently in training. The existing Exp3 D6/D7 primary exclusion leaves only two wells in their PFHxA_10 group, without deleting the group or rewriting source QC; nominal fold well sizes become 22, 24 and 24.

**Purpose and limitations.** Assess relative performance on previously unseen *condition-level solution groups within Exp3*, not on genuinely independently prepared replicates of the same chemical condition or independent batches, because those are not established. The same fixed outer folds can support the two previously accepted **separate** tasks: six-class PFAS identity classification and known-identity concentration regression. The latter has only **two independent solution concentration conditions per PFAS** in each training split; resulting regression estimates, particularly extrapolation to 5 or 20 ppm, must be considered highly uncertain/pilot-only. Learned scaling, feature selection or model fitting must be confined to training folds. Do not claim final unbiased model-selection performance from the same CV folds if model tuning is guided by them.

**Evidence/authorization status.** The researcher requested choosing the best method, not immediate model fitting. Details are recorded in [Issue #5 comment 6729701226](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6729701226). No fold implementation, real data opening, model training, evaluation, chemical relabeling or Exp8 inspection was performed here. The decision is a proposed implementation protocol requiring manifest/fold checks and separate researcher review of task-specific metrics/hyperparameters and remaining label eligibility before any training is authorized.

**Next:** prepare a small *metadata-only*, label-claim-based fold allocation and automated leakage/class/concentration-balance checks for scientific inspection. Keep all source and training-authorization flags unchanged, including Exp5 historically exposed and Exp8 locked.

## Entry 020 — 2026-11-08 | Researcher selects Leave-One-Group-Out as primary validation

**Question and decision.** After Notebook Entry 019 selected balanced 3-fold grouped CV, the researcher proposed **Leave-One-Group-Out (LOGO)** because they wanted to see every group's prediction individually. ChatGPT clarified that **both** methods use every group for validation exactly once: 3-fold holds out six groups per fitting for three total fits, whereas LOGO holds out one condition group for each of eighteen fits. The researcher explicitly answered **"evet"**, approving **LOGO as the primary Phase B evaluation strategy**. This supersedes the primary-method choice in Entry 019 / D-018 without rewriting that historical scientific discussion. The D-017 same-solution separation constraint is unchanged.

**Scientific rationale and tradeoff.** A dataset with only 18 nominally distinct PFAS×concentration condition groups benefits from holding out each one separately, analyzing condition-specific errors, and fitting on the remaining 17 groups. LOGO requires 18 training runs per fixed specification, yields only one ground-truth PFAS class per validation fold, and does **not** independently validate new physical preparations of an identical PFAS×concentration condition. Fixed balanced grouped 3-fold remains a possible **secondary robustness analysis**, but may not be chosen opportunistically based on results to claim an unbiased winner.

**Exact planned outer-fold contract (not implemented).** Group by the researcher-confirmed shared Exp3 PFAS×concentration prepared solution. Each of 18 nominal groups is held out in one fold; all technical replicate wells of that group stay together, and the other 17 condition groups form training. Earlier approved primary exclusion of physical Exp3 D6/D7 remains in effect, resulting in a **provisional** 70-well primary pool and two retained wells in the PFHxA_10 group. Keep historical QC, `candidate_included` and `training_authorized=False` unchanged until separate evidence/implementation approval.

**Separate tasks and metrics.** For six-class identity classification, a LOGO validation fold contains wells from one true class, so per-fold macro-F1, confusion matrix or six-class estimates are not meaningful. Pool all **out-of-fold** predictions from the 18 folds, predefine the principal aggregate metric, and report condition-level errors. Because D6/D7 change a group's well count, the primary metric should weight solution groups equally rather than treating correlated technical wells as independent examples; the precise aggregation rule and confidence statements need a separate protocol approval. For **known-identity** concentration regression, each PFAS has only two other concentration-level solution groups available during each fitting; predictions at 5/20 ppm can be extrapolation. Interpret results as exploratory. All learned scaling/model selection must be nested in training data, with frozen estimator and metric choices before inspecting outer-fold results.

**Other limitations.** Group separation avoids directly splitting the same prepared solution, but independence among different conditions is unverified (possible shared stocks, batches). Exp5 is reconstructed/historically exposed and not a pristine test; Exp8 remains locked pending exposure audit. No raw data, held-out outcomes, CV code, experiment or ML model was used or changed in this decision.

**Evidence and next action.** Researcher confirmation and reviewed scientific limits are recorded in [Issue #5 comment 6729822449](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6729822449). Next prepare a metadata-only LOGO fold map and leakage audit for scientific review, then freeze eligibility and model/metric protocol before any separate training authorization.


## Entry 021 — 2026-11-08 | Phase B deterministic 18-fold LOGO plan and leakage tests

**Question.** How should the researcher-approved 18-fold Leave-One-Group-Out (LOGO) cross-validation plan (D-019) be implemented and verified in code without accessing private experimental spectra, violating same-solution replicate constraints (D-017), dropping the PFHxA_10 group under Exp3 D6/D7 primary exclusion (D-016), or training machine learning models?

**Context and authorization.** Under Issue #19, Antigravity was assigned as the bounded implementation owner on dedicated branch `feature/phase-b-logo-plan`. Codex is not active in this worktree during this task. Authorized actions are strictly standard-library implementation, synthetic group-leakage tests, and evaluation plan documentation. No raw lab files, private manifests, or model training were accessed or performed.

**Implementation.**
1. Created `scientific_experiment_selection/logo_plan.py` (standard-library only). Provides canonical Exp3 condition groups (`TFA, PFPA, PFBA, PFHxA, PFOA, PFNA` × `5, 10, 20` ppm), canonical group formatting (`Exp3:{PFAS}_{concentration}` consistent with `dataset_contract.py`), deterministic 18-fold LOGO plan generator (`generate_logo_plan`), group ID validation (`validate_group_ids`), and sample partitioning with strict within-fold leakage guards (`split_samples_by_fold`, `verify_fold_leakage`, `verify_plan_integrity`).
2. Created `tests/test_logo_plan.py` containing synthetic test cases:
   - `test_canonical_groups_count_and_content`: verifies exactly 18 groups across 6 PFAS and 3 concentrations.
   - `test_make_and_parse_group_id`: verifies round-trip string formatting and validation.
   - `test_eighteen_folds_generated_deterministically`: verifies 18 folds, pure determinism, and that each canonical group is held out exactly once.
   - `test_zero_group_leakage_in_all_folds`: verifies 1 validation group and 17 training groups per fold with zero overlap.
   - `test_fail_closed_on_malformed_duplicate_or_unexpected_groups`: verifies rejection of duplicate, missing, unexpected, or malformed group IDs.
   - `test_synthetic_well_partition_and_technical_replicate_inseparability`: demonstrates that all 4 technical replicate wells of each condition group stay strictly together on one side of each split.
   - `test_synthetic_d6_d7_primary_exclusion_preserves_pfhxa_10_group`: demonstrates that under D-016 primary exclusion of wells D6 and D7, the provisional primary candidate pool has 70 wells and the `Exp3:PFHxA_10` condition retains 2 candidate wells (`D5`, `D8`), ensuring the group is preserved across all folds.
   - `test_split_samples_fail_closed_on_bad_inputs`: verifies rejection of missing or malformed sample group keys.
3. Created `docs/PHASE_B_LOGO_PLAN.md` documenting the 18-row group-to-fold mapping, replicate inseparability, provisional 70-well primary candidate counts, and mandatory evaluation rules:
   - Six-class PFAS classification requires pooled out-of-fold predictions and equal group weighting because validation folds each have only one true class.
   - Known-identity concentration regression has only two training concentration groups per analyte per fold and is exploratory.
   - Distinguishes static metadata and evaluation structures from physical measurements and unverified chemical ground truth.

**Exact execution and observed test results.**
- `uv run python -m unittest discover -s tests -v`: executed all 40 tests (32 prior tests + 8 test methods in `test_logo_plan.py`), 40 passed in 0.444s, exit code 0.
- `uv run python -m scientific_experiment_selection doctor`: passed with exit code 0 (`scientific_runs: none`).
- `python3 scripts/check_research_notebook.py`: verified append-only integrity of research notebook.

**Limitations and boundaries.**
- Static metadata and synthetic fixtures only; no raw laboratory workbooks (`.xlsx`) or private candidate manifests were accessed.
- Replicate independence across different conditions remains unverified (`preparation_group='UNKNOWN'`, `group_independence_verified=False`).
- Exp5 remains historically exposed and reconstructed; Exp8 remains locked pending exposure audit. Neither is included in this Exp3 LOGO plan.
- No machine learning models were trained, no hyperparameter search was conducted, and no model performance was estimated.
- No git commits, pushes, PRs, or training authorizations were made.

**Next step.** Stop for researcher and ChatGPT scientific/code review.


## Entry 022 — 2026-11-08 | Harden LOGO fail-closed validation and clarify per-fold metrics

**Question.** How to address the three fail-closed validation weaknesses identified in ChatGPT independent code review of Issue #19, and correct the overly broad characterization of per-fold single-class validation metrics, without altering the approved 18-fold LOGO architecture or touching private experimental data?

**Review feedback and identified vulnerabilities.**
1. Contradictory caller-supplied group metadata: `generate_logo_plan(groups=...)` accepted caller-provided dicts with mismatched metadata (e.g. `pfas_claim='PFNA'` on `Exp3:TFA_5`), trusting caller fields rather than deriving authoritative metadata from group IDs.
2. Incomplete training-group validation: `verify_fold_leakage` checked group count and disjointness from the validation ID, but did not enforce that training group IDs equal the exact canonical 17-group complement; altered training IDs (e.g. foreign experiment IDs like `Exp5:PFOA_10`) passed without error.
3. Loose numeric conversions and unverified sample metadata: `make_group_id('TFA', 5.9)` silently truncated float concentration to integer 5; `split_samples_by_fold` did not check consistency between optional sample metadata (e.g. `experiment_id='Exp5'`, `condition_claim='PFNA_20'`) and `technical_replicate_group='Exp3:TFA_5'`; and an arbitrary subset missing the held-out group could silently produce an empty validation partition without warning.
4. Overly broad documentation wording: stating that all per-fold multiclass metrics are "statistically invalid" overlooked valid single-class metrics (accuracy, true-class recall, proper loss), whereas the true methodological issue is that standalone six-class macro-F1, AUROC, and full confusion matrices are not suitable representations of multiclass performance when only one class is present.

**Implementation and hardening.**
1. Authoritative group validation (`validate_group_record`): all group records passed to `generate_logo_plan` or verified in fold records are checked against authoritative metadata parsed from the group ID (`parse_group_id`). Contradictory caller metadata raises `ValueError`.
2. Canonical complement enforcement in verifier: `verify_fold_leakage` now enforces that the set of training group IDs in every fold equals `canonical_18_groups - {validation_group_id}` exactly. Foreign, duplicate, non-canonical, or missing training IDs are rejected with detailed diagnostics. Redundant `training_groups` dicts and fold-level summary fields (`held_out_pfas`, `held_out_concentration_ppm`) are also verified for consistency.
3. Strict concentration typing and sample metadata cross-check:
   - `make_group_id` strictly rejects float/fractional concentrations (e.g. `5.9` or `5.0`), requiring exact integers or clean integer strings in `{5, 10, 20}`.
   - `validate_sample_metadata` cross-checks optional sample keys (`experiment_id`, `condition`, `condition_claim`, `pfas_claim`, `label_claim`, `concentration_ppm`, `concentration_claim_ppm`) against the group ID; contradictions fail closed.
   - Added `allow_empty_validation: bool = True` to `split_samples_by_fold` (documented as not validating dataset completeness by default) and added `validate_fold_evaluation_readiness` to explicitly confirm non-empty validation and complete 17-group training coverage before evaluation.
4. Corrected documentation: refined `docs/PHASE_B_LOGO_PLAN.md` Section 4.1 to clarify that standalone per-fold six-class macro-F1, AUROC, and confusion summaries are not suitable, while single-class accuracy/recall/loss remain calculable, and reconfirmed mandatory pooled out-of-fold predictions and equal group weighting for primary evaluation.
5. Added 5 synthetic negative test methods in `tests/test_logo_plan.py` (total 13 tests in suite) verifying rejection of float concentrations, contradictory caller group metadata, foreign/altered training sets, contradictory sample metadata, and empty validation/incomplete training readiness.

**Exact execution and observed test results.**
- `uv run python -m unittest discover -s tests -v`: all 45 tests passed in 0.457s (exit code 0; 32 baseline + 13 LOGO plan/leakage/hardening tests).
- `uv run python -m scientific_experiment_selection doctor`: exit code 0 (`scientific_runs: none`).
- `python3 scripts/check_research_notebook.py` validation: append-only check confirmed valid (`valid_append: True`).
- `git diff --check`: exit code 0.

**Boundaries.** No raw data or private manifests accessed; no models trained; work remains local on `feature/phase-b-logo-plan` without commit or push.
**Next step.** Submit updated five-file review package for follow-up ChatGPT review.


## Entry 023 — 2026-11-08 | Fix redundant sample metadata and readiness integrity guards

**Question.** How to resolve the two remaining validation weaknesses identified in ChatGPT's Draft PR #20 review (review 5820798245 / Issue #19 comment 6730328542) while preserving the five-file scope, LOGO design, and prior notebook history?

**Review feedback and identified gaps.**
1. Redundant sample metadata and fractional concentration truncation (`logo_plan.py:311–336`):
   - `sample.get('condition_claim') or sample.get('condition')` and `sample.get('pfas_claim') or sample.get('label_claim')` only validated the first truthy field when both were present, allowing contradictory pairs such as `{'condition_claim': 'TFA_5', 'condition': 'PFNA_20'}` or `{'pfas_claim': 'TFA', 'label_claim': 'PFNA'}` to pass.
   - `int(conc_num)` in `validate_sample_metadata` truncated float values such as `concentration_ppm=5.9` to `5`.
2. Evaluation readiness integrity and scope documentation (`logo_plan.py:393–435`):
   - `validate_fold_evaluation_readiness` did not call `verify_fold_leakage(fold_record)`, did not validate per-sample metadata via `validate_sample_metadata`, did not check for duplicate or overlapping physical well IDs (`physical_well` / `well`) within or across validation and training partitions, and did not validate or enforce its `expected_training_groups` parameter.
   - Documentation described the check as "dataset completeness" rather than condition-group coverage and metadata consistency.

**Implementation and fixes.**
1. Independent sample field validation and strict integer concentrations:
   - Added `_validate_exact_concentration` to reject `bool`, `float`/fractional values (e.g. `5.9`, `5.0`), and malformed strings across `make_group_id` and `validate_sample_metadata`.
   - Updated `validate_sample_metadata` to independently check every present field among `group_id`, `technical_replicate_group`, `experiment_id`, `batch_claim`, `condition_claim`, `condition`, `pfas_claim`, `label_claim`, `concentration_claim_ppm`, `concentration_ppm`, `physical_well`, and `well`.
   - Added `_extract_sample_well` to validate `physical_well` and `well` independently and reject disagreements when both are present.
2. Hardened `validate_fold_evaluation_readiness` and `split_samples_by_fold`:
   - `validate_fold_evaluation_readiness` now verifies `fold_record` via `verify_fold_leakage`, validates `min_validation_samples` and `expected_training_groups` (`17`), validates every validation and training sample via `validate_sample_metadata`, rejects duplicate or overlapping physical well IDs within and across validation and training sets, and rejects mixed presence/absence of well identifiers across samples.
   - `split_samples_by_fold` also rejects duplicate physical well IDs when present.
   - Updated docstrings and `docs/PHASE_B_LOGO_PLAN.md` Section 5 to state that `validate_fold_evaluation_readiness` establishes condition-group coverage and metadata consistency, not full 70-well physical plate completeness or verified chemical ground truth.
3. Focused negative synthetic tests in `tests/test_logo_plan.py`:
   - Expanded `test_rejects_contradictory_sample_metadata_and_fractional_concentrations` to test simultaneous contradictory `condition_claim`/`condition`, `pfas_claim`/`label_claim`, `experiment_id`/`batch_claim`, `physical_well`/`well`, and fractional/float `concentration_ppm` (`5.9`, `5.0`) and `concentration_claim_ppm` (`'5.9'`).
   - Added `test_readiness_rejects_corrupted_fold_samples_and_duplicate_wells` testing corrupted `fold_record`, corrupted sample metadata in `split_result`, duplicate physical wells in validation or training, overlapping physical wells between validation and training (`physical_well` vs `well`), inconsistent well key presence, and invalid `expected_training_groups`.

**Exact execution and observed test results.**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s tests -p test_logo_plan.py -v`: 14/14 tests passed in 0.019s (exit code 0).
- `uv run python -m unittest discover -s tests -v`: 46/46 tests passed in 0.465s (exit code 0; 32 baseline + 14 LOGO plan/leakage/hardening tests).
- `uv run python -m scientific_experiment_selection doctor`: exit code 0 (`scientific_runs: none`).
- `python3 scripts/check_research_notebook.py`: passed (`Notebook gate: dated append-only research entry found`).
- `git diff --check`: exit code 0.

**Boundaries.** No raw data or private manifests accessed; no ML models trained; no merge performed.
**Next step.** Push commit to `feature/phase-b-logo-plan` on Draft PR #20 and stop for final ChatGPT review.

## Entry 024 — 2026-11-08 | Propose Phase B pre-fit eligibility, metrics, and fixed baseline protocol

**Question.** With the researcher-approved Exp3 LOGO splitter merged in PR #20 (Issue #19), what must be scientifically decided before the first real supervised model fitting for Ce–ARS/PFAS identity and known-identity concentration prediction?

**Current evidence and boundaries.** Reviewed current published project charter, D-012/D-016/D-017/D-019, `docs/PHASE_A_REVIEW.md`, `docs/PHASE_B_LOGO_PLAN.md`, Issue #5, and merged source/software CI. Phase A documents 72 Exp3 individual-PFAS candidates (6 PFAS × 3 concentration conditions × 4 technical aliquots); D-016 excludes physical D6 and D7 in primary Phase B analysis, leaving **70 provisional candidates in 18 non-overlapping nominal shared-solution groups**. No independent chemical preparation verification exists for all nominal condition labels. All candidate source rows previously retained `physical_label_verified=False` and `training_authorized=False`. Exp5 is reconstructed and historically exposed; Exp8 remains intended locked holdout. No raw/private/Exp8 files were accessed for this proposal.

**Alternatives considered.**
- Promote historical condition labels to independently verified ground truth: **rejected** absent preparation/source evidence.
- Train immediately on all 72 Exp3 candidate wells using well-level K-fold: **rejected** because D6/D7 exclusion is researcher-approved and shared-solution technical replicates leak under well-level splitting.
- Require perfect independent preparation logs as an unconditional barrier to all future exploratory analysis: **not adopted as a new rule**; researcher may instead explicitly authorize a clearly labeled **provisional-label pilot** with strict scientific claims and no false verification flag.
- Predefine modest fixed baseline models/metrics using the accepted 18-fold LOGO infrastructure, then obtain a separate fitting approval: **proposed**, subject to researcher review.

**Proposed scientific protocol (NOT approved/frozen).**
1. **Exp3 eligibility audit**: Exp3-only metadata audit for 70 primary candidate wells, 18 groups, no blank/mix/QC samples, required spectral presence and consistent claimed PFAS/concentration/QC/source provenance; exclude only D6/D7 automatically. Do not silently alter other historical review notes or original labels. Confirm any additional source conflicts with researcher, never upload a private per-well manifest to GitHub.
2. **Classification primary metric**: mean held-out **condition-group accuracy** over 18 LOGO groups, each group equal weight (two-well PFHxA_10 group not suppressed). Given exactly three groups per PFAS, this also yields class-balanced recall. Secondary: pooled OOF **group-weighted macro-F1**, confusion matrix, per-class recall. Avoid pretending each individual technical well is an independent batch.
3. **Known-identity concentration regression primary metric**: mean condition-wise **MAE in ppm** over 18 LOGO groups; secondary condition-weighted RMSE and residuals by PFAS and concentration. Use separately known/claimed PFAS as oracle for this task, not model-predicted PFAS. Only two training concentration conditions per analyte in each fold; 5/20 held-out predictions are extrapolations and must remain exploratory.
4. **Model/representation scope**: four previously approved A Raw/full, B Raw/Compact8, C Area/full, D Area/Compact8 features; same 18 folds. Proposed fixed benchmark: most-frequent dummy vs regularized logistic regression (train-only scaling; fixed C=1.0) for identity; per-PFAS training-mean dummy vs Ridge (train-only scaling; fixed alpha=1.0) for concentration. Exact group/sample weighting, numerical choices and runtime dependency versions require protocol freeze before training. No search over hyperparameters in pilot.
5. **Selection bias**: Even if fixed folds are used, comparing four representations on the same LOGO development predictions and choosing a winner does not produce a final untouched generalization estimate. Exp5 may later give a qualified historically exposed transfer diagnostic; Exp8 must not be touched until its audit and explicit authorization.

**Decision status and execution.** The researcher instructed beginning this next phase; **the exact eligibility waiver, metrics, estimator specification and permission to fit have not yet been explicitly approved**. Proposed choices are in [Issue #21](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21). No new software, feature extraction, model, fit, prediction, metrics, private metadata, or chemical audit was executed. This is documentation/planning only. No alteration to `training_authorized` or `physical_label_verified`.

**Next action.** Obtain researcher sign-off on the provisional-label policy and protocol; then assign a bounded agent task for an Exp3-only metadata audit and, after passing separate fit-authorization gate, an initial fixed-parameter benchmark. Preserve original negative and uncertain evidence; report both observed tests and failures.

## Entry 025 — 2026-11-08 | Researcher approves use of historical Exp3 labels for a clearly provisional pilot

**Question and precise authorization.** The researcher was asked whether the historical PFAS identity and concentration claims for the **70 prospective primary Exp3 candidate wells** may be used in an explicitly labeled *provisional-label ML pilot*, without treating them as independently verified physical chemical identities. The researcher explicitly replied **“evet onaylıyorum.”** This approves the limited provisional-label **use policy**, and proceeding to a private/local **metadata-only Exp3 candidate eligibility audit**, not verified-label promotion or unconditional model training.

**Current source evidence and unresolved facts.** Phase A generated 72 nominal single-analyte Exp3 candidate rows covering six PFAS × 5/10/20 ppm with four technical aliquots per nominal condition. The earlier D-016 scientific decision excludes physical D6/D7 from primary analysis but retains original raw/QC/history and a frozen-protocol sensitivity path; 70 candidate wells remain **provisionally**, in 18 condition groups including retained D5/D8 (PFHxA_10). D-017 establishes from the researcher's first-hand account that technical replicate wells within each condition share a prepared solution, but does not verify independence between conditions. Original preparation records do not independently certify actual chemicals and all source rows previously retained `physical_label_verified=False` and `training_authorized=False`. Some historical review notes (e.g., B4/B5/C9) need explicitly documented treatment, not silent exclusion.

**Accepted interpretation.** An exploratory model may eventually estimate relationships between spectra and **nominal historical label claims**, with clear uncertainty disclosure and no claim that the trained model generalizes to independently re-prepared solutions/batches. The approval must not be read as converting a claimed label into verified chemistry, changing source/QC/well files, promoting any source flags, opening Exp8, or declaring measured ML performance.

**Alternatives and tradeoffs.** Insist on independent physically verified preparations for all training before any provisional analysis (more stringent but indefinite blockage); silently use historical labels as verified ground truth (scientifically unsound); or proceed with a carefully labeled provisional pilot plus eligibility audit and distinct evaluation gate (**researcher-approved third choice**). Avoid well-level leakage and keep original unverified evidence visible.

**Immediate next task — approved bounded use.** A dedicated Codex task may **read an existing local/private Exp3-only Phase A candidate metadata manifest** (not raw spectra or Exp5/Exp8 measurements), check exact candidate count, physical coordinate uniqueness, missing/conflicting claimed conditions, preserved historical QC/warnings and group membership, and report only redacted aggregated evidence. The exact 70 eligible wells must be reviewed prior to fitting. Any unexpected discrepancy is a stop, not a silent fix or extra well exclusion. Source flags remain untouched.

**Still proposed, not scientifically frozen.** Notebook Entry 024's group-equal accuracy, condition-weighted pooled F1/confusion, concentration MAE, dummy/logistic/Ridge settings and feature A/B/C/D comparison remain candidates for a separate pre-fit review. Neither a model nor a preprocessing fit is authorized by the present approval.

**Execution status and next gate.** No raw/private file was accessed by ChatGPT; no audit, software code, model fit, metrics, or scientific experiment was executed here. Approval and scope are recorded in [Issue #21 comment 6730714986](https://github.com/batuzunoglu/scientific-experiment-selection/issues/21#issuecomment-6730714986) and Decision D-020. Next: obtain private eligibility-audit handoff and then separately freeze model/metric protocol and authorize fitting.

## Entry 026 — 2026-11-08 | Issue #23 private Exp3 metadata eligibility audit

**Owner/authority/question.** Owner Codex; scientific reviewers researcher + ChatGPT.
Read AGENTS.md, AGENT_WORKFLOW.md, Issue #23 (no comments), D-020 and Entry 025.
Question: does inherited provisional Exp3 metadata support the expected primary
pool while preserving all uncertainty? Started from clean latest main after merged
PR #22, base `f08acbd`, dedicated `feature/phase-b-exp3-eligibility-audit`. No concurrent
writing agent was used. Scope permits private read-only metadata audit, synthetic
checks and a safe Draft PR after security/test gates; no training or merge.

**Rationale/alternatives.** Compared expected contract/count/group structure with
existing metadata claims. Did not promote provisional labels or require expected
unknown physical verification to become true. Only the previously approved primary
analysis exclusion is applied as a derived count; historical-note candidates remain
retained. Any new structural/claim/provenance discrepancy would stop for review,
not cause silent repair, relabeling or additional exclusion. No new scientific
approval, model/metric or split design selected; DECISIONS.md unchanged.

**Implementation/commands.** Added `scripts/audit_exp3_eligibility.py`, fabricated
synthetic fixtures/tests and `docs/EXP3_ELIGIBILITY_AUDIT.md`; appended this entry and
handoff checkpoint. Complete exact audit wrapper, CLI template, commands, public
allowlist and limitations are in that report. Private input: documented Phase A
candidate metadata, description only. Combined file is parsed locally and Exp3
selected before any validation/diagnostics; foreign rows never enter analysis,
logs or model context. No private source paths/digests, well-level records, original
source text, class-by-well assignments, spectra or private artifacts are reproduced.
The tool returns only fixed aggregate categories/counts and redacts CLI failures.
Source bytes compared before/after; flags/QC/labels not modified.

**Observed aggregate results.** 96 unique Exp3 coordinates; 72 original candidate
and 24 noncandidate records. Two analysis-only exclusions leave **70 provisional
primary candidates across 18 groups**, including two retained members of the special
reduced group. Three disclosed historical-note candidates remain included. Two
original candidate QC-review records preserved. All 96 records remain physically
unverified with source warnings; seven retain unresolved-conflict warnings and seven
retain historical-findings warnings (overlapping categories). **Zero new structural,
claim or provenance discrepancies**. Both local audit invocations exit 0; final
status `consistent-pending-scientific-review`. No row or flag is training-authorized.

**Software evidence and negative tests.** Baseline 46 tests passed. New synthetic
suite initially failed for missing module; later negative tests exposed incomplete
conflict/lineage/source-reference checks in the new audit and were fixed before
final run. No metadata repair. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest
discover -s tests -p test_exp3_eligibility.py -v`: 11 passed. Full command
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`: 57 passed,
exit 0. `synthetic_logo_check()` uses only canonical synthetic metadata: 18 folds,
18 distinct held-out groups, zero group overlap. No real-metadata folds/fits run.
Python 3.12.14, standard library only, deterministic/no seed. Tests use fabricated
fixtures, not hidden copies of real records.

**Limitations / stop.** Observed metadata/software checks, not new laboratory
measurements, simulations of chemistry, physical verification or performance.
Source provenance is checked internally; raw measurements are deliberately not
opened/rehashed. Historical-note disclosure does not validate preparations; group
independence remains unverified. No raw XLSX, Exp5 transfer, Exp8 measurements,
preprocessing fit, predictions, metrics or models accessed/performed. No scientific
label, original candidate/QC or authorization flag changes. Follow Issue #23's
staged privacy audit and allowlisted Draft publication; next ChatGPT/researcher
review of aggregate eligibility and remaining Issue #21 protocol must precede fitting.

**Pre-publication security result.** Exact five-file staged allowlist verified;
complete new diff reviewed. No raw/private/unrelated artifact, actual per-well
assignment, source text, private location/digest or detected credential pattern
in newly added content. Synthetic fixtures and issue-approved constants only.
Notebook/handoff append-only checks and staged whitespace check passed. Authorized
next step: commit/push safe five-file scope and open Draft PR; outcome and CI will
be reported in the PR handoff after observation. Stop at independent review.

## Entry 027 — 2026-11-08 | Issue #23 CI test-launcher portability correction

**Observed negative result.** First Draft PR #25 workflow run 42551592982 passed
the notebook gate but failed two new CLI tests: the tests invoked a local virtual
environment interpreter unavailable on the clean CI runner. This was a test harness
portability defect, not a private-data discrepancy or changed scientific result.

**Correction and evidence.** Reproduced the two launcher errors using copies of
only public source/scripts/tests in an isolated temporary directory without a local
virtual environment. Changed only the test subprocess interpreter to `sys.executable`.
Audit implementation, private input, real aggregate results and scientific flags
unchanged; private metadata was not reopened. After the fix, both the clean copied
suite and repository suite passed all 57 tests. Exact repository command:
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`.
The copied-suite check invokes the same `-m unittest discover -s tests -v` arguments
with `sys.executable` and bytecode disabled, after copying only the three public code,
script and test directories. Only synthetic fixtures are used. No model/Exp8/raw
access, no decisions modified. Original Entry 026 retained. Reaudit the same five-file
publication scope and push correction to the existing Draft; stop for review.


## Entry 028 — 2026-11-08 | Fix research-notebook CI race when ready_for_review overlaps PR merge

**Owner, authority, and question.** Owner: Antigravity; reviewers: ChatGPT + researcher ([Issue #24 comment 6731003297](https://github.com/batuzunoglu/scientific-experiment-selection/issues/24#issuecomment-6731003297)). Started from clean `main` at `424ea813a9e96acd9085236054a903ffdb00a697` on dedicated branch `fix/notebook-gate-merge-race`. Question: how can `scripts/check_research_notebook.py` eliminate false-negative CI failures when a `ready_for_review` workflow run overlaps a squash or normal merge of the same PR, while preserving strict append-only enforcement and failing closed on invalid or ambiguous baselines?

**Observed CI failures and root cause.** In GitHub Actions run `42550850591` (PR #22, head `52d1303`) and run `42552272582` (PR #25, head `4036d03`), earlier CI runs on the identical PR head SHAs passed both the notebook gate and unit tests, but the `ready_for_review` workflow triggered moments before PR merge failed at `Require dated research notebook entry` with `ERROR: No new notebook content was appended.` During `actions/checkout@v4`, `HEAD` was checked out at the PR's synthetic merge commit (`refs/pull/<N>/merge`, merging PR head into pre-merge `main`), whereas `origin/main` in the fetched repository had already advanced to the post-merge `main` commit containing the PR's new notebook entries. Because `scripts/check_research_notebook.py` computed changed paths using `git diff origin/main...HEAD` (three-dot merge-base semantics, which saw the PR's research changes relative to pre-merge `main`) but loaded `old` via `git show origin/main:docs/RESEARCH_LAB_NOTEBOOK.md` (branch-tip semantics, which read the post-merge notebook), `old` and `new` were identical (`added == ""`), causing a false negative.

**Evaluation of alternative baseline strategies.**
1. *Mixing `origin/main...HEAD` with `origin/main:<path>` (previous code):* Vulnerable to any advancement of `origin/main` between PR merge-ref creation and checkout.
2. *Naive `git merge-base origin/main HEAD` for both diff and file retrieval:* Works when `origin/main` advances via a **squash merge** $S$ (parent $B$), because $S$ and the PR synthetic merge commit $M_{\text{pr}}$ (parents $B, F$) share only $B$. However, it **fails after a normal (`--no-ff`) merge commit** $M_{\text{main}}$ (parents $B, F$), because both $B$ and the feature tip $F$ are common ancestors of $M_{\text{main}}$ and $M_{\text{pr}}$, so `git merge-base` returns $F$ (the feature branch tip) rather than the pre-merge base $B$. Comparing $M_{\text{pr}}$ against $F$ would either yield an empty diff (silently bypassing the gate) or compare the notebook against itself.
3. *Immutable event base SHA (`GITHUB_BASE_SHA`) + `refs/pull/<N>/merge` first-parent (`HEAD^1`) verification with `merge-base` fallback (selected):*
   - Pass `GITHUB_BASE_SHA: ${{ github.event.pull_request.base.sha }}` in `.github/workflows/research-notebook.yml` so CI supplies the immutable pre-merge base SHA from the PR event payload; fall back to `origin/<GITHUB_BASE_REF or main>` when unset.
   - In `resolve_base_commit()`, verify the target ref resolves to a valid commit object (`^{commit}`). Inspect `HEAD`'s parents (`git rev-list --parents -n 1 HEAD`). When `HEAD` is a two-parent PR synthetic merge commit `(P1, P2)` where `P1` (`HEAD^1`) is on the target base history (`is_ancestor(P1, target_ref)`) and `P2` (`HEAD^2`) is the PR head (`not is_ancestor(P2, P1)`), use `P1` directly as `base_commit`. Because commit parents are immutable in the Git object graph, `P1` remains the exact pre-merge `main` commit regardless of whether `origin/main` subsequently advances via squash merge or normal merge.
   - For single-parent branch checkouts (or feature branches that merged `main` into themselves), use `git merge-base <target_ref> HEAD`.
   - Use the single resolved `base_commit` for both `git diff --name-only --diff-filter=ACMR <base_commit> HEAD` and `git show <base_commit>:docs/RESEARCH_LAB_NOTEBOOK.md`.
   - Fail closed (exit code 2) if the target ref is missing/invalid or if `base_commit == head_sha`, preventing silent bypass when comparing an already-merged branch head against post-merge `origin/main` without a distinct pre-merge base.

**Implementation and synthetic Git-history regression tests.**
- Updated `.github/workflows/research-notebook.yml`, `scripts/check_research_notebook.py`, and `tests/test_research_notebook_gate.py`.
- Preserved the 5 existing unit tests and added 8 synthetic Git-history tests in `tests/test_research_notebook_gate.py` (13 total in module):
  1. Unmerged PR with genuine dated append passes (both branch checkout and `refs/pull/1/merge`).
  2. `refs/pull/1/merge` checkout after `origin/main` advances from a **squash merge** passes (both with and without `GITHUB_BASE_SHA`).
  3. `refs/pull/1/merge` checkout after `origin/main` advances from a **normal (`--no-ff`) merge commit** passes (verifying naive `merge-base` would have returned `feature_sha`, while `resolve_base_commit` returns `base_sha`).
  4. Research code change without a notebook append fails (exit code 1).
  5. Rewriting/deleting historical notebook content fails (exit code 1).
  6. Undated/malformed appended heading fails (exit code 1).
  7. Plain non-research documentation change (`README.md`, `docs/HANDOFF.md`) passes without requiring a notebook entry (exit code 0).
  8. Missing/invalid `GITHUB_BASE_SHA` or identical `base_commit == HEAD` fails closed (exit code 2).

**Exact commands and observed results.**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s tests -p test_research_notebook_gate.py -v`: 13/13 passed in 0.217s (exit 0).
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`: 65/65 passed in 0.751s (exit 0).
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor`: exit 0 (`scientific_runs: none`).
- `git diff --check`: exit 0.

**Limitations and boundaries.** CI quality-gate engineering only. No scientific code, dataset contracts, eligibility rules, labels, or decisions modified; no raw XLSX, `data/private/**`, or Exp5/Exp8 files accessed; no ML models trained. Next: open Draft PR against `main` and stop for ChatGPT review (do not mark ready-for-review or merge).


## Entry 029 — 2026-11-09 | Fix PR notebook gate false-pass when main advances between event base and synthetic merge checkout

**Owner, authority, and question.** Owner: Antigravity; reviewers: ChatGPT + researcher ([PR #26 review 5821207205](https://github.com/batuzunoglu/scientific-experiment-selection/pull/26#pullrequestreview-5821207205) and [Issue #24 comment 6731187621](https://github.com/batuzunoglu/scientific-experiment-selection/issues/24#issuecomment-6731187621)). Branch: `fix/notebook-gate-merge-race` (updating Draft PR #26 against `main` at `424ea813a9e96acd9085236054a903ffdb00a697`). Question: how do we prevent a false-pass in `scripts/check_research_notebook.py` when `main` advances from the event base `GITHUB_BASE_SHA = B` to a newer commit `N` (containing an unrelated notebook entry) *before* `refs/pull/<N>/merge` is checked out (`M = (N, F)`), while preserving the post-squash and post-normal merge race fixes from Entry 028?

**Reproduced blocking edge case (negative finding in commit `0879b7f`).** In commit `0879b7f1664b3dc5e4a18c07f1f559bec37673e0`, `resolve_base_commit()` selected the synthetic merge first parent `P1` (`parents[0]`) only when `is_ancestor(P1, target_ref)` was true. When `target_ref` was set to `GITHUB_BASE_SHA = B`, and another PR updated `main` from `B` to `N` (appending a legitimate unrelated notebook entry) before `actions/checkout@v4` fetched `refs/pull/<N>/merge`, GitHub's synthetic merge commit `M` had parents `(P1 = N, P2 = F)`. Because `N` is a descendant of `B` rather than an ancestor (`is_ancestor(N, B) == False`), `resolve_base_commit()` fell back to `git merge-base(B, M) == B`. Comparing `B -> M` included the unrelated `main` notebook append from `B -> N`, causing a feature branch `F` that modified research code *without* any notebook entry of its own to falsely pass the gate.

**Resolution and merge-shape verification.**
1. Added `same_base_history(commit_a, commit_b)` in `scripts/check_research_notebook.py` (`is_ancestor(commit_a, commit_b) or is_ancestor(commit_b, commit_a)`).
2. In `resolve_base_commit()`, when `HEAD` is a two-parent PR synthetic merge commit `(P1, P2)`, select `P1` (`parents[0]`) when `P1` and `target_ref` belong to the same base-history line in **either direction** (`same_base_history(parents[0], target_ref)`), `P2` is not an ancestor of `P1` (`not is_ancestor(parents[1], parents[0])`), and (when `GITHUB_HEAD_SHA` is supplied) `HEAD` descends from `GITHUB_HEAD_SHA` with `P2` descending from `GITHUB_HEAD_SHA` and `P1` not descending from `GITHUB_HEAD_SHA`.
3. Passed `GITHUB_HEAD_SHA: ${{ github.event.pull_request.head.sha }}` alongside `GITHUB_BASE_SHA` in `.github/workflows/research-notebook.yml`, failing closed (exit code 2) if either SHA is invalid or not in `HEAD`'s ancestry.
4. Added two end-to-end synthetic Git-history regression tests in `tests/test_research_notebook_gate.py` (plus invalid `GITHUB_HEAD_SHA` fail-closed verification in `test_git_missing_or_identical_base_fails_closed`, bringing the module to 15 tests and the full suite to 67 tests):
   - `test_git_pr_merge_ref_rejects_missing_entry_when_main_advances_after_event_base`: models `B -> N` (with unrelated Entry 002 on `main`), `B -> F` (research code change in `scientific_experiment_selection/model.py` without any notebook entry), and synthetic PR merge `M = (N, F)` under `GITHUB_BASE_SHA = B`. Verifies `resolve_base_commit() == N` and `check_repo() == 1` (`require an appended`), not `0`.
   - `test_git_pr_merge_ref_passes_when_main_advances_after_event_base_and_pr_appends_own_entry`: positive counterpart with the same topology where `F` genuinely appends its own dated Entry 003; verifies `resolve_base_commit() == N` and `check_repo() == 0`.

**Exact commands and observed results.**
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s tests -p test_research_notebook_gate.py -v`: 15/15 passed in 0.317s (exit 0).
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`: 67/67 passed in 0.819s (exit 0).
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection doctor`: exit 0 (`scientific_runs: none`).
- `git diff --check`: exit 0.

**Limitations and boundaries.** CI quality-gate engineering only within the same five-file scope. Entry 028 preserved unchanged; no scientific code, dataset contracts, eligibility rules, labels, or decisions modified; no raw XLSX, `data/private/**`, or Exp5/Exp8 files accessed; no ML models trained. Next: push to Draft PR #26 and stop for ChatGPT review (keep Draft and unmerged).

## Entry 030 — 2026-11-09 | Synthetic-only next-experiment selection MVP

**Owner, question and authority.** Codex implements Issue #27; scientific reviewers
ChatGPT + researcher. Read project/agent workflow, binding D-012/D-016/D-017/D-019/
D-020, notebook and Issue #21 discussion. Researcher approved direction (TFA versus
non-TFA, selection of conditions under budget) and explicitly requested this
synthetic-only scaffold, not real-data fitting. Dedicated branch
`feature/synthetic-experiment-selection-mvp` starts at exact approved main base
`aaf8ca8`. No concurrent writing agent or private-source access.

**Scientific explanation / alternatives.** A next-measurement policy must act before
knowing the measured spectrum. Random and nominal design coverage need prospective
settings only; ordinary uncertainty on hidden candidate spectra would peek. Implemented
Random and elementary factor-level coverage, with a refusing uncertainty stub until
budgeted screening or validated surrogate information gets scientific approval.
Selectors receive designs/acquisition metadata/budget only, never oracle outcomes
or holdout scores. No decision-register, spectral formula or scientific label changes.

**Implementation choices for review.** `selection.py` has frozen synthetic candidate,
replicate/group/scenario/budget contracts, one-shot oracle, selector/model protocols,
seeded Random, deterministic greedy nominal-level novelty (ID tie break), sequential
whole-condition acquisitions and separate fixed evaluator. Integer positive costs
are synthetic units; zero budget records baseline only. Conditions, not technical
wells, are the acquisition unit. Initial/acquisition/holdout group IDs are disjoint.
Training hooks receive grouped outcomes and per-well weights with equal group totals;
that engineering normalization does not freeze a real estimator protocol. A fake
spectrum-agnostic weighted-mean adapter exercises fit/predict only. Evaluator predicts
on a deep copy so ordinary predict mutations do not feed evaluation data back to
learner state; no evaluator result reaches selector inputs. Curves/logs record
budget, seed, actions and condition-equal toy accuracy from zero acquisitions.

`selection_demo.py` builds only fabricated synthetic constants; paired runs use
identical initial/pool/holdout, cost schedule, budget and fresh policies/adapters.
`docs/SELECTION_MVP.md` specifies architecture, access boundaries, DoE rule, weight
convention and caveats; a short implementation plan accompanies it. No data readers,
real models, runtime dependencies or feature framework added.

**Observed executions / negative evidence.** New test module failed initially
because selection.py did not exist. After implementation, 19 synthetic test methods
cover immutability, unique/disjoint groups, no peeking, invalid/duplicate/holdout
selection, one-shot whole-group reveal order, positive/zero/insufficient budgets,
equal group totals, run/order determinism, seed and actual-cost logging, fixed
holdout isolation, counterfactual outcome invariance and uncertainty refusal.
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_selection.py -v`
passed 19 tests. Demo command
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.selection_demo --seed 7 --budget 3`
ran successfully with three one-unit acquisitions and a zero-acquisition starting
point per method. These are synthetic software demonstrations, not measured
experimental performance or a calibrated chemical simulator. Full-suite/gate/privacy
verification recorded below before publication. Python 3.12.14, standard library,
explicit demo seed 7 (other synthetic seeds in tests), no stochastic real experiment.

**Limits / next review.** Greedy coverage is not optimal experimental design;
uncertainty remains nonexecuting. Canonical group IDs must truthfully represent
shared preparations; alias detection/physical independence is not established.
Pure Python boundaries are not a sandbox against malicious introspection/global
state or externally captured oracle objects. Returned curves can only remain a
valid evaluation if not reused for tuning. Adapters must support deepcopy; no
laboratory transactions/recovery. Integer costs, fake model and toy diagnostic are
engineering choices, not frozen real benchmark settings. No Exp3/5/8 files,
private manifests, spectra or measured outcomes accessed, no real models fitted,
no preprocessing change or real benchmark result claimed. Safe code/synthetic tests/
docs Draft PR only; stop for ChatGPT/researcher review, no ready/merge/training.

**Final local verification.** Full command
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
passed **86/86 tests** (67 prior + 19 new), exit 0. Final demo was repeated twice
with seed 7/budget 3; stdout byte-identical, both methods have cumulative cost points
0/1/2/3 and three distinct condition acquisitions. No effectiveness comparison is
inferred from the fake adapter's toy scores. `git diff --check` passed. Safe eight-file
code/test/docs scope only, prior notebook/handoff/learning bytes preserved, decision
register unchanged. Before Draft publication, exact staged allowlist/full diff and
secret/path/data exclusion audit must pass; actual PR/CI outcome will be reported
in the PR handoff after observation. No model or real-data access authorization.

## Entry 031 — 2026-11-09 | Synthetic Logistic Regression NES integration

**Owner/authority.** Codex, Issue #29; scientific reviewers ChatGPT + researcher.
Read AGENTS/workflow, required decisions and latest Issue #21 approvals (6749253141,
6749392851, 6749605069). Dedicated `feature/synthetic-logistic-nes` from latest main
`861e07e` after PR #28. Approval covers the synthetic implementation and Draft PR,
not real measured-data access/fitting, eligibility certification or merge.

**Question/rationale.** Exercise the approved binary learner, train-only weighting/
scaling, fixed acquisition/evaluation split and condition-aware metrics with existing
Random/DoE engine. Unlike the fake mean adapter, optional scikit-learn Logistic
Regression learns only from fabricated spectral arrays. Preserve all four planned
representations; start B Raw/Compact8, no blank/baseline/area correction in B.
Standard-library scaffold remains usable without optional ML libraries.

**Implementation.** New public nominal-protocol/synthetic generator/metric module,
lazy optional LR adapter, paired demonstration and 16 synthetic tests. Engine gains
an explicit condition-balanced evaluation mode, preserving default accuracy behavior
and oracle/selector/budget/holdout guards. Optional requirements pin numpy 2.2.6,
scipy 1.15.3, scikit-learn 1.7.2, joblib 1.5.2 and threadpoolctl 3.6.0. Dedicated
CI installs/verifies pins before full tests/demo; old standard-library job unchanged.
No spectral formula, decision-register, historical eligibility or source-flag edits.

Approved constraints: binary TFA=1/other=0, LR L2/C=1.0/class_weight=None; weighted
training-only StandardScaler and condition-equal fitting. Fixed engineering solver
settings for review: lbfgs/max_iter=5000/random_state=0/tol=1e-4/intercept=True,
no warm start, native thread limit 1. No hyperparameter search. Every acquisition
recomputes per-well N/(G*n_group), fits a fresh scaler and classifier on initial+
already acquired whole groups only, and logs training provenance/convergence.
A feature/convergence failure aborts without dropping samples or changing recipe.

**Split/evaluation.** The public six-holdout/twelve-acquisition nominal assignment
from Issue #21 is encoded and validated before the demo, using synthetic prefixes
and fabricated analytic Gaussian curves only. Initial fixture has 18 groups/70
rows; acquisition 12/35; fixed evaluator 6/18. These illustrate public design counts,
not a private manifest or real-world preparation certification. Each class recall
averages correctness within conditions first, then equally over same-label conditions;
BA is mean sensitivity/specificity. Missing class is an error, not a fabricated
score. Every curve includes all costs 0–12, with whole-condition unit acquisition
cost. Evaluator uses a deep-copied fitted model; no scores/features enter selectors.
Uncertainty remains blocked. D-019 LOGO is a separate protocol, not run here.

**Exact commands / observed results.** Full reproducible installation/demo/test
commands, model details, exact synthetic curves and caveats are in
`docs/SYNTHETIC_LOGISTIC_NES.md`. Executed:
- `uv pip install --python .venv/bin/python -r requirements/logistic.txt`: exact five
  optional packages installed; no real datasets or models downloaded.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_logistic_nes.py -v`:
  16 passed. Initial missing-module failure preceded implementation; negative tests
  include convergence and bad-transform errors as expected failure cases.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`:
  102 passed (86 existing + 16 new), no skips with optional dependencies installed.
- In a clean venv created with `venv.EnvBuilder(with_pip=False)`, same unittest
  arguments passed all available tests: 102 run, 10 ML-dependent tests skipped.
- Full B-arm `demonstrate()` default (equivalent to
  `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.logistic_demo --arm B --budget 12 --seeds 7 11 19`)
  completed four runs, each with 13 scaler/classifier fits (baseline+12 acquisitions).

**Synthetic observations, not chemical results.** All four BA curves start at 0.5
and end at 1.0. For seeds 7/11/19 and DoE respectively, BA remains 0.5 until cost
6/4/1/6 and then is 1.0; every checkpoint and seed is retained in the report.
Specificity stays 1.0; sensitivity changes from 0 to 1. These are computations on
one predeclared fabricated fixture, not proof of laboratory gains or a winning
selector. Generator constants were not changed to improve held-out scores.
The one positive evaluator condition creates severe condition-level uncertainty.

**Limits/next.** No real Exp3/5/8 files, private manifests, experimental spectra,
source labels or outcomes accessed; no actual-spectra fitting/metrics, new chemical
claims or benchmark tuning. Pure Python boundaries assume trusted adapters/canonical
IDs and cannot sandbox malicious introspection/global state. Optional pins constrain
reproducibility; other platforms need independent numerical checks. All four arms
are supported/tested, but only B budget curves reported, with no arm selection by
holdout score. Separate real access/eligibility/fitting and future Exp8 audit gates
remain. After final notebook/privacy/whitespace checks, open Draft only and stop
for ChatGPT/researcher scientific and code review.

**Final local verification.** Exact documented B-arm CLI executed twice with
--budget 12 --seeds 7 11 19; stdout byte-identical and every run contains cost
checkpoints 0–12 and 13 refits. Final full suite 102/102 passed after adding explicit
weighted-scaler variance verification; no skips with pinned dependencies installed.
Whitespace passed. Publication scope is 11 public code/test/workflow/requirements/
documentation files only; no raw/private artifacts. Prior notebook/handoff bytes
must remain intact; decisions, spectral formulas and standard-library fake demo
unchanged. Complete staged privacy/credential/path audit and notebook gate precede
Draft handoff. CI/PR outcome will be reported after actual observation, not assumed.

## Entry 032 — 2026-11-09 | Issue #31 existing-label to raw-column consistency check

**Owner/scope.** Codex; reviewers researcher + ChatGPT. Read updated Issue #31,
its supplemental comment, Issue #21 approvals and the required project/agent/source
reports. Latest main after PR #30, base `5ae57fb`; dedicated branch
`feature/exp3-exp5-raw-label-join`. Authorized bounded read-only join of the existing
mapping to Exp3/5 raw columns, not label reconstruction, fitting or Exp8 access.

**Reference / alternative.** Three preferred source options (compact attachment,
original all-wells and supplemental exact supervised-classification workbook) were
absent in the documented local source folder. Used the explicitly permitted existing
historical Step4 Well_Metadata fallback. No home crawl, source import or unnecessary
historical archaeology. Only that metadata sheet was parsed, not prediction/score
sheets. Existing labels/roles were the reference; no spectral shape inferred chemistry.
This does not independently certify the exact historical fitted y-vector lineage
or wet-lab identities. The source's historical assertions remain assertions.

**Implementation and actual result.** Small standard-library join module keyed by
experiment and physical well, with approved analysis-only exclusions, frozen 12/6
Exp5 role assignment, raw hash/header/grid/finite-176-point/presence checks and
metadata claim/group/role checks. Original source labels/QC and eligibility flags
not edited; no model-use flag used alone for inclusion. Read-only checks passed:
**70 training / 35 acquisition / 18 holdout / 3 excluded**, 123 included columns
matched, group counts 18/12/6, **zero mismatch categories**. Source bytes unchanged.
No per-well report, private digest/path, label map or raw/feature arrays exported.
Having passed the bounded join, source investigation stopped as instructed.

**Commands and software evidence.** Exact redacted CLI, source-resolution wrapper,
source description, limitations and full test commands in RAW_LABEL_JOIN_AUDIT.md.
Actual join CLI exited 0. New suite command
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_raw_label_join.py -v`
passed 7 synthetic tests. Full
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
passed 109 tests (102 existing + 7 new). Initial missing-module failure preceded
implementation. Negative tests cover schema/provenance/join/role failures and
redaction using fabricated workbooks only. Python 3.12.14, no new dependency/seed.

**Status / limits / next.** Observed file/metadata consistency, not new measured or
simulated chemical results. No actual-spectrum model fitting, metrics, preprocessing
or held-out outcome selection. No Exp8 workbook/row inspection. Labels are the
researcher-endorsed provisional analytical reference, not newly physically verified.
No original source, exclusion, formula, model protocol or scientific decision changes.
Five safe code/test/doc files only for Draft review after staged privacy/notebook/
whitespace checks; prior entries preserved. Next researcher + ChatGPT reviews the
aggregate join and then separately decides on actual Exp3/Exp5 pilot fitting.

## Entry 033 — 2026-11-09 | Archive researcher Exp3–Exp8 label master privately, register checksum publicly

**Question and authorization.** Researcher uploaded `CeARS_All_Experiments_Exp3_to_Exp8_Well_Label_Master(1).xlsx` and asked to preserve it for future experiment work, explicitly deferring supervised model fitting. The GitHub repository is public, and the existing project workflow protects provisional well-level mappings/private data. Therefore the original workbook was saved **unchanged in private ChatGPT File Library**, while the public GitHub change is **only a safe locator/checksum register**; do not mistake the latter for a copy of the workbook or a link accessible to Codex.

**Evidence and verification.** File SHA-256 `68cf034687f167fac1c5b881c95a140e87b33cdf8b61ef75db839f1b4c556761`, 164,473 bytes. Imported the uploaded workbook read-only: 10 sheets, including `ALL_WELLS` with 576 records (96 per experiment Exp3–Exp8). Compared 288 overlapping Exp3/Exp5/Exp8 source rows with the earlier uploaded combined mapping on 23 common fields: zero discrepancies. Compared 123 currently included Exp3/Exp5 pilot rows with the saved private pilot mapping on well/condition/replicate and QC/presence fields: zero discrepancies. These checks compare **source assertions**, not independently confirmed preparation chemistry. No UV–Vis model fit, feature extraction, experimental measurements, tuning or Exp8 training occurred.

**Storage and safeguards.** Private archive: `/Scientific_Experiment_Selection/CeARS_All_Experiments_Exp3_to_Exp8_Well_Label_Master_original.xlsx`. Existing private reference: `/Scientific_Experiment_Selection/Exp3_Exp5_Pilot_Label_Map.xlsx`. New public register: `docs/EXPERIMENT_LABEL_MASTER_REGISTER.md`; no actual well-level master, private manifests or raw spectra included in the public repository. Archive may contain Exp8 labels but **Exp8 remains locked and unused**. `verification_status=Verified` belongs to the supplied workbook and is not a new independent physical verification claim.

**Next step/permission.** Resume from the verified Exp3 70 / Exp5 acquisition 35 / Exp5 fixed holdout 18 pilot boundary. When the researcher later expressly authorizes actual-spectra fitting, supply/copy the verified private dataset into Codex's offline controlled workspace, validate file SHA-256, obey the frozen group split and provenance/exclusion rules, and do not commit source workbooks to public GitHub. No current model-training or public-release authorization is inferred from this archival request. Documentation-only Draft PR awaits review/merge.

## Entry 034 — 2026-11-09 | Issue #34 controlled measured Exp3→Exp5 NES pilot

**Owner/question/authority.** Codex; scientific and code reviewers researcher +
ChatGPT. Read Issue #34 and latest Issue #21 approval 6752036077, AGENTS/workflow,
charter, decisions, notebook/handoff, prior join audit and synthetic LR protocol.
Dedicated branch `feature/measured-exp3-exp5-pilot`, latest main `8beacead30c6fd9e33ccaf7454f67fed46ddd0cb`
after reviewed PR #32. Narrow authorization is actual local retrospective binary
TFA/non-TFA fitting/evaluation on the previously validated Exp3/5 mapping, followed
by safe Draft publication and review. No new scientific decision or merge authority.
Entry 033 is reserved for the separate optional archival documentation PR; its
branch/register is untouched. All earlier notebook entries remain byte-for-byte.

**Design/alternatives/why.** Issue #34 explicitly requires a measured-specific
loader/adapter rather than weakening synthetic guards or misnaming actual batches
as synthetic. Reused the read-only raw/join checks, frozen feature functions,
existing Random/DoE selectors and budget state. Extracted only numeric weighted LR
fit and condition-score arithmetic for shared use, retaining synthetic wrapper
validation. No spectral formula, split, reward, label, source flag, model setting,
seed or exclusion changed. Required exact frozen 70/35/18 counts, 18/12/6 groups,
three exclusions, source claims/checksums/grid and complete transforms before fit.
No label archaeology or fresh reconstruction. Known audited Step4 metadata remains
the existing local reference, distinct from independent physical verification.

**Approved scientific recipe.** B Raw/Compact8 first; A raw/full, C area/full and D
area/Compact8 subsequently, with identical roles and fixed parameters. Fresh weighted
StandardScaler + L2 LR C=1, class_weight=None, lbfgs, max_iter=5000, tol=1e-4,
random_state=0, fit_intercept=True, warm_start=False and existing exact dependency
pins. Both fit steps use `N/(G*n_group)`, recomputed after each complete condition.
Random seeds 7/11/19 and deterministic nominal DoE, checkpoints/cost 0–12, one
whole condition per proxy unit. DoE novelty is within acquisition history only.
Evaluator predicts on copied models, averages well correctness within condition
then within class, and records BA/sensitivity/specificity privately. No evaluator
feedback reaches selectors/scaling/weighting or method choice.

**Observed actual measured-data execution, separate from synthetic tests.** Ran
one local B-first then A/C/D protocol. CLI exit 0, 16 full trajectories and **208
fresh converged fits**. All **123 included wells** transformed in each arm. No
additional exclusions or source edits; before/after source hashes unchanged. Private
artifact consistency checks passed: 13 checkpoints/run, 12 unique acquisitions,
paired orders across representations, 70 initial and 105 final training wells,
identical per-arm baseline/final metrics across policies and correct BA arithmetic.
These are actual computations on previously measured spectra, not new physical
experiments, a calibrated simulation or evidence of policy superiority. Complete
measured trajectories and all models/predictions remain private; no real metric
values, spectra, per-well map or source digest/location are published in this entry.

**Exact commands / evidence.** Runnable source-variable CLI and full protocol are
in MEASURED_PILOT.md. Actual local wrapper resolved only the two documented roots
and exact prior Step4 relative location; no home search or Exp8 open. Private
reproduction record retains resolved interpreter/argv/environment, hashes, code
hashes, versions, authorization and input mapping. Private aggregate REVIEW.md
contains every arm/policy/seed BA, sensitivity and specificity checkpoint without
per-well exports; detailed JSON and 208 fitted checkpoints remain ignored locally.
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
initially passed **121/121** after implementation (109 prior + 12 new). Final checks
are appended below after observation. New tests use analytic synthetic spectra and
fabricated workbook mappings only. Initial new-module import failure preceded code.
A separate no-ML run exposed one test assertion invoking the optional adapter without
dependencies; guarded that assertion on ML availability, leaving implementation and
measured execution unchanged. Clean standard-library command
`PYTHONDONTWRITEBYTECODE=1 /tmp/issue34-stdlib-env/bin/python -m unittest discover -s tests -v`
passed **121 tests, 16 optional ML skips**. No actual data fitting in public CI.

**Limitations/next decision.** Historical labels remain researcher-endorsed
provisional analytical references, not independently proven physical solutions;
source authorization/verification assertions remain unchanged and pilot authority
is separate. Exp5 is historically exposed and retrospective, with only one positive
evaluator condition; correlated technical wells do not give independent conditions
or confidence/generalization guarantees. Budget is a proxy, not measured laboratory
cost. No holdout tuning, uncertainty policy, LOGO task, Exp8 access or private GitHub
upload. Trusted Python interfaces are not a hostile-code security sandbox. Publish
safe code/synthetic tests/method docs only after final privacy, notebook and tests;
open Draft and stop for ChatGPT/researcher review of both code and private aggregate
trajectories. Do not merge or choose a best arm/seed/checkpoint using this holdout.

**Final local verification.** Full optional-ML suite after the test-only portability
correction: **121 tests in 19.257s, OK, exit 0**, no skips. Clean standard-library
suite: **121 tests in 1.559s, OK (skipped=16), exit 0**. `git diff --check` exited 0;
byte-prefix checks against origin/main confirmed all prior notebook/HANDOFF text
preserved and `valid_append` accepted the dated entry. Measured implementation code
is unchanged from the recorded actual execution. Eight-file public allowlist and
staged privacy check precede feature-branch commit; GitHub notebook/ML CI outcomes
will be reported only after observation. No merge.

## Entry 035 — 2026-11-09 | Authorized sanitized measured-results publication

**Question/owner/approval.** Owner Codex; reviewers researcher + ChatGPT. The latest
researcher instruction on PR #35 (comment 6753082959) explicitly authorizes public
aggregate measured performance so ChatGPT can review complete trajectories directly
in GitHub. This supersedes Entry 034's private-only **score reporting** boundary;
it does not authorize private inputs/outputs, new fitting, tuning, label changes,
Exp8 access or merge. Read the full instruction and preceding scientific review.
Continue the existing feature branch, preserving all prior notebook entries. PR
#33's separate Entry 033 remains on its untouched branch; future authorized notebook
reconciliation must retain both histories before any merge.

**Alternatives/why.** Copying the private report wholesale was rejected by the
instruction. Implemented an explicit deterministic allowlist exporter that reads
only the completed aggregate REVIEW.md and run summary, constructs static arm/
representation/policy/seed labels and numeric checkpoint scores, and discards all
private prose and non-score fields. Published both human-readable
MEASURED_PILOT_RESULTS.md and machine-readable aggregate JSON for review/reuse.
Six decimal places match the original report; the full-precision run summary is
rounded to that precision for comparison, without rerunning any model. DoE's
runner name `coverage` is displayed as DoE/nominal coverage; deterministic seed is
JSON null. Selected-condition sequences are intentionally omitted as unnecessary.
No private file was copied wholesale; no requested aggregate artifact was omitted.

**Observed measured results (existing run, not synthetic).** Published all **16
trajectories × 13 checkpoints**, with acquired condition count, cumulative proxy
cost, BA, sensitivity and specificity. All B and D checkpoints have BA 0.500000,
sensitivity 0.000000 and specificity 1.000000. A's common baseline/final BA is
0.933333/0.833333; C's is 0.900000/0.600000. All intermediate fluctuations and all
three Random seeds plus DoE are retained in the result files. These are descriptive
retrospective measured Exp3→Exp5 model results, not new physical experiments or
independent validation. No best arm/policy/seed/checkpoint selected or model retuned.

**Validation and runnable record.** The exporter verifies each of **624 metric
values** against both private originals; exit 0 for export and subsequent --check,
reporting 16 trajectories / 208 checkpoints / status verified. It fails closed on
missing/duplicate/unknown trajectories, invalid curve keys, scores outside [0,1],
nonfinite or boolean scores, mismatched/missing checkpoints/costs, BA arithmetic
inconsistency (six-decimal tolerance), source/report disagreement and per-arm
baseline/final inconsistency. Source/output aliases and hardlinks are rejected;
private source hashes are compared internally, never published. Independent byte
integrity checks cover the entire existing private run directory before/after.
Exact local source-variable commands (values remain outside Git):

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.pilot_results_export --review "$PRIVATE_REVIEW" --summary "$PRIVATE_SUMMARY" --markdown docs/MEASURED_PILOT_RESULTS.md --json docs/results/exp3-exp5-nes-2026-11-09-aggregate.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.pilot_results_export --review "$PRIVATE_REVIEW" --summary "$PRIVATE_SUMMARY" --markdown docs/MEASURED_PILOT_RESULTS.md --json docs/results/exp3-exp5-nes-2026-11-09-aggregate.json --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_pilot_results_export.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 /tmp/issue34-stdlib-env/bin/python -m unittest discover -s tests -v
git diff --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_research_notebook.py
```

**Synthetic software tests.** Six new tests use fabricated aggregate trajectories
and privacy canaries only, not measured scores or private inputs. Initial missing-
module failure preceded implementation; the first parser run caught the Markdown
separator being mistaken for a numeric row. A separate failing hardlink test led
to rejecting inode aliases before writing. All six targeted tests subsequently
passed. Public Actions runs only synthetic software tests, never private-source
export or measured fitting. Final full-suite and publication checks follow below
once observed.

**Limitations/next.** Labels remain provisional; the 70/35/18 fixed eligibility and
condition-equal scoring are unchanged. Exp5 is historically exposed; its sole
positive evaluator condition TFA_10 and technical replicates do not establish
independent positive preparations, confidence or generalization. Cost is one proxy
unit per whole prepared condition, not measured money/time. Random and nominal DoE
are not model-adaptive or uncertainty selectors. Numerical outcome review is still
pending, including negative/no-improvement results. Raw spectra, well-level labels/
predictions, feature matrices, fitted models, local paths and private hashes remain
excluded. Stop at Draft PR #35 for ChatGPT review; no merge or scientific changes.

**Final local verification.** Full pinned-ML suite: **127 tests in 19.063s, OK,
exit 0** (121 prior + six exporter tests, no skips). Clean standard-library suite:
**127 tests in 1.542s, OK (skipped=16), exit 0**. Final aggregate --check again
verified all 208 checkpoints/624 scores; `git diff --check` exited 0. Final staged
allowlist/privacy/source-integrity and appended-entry checks precede publication;
CI results will be reported on the PR after observation. No measured refitting.

## Entry 036 — 2026-11-09 | Independent numerical review, accepted retrospective record, and researcher pause

**Researcher instruction and status.** The researcher authorized integrating Draft PR #33 first and then PR #35 with necessary accurate scientific notes, while explicitly choosing to **review the existing results before initiating any next research step**. This is **not** authorization for a new experiment, model rerun, reweighting, feature tuning, holdout-guided selection, or use of Exp8.

**Independent review and evidence boundaries.** ChatGPT independently inspected the public measured-pilot results report and aggregate JSON at PR #35 head `606d0ad63e06d0b8ac851059ddf4253be0befc44`: all **16** A/B/C/D × Random(7/11/19)/DoE trajectories, all **208** cost checkpoints (0–12), and **624** reported BA/sensitivity/specificity values. Every Markdown row matched the corresponding published JSON value, without discrepancies; the BA identity and score bounds were coherent. Codex's private-original 624-value verification was reported, but the original private Ubuntu `REVIEW.md` and `summary.json` were **not independently accessed by ChatGPT**. GitHub CI at that reviewed head passed **127 software tests**, and notebook checks passed. These are retrospective **measured-spectra model calculations**, not new laboratory measurements.

**Observed fixed evaluator BA and TFA sensitivity:** A Raw/Full `k=0: 0.933333 / 1.000000`, `k=12: 0.833333 / 0.666667`; C Area/Full `k=0: 0.900000 / 1.000000`, `k=12: 0.600000 / 0.333333`; B Raw/Compact8 and D Area/Compact8 show `BA=0.500000, sensitivity=0, specificity=1.000000` at **every checkpoint for every predeclared selection strategy**. Additional acquired conditions did not produce a reliable monotone improvement on the fixed evaluator. A/C intermediate values depend on acquisition ordering, but **Random vs DoE superiority is not established** and no winner or best budget was selected. DoE is nominal coverage of acquisition history only and is **not** model-adaptive active learning.

**Critical interpretation limits.** Fixed evaluator has **one TFA-positive prepared condition** (three related technical wells) and five non-TFA conditions; one positive-well decision changes BA by about `1/6`. Historical Exp5 has already been explored; the evaluator is not pristine. Labels are researcher-endorsed provisional analyses, not independently confirmed physical preparation. Costs are proxy whole-condition units. The possible reasons for B/D failure or A/C degradation are **hypotheses** requiring separately authorized group-level diagnostics; they are not yet verified causes. The frozen results, including unfavorable runs, must be preserved without tuning to this evaluator.

**Version-control integration and future boundary.** PR #33's archive note **Entry 033** must remain before PR #35's Entries 034–035; the corresponding HANDOFF checkpoints are renumbered to prevent duplicate headings. The PR #35 branch is reconciled by preserving original content and joining the current `main` documentation branch. This Entry 036 captures independent scientific assessment before the authorized merge; neither scripts nor private artifacts or training inputs are changed by this entry. After final CI and merged-commit checks, **pause here for researcher review**. Potential future work such as Exp3 preparation-level leave-one-group-out assessment or training-only Compact8 diagnosis requires a fresh explicit decision; **Exp8 remains locked**.

## Entry 037 — 2026-11-10 | Publication figures and reproducibility archive of the measured pilot

**Question/owner/authority.** Owner Codex; scientific reviewers researcher + ChatGPT.
The researcher explicitly requested reporting/archival figures of the existing
measured Exp3–Exp5 pilot, with no new training, scientific-method changes or Exp8
access. GitHub confirms PR #33 and PR #35 merged into main; dedicated branch
`analysis/measured-pilot-paper-figures` starts at latest main
`cf0084fcc0b6ba4113edaab7e5c157d4db19a5e6`. Read the project/agent instructions,
charter, decisions, notebook/handoff, published results and actual implementation.
Latest prior notebook Entry 036 and all earlier entries are preserved. This reporting
instruction supersedes the pause only within this task, not for a next research phase.

**Source/evidence.** Sole main-figure data source:
`docs/results/exp3-exp5-nes-2026-11-09-aggregate.json`; SHA-256:
`3d0ebbb13632854b14ee4e97dabdcef305f06dca4ebd1246b621456ff55e767e`.
Before plotting, verified four arms, Random seeds 7/11/19, one deterministic DoE,
all budgets 0–12, **16 trajectories / 208 checkpoints / 624 score values**. Main
plotting imports no learner or private-source module. The CSV retains every source
JSON metric value through Decimal parsing/writing, with no added rounding. The
source JSON itself already has six-decimal reporting precision; no additional
measurement precision is inferred or recovered. Existing result files are unchanged.

**Reporting alternatives/why.** Use every observed checkpoint as a marker rather
than smoothed or interpolated curves. Different shapes, sizes and colorblind-friendly
colors expose coincident seeds; constant panels are annotated so B/D zero sensitivity
cannot disappear on the axis. Random mean and **sample SD (ddof=1, n=3)** are shown
as checkpoint-wise error bars, not a confidence interval or superiority test. No
smoothing, jitter, favorable budget/seed selection or band interpolation. Full
source CSV plus endpoint summary CSV/Markdown make the graphics reproducible. Delta
is paired final minus initial within each seed; descriptive arithmetic uses 50-digit
Decimal precision. Main PDFs are vector with embedded TrueType fonts; PNGs are
300 dpi, 3000×2340 pixels, all using the same four-panel A/B/C/D layout.

**Exact scripts/commands and outputs.** New main script:
`scripts/plot_measured_pilot_results.py`. Optional plotting dependencies are pinned
separately in `requirements/figures.txt`; existing ML pins are unchanged.

```bash
uv pip install --python .venv/bin/python -r requirements/figures.txt
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python scripts/plot_measured_pilot_results.py
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 /tmp/issue34-stdlib-env/bin/python -m unittest discover -s tests -v
git diff --check
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_research_notebook.py
```

The plotting command exited 0 with the validated 16/208/624 counts and source hash.
Files in `docs/figures/measured_pilot/`:
`figure_1_balanced_accuracy.png`, `figure_1_balanced_accuracy.pdf`,
`figure_2_tfa_sensitivity.png`, `figure_2_tfa_sensitivity.pdf`,
`figure_3_specificity.png`, `figure_3_specificity.pdf`, and `manifest.json`.
Numerical archive: `docs/results/measured_pilot_plot_data.csv`,
`docs/results/measured_pilot_summary.csv`, `docs/results/measured_pilot_summary.md`.
The manifest records public input/output hashes, software versions and plotting
conventions, without private provenance. MEASURED_PILOT_FIGURE_NOTES.md verifies
the model/formulas against source and gives captions, observations and limitations.

**Verified configuration/preprocessing.** Binary TFA=1 vs other single PFAS=0;
70 Exp3 training / 18 conditions, 35 Exp5 acquisition / 12 conditions, 18 Exp5 fixed
evaluator / six conditions, three existing exclusions. L2 LR C=1, class_weight=None,
lbfgs, max_iter=5000, tol=1e-4, fit_intercept=True, random_state=0, warm_start=False.
Fresh StandardScaler and LR were fitted at every historical checkpoint with the
same recomputed condition-equal weights N/(G*n_group), training-only scaler fitting,
and native thread limit one. No fit is repeated for these figures. Spectral
representations are A Raw/Full, B Raw/Compact8, C Area/Full, D Area/Compact8; Area is
the positive 380–580 nm trapezoid applied to the full 350:2:700 grid. Compact8's exact
ordered amplitudes/ratio, discrete centroid/spread, absolute derivative area,
derivative at 450 and unsmoothed 440–480 slope formulas are recorded in the notes.
SG derivative is window15/poly2/deriv1/delta2 with interpolated edges. Feature
standardization is across training examples, **not** spectral baseline correction.
Source confirms no Ce–ARS blank subtraction or 650–700 nm offset correction.

**Observed retrospective results.** A and C differ and fluctuate by acquisition
order; BA changes from 0.933333→0.833333 (A) and 0.900000→0.600000 (C). B and D have
BA0.5, TFA sensitivity0 and specificity1 throughout every recorded trajectory.
A/C sensitivity declines to 0.666667/0.333333 from 1.0; specificity changes to
1.0/0.866667 from 0.866667/0.8. There is no consistent monotonic gain with
acquisition and no Random/DoE superiority claim. These are existing measured-spectra
model calculations, separate from synthetic test outcomes and not new wet-lab data.

**Saved supplementary diagnostics.** Existing local artifacts contain grouped
holdout predictions and saved model coefficients at 208 checkpoints. The optional
`scripts/inspect_measured_pilot_artifacts.py` read only those known files and generated
two **private-only** supplementary figures (condition-level correctness and existing
coefficient norms, PNG/PDF). It calls no fit, predict, transform or spectral routine.
Source pickles used a CLI `__main__` class name; a synthetic regression test reproduced
the loading failure and a narrow class-name compatibility mapping restores existing
state without rewriting artifacts. No new coefficients or predictions were computed.
No saved Compact8 training/holdout matrices were present; matrix diagnostics remain
unavailable, with no substitute feature computation from raw scenario records.
Original private input bytes remain unchanged; all sensitive diagnostic outputs
stay in ignored private storage and are excluded from GitHub.

Optional command (variables configured privately, never logged):

```bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/measured-pilot-mpl .venv/bin/python -m scripts.inspect_measured_pilot_artifacts --source "$PRIVATE_RUN" --output "$PRIVATE_DIAGNOSTICS" --inspect-trusted-pickles
```

**Software/visual verification.** Initial missing-module tests preceded each new
implementation. Nine new reporting/diagnostic tests cover strict public schema,
16/208/624 retention, every budget, exact CSV round-trip, sample SD, generated PNG/PDF
files, axis/marker conventions, reporting's blocked learner imports, private output
restrictions and CLI-pickle compatibility without fit/predict. PDF inspection found
that save-time font settings had fallen outside the style context; a failing font
regression test preceded the fix, now requiring embedded TrueType and no raster
image objects. All three final PNGs and all three rendered PDFs were visually
inspected; zero-valued markers and all labels are visible. Final full-suite,
repeat-generation, privacy, append-only and CI observations follow after execution.

**Limits/next.** One positive fixed evaluator condition TFA_10, three related
technical wells, historical Exp5 exposure, provisional physical labels and proxy
whole-condition costs remain. Three Random seeds describe order variability, not
independent preparation/batch evidence. No chemistry or unseen-batch generalization
claim; saved coefficient norms cannot establish a causal Compact8 failure mechanism.
Reporting scripts performed zero model fit/refit/predict calls and accessed no Exp8.
The full existing test suite exercises synthetic fits only. No preprocessing,
labels, model settings or historical results changed; no alternate classifier or
new research phase. Open Draft PR and stop for ChatGPT scientific/code review,
without merge. Full publication captions are archived below as well as in the notes.

**Archived figure captions.**

Figure 1 — Balanced Accuracy Learning Curves. Retrospective measured Exp3→Exp5 condition-aware Balanced Accuracy
versus acquired experimental conditions for (a) A Raw/Full, (b) B Raw/Compact8,
(c) C Area/Full and (d) D Area/Compact8. Each marker is an observed checkpoint from
the frozen pilot: three Random acquisition seeds, their descriptive mean ± sample
SD (n=3, ddof=1), and deterministic nominal-coverage DoE. One proxy cost unit
acquires a complete condition; every run retains budgets 0–12. No interpolation,
smoothing or favorable-run selection is applied. Error bars are not confidence
intervals. The same fixed, historically exposed Exp5 evaluator and provisional
labels are used throughout; these results do not establish policy superiority.

Figure 2 — TFA Sensitivity Learning Curves. TFA sensitivity on the fixed Exp5 evaluator across the same complete
acquisition trajectories, panel order, markers, proxy costs and descriptive Random
mean ± sample SD as Figure 1. No new model calculations are performed for this
figure; it displays the recorded checkpoint sensitivities. Compact8 zero-sensitivity
panels retain the zero-valued markers and an explicit coincidence annotation.
The evaluator contains one positive prepared condition with three technical wells,
so these values provide limited independent positive-condition evidence.

Figure 3 — Specificity Learning Curves. Non-TFA specificity on the same five fixed negative Exp5 condition
groups across all 16 acquisition trajectories, with the same panels and plotting
conventions as Figures 1–2. Within-condition technical-well correctness is averaged
first, followed by the mean across negative conditions. Markers retain every
budget; black error bars describe variation among three Random seeds and are not
confidence intervals. DoE is deterministic nominal coverage, not active learning.

**Final local outcomes.** Full optional-ML/plotting suite: **136 tests in 20.525s,
OK, exit 0** (127 prior + nine reporting/diagnostic tests). Clean standard-library
suite: **136 tests in 1.559s, OK (skipped=18), exit 0** (16 optional ML tests and
two optional Matplotlib tests). A second full figure/table generation into temporary
public-only directories was byte-identical, including all PNGs/PDFs and manifest.
CSV equality tests checked all624 scores. Source JSON SHA and original private-run
file hashes are unchanged; notebook and HANDOFF retain the complete byte-prefix
from main. Poppler-rendered PDFs and PNGs passed visual review; `pdffonts` confirms
embedded CID TrueType, and tests reject Type3/raster-image PDF objects. Whitespace
and final staged privacy/notebook checks precede commit; CI outcomes will be posted
on the Draft after observation. No new measured model fit or Exp8 access.

**Post-staging format check.** Git whitespace validation exposed the CSV writer's
default CRLF terminators. A failing line-ending regression assertion preceded
switching both CSV writers to explicit LF; no numeric value changed. Regenerated
public figures/tables and their checksums, then repeated generation byte-identically.
Final full suite: **136 tests in 20.800s, OK**; clean stdlib: **136 in 1.539s,
OK (skipped=18)**. `git diff --check` now exits 0. Original public JSON/private
inputs remain unchanged. Publication remains limited to the 19-file reporting
allowlist, with final staged checks and Draft CI required before handoff.
