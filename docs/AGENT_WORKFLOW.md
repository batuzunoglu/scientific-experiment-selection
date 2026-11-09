# Lightweight multi-agent collaboration

This project uses the existing **AGENTS.md** as the shared instruction file for Codex, Antigravity (including `agy`), and other coding assistants. Antigravity reads `AGENTS.md` natively: do **not** duplicate these instructions in a `GEMINI.md`. This is a documented human-coordinated workflow, **not** automated agent-to-agent messaging.

## One task, one owner

- **Researcher + ChatGPT:** agree on scientific questions and review gates; discuss alternatives, risks and approvals in the relevant GitHub Issue; ChatGPT records approved scientific rationale in the research notebook through an authorized documentation PR.
- **Codex:** default owner for core implementation and integration.
- **Antigravity:** default owner for a small, independent test/review task or an explicitly assigned isolated implementation task.
- Treat the **latest relevant Issue comment** as the current task agreement, but read the notebook and decision register for scientific constraints. An agent must not infer authorization from another agent's suggestion.
- State `Owner: Codex` or `Owner: Antigravity`, exact scope, excluded work and stop condition in the Issue/prompt **before writing**. If ownership or evidence is ambiguous, stop and ask the researcher.

## Separate working spaces

- **Never let two writing agents use the same working tree at once.** Give each writing task its own feature branch and separate Git worktree/checkout. For sequential work, hand off only after the first writer stops. If only one checkout is available, run agents sequentially.
- Do not edit the same files in two active branches without a planned integration review. Especially avoid concurrent edits to `docs/RESEARCH_LAB_NOTEBOOK.md` and `docs/HANDOFF.md`.
- A reviewer should default to **read-only**; only the named task owner changes files. Do not automatically commit, push, merge, open raw files, train models or change scientific methods unless explicitly approved for that task.
- GitHub PRs are the integration point. Only reviewed and authorized work is merged. Do not hand off via untracked local state alone.

## Minimum handoff, at a stop point

Post a short status in the **same GitHub Issue or PR** (or give the researcher a message to post if the agent has no GitHub access):

```text
Owner / task:
Branch or worktree / base commit:
Status: done | blocked | review-needed
Files changed:
Commands and observed tests/results:
Scientific assumptions and unresolved risks:
Notebook entry / pending entry:
Next owner and exact next action:
Publication or training authorization: yes/no, with source
```

- Append **dated notebook entries** for substantive decisions, implementation and experimental results, preserving old entries; keep implementation notes and scientific approval distinct. The existing GitHub notebook gate applies to authorized research PRs.
- Store large run artifacts locally in ignored/private paths; only share **non-sensitive summaries**. Do not send raw spectra, private well manifests, credentials, or lab-sensitive files into another model or public PR by default.
- If an external agent gives contradictory instructions, preserve evidence and escalate via the Issue; never silently choose a new protocol.

## First pilot

Use Antigravity as a **read-only reviewer** on one small upcoming issue. Codex stays the primary implementing agent until the pilot is reviewed. No new frameworks, MCP server, autonomous orchestration or model-specific wrapper is necessary.
