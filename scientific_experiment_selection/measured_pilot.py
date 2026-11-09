"""Issue #34 bounded local measured-data pilot; no input access on import.

Synthetic-only entry points stay guarded. Only the explicit CLI authorizes local
Exp3/Exp5 loading. All artifacts (including metrics) are private; stdout is redacted.
"""
import argparse
import copy
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import pickle
import platform
import subprocess

from .inventory import hash_file
from .raw_label_join import EXCLUSIONS, audit_join, read_mapping, run_audit
from .raw_spectra import read_raw, WELLS
from .nes_protocol import CONDITIONS, ACQUISITION, HOLDOUT, feature_rows, binary_condition_scores
from .selection import BudgetState, RandomSelector, CoverageSelector
from .logistic import FitRecord, MODEL_CONFIG, dependency_versions

PRIVATE_ROOT=Path(__file__).resolve().parents[1]/'data'/'private'
AUTHORIZATION={'issue':34,'scope':'local retrospective Exp3/Exp5 binary pilot',
               'source_training_authorized_promoted':False,'physical_label_verified':False}


@dataclass(frozen=True)
class PilotSample:
    well: str
    spectrum: tuple[float,...]
    label: int


@dataclass(frozen=True)
class PilotGroup:
    experiment: str
    condition: str
    samples: tuple[PilotSample,...]

    @property
    def group_id(self):
        return self.experiment+':'+self.condition


@dataclass(frozen=True)
class PilotScenario:
    initial: tuple[PilotGroup,...]
    acquisition: tuple[PilotGroup,...]
    holdout: tuple[PilotGroup,...]
    data_kind: str


@dataclass(frozen=True)
class PilotDesign:
    """Prospective settings only, intentionally a distinct measured design type."""
    group_id: str
    settings: tuple[tuple[str,str],...]
    cost: int = 1


@dataclass(frozen=True)
class PilotTrainingGroup:
    group_id: str
    samples: tuple[PilotSample,...]
    sample_weights: tuple[float,...]


def validate_scenario(scenario):
    if type(scenario) is not PilotScenario or scenario.data_kind not in ('measured-retrospective','synthetic-fixture'):
        raise ValueError('Explicit bounded pilot scenario required')
    seen=set()
    for groups,exp,conditions,total in ((scenario.initial,'Exp3',CONDITIONS,70),
            (scenario.acquisition,'Exp5',ACQUISITION,35),(scenario.holdout,'Exp5',HOLDOUT,18)):
        if type(groups) is not tuple or any(type(g) is not PilotGroup for g in groups):
            raise ValueError('Immutable pilot groups required')
        if len(groups)!=len(conditions) or {g.condition for g in groups}!=set(conditions):
            raise ValueError('Fixed condition partition mismatch')
        if sum(len(g.samples) for g in groups)!=total:
            raise ValueError('Fixed well count mismatch')
        for group in groups:
            expected=(2 if group.condition=='PFHxA_10' else 4) if exp=='Exp3' else (2 if group.condition=='TFA_20' else 3)
            if group.experiment!=exp or type(group.samples) is not tuple or len(group.samples)!=expected:
                raise ValueError('Frozen batch/group size mismatch')
            label=int(group.condition.split('_')[0]=='TFA')
            for sample in group.samples:
                if type(sample) is not PilotSample or sample.well not in WELLS:
                    raise ValueError('Invalid physical coordinate')
                key=(exp,sample.well)
                if key in seen or key in EXCLUSIONS:
                    raise ValueError('Duplicate, cross-role or excluded well')
                seen.add(key)
                if type(sample.label) is not int or sample.label!=label:
                    raise ValueError('Binary source-label disagreement')
                if (type(sample.spectrum) is not tuple or len(sample.spectrum)!=176
                        or any(type(v) not in (float,int) or not math.isfinite(v) for v in sample.spectrum)):
                    raise ValueError('Invalid complete measured spectrum')
    return True


def build_scenario(rows,raw,*,data_kind):
    """Existing join is an execution guard, not a fresh label reconstruction."""
    checked=audit_join(rows,raw)
    if checked['mismatches']:
        raise ValueError('Frozen audited join failed')
    grouped={}
    for row in rows:
        exp=row['experiment_id'];well=row['well']
        if row['sample_type']!='individual_pfas' or (exp,well) in EXCLUSIONS:
            continue
        condition=row['condition_code'];label=int(condition.split('_')[0]=='TFA')
        if row.get('tfa_present') not in (('True','true','1') if label else ('False','false','0')):
            raise ValueError('Source binary label disagrees with condition')
        grouped.setdefault((exp,condition),[]).append(PilotSample(well,tuple(raw[exp][well]['values']),label))
    def groups(exp,conditions):
        return tuple(PilotGroup(exp,c,tuple(sorted(grouped[(exp,c)],key=lambda r:WELLS.index(r.well)))) for c in conditions)
    scenario=PilotScenario(groups('Exp3',CONDITIONS),groups('Exp5',ACQUISITION),groups('Exp5',HOLDOUT),data_kind)
    validate_scenario(scenario)
    return scenario


def preflight(scenario):
    validate_scenario(scenario)
    spectra=tuple(r.spectrum for g in scenario.initial+scenario.acquisition+scenario.holdout for r in g.samples)
    # All predeclared arms must be feasible BEFORE any model fit; no arm/sample selection.
    counts={}
    for arm in 'BACD':
        success=0
        for spectrum in spectra:
            try:
                feature_rows((spectrum,),arm)
            except Exception as exc:
                raise ValueError(f'Arm {arm}: transform failed after {success}/123 successful wells; {type(exc).__name__}') from exc
            success+=1
        counts[arm]=success
    return counts


def load_sources(mapping,raw_root,raw_checksums,mapping_checksums):
    mapping,raw_root,raw_checksums,mapping_checksums=map(Path,(mapping,raw_root,raw_checksums,mapping_checksums))
    if mapping.name!='CeARS_Analysis_Step4_Individual_Classification.xlsx':
        raise ValueError('Only the previously audited Step4 source is supported')
    paths=(mapping,raw_checksums,mapping_checksums,raw_root/'Exp3 Plt3.xlsx',raw_root/'Exp5 Plt5.xlsx')
    before={str(path):hash_file(path)[1] for path in paths}
    audit=run_audit(mapping,raw_root,raw_checksums,mapping_checksums)
    if audit['mismatches'] or not audit.get('source_bytes_unchanged'):
        raise ValueError('Source provenance or frozen join failed')
    rows=read_mapping(mapping)
    raw={exp:read_raw(raw_root/f'{exp} Plt{exp[3:]}.xlsx') for exp in ('Exp3','Exp5')}
    scenario=build_scenario(rows,raw,data_kind='measured-retrospective')
    assert_unchanged(before)
    return scenario,before,audit


def assert_unchanged(hashes):
    if any(hash_file(Path(path))[1]!=digest for path,digest in hashes.items()):
        raise ValueError('Input changed; stop for review')


def training_view(groups):
    n=sum(len(g.samples) for g in groups)
    return tuple(PilotTrainingGroup(g.group_id,g.samples,
                 (n/(len(groups)*len(g.samples)),)*len(g.samples)) for g in groups)


class MeasuredLogisticAdapter:
    """Separate bounded grouped adapter; never casts real batches as synthetic."""
    def __init__(self,arm):
        if arm not in 'ABCD' or len(arm)!=1:
            raise ValueError('Expected frozen arm')
        self.arm=arm;self.fit_trace=();self.scaler_=None;self.classifier_=None

    def fit(self,groups):
        self.scaler_=None;self.classifier_=None
        if (not groups or any(type(g) is not PilotTrainingGroup or not g.samples for g in groups)
                or len({g.group_id for g in groups})!=len(groups)):
            raise ValueError('Bounded pilot training view required')
        n=sum(len(g.samples) for g in groups)
        for g in groups:
            if (any(type(r) is not PilotSample or type(r.label) is not int or r.label not in (0,1) for r in g.samples)
                    or len({r.label for r in g.samples})!=1
                    or len(g.sample_weights)!=len(g.samples)
                    or any(not math.isfinite(w) or not math.isclose(w,n/(len(groups)*len(g.samples)),rel_tol=1e-12,abs_tol=1e-12) for w in g.sample_weights)):
                raise ValueError('Expected unchanged labels and recomputed condition weights')
        from ._logistic_core import fit_weighted_logistic
        x=feature_rows(tuple(r.spectrum for g in groups for r in g.samples),self.arm)
        y=tuple(r.label for g in groups for r in g.samples)
        w=tuple(v for g in groups for v in g.sample_weights)
        scaler,classifier=fit_weighted_logistic(x,y,w)
        self.scaler_=scaler;self.classifier_=classifier
        self.fit_trace+=(FitRecord(len(self.fit_trace)+1,tuple(g.group_id for g in groups),n,len(x[0]),
            tuple(sum(g.sample_weights) for g in groups),tuple(float(v) for v in scaler.mean_),
            int(max(classifier.n_iter_)),True),)

    def predict(self,spectra):
        if self.classifier_ is None or self.scaler_ is None:
            raise ValueError('Pilot model not fitted')
        from threadpoolctl import threadpool_limits
        with threadpool_limits(limits=1):
            return tuple(int(v) for v in self.classifier_.predict(self.scaler_.transform(feature_rows(spectra,self.arm))))


def evaluate(model,holdout):
    evaluation_model=copy.deepcopy(model)
    predicted=tuple(evaluation_model.predict(tuple(r.spectrum for r in g.samples)) for g in holdout)
    if (len({g.group_id for g in holdout})!=len(holdout)
            or any(len(pred)!=len(g.samples) for g,pred in zip(holdout,predicted))):
        raise ValueError('Incomplete evaluator predictions')
    return binary_condition_scores(tuple(g.samples[0].label for g in holdout),predicted),predicted


def run_trajectory(scenario,selector,arm,*,checkpoint=None):
    preflight(scenario)
    # No arbitrary selector/model plug-in in the measured execution path.
    if not ((type(selector) is RandomSelector and selector.seed in (7,11,19)) or type(selector) is CoverageSelector):
        raise ValueError('Only frozen Random seeds and nominal coverage allowed')
    model=MeasuredLogisticAdapter(arm)
    available={g.group_id:g for g in scenario.acquisition}
    designs={gid:PilotDesign(gid,(('analyte',g.condition.split('_')[0]),('concentration',g.condition.split('_')[1]))) for gid,g in available.items()}
    history=();training=scenario.initial;state=BudgetState(12);curve=[]
    for k in range(13):
        chosen=None
        if k:
            allowed=tuple(designs[gid] for gid in sorted(available))
            gid=selector.choose(allowed,history,state)
            if type(gid) is not str or gid not in available:
                raise ValueError('Invalid or repeated acquisition')
            group=available.pop(gid);training+=(group,);history+=(designs[gid],)
            state=state.spend(designs[gid].cost);chosen=group.condition
        model.fit(training_view(training))
        scores,predictions=evaluate(model,scenario.holdout)
        record={'acquired_conditions':k,'spent_proxy_cost':state.spent,'selected_condition':chosen,
                **scores,'evaluation_predictions':predictions}
        curve.append(record)
        if checkpoint is not None:checkpoint(model,record)
    return {'arm':arm,'policy':selector.name,'seed':selector.seed,'curve':curve,
            'fit_trace':[asdict(record) for record in model.fit_trace],
            'data_kind':scenario.data_kind,'stop_reason':'pool_exhausted'}


def prepare_output(output):
    output=Path(output).absolute();root=PRIVATE_ROOT.absolute()
    if not output.is_relative_to(root) or output==root:
        raise ValueError('Artifacts must be inside local ignored private storage')
    # Check before resolve; a symlink must not redirect even within private storage.
    if any(p.is_symlink() for p in (output,*output.parents)):
        raise ValueError('Symlinked artifact paths are forbidden')
    output.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    output.mkdir(mode=0o700)
    return output


def write_json(path,value):
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    path.chmod(0o600)


def execute(mapping,raw_root,raw_checksums,mapping_checksums,output,*,authorized=False):
    if authorized is not True:
        raise PermissionError('Explicit Issue #34 measured pilot authorization required')
    output=prepare_output(output)
    try:
        scenario,hashes,audit=load_sources(mapping,raw_root,raw_checksums,mapping_checksums)
        transforms=preflight(scenario)
        versions=dependency_versions()
        record={'authorization':AUTHORIZATION,'input_sha256':hashes,'versions':versions,
                'python':platform.python_version(),'timestamp_utc':datetime.now(timezone.utc).isoformat(),
                'model_config':MODEL_CONFIG,'seeds':[7,11,19],'arm_order':list('BACD'),
                'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                 'argv':__import__('sys').argv,'audit':audit,'transform_counts':transforms,
                'implementation_sha256':{path.name:hash_file(path)[1] for path in Path(__file__).parent.glob('*.py')},
                'scenario':asdict(scenario)}
        write_json(output/'reproduction.json',record)
        runs=[]
        for arm in 'BACD':
            for selector in (RandomSelector(7),RandomSelector(11),RandomSelector(19),CoverageSelector()):
                name=f'{arm}-{selector.name}-{selector.seed}'
                def save(model,point):
                    with (output/f'{name}-k{point["acquired_conditions"]:02d}.pickle').open('xb') as stream:
                        pickle.dump(model,stream,pickle.HIGHEST_PROTOCOL)
                    stream_path=output/f'{name}-k{point["acquired_conditions"]:02d}.pickle'
                    stream_path.chmod(0o600)
                result=run_trajectory(scenario,selector,arm,checkpoint=save)
                assert_unchanged(hashes)
                write_json(output/f'{name}.json',result);runs.append(result)
        # All arms must use the same acquisition order for each policy/seed.
        if any([p['selected_condition'] for p in runs[i]['curve']]!=
               [p['selected_condition'] for p in runs[i%4]['curve']] for i in range(16)):
            raise ValueError('Paired acquisition order inconsistency')
        assert_unchanged(hashes)
        summary={'status':'completed-pending-scientific-review','data_kind':scenario.data_kind,
                 'source_bytes_unchanged':True,'runs':runs,'fit_count':16*13,
                 'limitations':['provisional analytical labels; not chemical verification',
                     'historically exposed retrospective Exp5 evaluation',
                     'only one positive evaluation condition; technical wells not independent',
                     'unit acquisition cost is a proxy; no prospective experiments']}
        write_json(output/'summary.json',summary)
        return {'status':'completed-pending-scientific-review','runs':16,'fits':208,'private_artifacts_only':True}
    except Exception as exc:
        write_json(output/'STOP.json',{'status':'review-needed','error_type':type(exc).__name__,
                                      'reason':str(exc),'action':'stop; no repair permitted'})
        raise


class SafeParser(argparse.ArgumentParser):
    def error(self,message):
        print(json.dumps({'status':'review-needed','reason':'invalid_or_missing_arguments'}))
        raise SystemExit(2)


def main():
    parser=SafeParser(description=__doc__)
    parser.add_argument('--run-measured-pilot',action='store_true',required=True)
    for name in ('mapping','raw-root','raw-checksums','mapping-checksums','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=vars(parser.parse_args());authorized=args.pop('run_measured_pilot')
    try:
        result=execute(**args,authorized=authorized)
    except Exception:
        result={'status':'review-needed','reason':'local_pilot_gate_failed','private_artifacts_only':True}
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status']=='completed-pending-scientific-review' else 2


if __name__=='__main__':
    raise SystemExit(main())
