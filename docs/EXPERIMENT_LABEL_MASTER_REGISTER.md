# Experiment label master — private archive reference

**Recorded:** 2026-11-09. **Researcher-provided source:** `CeARS_All_Experiments_Exp3_to_Exp8_Well_Label_Master(1).xlsx`.

**Archived original:** ChatGPT **private File Library**, `/Scientific_Experiment_Selection/CeARS_All_Experiments_Exp3_to_Exp8_Well_Label_Master_original.xlsx` (this is **not a file in the public GitHub repository**). Archive copy retains source bytes unchanged.

- SHA-256: `68cf034687f167fac1c5b881c95a140e87b33cdf8b61ef75db839f1b4c556761`
- Size: **164,473 bytes**; 10 worksheets: README, ALL_WELLS, ISSUES_AND_DEVIATIONS, Exp3, Exp4, Exp5, Exp6, Exp7, Exp8, EXPERIMENT_SUMMARY
- Coverage: **576 claimed well records**, 96 for each of Exp3–Exp8; includes individual experiments, mixtures, blank/QC, historical exceptions, and execution notes. Source `verification_status` assertions remain source claims, **not independent confirmation of physical sample identity**.
- Compared 288 overlapping Exp3/Exp5/Exp8 records against the earlier researcher-uploaded `Exp3_Exp5_Exp8_All_Wells_and_Labels(2).xlsx` on all 23 shared fields: **0 discrepancies**. Compared all **123 included** Exp3/Exp5 pilot rows against the saved private `Exp3_Exp5_Pilot_Label_Map.xlsx` for common join/label/QC fields: **0 discrepancies**. These are metadata comparisons only.
- Prior code audit: [PR #32](https://github.com/batuzunoglu/scientific-experiment-selection/pull/32) / `docs/RAW_LABEL_JOIN_AUDIT.md` confirms **123/123** Exp3/Exp5 eligible physical wells mapped to raw workbook columns, no mismatches, with unchanged raw sources.

**Canonical pilot mapping:** ChatGPT private File Library `/Scientific_Experiment_Selection/Exp3_Exp5_Pilot_Label_Map.xlsx`, with **Exp3 train 70**, **Exp5 acquisition 35**, **Exp5 fixed evaluation 18**; primary-analysis exclusions **Exp3 D6/D7** and **Exp5 B7** remain recorded separately. Use the pilot map and approved fixed group split, not raw `use_in_model=Yes`, for the future TFA/non-TFA pilot.

**Important access restrictions:** This public GitHub repository contains **only this metadata pointer**, not the full workbook, experimental labels, raw spectra or private manifests. ChatGPT Library is **not directly mounted in Codex's Ubuntu environment**. Before future authorized fitting, the researcher must locally supply/read the controlled copy from a private folder outside the public repository, validate its SHA-256 and preserve the original. Do not commit it to public GitHub without separate explicit *public release* consent. **Exp8 remains locked**, including any Exp8 contents in the archived workbook. Do not train models now; a separate, explicit real-data fitting authorization and task are required.

**Provenance:** Original from researcher upload; checksum calculated on uploaded original bytes on 2026-11-09. Researcher requested storage for resuming experiments and model training later. This entry is an archive locator, **not a data-access capability for GitHub/CI/Codex**.
