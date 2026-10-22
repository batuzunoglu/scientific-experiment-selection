"""Extra documentary comparisons and explicit evidence separation for review."""
import runpy, sys
from pathlib import Path
g=runpy.run_path(str(Path(__file__).with_name('reconcile.py')))
globals().update({k:v for k,v in g.items() if not k.startswith('__')})
defs=table('CeARS_PFAS_Master_Experiment_Record_and_Analysis_Plan.xlsx','Condition_Definitions',3)
nd=table('PFCA_Mixture_Plate_Plan_RQ5_RQ8.xlsx','Plate Plan',17)
planchecks=[]
for k,d in draft.items():
    c=d['condition_code_claim']
    # Explicit header spelling; empty codes never join to missing fields.
    candidates=[r for r in defs if c and r.get('Code')==c] if k[0] in ('Exp3','Exp4','Exp5','Exp6') else [r for r in nd if c and r.get('ID')==c] if k[0]=='Exp7' else []
    for r in candidates:
        composition={a:r.get(a+'_ppm',r.get(a+' ppm',r.get(a,''))) for a in AN}
        planchecks.append({'experiment_id':k[0],'well':k[1],'condition_claim':c,'definition_reference':r['_ref'],'definition_record':json.dumps(r,ensure_ascii=False),'composition_disagreements':','.join(a for a,v in composition.items() if v!='' and norm(v)!=norm(d['master_'+a+'_ppm']))})
csvout('plan_composition_comparisons.csv',planchecks)
presence_checks=[]
for s,records in sources.items():
    for k,r in records.items():
        for field in ('spectrum_present','has_spectrum'):
            if field not in r or k not in rawmap: continue
            claimed=r[field].lower() in ('yes','true','1')
            if claimed != (rawmap[k]['nonempty_points']>0): presence_checks.append({'source':r['_ref'],'key':k,'claim':r[field]})
dump('additional_checks.json',{'historical_presence_disagreements':presence_checks,'plan_composition_rows_compared':len(planchecks),'plan_composition_disagreements':[r for r in planchecks if r['composition_disagreements']]})
issue='https://github.com/batuzunoglu/scientific-experiment-selection/issues/3#issuecomment-6342506517'
for r in perwell:
    k=key(r); exp,well=k
    r['operator_report_reference']=issue+' (2026-10-22 retrospective audit; original conversation not independently available)'
    r['spectral_qc_inference']='Historical claim only: '+r['historical_qc_reason'] if r['historical_qc_reason'] else 'No new spectral QC performed'
    pc=[p for p in planchecks if (p['experiment_id'],p['well'])==k]
    r['plan_composition_evidence']=json.dumps(pc,ensure_ascii=False)
    if any(p['composition_disagreements'] for p in pc): r['findings']+=';PLAN_VS_MASTER_MISSING_OR_DIFFERENT_CONCENTRATION'
    if exp=='Exp1': r['reported_as_executed']='2026-07-13 reported canceled pilot; limited UV coverage; incomplete physical mapping.'
    if exp=='Exp2': r['reported_as_executed']='2026-07-14 reported instrument failure and ~24-hour bench delay; diagnostic only.'
    if exp=='Exp3' and well in ('B4','B5','C9'): r['reported_as_executed']='2026-07-22 accepted retention for sensitivity review; no new hard exclusion.'
    if exp=='Exp7' and well in [f'{a}{i}' for a in 'GH' for i in range(1,13)]: r['reported_as_executed']='2026-09-21: G1:G6 actual blanks; remaining reserved G/H wells left empty; fresh solutions.'
    if exp=='Exp8' and (well.startswith('A') or well in [f'B{i}' for i in range(1,7)]): r['reported_as_executed']='2026-09-22: all 18 sample wells unchanged from bridge plan; operator report, not independent chemical validation.'
csvout('per_well_discrepancies.csv',perwell)
print('Additional:',len(planchecks),'plan-composition comparisons;',len(presence_checks),'historical presence discrepancies')
