# Dataset provenance

No experimental data are included in the scaffold. Store raw exports unchanged in `data/raw/` (ignored by Git). Create a manifest listing SHA-256 hashes, date, instrument, plate/batch, preparation, sample, replicates, blank/QC classification, concentration, units, and permission to share. Scripts producing processed data must name their original sources. Git alone is not a second backup.

## Phase 1 inventory (Issue #3)

The read-only CLI enumerates **only explicitly supplied directories**, recursively,
including hidden files and all extensions. No copying, spectrum parsing, redaction,
uploading, or QC-based exclusions are implemented. Source directories must be stable
during a run. Do not run against actively changing instrument output directories.

From the repository root, replace the example source paths with researcher-confirmed
directories and choose a new output directory outside every source:

```bash
uv run python -m scientific_experiment_selection.inventory \
  --source export_a=/absolute/path/to/approved/exports \
  --source export_b=/absolute/path/to/another/approved/directory \
  --output /tmp/exp3-exp8-inventory-review \
  --data-kind researcher-provided
```

Use one or more `--source ID=DIRECTORY` arguments. IDs must be unique letters,
digits, underscores or hyphens; roots must not overlap. Omit a second source when
unneeded. Add `--backup-status confirmed-by-researcher` **only after** the researcher
confirms a separate backup. This flag records a declaration, not a backup audit.
The installed environment can run the same command with `.venv/bin/python` instead
of `uv run python`. No third-party runtime dependency or random seed is needed.

Outputs are `manifest.json` and `summary.md`. The manifest records source IDs and
resolved absolute roots, original relative filenames and final extensions (case
preserved), byte sizes, SHA-256, provisional experiment mapping and its path evidence,
unknown batch/plate IDs, and `inventoried_not_imported` status. It also records tool
and Python versions and operator-declared data kind. Review absolute source paths
before publication; outputs are local until approved. `researcher-provided` does
not assert that every file contains an observed spectrum.

Token matches such as `Exp3`, `Exp03` and `Exp7` in **relative paths** provide provisional
experiment evidence. No tokens, conflicting experiment numbers, or numbers outside
Exp3–Exp8 produce `UNKNOWN`. Source-root names and source IDs are deliberately not
treated as experimental metadata. Batch and plate remain `UNKNOWN`: Exp numbers
and technical replicates do not establish independently prepared batches. A later
reviewed metadata mapping is needed for stronger assignments.

The summary reports counts, bytes, duplicate checksum groups, unknown mappings and
expected experiments with no unambiguous filename evidence. Actual missing batches
cannot be identified until a researcher supplies an authoritative batch roster.
Every regular file is listed for relevance review; unrelated files are not silently
discarded. Symlinks and special filesystem entries are listed as excluded and not
followed/read. Read or traversal failures abort with a nonzero exit, rather than
silently emitting an incomplete inventory. Existing output directories and outputs
overlapping inputs are refused. A report-write failure may leave a partial output
directory; review it and select a fresh destination for the retry.

Outputs are deterministic for unchanged sources, root paths, arguments and Python/tool
versions; no timestamp or randomness is embedded. Hashing checks file identity, size,
and modification metadata around reads. This is not a filesystem snapshot: concurrent
directory changes are not fully guarded. Use quiescent, trusted local directories.
No copy verification is applicable because copying is not implemented.

## Scientific metadata for later curation

Record values from original lab records, their source references, and an explicit
unknown/not-recorded status rather than filling gaps by assumption.

| Field | Required context |
| --- | --- |
| Acquisition date/time | Timezone and original record |
| Instrument | Make/model, identifier, software/export version |
| Acquisition settings | Mode, wavelength range/spacing, integration time and other recorded settings |
| Raw axes and units | Wavelength and intensity/absorbance units, transformations already applied by instrument |
| Experiment, preparation batch, plate, well, sample | Distinct IDs and documented relationships; independence not assumed |
| Treatment/condition | Analyte, reagent conditions and recorded environmental conditions |
| Standard concentration | Value, unit, stock/dilution provenance |
| Technical replicate | Replicate group and relationship to preparation/sample |
| Blanks | Reagent/solvent/other type supported by records |
| QC flags | Original flag, reason, reviewer and evidence; preserve flagged raw records |
| Preparation recipe | Reagent identities/lots, volumes, order, timing and protocol reference |
| Provenance | Original relative path, source ID/root, checksum, size, owner and acquisition record |
| Sharing status | Permission scope, approver/date, restrictions and separate backup confirmation |

Issue #3 reports researcher permission for Exp3–Exp8 storage in the private repository;
the current instruction still prohibits raw upload, commit and push pending inventory
review. No `.gitignore` change is made. Exp7 G1:G6/F8, Exp8 F1:F3 and Exp5 B7 QC notes
from the issue are **unverified leads**, not assigned QC labels.

## Validation and current limitations

```bash
.venv/bin/python -m scientific_experiment_selection doctor
.venv/bin/python -m unittest discover -s tests -v
```

Tests generate small synthetic byte fixtures in temporary directories, exercise the
real CLI, and remove their temporary files afterward. These are software checks,
not simulated spectra or scientific results. See `docs/DATASET_INVENTORY.md` for the
current review checkpoint. Source paths and backup confirmation are still pending;
no real dataset manifest has yet been generated.
