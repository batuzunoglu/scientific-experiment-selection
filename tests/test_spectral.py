import copy
import math
import unittest
from scientific_experiment_selection import spectral as s


class SpectralTests(unittest.TestCase):
    def test_raw_roundtrip_and_provenance(self):
        y = [1 + i / 1000 for i in range(176)]
        source = {'sha256': 'synthetic', 'cell_range': 'C2:C177', 'nested': ['original']}
        before = copy.deepcopy(source)
        out = s.representations(s.GRID, y, source)
        self.assertEqual(out['A']['values'], y)
        self.assertEqual([len(out[k]['values']) for k in 'ABCD'], [176, 8, 176, 8])
        self.assertEqual(out['provenance'], source)
        out['provenance']['nested'].append('changed output')
        self.assertEqual(source, before)
        self.assertEqual(y, [1 + i / 1000 for i in range(176)])

    def test_area_window_and_full_division(self):
        y = [2.0 if 380 <= x <= 580 else 9.0 for x in s.GRID]
        self.assertEqual(s.area_factor(s.GRID, y), 400)
        result = s.representations(s.GRID, y, {})
        self.assertAlmostEqual(result['C']['values'][0], 9 / 400)
        self.assertAlmostEqual(s.area_factor(s.GRID, result['C']['values']), 1)

    def test_positive_scale_invariance(self):
        y = [1 + (x - 350) / 500 for x in s.GRID]
        a = s.representations(s.GRID, y, {})
        b = s.representations(s.GRID, [7*v for v in y], {})
        for branch in 'CD':
            for v,w in zip(a[branch]['values'], b[branch]['values']):
                self.assertAlmostEqual(v,w, places=10)
        self.assertNotEqual(a['A']['values'],b['A']['values'])

    def test_constant_compact_moments(self):
        f = s.compact8(s.GRID, [2.0]*176)
        self.assertEqual(f[:3], [2, 2, 1])
        self.assertAlmostEqual(f[3],480)
        self.assertAlmostEqual(f[4],math.sqrt(3400))  # discrete 101-point variance
        for v in f[5:]: self.assertAlmostEqual(v,0,places=12)

    def test_sg_linear_quadratic_and_boundary_convention(self):
        y = [3 + .02*(x-480) + .0001*(x-480)**2 for x in s.GRID]
        d = s.sg_derivative(s.GRID,y)
        for x,v in zip(s.GRID,d):
            self.assertAlmostEqual(v,.02+.0002*(x-480),places=12)
        f = s.compact8(s.GRID,[1+.01*(x-350) for x in s.GRID])
        self.assertAlmostEqual(f[5],2,places=11)
        self.assertAlmostEqual(f[6],.01,places=12)
        self.assertAlmostEqual(f[7],.01,places=12)

    def test_area_guards_leave_raw_available(self):
        for y in [[0.0]*176,[-1.0]*176,[1e-20]*176]:
            out=s.representations(s.GRID,y,{})
            self.assertEqual(out['A']['values'],y)
            self.assertIsNone(out['C']['values'])
            self.assertIsNotNone(out['C']['error'])
        with self.assertRaises(ValueError):
            s.compact8(s.GRID,[0.0]*176)

    def test_ratio_and_negative_weight_guards(self):
        y=[1.0]*176
        y[84]=0  # 518 nm
        out=s.representations(s.GRID,y,{})
        self.assertIsNone(out['B']['values'])
        self.assertIsNotNone(out['C']['values'])
        y=[1.0]*176; y[20]=-0.01
        with self.assertRaisesRegex(ValueError,'negative'):
            s.compact8(s.GRID,y)

    def test_invalid_input(self):
        for y in [[1.0]*175,[float('nan')]*176,[float('inf')]*176]:
            with self.assertRaises(ValueError): s.representations(s.GRID,y,{})
        with self.assertRaises(ValueError): s.representations(list(reversed(s.GRID)),[1]*176,{})
        with self.assertRaises(ValueError): s.area_factor(s.GRID,[1]*176,epsilon=-1)

    def test_exact_fifteen_sample_derivative_stencil(self):
        y=[0.0]*176; y[57]=1
        self.assertAlmostEqual(s.sg_derivative(s.GRID,y)[50],14/1120,places=14)
        y=[0.0]*176; y[58]=1
        self.assertEqual(s.sg_derivative(s.GRID,y)[50],0)
