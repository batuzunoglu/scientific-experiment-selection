"""Synthetic group-leakage and deterministic 18-fold LOGO plan tests.

No raw data, physical spectra, or ML model fitting.
Tests fail-closed group validation, inseparability of same-solution replicates,
preservation of the PFHxA_10 group under D6/D7 primary exclusion, and
rejection of contradictory metadata, non-canonical training sets, fractional concentrations,
and readiness integrity violations.
"""
from __future__ import annotations

import copy
from typing import Any
import unittest
from scientific_experiment_selection import logo_plan as lp


def make_synthetic_exp3_wells(include_d6_d7: bool = True) -> list[dict[str, Any]]:
    """Generate synthetic well records for Exp3's 18 conditions (4 wells each = 72 wells).

    If include_d6_d7 is False, physical wells D6 and D7 (part of PFHxA_10)
    are excluded, leaving 70 provisional primary candidate wells.
    """
    rows: list[dict[str, Any]] = []
    well_assignments = [
        ('TFA', 5, ['A1', 'A2', 'A3', 'A4']),
        ('TFA', 10, ['A5', 'A6', 'A7', 'A8']),
        ('TFA', 20, ['A9', 'A10', 'A11', 'A12']),
        ('PFPA', 5, ['B1', 'B2', 'B3', 'B4']),
        ('PFPA', 10, ['B5', 'B6', 'B7', 'B8']),
        ('PFPA', 20, ['B9', 'B10', 'B11', 'B12']),
        ('PFBA', 5, ['C1', 'C2', 'C3', 'C4']),
        ('PFBA', 10, ['C5', 'C6', 'C7', 'C8']),
        ('PFBA', 20, ['C9', 'C10', 'C11', 'C12']),
        ('PFHxA', 5, ['D1', 'D2', 'D3', 'D4']),
        ('PFHxA', 10, ['D5', 'D6', 'D7', 'D8']),
        ('PFHxA', 20, ['D9', 'D10', 'D11', 'D12']),
        ('PFOA', 5, ['E1', 'E2', 'E3', 'E4']),
        ('PFOA', 10, ['E5', 'E6', 'E7', 'E8']),
        ('PFOA', 20, ['E9', 'E10', 'E11', 'E12']),
        ('PFNA', 5, ['F1', 'F2', 'F3', 'F4']),
        ('PFNA', 10, ['F5', 'F6', 'F7', 'F8']),
        ('PFNA', 20, ['F9', 'F10', 'F11', 'F12']),
    ]

    for pfas, conc, wells in well_assignments:
        condition = f"{pfas}_{conc}"
        group_id = f"Exp3:{condition}"
        for w in wells:
            if not include_d6_d7 and w in ('D6', 'D7'):
                continue
            rows.append({
                'physical_well': w,
                'experiment_id': 'Exp3',
                'condition_claim': condition,
                'pfas_claim': pfas,
                'concentration_claim_ppm': str(conc),
                'concentration_ppm': conc,
                'technical_replicate_group': group_id,
            })
    return rows


class LogoPlanTests(unittest.TestCase):
    def test_canonical_groups_count_and_content(self):
        groups = lp.get_canonical_groups()
        self.assertEqual(len(groups), 18)

        # Check PFAS coverage (exactly 6 classes, 3 concentrations each)
        pfas_counts: dict[str, int] = {}
        conc_counts: dict[int, int] = {}
        for g in groups:
            pfas = g['pfas_claim']
            conc = g['concentration_ppm']
            pfas_counts[pfas] = pfas_counts.get(pfas, 0) + 1
            conc_counts[conc] = conc_counts.get(conc, 0) + 1
            self.assertEqual(g['group_id'], f"Exp3:{pfas}_{conc}")
            self.assertEqual(g['experiment_id'], 'Exp3')

        self.assertEqual(sorted(pfas_counts.keys()), sorted(lp.EXP3_PFAS_CLASSES))
        for pfas in lp.EXP3_PFAS_CLASSES:
            self.assertEqual(pfas_counts[pfas], 3)

        self.assertEqual(sorted(conc_counts.keys()), sorted(lp.EXP3_CONCENTRATIONS))
        for conc in lp.EXP3_CONCENTRATIONS:
            self.assertEqual(conc_counts[conc], 6)

    def test_make_and_parse_group_id(self):
        gid = lp.make_group_id('TFA', 5)
        self.assertEqual(gid, 'Exp3:TFA_5')
        parsed = lp.parse_group_id(gid)
        self.assertEqual(parsed['pfas_claim'], 'TFA')
        self.assertEqual(parsed['concentration_ppm'], 5)
        self.assertEqual(parsed['condition'], 'TFA_5')

        # Invalid cases raise ValueError
        with self.assertRaises(ValueError):
            lp.make_group_id('UNKNOWN_PFAS', 5)
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', 15)  # 15 not in (5, 10, 20)
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', 5, experiment_id='Exp5')

    def test_rejects_float_or_fractional_concentration(self):
        """Item 3 review fix: do not truncate fractional or accept boolean concentrations."""
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', 5.9)
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', 5.0)  # float prohibited to prevent silent truncation
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', '5.9')
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', ' 5 ')  # whitespace string rejected
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', True)  # bool is subclass of int; must be rejected
        with self.assertRaises(ValueError):
            lp.make_group_id('TFA', 'five')

    def test_eighteen_folds_generated_deterministically(self):
        plan1 = lp.generate_logo_plan()
        plan2 = lp.generate_logo_plan()

        self.assertEqual(len(plan1), 18)
        self.assertEqual(len(plan2), 18)
        self.assertEqual(plan1, plan2)  # Strict determinism

        held_out_groups = [f['validation_group_id'] for f in plan1]
        self.assertEqual(len(held_out_groups), 18)
        self.assertEqual(len(set(held_out_groups)), 18)  # Every group held out exactly once

        canonical_ids = [g['group_id'] for g in lp.get_canonical_groups()]
        self.assertEqual(held_out_groups, canonical_ids)

    def test_zero_group_leakage_in_all_folds(self):
        plan = lp.generate_logo_plan()
        for fold in plan:
            val_id = fold['validation_group_id']
            train_ids = fold['training_group_ids']

            self.assertEqual(fold['num_validation_groups'], 1)
            self.assertEqual(fold['num_training_groups'], 17)
            self.assertEqual(len(train_ids), 17)

            # Strict zero overlap
            self.assertNotIn(val_id, train_ids)
            self.assertEqual(set(train_ids) & {val_id}, set())

            # Verification function agrees
            self.assertTrue(lp.verify_fold_leakage(fold))

    def test_fail_closed_on_malformed_duplicate_or_unexpected_groups(self):
        canonical = [g['group_id'] for g in lp.get_canonical_groups()]

        # Duplicate group
        duplicate_list = canonical[:-1] + [canonical[0]]
        with self.assertRaises(ValueError):
            lp.validate_group_ids(duplicate_list)

        # Missing group (only 17 groups)
        with self.assertRaises(ValueError):
            lp.validate_group_ids(canonical[:-1])

        # Extra group (19 groups)
        with self.assertRaises(ValueError):
            lp.validate_group_ids(canonical + ['Exp3:TFA_5'])

        # Unexpected group ID (e.g. Exp3:GenX_10)
        unexpected = canonical[:-1] + ['Exp3:GenX_10']
        with self.assertRaises(ValueError):
            lp.validate_group_ids(unexpected)

        # Malformed group string
        malformed = canonical[:-1] + ['Exp3:TFA_invalid']
        with self.assertRaises(ValueError):
            lp.validate_group_ids(malformed)

        # Wrong experiment
        wrong_exp = canonical[:-1] + ['Exp5:TFA_5']
        with self.assertRaises(ValueError):
            lp.validate_group_ids(wrong_exp)

    def test_rejects_contradictory_caller_supplied_group_metadata(self):
        """Item 1 review fix: caller-supplied contradictory metadata must be rejected."""
        groups = [dict(g) for g in lp.get_canonical_groups()]

        # Corrupt pfas_claim on first group ('Exp3:TFA_5' claim changed to 'PFNA')
        bad_groups_pfas = copy.deepcopy(groups)
        bad_groups_pfas[0]['pfas_claim'] = 'PFNA'
        with self.assertRaises(ValueError) as ctx:
            lp.generate_logo_plan(groups=bad_groups_pfas)
        self.assertIn("Contradictory metadata", str(ctx.exception))

        # Corrupt concentration_ppm on first group ('Exp3:TFA_5' concentration changed to 20)
        bad_groups_conc = copy.deepcopy(groups)
        bad_groups_conc[0]['concentration_ppm'] = 20
        with self.assertRaises(ValueError) as ctx:
            lp.generate_logo_plan(groups=bad_groups_conc)
        self.assertIn("Contradictory metadata", str(ctx.exception))

        # Float concentration_ppm on group record ('5.0' float instead of int 5)
        bad_groups_float = copy.deepcopy(groups)
        bad_groups_float[0]['concentration_ppm'] = 5.0
        with self.assertRaises(ValueError) as ctx:
            lp.generate_logo_plan(groups=bad_groups_float)
        self.assertIn("Contradictory metadata", str(ctx.exception))

    def test_rejects_altered_invalid_training_group_sets_in_verifier(self):
        """Item 2 review fix: training set must equal exact canonical complement."""
        plan = lp.generate_logo_plan()
        fold0 = copy.deepcopy(plan[0])

        # Probe 1: Replace a training group ID with a foreign experiment group
        bad_train_ids = list(fold0['training_group_ids'])
        bad_train_ids[0] = 'Exp5:PFOA_10'
        bad_fold = copy.deepcopy(fold0)
        bad_fold['training_group_ids'] = tuple(bad_train_ids)
        with self.assertRaises(ValueError) as ctx:
            lp.verify_fold_leakage(bad_fold)
        self.assertIn("Training groups do not match canonical complement", str(ctx.exception))

        # Probe 2: Omit a training group ID (16 instead of 17)
        bad_fold_short = copy.deepcopy(fold0)
        bad_fold_short['training_group_ids'] = tuple(fold0['training_group_ids'][:-1])
        with self.assertRaises(ValueError):
            lp.verify_fold_leakage(bad_fold_short)

        # Probe 3: Contradictory held_out_pfas on fold record
        bad_fold_meta = copy.deepcopy(fold0)
        bad_fold_meta['held_out_pfas'] = 'PFNA'  # fold 0 is TFA_5
        with self.assertRaises(ValueError) as ctx:
            lp.verify_fold_leakage(bad_fold_meta)
        self.assertIn("Contradictory held_out_pfas", str(ctx.exception))

        # Probe 4: Contradictory metadata in training_groups dict
        bad_fold_tg = copy.deepcopy(fold0)
        tg_list = list(bad_fold_tg['training_groups'])
        tg_list[0]['pfas_claim'] = 'WRONG_PFAS'
        bad_fold_tg['training_groups'] = tuple(tg_list)
        with self.assertRaises(ValueError) as ctx:
            lp.verify_fold_leakage(bad_fold_tg)
        self.assertIn("Contradictory metadata", str(ctx.exception))

    def test_rejects_contradictory_sample_metadata_and_fractional_concentrations(self):
        """PR #20 review Gap 1: validate every present redundant field and reject fractional concentrations."""
        plan = lp.generate_logo_plan()
        fold0 = plan[0]

        # Contradictory experiment_id
        bad_sample1 = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'experiment_id': 'Exp5',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_sample1)
        self.assertIn("contradicts", str(ctx.exception))

        # Contradictory condition_claim
        bad_sample2 = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'condition_claim': 'PFNA_20',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_sample2)
        self.assertIn("contradicts", str(ctx.exception))

        # Contradictory pfas_claim
        bad_sample3 = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'pfas_claim': 'PFBA',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_sample3)
        self.assertIn("contradicts", str(ctx.exception))

        # Contradictory concentration_claim_ppm
        bad_sample4 = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'concentration_claim_ppm': '10',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_sample4)
        self.assertIn("contradicts", str(ctx.exception))

        # Redundant condition_claim valid ('TFA_5'), but condition contradicts ('PFNA_20')
        bad_redundant_cond = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'condition_claim': 'TFA_5',
            'condition': 'PFNA_20',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_redundant_cond)
        self.assertIn("condition 'PFNA_20' contradicts", str(ctx.exception))

        # Redundant pfas_claim valid ('TFA'), but label_claim contradicts ('PFNA')
        bad_redundant_pfas = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'pfas_claim': 'TFA',
            'label_claim': 'PFNA',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_redundant_pfas)
        self.assertIn("label_claim 'PFNA' contradicts", str(ctx.exception))

        # Redundant experiment_id valid ('Exp3'), but batch_claim contradicts ('Exp5')
        bad_redundant_exp = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'experiment_id': 'Exp3',
            'batch_claim': 'Exp5',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_redundant_exp)
        self.assertIn("batch_claim 'Exp5' contradicts", str(ctx.exception))

        # Redundant physical_well ('A1') contradicts well ('A2')
        bad_redundant_well = [{
            'physical_well': 'A1',
            'well': 'A2',
            'technical_replicate_group': 'Exp3:TFA_5',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_redundant_well)
        self.assertIn("physical_well 'A1' contradicts well 'A2'", str(ctx.exception))

        # Fractional concentration_ppm (5.9 must not truncate to 5)
        bad_frac_conc = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'concentration_ppm': 5.9,
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_frac_conc)
        self.assertIn("Float/fractional concentration_ppm not permitted", str(ctx.exception))

        # Float concentration_ppm (5.0 rejected)
        bad_float_conc = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'concentration_ppm': 5.0,
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_float_conc)
        self.assertIn("Float/fractional concentration_ppm not permitted", str(ctx.exception))

        # Fractional concentration_claim_ppm string ('5.9')
        bad_frac_claim = [{
            'physical_well': 'A1',
            'technical_replicate_group': 'Exp3:TFA_5',
            'concentration_claim_ppm': '5.9',
        }]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, bad_frac_claim)
        self.assertIn("Invalid integer concentration_claim_ppm string", str(ctx.exception))

    def test_synthetic_well_partition_and_technical_replicate_inseparability(self):
        """All technical replicate wells of the same prepared solution must stay strictly together."""
        synthetic_wells = make_synthetic_exp3_wells(include_d6_d7=True)
        self.assertEqual(len(synthetic_wells), 72)

        plan = lp.generate_logo_plan()

        for fold in plan:
            split = lp.split_samples_by_fold(fold, synthetic_wells)
            train_wells = split['training']
            val_wells = split['validation']

            self.assertEqual(len(val_wells), 4)
            self.assertEqual(len(train_wells), 68)
            self.assertEqual(len(val_wells) + len(train_wells), 72)

            val_gids = {w['technical_replicate_group'] for w in val_wells}
            train_gids = {w['technical_replicate_group'] for w in train_wells}

            # Exactly the single held-out group in validation
            self.assertEqual(val_gids, {fold['validation_group_id']})
            # Held-out group is completely absent from training
            self.assertNotIn(fold['validation_group_id'], train_gids)
            # Training and validation group sets are disjoint
            self.assertEqual(val_gids & train_gids, set())

            # No physical well coordinate is shared
            val_coords = {w['physical_well'] for w in val_wells}
            train_coords = {w['physical_well'] for w in train_wells}
            self.assertEqual(val_coords & train_coords, set())

            # Verify inseparability: for EVERY condition group, its wells are either 100% in val or 100% in train
            by_group: dict[str, list[dict[str, Any]]] = {}
            for w in synthetic_wells:
                by_group.setdefault(w['technical_replicate_group'], []).append(w)

            for gid, grp_wells in by_group.items():
                in_val = [w for w in grp_wells if w in val_wells]
                in_train = [w for w in grp_wells if w in train_wells]
                if gid == fold['validation_group_id']:
                    self.assertEqual(len(in_val), len(grp_wells))
                    self.assertEqual(len(in_train), 0)
                else:
                    self.assertEqual(len(in_val), 0)
                    self.assertEqual(len(in_train), len(grp_wells))

    def test_synthetic_d6_d7_primary_exclusion_preserves_pfhxa_10_group(self):
        """D-016 excludes Exp3 D6/D7: PFHxA_10 retains 2 wells; group is not dropped."""
        synthetic_wells_70 = make_synthetic_exp3_wells(include_d6_d7=False)
        self.assertEqual(len(synthetic_wells_70), 70)

        # Check well counts by group in primary pool
        counts: dict[str, int] = {}
        for w in synthetic_wells_70:
            gid = w['technical_replicate_group']
            counts[gid] = counts.get(gid, 0) + 1

        self.assertEqual(counts['Exp3:PFHxA_10'], 2)  # D5 and D8 remain
        for gid, count in counts.items():
            if gid == 'Exp3:PFHxA_10':
                self.assertEqual(count, 2)
            else:
                self.assertEqual(count, 4)

        plan = lp.generate_logo_plan()

        for fold in plan:
            split = lp.split_samples_by_fold(fold, synthetic_wells_70)
            train_wells = split['training']
            val_wells = split['validation']

            if fold['validation_group_id'] == 'Exp3:PFHxA_10':
                # Held-out fold for PFHxA_10 has 2 wells (not dropped!)
                self.assertEqual(len(val_wells), 2)
                self.assertEqual(len(train_wells), 68)  # 17 groups * 4 wells
                self.assertEqual(
                    {w['physical_well'] for w in val_wells},
                    {'D5', 'D8'}
                )
            else:
                # All other 17 folds have 4 wells in validation
                self.assertEqual(len(val_wells), 4)
                # Training has 66 wells: 16 groups * 4 = 64, plus PFHxA_10 * 2 = 66
                self.assertEqual(len(train_wells), 66)

            self.assertEqual(len(val_wells) + len(train_wells), 70)
            # Replicate inseparability still holds
            self.assertNotIn(fold['validation_group_id'], {w['technical_replicate_group'] for w in train_wells})

    def test_empty_validation_partition_and_readiness_validation(self):
        """Item 3 & PR #20 Gap 2 fix: condition-group coverage & evaluation readiness integrity."""
        synthetic_wells_70 = make_synthetic_exp3_wells(include_d6_d7=False)
        plan = lp.generate_logo_plan()
        fold0 = plan[0]  # Exp3:TFA_5

        # 1. Complete dataset passes readiness validation
        split_full = lp.split_samples_by_fold(fold0, synthetic_wells_70)
        self.assertTrue(lp.validate_fold_evaluation_readiness(split_full, fold0))

        # 2. Dataset missing held-out group (only non-TFA_5 wells)
        subset_no_val = [w for w in synthetic_wells_70 if w['technical_replicate_group'] != 'Exp3:TFA_5']

        # By default, split_samples_by_fold allows empty validation (arbitrary subset partitioning)
        split_no_val = lp.split_samples_by_fold(fold0, subset_no_val, allow_empty_validation=True)
        self.assertEqual(len(split_no_val['validation']), 0)

        # When allow_empty_validation=False, it raises ValueError
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, subset_no_val, allow_empty_validation=False)
        self.assertIn("validation partition is empty", str(ctx.exception))

        # validate_fold_evaluation_readiness catches empty validation
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(split_no_val, fold0)
        self.assertIn("expected at least 1", str(ctx.exception))

        # 3. Dataset missing one training group (Exp3:PFNA_20 missing)
        subset_missing_train = [w for w in synthetic_wells_70 if w['technical_replicate_group'] != 'Exp3:PFNA_20']
        split_missing_train = lp.split_samples_by_fold(fold0, subset_missing_train)
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(split_missing_train, fold0)
        self.assertIn("Training set incomplete: missing samples for 1 expected group(s)", str(ctx.exception))

    def test_readiness_rejects_corrupted_fold_samples_and_duplicate_wells(self):
        """PR #20 review Gap 2: readiness verifies fold integrity, sample claims, well uniqueness, and expected_training_groups."""
        synthetic_wells_70 = make_synthetic_exp3_wells(include_d6_d7=False)
        plan = lp.generate_logo_plan()
        fold0 = copy.deepcopy(plan[0])
        split_full = lp.split_samples_by_fold(fold0, synthetic_wells_70)

        # 1. Corrupted fold_record passed to validate_fold_evaluation_readiness
        bad_fold = copy.deepcopy(fold0)
        bad_fold['held_out_pfas'] = 'PFNA'
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(split_full, bad_fold)
        self.assertIn("Contradictory held_out_pfas", str(ctx.exception))

        # 2. Corrupted sample metadata inside split_result['validation']
        bad_split_meta = copy.deepcopy(split_full)
        bad_split_meta['validation'][0]['condition'] = 'PFNA_20'
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(bad_split_meta, fold0)
        self.assertIn("contradicts", str(ctx.exception))

        # 3. Duplicate physical well ID within validation
        bad_split_dup_val = copy.deepcopy(split_full)
        bad_split_dup_val['validation'][1]['physical_well'] = bad_split_dup_val['validation'][0]['physical_well']
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(bad_split_dup_val, fold0)
        self.assertIn("Duplicate physical well ID in validation set", str(ctx.exception))

        # 4. Duplicate physical well ID within training
        bad_split_dup_train = copy.deepcopy(split_full)
        bad_split_dup_train['training'][1]['physical_well'] = bad_split_dup_train['training'][0]['physical_well']
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(bad_split_dup_train, fold0)
        self.assertIn("Duplicate physical well ID in training set", str(ctx.exception))

        # 5. Overlapping physical well ID between validation and training (even across 'physical_well' and 'well')
        bad_split_overlap = copy.deepcopy(split_full)
        del bad_split_overlap['training'][0]['physical_well']
        bad_split_overlap['training'][0]['well'] = bad_split_overlap['validation'][0]['physical_well']
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(bad_split_overlap, fold0)
        self.assertIn("Overlapping physical well ID between validation and training", str(ctx.exception))

        # 6. Mixed presence/absence of physical well IDs across samples
        bad_split_mixed_wells = copy.deepcopy(split_full)
        del bad_split_mixed_wells['training'][0]['physical_well']
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(bad_split_mixed_wells, fold0)
        self.assertIn("Inconsistent physical well metadata", str(ctx.exception))

        # 7. Invalid expected_training_groups argument
        with self.assertRaises(ValueError) as ctx:
            lp.validate_fold_evaluation_readiness(split_full, fold0, expected_training_groups=16)
        self.assertIn("expected_training_groups must equal 17", str(ctx.exception))
        with self.assertRaises(ValueError):
            lp.validate_fold_evaluation_readiness(split_full, fold0, expected_training_groups=True)

    def test_split_samples_fail_closed_on_bad_inputs(self):
        plan = lp.generate_logo_plan()
        fold0 = plan[0]

        # Missing technical_replicate_group
        bad_sample1 = [{'physical_well': 'A1'}]
        with self.assertRaises(ValueError):
            lp.split_samples_by_fold(fold0, bad_sample1)

        # Malformed group ID
        bad_sample2 = [{'physical_well': 'A1', 'technical_replicate_group': 'Exp3:BadCondition'}]
        with self.assertRaises(ValueError):
            lp.split_samples_by_fold(fold0, bad_sample2)

        # Unexpected group from another experiment
        bad_sample3 = [{'physical_well': 'A1', 'technical_replicate_group': 'Exp5:TFA_5'}]
        with self.assertRaises(ValueError):
            lp.split_samples_by_fold(fold0, bad_sample3)

        # Duplicate physical well ID in samples passed to split_samples_by_fold
        dup_well_samples = [
            {'physical_well': 'A1', 'technical_replicate_group': 'Exp3:TFA_5'},
            {'physical_well': 'A1', 'technical_replicate_group': 'Exp3:TFA_5'},
        ]
        with self.assertRaises(ValueError) as ctx:
            lp.split_samples_by_fold(fold0, dup_well_samples)
        self.assertIn("Duplicate physical well ID", str(ctx.exception))

        # Non-dict sample
        with self.assertRaises(ValueError):
            lp.split_samples_by_fold(fold0, ['not_a_dict'])  # type: ignore[arg-type]


if __name__ == '__main__':
    unittest.main()
