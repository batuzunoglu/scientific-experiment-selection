# Instructions for Codex, Claude, ChatGPT or any new assistant

1. Before acting, read `README.md`, `docs/PROJECT_CHARTER.md`, `docs/DECISIONS.md`, `docs/HANDOFF.md`, `docs/RESEARCH_LAB_NOTEBOOK.md`.
2. Do not silently change research questions, evaluation splits, physical experiment conditions, or reward design. Log proposals and researcher approvals.
3. Never invent lab measurements, benchmark scores, test outcomes, citations, or successful executions.
4. Every code change must list files changed, its exact runnable command, tests performed, remaining limitations, and whether results are observed or simulated.
5. Preserve raw experimental exports. Derive processed data reproducibly using scripts and data identifiers/checksums.
6. Prevent evaluation leakage between selected adaptation experiments and independently held-out test samples/batches. Do not assume replicates are independent batches.
7. Do not treat an unmeasured physical experiment as having an observed spectrum; simulation or surrogate outputs must be labeled explicitly.
8. Keep settings/paths configurable. Prefer scripts/packages over notebook-only code. Record random seeds, versions and dataset provenance.
9. End sessions by updating `docs/HANDOFF.md` and the relevant experiment/decision/learning logs.
10. Explain scientific concepts to the researcher before significant new methodological code is introduced.

11. For every substantive methodological decision, analysis or experiment, append a dated entry to `docs/RESEARCH_LAB_NOTEBOOK.md`: question, alternatives, evidence, why, approval status, exact runs (or not run), limitations, and next decision. Preserve prior entries and negative results. Keep the brief approved decision in `docs/DECISIONS.md` and a runnable record in `docs/EXPERIMENT_TEMPLATE.md` when appropriate.
12. Do not silently choose preprocessing, engineered features, evaluation splits or new reward designs; define the question and compare against Raw/no-transform controls before implementation and researcher review.
