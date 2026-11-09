"""Deterministic 18-fold Leave-One-Group-Out (LOGO) cross-validation plan for Exp3.

Standard-library only. Never reads raw data, fits models, or alters QC status.
Evaluates shared-solution condition groups under D-016, D-017, and D-019.
"""
from __future__ import annotations

import copy
import re
from typing import Any, Iterable, Sequence

EXPERIMENT_ID: str = 'Exp3'
EXP3_PFAS_CLASSES: tuple[str, ...] = ('TFA', 'PFPA', 'PFBA', 'PFHxA', 'PFOA', 'PFNA')
EXP3_CONCENTRATIONS: tuple[int, ...] = (5, 10, 20)
EXPECTED_GROUPS_COUNT: int = 18

_GROUP_ID_PATTERN = re.compile(
    r'^Exp3:(TFA|PFPA|PFBA|PFHxA|PFOA|PFNA)_(5|10|20)$'
)


def _validate_exact_concentration(value: Any, field_name: str = 'concentration') -> int:
    """Validate that a concentration value is an exact integer or integer string in {5, 10, 20}.

    Strictly rejects bool, float/fractional values (e.g. 5.9, 5.0), and malformed strings.
    """
    if isinstance(value, bool):
        raise ValueError(f"Boolean {field_name} not permitted (got {value!r}); use exact integer")
    if isinstance(value, float):
        raise ValueError(f"Float/fractional {field_name} not permitted (got {value!r}); use exact integer")
    if isinstance(value, int):
        conc_int = value
    elif isinstance(value, str):
        if not value.isascii() or not value.isdigit() or value != value.strip():
            raise ValueError(f"Invalid integer {field_name} string: {value!r}")
        conc_int = int(value)
    else:
        raise ValueError(f"Invalid {field_name} type: {type(value).__name__}")

    if conc_int not in EXP3_CONCENTRATIONS:
        raise ValueError(
            f"Unsupported {field_name}: {conc_int}; expected one of {EXP3_CONCENTRATIONS}"
        )
    return conc_int


def make_group_id(pfas: str, concentration: int | str, experiment_id: str = EXPERIMENT_ID) -> str:
    """Return canonical group identifier matching dataset_contract.py conventions.

    Concentration must be an exact integer or integer string in {5, 10, 20}.
    Float, fractional, or boolean values (e.g. 5.9, 5.0, True) are strictly rejected.
    """
    if experiment_id != EXPERIMENT_ID:
        raise ValueError(f"Unsupported experiment ID: {experiment_id!r}; expected {EXPERIMENT_ID!r}")
    if pfas not in EXP3_PFAS_CLASSES:
        raise ValueError(f"Unsupported PFAS class: {pfas!r}; expected one of {EXP3_PFAS_CLASSES}")

    conc_int = _validate_exact_concentration(concentration, field_name='concentration')
    return f"{experiment_id}:{pfas}_{conc_int}"


def parse_group_id(group_id: str) -> dict[str, Any]:
    """Parse and validate an Exp3 group identifier into structured metadata."""
    if not isinstance(group_id, str):
        raise ValueError(f"group_id must be a string, got {type(group_id).__name__}")
    match = _GROUP_ID_PATTERN.fullmatch(group_id)
    if not match:
        raise ValueError(
            f"Malformed or unexpected group ID: {group_id!r}. "
            f"Must match format 'Exp3:{{PFAS}}_{{5|10|20}}'."
        )
    pfas = match.group(1)
    conc = int(match.group(2))
    return {
        'group_id': group_id,
        'experiment_id': EXPERIMENT_ID,
        'condition': f"{pfas}_{conc}",
        'pfas_claim': pfas,
        'concentration_ppm': conc,
        'concentration_claim_ppm': str(conc),
    }


def validate_group_record(group: dict[str, Any]) -> dict[str, Any]:
    """Validate a group metadata dict against authoritative parsed metadata.

    Fails closed if any caller-supplied field contradicts the canonical parsed fields.
    Returns the authoritative record.
    """
    if not isinstance(group, dict):
        raise ValueError(f"Group record must be a dict, got {type(group).__name__}")
    gid = group.get('group_id')
    if not gid or not isinstance(gid, str):
        raise ValueError(f"Group record missing or invalid 'group_id': {gid!r}")

    authoritative = parse_group_id(gid)
    for key, expected_val in authoritative.items():
        if key in group:
            actual_val = group[key]
            if type(actual_val) is not type(expected_val) or actual_val != expected_val:
                raise ValueError(
                    f"Contradictory metadata in group {gid!r} for key {key!r}: "
                    f"supplied {actual_val!r} != authoritative {expected_val!r}"
                )

    alias_checks = (
        ('batch_claim', authoritative['experiment_id']),
        ('condition_claim', authoritative['condition']),
        ('label_claim', authoritative['pfas_claim']),
        ('technical_replicate_group', authoritative['group_id']),
    )
    for alias_key, expected_val in alias_checks:
        if alias_key in group:
            actual_val = group[alias_key]
            if type(actual_val) is not type(expected_val) or actual_val != expected_val:
                raise ValueError(
                    f"Contradictory metadata in group {gid!r} for key {alias_key!r}: "
                    f"supplied {actual_val!r} != authoritative {expected_val!r}"
                )

    return authoritative


def get_canonical_groups(experiment_id: str = EXPERIMENT_ID) -> tuple[dict[str, Any], ...]:
    """Return the 18 nominal Exp3 condition groups in fixed deterministic order.

    Order: by PFAS class (TFA -> PFNA), then concentration (5 -> 20 ppm).
    """
    if experiment_id != EXPERIMENT_ID:
        raise ValueError(f"Unsupported experiment ID: {experiment_id!r}; expected {EXPERIMENT_ID!r}")
    groups: list[dict[str, Any]] = []
    for pfas in EXP3_PFAS_CLASSES:
        for conc in EXP3_CONCENTRATIONS:
            grp_id = f"{experiment_id}:{pfas}_{conc}"
            groups.append(parse_group_id(grp_id))
    return tuple(groups)


def validate_group_ids(group_ids: Sequence[str]) -> list[str]:
    """Fail-closed validation of Exp3 condition group IDs.

    Verifies:
    - Exactly 18 group IDs provided
    - No duplicate IDs
    - Every ID matches the valid format and known PFAS/concentration set
    - Every canonical group is present
    """
    if len(group_ids) != EXPECTED_GROUPS_COUNT:
        raise ValueError(
            f"Expected exactly {EXPECTED_GROUPS_COUNT} groups, got {len(group_ids)}"
        )
    seen: set[str] = set()
    validated: list[str] = []
    for gid in group_ids:
        if not isinstance(gid, str):
            raise ValueError(f"Group ID must be a string, got {type(gid).__name__}")
        if gid in seen:
            raise ValueError(f"Duplicate group ID detected: {gid!r}")
        parse_group_id(gid)  # validates format
        seen.add(gid)
        validated.append(gid)

    canonical_ids = {g['group_id'] for g in get_canonical_groups()}
    missing = canonical_ids - seen
    if missing:
        raise ValueError(f"Missing expected canonical groups: {sorted(missing)}")
    unexpected = seen - canonical_ids
    if unexpected:
        raise ValueError(f"Unexpected groups detected: {sorted(unexpected)}")
    return validated


def generate_logo_plan(
    groups: Sequence[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return deterministic 18-fold Leave-One-Group-Out (LOGO) cross-validation records.

    Each record contains:
    - fold_index: 0 to 17
    - validation_group_id: string ID of the single held-out group
    - validation_group: dict metadata of held-out group (canonical & verified)
    - training_group_ids: tuple of 17 string IDs for training groups
    - training_groups: tuple of 17 dict metadata records for training groups
    - held_out_pfas: PFAS identity of held-out group
    - held_out_concentration_ppm: nominal concentration of held-out group
    - num_validation_groups: 1
    - num_training_groups: 17

    Folds are never shuffled or selected by outcomes.
    """
    if groups is None:
        group_list = list(get_canonical_groups())
    else:
        if len(groups) != EXPECTED_GROUPS_COUNT:
            raise ValueError(
                f"Expected exactly {EXPECTED_GROUPS_COUNT} groups, got {len(groups)}"
            )
        # Validate each group against authoritative metadata (rejects contradictory metadata)
        validated_groups = [validate_group_record(g) for g in groups]
        validate_group_ids([g['group_id'] for g in validated_groups])
        group_list = validated_groups

    folds: list[dict[str, Any]] = []
    for i, val_grp in enumerate(group_list):
        train_grps = [g for j, g in enumerate(group_list) if j != i]
        val_gid = val_grp['group_id']
        train_gids = tuple(g['group_id'] for g in train_grps)

        # Leakage guard: zero overlap between validation and training groups
        if val_gid in train_gids:
            raise RuntimeError(f"Group leakage detected in fold {i}: {val_gid} appears in training")

        fold_record = {
            'fold_index': i,
            'validation_group_id': val_gid,
            'validation_group': copy.deepcopy(val_grp),
            'training_group_ids': train_gids,
            'training_groups': tuple(copy.deepcopy(g) for g in train_grps),
            'held_out_pfas': val_grp['pfas_claim'],
            'held_out_concentration_ppm': val_grp['concentration_ppm'],
            'num_validation_groups': 1,
            'num_training_groups': len(train_grps),
        }
        folds.append(fold_record)

    verify_plan_integrity(folds)
    return folds


def verify_fold_leakage(fold_record: dict[str, Any]) -> bool:
    """Verify zero group leakage, canonical complement, and metadata integrity within a single fold record."""
    if not isinstance(fold_record, dict):
        raise ValueError(f"fold_record must be a dict, got {type(fold_record).__name__}")
    val_id = fold_record.get('validation_group_id')
    if not isinstance(val_id, str):
        raise ValueError("validation_group_id must be a string")

    val_meta = parse_group_id(val_id)

    # Check held-out summary fields if present
    if 'held_out_pfas' in fold_record and fold_record['held_out_pfas'] != val_meta['pfas_claim']:
        raise ValueError(
            f"Contradictory held_out_pfas: {fold_record['held_out_pfas']!r} != {val_meta['pfas_claim']!r}"
        )
    if 'held_out_concentration_ppm' in fold_record:
        hc = fold_record['held_out_concentration_ppm']
        if type(hc) is not int or hc != val_meta['concentration_ppm']:
            raise ValueError(
                f"Contradictory held_out_concentration_ppm: {hc!r} != {val_meta['concentration_ppm']!r}"
            )
    if 'num_validation_groups' in fold_record:
        nv = fold_record['num_validation_groups']
        if type(nv) is not int or nv != 1:
            raise ValueError(f"Invalid num_validation_groups: {nv!r}; expected 1")
    if 'num_training_groups' in fold_record:
        nt = fold_record['num_training_groups']
        if type(nt) is not int or nt != EXPECTED_GROUPS_COUNT - 1:
            raise ValueError(
                f"Invalid num_training_groups: {nt!r}; expected {EXPECTED_GROUPS_COUNT - 1}"
            )
    if 'validation_group' in fold_record:
        validate_group_record(fold_record['validation_group'])
        if fold_record['validation_group'].get('group_id') != val_id:
            raise ValueError(
                f"validation_group group_id {fold_record['validation_group'].get('group_id')!r} != {val_id!r}"
            )

    train_ids = fold_record.get('training_group_ids')
    if not isinstance(train_ids, (tuple, list)):
        raise ValueError("training_group_ids must be a tuple or list of strings")
    if len(train_ids) != EXPECTED_GROUPS_COUNT - 1:
        raise ValueError(
            f"Expected {EXPECTED_GROUPS_COUNT - 1} training groups, got {len(train_ids)}"
        )
    if val_id in train_ids:
        raise ValueError(f"Leakage: validation group {val_id!r} found in training groups")
    if len(set(train_ids)) != len(train_ids):
        raise ValueError("Duplicate training group IDs detected")
    overlap = set(train_ids) & {val_id}
    if overlap:
        raise ValueError(f"Leakage overlap detected: {overlap}")

    # Require each fold's training IDs to equal the exact canonical 17-group complement of its validation ID
    canonical_all = {g['group_id'] for g in get_canonical_groups()}
    expected_train_set = canonical_all - {val_id}
    train_set = set(train_ids)
    if train_set != expected_train_set:
        diff_unexpected = train_set - expected_train_set
        diff_missing = expected_train_set - train_set
        raise ValueError(
            f"Training groups do not match canonical complement of {val_id}. "
            f"Unexpected: {sorted(diff_unexpected)}, Missing: {sorted(diff_missing)}"
        )

    # Validate each training group ID string format
    for tid in train_ids:
        parse_group_id(tid)

    # Validate redundant training_groups metadata records if present
    if 'training_groups' in fold_record:
        tg_records = fold_record['training_groups']
        if not isinstance(tg_records, (tuple, list)) or len(tg_records) != len(train_ids):
            raise ValueError("training_groups length does not match training_group_ids")
        for i, tg in enumerate(tg_records):
            validate_group_record(tg)
            if tg.get('group_id') != train_ids[i]:
                raise ValueError(
                    f"training_groups[{i}] group_id {tg.get('group_id')!r} != training_group_ids[{i}] {train_ids[i]!r}"
                )

    return True


def verify_plan_integrity(folds: Sequence[dict[str, Any]]) -> bool:
    """Verify complete 18-fold LOGO plan integrity and coverage."""
    if len(folds) != EXPECTED_GROUPS_COUNT:
        raise ValueError(f"Expected {EXPECTED_GROUPS_COUNT} folds, got {len(folds)}")
    held_out_ids: list[str] = []
    for i, fold in enumerate(folds):
        if fold.get('fold_index') != i:
            raise ValueError(f"Fold index mismatch at position {i}: {fold.get('fold_index')}")
        verify_fold_leakage(fold)
        held_out_ids.append(fold['validation_group_id'])

    validate_group_ids(held_out_ids)
    return True


def _extract_sample_well(sample: dict[str, Any]) -> str | None:
    """Extract and validate optional physical well coordinate from a sample dict.

    Validates both 'physical_well' and 'well' independently when present and requires
    them to agree if both are supplied.
    """
    has_pw = 'physical_well' in sample
    has_w = 'well' in sample
    if not has_pw and not has_w:
        return None

    pw_val: str | None = None
    w_val: str | None = None
    if has_pw:
        raw_pw = sample['physical_well']
        if not isinstance(raw_pw, str) or not raw_pw.strip() or raw_pw != raw_pw.strip():
            raise ValueError(f"Sample has invalid physical_well: {raw_pw!r}")
        pw_val = raw_pw
    if has_w:
        raw_w = sample['well']
        if not isinstance(raw_w, str) or not raw_w.strip() or raw_w != raw_w.strip():
            raise ValueError(f"Sample has invalid well: {raw_w!r}")
        w_val = raw_w

    if pw_val is not None and w_val is not None and pw_val != w_val:
        raise ValueError(
            f"Sample physical_well {pw_val!r} contradicts well {w_val!r}"
        )
    return pw_val if pw_val is not None else w_val


def validate_sample_metadata(sample: dict[str, Any], group_key: str = 'technical_replicate_group') -> str:
    """Validate sample metadata consistency against its group ID.

    Independently validates every present redundant field (experiment_id, batch_claim,
    group_id, technical_replicate_group, condition_claim, condition, pfas_claim,
    label_claim, concentration_ppm, concentration_claim_ppm, physical_well, well)
    and rejects fractional/float or boolean concentration values.
    """
    if not isinstance(sample, dict):
        raise ValueError(f"Sample must be a dict, got {type(sample).__name__}")
    gid = sample.get(group_key)
    if not gid or not isinstance(gid, str):
        raise ValueError(f"Sample missing or invalid {group_key!r}: {gid!r}")

    parsed = parse_group_id(gid)

    # Validate well fields if present
    _extract_sample_well(sample)

    # Independently check every present group/experiment/condition/analyte field
    for g_alias in ('group_id', 'technical_replicate_group'):
        if g_alias in sample:
            val = sample[g_alias]
            if not isinstance(val, str) or val != parsed['group_id']:
                raise ValueError(
                    f"Sample {g_alias} {val!r} contradicts {group_key} {gid!r} (expected {parsed['group_id']!r})"
                )

    for exp_key in ('experiment_id', 'batch_claim'):
        if exp_key in sample:
            exp = sample[exp_key]
            if not isinstance(exp, str) or exp != parsed['experiment_id']:
                raise ValueError(
                    f"Sample {exp_key} {exp!r} contradicts {group_key} {gid!r} (expected {parsed['experiment_id']!r})"
                )

    for cond_key in ('condition_claim', 'condition'):
        if cond_key in sample:
            cond = sample[cond_key]
            if not isinstance(cond, str) or cond != parsed['condition']:
                raise ValueError(
                    f"Sample {cond_key} {cond!r} contradicts {group_key} {gid!r} (expected {parsed['condition']!r})"
                )

    for pfas_key in ('pfas_claim', 'label_claim'):
        if pfas_key in sample:
            pfas = sample[pfas_key]
            if not isinstance(pfas, str) or pfas != parsed['pfas_claim']:
                raise ValueError(
                    f"Sample {pfas_key} {pfas!r} contradicts {group_key} {gid!r} (expected {parsed['pfas_claim']!r})"
                )

    for conc_key in ('concentration_claim_ppm', 'concentration_ppm'):
        if conc_key in sample:
            raw_conc = sample[conc_key]
            try:
                conc_int = _validate_exact_concentration(raw_conc, field_name=conc_key)
            except ValueError as exc:
                raise ValueError(
                    f"Sample {conc_key} {raw_conc!r} invalid for {group_key} {gid!r}: {exc}"
                ) from exc
            if conc_int != parsed['concentration_ppm']:
                raise ValueError(
                    f"Sample {conc_key} {raw_conc!r} contradicts {group_key} {gid!r} "
                    f"(expected {parsed['concentration_ppm']} ppm)"
                )

    return gid


def split_samples_by_fold(
    fold_record: dict[str, Any],
    samples: Iterable[dict[str, Any]],
    group_key: str = 'technical_replicate_group',
    allow_empty_validation: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    """Deterministically partition sample records into training and validation sets.

    Note on group coverage:
    By default, this function partitions whatever sample subset is passed. It does NOT
    validate full condition-group coverage across the 18 groups unless checked via
    `validate_fold_evaluation_readiness` (or `allow_empty_validation=False` for the
    held-out group).

    Fail-closed validation:
    - Every sample must have valid `group_key` consistent with all present sample metadata.
    - Samples with unknown or unexpected group IDs raise ValueError.
    - Contradictory sample metadata or fractional concentrations raise ValueError.
    - Duplicate physical well IDs (when present) raise ValueError.
    - Replicates of the same solution stay strictly together on one side of the split.
    """
    verify_fold_leakage(fold_record)
    val_gid = fold_record['validation_group_id']
    train_gids = set(fold_record['training_group_ids'])

    training_samples: list[dict[str, Any]] = []
    validation_samples: list[dict[str, Any]] = []
    seen_wells: set[str] = set()

    for s_idx, sample in enumerate(samples):
        gid = validate_sample_metadata(sample, group_key=group_key)
        well_id = _extract_sample_well(sample)
        if well_id is not None:
            if well_id in seen_wells:
                raise ValueError(f"Duplicate physical well ID in samples: {well_id!r}")
            seen_wells.add(well_id)
        if gid == val_gid:
            validation_samples.append(sample)
        elif gid in train_gids:
            training_samples.append(sample)
        else:
            raise ValueError(
                f"Sample at index {s_idx} has unrecognized group {gid!r} "
                f"not in fold's validation or training groups"
            )

    if not allow_empty_validation and len(validation_samples) == 0:
        raise ValueError(
            f"Fold {fold_record.get('fold_index')} validation partition is empty: "
            f"no samples provided for held-out group {val_gid!r}"
        )

    return {
        'training': training_samples,
        'validation': validation_samples,
    }


def validate_fold_evaluation_readiness(
    split_result: dict[str, list[dict[str, Any]]],
    fold_record: dict[str, Any],
    min_validation_samples: int = 1,
    expected_training_groups: int = EXPECTED_GROUPS_COUNT - 1,
    group_key: str = 'technical_replicate_group',
) -> bool:
    """Validate condition-group coverage and fold/sample integrity before evaluation.

    Verifies:
    - `fold_record` passes full `verify_fold_leakage` integrity and complement checks.
    - Validation set is non-empty and has at least `min_validation_samples`.
    - Training set covers all `expected_training_groups` (17 canonical training groups).
    - Every validation and training sample passes `validate_sample_metadata` and belongs
      to the declared validation or training group set with zero group overlap.
    - Physical well identifiers (`physical_well` / `well`), when present, are consistent
      and strictly unique across and within training and validation partitions.

    Scope limitation: This check establishes condition-group coverage and metadata
    consistency, NOT full 70-well physical plate completeness or verified chemistry.
    """
    if not isinstance(split_result, dict):
        raise ValueError("split_result must be a dict with 'training' and 'validation' keys")
    if set(split_result.keys()) != {'training', 'validation'}:
        raise ValueError("split_result must contain exact keys {'training', 'validation'}")
    if isinstance(min_validation_samples, bool) or not isinstance(min_validation_samples, int) or min_validation_samples < 1:
        raise ValueError(f"min_validation_samples must be a positive integer, got {min_validation_samples!r}")
    if isinstance(expected_training_groups, bool) or not isinstance(expected_training_groups, int):
        raise ValueError(f"expected_training_groups must be an integer, got {expected_training_groups!r}")
    if expected_training_groups != EXPECTED_GROUPS_COUNT - 1:
        raise ValueError(
            f"expected_training_groups must equal {EXPECTED_GROUPS_COUNT - 1}, got {expected_training_groups}"
        )

    verify_fold_leakage(fold_record)

    val_samples = split_result['validation']
    train_samples = split_result['training']
    if not isinstance(val_samples, (list, tuple)) or not isinstance(train_samples, (list, tuple)):
        raise ValueError("'validation' and 'training' entries in split_result must be sequences")

    if len(val_samples) < min_validation_samples:
        raise ValueError(
            f"Validation set has {len(val_samples)} samples; expected at least {min_validation_samples}"
        )

    val_gid = fold_record['validation_group_id']
    expected_train_gids = set(fold_record['training_group_ids'])

    val_wells: set[str] = set()
    well_presence: list[bool] = []
    for s in val_samples:
        gid = validate_sample_metadata(s, group_key=group_key)
        if gid != val_gid:
            raise ValueError(f"Sample in validation set has group {gid!r} != {val_gid!r}")
        well_id = _extract_sample_well(s)
        well_presence.append(well_id is not None)
        if well_id is not None:
            if well_id in val_wells:
                raise ValueError(f"Duplicate physical well ID in validation set: {well_id!r}")
            val_wells.add(well_id)

    train_gids: set[str] = set()
    train_wells: set[str] = set()
    for s in train_samples:
        gid = validate_sample_metadata(s, group_key=group_key)
        if gid == val_gid:
            raise ValueError(f"Leakage: validation group {val_gid!r} sample found in training set")
        if gid not in expected_train_gids:
            raise ValueError(f"Sample in training set has unexpected group {gid!r}")
        train_gids.add(gid)
        well_id = _extract_sample_well(s)
        well_presence.append(well_id is not None)
        if well_id is not None:
            if well_id in val_wells:
                raise ValueError(
                    f"Overlapping physical well ID between validation and training: {well_id!r}"
                )
            if well_id in train_wells:
                raise ValueError(f"Duplicate physical well ID in training set: {well_id!r}")
            train_wells.add(well_id)

    if any(well_presence) and not all(well_presence):
        raise ValueError(
            "Inconsistent physical well metadata: some samples specify physical_well/well while others omit it"
        )

    missing_train = expected_train_gids - train_gids
    if missing_train:
        raise ValueError(
            f"Training set incomplete: missing samples for {len(missing_train)} expected group(s): {sorted(missing_train)}"
        )

    if len(train_gids) != expected_training_groups:
        raise ValueError(
            f"Training set covers {len(train_gids)} groups; expected {expected_training_groups}"
        )

    return True
