# Phase B Leave-One-Group-Out (LOGO) Cross-Validation Plan for Exp3

## 1. Context and Authority

- **Scientific Decisions:** [D-016](DECISIONS.md#d-016--2026-11-08-exp3-d6d7-primary-analysis-eligibility) (Exp3 D6/D7 primary exclusion), [D-017](DECISIONS.md#d-017--2026-11-08-exp3-shared-solution-replicate-grouping) (Exp3 shared-solution replicate grouping), and [D-019](DECISIONS.md#d-019--2026-11-08-logo-primary-cv-supersedes-d-018-primary-split-choice) (LOGO primary CV supersedes D-018 three-fold).
- **Notebook Entries:** [Entry 017](RESEARCH_LAB_NOTEBOOK.md#entry-017--2026-11-08--exp3-d6d7-primary-analysis-exclusion-with-sensitivity-follow-up), [Entry 018](RESEARCH_LAB_NOTEBOOK.md#entry-018--2026-11-08--exp3-technical-replicates-share-one-prepared-solution), [Entry 019](RESEARCH_LAB_NOTEBOOK.md#entry-019--2026-11-08--choose-balanced-three-fold-grouped-cv-for-exp3-phase-b), [Entry 020](RESEARCH_LAB_NOTEBOOK.md#entry-020--2026-11-08--researcher-selects-leave-one-group-out-as-primary-validation), and [Entry 021](RESEARCH_LAB_NOTEBOOK.md#entry-021--2026-11-08--phase-b-deterministic-18-fold-logo-plan-and-leakage-tests).
- **Task Scope:** Phase B evaluation plan and leakage guardrails. **No ML models are trained, no raw spectra are accessed, and no training authorization is granted.**

---

## 2. Shared-Solution Grouping and Leakage Constraints

Under D-017, the researcher confirmed first-hand that the four technical replicate wells for each Exp3 PFAS × concentration condition originated from **one prepared solution**. Therefore:

1. **Inseparability:** All replicate wells sharing the same condition identifier `Exp3:{PFAS}_{concentration}` must reside strictly on the same side of any train/validation split.
2. **Zero Leakage:** For each fold, the intersection between the validation group ID and the set of 17 training group IDs is strictly empty ($\emptyset$).
3. **No Random Well-Level Splitting:** Random splitting of wells across folds would leak within-solution preparation signatures and produce artificially optimistic validation metrics.

---

## 3. Deterministic 18-Fold LOGO Allocation

The 18 condition groups are ordered deterministically by PFAS class (`TFA`, `PFPA`, `PFBA`, `PFHxA`, `PFOA`, `PFNA`) and concentration (`5`, `10`, `20` ppm). In each fold $i \in \{0, \dots, 17\}$, group $i$ is held out as validation and the remaining 17 groups form the training set.

| Fold Index | Validation Group ID | Held-Out Condition | Held-Out PFAS | Concentration (ppm) | Nominal Candidate Wells | Provisional Primary Wells (Post D6/D7 Exclusion) | Training Groups Count |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | `Exp3:TFA_5` | `TFA_5` | TFA | 5 | 4 | 4 | 17 |
| 1 | `Exp3:TFA_10` | `TFA_10` | TFA | 10 | 4 | 4 | 17 |
| 2 | `Exp3:TFA_20` | `TFA_20` | TFA | 20 | 4 | 4 | 17 |
| 3 | `Exp3:PFPA_5` | `PFPA_5` | PFPA | 5 | 4 | 4 | 17 |
| 4 | `Exp3:PFPA_10` | `PFPA_10` | PFPA | 10 | 4 | 4 | 17 |
| 5 | `Exp3:PFPA_20` | `PFPA_20` | PFPA | 20 | 4 | 4 | 17 |
| 6 | `Exp3:PFBA_5` | `PFBA_5` | PFBA | 5 | 4 | 4 | 17 |
| 7 | `Exp3:PFBA_10` | `PFBA_10` | PFBA | 10 | 4 | 4 | 17 |
| 8 | `Exp3:PFBA_20` | `PFBA_20` | PFBA | 20 | 4 | 4 | 17 |
| 9 | `Exp3:PFHxA_5` | `PFHxA_5` | PFHxA | 5 | 4 | 4 | 17 |
| 10 | `Exp3:PFHxA_10` | `PFHxA_10` | PFHxA | 10 | 4 | **2** (D6, D7 excluded) | 17 |
| 11 | `Exp3:PFHxA_20` | `PFHxA_20` | PFHxA | 20 | 4 | 4 | 17 |
| 12 | `Exp3:PFOA_5` | `PFOA_5` | PFOA | 5 | 4 | 4 | 17 |
| 13 | `Exp3:PFOA_10` | `PFOA_10` | PFOA | 10 | 4 | 4 | 17 |
| 14 | `Exp3:PFOA_20` | `PFOA_20` | PFOA | 20 | 4 | 4 | 17 |
| 15 | `Exp3:PFNA_5` | `PFNA_5` | PFNA | 5 | 4 | 4 | 17 |
| 16 | `Exp3:PFNA_10` | `PFNA_10` | PFNA | 10 | 4 | 4 | 17 |
| 17 | `Exp3:PFNA_20` | `PFNA_20` | PFNA | 20 | 4 | 4 | 17 |

- **Nominal candidate pool:** 72 wells ($18 \times 4$).
- **Provisional primary pool:** 70 wells ($17 \times 4 + 1 \times 2$), reflecting approved primary exclusion of physical Exp3 D6 and D7 under D-016.
- **Group integrity:** Excluding D6/D7 reduces `Exp3:PFHxA_10` from 4 to 2 wells; it **does not eliminate** the group. When Fold 10 is evaluated, the validation set contains the 2 retained candidate wells (`D5` and `D8`), while all other 17 folds contain 4 validation wells each.

---

## 4. Evaluation and Task-Specific Methodological Rules

### 4.1. Six-Class PFAS Identity Classification
- **Single True Class Per Fold:** In LOGO, every validation fold contains samples from exactly **one** true PFAS analyte.
- **Standalone Per-Fold Multiclass Metrics Not Suitable:** Because each validation fold has only one true ground-truth class, standalone per-fold six-class macro-F1, AUROC, or full multiclass confusion summaries are not suitable representations of model performance. Single-class per-fold accuracy, true-class recall, or well-defined loss metrics remain calculable, but cannot characterize six-class discrimination in isolation.
- **Mandatory Pooled Out-of-Fold Predictions:** For the primary six-class evaluation, predictions from all 18 validation folds must be pooled into an aggregate out-of-fold prediction array before calculating overall macro-F1, multiclass cross-entropy, or confusion matrices.
- **Condition-Level Weighting:** Because `Exp3:PFHxA_10` has 2 candidate wells under D-016 while the other 17 groups have 4 wells, unweighted sample averaging would under-weight `PFHxA_10`. The primary evaluation protocol should specify equal group weighting (macro-average over condition groups) to prevent bias toward conditions with more technical replicates.

### 4.2. Known-Identity Concentration Regression
- **Restricted Within-Class Training Data:** When one concentration group for an analyte is held out (e.g., `TFA_5`), only **two** other concentration groups for that analyte (`TFA_10` and `TFA_20`) remain in the training set.
- **Extrapolation Risk:** Regressing on 5 ppm or 20 ppm requires extrapolating beyond or predicting at the extremes of a two-point calibration.
- **Exploratory Status:** Known-identity concentration regression under LOGO must be explicitly reported as exploratory.

---

## 5. Metadata Boundaries and Verification Guardrails

1. **Static Metadata vs. Physical Measurements:** This LOGO plan defines the structural group-to-fold mapping and partitioning contract. It does **not** load, parse, or evaluate physical spectra.
2. **Provenance Limitations:** Chemical labels and preparation independence between distinct conditions remain unverified (`preparation_group='UNKNOWN'`, `physical_label_verified=False`).
3. **External Batches:** Exp5 remains historically exposed and reconstructed; Exp8 remains a locked holdout. Neither is included in this Exp3 LOGO plan.
4. **Automated Leakage Guardrails:** The standard-library module `scientific_experiment_selection/logo_plan.py` enforces:
   - `validate_group_ids()`: rejects duplicate, missing, unexpected, or malformed groups.
   - `validate_group_record()`: ensures caller-supplied group metadata matches authoritative parsed values.
   - `verify_fold_leakage()`: guarantees zero train/validation group overlap, requires training groups to equal the exact canonical 17-group complement, and verifies metadata consistency.
   - `split_samples_by_fold()`: enforces sample metadata consistency against group IDs and ensures technical replicates cannot be split across training and validation folds.
   - `validate_fold_evaluation_readiness()`: guards dataset completeness by checking that validation is non-empty and all 17 training condition groups are represented before model evaluation.
