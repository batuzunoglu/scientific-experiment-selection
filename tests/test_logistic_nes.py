"""Synthetic-only protocol/ML checks. Optional dependency tests skip in stdlib CI."""
from dataclasses import replace
import copy
import importlib.util
import math
import unittest
from scientific_experiment_selection import spectral
from scientific_experiment_selection.selection import (
    Replicate, OutcomeGroup, TrainingGroup, CoverageSelector, RandomSelector, run_selection,
)
from scientific_experiment_selection.nes_protocol import (
    HOLDOUT, ACQUISITION, make_synthetic_scenario, validate_nes_scenario,
    condition_binary_metrics, feature_rows,
)
from scientific_experiment_selection.logistic import LogisticAdapter

HAS_ML=importlib.util.find_spec('sklearn') is not None


class ProtocolTests(unittest.TestCase):
    def test_exact_approved_split_concentrations_and_unequal_replicates(self):
        s=make_synthetic_scenario();validate_nes_scenario(s)
        self.assertEqual(len(s.initial),18)
        self.assertEqual(sum(len(g.replicates) for g in s.initial),70)
        self.assertEqual(len(s.outcomes),12);self.assertEqual(len(s.holdout),6)
        self.assertEqual(sum(len(g.replicates) for g in s.outcomes),35)
        self.assertEqual(sum(len(g.replicates) for g in s.holdout),18)
        self.assertEqual(set(HOLDOUT),{'PFPA_5','PFOA_5','TFA_10','PFHxA_10','PFBA_20','PFNA_20'})
        for conditions in (HOLDOUT,ACQUISITION):
            self.assertEqual({c.split('_')[1] for c in conditions},{'5','10','20'})
        self.assertEqual(sum(g.replicates[0].label for g in s.holdout),1)
        self.assertFalse(set(g.group_id for g in s.outcomes)&set(g.group_id for g in s.holdout))

    def test_wrong_split_or_nominal_metadata_or_labels_rejected(self):
        s=make_synthetic_scenario()
        for bad in [lambda:replace(s,outcomes=s.outcomes+s.holdout[:1]),
                    lambda:replace(s,designs=(replace(s.designs[0],settings=(('analyte','wrong'),)),)+s.designs[1:]),
                    lambda:replace(s,initial=s.initial[:-1])]:
            with self.assertRaises(ValueError):validate_nes_scenario(bad())
        g=s.outcomes[0]
        altered=replace(g,replicates=tuple(replace(r,label=1-r.label) for r in g.replicates))
        with self.assertRaises(ValueError):validate_nes_scenario(replace(s,outcomes=(altered,)+s.outcomes[1:]))

    def test_metrics_exact_group_then_class_average_not_well_accuracy(self):
        def g(gid,label,n):return OutcomeGroup(gid,'synthetic-eval',tuple(Replicate((1.,),label) for _ in range(n)))
        groups=(g('p',1,2),g('n1',0,1),g('n2',0,9))
        scores=condition_binary_metrics(groups,((1,0),(0,),(1,)*9))
        self.assertEqual(scores['sensitivity'],.5)
        self.assertEqual(scores['specificity'],.5)
        self.assertEqual(scores['balanced_accuracy'],.5)
        self.assertEqual(scores['positive_conditions'],1)
        self.assertEqual(scores['negative_conditions'],2)

    def test_invalid_predictions_and_missing_class_report_error(self):
        s=make_synthetic_scenario()
        for predictions in [(),((2,)*3,)*6,((0,),)*6,((True,)*3,)*6]:
            with self.assertRaises(ValueError):condition_binary_metrics(s.holdout,predictions)
        with self.assertRaises(ValueError):condition_binary_metrics((s.holdout[0],),((0,)*3,))

    def test_all_four_representations_match_existing_math_no_extra_offset(self):
        y=make_synthetic_scenario().initial[0].replicates[0].spectrum
        original=copy.deepcopy(y)
        existing=spectral.representations(spectral.GRID,y,{})
        for arm,width in [('A',176),('B',8),('C',176),('D',8)]:
            row=feature_rows((y,),arm)[0]
            self.assertEqual(len(row),width)
            self.assertEqual(list(row),existing[arm]['values'])
        self.assertEqual(y,original)
        self.assertEqual(feature_rows((y,),'A')[0],y)
        self.assertEqual(feature_rows((y,),'B')[0][0],y[35])
        with self.assertRaises(ValueError):feature_rows((y[:-1],),'B')
        with self.assertRaises(ValueError):feature_rows(((0.,)*176,),'B')
        with self.assertRaises(ValueError):feature_rows((y,),'offset')


@unittest.skipUnless(HAS_ML,'install optional requirements/logistic.txt')
class LogisticTests(unittest.TestCase):
    def training(self,groups):
        n=sum(len(g.replicates) for g in groups)
        return tuple(TrainingGroup(g.group_id,g.batch,g.replicates,(n/(len(groups)*len(g.replicates)),)*len(g.replicates)) for g in groups)

    def test_fixed_model_recipe_and_no_class_balancing(self):
        m=LogisticAdapter();m.fit(self.training(make_synthetic_scenario().initial))
        p=m.classifier_.get_params()
        for key,value in {'penalty':'l2','C':1.,'class_weight':None,'solver':'lbfgs','max_iter':5000,'random_state':0}.items():
            self.assertEqual(p[key],value)
        self.assertEqual(m.arm,'B')
        self.assertEqual(m.classifier_.n_features_in_,8)
        self.assertTrue(m.fit_trace[-1].converged)

    def test_exact_group_weighting_and_scaler_weighted_training_mean(self):
        import numpy as np
        s=make_synthetic_scenario();train=self.training(s.initial)
        m=LogisticAdapter();m.fit(train)
        x=np.array(feature_rows(tuple(r.spectrum for g in train for r in g.replicates),'B'))
        w=np.array([v for g in train for v in g.sample_weights])
        np.testing.assert_allclose(m.scaler_.mean_,np.average(x,axis=0,weights=w),rtol=1e-13)
        expected_mean=np.average(x,axis=0,weights=w)
        np.testing.assert_allclose(m.scaler_.var_,np.average((x-expected_mean)**2,axis=0,weights=w),rtol=1e-12,atol=1e-15)
        self.assertFalse(np.allclose(m.scaler_.mean_,np.mean(x,axis=0)))
        totals=[sum(g.sample_weights) for g in train]
        self.assertTrue(all(math.isclose(v,70/18) for v in totals))
        self.assertAlmostEqual(sum(w),70)
        pos=sum(sum(g.sample_weights) for g in train if g.replicates[0].label==1)
        self.assertAlmostEqual(pos,sum(w)/6)
        bad=(replace(train[0],sample_weights=(99.,)*len(train[0].replicates)),)+train[1:]
        with self.assertRaises(ValueError):LogisticAdapter().fit(bad)

    def test_estimator_receives_same_weights_as_scaler(self):
        from unittest.mock import patch
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        seen={};sf=StandardScaler.fit;lf=LogisticRegression.fit
        def scaler_fit(obj,x,y=None,sample_weight=None):
            seen['scaler']=sample_weight.copy();return sf(obj,x,y,sample_weight=sample_weight)
        def model_fit(obj,x,y,sample_weight=None):
            seen['model']=sample_weight.copy();return lf(obj,x,y,sample_weight=sample_weight)
        with patch.object(StandardScaler,'fit',scaler_fit),patch.object(LogisticRegression,'fit',model_fit):
            LogisticAdapter().fit(self.training(make_synthetic_scenario().initial))
        np.testing.assert_array_equal(seen['model'],seen['scaler'])

    def test_refit_every_step_only_initial_plus_selected_groups(self):
        s=make_synthetic_scenario();m=LogisticAdapter()
        result=run_selection(s,RandomSelector(7),3,m,evaluation='condition_balanced')
        self.assertEqual(len(m.fit_trace),4)
        acquired=[]
        for i,t in enumerate(m.fit_trace):
            self.assertEqual(set(t.group_ids),{g.group_id for g in s.initial}|set(acquired))
            self.assertEqual(t.feature_width,8)
            self.assertEqual(t.fit_number,i+1)
            self.assertFalse(set(t.group_ids)&{g.group_id for g in s.holdout})
            if i<3:acquired.append(result.actions[i].group_id)
        self.assertEqual([p.spent for p in result.curve],[0,1,2,3])
        self.assertTrue(all(p.balanced_accuracy is not None and p.sensitivity is not None and p.specificity is not None for p in result.curve))

    def test_unselected_and_holdout_extremes_do_not_affect_scaler(self):
        import numpy as np
        s=make_synthetic_scenario()
        m=LogisticAdapter();run_selection(s,CoverageSelector(),0,m,evaluation='condition_balanced')
        def extreme(g):return replace(g,replicates=tuple(replace(r,spectrum=tuple(1e8+v for v in r.spectrum)) for r in g.replicates))
        altered=replace(s,outcomes=tuple(extreme(g) for g in s.outcomes),holdout=tuple(extreme(g) for g in s.holdout))
        other=LogisticAdapter();run_selection(altered,CoverageSelector(),0,other,evaluation='condition_balanced')
        np.testing.assert_array_equal(m.scaler_.mean_,other.scaler_.mean_)
        np.testing.assert_array_equal(m.classifier_.coef_,other.classifier_.coef_)

    def test_fresh_scaler_model_and_all_arms_supported(self):
        train=self.training(make_synthetic_scenario().initial)
        for arm,width in [('A',176),('B',8),('C',176),('D',8)]:
            m=LogisticAdapter(arm);m.fit(train);old=(m.scaler_,m.classifier_)
            m.fit(train)
            self.assertIsNot(m.scaler_,old[0]);self.assertIsNot(m.classifier_,old[1])
            self.assertEqual(m.classifier_.n_features_in_,width)
        with self.assertRaises(ValueError):LogisticAdapter().fit(train[:1])

    def test_hidden_outcomes_scores_do_not_change_random_or_doe_actions(self):
        s=make_synthetic_scenario()
        def flip(g):return replace(g,replicates=tuple(replace(r,label=1-r.label) for r in g.replicates))
        altered=replace(s,outcomes=tuple(flip(g) for g in s.outcomes),holdout=tuple(flip(g) for g in s.holdout))
        for factory in (lambda:RandomSelector(7),CoverageSelector):
            a=run_selection(s,factory(),3,LogisticAdapter(),evaluation='condition_balanced')
            b=run_selection(altered,factory(),3,LogisticAdapter(),evaluation='condition_balanced')
            self.assertEqual(a.actions,b.actions)

    def test_convergence_failure_raises_without_changing_recipe(self):
        from unittest.mock import patch
        import warnings
        from sklearn.exceptions import ConvergenceWarning
        from sklearn.linear_model import LogisticRegression
        def failed(*args,**kwargs):warnings.warn('synthetic convergence failure',ConvergenceWarning)
        with patch.object(LogisticRegression,'fit',failed):
            with self.assertRaises(RuntimeError):LogisticAdapter().fit(self.training(make_synthetic_scenario().initial))


class StdlibIsolationTests(unittest.TestCase):
    def test_standard_library_demo_remains_independent_of_ml_dependencies(self):
        import builtins
        from unittest.mock import patch
        original=builtins.__import__
        def without_ml(name,*args,**kwargs):
            if name.split('.')[0] in ('numpy','scipy','sklearn','joblib','threadpoolctl'):
                raise AssertionError('optional ML dependency imported by stdlib demo')
            return original(name,*args,**kwargs)
        from scientific_experiment_selection.selection_demo import make_scenario
        with patch('builtins.__import__',without_ml):
            self.assertTrue(run_selection(make_scenario(),CoverageSelector(),1,
                __import__('scientific_experiment_selection.selection',fromlist=['SyntheticMeanModel']).SyntheticMeanModel()).curve)


@unittest.skipUnless(HAS_ML,'install optional requirements/logistic.txt')
class DemonstrationTests(unittest.TestCase):
    def test_paired_budgets_refit_counts_determinism_and_no_seed_selection(self):
        from scientific_experiment_selection.logistic_demo import demonstrate
        a=demonstrate(budget=2,seeds=(7,11))
        b=demonstrate(budget=2,seeds=(7,11))
        self.assertEqual(a,b)
        self.assertEqual(set(a['runs']),{'random-7','random-11','coverage'})
        for result in a['runs'].values():
            self.assertEqual([p['spent'] for p in result['trajectory']['curve']],[0,1,2])
            self.assertEqual(len(result['refits']),3)
            for trace in result['refits']:
                self.assertTrue(all(math.isclose(t,trace['sample_count']/len(trace['group_ids'])) for t in trace['group_total_weights']))
        zero=demonstrate(budget=0,seeds=(7,))
        self.assertTrue(all(len(r['refits'])==1 for r in zero['runs'].values()))
        for seeds in [(7,7),(),(True,)]:
            with self.assertRaises(ValueError):demonstrate(budget=1,seeds=seeds)

    def test_failed_transform_invalidates_old_fit_instead_of_dropping_well(self):
        train=LogisticTests().training(make_synthetic_scenario().initial)
        m=LogisticAdapter();m.fit(train)
        first=train[0]
        broken=replace(first,replicates=(Replicate((0.,)*176,1),)+first.replicates[1:])
        with self.assertRaises(ValueError):m.fit((broken,)+train[1:])
        with self.assertRaises(ValueError):m.predict((first.replicates[0].spectrum,))
