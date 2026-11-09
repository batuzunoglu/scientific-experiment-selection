# Issue #23 — private Exp3 provisional-label eligibility audit

Owner: Codex. Scientific reviewers: researcher + ChatGPT.
Status: **consistent pending scientific review; training permission NO**.
Authority: Issue #23, D-020 and Notebook Entry 025. Base: latest main after PR #22,
`f08acbd`, on dedicated `feature/phase-b-exp3-eligibility-audit`.

## Observed aggregate findings

| Check | Count |
| --- | ---: |
| Exp3 coordinates / unique coordinates | 96 / 96 |
| Original candidate rows / noncandidate rows | 72 / 24 |
| Analysis-level primary exclusions only | 2 |
| Provisional primary candidates | 70 |
| Primary condition groups retained | 18 |
| Retained members in the special reduced group | 2 |
| Disclosed historical-note candidates retained | 3 |
| Original candidate QC-review records preserved | 2 |
| Physically unverified records / records with source warnings | 96 / 96 |
| Existing conflict-warning records | 7 |
| Existing historical-findings-warning records | 7 |
| New structural/claim/provenance discrepancies | 0 |

Warning categories may overlap; their counts must not be added as independent
records. Expected missing independent preparation/verification evidence is baseline
uncertainty, not a new structural failure. Existing conflicts are retained outside
the individual candidate pool; no alternative is resolved. The historical-note
category is disclosed under Issue #23, not newly inferred from spectral data.

The private input is the existing Phase A candidate metadata manifest documented
in PHASE_A_REVIEW.md. No private path, digest, actual record, source text,
class-by-well assignment, per-well output or spectrum is included here. The combined
JSON is parsed locally, then only records whose experiment_id equals Exp3 enter
validation/diagnostics. Foreign records are ignored without diagnostics, even if
malformed. This is not authorization to inspect other experiments. No raw workbook
was opened; no Exp5/Exp8 records entered analysis or output.

## Implementation and limits

`scripts/audit_exp3_eligibility.py` checks coordinate coverage/uniqueness, metadata
presence, preserved false verification/training/independence flags, nominal candidate
claims/components/group agreement, provenance references and internal source-link
consistency, source QC/partition preservation, original count structure and the
approved analysis-only exclusion. It never writes the input or returns row records.
Before/after input bytes are compared locally; no digest is emitted. The script
imports no raw-reader, spectral-transform or model code. Output is limited to fixed
categories and counts; CLI errors suppress private values, paths and tracebacks.

Missing required fields, contradictory claims, unexpected provenance/QC flags or
count/group mismatches produce `review-needed` with aggregate categories/counts and
CLI exit 2. No repair, additional exclusion or relabeling is attempted. Success is
exit 0 with `consistent-pending-scientific-review`, never training authorization.
`training_permission` and `chemical_verification` remain false in the summary.

The separate `synthetic_logo_check()` calls the existing planner using canonical
synthetic group metadata only: **18 folds, 18 distinct validation-group visits,
zero group overlap**. Real manifest rows are not partitioned or fitted in this task.
No new CV design, model/metric choice or preprocessing is introduced.

This establishes consistency of inherited provisional metadata, not physical label
truth, source authenticity, new experimental presence verification, complete lab
records or independent preparations. Raw source digests are checked only for valid
metadata form and internal consistency; raw files are deliberately not rehashed.
Historical-note disclosure is not independent preparation evidence. Group proxies
and same-solution reports do not certify between-condition independence. D-020 and
all original source flags remain unchanged; label eligibility and model/metric
settings still require researcher + ChatGPT review under Issue #21 before fitting.

## Commands and software evidence

Private CLI usage (set the variable locally; never share its value):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python scripts/audit_exp3_eligibility.py --manifest "$EXP3_CANDIDATE_MANIFEST"
```

The following exact wrapper was executed from the repository root to locate the
single documented Phase A manifest without printing its location. Both audit
invocations exited 0; final output contained only the aggregate findings above.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python - <<'PY'
from pathlib import Path
import re,subprocess,os,json
from scripts.audit_exp3_eligibility import synthetic_logo_check
roots=re.findall(r'`(data/private/[^`\n]+-final/?)`',Path('docs/PHASE_A_REVIEW.md').read_text())
sources=[Path(p)/'candidate_wells.json' for p in dict.fromkeys(roots)]
sources=[p for p in sources if p.is_file()]
if len(sources)!=1:
 print(json.dumps({'status':'review-needed','new_inconsistencies':{'source_resolution':1}}))
 raise SystemExit(2)
r=subprocess.run(['.venv/bin/python','scripts/audit_exp3_eligibility.py','--manifest',str(sources[0])],capture_output=True,text=True,env=dict(os.environ,PYTHONPATH='.',PYTHONDONTWRITEBYTECODE='1'))
print(r.stdout.strip())
print('audit_exit_code:',r.returncode)
if r.stderr:
 print('Unexpected stderr suppressed; review-needed')
 raise SystemExit(2)
if r.returncode: raise SystemExit(r.returncode)
print('Synthetic LOGO only:',json.dumps(synthetic_logo_check(),sort_keys=True))
PY
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -p test_exp3_eligibility.py -v
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Observed: **11/11 new synthetic tests**, **57/57 full-suite tests**, exit 0.
Baseline: 46 tests passed before implementation. Artificial fixtures are generated
in test code, never copied from the private manifest. Tests cover source preservation,
aggregate success counts, foreign-record exclusion before diagnostics, malformed and
missing input redaction, missing/duplicate coordinates, invalid/promoted flags,
contradictory source and inherited claims, component metadata, unexpected warnings,
source-reference/role mismatches, only-approved exclusion, and synthetic LOGO isolation.
Initial missing-module failure preceded implementation; later failing synthetic
regressions drove tighter candidate-conflict, lineage and source checks. No private
record was repaired. Python 3.12.14, standard library only, no random seed needed.

## Publication / review gate

Allowlist (five files):
- `scripts/audit_exp3_eligibility.py`
- `tests/test_exp3_eligibility.py`
- `docs/EXP3_ELIGIBILITY_AUDIT.md`
- `docs/RESEARCH_LAB_NOTEBOOK.md` (append Entry 026)
- `docs/HANDOFF.md` (new checkpoint)

Exclude all private manifests/outputs, raw XLSX, source exports and unrelated files.
No changes to DECISIONS.md or original label/QC metadata. The staged full diff,
credential/private-content scan, notebook append check and tests must pass before
commit/push. Issue #23 permits a Draft PR of this safe scope for independent review;
it grants no merge or training permission. Next owner: ChatGPT/researcher reviews
the aggregate evidence and remaining protocol gates; stop before any model fit.

Pre-publication result: staged five-file allowlist and full new diff reviewed;
privacy/credential-pattern scan, append-only notebook/handoff and staged whitespace
checks passed. Only synthetic fixtures and explicitly approved rule constants are
in source/tests. No actual metadata row or private artifact is proposed for Git.

CI portability follow-up: first Draft PR #25 run passed notebook gate but failed
two new CLI tests because they assumed a local virtual environment interpreter.
The test subprocesses now use `sys.executable`. Reproduced the failure and confirmed
57/57 passes after correction in an isolated copy of public code/scripts/tests with
no local virtual environment, as well as in the full repository. No audit logic,
real metadata/result or scientific policy changed; no private data was reopened.
Notebook Entry 027 preserves this negative result and correction.
