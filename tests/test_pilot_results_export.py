"""Exporter tests use fabricated aggregate numbers and privacy canaries only."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from scientific_experiment_selection import pilot_results_export as e


def fixture():
    lines=['PRIVATE_CANARY_SOURCE_PATH\n']
    runs=[]
    for arm in 'BACD':
        for policy,seed in [('random',7),('random',11),('random',19),('coverage',None)]:
            lines.extend([f'### {arm} / {policy} / seed {seed}',
                '| Acquired conditions / proxy cost | BA | TFA sensitivity | non-TFA specificity |',
                '| ---: | ---: | ---: | ---: |'])
            curve=[]
            for k in range(13):
                sensitivity=.2+.05*k;specificity=.8-.025*k;ba=(sensitivity+specificity)/2
                lines.append(f'| {k} | {ba:.6f} | {sensitivity:.6f} | {specificity:.6f} |')
                curve.append(dict(acquired_conditions=k,spent_proxy_cost=k,balanced_accuracy=ba,
                    sensitivity=sensitivity,specificity=specificity,evaluation_predictions=['PRIVATE_CANARY'],
                    selected_condition='PRIVATE_CANARY'))
            lines.append('')
            runs.append(dict(arm=arm,policy=policy,seed=seed,curve=curve,fit_trace=['PRIVATE_CANARY']))
    lines.append('## Reproduction and limits\nPRIVATE_CANARY')
    return '\n'.join(lines),dict(status='completed-pending-scientific-review',
        data_kind='measured-retrospective',source_bytes_unchanged=True,runs=runs,private='PRIVATE_CANARY')


class ExportTests(unittest.TestCase):
    def test_complete_allowlisted_deterministic_roundtrip(self):
        report,summary=fixture();old=copy.deepcopy(summary)
        result=e.sanitize(report,summary)
        self.assertEqual(summary,old)
        self.assertEqual(len(result['trajectories']),16)
        self.assertEqual(sum(len(r['checkpoints']) for r in result['trajectories']),208)
        for run in result['trajectories']:
            self.assertEqual(set(run),{'arm','representation','policy','seed','checkpoints'})
            for point in run['checkpoints']:
                self.assertEqual(set(point),set(e.POINT_FIELDS))
        md=e.render_markdown(result);data=e.render_json(result)
        self.assertEqual(data,e.render_json(e.sanitize(report,summary)))
        self.assertEqual(json.loads(data),result)
        self.assertNotIn('PRIVATE_CANARY',md+data)
        self.assertNotIn('/home/',md+data)
        self.assertEqual(md.count('### '),16)
        self.assertIn('retrospective measured Exp3→Exp5 model results',md)

    def test_missing_duplicate_unknown_trajectories_and_checkpoints_fail(self):
        for mutate in (lambda s:s['runs'].pop(),lambda s:s['runs'].append(copy.deepcopy(s['runs'][0])),
                       lambda s:s['runs'][0]['curve'].pop(),
                       lambda s:s['runs'][0].update(arm='PRIVATE_CANARY'),
                       lambda s:s['runs'][0].update(seed=99),
                       lambda s:s['runs'][0]['curve'][1].update(acquired_conditions=0),
                       lambda s:s['runs'][0]['curve'][1].update(spent_proxy_cost=2)):
            report,summary=fixture();mutate(summary)
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):e.sanitize(report,summary)
        report,summary=fixture()
        for bad in (report.replace('### B / random / seed 7','### X / random / seed 7'),
                    report.replace('| 0 | 0.500000 | 0.200000 | 0.800000 |','',1),
                    report+ '\n### B / random / seed 7\n'):
            with self.assertRaises(ValueError):e.sanitize(bad,summary)

    def test_score_mismatch_bounds_nan_boolean_and_metric_identity_fail(self):
        for value in (-.1,1.1,float('nan'),float('inf'),True,'0.5'):
            report,summary=fixture();summary['runs'][0]['curve'][1]['balanced_accuracy']=value
            with self.subTest(value=value),self.assertRaises(ValueError):e.sanitize(report,summary)
        report,summary=fixture()
        summary['runs'][0]['curve'][1]['balanced_accuracy']=.123
        with self.assertRaises(ValueError):e.sanitize(report,summary)
        # Two sources agreeing on bad arithmetic still must fail.
        report,summary=fixture();summary['runs'][0]['curve'][0]['balanced_accuracy']=.4
        report=report.replace('| 0 | 0.500000 | 0.200000 | 0.800000 |','| 0 | 0.400000 | 0.200000 | 0.800000 |',1)
        with self.assertRaises(ValueError):e.sanitize(report,summary)

    def test_baseline_final_inconsistency_and_unfinished_run_fail(self):
        for k in (0,12):
            report,summary=fixture();point=summary['runs'][0]['curve'][k]
            old=f"| {k} | {point['balanced_accuracy']:.6f} | {point['sensitivity']:.6f} | {point['specificity']:.6f} |"
            point['specificity']-=.1;point['balanced_accuracy']-=.05
            new=f"| {k} | {point['balanced_accuracy']:.6f} | {point['sensitivity']:.6f} | {point['specificity']:.6f} |"
            report=report.replace(old,new,1)
            with self.assertRaises(ValueError):e.sanitize(report,summary)
        for field,value in [('status','failed'),('data_kind','synthetic-only'),('source_bytes_unchanged',False)]:
            report,summary=fixture();summary[field]=value
            with self.assertRaises(ValueError):e.sanitize(report,summary)

    def test_export_check_read_only_sources_and_tamper_detection(self):
        report,summary=fixture()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);private=root/'private';private.mkdir();public=root/'public';public.mkdir()
            review=private/'REVIEW.md';original=private/'summary.json'
            review.write_text(report);original.write_text(json.dumps(summary));before={p:p.read_bytes() for p in (review,original)}
            md=public/'results.md';js=public/'aggregate.json'
            e.export(review,original,md,js)
            e.export(review,original,md,js,check=True)
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            md.write_text(md.read_text()+'tampered')
            with self.assertRaises(ValueError):e.export(review,original,md,js,check=True)
            with self.assertRaises(ValueError):e.export(review,original,review,js)
            self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_hardlink_output_cannot_modify_private_original(self):
        import os
        report,summary=fixture()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);review=root/'REVIEW.md';original=root/'summary.json'
            review.write_text(report);original.write_text(json.dumps(summary))
            alias=root/'public.md';os.link(review,alias)
            before=review.read_bytes()
            with self.assertRaises(ValueError):e.export(review,original,alias,root/'aggregate.json')
            self.assertEqual(review.read_bytes(),before)
