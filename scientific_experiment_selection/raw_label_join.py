"""Issue #31 read-only historical metadata/raw-column join; aggregate output only.

Uses existing Well_Metadata labels; no label reconstruction, feature transforms or
models. Raw file selection is hard-limited to the two authorized experiments.
"""
import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET
from .inventory import hash_file
from .raw_spectra import read_raw, WELLS
from .nes_protocol import SPECIES, CONDITIONS, HOLDOUT, ACQUISITION

EXPERIMENTS=('Exp3','Exp5')
EXCLUSIONS=frozenset((('Exp3','D6'),('Exp3','D7'),('Exp5','B7')))
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_mapping(path):
    """Decode only historical Well_Metadata; select Exp3/5 before deriving records."""
    with zipfile.ZipFile(path) as z:
        rels={r.get('Id'):r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets=ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS)
        sheet=next(s for s in sheets if s.get('name')=='Well_Metadata')
        target=rels[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
        target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        def value(c):
            if c.find('s:f',NS) is not None:raise ValueError('Mapping formula unsupported')
            v=c.find('s:v',NS);v=v.text if v is not None else ''
            if c.get('t')=='s':return strings[int(v)]
            if c.get('t')=='inlineStr':return ''.join(c.find('s:is',NS).itertext())
            return v
        xmlrows=ET.fromstring(z.read(target)).findall('s:sheetData/s:row',NS)
        headers={re.sub('[0-9]','',c.get('r')):value(c) for c in xmlrows[0]}
        if len(set(headers.values()))!=len(headers):raise ValueError('Duplicate metadata headers')
        expcol=next(k for k,v in headers.items() if v=='experiment_id')
        result=[]
        for row in xmlrows[1:]:
            cells={re.sub('[0-9]','',c.get('r')):c for c in row}
            if expcol not in cells or value(cells[expcol]) not in EXPERIMENTS:continue
            result.append({name:value(cells[col]) if col in cells else '' for col,name in headers.items()})
        return result


def audit_join(mapping, raw):
    mismatches=Counter();counts=Counter();seen=set();groups=defaultdict(set)
    source_groups=defaultdict(set)
    rows=[r for r in mapping if isinstance(r,dict) and r.get('experiment_id') in EXPERIMENTS]
    coord=Counter(r['experiment_id'] for r in rows)
    counts['mapping_coordinates']=len(rows)
    for row in rows:
        exp=row['experiment_id'];well=row.get('well');key=(exp,well)
        if not isinstance(well,str) or well not in WELLS:
            mismatches['invalid_mapping_coordinate']+=1;continue
        if key in seen:mismatches['duplicate_mapping_coordinate']+=1
        seen.add(key)
        if row.get('sample_type')!='individual_pfas':continue
        counts['source_individual_'+exp]+=1
        condition=row.get('condition_code')
        if condition not in CONDITIONS:
            mismatches['invalid_condition_claim']+=1;continue
        p,level=condition.split('_')
        for name in SPECIES:
            try:
                number=Decimal(row.get(name+'_ppm',''))
                if not number.is_finite() or number!=Decimal(level if name==p else '0'):
                    mismatches['component_condition_disagreement']+=1
            except (InvalidOperation,TypeError,ValueError):
                mismatches['missing_or_invalid_component']+=1
        expected_role='individual_train' if exp=='Exp3' else 'individual_external_test'
        if row.get('model_partition')!=expected_role:mismatches['historical_role_disagreement']+=1
        gid=row.get('analysis_group_id')
        if not isinstance(gid,str) or not gid:mismatches['missing_source_group']+=1
        else:source_groups[(exp,gid)].add(condition)
        if row.get('has_spectrum') not in ('True','true','1',True):mismatches['mapping_presence_disagreement']+=1
        if key in EXCLUSIONS:
            counts['excluded_wells']+=1
            if exp=='Exp5' and row.get('qc_status')!='exclude':mismatches['known_exclusion_qc_disagreement']+=1
            continue
        if row.get('qc_status') not in ('include','review_include','review','accepted'):
            mismatches['unexpected_eligible_qc']+=1
        if exp=='Exp3':role='training'
        elif condition in HOLDOUT:role='holdout'
        elif condition in ACQUISITION:role='acquisition'
        else:mismatches['fixed_role_unassigned']+=1;continue
        groups[(exp,condition,role)].add(well)
        counts[role+'_wells']+=1
        matched=raw.get(exp,{}).get(well)
        if matched is None:mismatches['raw_column_absent']+=1
        elif matched.get('point_count')!=176 or matched.get('values') is None:
            mismatches['raw_presence_or_shape']+=1
        else:counts['joined_wells']+=1
    if any(len(cs)!=1 for cs in source_groups.values()):mismatches['source_group_condition_alias']+=1
    for exp in EXPERIMENTS:
        if coord[exp]!=96 or {w for e,w in seen if e==exp}!=set(WELLS):mismatches['mapping_coordinate_coverage']+=1
    expected={'training_wells':70,'acquisition_wells':35,'holdout_wells':18,
              'excluded_wells':3,'joined_wells':123,'source_individual_Exp3':72,'source_individual_Exp5':54}
    for field,n in expected.items():
        if counts[field]!=n:mismatches['count_mismatch_'+field]+=1
    for exp,role,conditions in [('Exp3','training',CONDITIONS),('Exp5','acquisition',ACQUISITION),('Exp5','holdout',HOLDOUT)]:
        subset={condition:wells for (e,condition,r),wells in groups.items() if e==exp and r==role}
        counts[role+'_groups']=len(subset)
        if set(subset)!=set(conditions):mismatches['condition_group_coverage']+=1
        for c,wells in subset.items():
            expected_n=(2 if c=='PFHxA_10' else 4) if exp=='Exp3' else (2 if c=='TFA_20' else 3)
            if len(wells)!=expected_n:mismatches['condition_group_size']+=1
    # No complete source condition may cross current acquisition/evaluator roles.
    roles=defaultdict(set)
    for exp,condition,role in groups:roles[(exp,condition)].add(role)
    if any(len(rs)>1 for rs in roles.values()):mismatches['condition_role_leakage']+=1
    return {'status':'review-needed' if mismatches else 'join-consistent-pending-review',
        'counts':dict(sorted(counts.items())),'mismatches':dict(sorted(mismatches.items())),
        'training_permission':False,'physical_labels_verified':False}


def _csv(path):
    with path.open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))


def run_audit(mapping,raw_root,raw_checksums,mapping_checksums):
    mapping,raw_root,raw_checksums,mapping_checksums=map(Path,(mapping,raw_root,raw_checksums,mapping_checksums))
    paths=(mapping,raw_checksums,mapping_checksums)
    before={p:hash_file(p)[1] for p in paths}
    relative=mapping.resolve().relative_to(mapping_checksums.resolve().parent).as_posix()
    matches=[r for r in _csv(mapping_checksums) if r['zip_relative_path']==relative]
    if len(matches)!=1 or before[mapping]!=matches[0]['sha256']:
        return failure('mapping_provenance_mismatch')
    if mapping.stat().st_size!=int(matches[0]['size_bytes']):return failure('mapping_size_mismatch')
    expected={}
    for line in raw_checksums.read_text().splitlines():
        digest,name=line.split('  ',1)
        if Path(name).name in ('Exp3 Plt3.xlsx','Exp5 Plt5.xlsx'):
            if Path(name).name in expected:return failure('duplicate_raw_provenance')
            expected[Path(name).name]=digest
    rows=read_mapping(mapping)
    raw={}
    for exp in EXPERIMENTS:
        path=raw_root/f'{exp} Plt{exp[3:]}.xlsx'
        digest=hash_file(path)[1]
        if digest!=expected.get(path.name):return failure('raw_provenance_mismatch')
        before[path]=digest
        try:raw[exp]=read_raw(path)
        except Exception:return failure('raw_schema_or_numeric_error')
    result=audit_join(rows,raw)
    if any(hash_file(p)[1]!=digest for p,digest in before.items()):return failure('source_changed')
    result['source_bytes_unchanged']=True
    return result


def failure(category):
    return {'status':'review-needed','counts':{},'mismatches':{category:1},
            'training_permission':False,'physical_labels_verified':False}


class SafeParser(argparse.ArgumentParser):
    def error(self,message):
        print(json.dumps(failure('invalid_arguments'),sort_keys=True));raise SystemExit(2)


def main():
    parser=SafeParser(description=__doc__)
    for name in ('mapping','raw-root','raw-checksums','mapping-checksums'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    try:result=run_audit(**vars(args))
    except Exception:result=failure('source_missing_or_schema_error')
    print(json.dumps(result,sort_keys=True))
    return 2 if result['mismatches'] else 0


if __name__=='__main__':raise SystemExit(main())
