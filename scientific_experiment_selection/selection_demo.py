"""Run paired Random/coverage curves on fabricated binary conditions only."""
import argparse
from dataclasses import asdict
import json

from .selection import CandidateExperiment, OutcomeGroup, Replicate, SyntheticScenario, compare_selectors


def make_scenario():
    """Synthetic constants, not measurements, calibrated simulation or private labels."""
    def group(gid, batch, label, n):
        return OutcomeGroup(gid, batch, tuple(Replicate((.2 + .6*label,), label) for _ in range(n)))
    designs = tuple(CandidateExperiment(f'candidate-{i}', 'synthetic-pool',
                    (('nominal_standard', species), ('nominal_level', level)), 1)
                    for i, (species, level) in enumerate((('TFA','low'),('other','low'),
                                                         ('TFA','high'),('other','high'))))
    return SyntheticScenario(designs,
        tuple(group(d.group_id, d.batch, int(dict(d.settings)['nominal_standard'] == 'TFA'), i + 1)
              for i,d in enumerate(designs)),
        (group('initial-zero','synthetic-initial',0,2),group('initial-one','synthetic-initial',1,2)),
        (group('eval-zero','synthetic-evaluation',0,3),group('eval-one','synthetic-evaluation',1,3)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--budget', type=int, default=3, help='Nonnegative integer synthetic cost units')
    args = parser.parse_args()
    results = compare_selectors(make_scenario(), args.budget, args.seed)
    print(json.dumps({name: asdict(result) for name,result in results.items()}, indent=2, sort_keys=True))


if __name__ == '__main__': main()
