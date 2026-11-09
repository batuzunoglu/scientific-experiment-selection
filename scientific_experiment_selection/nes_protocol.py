"""Approved public nominal split, synthetic spectra, fixed-arm features and metrics.

No file/data loader. Nominal group names are approved metadata, not private labels.
"""
import math
from .selection import CandidateExperiment, OutcomeGroup, Replicate, SyntheticScenario
from .spectral import GRID, validate, compact8, area_factor

SPECIES = ('TFA','PFPA','PFBA','PFHxA','PFOA','PFNA')
LEVELS = (5,10,20)
HOLDOUT = ('PFPA_5','PFOA_5','TFA_10','PFHxA_10','PFBA_20','PFNA_20')
ACQUISITION = ('TFA_5','PFBA_5','PFHxA_5','PFNA_5','PFPA_10','PFBA_10',
               'PFOA_10','PFNA_10','TFA_20','PFPA_20','PFHxA_20','PFOA_20')
CONDITIONS = tuple(f'{p}_{c}' for p in SPECIES for c in LEVELS)
ARMS = ('A','B','C','D')


def feature_rows(spectra, arm='B'):
    if arm not in ARMS:
        raise ValueError('Expected fixed arm A/B/C/D; no extra preprocessing')
    rows=[]
    for spectrum in spectra:
        y=validate(GRID,spectrum)
        if arm in ('C','D'):
            factor=area_factor(GRID,y)
            y=[v/factor for v in y]
        row=compact8(GRID,y) if arm in ('B','D') else y
        if not all(math.isfinite(v) for v in row):
            raise ValueError('Nonfinite representation; no sample dropping')
        rows.append(tuple(row))
    return tuple(rows)


def condition_binary_metrics(groups, predictions):
    """Within-condition correctness, then within-class means; both classes required."""
    if not groups or len(groups)!=len(predictions):
        raise ValueError('Aligned nonempty groups/predictions required')
    if len({g.group_id for g in groups})!=len(groups):
        raise ValueError('Duplicate evaluation condition')
    for group,predicted in zip(groups,predictions):
        if type(group) is not OutcomeGroup or len(predicted)!=len(group.replicates):
            raise ValueError('Predictions must cover complete synthetic condition')
    return binary_condition_scores(tuple(g.replicates[0].label for g in groups), predictions)


def binary_condition_scores(labels, predictions):
    """Data-independent metric math; callers validate complete disjoint groups."""
    if not labels or len(labels)!=len(predictions):
        raise ValueError('Aligned nonempty condition labels/predictions required')
    recalls={0:[],1:[]}
    for label,predicted in zip(labels,predictions):
        if type(label) is not int or label not in (0,1) or not predicted:
            raise ValueError('Expected binary condition label and nonempty predictions')
        if any(type(p) is not int or p not in (0,1) for p in predicted):
            raise ValueError('Expected integer binary predictions')
        recalls[label].append(sum(p==label for p in predicted)/len(predicted))
    if not recalls[0] or not recalls[1]:
        raise ValueError('Balanced accuracy undefined: both condition classes required')
    sensitivity=sum(recalls[1])/len(recalls[1])
    specificity=sum(recalls[0])/len(recalls[0])
    return {'balanced_accuracy':(sensitivity+specificity)/2,
            'sensitivity':sensitivity,'specificity':specificity,
            'positive_conditions':len(recalls[1]),'negative_conditions':len(recalls[0])}


def validate_nes_scenario(scenario):
    if type(scenario) is not SyntheticScenario:
        raise ValueError('Synthetic scenario required')
    def check(groups,batch,conditions):
        expected={f'{batch}:{c}' for c in conditions}
        if {g.group_id for g in groups}!=expected:
            raise ValueError('Nominal condition-role partition mismatch')
        for group in groups:
            if group.batch!=batch:
                raise ValueError('Synthetic nominal batch mismatch')
            condition=group.group_id.split(':',1)[1]
            if group.replicates[0].label!=int(condition.split('_')[0]=='TFA'):
                raise ValueError('Synthetic binary nominal-label mismatch')
            if any(len(r.spectrum)!=176 for r in group.replicates):
                raise ValueError('Expected full 176-channel synthetic inputs')
    check(scenario.initial,'synthetic-exp3',CONDITIONS)
    check(scenario.outcomes,'synthetic-exp5',ACQUISITION)
    check(scenario.holdout,'synthetic-exp5',HOLDOUT)
    if {d.group_id for d in scenario.designs}!={f'synthetic-exp5:{c}' for c in ACQUISITION}:
        raise ValueError('Acquisition designs must match approved pool')
    for d in scenario.designs:
        condition=d.group_id.split(':',1)[1];p,c=condition.split('_')
        if dict(d.settings)!={'analyte':p,'concentration':c} or d.cost!=1:
            raise ValueError('Nominal design settings/unit-cost schedule mismatch')
    return True


def make_synthetic_scenario():
    """Fixed analytic Gaussian toy curves; no measured/calibrated parameters or I/O.

    Constants chosen before evaluation. Synthetic target changes baseline and
    positive peak strength; no regeneration/tuning based on evaluation performance.
    """
    def group(condition,batch):
        p,concentration=condition.split('_');level=int(concentration);label=int(p=='TFA')
        n=(2 if condition=='PFHxA_10' else 4) if batch=='synthetic-exp3' else (2 if condition=='TFA_20' else 3)
        reps=[]
        for i in range(n):
            target=batch=='synthetic-exp5'
            baseline=.12+(.08 if target else 0)+.0005*level+.001*i
            peak420=(.38 if target else .7) if label else .15+.01*SPECIES.index(p)
            peak518=.22 if label else .62
            y=tuple(baseline+peak420*math.exp(-((x-420)/28)**2)
                    +peak518*math.exp(-((x-518)/34)**2)+.00002*level*(x-350)
                    for x in GRID)
            reps.append(Replicate(y,label))
        return OutcomeGroup(f'{batch}:{condition}',batch,tuple(reps))
    designs=tuple(CandidateExperiment(f'synthetic-exp5:{c}','synthetic-exp5',
                  (('analyte',c.split('_')[0]),('concentration',c.split('_')[1])),1) for c in ACQUISITION)
    s=SyntheticScenario(designs,tuple(group(c,'synthetic-exp5') for c in ACQUISITION),
        tuple(group(c,'synthetic-exp3') for c in CONDITIONS),
        tuple(group(c,'synthetic-exp5') for c in HOLDOUT))
    validate_nes_scenario(s)
    return s
