# Learning Journal

## Lesson template
- Date / topic:
- What problem does this concept solve?
- Plain-language explanation:
- Definition / assumptions / equations:
- Concrete example in spectroscopy:
- Files and commands involved:
- What I predicted / what actually happened:
- How would I explain it to another researcher?
- Questions to revisit:

## 2026-10-21 — Workflow verification

- The initial uv commands could not run Python because the sandbox prevented writing to the existing uv cache. Approved retries of the same commands passed: the doctor exited 0 and the unittest suite reported 2 tests, OK.
- These observed infrastructure checks verify basic execution, not scientific validity. No scientific measurements were produced or simulated.
- The default `gh issue view` query failed on a deprecated Projects field; requesting explicit JSON fields retrieved Issue #1 successfully.
- Exact commands and observed outputs are recorded in `docs/WORKFLOW_TEST.md`. The researcher approved the local diff and publication; connected-repository review remains untested.
