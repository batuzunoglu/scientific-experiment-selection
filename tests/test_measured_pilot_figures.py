"""Reporting tests: fabricated aggregates plus a read-only public-JSON audit."""
import copy
import csv
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import plot_measured_pilot_results as p

HAS_PLOTS=importlib.util.find_spec('matplotlib') is not None


def fixture():
    runs=[]
    for arm in 'ABCD':
        for policy,seed in [('random',7),('random',11),('random',19),('doe',None)]:
            points=[]
            for k in range(13):
                sensitivity=Decimal('0.1234567890123456789012345')+Decimal(k)/100
                specificity=Decimal('0.8')
                points.append(dict(acquired_conditions=k,spent_proxy_cost=k,
                    balanced_accuracy=(sensitivity+specificity)/2,sensitivity=sensitivity,specificity=specificity))
            runs.append(dict(arm=arm,representation=p.REPRESENTATIONS[arm],policy=policy,seed=seed,checkpoints=points))
    return dict(schema_version=1,data_kind=p.DATA_KIND,decimal_places=6,trajectories=runs)


class ReportTests(unittest.TestCase):
    def test_counts_precision_csv_and_summary(self):
        data=fixture();p.validate(data)
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'points.csv';p.write_plot_csv(data,dest)
            with dest.open() as stream:rows=list(csv.DictReader(stream))
            self.assertEqual(len(rows),208)
            self.assertEqual(sum(len(r['checkpoints'])*3 for r in data['trajectories']),624)
            self.assertEqual(Decimal(rows[0]['sensitivity']),data['trajectories'][0]['checkpoints'][0]['sensitivity'])
            summary=p.summary_rows(data)
            self.assertEqual(len(summary),24)
            first=summary[0]
            self.assertEqual(first['initial_sd'],Decimal(0))
            self.assertEqual(first['change'],Decimal('0.06'))
            self.assertNotIn('PRIVATE_CANARY',dest.read_text())
            self.assertNotIn(b'\r',dest.read_bytes())

    def test_strict_schema_counts_budgets_scores_and_metadata(self):
        changes=[lambda d:d['trajectories'].pop(),lambda d:d['trajectories'].append(copy.deepcopy(d['trajectories'][0])),
            lambda d:d['trajectories'][0]['checkpoints'].pop(),
            lambda d:d['trajectories'][0].update(representation='PRIVATE_CANARY'),
            lambda d:d['trajectories'][0].update(seed=99),
            lambda d:d['trajectories'][0]['checkpoints'][1].update(acquired_conditions=0),
            lambda d:d['trajectories'][0]['checkpoints'][0].update(sensitivity=Decimal('NaN')),
            lambda d:d['trajectories'][0]['checkpoints'][0].update(specificity=Decimal('1.1')),
            lambda d:d['trajectories'][0]['checkpoints'][0].update(balanced_accuracy=True),
            lambda d:d.update(private_predictions=['PRIVATE_CANARY']),
            lambda d:d['trajectories'][0]['checkpoints'][0].update(raw_spectrum=['PRIVATE_CANARY'])]
        for change in changes:
            data=fixture();change(data)
            with self.subTest(change=change),self.assertRaises(ValueError):p.validate(data)

    def test_sample_sd_and_paired_change_use_three_seeds(self):
        mean,sd=p.mean_sd((Decimal('0.1'),Decimal('0.2'),Decimal('0.3')))
        self.assertEqual(mean,Decimal('0.2'));self.assertEqual(sd,Decimal('0.1'))
        self.assertEqual(p.mean_sd((Decimal('.2'),)*3),(Decimal('.2'),Decimal(0)))

    def test_public_source_624_values_and_csv_roundtrip(self):
        source=Path('docs/results/exp3-exp5-nes-2026-11-09-aggregate.json')
        data=p.load_data(source)
        self.assertEqual(len(data['trajectories']),16)
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'data.csv';p.write_plot_csv(data,dest)
            with dest.open() as stream:rows=list(csv.DictReader(stream))
        expected={(r['arm'],r['policy'],str(r['seed']) if r['seed'] is not None else '',pt['acquired_conditions']):pt
                  for r in data['trajectories'] for pt in r['checkpoints']}
        for row in rows:
            pt=expected[(row['arm'],row['policy'],row['seed'],int(row['acquired_conditions']))]
            self.assertEqual(int(row['spent_proxy_cost']),pt['spent_proxy_cost'])
            for metric in p.METRICS:self.assertEqual(Decimal(row[metric]),pt[metric])
        self.assertEqual(len(rows)*len(p.METRICS),624)

    @unittest.skipUnless(HAS_PLOTS,'optional plotting dependencies required')
    def test_render_all_observed_points_axes_sd_and_no_interpolation(self):
        import matplotlib.pyplot as plt
        fig=p.make_figure(fixture(),'sensitivity')
        self.assertEqual(len(fig.axes),4)
        for ax in fig.axes:
            lines={line.get_label():line for line in ax.lines}
            for label in ('Random 7','Random 11','Random 19','DoE'):
                self.assertEqual(list(lines[label].get_xdata()),list(range(13)))
                self.assertEqual(lines[label].get_linestyle(),'None')
            self.assertEqual(ax.get_ylim(),(0.,1.))
            self.assertEqual(list(ax.get_xticks()),list(range(13)))
        plt.close(fig)

    @unittest.skipUnless(HAS_PLOTS,'optional plotting dependencies required')
    def test_generate_six_files_metadata_and_no_model_imports(self):
        from PIL import Image
        source=Path('docs/results/exp3-exp5-nes-2026-11-09-aggregate.json')
        before=source.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            import builtins
            original_import=builtins.__import__
            def reporting_import(name,*args,**kwargs):
                if name.startswith(('sklearn','scientific_experiment_selection')):
                    raise AssertionError('Reporting must not import training/data code')
                return original_import(name,*args,**kwargs)
            with patch('builtins.__import__',reporting_import):
                result=p.generate(source,root/'figures',root/'results')
            self.assertEqual(result['checkpoints'],208)
            self.assertEqual(len(list((root/'figures').glob('*.png'))),3)
            self.assertEqual(len(list((root/'figures').glob('*.pdf'))),3)
            for png in (root/'figures').glob('*.png'):
                with Image.open(png) as im:
                    self.assertGreaterEqual(im.width,2700)
                    self.assertAlmostEqual(im.info['dpi'][0],300,places=1)
                    self.assertNotIn('/home/',str(im.info))
            for pdf in (root/'figures').glob('*.pdf'):
                self.assertTrue(pdf.read_bytes().startswith(b'%PDF'))
                self.assertNotIn(b'/Subtype /Image',pdf.read_bytes())
                self.assertNotIn(b'/Subtype /Type3',pdf.read_bytes())
            self.assertNotIn('/home/',(root/'figures'/'manifest.json').read_text())
        self.assertEqual(source.read_bytes(),before)
