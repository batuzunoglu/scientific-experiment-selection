"""Fabricated spectra and mappings only. No real-source access in tests/CI."""
import copy
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scientific_experiment_selection import measured_pilot as p
from scientific_experiment_selection.nes_protocol import make_synthetic_scenario, ACQUISITION
from scientific_experiment_selection.selection import RandomSelector, CoverageSelector, run_selection
from test_raw_label_join import mapping, raw_metadata

ML = importlib.util.find_spec('sklearn') is not None


def fixture():
    """Use analytic public toy spectra with invented physical coordinates."""
    toy = make_synthetic_scenario()
    rows = mapping()
    raw = raw_metadata()
    groups = {('Exp3' if g.batch.endswith('exp3') else 'Exp5',g.group_id.split(':')[1]):g
              for g in toy.initial+toy.outcomes+toy.holdout}
    index = {}
    for row in rows:
        key = (row['experiment_id'],row['condition_code'])
        if key not in groups or (row['experiment_id'],row['well']) in p.EXCLUSIONS:
            continue
        i = index.get(key,0);index[key] = i+1
        raw[row['experiment_id']][row['well']]['values'] = list(groups[key].replicates[i].spectrum)
    return rows,raw


def scenario():
    return p.build_scenario(*fixture(), data_kind='synthetic-fixture')


class ContractTests(unittest.TestCase):
    def test_exact_counts_flags_and_synthetic_guards_preserved(self):
        rows,raw = fixture();before=copy.deepcopy(rows)
        s=p.build_scenario(rows,raw,data_kind='synthetic-fixture')
        self.assertEqual([sum(len(g.samples) for g in part) for part in (s.initial,s.acquisition,s.holdout)],[70,35,18])
        self.assertEqual(rows,before)
        self.assertEqual(s.data_kind,'synthetic-fixture')
        with self.assertRaises(ValueError):run_selection(s,RandomSelector(7),12,None)
        from scientific_experiment_selection.logistic import LogisticAdapter
        if ML:
            with self.assertRaises(ValueError):LogisticAdapter().fit(p.training_view(s.initial))

    def test_bad_mapping_duplicate_missing_qc_components_label_stop(self):
        changes=[lambda r:r.pop(0),lambda r:r.append(copy.deepcopy(r[0])),
                 lambda r:r[0].update(TFA_ppm='99'),lambda r:r[0].update(tfa_present='False'),
                 lambda r:r[0].update(qc_status='exclude'),lambda r:r[0].update(condition_code='PFPA_5'),
                 lambda r:r[0].update(sample_type='blank')]
        for change in changes:
            rows,raw=fixture();change(rows)
            with self.subTest(change=change),self.assertRaises(ValueError):
                p.build_scenario(rows,raw,data_kind='synthetic-fixture')

    def test_validate_constructed_scenario_and_all_transform_failures_before_fit(self):
        s=scenario()
        for changed in (replace(s,initial=s.initial[:-1]),replace(s,holdout=s.acquisition[:6]),
                        replace(s,acquisition=s.acquisition[:-1]),replace(s,data_kind='unapproved')):
            with self.assertRaises(ValueError):p.validate_scenario(changed)
        g=s.initial[0];sample=replace(g.samples[0],label=1-g.samples[0].label)
        bad=replace(s,initial=(replace(g,samples=(sample,)+g.samples[1:]),)+s.initial[1:])
        with self.assertRaises(ValueError):p.validate_scenario(bad)
        for spectrum in ((1.,)*175,(float('nan'),)*176,(0.,)*176):
            bad=replace(s,initial=(replace(g,samples=(replace(g.samples[0],spectrum=spectrum),)+g.samples[1:]),)+s.initial[1:])
            with self.assertRaises(ValueError):p.preflight(bad)
        self.assertEqual(p.preflight(s),{a:123 for a in 'BACD'})

    def test_authorization_and_cli_redaction_before_data_access(self):
        with patch.object(p,'load_sources',side_effect=AssertionError('must not load')):
            with self.assertRaises(PermissionError):p.execute(None,None,None,None,None,authorized=False)
        r=subprocess.run([sys.executable,'-m','scientific_experiment_selection.measured_pilot','--mapping','PRIVATE_CANARY'],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertNotIn('PRIVATE_CANARY',r.stdout+r.stderr)

    def test_private_output_only_no_overwrite_or_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'private';root.mkdir()
            with patch.object(p,'PRIVATE_ROOT',root):
                with self.assertRaises(ValueError):p.prepare_output(Path(tmp)/'public')
                dest=root/'new';p.prepare_output(dest)
                self.assertEqual(dest.stat().st_mode & 0o777,0o700)
                with self.assertRaises(FileExistsError):p.prepare_output(dest)
                (root/'link').symlink_to(Path(tmp),target_is_directory=True)
                with self.assertRaises(ValueError):p.prepare_output(root/'link'/'unsafe')


@unittest.skipUnless(ML,'optional pinned ML dependencies required')
class FitTests(unittest.TestCase):
    def test_weights_scaler_fresh_fit_and_exact_recipe_all_arms(self):
        import numpy as np
        from scientific_experiment_selection.nes_protocol import feature_rows
        from scientific_experiment_selection.logistic import MODEL_CONFIG
        s=scenario();view=p.training_view(s.initial)
        for arm,width in [('A',176),('B',8),('C',176),('D',8)]:
            model=p.MeasuredLogisticAdapter(arm)
            model.fit(view);old=(model.scaler_,model.classifier_)
            x=np.asarray(feature_rows(tuple(r.spectrum for g in s.initial for r in g.samples),arm))
            w=np.array([v for g in view for v in g.sample_weights])
            np.testing.assert_allclose(model.scaler_.mean_,np.average(x,axis=0,weights=w))
            np.testing.assert_allclose(model.scaler_.var_,np.average((x-model.scaler_.mean_)**2,axis=0,weights=w),rtol=1e-10,atol=1e-14)
            self.assertEqual(model.scaler_.n_features_in_,width)
            for key,value in MODEL_CONFIG.items():self.assertEqual(model.classifier_.get_params()[key],value)
            self.assertTrue(all(abs(sum(g.sample_weights)-70/18)<1e-10 for g in view))
            model.fit(view);self.assertIsNot(model.scaler_,old[0]);self.assertIsNot(model.classifier_,old[1])
            bad=(replace(view[0],sample_weights=(1.,)*len(view[0].samples)),)+view[1:]
            with self.assertRaises(ValueError):model.fit(bad)
            self.assertIsNone(model.classifier_)

    def test_paired_trajectories_retrain_budget_and_no_holdout_or_unselected_fit(self):
        s=scenario();orders=[]
        for arm in 'BACD':
            for selector in [RandomSelector(7),RandomSelector(11),RandomSelector(19),CoverageSelector()]:
                artifacts=[]
                out=p.run_trajectory(s,selector,arm,checkpoint=lambda model,record:artifacts.append((copy.deepcopy(model.fit_trace),record)))
                self.assertEqual([r['spent_proxy_cost'] for r in out['curve']],list(range(13)))
                self.assertEqual(len(artifacts),13)
                selected=[]
                for trace,record in artifacts:
                    if record['selected_condition'] is not None:selected.append('Exp5:'+record['selected_condition'])
                    self.assertEqual(set(trace[-1].group_ids),{g.group_id for g in s.initial}|set(selected))
                    self.assertEqual(trace[-1].sample_count,70+sum(len(g.samples) for g in s.acquisition if g.group_id in selected))
                orders.append([r['selected_condition'] for r in out['curve']])
                self.assertEqual(out['data_kind'],'synthetic-fixture')
        self.assertTrue(all(orders[i:i+4]==orders[:4] for i in (4,8,12)))

    def test_holdout_changes_cannot_affect_training_or_selection(self):
        s=scenario();g=s.holdout[0]
        changed=replace(s,holdout=(replace(g,samples=tuple(replace(r,spectrum=tuple(v*1000 for v in r.spectrum)) for r in g.samples)),)+s.holdout[1:])
        fits=[]
        for data in (s,changed):
            trace=[]
            p.run_trajectory(data,RandomSelector(7),'B',checkpoint=lambda model,record:trace.append((model.fit_trace[-1],model.classifier_.coef_.tolist())))
            fits.append(trace)
        self.assertEqual(fits[0],fits[1])

    def test_metric_correctness_evaluator_copy_and_invalid_predictions(self):
        s=scenario()
        class Stateful:
            def __init__(self):self.touched=False
            def predict(self,spectra):self.touched=True;return (0,)*len(spectra)
        model=Stateful();scores,pred=p.evaluate(model,s.holdout)
        self.assertFalse(model.touched)
        self.assertEqual(scores['balanced_accuracy'],.5)
        self.assertEqual(scores['sensitivity'],0.)
        self.assertEqual(scores['specificity'],1.)
        class Invalid:
            def predict(self,spectra):return (2,)*len(spectra)
        with self.assertRaises(ValueError):p.evaluate(Invalid(),s.holdout)

    def test_convergence_failure_stops_no_stale_model(self):
        import warnings
        from sklearn.exceptions import ConvergenceWarning
        model=p.MeasuredLogisticAdapter('B')
        model.fit(p.training_view(scenario().initial))
        def failed(*args,**kwargs):warnings.warn('synthetic convergence failure',ConvergenceWarning)
        with patch('sklearn.linear_model.LogisticRegression.fit',failed),self.assertRaises(RuntimeError):
            model.fit(p.training_view(scenario().initial))
        self.assertIsNone(model.classifier_)


class SourceTests(unittest.TestCase):
    def test_known_source_only_hash_guard_and_never_open_exp8(self):
        import csv,hashlib
        from test_raw_label_join import write_mapping
        from test_dataset_contract import workbook,column
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);raw=root/'raw';raw.mkdir();evidence=root/'evidence';evidence.mkdir()
            m=evidence/'CeARS_Analysis_Step4_Individual_Classification.xlsx'
            write_mapping(m,mapping());mc=evidence/'SHA256SUMS.csv'
            with mc.open('w',newline='') as f:
                w=csv.writer(f);w.writerow(['zip_relative_path','size_bytes','sha256'])
                w.writerow([m.name,m.stat().st_size,hashlib.sha256(m.read_bytes()).hexdigest()])
            def populate(cells):
                for c in range(3,99):
                    for r in range(2,178):cells[f'{column(c)}{r}']=1.
            checks=[]
            for exp in ('Exp3','Exp5'):
                path=raw/f'{exp} Plt{exp[3:]}.xlsx';workbook(path,populate)
                checks.append(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+str(path))
            forbidden=raw/'Exp8 Plt8.xlsx';forbidden.write_bytes(b'PRIVATE_CANARY_FORBIDDEN')
            rc=root/'raw_hashes.txt';rc.write_text('\n'.join(checks)+'\n')
            import builtins,os
            original_builtin_open=builtins.open;original_os_open=os.open
            def builtin_guard(path,*args,**kwargs):
                if isinstance(path,(str,Path)) and Path(path)==forbidden:raise AssertionError('Exp8 forbidden')
                return original_builtin_open(path,*args,**kwargs)
            def os_guard(path,*args,**kwargs):
                if Path(path)==forbidden:raise AssertionError('Exp8 forbidden')
                return original_os_open(path,*args,**kwargs)
            original_open=Path.open
            def guarded_open(path,*args,**kwargs):
                if path==forbidden:raise AssertionError('Exp8 must never be opened')
                return original_open(path,*args,**kwargs)
            with patch.object(Path,'open',guarded_open),patch('builtins.open',builtin_guard),patch('os.open',os_guard):
                s,hashes,audit=p.load_sources(m,raw,rc,mc)
            self.assertEqual(audit['mismatches'],{});self.assertEqual(p.preflight(s),{a:123 for a in 'BACD'})
            p.assert_unchanged(hashes)
            with self.assertRaises(ValueError):p.load_sources(evidence/'unapproved.xlsx',raw,rc,mc)
            rc.write_text('0'*64+'  Exp3 Plt3.xlsx\n'+checks[1]+'\n')
            with self.assertRaises(ValueError):p.load_sources(m,raw,rc,mc)

    @unittest.skipUnless(ML,'optional pinned ML dependencies required')
    def test_execute_private_artifacts_authorization_failure_and_16_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with patch.object(p,'PRIVATE_ROOT',root),patch.object(p,'load_sources',return_value=(scenario(),{},{})):
                out=p.execute(None,None,None,None,root/'success',authorized=True)
                self.assertEqual(out['fits'],208)
                report=json.loads((root/'success'/'summary.json').read_text())
                self.assertEqual(report['data_kind'],'synthetic-fixture')
                self.assertEqual(len(list((root/'success').glob('*.pickle'))),208)
                self.assertEqual(len(report['runs']),16)
                self.assertNotIn('balanced_accuracy',out)
            with patch.object(p,'PRIVATE_ROOT',root),patch.object(p,'load_sources',side_effect=ValueError('synthetic failure')):
                with self.assertRaises(ValueError):p.execute(None,None,None,None,root/'failed',authorized=True)
                self.assertTrue((root/'failed'/'STOP.json').exists())
                self.assertFalse((root/'failed'/'summary.json').exists())
