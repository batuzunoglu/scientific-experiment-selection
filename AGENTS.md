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

13. Before any **authorized** research-affecting commit/PR, append a dated `## Entry NNN — YYYY-MM-DD` section to `docs/RESEARCH_LAB_NOTEBOOK.md` in the **same PR**. Never modify previous entries; use a correction/new entry instead. GitHub's `research-notebook` PR check enforces the presence of an appended entry for research code/method changes, but humans must check scientific completeness. Do not bypass by directly pushing research changes to `main`.
14. For chat-only research decisions, ChatGPT should promptly propose/record the entry in a documentation PR; Codex must read the committed entry rather than reconstructing motivations from code. If commit/push is not yet approved, maintain a proposed local notebook entry for later review; do not mistake the notebook requirement for new authorization to publish data or code.

## Multi-agent working agreement (Codex, Antigravity, other coding assistants)

15. Read `docs/AGENT_WORKFLOW.md` before accepting a delegated task. This `AGENTS.md` is the **shared canonical rules file**; do not add a second `GEMINI.md` that might diverge.
16. Work on only the **explicitly assigned GitHub Issue scope**. Name one owner and one reviewer; stop at the stated review gate. No assistant may grant scientific, publishing, model-training or merge approval on the researcher's behalf.
17. Never run two writing agents in the same working tree; use separate branches/worktrees or work sequentially. Keep GitHub Issue/PR comments as the handoff channel; a short handoff must include changed files, tests, observed outcomes, provenance, blockers, notebook status and next owner.
18. A read-only reviewer does not edit files. Do not expose private spectra, provisional per-well manifests or secrets to external models, commits or PRs; use non-sensitive summaries and synthetic fixtures. Preserve the existing append-only notebook and PR checks.
