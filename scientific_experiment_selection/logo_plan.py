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


def make_group_id(pfas: str, concentration: int | str, experiment_id: str = EXPERIMENT_ID) -> str:
    """Return canonical group identifier matching dataset_contract.py conventions.

    Concentration must be an exact integer or integer string in {5, 10, 20}.
    Float or fractional values (e.g. 5.9) are strictly rejected.
    """
    if experiment_id != EXPERIMENT_ID:
        raise ValueError(f"Unsupported experiment ID: {experiment_id!r}; expected {EXPERIMENT_ID!r}")
    if pfas not in EXP3_PFAS_CLASSES:
        raise ValueError(f"Unsupported PFAS class: {pfas!r}; expected one of {EXP3_PFAS_CLASSES}")

    if isinstance(concentration, float):
        raise ValueError(f"Float concentration not permitted (got {concentration!r}); use exact integer")
    elif isinstance(concentration, int):
        conc_int = concentration
    elif isinstance(concentration, str):
        s = concentration.strip()
        if not s.isdigit():
            raise ValueError(f"Invalid integer concentration string: {concentration!r}")
        conc_int = int(s)
    else:
        raise ValueError(f"Invalid concentration type: {type(concentration).__name__}")

    if conc_int not in EXP3_CONCENTRATIONS:
        raise ValueError(
            f"Unsupported concentration: {conc_int}; expected one of {EXP3_CONCENTRATIONS}"
        )
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
            if actual_val != expected_val:
                raise ValueError(
                    f"Contradictory metadata in group {gid!r} for key {key!r}: "
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
    val_id = fold_record.get('validation_group_id')
    if not isinstance(val_id, str):
        raise ValueError("validation_group_id must be a string")

    val_meta = parse_group_id(val_id)

    # Check held-out summary fields if present
    if 'held_out_pfas' in fold_record and fold_record['held_out_pfas'] != val_meta['pfas_claim']:
        raise ValueError(
            f"Contradictory held_out_pfas: {fold_record['held_out_pfas']!r} != {val_meta['pfas_claim']!r}"
        )
    if 'held_out_concentration_ppm' in fold_record and fold_record['held_out_concentration_ppm'] != val_meta['concentration_ppm']:
        raise ValueError(
            f"Contradictory held_out_concentration_ppm: {fold_record['held_out_concentration_ppm']!r} != {val_meta['concentration_ppm']!r}"
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
        if len(tg_records) != len(train_ids):
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


def validate_sample_metadata(sample: dict[str, Any], group_key: str = 'technical_replicate_group') -> str:
    """Validate sample metadata consistency against its group ID.

    Fails closed if any optional metadata (experiment_id, condition, condition_claim,
    pfas_claim, label_claim, concentration_ppm, concentration_claim_ppm) contradicts
    the parsed authoritative group.
    """
    if not isinstance(sample, dict):
        raise ValueError(f"Sample must be a dict, got {type(sample).__name__}")
    gid = sample.get(group_key)
    if not gid or not isinstance(gid, str):
        raise ValueError(f"Sample missing or invalid {group_key!r}: {gid!r}")

    parsed = parse_group_id(gid)

    # Consistency checks on optional keys
    exp = sample.get('experiment_id')
    if exp is not None and exp != parsed['experiment_id']:
        raise ValueError(
            f"Sample experiment_id {exp!r} contradicts {group_key} {gid!r} (expected {parsed['experiment_id']!r})"
        )

    cond = sample.get('condition_claim') or sample.get('condition')
    if cond is not None and cond != parsed['condition']:
        raise ValueError(
            f"Sample condition {cond!r} contradicts {group_key} {gid!r} (expected {parsed['condition']!r})"
        )

    pfas = sample.get('pfas_claim') or sample.get('label_claim')
    if pfas is not None and pfas != parsed['pfas_claim']:
        raise ValueError(
            f"Sample PFAS claim {pfas!r} contradicts {group_key} {gid!r} (expected {parsed['pfas_claim']!r})"
        )

    conc = sample.get('concentration_claim_ppm')
    if conc is not None and str(conc) != parsed['concentration_claim_ppm']:
        raise ValueError(
            f"Sample concentration_claim_ppm {conc!r} contradicts {group_key} {gid!r} (expected {parsed['concentration_claim_ppm']!r})"
        )

    conc_num = sample.get('concentration_ppm')
    if conc_num is not None:
        try:
            if int(conc_num) != parsed['concentration_ppm']:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError(
                f"Sample concentration_ppm {conc_num!r} contradicts {group_key} {gid!r} (expected {parsed['concentration_ppm']!r})"
            )

    return gid


def split_samples_by_fold(
    fold_record: dict[str, Any],
    samples: Iterable[dict[str, Any]],
    group_key: str = 'technical_replicate_group',
    allow_empty_validation: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    """Deterministically partition sample records into training and validation sets.

    Note on dataset completeness:
    By default, this function partitions whatever sample subset is passed. It does NOT
    validate overall dataset completeness (e.g. that all conditions are present on the plate).
    To reject empty validation partitions, set `allow_empty_validation=False`, or use
    `validate_fold_evaluation_readiness`.

    Fail-closed validation:
    - Every sample must have valid `group_key` consistent with optional sample metadata.
    - Samples with unknown or unexpected group IDs raise ValueError.
    - Contradictory sample metadata (e.g. experiment_id='Exp5' with group 'Exp3:TFA_5') raises ValueError.
    - Replicates of the same solution stay strictly together on one side of the split.
    """
    verify_fold_leakage(fold_record)
    val_gid = fold_record['validation_group_id']
    train_gids = set(fold_record['training_group_ids'])

    training_samples: list[dict[str, Any]] = []
    validation_samples: list[dict[str, Any]] = []

    for s_idx, sample in enumerate(samples):
        gid = validate_sample_metadata(sample, group_key=group_key)
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
    """Validate evaluation readiness for a split before any model fitting or evaluation.

    Verifies:
    - Validation set is non-empty and has at least `min_validation_samples`.
    - Training set covers all 17 expected training groups (no missing training conditions).
    - Zero overlap between validation and training samples.
    """
    val_samples = split_result.get('validation', [])
    train_samples = split_result.get('training', [])

    if len(val_samples) < min_validation_samples:
        raise ValueError(
            f"Validation set has {len(val_samples)} samples; expected at least {min_validation_samples}"
        )

    val_gid = fold_record['validation_group_id']
    for s in val_samples:
        if s.get(group_key) != val_gid:
            raise ValueError(f"Sample in validation set has group {s.get(group_key)!r} != {val_gid!r}")

    train_gids = {s.get(group_key) for s in train_samples}
    expected_train_gids = set(fold_record['training_group_ids'])

    missing_train = expected_train_gids - train_gids
    if missing_train:
        raise ValueError(
            f"Training set incomplete: missing samples for {len(missing_train)} expected group(s): {sorted(missing_train)}"
        )

    unexpected_train = train_gids - expected_train_gids
    if unexpected_train:
        raise ValueError(
            f"Training set has unexpected group(s): {sorted(unexpected_train)}"
        )

    return True
