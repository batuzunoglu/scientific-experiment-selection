"""Deterministic aggregate-only export; reads completed reports, never fits/loads raw.

Build output from fixed labels and numeric allowlists, never private free text.
Compare REVIEW's six-decimal values with the original summary before any write.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

ARMS=('B','A','C','D')
REPRESENTATIONS={'A':'Raw/Full','B':'Raw/Compact8','C':'Area/Full','D':'Area/Compact8'}
STRATEGIES=(('random',7),('random',11),('random',19),('coverage',None))
POINT_FIELDS=('acquired_conditions','spent_proxy_cost','balanced_accuracy','sensitivity','specificity')
SCORES=POINT_FIELDS[2:]
HEADER=re.compile(r'### ([ABCD]) / (random|coverage) / seed (7|11|19|None)')
ROW=re.compile(r'\| (\d+) \| ([0-9]+\.[0-9]{6}) \| ([0-9]+\.[0-9]{6}) \| ([0-9]+\.[0-9]{6}) \|')


def _expected():
    return {(arm,policy,seed) for arm in ARMS for policy,seed in STRATEGIES}


def _review_curves(text):
    curves={};current=None
    for line in text.splitlines():
        if line.startswith('### '):
            match=HEADER.fullmatch(line)
            if match is None:
                raise ValueError('Unexpected review trajectory')
            arm,policy,seed=match.groups();key=(arm,policy,None if seed=='None' else int(seed))
            if key not in _expected() or key in curves:
                raise ValueError('Duplicate or unexpected review trajectory')
            curves[key]=[];current=key
        elif line.startswith('## '):
            current=None
        elif current is not None and re.match(r'\|\s*[+-]?\d',line):
            match=ROW.fullmatch(line)
            if match is None:
                raise ValueError('Invalid review numeric row')
            k,ba,sensitivity,specificity=match.groups()
            curves[current].append(dict(zip(POINT_FIELDS,(int(k),int(k),float(ba),float(sensitivity),float(specificity)))))
    if set(curves)!=_expected():
        raise ValueError('Expected every predeclared review trajectory')
    return curves


def _point(point):
    if not isinstance(point,dict) or not set(POINT_FIELDS)<=set(point):
        raise ValueError('Incomplete curve keys')
    result={name:point[name] for name in POINT_FIELDS}
    if any(type(result[name]) is not int for name in POINT_FIELDS[:2]):
        raise ValueError('Expected integer checkpoint/cost')
    for name in SCORES:
        value=result[name]
        if type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=1:
            raise ValueError('Scores must be finite numbers in [0,1]')
        result[name]=float(f'{value:.6f}')
    if abs(result['balanced_accuracy']-(result['sensitivity']+result['specificity'])/2)>1.000001e-6:
        raise ValueError('Balanced accuracy identity failed')
    return result


def sanitize(review_text,summary):
    """Return only static protocol labels and verified six-decimal aggregate scores."""
    if (summary.get('status')!='completed-pending-scientific-review'
            or summary.get('data_kind')!='measured-retrospective'
            or summary.get('source_bytes_unchanged') is not True):
        raise ValueError('Completed unchanged-source measured run required')
    reference=_review_curves(review_text);runs={}
    for run in summary['runs']:
        key=(run['arm'],run['policy'],run['seed'])
        if key not in _expected() or key in runs or (run['seed'] is not None and type(run['seed']) is not int):
            raise ValueError('Duplicate or unexpected original trajectory')
        points=[_point(point) for point in run['curve']]
        if (len(points)!=13 or [p['acquired_conditions'] for p in points]!=list(range(13))
                or [p['spent_proxy_cost'] for p in points]!=list(range(13))):
            raise ValueError('Expected all 13 checkpoints and fixed proxy budgets')
        if points!=[_point(point) for point in reference[key]]:
            raise ValueError('Original run and private report disagree')
        runs[key]=points
    if set(runs)!=_expected():
        raise ValueError('Expected all 16 original trajectories')
    for arm in ARMS:
        for k in (0,12):
            endpoints=[tuple(runs[(arm,policy,seed)][k][name] for name in SCORES) for policy,seed in STRATEGIES]
            if len(set(endpoints))!=1:
                raise ValueError('Per-arm baseline/final inconsistency')
    trajectories=[]
    for arm in ARMS:
        for policy,seed in STRATEGIES:
            trajectories.append({'arm':arm,'representation':REPRESENTATIONS[arm],
                'policy':'doe' if policy=='coverage' else 'random','seed':seed,
                'checkpoints':runs[(arm,policy,seed)]})
    return {'schema_version':1,'data_kind':'retrospective measured Exp3→Exp5 model results',
            'decimal_places':6,'trajectories':trajectories}


def render_json(result):
    return json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n'


def render_markdown(result):
    lines=['# Retrospective measured Exp3→Exp5 pilot results','',
        '**Evidence type: retrospective measured Exp3→Exp5 model results.** These are',
        'evaluations of the completed local pilot on existing measured spectra, separate',
        'from the earlier synthetic demo. No new wet-lab experiments or chemistry validation.', '',
        'Publication authority: [researcher instruction on Draft PR #35](https://github.com/batuzunoglu/scientific-experiment-selection/pull/35#issuecomment-6753082959).',
        'Only sanitized aggregate scores are published; private reports and artifacts remain unchanged.', '',
        '## Frozen protocol and interpretation','',
        '- Initial training: 70 Exp3 wells / 18 conditions; acquisition: 35 Exp5 wells / 12 conditions; fixed evaluation: 18 Exp5 wells / 6 conditions.',
        '- Historical labels are provisional analytical references. Exp5 was historically exposed; these are not pristine independent validation scores.',
        '- One positive fixed evaluator condition, `TFA_10`, and five negative conditions. Technical well replicates do not create independent prepared conditions.',
        '- Scoring averages correctness within each condition, then across conditions within each class. Balanced Accuracy = (TFA sensitivity + non-TFA specificity)/2.',
        '- Each whole prepared-condition acquisition costs one **proxy** unit; acquired conditions and cumulative proxy cost both run from 0 to 12.',
        '- Fixed condition-weighted StandardScaler and Logistic Regression L2/C=1/class_weight=None are refitted after each acquisition using training data only. No tuning or new fitting for this export.',
        '- B ran first, then A/C/D. Each arm uses Random seeds 7, 11, 19 and deterministic nominal DoE (`coverage` in the runner). DoE novelty considers acquisition history only.',
        '- Random and DoE are non-model-adaptive policies. No uncertainty/active-learning selector or prospective recommendation is demonstrated.',
        '- These exposed-holdout curves do not establish arm/policy superiority, confidence or generalization. More acquisition need not improve this fixed evaluation score.', '',
        '## Baseline and final (all policies agree at these endpoints)','',
        '| Arm | Representation | Budget / proxy cost | Balanced Accuracy | Sensitivity | Specificity |',
        '| --- | --- | ---: | ---: | ---: | ---: |']
    for arm in ARMS:
        run=next(r for r in result['trajectories'] if r['arm']==arm)
        for k in (0,12):
            p=run['checkpoints'][k]
            lines.append(f"| {arm} | {run['representation']} | {k} | {p['balanced_accuracy']:.6f} | {p['sensitivity']:.6f} | {p['specificity']:.6f} |")
    lines+=['','## Complete trajectories','',
        'All 16 predeclared trajectories and all 13 checkpoints follow, including unfavorable outcomes.',
        'Scores are rounded to six decimal places, matching the private original aggregate report.',
        'JSON has the same rounded values; rounding may cause at most 0.000001 BA arithmetic difference.',
        '[Machine-readable aggregate JSON](results/exp3-exp5-nes-2026-11-09-aggregate.json).','']
    for run in result['trajectories']:
        seed='none (deterministic)' if run['seed'] is None else str(run['seed'])
        policy='DoE / nominal coverage' if run['policy']=='doe' else 'Random'
        lines += [f"### {run['arm']} — {run['representation']} — {policy} — seed {seed}",'',
            '| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |',
            '| ---: | ---: | ---: | ---: | ---: |']
        for p in run['checkpoints']:
            lines.append(f"| {p['acquired_conditions']} | {p['spent_proxy_cost']} | {p['balanced_accuracy']:.6f} | {p['sensitivity']:.6f} | {p['specificity']:.6f} |")
        lines+=['']
    lines += ['## Export verification and reproduction','',
        'The deterministic exporter reads only the existing private aggregate REVIEW.md and completed',
        'run summary. It constructs an allowlisted output, compares every published score against',
        'both originals at six decimals, and rejects missing/duplicate trajectories, invalid scores,',
        'incomplete checkpoints, wrong costs, BA arithmetic or baseline/final inconsistencies.',
        'No private prose, paths, source hashes, well labels, predictions, spectra, features or models',
        'are copied. Selected-condition sequences are intentionally omitted as unnecessary here.','',
        'Configure input variables locally; their values are never printed:','', '```bash',
        'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.pilot_results_export \\',
        '  --review "$PRIVATE_REVIEW" --summary "$PRIVATE_SUMMARY" \\',
        '  --markdown docs/MEASURED_PILOT_RESULTS.md \\',
        '  --json docs/results/exp3-exp5-nes-2026-11-09-aggregate.json',
        '# Repeat the same command with --check to verify without writing.',
        'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v',
        'git diff --check', '```','',
        'Synthetic exporter tests use fabricated scores and privacy canaries, never these measured',
        'values or private sources. Public CI tests code, not the original private measured run.',
        'See [pilot methodology](MEASURED_PILOT.md) and appended Notebook Entry 035 for execution',
        'and verification notes. Numerical scientific review remains pending; keep PR #35 Draft.', '']
    return '\n'.join(lines)


def export(review,summary,markdown,json_path,*,check=False):
    review,summary,markdown,json_path=map(Path,(review,summary,markdown,json_path))
    paths=(review,summary,markdown,json_path)
    if len({p.resolve() for p in paths})!=4 or any(p.is_symlink() for p in paths):
        raise ValueError('Inputs and outputs must be distinct regular paths')
    if any(left.exists() and right.exists() and left.samefile(right)
           for i,left in enumerate(paths) for right in paths[i+1:]):
        raise ValueError('Hardlinked inputs/outputs are forbidden')
    before={p:hashlib.sha256(p.read_bytes()).digest() for p in (review,summary)}
    result=sanitize(review.read_text(),json.loads(summary.read_text()))
    outputs={markdown:render_markdown(result),json_path:render_json(result)}
    if any(hashlib.sha256(p.read_bytes()).digest()!=digest for p,digest in before.items()):
        raise ValueError('Private source changed during export')
    if check:
        if any(path.read_text()!=text for path,text in outputs.items()):
            raise ValueError('Published output does not match verified export')
    else:
        for path,text in outputs.items():
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(text,encoding='utf-8')
    return {'status':'verified','trajectories':16,'checkpoints':208,'metric_values_checked':624}


class SafeParser(argparse.ArgumentParser):
    def error(self,message):
        print('{"status":"failed","reason":"invalid_arguments"}')
        raise SystemExit(2)


def main():
    parser=SafeParser(description=__doc__)
    for flag in ('review','summary','markdown','json'):
        parser.add_argument('--'+flag,type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=vars(parser.parse_args());args['json_path']=args.pop('json')
    try:
        result=export(**args)
    except Exception:
        print('{"status":"failed","reason":"aggregate_export_validation"}')
        return 2
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
