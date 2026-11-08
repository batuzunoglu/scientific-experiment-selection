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
