"""Issue #23: private read-only Exp3 metadata audit; aggregate output only.

No raw-spectrum reader, feature transform, model or private output export.
All errors are fixed categories; private values and exceptions are never echoed.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from scientific_experiment_selection.logo_plan import (
    get_canonical_groups, generate_logo_plan, parse_group_id,
    validate_sample_metadata, verify_plan_integrity,
)

WELLS = frozenset(f'{r}{c}' for r in 'ABCDEFGH' for c in range(1, 13))
PRIMARY_EXCLUSIONS = frozenset(('D6', 'D7'))  # Public D-016 rule; never edits source.
HISTORICAL_NOTE_WELLS = frozenset(('B4', 'B5', 'C9'))  # Disclose, do not exclude.
WARNINGS = frozenset(('physical_label_not_independently_verified',
    'preparation_group_unknown', 'preparation_status_missing', 'qc_review',
    'unresolved_conflict', 'historical_findings_preserved',
    'missing_component_claims_not_imputed'))
BASE_WARNINGS = frozenset(('physical_label_not_independently_verified',
    'preparation_group_unknown', 'preparation_status_missing'))
REQUIRED = frozenset(('batch_claim', 'physical_well', 'candidate_included',
    'spectrum_present', 'condition_claim', 'label_claim', 'concentration_claim_ppm',
    'component_claims_ppm', 'technical_replicate_group', 'preparation_group',
    'group_independence_verified', 'physical_label_verified', 'training_authorized',
    'label_status', 'preparation_status', 'source_sha256', 'source_file',
    'source_sheet', 'raw_header_cell', 'raw_value_range', 'qc_status_claim',
    'qc_reason_claim', 'warnings', 'source_evidence'))


def synthetic_logo_check():
    """Exercise planner on canonical synthetic group metadata only, never real rows."""
    plan = generate_logo_plan(get_canonical_groups())
    verify_plan_integrity(plan)
    overlap = sum(len(set(f['training_group_ids']) & {f['validation_group_id']}) for f in plan)
    return {'folds': len(plan), 'group_overlap_count': overlap,
            'validation_group_visits': len({f['validation_group_id'] for f in plan})}


def audit_exp3(records):
    """Filter first; inspect only Exp3. No row/source text leaves this function.

    Returns counts and fixed-category discrepancies, never repaired records or
    authorization. Group checks are an audit of claims, not verified chemistry.
    """
    if not isinstance(records, list):
        return failure('input_schema')
    rows = [r for r in records if isinstance(r, dict) and r.get('experiment_id') == 'Exp3']
    issues = Counter()
    counts = Counter()
    seen = set()
    digests = set()
    source_files = set()
    groups = Counter()
    primary_groups = Counter()
    retained_special = set()
    candidate_wells = set()
    for row in rows:
        errors = set()
        if not REQUIRED <= row.keys():
            issues['missing_required_metadata'] += 1
            continue  # Result fails closed; no inferred or repaired record.
        well = row['physical_well']
        valid_well = isinstance(well, str) and well in WELLS
        if not valid_well: errors.add('invalid_coordinate')
        elif well in seen: errors.add('duplicate_coordinate')
        else: seen.add(well)
        candidate = row['candidate_included']
        if type(candidate) is not bool: errors.add('invalid_candidate_flag')
        for name in ('physical_label_verified', 'training_authorized', 'group_independence_verified'):
            if row[name] is not False: errors.add('unexpected_verification_or_authorization')
        if row['batch_claim'] != 'Exp3': errors.add('contradictory_batch')
        if (row['label_status'] != 'provisional_not_independently_verified'
                or row['preparation_status'] != 'unknown' or row['preparation_group'] != 'UNKNOWN'):
            errors.add('unexpected_provenance_status')
        warnings = row['warnings']
        if (not isinstance(warnings, list) or not all(isinstance(w, str) for w in warnings)
                or not set(warnings) <= WARNINGS or not BASE_WARNINGS <= set(warnings)):
            errors.add('unexpected_provenance_flags')
        else:
            counts['records_with_source_warnings'] += bool(warnings)
            counts['records_with_unresolved_conflict_warning'] += 'unresolved_conflict' in warnings
            counts['records_with_historical_findings_warning'] += 'historical_findings_preserved' in warnings
        if row['spectrum_present'] is not True: errors.add('missing_presence_metadata')
        sha = row['source_sha256']
        if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
            errors.add('missing_or_invalid_provenance')
        else: digests.add(sha)
        if (not isinstance(row['source_file'], str) or not row['source_file']
                or row['source_sheet'] != 'Sheet1'
                or not re.fullmatch('[A-Z]+1', str(row['raw_header_cell']))
                or not re.fullmatch('[A-Z]+2:[A-Z]+177', str(row['raw_value_range']))):
            errors.add('missing_or_invalid_provenance')
        else: source_files.add(row['source_file'])
        evidence = row['source_evidence']
        if not isinstance(evidence, dict):
            errors.add('missing_required_provenance')
            evidence = {}
        pairs = (('experiment_id', 'experiment_id'), ('physical_well', 'well'),
                 ('source_sha256', 'sha256'), ('source_file', 'raw_file'),
                 ('condition_claim', 'condition_claim'), ('qc_status_claim', 'historical_qc_status'),
                 ('raw_header_cell', 'raw_header_cell'), ('raw_value_range', 'raw_value_range'),
                 ('qc_reason_claim', 'historical_qc_reason'))
        if any(row.get(a) != evidence.get(b) for a, b in pairs):
            errors.add('contradictory_source_metadata')
        if any(not isinstance(evidence.get(k), str) or not evidence[k]
               for k in ('draft_reference', 'uploaded_master_reference', 'layout_source', 'historical_variants')):
            errors.add('missing_required_provenance')
        variants = []
        try:
            variants = json.loads(evidence.get('historical_variants', 'null'))
            if not isinstance(variants, list) or not all(isinstance(v, dict) for v in variants):
                errors.add('invalid_lineage_metadata')
                variants = []
        except (ValueError, TypeError):
            errors.add('invalid_lineage_metadata')
        if any(evidence.get(k) != '176' for k in ('nonempty_points', 'numeric_points')):
            errors.add('contradictory_presence_metadata')
        if type(candidate) is bool:
            individual = evidence.get('master_partition') == 'individual_dataset'
            if candidate != individual: errors.add('candidate_partition_disagreement')
        if candidate is True:
            counts['candidate_rows'] += 1
            if evidence.get('master_use_in_model') != 'Yes':
                errors.add('candidate_source_role_disagreement')
            if any(v.get('condition') not in (None, '', row['condition_claim']) for v in variants):
                errors.add('contradictory_inherited_condition')
            if isinstance(warnings, list) and 'unresolved_conflict' in warnings:
                errors.add('unexpected_candidate_conflict')
            if valid_well: candidate_wells.add(well)
            if row['qc_status_claim'] not in ('include', 'review'):
                errors.add('unexpected_candidate_qc')
            if row['qc_status_claim'] == 'review' and valid_well and well not in PRIMARY_EXCLUSIONS:
                errors.add('unexpected_candidate_review')
            if valid_well and well in PRIMARY_EXCLUSIONS and row['qc_status_claim'] != 'review':
                errors.add('missing_known_review_flag')
            if row['qc_status_claim'] == 'review': counts['candidate_qc_review'] += 1
            try:
                gid = validate_sample_metadata(row)
                parsed = parse_group_id(gid)
                components = row['component_claims_ppm']
                classes = {g['pfas_claim'] for g in get_canonical_groups()}
                if not isinstance(components, dict) or set(components) != classes:
                    errors.add('missing_component_metadata')
                else:
                    for pfas, value in components.items():
                        if value in ('', None): errors.add('missing_component_metadata')
                        elif str(value) != str(parsed['concentration_ppm'] if pfas == parsed['pfas_claim'] else 0):
                            errors.add('contradictory_component_claim')
                if components != json.loads(evidence.get('master_composition_ppm', 'null')):
                    errors.add('contradictory_component_source')
                groups[gid] += 1
                if valid_well and well not in PRIMARY_EXCLUSIONS:
                    primary_groups[gid] += 1
                    if gid == 'Exp3:PFHxA_10': retained_special.add(well)
            except (ValueError, TypeError, KeyError):
                errors.add('contradictory_condition_claim')
            if valid_well and well in PRIMARY_EXCLUSIONS: counts['analysis_only_exclusions'] += 1
            else: counts['primary_candidates'] += 1
            if valid_well and well in HISTORICAL_NOTE_WELLS:
                counts['disclosed_note_candidates_retained'] += 1
        else:
            counts['noncandidate_rows'] += candidate is False
        issues.update(errors)
    counts['coordinates'] = len(rows)
    counts['unique_coordinates'] = len(seen)
    counts['primary_groups'] = len(primary_groups)
    counts['special_group_retained'] = len(retained_special)
    counts['provisional_records'] = sum(r.get('physical_label_verified') is False for r in rows)
    expected_counts = {'coordinates': 96, 'unique_coordinates': 96, 'candidate_rows': 72,
        'noncandidate_rows': 24, 'primary_candidates': 70, 'primary_groups': 18,
        'analysis_only_exclusions': 2, 'special_group_retained': 2,
        'disclosed_note_candidates_retained': 3}
    for key, expected in expected_counts.items():
        if counts[key] != expected: issues['count_mismatch_' + key] += 1
    if seen != WELLS: issues['coordinate_coverage'] += 1
    canonical = {g['group_id'] for g in get_canonical_groups()}
    if set(groups) != canonical or any(n != 4 for n in groups.values()):
        issues['nominal_group_structure'] += 1
    if set(primary_groups) != canonical or any(n != (2 if g == 'Exp3:PFHxA_10' else 4) for g,n in primary_groups.items()):
        issues['primary_group_structure'] += 1
    if retained_special != {'D5', 'D8'}: issues['special_group_membership'] += 1
    if not PRIMARY_EXCLUSIONS | HISTORICAL_NOTE_WELLS <= candidate_wells:
        issues['known_note_candidate_missing'] += 1
    if len(digests) != 1 or len(source_files) != 1: issues['source_consistency'] += 1
    return {'status': 'review-needed' if issues else 'consistent-pending-scientific-review',
        'counts': dict(sorted(counts.items())), 'new_inconsistencies': dict(sorted(issues.items())),
        'training_permission': False, 'chemical_verification': False}


def failure(category):
    return {'status': 'review-needed', 'counts': {}, 'new_inconsistencies': {category: 1},
            'training_permission': False, 'chemical_verification': False}


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps(failure('invalid_cli_arguments'), sort_keys=True))
        raise SystemExit(2)


def main():
    parser = SafeParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True, help='Private local metadata JSON; path never echoed')
    args = parser.parse_args()
    try:
        # Full-file bytes are only parsed/filter-selected locally; foreign rows are
        # discarded before any diagnostics. No path, hash, row or exception is output.
        before = args.manifest.read_bytes()
        result = audit_exp3(json.loads(before))
        if args.manifest.read_bytes() != before:
            result = failure('input_changed_during_audit')
    except Exception:
        result = failure('input_or_schema_error')
    print(json.dumps(result, sort_keys=True))
    return 2 if result['new_inconsistencies'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
