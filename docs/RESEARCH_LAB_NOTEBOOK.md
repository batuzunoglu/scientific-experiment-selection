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

