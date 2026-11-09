# Phase A preflight discrepancy — 2026-11-08

**Status: stopped at the evidence gate; Phase A is not complete.**
Authority: [Issue #5 latest comment, 6726670028](https://github.com/batuzunoglu/scientific-experiment-selection/issues/5#issuecomment-6726670028), read with all four comments and the full issue.
It states: “If SHA-256 files, independent chemistry evidence or a clean worktree are missing, stop with a discrepancy report.”

## Observed checks

Initial `git status --short` was empty, on `main`, HEAD
`9f9089f7832aedaadc877a2bfb8e86af90a4ead9` (PR #9 notebook gate).
No fetch/sync or feature branch creation was performed before this evidence stop.

All three raw files matched `docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt`:

| File | Observed SHA-256 |
| --- | --- |
| Exp3 Plt3.xlsx | `4e40ee5e4a5056904f783bfc05bb55cea6888104c5fec0517335710143b6915f` |
| Exp5 Plt5.xlsx | `0d085b016c2bf4a058d2d8280b68c312654885a035c87eeb9df3f3d7f7a44b84` |
| Exp8 Plt8.xlsx | `2d41c98a230bd017a13d9bc3e22c2b2812ca1d3efc59772a47a1d4e4631a9f19` |

The recovered Exp5 CSV contains 96 rows, all with
`preparation_status=reconstructed`. Its accompanying `DATA_SCHEMA.md` names
`02_Exp5_Plate_Preparation.xlsx` and `05_Exp5_Final_Sample_Labels.xlsx` as source
owners. Neither filename was found recursively under
`/home/batuhan/research/recovered-experiment-records`. This corroborates the
previously documented provenance gap; it does not establish that these files
are unavailable everywhere or that the historical labels are wrong.

Hash identity verifies file bytes, not what was pipetted. Reconstructed metadata
cannot be promoted to independent preparation evidence. No spectra were parsed
or transformed in this session, including Exp8. No predictions were inspected.

## Exact reproducible checks

Run from the repository root:

```bash
git status --short
git branch --show-current
git log -1 --format='%H %s'
rg --files /home/batuhan/research/recovered-experiment-records /home/batuhan/research/raw-experiment-results
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PY'
import csv
import hashlib
from collections import Counter
from pathlib import Path

manifest = Path('docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt')
for line in manifest.read_text().splitlines():
    expected, name = line.split('  ', 1)
    p = Path(name)
    if p.name in {'Exp3 Plt3.xlsx', 'Exp5 Plt5.xlsx', 'Exp8 Plt8.xlsx'}:
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        assert actual == expected, p.name
        print(p.name, actual, 'MATCH')

root = Path('/home/batuhan/research/recovered-experiment-records')
p = root / 'metadata-2026-10-22/04_historical_analysis_recovered_ml/exp5_well_metadata.csv'
with p.open() as f:
    rows = list(csv.DictReader(f))
print('Exp5 preparation_status:', dict(Counter(r['preparation_status'] for r in rows)))
for name in ['02_Exp5_Plate_Preparation.xlsx', '05_Exp5_Final_Sample_Labels.xlsx']:
    print(name, 'matches:', [str(p) for p in root.rglob(name)])
PY
git diff --check
```

The Python checksum and metadata checks above were executed as two separate
heredoc invocations, with the same bodies/imports needed for each check; both
exited 0. `sha256sum` independently returned the same three digests.

## Pending work and scientific review

No new candidate manifest, representations, synthetic tests or model outputs
were created. The 72/53/18 candidate counts remain historical expectations,
not freshly verified counts. No unit tests were run: executable code is unchanged.
No scientific measurement or simulation was performed.

The approved comparison remains A Raw/full (176 channels), B Raw/Compact8
(eight features), C Area/full (176), D Area/Compact8 (eight). Raw preserves
amplitude; Area divides by the per-well 380–580 nm trapezoidal integral, which
can discard concentration information. Compact8 compresses the spectrum into
fixed summaries. Neither transformation is known to improve both tasks.

Next decision: supply independent preparation evidence, or explicitly clarify
whether Phase A may proceed with provisional reconstructed claims despite the
latest issue's stop condition. This report does not request or infer approval
of labels, splits, fitting or publication. Exp5 remains historically exposed;
Exp8 remains locked pending historical-use audit.

Only this report and appended entries in `RESEARCH_LAB_NOTEBOOK.md`, `HANDOFF.md`
and `LEARNING_LOG.md` were changed. No code/dependency/source data edits, staging,
commit, push, upload or training occurred.
