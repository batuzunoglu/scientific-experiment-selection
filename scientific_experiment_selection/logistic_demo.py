"""Approved-recipe NES demonstration, fabricated 176-channel curves only."""
import argparse
from dataclasses import asdict
import json
from .nes_protocol import ARMS, make_synthetic_scenario, validate_nes_scenario
from .logistic import LogisticAdapter, MODEL_CONFIG, dependency_versions
from .selection import RandomSelector, CoverageSelector, run_selection


def demonstrate(arm='B',budget=12,seeds=(7,11,19)):
    if type(budget) is not int or not 0<=budget<=12:
        raise ValueError('Synthetic budget must be integer 0 through 12')
    if not seeds or any(type(s) is not int for s in seeds) or len(set(seeds))!=len(seeds):
        raise ValueError('Distinct explicit integer random seeds required')
    scenario=make_synthetic_scenario();validate_nes_scenario(scenario)
    runs={}
    for policy in tuple(RandomSelector(s) for s in seeds)+(CoverageSelector(),):
        model=LogisticAdapter(arm)
        result=run_selection(scenario,policy,budget,model,evaluation='condition_balanced')
        key=f'random-{policy.seed}' if policy.name=='random' else 'coverage'
        runs[key]={'trajectory':asdict(result),'refits':[asdict(r) for r in model.fit_trace]}
    return {'data_kind':'fabricated-synthetic-only','representation':arm,
        'model_config':dict(MODEL_CONFIG),'dependencies':dependency_versions(),
        'scaler':'training-only StandardScaler; same condition-equal weights as estimator',
        'positive_evaluation_conditions':1,'negative_evaluation_conditions':5,
        'caveat':'one positive condition; no real-data fitting, tuning or generalization claim',
        'runs':runs}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arm',choices=ARMS,default='B')
    parser.add_argument('--budget',type=int,default=12)
    parser.add_argument('--seeds',type=int,nargs='+',default=[7,11,19])
    args=parser.parse_args()
    print(json.dumps(demonstrate(args.arm,args.budget,tuple(args.seeds)),indent=2,sort_keys=True))


if __name__=='__main__':main()
