"""Build a local provisional manifest. Never exports spectra or fits models."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import re

from .inventory import hash_file
from .raw_spectra import WELLS, read_raw

EXPERIMENTS = ('Exp3','Exp5','Exp8')
EXPECTED = {'Exp3':72,'Exp5':53,'Exp8':18}
ROLES = {'Exp3':'proposed_development',
         'Exp5':'proposed_historically_exposed_batch_transfer',
         'Exp8':'proposed_locked_holdout_pending_exposure_audit'}


def verify_hash(path, expected):
    digest=hash_file(Path(path))[1]
    if digest!=expected: raise ValueError(f'SHA-256 mismatch: {path}')
    return digest


def index_evidence(rows):
    result={}
    for row in rows:
        if row['experiment_id'] not in EXPERIMENTS: continue
        key=(row['experiment_id'],row['well'])
        if key in result: raise ValueError(f'Duplicate evidence coordinate: {key}')
        if row['well'] not in WELLS: raise ValueError(f'Invalid well: {key}')
        result[key]=row
    return result


def candidate_row(row, spectrum_present):
    exp=row['experiment_id']; condition=row['condition_claim']
    match=re.fullmatch(r'(TFA|PFPA|PFBA|PFHxA|PFOA|PFNA)_(5|10|20)',condition)
    individual=row['master_partition'] in ('individual_dataset','individual_external_batch_test')
    qc=row['historical_qc_status']
    included=bool(spectrum_present and match and individual and qc in ('include','review'))
    variants=json.loads(row['historical_variants'])
    preparation=[v for v in variants if v.get('preparation_status')]
    preparation_statuses=sorted({v['preparation_status'] for v in preparation})
    preparation_status=(preparation_statuses[0] if len(preparation_statuses)==1 else
                        'conflicting_claims' if preparation_statuses else 'unknown')
    warnings=['physical_label_not_independently_verified','preparation_group_unknown']
    if preparation_status=='reconstructed': warnings.append('reconstructed_preparation')
    if preparation_status=='unknown': warnings.append('preparation_status_missing')
    if preparation_status=='conflicting_claims': warnings.append('preparation_status_conflict')
    if exp=='Exp5': warnings.extend(['original_preparation_records_unavailable','historically_exposed'])
    if exp=='Exp8': warnings.append('locked_pending_historical_exposure_audit')
    if qc=='review': warnings.append('qc_review')
    if 'CONFLICT' in row['draft_mapping_review_status']: warnings.append('unresolved_conflict')
    if row['findings']: warnings.append('historical_findings_preserved')
    components=json.loads(row['master_composition_ppm'])
    disagreement=False
    if match and individual:
        # Compare explicit claims only. Missing fields stay missing, never zero.
        for analyte,value in components.items():
            if value in ('',None): continue
            try:
                number=float(value)
                expected=float(match[2]) if analyte==match[1] else 0.0
                disagreement |= not math.isfinite(number) or number!=expected
            except (TypeError,ValueError):
                disagreement=True
        if disagreement:
            warnings.append('condition_component_disagreement')
            included=False
    if spectrum_present and any(v in ('',None) for v in components.values()): warnings.append('missing_component_claims_not_imputed')
    if not spectrum_present: reason='no_recorded_spectrum'
    elif not individual or not match: reason='outside_single_analyte_task'
    elif disagreement: reason='conflicting_individual_claims_pending_review'
    elif qc not in ('include','review'): reason='historical_qc_exclusion_or_unapproved_status'
    else: reason='provisional_candidate_pending_review'
    return dict(experiment_id=exp,batch_claim=exp,physical_well=row['well'],
        source_sha256=row['sha256'],source_file=row['raw_file'],source_sheet='Sheet1',
        raw_header_cell=row['raw_header_cell'],raw_value_range=row['raw_value_range'],
        spectrum_present=spectrum_present,candidate_included=included,disposition_reason=reason,
        condition_claim=condition,label_claim=match[1] if match else None,
        concentration_claim_ppm=match[2] if match else None,
        component_claims_ppm=components,physical_label_verified=False,
        label_status='provisional_reconstructed' if preparation_status=='reconstructed' else 'provisional_not_independently_verified',
        preparation_status=preparation_status,
        preparation_source_claims=preparation,preparation_group='UNKNOWN',
        technical_replicate_group=f'{exp}:{condition}' if condition else None,
        group_basis='batch_condition_proxy_not_independent_preparation',group_independence_verified=False,
        replicate_claims=sorted({v['replicate'] for v in variants if v.get('replicate')}),
        qc_status_claim=qc,qc_reason_claim=row['historical_qc_reason'],
        proposed_role=ROLES[exp],locked=exp=='Exp8',
        target_tasks=['identity','concentration_known_identity'] if included else [],
        training_authorized=False,warnings=warnings,source_evidence=dict(row))


def validate_output(output, roots):
    output=Path(output).resolve()
    if output.exists(): raise ValueError('Output must be a fresh directory')
    for root in roots:
        root=Path(root).resolve()
        if output.is_relative_to(root) or root.is_relative_to(output):
            raise ValueError('Output and input locations must not overlap')


def _csv(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def build_manifest(raw_root, evidence_csv, raw_checksums, evidence_root, output):
    raw_root,evidence_csv,raw_checksums,evidence_root,output=map(Path,
        (raw_root,evidence_csv,raw_checksums,evidence_root,output))
    validate_output(output,[raw_root,evidence_root,evidence_csv.parent,raw_checksums.parent])
    inputs={}
    def track(path):
        inputs[str(path.resolve())]=hash_file(path)[1]
    for p in (evidence_csv,raw_checksums,evidence_root/'SHA256SUMS.csv'): track(p)
    # Verify the evidence bundle, without interpreting historical prediction sheets.
    bundle_checks=[]
    for r in _csv(evidence_root/'SHA256SUMS.csv'):
        p=(evidence_root/r['zip_relative_path']).resolve()
        if not p.is_relative_to(evidence_root.resolve()): raise ValueError('Unsafe manifest path')
        digest=verify_hash(p,r['sha256'])
        if p.stat().st_size!=int(r['size_bytes']): raise ValueError(f'Size mismatch: {p}')
        inputs[str(p)]=digest
        bundle_checks.append({'path':r['zip_relative_path'],'sha256':digest})
    expected_hashes={}
    for line in raw_checksums.read_text().splitlines():
        digest,name=line.split('  ',1)
        key=Path(name).name
        if key in expected_hashes: raise ValueError('Duplicate raw manifest filename')
        expected_hashes[key]=digest
    evidence=index_evidence(_csv(evidence_csv))
    expected_keys={(exp,w) for exp in EXPERIMENTS for w in WELLS}
    if set(evidence)!=expected_keys: raise ValueError('Evidence must cover all 288 coordinates')
    rows=[]; raw_checks=[]
    for exp in EXPERIMENTS:
        filename=f'{exp} Plt{exp[3:]}.xlsx'; path=raw_root/filename
        digest=verify_hash(path,expected_hashes[filename]); inputs[str(path.resolve())]=digest
        raw=read_raw(path)
        raw_checks.append({'experiment':exp,'file':filename,'sha256':digest,
                           'populated_wells':sum(v['values'] is not None for v in raw.values())})
        for well in WELLS:
            source=evidence[(exp,well)]; measured=raw[well]
            if source['sha256']!=digest or source['raw_file']!=filename:
                raise ValueError(f'Raw/evidence provenance mismatch: {exp} {well}')
            for key in ('raw_header_cell','raw_value_range'):
                if source[key]!=measured[key]: raise ValueError(f'Coordinate mismatch: {exp} {well}')
            if any(int(source[k])!=measured['point_count'] for k in ('nonempty_points','numeric_points')):
                raise ValueError(f'Presence mismatch: {exp} {well}')
            rows.append(candidate_row(source,measured['values'] is not None))
    counts=dict(Counter(r['experiment_id'] for r in rows if r['candidate_included']))
    if counts!=EXPECTED: raise ValueError(f'Candidate count discrepancy: {counts}; expected {EXPECTED}')
    for path,digest in inputs.items(): verify_hash(Path(path),digest)
    group_counts=Counter((r['experiment_id'],r['label_claim'],r['concentration_claim_ppm'])
                         for r in rows if r['candidate_included'])
    summary={'schema_version':'phase-a-v1','python':platform.python_version(),
        'data_kind':'observed_file_and_metadata_audit_not_verified_chemistry',
        'scientific_review':'pending','candidate_counts':counts,'total_coordinates':len(rows),
        'raw_checks':raw_checks,'evidence_bundle_checks':bundle_checks,'input_sha256':inputs,
        'candidate_class_concentration_counts':[dict(experiment=e,label_claim=l,concentration_claim_ppm=c,count=n)
                                              for (e,l,c),n in sorted(group_counts.items())],
        'counts_by_batch':{},'features_on_experimental_spectra':'not_run',
        'models_trained':False,'randomness':'none','source_hashes_unchanged':True}
    for exp in EXPERIMENTS:
        subset=[r for r in rows if r['experiment_id']==exp]
        summary['counts_by_batch'][exp]={
            'candidates':sum(r['candidate_included'] for r in subset),
            'excluded':sum(not r['candidate_included'] for r in subset),
            'qc':dict(Counter(r['qc_status_claim'] for r in subset)),
            'role':dict(Counter(r['proposed_role'] for r in subset)),
            'source':dict(Counter(r['source_file'] for r in subset)),
            'warnings':dict(Counter(w for r in subset for w in r['warnings'])),
            'candidate_warnings':dict(Counter(w for r in subset if r['candidate_included'] for w in r['warnings']))}
    output.mkdir(parents=True,exist_ok=False)
    manifest=output/'candidate_wells.json'
    manifest.write_text(json.dumps(rows,indent=2,sort_keys=True,ensure_ascii=True)+'\n')
    summary['candidate_manifest_sha256']=hash_file(manifest)[1]
    (output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    with (output/'candidate_wells.csv').open('w',newline='') as f:
        fields=[k for k in rows[0] if k!='source_evidence']+['evidence_record_reference']
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        for row in rows:
            flat={k:(json.dumps(v,sort_keys=True) if isinstance(v,(dict,list)) else v)
                  for k,v in row.items() if k!='source_evidence'}
            flat['evidence_record_reference']=f"{evidence_csv}#experiment={row['experiment_id']}&well={row['physical_well']}"
            writer.writerow(flat)
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('raw-root','evidence-csv','raw-checksums','evidence-root','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    try:
        summary=build_manifest(**vars(args))
    except (ValueError,OSError,KeyError) as exc:
        parser.exit(2,f'dataset-contract: {exc}\n')
    print(json.dumps({'candidate_counts':summary['candidate_counts'],'output':str(args.output)},sort_keys=True))


if __name__=='__main__': main()
