"""Entirely fabricated metadata; never loads a laboratory manifest."""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from scripts.audit_exp3_eligibility import audit_exp3, synthetic_logo_check


def fixture():
    classes=('TFA','PFPA','PFBA','PFHxA','PFOA','PFNA')
    rows=[]
    for ri,letter in enumerate('ABCDEFGH'):
        for col in range(1,13):
            candidate=ri<6
            condition=f'{classes[ri]}_{(5,10,20)[(col-1)//4]}' if candidate else 'synthetic_control'
            pfas,conc=(condition.split('_') if candidate else (None,None))
            comp={p:'0' for p in classes}
            if candidate: comp[pfas]=conc
            qc='review' if letter=='D' and col in (6,7) else 'include'
            rows.append(dict(experiment_id='Exp3',batch_claim='Exp3',physical_well=f'{letter}{col}',
                candidate_included=candidate,spectrum_present=True,condition_claim=condition,
                label_claim=pfas,concentration_claim_ppm=conc,component_claims_ppm=comp,
                technical_replicate_group='Exp3:'+condition,preparation_group='UNKNOWN',
                group_independence_verified=False,physical_label_verified=False,training_authorized=False,
                label_status='provisional_not_independently_verified',preparation_status='unknown',
                source_sha256='a'*64,source_file='synthetic.xlsx',source_sheet='Sheet1',
                raw_header_cell='C1',raw_value_range='C2:C177',qc_status_claim=qc,qc_reason_claim='',
                warnings=['physical_label_not_independently_verified','preparation_group_unknown','preparation_status_missing']+(['qc_review'] if qc=='review' else []),
                source_evidence=dict(experiment_id='Exp3',well=f'{letter}{col}',sha256='a'*64,
                    raw_file='synthetic.xlsx',historical_qc_status=qc,historical_qc_reason='',
                    raw_header_cell='C1',raw_value_range='C2:C177',
                    master_partition='individual_dataset' if candidate else 'qc',
                    master_use_in_model='Yes' if candidate else 'No',condition_claim=condition,
                    master_composition_ppm=json.dumps(comp),nonempty_points='176',numeric_points='176',
                    draft_reference='synthetic#record',uploaded_master_reference='synthetic#record',
                    layout_source='synthetic#cell',historical_variants='[]',findings='')))
    return rows


class EligibilityTests(unittest.TestCase):
    def test_consistent_fixture_counts_and_source_unchanged(self):
        rows=fixture(); before=copy.deepcopy(rows)
        result=audit_exp3(rows)
        self.assertEqual(result['new_inconsistencies'],{})
        self.assertEqual(result['counts']['primary_candidates'],70)
        self.assertEqual(result['counts']['primary_groups'],18)
        self.assertEqual(result['counts']['special_group_retained'],2)
        self.assertEqual(result['counts']['disclosed_note_candidates_retained'],3)
        self.assertEqual(rows,before)
        self.assertFalse(result['training_permission'])

    def test_non_exp3_filtered_before_any_diagnostic(self):
        class Foreign(dict):
            def __getitem__(self,key): raise AssertionError('foreign data examined')
        result=audit_exp3(fixture()+[Foreign(experiment_id='Exp8',secret='PRIVATE_CANARY')])
        self.assertEqual(result,audit_exp3(fixture()))
        self.assertNotIn('PRIVATE_CANARY',json.dumps(result))

    def test_count_missing_duplicate_and_claim_discrepancies_stop(self):
        for mutate in [lambda r:r.pop(),lambda r:r.append(copy.deepcopy(r[0])),
                       lambda r:r[0].update(label_claim='PFNA'),
                       lambda r:r[0].pop('source_sha256'),
                       lambda r:r[0].update(spectrum_present=False),
                       lambda r:r[0].update(training_authorized=True),
                       lambda r:r[0].update(group_independence_verified=True),
                       lambda r:r[0].update(candidate_included='true')]:
            rows=fixture(); mutate(rows)
            result=audit_exp3(rows)
            self.assertEqual(result['status'],'review-needed')
            self.assertTrue(result['new_inconsistencies'])

    def test_unknown_warning_and_contradictory_source_stop(self):
        for mutate in [lambda r:r[0]['warnings'].append('PRIVATE_CANARY'),
                       lambda r:r[0]['source_evidence'].update(condition_claim='PRIVATE_CANARY'),
                       lambda r:r[0]['component_claims_ppm'].update(TFA=''),
                       lambda r:r[0].update(preparation_status='verified')]:
            rows=fixture(); mutate(rows)
            result=audit_exp3(rows)
            self.assertEqual(result['status'],'review-needed')
            self.assertNotIn('PRIVATE_CANARY',json.dumps(result))

    def test_only_primary_exclusion_no_silent_note_exclusion(self):
        rows=fixture(); rows[0]['qc_status_claim']='exclude'
        result=audit_exp3(rows)
        self.assertEqual(result['status'],'review-needed')
        self.assertTrue(result['new_inconsistencies'])

    def test_cli_redacts_path_parse_errors_and_foreign_payload(self):
        with tempfile.TemporaryDirectory(prefix='PRIVATE_CANARY') as tmp:
            path=Path(tmp)/'PRIVATE_CANARY.json'
            env=dict(os.environ,PYTHONPATH='.',PYTHONDONTWRITEBYTECODE='1')
            for contents in ['bad PRIVATE_CANARY',json.dumps(fixture()+[{'experiment_id':'Exp8','secret':'PRIVATE_CANARY'}])]:
                path.write_text(contents)
                before=path.read_bytes()
                r=subprocess.run(['.venv/bin/python','scripts/audit_exp3_eligibility.py','--manifest',str(path)],capture_output=True,text=True,env=env)
                self.assertNotIn('PRIVATE_CANARY',r.stdout+r.stderr)
                self.assertEqual(path.read_bytes(),before)
                self.assertIn(r.returncode,(0,2))
                json.loads(r.stdout)
            r=subprocess.run(['.venv/bin/python','scripts/audit_exp3_eligibility.py','--manifest',str(path/'missing')],capture_output=True,text=True,env=env)
            self.assertEqual(r.returncode,2)
            self.assertNotIn('PRIVATE_CANARY',r.stdout+r.stderr)

    def test_synthetic_logo_eighteen_folds_group_isolation(self):
        self.assertEqual(synthetic_logo_check(),{'folds':18,'group_overlap_count':0,'validation_group_visits':18})

    def test_unexpected_candidate_conflict_review_or_broken_lineage_stops(self):
        for mutate in [lambda r:r[0]['warnings'].append('unresolved_conflict'),
                       lambda r:r[0].update(qc_status_claim='review'),
                       lambda r:r[0]['source_evidence'].update(historical_variants='PRIVATE_CANARY')]:
            rows=fixture(); mutate(rows)
            result=audit_exp3(rows)
            self.assertEqual(result['status'],'review-needed')
            self.assertNotIn('PRIVATE_CANARY',json.dumps(result))

    def test_cli_argument_errors_do_not_echo_sensitive_arguments(self):
        r=subprocess.run(['.venv/bin/python','scripts/audit_exp3_eligibility.py','--PRIVATE_CANARY'],
            capture_output=True,text=True,env=dict(os.environ,PYTHONPATH='.',PYTHONDONTWRITEBYTECODE='1'))
        self.assertEqual(r.returncode,2)
        self.assertNotIn('PRIVATE_CANARY',r.stdout+r.stderr)
        self.assertEqual(json.loads(r.stdout)['status'],'review-needed')

    def test_contradictory_inherited_candidate_claim_stops(self):
        rows=fixture()
        rows[0]['source_evidence']['historical_variants']=json.dumps([{'condition':'PFNA_20'}])
        result=audit_exp3(rows)
        self.assertEqual(result['status'],'review-needed')

    def test_coordinate_reference_and_original_candidate_role_stops(self):
        for mutate in [lambda r:r[0]['source_evidence'].update(raw_header_cell='Z1'),
                       lambda r:r[0]['source_evidence'].update(master_use_in_model='No')]:
            rows=fixture(); mutate(rows)
            result=audit_exp3(rows)
            self.assertEqual(result['status'],'review-needed')
