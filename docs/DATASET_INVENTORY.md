# Issue #3 — Phase 1 review checkpoint

Date: 2026-10-21. Branch: `data/dataset-inventory`.
Base: `7996a8bfa743f65b6d9589d98419d726c2bccefb` (freshly fetched `origin/main`).
Issue: https://github.com/batuzunoglu/scientific-experiment-selection/issues/3

## Implemented locally

- Standard-library, CPU-runnable, read-only inventory CLI and synthetic integration tests.
- Deterministic JSON manifest and Markdown summary, SHA-256 and byte counts,
  duplicate groups, provisional experiment mappings and unknown/missing-evidence reporting.
- Explicit source roots, no symlink traversal, no overwrite of existing output,
  and no output inside source directories.
- Metadata guidance and limitations in [data/README.md](../data/README.md).

## Pending researcher input

- Specific Exp3–Exp8 source directories. No home-directory search was performed.
- Confirmation that source data are backed up separately from GitHub.
- Authoritative experiment/batch/plate mapping and expected batch roster.

No real file counts, sizes, hashes, duplicates, missing batches, spectrum observations,
or QC findings are claimed. No real files were read/copied/uploaded. Git versus LFS
will be assessed using actual sizes after the source inventory is available.
Phase 1 is **not complete** until real inventory generation, backup confirmation and review.

## Changed files

- `scientific_experiment_selection/inventory.py`: new executable inventory module.
- `tests/test_inventory.py`: six synthetic CLI integration tests.
- `data/README.md`: invocation, schema interpretation, metadata fields and limitations.
- `docs/DATASET_INVENTORY.md`: this review record.
- `docs/HANDOFF.md`, `docs/DECISIONS.md`, `docs/LEARNING_LOG.md`: checkpoint and rationale.

## Observed verification

Exact commands run from the repository root:

```bash
git fetch origin main
git rev-parse HEAD origin/main
git status --short
git switch -c data/dataset-inventory origin/main
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest discover -s tests -p test_inventory.py -v
.venv/bin/python -m scientific_experiment_selection doctor
gh repo view batuzunoglu/scientific-experiment-selection --json nameWithOwner,isPrivate
git diff --check
```

- Baseline: 2 tests passed. Before implementation: all 6 inventory tests failed
  because the module did not exist (after strengthening an error-path assertion).
- After implementation: 8 tests passed, including all 6 inventory tests.
- Doctor: exit 0; Python 3.12.14, Linux, project 0.1.0, `scientific_runs: none`.
- GitHub query: `isPrivate: true`. No visibility setting was changed.
- Initial fetch was blocked by read-only `.git`; approved retry fetched and created
  the branch. Initial `gh` request was network-blocked; approved read-only retry succeeded.
- `git diff --check`: exit 0. Nothing staged, committed or pushed.

Observed outcomes are software/infrastructure behavior using **synthetic bytes**.
No laboratory measurements, simulated spectra, model runs or benchmark scores.

## Remaining limitations

No metadata ingestion, import/copy operation, content validation, automatic relevance
classification, batch-independence validation, or QC adjudication is implemented.
The tool needs stable local directories; it is not a concurrent filesystem snapshot.
Manifests include absolute source roots and require review before publication.
Approval to inspect files does not imply approval to import or publish them.


## 2026-10-22 — Actual Exp1–Exp8 inventory; stopped for review

This checkpoint supersedes the earlier pending-source statements above.
Read Issue #3 and its sole/latest comment:
https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6328247164

Source: `/home/batuhan/research/raw-experiment-results` (read-only).
Branch retained: `data/dataset-inventory`; HEAD:
`7996a8bfa743f65b6d9589d98419d726c2bccefb`.
All seven pre-existing uncommitted files retained; no source or code edits.
Eight regular files, 685147 bytes, zero duplicate checksum groups, zero excluded
filesystem entries. Exp1–Exp8 filenames are all present. Filename labels are not
validated experiment, preparation-batch or plate identities.

| Exact relative filename | Bytes | SHA-256 |
| --- | ---: | --- |
| `Exp1 Plt1.xlsx` | 108875 | `f41b973b8b96dd6eaef19bf7adf4b17a4cc89914fd0d3c48480df00c5b581079` |
| `Exp2 Plt2.xlsx` | 39645 | `248c56908c6e8cba5a6d7bb2ddb4861137ea66787057f23bfc873736ecc07d0f` |
| `Exp3 Plt3.xlsx` | 119456 | `4e40ee5e4a5056904f783bfc05bb55cea6888104c5fec0517335710143b6915f` |
| `Exp4 Plt4.xlsx` | 103576 | `68f1a5672f63f02f97e84aaf20892bd312ed6fc83d974e96e3247ee2a7bedb34` |
| `Exp5 Plt5.xlsx` | 92408 | `0d085b016c2bf4a058d2d8280b68c312654885a035c87eeb9df3f3d7f7a44b84` |
| `Exp6 Plt6.xlsx` | 85381 | `d956d53ab6830827f995cc0780bff7c6908ca281785d9ec073415911994affc6` |
| `Exp7 Plt7.xlsx` | 96831 | `9808580f38e0c35f97bff3c3f6d6d63831dec86bc47f2e2b0b17166649c2f32d` |
| `Exp8 Plt8.xlsx` | 38975 | `2d41c98a230bd017a13d9bc3e22c2b2812ca1d3efc59772a47a1d4e4631a9f19` |

Exp8's local checksum exactly matches the recovered attachment checksum documented
in the issue comment. This establishes byte identity with that reference, not its
scientific identity, acquisition provenance or QC validity.

Machine-readable manifest: `/tmp/issue-3-inventory-2026-10-22/manifest.json`.
Human-readable CLI output: `/tmp/issue-3-inventory-2026-10-22/summary.md`.
These temporary artifacts remain local; the complete file table is retained here.
Existing CLI scope limitation: Exp1 and Exp2 are hashed and listed but their
`experiment` fields remain `UNKNOWN` because its mapper recognizes only Exp3–Exp8.
The CLI missing-expected list covers only Exp3–Exp8. Direct inspection of all eight
manifest filenames confirms filename presence across Exp1–Exp8. No code changed.

### Missing evidence before scientific analysis or import

- An independently documented well-to-condition mapping: original lab notebook,
  plate-layout record or preparation sheet, linked to these files and wells;
  analyte identities, concentrations and units, blanks/controls, reagent conditions,
  replicate/sample relationships, and source reference/version/author for each entry.
- QC decisions supported by original records, with reason, reviewer and evidence.
  Issue notes about Exp7 G1:G6/F8, Exp8 F1:F3 and Exp5 B7 remain unverified leads.
- Acquisition dates, instrument/settings, axes/units and export processing history;
  preparation recipes, stock/dilution provenance, batch and plate roster, and
  evidence of independence for any later evaluation split.
- Separate backup confirmation and Exp8 recovery/acquisition provenance.
- Sharing authorization for Exp1–Exp2 is not established by the issue's original
  Exp3–Exp8 sharing statement. Local inventory authorization is not upload approval.

The source contains only the eight XLSX files, with no separate mapping sidecar.
Workbook contents were not parsed; this does not establish whether embedded
metadata exist. No well identities, concentrations or QC labels were inferred.
No spectra, scientific outcomes or simulated measurements were produced.

### Commands and observed verification

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.inventory --source raw_exports=/home/batuhan/research/raw-experiment-results --output /tmp/issue-3-inventory-2026-10-22 --data-kind researcher-provided
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
sha256sum /home/batuhan/research/raw-experiment-results/*.xlsx
git diff --check
git status --short --branch
```

The inventory command exited 0. For reruns choose a fresh output path; existing
output is deliberately refused. All eight software tests passed (synthetic byte
fixtures/infrastructure, not scientific validation). Independent `sha256sum`
output matched every manifest hash. Backup status remains unconfirmed.
No import, raw copy, commit, push, upload, GitHub comment or scientific analysis.
Session changes: appended this report and entries in `docs/HANDOFF.md`,
`docs/DECISIONS.md`, `docs/LEARNING_LOG.md`; generated the two local /tmp reports.
Next step: researcher reviews inventory and supplies authoritative mapping and
backup/provenance evidence before further work.
