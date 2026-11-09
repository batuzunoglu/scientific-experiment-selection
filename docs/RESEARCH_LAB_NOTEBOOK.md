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
