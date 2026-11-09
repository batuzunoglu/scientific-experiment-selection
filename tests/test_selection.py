"""Fabricated arrays/designs only; never reads an experimental source."""
from dataclasses import FrozenInstanceError, fields
import math
import unittest
from scientific_experiment_selection.selection import (
    CandidateExperiment as C, Replicate, OutcomeGroup as G, SyntheticScenario,
    SyntheticOracle, BudgetState, RandomSelector, CoverageSelector,
    UncertaintySelector, SyntheticMeanModel, run_selection, compare_selectors,
)


def design(gid, level='low', cost=1, batch='synthetic-pool'):
    return C(gid, batch, (('level',level),), cost)


def outcome(gid, label=0, n=2, feature=.2, batch='synthetic-pool'):
    return G(gid,batch,tuple(Replicate((feature,),label) for _ in range(n)))


def scenario(changed_holdout=False):
    ds=(design('a'),design('b','high'),design('c','mid'))
    return SyntheticScenario(ds,tuple(outcome(d.group_id,i%2,n=i+1) for i,d in enumerate(ds)),
        (outcome('initial',0,batch='synthetic-initial'),),
        (outcome('holdout',int(changed_holdout),batch='synthetic-evaluation'),))


class SelectionTests(unittest.TestCase):
    def test_immutable_finite_synthetic_contracts(self):
        c=design('a')
        with self.assertRaises(FrozenInstanceError): c.cost=4
        with self.assertRaises(ValueError): C('a','Exp5',(('x','low'),),1)
        for cost in [0,-1,True,1.1,float('nan')]:
            with self.assertRaises(ValueError): design('a',cost=cost)
        with self.assertRaises(ValueError): C('a','synthetic-pool',(('x','a'),('x','b')),1)
        with self.assertRaises(ValueError): Replicate((float('nan'),),0)
        with self.assertRaises(ValueError): Replicate((1,),True)
        with self.assertRaises(ValueError): G('x','synthetic-pool',())
        with self.assertRaises(ValueError): G('x','synthetic-pool',(Replicate((1,),0),Replicate((2,),1)))

    def test_disjoint_groups_duplicate_ids_and_batch_agreement(self):
        s=scenario()
        for bad in [lambda: SyntheticScenario(s.designs+s.designs,s.outcomes,s.initial,s.holdout),
                    lambda: SyntheticScenario(s.designs,s.outcomes,(s.outcomes[0],),s.holdout),
                    lambda: SyntheticScenario(s.designs,s.outcomes,s.initial,(s.outcomes[0],)),
                    lambda: SyntheticScenario(s.designs,s.outcomes[:-1],s.initial,s.holdout),
                    lambda: SyntheticScenario(s.designs,(outcome('a',batch='synthetic-other'),)+s.outcomes[1:],s.initial,s.holdout)]:
            with self.assertRaises(ValueError): bad()

    def test_budget_zero_exact_limit_invalid_and_no_overspend(self):
        b=BudgetState(2)
        self.assertEqual(b.spend(2).remaining,0)
        self.assertEqual(b.remaining,2)
        with self.assertRaises(ValueError): b.spend(3)
        for total in [-1,True,1.5,float('inf')]:
            with self.assertRaises(ValueError): BudgetState(total)
        r=run_selection(scenario(),RandomSelector(9),0,SyntheticMeanModel())
        self.assertEqual(len(r.curve),1)
        self.assertEqual(r.curve[0].spent,0)
        self.assertEqual(r.actions,())

    def test_oracle_one_shot_and_complete_group(self):
        s=scenario(); oracle=SyntheticOracle(s.designs,s.outcomes)
        group=oracle.reveal('b')
        self.assertEqual(len(group.replicates),2)
        with self.assertRaises(ValueError): oracle.reveal('b')
        with self.assertRaises(ValueError): oracle.reveal('unknown')

    def test_random_determinism_and_order_independence(self):
        a=run_selection(scenario(),RandomSelector(42),3,SyntheticMeanModel())
        b=run_selection(scenario(),RandomSelector(42),3,SyntheticMeanModel())
        self.assertEqual(a,b)
        self.assertEqual(a.seed,42)
        s=scenario()
        reordered=SyntheticScenario(tuple(reversed(s.designs)),s.outcomes,s.initial,s.holdout)
        self.assertEqual(a,run_selection(reordered,RandomSelector(42),3,SyntheticMeanModel()))

    def test_coverage_uses_design_levels_and_stable_id_ties(self):
        policy=CoverageSelector()
        self.assertEqual(policy.choose((design('b'),design('a')),(),BudgetState(2)),'a')
        self.assertEqual(policy.choose((design('b'),design('c','high')),(design('a'),),BudgetState(2)),'c')
        a=run_selection(scenario(),CoverageSelector(),3,SyntheticMeanModel())
        self.assertEqual(len(set(x.group_id for x in a.actions)),3)

    def test_whole_group_training_equal_total_weights(self):
        class Spy(SyntheticMeanModel):
            def fit(self,groups):
                self.seen=getattr(self,'seen',[])+[groups]
                return super().fit(groups)
        model=Spy();run_selection(scenario(),CoverageSelector(),3,model)
        self.assertEqual([len(g.replicates) for g in model.seen[-1]],[2,1,2,3])
        for groups in model.seen:
            n=sum(len(g.replicates) for g in groups)
            totals=[sum(g.sample_weights) for g in groups]
            self.assertTrue(all(math.isclose(x,n/len(groups)) for x in totals))
            self.assertAlmostEqual(sum(totals),n)

    def test_selector_never_receives_spectra_labels_or_holdout_scores(self):
        class Probe:
            name='probe';seed=None
            def choose(self,available_designs,observed_history,budget_state):
                for d in available_designs+observed_history:
                    self_outer.assertEqual({f.name for f in fields(d)}, {'group_id','batch','settings','cost'})
                    self_outer.assertFalse(hasattr(d,'replicates'))
                    self_outer.assertFalse(hasattr(d,'label'))
                self_outer.assertIsInstance(budget_state,BudgetState)
                return available_designs[0].group_id
        self_outer=self
        a=run_selection(scenario(),Probe(),3,SyntheticMeanModel())
        b=run_selection(scenario(True),Probe(),3,SyntheticMeanModel())
        self.assertEqual(a.actions,b.actions)
        self.assertNotEqual(a.curve[0].accuracy,b.curve[0].accuracy)

    def test_duplicate_unknown_holdout_and_unaffordable_actions_rejected(self):
        class Bad:
            name='bad';seed=None
            def __init__(self,ids): self.ids=iter(ids)
            def choose(self,*args): return next(self.ids)
        for ids in [('a','a'),('unknown',),('holdout',)]:
            with self.assertRaises(ValueError): run_selection(scenario(),Bad(ids),3,SyntheticMeanModel())
        s=scenario();ds=(design('a',cost=9),)+s.designs[1:]
        expensive=SyntheticScenario(ds,s.outcomes,s.initial,s.holdout)
        with self.assertRaises(ValueError): run_selection(expensive,Bad(('a',)),1,SyntheticMeanModel())

    def test_cost_is_per_condition_not_per_replicate(self):
        s=scenario();ds=tuple(design(d.group_id,cost=2) for d in s.designs)
        costly=SyntheticScenario(ds,s.outcomes,s.initial,s.holdout)
        r=run_selection(costly,CoverageSelector(),5,SyntheticMeanModel())
        self.assertEqual([p.spent for p in r.curve],[0,2,4])
        self.assertEqual(r.stop_reason,'no_affordable_design')
        self.assertEqual(r.curve[-1].acquired_conditions,2)

    def test_paired_same_scenario_budget_curve_and_seed_record(self):
        curves=compare_selectors(scenario(),3,seed=7)
        self.assertEqual(set(curves),{'random','coverage'})
        for r in curves.values():
            self.assertEqual([p.spent for p in r.curve],[0,1,2,3])
            self.assertEqual([p.acquired_conditions for p in r.curve],[0,1,2,3])
            self.assertEqual(r.budget,3)
        self.assertEqual(curves,compare_selectors(scenario(),3,seed=7))

    def test_uncertainty_rejects_unapproved_capabilities(self):
        for regime in ('none','screening','surrogate'):
            with self.assertRaises(PermissionError):
                run_selection(scenario(),UncertaintySelector(regime),1,SyntheticMeanModel())

    def test_no_holdout_training_or_evaluation_features_in_fit(self):
        class Spy(SyntheticMeanModel):
            def fit(self,groups):
                self_outer.assertNotIn('holdout',{g.group_id for g in groups})
                return super().fit(groups)
        self_outer=self
        run_selection(scenario(),CoverageSelector(),3,Spy())

    def test_hidden_candidate_values_cannot_change_actions(self):
        s=scenario()
        altered=tuple(outcome(g.group_id,1-g.replicates[0].label,n=5,feature=900) for g in s.outcomes)
        different=SyntheticScenario(s.designs,altered,s.initial,s.holdout)
        for make in (lambda:RandomSelector(4),CoverageSelector):
            a=run_selection(s,make(),3,SyntheticMeanModel())
            b=run_selection(different,make(),3,SyntheticMeanModel())
            self.assertEqual(a.actions,b.actions)

    def test_reveal_follows_valid_action_and_invalid_action_never_reveals(self):
        from unittest.mock import patch
        events=[]; original=SyntheticOracle.reveal
        class Recording(CoverageSelector):
            def choose(self,*args):
                chosen=super().choose(*args);events.append(('choose',chosen));return chosen
        def reveal(oracle,gid):
            events.append(('reveal',gid));return original(oracle,gid)
        with patch.object(SyntheticOracle,'reveal',reveal):
            run_selection(scenario(),Recording(),3,SyntheticMeanModel())
        self.assertEqual([x[0] for x in events],['choose','reveal']*3)
        self.assertTrue(all(events[i][1]==events[i+1][1] for i in range(0,6,2)))
        class Invalid:
            name='invalid';seed=None
            def choose(self,*args):return 'holdout'
        events.clear()
        with patch.object(SyntheticOracle,'reveal',reveal):
            with self.assertRaises(ValueError): run_selection(scenario(),Invalid(),3,SyntheticMeanModel())
        self.assertEqual(events,[])

    def test_evaluation_predict_side_effects_do_not_reach_learner(self):
        class Spy(SyntheticMeanModel):
            def predict(self,spectra):
                self.predict_saw_holdout=True
                return super().predict(spectra)
        model=Spy();run_selection(scenario(),CoverageSelector(),3,model)
        self.assertFalse(hasattr(model,'predict_saw_holdout'))

    def test_holdout_accuracy_weights_conditions_equally(self):
        s=scenario()
        holdout=(outcome('eval-zero',0,1,batch='synthetic-evaluation'),
                 outcome('eval-one',1,9,batch='synthetic-evaluation'))
        modified=SyntheticScenario(s.designs,s.outcomes,s.initial,holdout)
        r=run_selection(modified,CoverageSelector(),0,SyntheticMeanModel())
        self.assertEqual(r.curve[0].accuracy,.5)

    def test_mutable_nested_input_and_observed_design_features_rejected(self):
        with self.assertRaises(ValueError): C('a','synthetic-pool',[('level','low')],1)
        with self.assertRaises(ValueError): C('a','synthetic-pool',(('observed_spectrum','secret'),),1)
        with self.assertRaises(ValueError): Replicate([1.0],0)
        s=scenario()
        with self.assertRaises(ValueError): SyntheticScenario(s.designs,s.outcomes,list(s.initial),s.holdout)

    def test_demo_synthetic_positive_label_and_reproducibility(self):
        from scientific_experiment_selection.selection_demo import make_scenario
        s=make_scenario()
        for d,g in zip(s.designs,s.outcomes):
            self.assertEqual(g.replicates[0].label,int(dict(d.settings)['nominal_standard']=='TFA'))
        self.assertEqual(compare_selectors(s,3,7),compare_selectors(make_scenario(),3,7))
