# Issue #27 synthetic selection MVP implementation plan

Owner Codex; scientific reviewers ChatGPT + researcher. Spec: Issue #27 and
Issue #21 direction comment 6745484839. Exact base aaf8ca8. Synthetic-only;
no data readers, real models, changes to decisions/features, or merge.

1. Write failing synthetic tests for immutable candidate/replicate/group contracts,
   unique/disjoint group identities and exact integer budgets (including zero).
   Implement selection.py contracts, hidden synthetic oracle and evaluator.
2. Write failing policy/engine tests: seeded sorted-input Random; deterministic
   greedy nominal-factor-level coverage; uncertainty refusal without approved
   prospective inputs; one-shot reveal after valid unselected affordable action;
   indivisible groups and equal-total group weights. Implement loop and adapter hooks.
3. Test evaluator-only fixed holdout, no score/outcome feedback into selector views,
   malicious invalid/duplicate actions, deterministic paired runs, identical scenario
   and cost schedule, baseline at zero acquisitions, and no affordable/exhausted stop.
4. Add a fully synthetic runnable demonstration and concise architecture/caveats.
   Log synthetic curves as evaluator output only, never experimental performance.
5. Full suite, notebook gate, staged publication/privacy audit. Append next available
   notebook entry and handoff. Commit/push safe files and open Draft PR, not ready/merged.

Implementation choices (not frozen scientific protocol): positive integer synthetic
cost units; DoE novelty counts unseen factor-level pairs, ID tie break. Fake learner
uses condition-equal weighted synthetic means, threshold 0.5, solely to exercise
fit/predict hooks. Binary condition-equal accuracy is a toy evaluator diagnostic,
not the approved real model/metric. Group IDs denote indivisible preparations;
alias detection requires caller's truthful canonical IDs. Pure Python interface
separation is not a sandbox against malicious introspection or captured closures.

Progress: contracts, loop, policies, fake adapter and demo implemented; 19 new tests pass.
Final local verification: 86 tests passed; demo repeated byte-identically.
Notebook append validation passed; staged security audit and Draft publication follow.
