# Issue #31 — bounded Exp3/Exp5 raw-column join

Owner Codex; reviewers ChatGPT + researcher. Base `5ae57fb` after PR #30,
branch `feature/exp3-exp5-raw-label-join`. Status: **join-consistent, pending review**.

| Primary view | Joined wells | Condition groups |
| --- | ---: | ---: |
| Exp3 training | 70 | 18 |
| Exp5 acquisition | 35 | 12 |
| Exp5 fixed holdout | 18 | 6 |
| Approved exclusions, outside all primary views | 3 | — |

**123 included wells matched; mismatch categories: none (0).** Source bytes unchanged.
Existing condition labels are the reference; no labels were reconstructed or repaired.
No additional exclusions or eligibility changes. Group counts and immutable nominal
12/6 role assignment use the approved Issue #21 split; no QC/blank/mixture promoted
by a model-use flag. The existing historical model partition remains distinct from
the new acquisition/evaluator roles. The primary-analysis override preserves source QC.

## Source availability and evidence limits

The compact mapping attachment, original all-wells workbook and supplemental exact
supervised-classification workbook were absent from the documented local source
folder (3 unavailable preferred options). Issue #31 explicitly permits existing
local Step3–5 metadata as fallback; the existing Step4 `Well_Metadata` was available
and used. No full-home search, bulk import, alternative label reconstruction or
open-ended recovery. Only the metadata worksheet was parsed, with Exp3/5 filtering
before deriving records; prediction/score/feature worksheets were not opened.

This is a join against a researcher-endorsed historical analytical mapping. It is
**not independent proof of the exact old fitted model's y-vector lineage or of wet-lab
identity**. Earlier source `Verified` assertions are not adopted as new verification.
Once header/presence/provenance/condition checks passed, source investigation stopped.

The existing raw reader checked exact physical headers, finite 176-point columns
and the 350:2:700 grid on only the two authorized raw exports. Mapping-file hash/size
matched its existing evidence manifest; raw hashes matched the recorded raw manifest.
Before/after mapping, manifests and raw hashes agreed; no digest or absolute source
location is published. No raw spectra, derived feature vectors or per-well joins
are exported. No Exp8 workbook/rows, model predictions or holdout metrics inspected.

This is readiness for **scientific review of a provisional retrospective pilot**,
not actual fitting permission, physical certification or a pristine-test claim.
The separate actual-spectrum fitting decision remains with the researcher after
ChatGPT reviews this result. No model is fitted by the audit code.

## Commands / tests

CLI (source variables configured locally outside Git; values never logged):

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.raw_label_join --mapping "$MAP" --raw-root "$RAW_ROOT" --raw-checksums docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt --mapping-checksums "$MAPPING_CHECKSUMS"
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_raw_label_join.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Actual local execution resolved locations from existing documented source roots,
without printing them, then invoked that CLI once; exit 0, no mismatches. Exact
source-resolution wrapper (no source paths or well records embedded):

```python
from pathlib import Path
import re, subprocess, sys, os, json
text = Path('docs/WELL_MAP_DISCREPANCIES.md').read_text()
try:
    evidence = Path(re.search(r'`(/[^`]+/metadata-2026-10-22/)`', text).group(1))
    raw = Path(re.search(r'Raw root: `([^`]+)`', text).group(1))
    mappings = list(evidence.rglob('CeARS_Analysis_Step4_Individual_Classification.xlsx'))
    if len(mappings) != 1:
        raise ValueError('source resolution')
    cmd = [sys.executable, '-m', 'scientific_experiment_selection.raw_label_join',
           '--mapping', str(mappings[0]), '--raw-root', str(raw),
           '--raw-checksums', 'docs/audits/2026-10-22-reconciliation/raw_sha256sum.txt',
           '--mapping-checksums', str(evidence / 'SHA256SUMS.csv')]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    if r.stderr:
        raise ValueError('unexpected diagnostic')
    print(r.stdout.strip())
    print('join_audit_exit_code:', r.returncode)
    raise SystemExit(r.returncode)
except Exception:
    print(json.dumps({'status': 'review-needed', 'mismatches': {'source_resolution_or_execution': 1}}))
    raise SystemExit(2)
```

Observed software checks: **7 new synthetic tests passed; 109 full-suite tests passed**
(102 prior + 7 new). Existing full-suite ML tests use synthetic fixtures only; the
actual join invokes no learner, spectral representation or scaler. Python 3.12.14,
no new dependencies or randomness. Initial missing-module failure preceded code.
Tests cover immutable source mappings, duplicate/missing coordinates, wrong claims/
roles/components, excluded-well counts, fixed groups, missing/partial raw columns,
raw/mapping provenance, raw-grid failures, foreign-row filtering, unrelated-sheet
avoidance, no-Exp8-read sentinel and CLI path/error redaction. Synthetic mappings
are fabricated in test code; none is copied from a private map.

## Safe publication / handoff

Five-file scope only: `scientific_experiment_selection/raw_label_join.py`,
`tests/test_raw_label_join.py`, this report, append-only Notebook Entry 032 and
HANDOFF checkpoint. Existing mapping/raw reader, formulas, model code, decision
register, original labels and QC remain unchanged. No private source workbook,
derived label map, raw values or private manifest is staged. Privacy/path/secret,
whitespace and notebook checks precede authorized Draft publication. No merge.
Next owner: researcher + ChatGPT reviews this short aggregate result, then a separate
researcher decision is required for actual Exp3/Exp5 model fitting. Stop here.
