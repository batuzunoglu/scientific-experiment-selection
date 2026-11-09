# Issue #29 synthetic Logistic Regression integration plan / execution record

Owner Codex; reviewers researcher + ChatGPT. Binding spec Issue #29 and final
Issue #21 split/representation/weight/metric approvals. Base 861e07e.

- Tests first for fixed 12/6 roles, raw representations, class/group metric math,
  model/scaler config, training weights, refit/fit-source isolation, no peeking.
- Implement standard-library protocol + synthetic generator and lazy optional
  pinned ML adapter; add named balanced evaluation mode without weakening engine.
- Add default B demonstration for fixed seeds 7/11/19 and DoE, all budgets 0–12;
  retain all planned A/B/C/D options and tests, no tuning or representation selection.
- Keep stdlib tests runnable without ML; add dedicated CI requiring exact optional
  dependencies and full integration coverage. No spectral/decision-register edits.
- Append notebook/handoff; run full and clean-stdlib suites, demo determinism,
  notebook/whitespace/security audit; safe Draft only, no real data/fitting/merge.

Observed: missing-module failure first, then 16 new tests pass; 102 full tests pass
with ML. Clean stdlib environment passes with 10 optional skips. All four arms
fit/refit in tests; full reported budget experiment is B only. Documentation records
fixed solver engineering choices, measured synthetic curves and remaining gates.
Final publication checks and Draft handoff follow, no additional scientific approval.
