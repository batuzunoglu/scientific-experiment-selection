"""Read-only, label-independent diagnostic run; explicitly limited to Exp3/Exp5.

Run from repository root with PYTHONPATH=.; exports diagnostics, never spectra.
Relative-area threshold is descriptive only and never changes branch eligibility.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import platform

from scientific_experiment_selection.inventory import hash_file
from scientific_experiment_selection.raw_spectra import read_raw
from scientific_experiment_selection.spectral import GRID, EPSILON, VERSION, representations

FILES = ('Exp3 Plt3.xlsx', 'Exp5 Plt5.xlsx')
CANCELLATION_DIAGNOSTIC = 1e-6


def trap(y):
    return math.fsum(a+b for a,b in zip(y,y[1:]))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-root',type=Path,required=True)
    parser.add_argument('--checksums',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve(); raw=args.raw_root.resolve()
    if output.exists() or output.is_relative_to(raw) or raw.is_relative_to(output):
        raise ValueError('Require fresh output directory outside raw source')
    old_notebook=Path('docs/RESEARCH_LAB_NOTEBOOK.md').read_bytes()
    code_paths=[Path('scientific_experiment_selection')/n for n in ('spectral.py','raw_spectra.py','inventory.py')]
    code_hashes={str(p):hash_file(p)[1] for p in code_paths}
    expected={}
    for line in args.checksums.read_text().splitlines():
        digest,name=line.split('  ',1)
        if Path(name).name in FILES: expected[Path(name).name]=digest
    rows=[];summary={'python':platform.python_version(),'version':VERSION,'epsilon':EPSILON,
        'relative_area_diagnostic_threshold':CANCELLATION_DIAGNOSTIC,
        'diagnostic_changes_eligibility':False,'code_sha256':code_hashes,'batches':{},
        'opened_raw_files':[],'labels_loaded':False,'randomness':'none'}
    before={}
    for filename in FILES:
        path=raw/filename; digest=hash_file(path)[1]
        if digest!=expected[filename]: raise ValueError('Raw hash mismatch: '+filename)
        before[str(path)]=digest; summary['opened_raw_files'].append(str(path))
        wells=read_raw(path); batch=filename.split()[0]
        bs={'populated':0,'empty_wells':[], 'success':dict.fromkeys('ABCD',0),
            'failures':{b:[] for b in 'ABCD'}}
        for well,record in wells.items():
            y=record['values']
            if y is None: bs['empty_wells'].append(well); continue
            bs['populated']+=1
            provenance={'source_sha256':digest,'source_file':filename,'well':well,
                        'raw_value_range':record['raw_value_range']}
            result=representations(GRID,y,provenance)
            assert result['provenance']==provenance
            assert result['A']['values']==y
            row={'batch':batch,'well':well,'source_sha256':digest}
            for b,n in [('A',176),('B',8),('C',176),('D',8)]:
                values=result[b]['values']; error=result[b]['error']
                if values is None: bs['failures'][b].append({'well':well,'reason':error})
                else:
                    assert len(values)==n and all(math.isfinite(v) for v in values)
                    bs['success'][b]+=1
                row[b+'_error']=error or ''
            band=y[15:116]; area=trap(band); absolute_area=trap([abs(v) for v in band])
            relative=abs(area)/absolute_area if absolute_area else 0.0
            row.update(area=area,absolute_area=absolute_area,relative_area=relative,
                       relative_cancellation_diagnostic=relative<CANCELLATION_DIAGNOSTIC,
                       negative_band_points=sum(v<0 for v in band),
                       raw_A518_abs=abs(y[84]),raw_moment_sum=math.fsum(band),
                       normalized_A518_abs=None,normalized_moment_sum=None,
                       normalized_area_error=None,raw_reconstruction_relative_error=None,
                       normalized_max_abs=None,scale2_C_max_error=None,scale2_D_max_error=None)
            if result['C']['values'] is not None:
                yn=result['C']['values']
                row.update(normalized_A518_abs=abs(yn[84]),normalized_moment_sum=math.fsum(yn[15:116]),
                    normalized_area_error=abs(trap(yn[15:116])-1),
                    raw_reconstruction_relative_error=max(abs(a*area-b) for a,b in zip(yn,y))/max(abs(v) for v in y),
                    normalized_max_abs=max(abs(v) for v in yn))
            # Positive rescaling probes arithmetic consistency, not concentration or a new physical measurement.
            twice=representations(GRID,[2*v for v in y],provenance)
            for b in 'CD':
                if result[b]['values'] is not None and twice[b]['values'] is not None:
                    row['scale2_'+b+'_max_error']=max(abs(v-w) for v,w in zip(result[b]['values'],twice[b]['values']))
            rows.append(row)
        summary['batches'][batch]=bs
    for path,digest in before.items(): assert hash_file(Path(path))[1]==digest
    for path,digest in code_hashes.items(): assert hash_file(Path(path))[1]==digest
    assert Path('docs/RESEARCH_LAB_NOTEBOOK.md').read_bytes()==old_notebook
    for batch,bs in summary['batches'].items():
        subset=[r for r in rows if r['batch']==batch]
        fields=[k for k,v in subset[0].items() if isinstance(v,(int,float)) and not isinstance(v,bool)]
        bs['ranges']={k:{'min':min(r[k] for r in subset if r[k] is not None),
                          'max':max(r[k] for r in subset if r[k] is not None)}
                      for k in fields if any(r[k] is not None for r in subset)}
        # Include optional diagnostics whose first row can be None.
        for k in ['normalized_A518_abs','normalized_moment_sum','normalized_area_error',
                  'raw_reconstruction_relative_error','normalized_max_abs','scale2_C_max_error','scale2_D_max_error']:
            vals=[r[k] for r in subset if r[k] is not None]
            bs['ranges'][k]={'min':min(vals),'max':max(vals)} if vals else None
        bs['negative_band_wells']=[r['well'] for r in subset if r['negative_band_points']]
        bs['relative_cancellation_wells']=[r['well'] for r in subset if r['relative_cancellation_diagnostic']]
    summary['source_sha256']=before;summary['raw_and_code_unchanged']=True
    output.mkdir(parents=True,exist_ok=False)
    with (output/'per_well_diagnostics.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__=='__main__': main()
