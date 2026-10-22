"""Read-only, deterministic evidence comparisons; never resolves chemical labels."""
import csv, json, re, sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from inspect_sources import read_xlsx, sha

raw, evidence, out = map(Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
before = {str(p):sha(p) for root in (raw,evidence) for p in sorted(root.rglob('*')) if p.is_file()}
books = {p.name:(p,read_xlsx(p)) for p in sorted(evidence.rglob('*.xlsx'))}
AN = ['TFA','PFPA','PFBA','PFHxA','PFOA','PFNA']
WELLS = [f'{r}{c}' for r in 'ABCDEFGH' for c in range(1,13)]
def dump(name,obj): (out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def csvout(name,rows):
    if not rows: return
    with (out/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def table(name,sheet,header=None):
    p,ss=books[name]; rows=ss[sheet]
    if header is None:
        header=next(r['row'] for r in rows if 'experiment_id' in r['cells'].values())
    h=next(r for r in rows if r['row']==header)
    columns={re.sub(r'\d','',c):v for c,v in h['cells'].items() if v}
    return [dict({v:r['cells'].get(c+str(r['row']),'') for c,v in columns.items()},_ref=f'{p.relative_to(evidence)}#{sheet}!row={r["row"]}') for r in rows if r['row']>header and any(r['cells'].values())]
def norm(v):
    if v in ('',None): return None
    try: return str(Decimal(str(v)).normalize())
    except InvalidOperation: return str(v)
def key(r): return r.get('experiment_id'),r.get('well')
def keyed(rows):
    keys=[key(r) for r in rows]; assert len(keys)==len(set(keys)), 'Duplicate metadata keys'
    return dict(zip(keys,rows))
def refcsv(p):
    return [dict(r,_ref=f'{p.relative_to(evidence)}#CSV-record={i}') for i,r in enumerate(csv.DictReader(p.open()),2)]

hashchecks=[]
for r in csv.DictReader((evidence/'SHA256SUMS.csv').open()):
    p=evidence/r['zip_relative_path']
    hashchecks.append(dict(r,observed_sha256=sha(p),hash_match=sha(p)==r['sha256'],size_match=p.stat().st_size==int(r['size_bytes'])))
assert all(r['hash_match'] and r['size_match'] for r in hashchecks)
dump('input_hashes.json',{'all_inputs':before,'bundle_manifest_checks':hashchecks})
hist=[]
for name,(p,ss) in books.items():
    for sheet in ('RAW_FILE_PROVENANCE','File_Provenance','File_Manifest'):
        if sheet not in ss: continue
        for row in ss[sheet]:
            vals=list(row['cells'].values())
            exp=next((v for v in vals if re.fullmatch('Exp[1-8]',v or '')),None)
            digest=next((v for v in vals if re.fullmatch('[0-9a-f]{64}',v or '')),None)
            if exp and digest:
                hist.append({'experiment':exp,'historical_filename':next((v for v in vals if v.endswith('.xlsx')),''),'historical_sha256':digest,'source':f'{p.relative_to(evidence)}#{sheet}!row={row["row"]}'})
rawrows=[]; summary=[]
for exp in range(1,9):
    p=raw/f'Exp{exp} Plt{exp}.xlsx'; ss=read_xlsx(p); assert list(ss)==['Sheet1']
    rows=ss['Sheet1']; headers=rows[0]['cells']; wh={c[:-1]:v for c,v in headers.items() if re.fullmatch(r'[A-H](?:[1-9]|1[0-2])',v or '')}
    assert list(wh.values())==WELLS and len(headers)==98
    waves=[Decimal(r['cells']['A'+str(r['row'])]) for r in rows[1:]]
    assert waves==[Decimal(350+2*i) for i in range(176)]
    counts=[]
    for col,well in wh.items():
        vals=[r['cells'].get(col+str(r['row']),'') for r in rows[1:]]
        nonempty=[v for v in vals if v!='']; numeric=[]
        for v in nonempty:
            try: numeric.append(Decimal(v).is_finite())
            except InvalidOperation: numeric.append(False)
        assert all(numeric), f'Non-numeric raw cell in {p.name} {well}'
        counts.append(len(nonempty))
        rawrows.append({'experiment_id':f'Exp{exp}','well':well,'raw_file':p.name,'sha256':sha(p),'raw_header_cell':col+'1','raw_value_range':f'{col}2:{col}177','nonempty_points':len(nonempty),'numeric_points':sum(numeric)})
    refs=[dict(r,match=r['historical_sha256']==sha(p)) for r in hist if r['experiment']==f'Exp{exp}']
    assert refs and all(r['match'] for r in refs)
    summary.append({'experiment':f'Exp{exp}','filename':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'headings':len(wh),'populated_wells':sum(c>0 for c in counts),'empty_wells':sum(c==0 for c in counts),'partial_wells':sum(0<c<176 for c in counts),'historical_hash_references':refs})
csvout('raw_well_columns.csv',rawrows); dump('raw_verification.json',summary)
rawmap=keyed(rawrows)
mastername='CeARS_Master_Well_Map_Verified(2).xlsx'
master=keyed(table(mastername,'MASTER_WELL_MAP',1))
draftpath=evidence/'01_reconciliation/CeARS_Evidence_Aware_Master_Well_Map_DRAFT_2026-10-22.csv'
draft=keyed(refcsv(draftpath))
draftxlsx=keyed(table('CeARS_Evidence_Aware_Master_Well_Map_DRAFT_2026-10-22.xlsx','EVIDENCE_WELL_MAP',1))
assert master.keys()==draft.keys()==draftxlsx.keys()
csv_xlsx_diffs=[{'key':k,'field':f,'csv':v,'xlsx':draftxlsx[k].get(f)} for k,r in draft.items() for f,v in r.items() if f!='_ref' and norm(v)!=norm(draftxlsx[k].get(f))]
audit=keyed(table('Step1_Dataset_Audit_Exp3_Exp8.xlsx','Well_Metadata',1))
shared=sorted((set(next(iter(master.values()))) & set(next(iter(audit.values()))))-{'_ref'})
lineage_diffs=[{'key':k,'field':f,'master':master[k][f],'audit':audit[k][f]} for k in master for f in shared if norm(master[k][f])!=norm(audit[k][f])]
sources={}
for name,(p,ss) in books.items():
    for sheet in ('Well_Metadata','Development_Features','External_Exp6_LOCKED','Step3_Well_Features'):
        if sheet in ss:
            records=table(name,sheet); sources[name+'#'+sheet]=keyed(records)
sources['exp5_well_metadata.csv']=keyed(refcsv(evidence/'04_historical_analysis_recovered_ml/exp5_well_metadata.csv'))
variants=defaultdict(list)
for source,records in sources.items():
    for k,r in records.items():
        if k not in rawmap: continue
        item={'source':source,'reference':r['_ref'],'condition':r.get('condition_code',''),'composition_ppm':{a:r.get(a+'_ppm',r.get(a.lower()+'_ppm','')) for a in AN},'replicate':r.get('technical_replicate',r.get('replicate','')),'qc':r.get('qc_status',''),'qc_reason':r.get('qc_reason',''),'partition':r.get('model_partition',r.get('dataset_partition',r.get('dataset_role',''))),'use_in_model':r.get('use_in_model',''),'preparation_status':r.get('preparation_status','')}
        if 'exp5_' in source: item['preparation_provenance']={f:v for f,v in r.items() if f.startswith(('preparation_','label_source')) or f in ('recipe','master_ul','water_ul','pfas_ul','final_volume_ul','pfas_source')}
        variants[k].append(item)

plans={}
plan_specs=[('CeARS_PFAS_Master_Experiment_Record_and_Analysis_Plan.xlsx','Plate_Maps',[(f'Exp{i}',start) for i,start in [(3,5),(4,18),(5,31),(6,44)]]),('PFCA_Mixture_Plate_Plan_RQ5_RQ8.xlsx','Plate Plan',[('Exp7',6)]),('Exp8_Bridge_Experiment_Plan.xlsx','Bridge Experiment Plan',[('Exp8',23)])]
for name,sheet,blocks in plan_specs:
    p,ss=books[name]; rows={r['row']:r['cells'] for r in ss[sheet]}
    for exp,start in blocks:
        for offset,letter in enumerate('ABCDEFGH'):
            rn=start+offset
            for c in range(1,13):
                cell=chr(65+c)+str(rn)
                plans[(exp,f'{letter}{c}') ]={'label':rows[rn].get(cell,''),'reference':f'{p.relative_to(evidence)}#{sheet}!{cell}','source_kind':'historical_analytical_plate_map' if int(exp[3:])<7 else 'planned_layout'}

def expand(selector):
    if selector=='Entire plate': return WELLS
    found=[]
    for chunk in selector.split(','):
        chunk=chunk.strip()
        if re.fullmatch(r'[A-H]\d{1,2}',chunk): found.append(chunk)
        elif re.fullmatch(r'[A-H]\d{1,2}:[A-H]\d{1,2}',chunk):
            a,b=chunk.split(':')
            found.extend(f'{r}{c}' for r in 'ABCDEFGH' if a[0]<=r<=b[0] for c in range(int(a[1:]),int(b[1:])+1))
    return found
qclog=table('CeARS_PFAS_Master_Experiment_Record_and_Analysis_Plan.xlsx','QC_Exclusion_Log',3)
qcrefs=defaultdict(list)
for r in qclog:
    for w in expand(r['Well(s)']): qcrefs[(r['Experiment'],w)].append(r)

comparisons=[]; perwell=[]; history_conflicts=[]
alias={'accepted':'include','review_include':'review','review-include':'review'}
for k,rr in rawmap.items():
    d=draft.get(k,{}); m=master.get(k,{}); vv=variants[k]
    conditions={v['condition'] for v in vv if v['condition']}
    composition={a:{norm(v['composition_ppm'][a]) for v in vv if norm(v['composition_ppm'][a]) is not None} for a in AN}
    qcs={alias.get(v['qc'],v['qc']) for v in vv if v['qc']}
    if len(conditions)>1 or any(len(s)>1 for s in composition.values()) or len(qcs)>1:
        history_conflicts.append({'experiment_id':k[0],'well':k[1],'condition_versions':sorted(conditions),'composition_versions':{a:sorted(v) for a,v in composition.items()},'qc_versions':sorted(qcs)})
    flags=[]
    if d:
        if (d['spectrum_present_claim']=='Yes') != (rr['nonempty_points']>0): flags.append('PRESENCE_MISMATCH')
        if norm(d['spectrum_points_claim'])!=norm(rr['nonempty_points']): flags.append('POINT_COUNT_MISMATCH')
        if d['mapping_review_status']=='CONFLICT': flags.append('CHEMISTRY_CONFLICT')
        if d['qc_conflict_flag']!='NO': flags.append('QC_CONFLICT')
    else: flags.append('OUTSIDE_DRAFT_SCOPE')
    for a in AN:
        if d and norm(d['master_'+a+'_ppm'])!=norm(m[a+'_ppm']): flags.append('DRAFT_MASTER_VALUE_MISMATCH_'+a)
    if len(conditions)>1: flags.append('HISTORY_CONDITION_DIFFERENCE')
    if any(len(s)>1 for s in composition.values()): flags.append('HISTORY_COMPOSITION_DIFFERENCE')
    if len(qcs)>1: flags.append('HISTORY_QC_DIFFERENCE')
    perwell.append(dict(rr,condition_claim=d.get('condition_code_claim',''),draft_mapping_review_status=d.get('mapping_review_status','MISSING_DRAFT'),identity_status='UNRESOLVED_CONFLICT' if 'CHEMISTRY_CONFLICT' in flags else ('NOT_INDEPENDENTLY_VERIFIED' if d else 'INCOMPLETE_PILOT_DIAGNOSTIC_MAPPING'),master_composition_ppm=json.dumps({a:d.get('master_'+a+'_ppm','') for a in AN}),proposed_composition_ppm=json.dumps({a:d.get('proposed_'+a+'_ppm','') for a in AN}),resolved_label='',planned_or_analytical_layout_label=plans.get(k,{}).get('label',''),layout_source=plans.get(k,{}).get('reference',''),layout_source_kind=plans.get(k,{}).get('source_kind',''),reported_as_executed=d.get('physical_execution_evidence',''),historical_qc_status=d.get('master_qc_status',''),historical_qc_reason=d.get('master_qc_reason',''),historical_accepted_qc_references=json.dumps(qcrefs[k],ensure_ascii=False),master_partition=d.get('master_dataset_partition',''),master_role=d.get('master_primary_dataset_role',''),master_use_in_model=d.get('master_use_in_model',''),training_approval='NONE; existing assignments unchanged',draft_reference=d.get('_ref',''),uploaded_master_reference=m.get('_ref',''),historical_variants=json.dumps(vv,ensure_ascii=False),findings=';'.join(flags),unresolved_question=d.get('unresolved_question','Original pilot/diagnostic well preparation mapping incomplete; no labels inferred.')))
csvout('per_well_discrepancies.csv',perwell)
csvout('source_condition_counts.csv',[{'source':s,'experiment_id':e,'condition_claim':c,'rows':n} for s,records in sources.items() for (e,c),n in sorted(Counter((r['experiment_id'],r.get('condition_code','')) for r in records.values()).items())])
dump('historical_conflicts.json',history_conflicts)
dump('source_counts.json',{s:dict(Counter(k[0] for k in records)) for s,records in sources.items()})
csvout('condition_counts.csv',[{'experiment_id':e,'condition_claim':c,'draft_rows':n,'raw_populated_rows':sum(rawmap[key(r)]['nonempty_points']>0 for r in draft.values() if r['experiment_id']==e and r['condition_code_claim']==c)} for (e,c),n in sorted(Counter((r['experiment_id'],r['condition_code_claim']) for r in draft.values()).items())])
catalog=table(mastername,'CONDITION_CATALOG',1)
duplicates={c:[r for r in catalog if r['condition_code']==c] for c,n in Counter(r['condition_code'] for r in catalog).items() if n>1}
dump('catalog_duplicates.json',duplicates)
dump('reconciliation_checks.json',{'csv_xlsx_differences':csv_xlsx_diffs,'master_audit_shared_fields':shared,'master_audit_differences':lineage_diffs,'draft_status_counts':dict(Counter(r['mapping_review_status'] for r in draft.values())),'draft_evidence_class_counts':dict(Counter(r['identity_evidence_class'] for r in draft.values())),'finding_counts':dict(Counter(f for r in perwell for f in r['findings'].split(';') if f)),'source_reference_note':'Workbook row numbers and CSV record numbers include header; source values retained, no label resolution.'})
assert before=={p:sha(Path(p)) for p in before},'Input changed during reconciliation'
print(json.dumps({'raw':[{k:v for k,v in r.items() if k!='historical_hash_references'} for r in summary],'checks':json.loads((out/'reconciliation_checks.json').read_text()),'history_conflicts':history_conflicts},indent=2))
