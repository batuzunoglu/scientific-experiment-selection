"""Explicit private-only inspection of the trusted saved Exp3/Exp5 pilot artifacts.

Never calls fit, predict, transform, or spectral functions. Does not open raw files
or reconstruct missing predictions/features. Not invoked by public plotting/CI.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import pickle

PRIVATE_ROOT=Path(__file__).resolve().parents[1]/'data'/'private'
CONDITIONS=('PFPA_5','PFOA_5','TFA_10','PFHxA_10','PFBA_20','PFNA_20')
STRATEGIES=(('random',7),('random',11),('random',19),('coverage',None))


class TrustedPilotUnpickler(pickle.Unpickler):
    """Resolve the original CLI class name; restore state without changing it.

    This is compatibility for user-trusted local files, not a safe unpickler for
    untrusted input. No estimator fit/predict/transform is performed.
    """
    def find_class(self,module,name):
        if module=='__main__' and name=='MeasuredLogisticAdapter':
            from scientific_experiment_selection.measured_pilot import MeasuredLogisticAdapter
            return MeasuredLogisticAdapter
        return super().find_class(module,name)


def private_output(output,private_root=PRIVATE_ROOT):
    output=Path(output).absolute();private_root=Path(private_root).absolute()
    if (not output.is_relative_to(private_root) or output==private_root
            or any(p.is_symlink() for p in (output,*output.parents))):
        raise ValueError('Diagnostics require local ignored private output')
    output.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    output.mkdir(mode=0o700)
    return output


def condition_accuracies(run):
    if len(run['curve'])!=13:raise ValueError('Missing saved checkpoints')
    values=[[] for _ in CONDITIONS]
    for k,point in enumerate(run['curve']):
        if point['acquired_conditions']!=k:raise ValueError('Saved checkpoint mismatch')
        predictions=point.get('evaluation_predictions')
        if not isinstance(predictions,list) or len(predictions)!=6:
            raise ValueError('Existing grouped predictions unavailable; no reconstruction')
        for i,(condition,pred) in enumerate(zip(CONDITIONS,predictions)):
            if len(pred)!=3 or any(type(v) is not int or v not in (0,1) for v in pred):
                raise ValueError('Incomplete or invalid saved evaluator predictions')
            label=int(condition=='TFA_10')
            values[i].append(sum(v==label for v in pred)/3)
    return values


def _validated_source_directory(source,private_root=None):
    """Accept only the exact private run directory, with no symlinked path components.

    The private root is trusted configuration; both it and the supplied source
    must resolve to their literal paths. Requiring the run to be its direct child
    also prevents traversal through an intermediate symlink.
    """
    source_path=Path(os.path.abspath(source))
    if private_root is None:private_root=PRIVATE_ROOT
    root_path=Path(private_root).absolute()
    try:
        resolved_root=root_path.resolve(strict=True)
        resolved_source=source_path.resolve(strict=True)
    except OSError as exc:
        raise ValueError('Only the existing private Exp3/Exp5 run is supported') from exc
    if root_path!=resolved_root:
        raise ValueError('Private root must not traverse symbolic links')
    if source_path!=resolved_source:
        raise ValueError('Source path must not traverse symbolic links')
    expected=root_path/'issue34-pilot-2026-11-09'
    if source_path!=expected or not source_path.is_dir():
        raise ValueError('Only the authorized private Exp3/Exp5 run is supported')
    return source_path


def inspect(source,output,*,trusted_pickles=False):
    if trusted_pickles is not True:raise ValueError('Explicit trusted-artifact inspection required')
    source=_validated_source_directory(source)
    summary_path=source/'summary.json'
    summary=json.loads(summary_path.read_text())
    if summary['status']!='completed-pending-scientific-review':raise ValueError('Incomplete saved run')
    by_key={(r['arm'],r['policy'],r['seed']):r for r in summary['runs']}
    expected={(a,p,s) for a in 'ABCD' for p,s in STRATEGIES}
    if len(summary['runs'])!=16 or set(by_key)!=expected:raise ValueError('Saved trajectory mismatch')
    # These exact filenames select only known artifacts; no model-directory crawl.
    files=[summary_path]+[source/f'{a}-{p}-{s}-k{k:02d}.pickle' for a in 'ABCD' for p,s in STRATEGIES for k in range(13)]
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    condition_scores={key:condition_accuracies(run) for key,run in by_key.items()}
    import numpy as np
    coefficients={}
    for a,p,s in sorted(expected,key=lambda key:(key[0],STRATEGIES.index(key[1:]))):
        values=[]
        for k in range(13):
            with (source/f'{a}-{p}-{s}-k{k:02d}.pickle').open('rb') as stream:
                model=TrustedPilotUnpickler(stream).load()  # User-authorized trusted local checkpoints only.
            width=8 if a in 'BD' else 176
            coef=model.classifier_.coef_
            if model.arm!=a or coef.shape!=(1,width) or not np.isfinite(coef).all():
                raise ValueError('Missing or invalid existing coefficients')
            values.append(float(np.linalg.norm(coef)))
        coefficients[(a,p,s)]=values
    # No stored matrix files are inferred from raw spectra or model state.
    matrix_files=[p for p in source.iterdir() if p.suffix in ('.npy','.npz','.csv','.parquet')]
    if matrix_files:raise ValueError('Additional matrix artifacts require explicit schema review')
    output=private_output(output)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from .plot_measured_pilot_results import plotting_style
    with plt.rc_context(plotting_style()):
        fig,axes=plt.subplots(4,4,figsize=(15,12),layout='constrained')
        for row,a in enumerate('ABCD'):
            for col,(policy,seed) in enumerate(STRATEGIES):
                ax=axes[row,col]
                image=ax.imshow(condition_scores[(a,policy,seed)],vmin=0,vmax=1,cmap='viridis',aspect='auto',interpolation='none')
                ax.set_title(f'{a} / {policy} / {seed}')
                ax.set_xticks(range(13));ax.set_yticks(range(6),CONDITIONS if col==0 else ['']*6)
                if row==3:ax.set_xlabel('Acquired conditions')
        fig.colorbar(image,ax=axes,label='Saved condition-level correctness fraction',shrink=.7)
        fig.suptitle('PRIVATE · Existing held-out condition predictions, no new predictions',fontsize=15)
        save_private(fig,output/'supplement_holdout_conditions')
        plt.close(fig)
        fig,axes=plt.subplots(2,2,figsize=(10,7.8),layout='constrained')
        colors=('#0072B2','#56B4E9','#009E73','#D55E00')
        for ax,a in zip(axes.flat,'ABCD'):
            for (policy,seed),color,marker in zip(STRATEGIES,colors,('o','D','^','x')):
                ax.plot(range(13),coefficients[(a,policy,seed)],linestyle='None',marker=marker,color=color,
                        label=f'{policy} {seed}')
            ax.set(title=f'{a} · existing standardized-feature coefficients',xlabel='Acquired conditions',ylabel='Coefficient L2 norm',xticks=range(13))
            ax.legend(fontsize=8);ax.grid(alpha=.2)
        fig.suptitle('PRIVATE · Saved coefficient norms (not comparable causal effects across arms)',fontsize=12)
        save_private(fig,output/'supplement_saved_coefficient_norms')
        plt.close(fig)
    if any(hashlib.sha256(p.read_bytes()).hexdigest()!=digest for p,digest in before.items()):
        raise ValueError('Original private input changed')
    report={'source_files_unchanged':True,'saved_grouped_prediction_checkpoints':208,'saved_coefficient_checkpoints':208,
        'saved_compact8_training_matrix_available':False,'saved_compact8_holdout_matrix_available':False,
        'matrix_diagnostics':'Not generated: no saved feature matrices; no reconstruction performed.',
        'new_fit_predict_or_transform_calls':0,'supplementary_figures_private_only':True}
    path=output/'availability.json';path.write_text(json.dumps(report,indent=2)+'\n');path.chmod(0o600)
    return report


def save_private(fig,stem):
    for ext in ('.png','.pdf'):
        path=stem.with_suffix(ext)
        fig.savefig(path,dpi=300,metadata={'Creator':'Private saved-artifact diagnostic','CreationDate':None,'ModDate':None} if ext=='.pdf' else None)
        path.chmod(0o600)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--inspect-trusted-pickles',action='store_true',required=True)
    args=parser.parse_args()
    try:report=inspect(args.source,args.output,trusted_pickles=args.inspect_trusted_pickles)
    except Exception:
        print('{"status":"unavailable_or_invalid","action":"document_missing_artifact_without_reconstruction"}')
        return 2
    print(json.dumps({'status':'inspected','prediction_checkpoints':report['saved_grouped_prediction_checkpoints'],
        'coefficient_checkpoints':report['saved_coefficient_checkpoints'],'saved_feature_matrices':0,'private_only':True}))
    return 0


if __name__=='__main__':raise SystemExit(main())
