"""Plot only the published aggregate JSON. No model/raw/private-data imports.

All computations retain Decimal input precision; only Matplotlib receives floats.
Random SD is sample SD (ddof=1), descriptive across the three fixed seeds, not CI.
"""
import argparse
import csv
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import platform

DATA_KIND='retrospective measured Exp3→Exp5 model results'
REPRESENTATIONS={'A':'Raw/Full','B':'Raw/Compact8','C':'Area/Full','D':'Area/Compact8'}
METRICS=('balanced_accuracy','sensitivity','specificity')
TITLES={'balanced_accuracy':'Balanced accuracy','sensitivity':'TFA sensitivity','specificity':'Non-TFA specificity'}
STEMS={'balanced_accuracy':'figure_1_balanced_accuracy','sensitivity':'figure_2_tfa_sensitivity','specificity':'figure_3_specificity'}
POINT_FIELDS={'acquired_conditions','spent_proxy_cost',*METRICS}
STRATEGIES=(('random',7),('random',11),('random',19),('doe',None))


def validate(data):
    if (set(data)!={'schema_version','data_kind','decimal_places','trajectories'}
            or data['schema_version']!=1 or data['data_kind']!=DATA_KIND):
        raise ValueError('Expected the public aggregate schema')
    if type(data['trajectories']) is not list or len(data['trajectories'])!=16:
        raise ValueError('Expected 16 trajectories')
    seen=set()
    for run in data['trajectories']:
        if set(run)!={'arm','representation','policy','seed','checkpoints'}:
            raise ValueError('Unexpected fields; private records are forbidden')
        arm=run['arm'];key=(arm,run['policy'],run['seed'])
        if (arm not in REPRESENTATIONS or run['representation']!=REPRESENTATIONS[arm]
                or (run['policy'],run['seed']) not in STRATEGIES or key in seen
                or (run['seed'] is not None and type(run['seed']) is not int)):
            raise ValueError('Invalid or duplicate public trajectory labels')
        seen.add(key)
        if len(run['checkpoints'])!=13:
            raise ValueError('Expected all 13 checkpoints')
        for k,point in enumerate(run['checkpoints']):
            if (set(point)!=POINT_FIELDS or type(point['acquired_conditions']) is not int
                    or type(point['spent_proxy_cost']) is not int
                    or point['acquired_conditions']!=k or point['spent_proxy_cost']!=k):
                raise ValueError('Unexpected fields or budget/checkpoint mismatch')
            for name in METRICS:
                value=point[name]
                if type(value) not in (int,Decimal) or not Decimal(value).is_finite() or not 0<=value<=1:
                    raise ValueError('Expected finite aggregate scores in [0,1]')
            if abs(Decimal(point['balanced_accuracy'])-(Decimal(point['sensitivity'])+Decimal(point['specificity']))/2)>Decimal('0.0000011'):
                raise ValueError('Balanced accuracy identity failed')
    return data


def load_data(source):
    return validate(json.loads(Path(source).read_text(),parse_float=Decimal))


def ordered_runs(data):
    return sorted(data['trajectories'],key=lambda r:(r['arm'],STRATEGIES.index((r['policy'],r['seed']))))


def mean_sd(values):
    with localcontext() as ctx:
        ctx.prec=50
        values=tuple(Decimal(v) for v in values)
        mean=sum(values)/len(values)
        sd=(sum((v-mean)**2 for v in values)/(len(values)-1)).sqrt()
        return +mean,+sd


def write_plot_csv(data,path):
    fields=('arm','representation','policy','seed','acquired_conditions','spent_proxy_cost',*METRICS)
    with Path(path).open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');writer.writeheader()
        for run in ordered_runs(data):
            for point in run['checkpoints']:
                writer.writerow({**{k:run[k] for k in fields[:4]},**point})


def summary_rows(data):
    with localcontext() as ctx:
        ctx.prec=50
        return _summary_rows(data)


def _summary_rows(data):
    rows=[]
    for arm in REPRESENTATIONS:
        random=[r for r in ordered_runs(data) if r['arm']==arm and r['policy']=='random']
        doe=next(r for r in data['trajectories'] if r['arm']==arm and r['policy']=='doe')
        for metric in METRICS:
            initial,initial_sd=mean_sd([r['checkpoints'][0][metric] for r in random])
            final,final_sd=mean_sd([r['checkpoints'][12][metric] for r in random])
            change,change_sd=mean_sd([Decimal(r['checkpoints'][12][metric])-Decimal(r['checkpoints'][0][metric]) for r in random])
            rows.append(dict(arm=arm,representation=REPRESENTATIONS[arm],metric=metric,policy='random_mean',
                n_seeds=3,initial=initial,initial_sd=initial_sd,final=final,final_sd=final_sd,change=change,change_sd=change_sd))
            start=Decimal(doe['checkpoints'][0][metric]);end=Decimal(doe['checkpoints'][12][metric])
            rows.append(dict(arm=arm,representation=REPRESENTATIONS[arm],metric=metric,policy='doe',
                n_seeds=0,initial=start,initial_sd='',final=end,final_sd='',change=end-start,change_sd=''))
    return rows


def write_summary(data,directory):
    rows=summary_rows(data)
    with (directory/'measured_pilot_summary.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    lines=['# Measured pilot endpoint summary','',
        'Source: published aggregate JSON, no model reruns. Random entries show mean ± sample SD',
        '(ddof=1, n=3); Δ is paired final minus initial for each seed. SD is descriptive, not a CI.',
        'DoE is deterministic (no seed SD). Source scores retain all JSON precision in plot-data CSV;',
        'full computed precision (50-digit Decimal arithmetic) is retained in the summary CSV.',
        'This display rounds to six decimal places. Endpoint equality does not imply equal intermediate curves.','',
        '| Arm | Metric | Random k=0 | Random k=12 | Random Δ | DoE k=0 | DoE k=12 | DoE Δ |',
        '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for i in range(0,len(rows),2):
        r,d=rows[i:i+2]
        cells=[f"{r[v]:.6f} ± {r[v+'_sd']:.6f}" for v in ('initial','final','change')]
        lines.append(f"| {r['arm']} | {r['metric']} | "+' | '.join(cells+[f"{d[v]:.6f}" for v in ('initial','final','change')])+' |')
    (directory/'measured_pilot_summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def plotting_style():
    return {'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,'axes.labelsize':11,
            'xtick.labelsize':9,'ytick.labelsize':10,'axes.spines.top':False,'axes.spines.right':False,
            'pdf.fonttype':42,'ps.fonttype':42,'savefig.dpi':300,'figure.facecolor':'white'}


def make_figure(data,metric):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    with plt.rc_context(plotting_style()):
        fig,axes=plt.subplots(2,2,figsize=(10,7.8),sharex=True,sharey=True)
        fig.subplots_adjust(left=.09,right=.98,bottom=.24,top=.87,hspace=.32,wspace=.12)
        colors=('#0072B2','#56B4E9','#009E73');markers=('o','D','^');sizes=(9,6.8,4.8)
        for panel,(arm,ax) in enumerate(zip(REPRESENTATIONS,axes.flat)):
            runs=[r for r in ordered_runs(data) if r['arm']==arm]
            random=runs[:3];doe=runs[3];x=list(range(13))
            for run,color,marker,size in zip(random,colors,markers,sizes):
                ax.plot(x,[float(p[metric]) for p in run['checkpoints']],linestyle='None',marker=marker,
                    color=color,markersize=size,markerfacecolor='none',markeredgewidth=1.1,clip_on=False,
                    label=f"Random {run['seed']}",zorder=3)
            stats=[mean_sd([r['checkpoints'][k][metric] for r in random]) for k in x]
            ax.errorbar(x,[float(m) for m,s in stats],yerr=[float(s) for m,s in stats],fmt='s',
                linestyle='None',color='#222222',markersize=3.2,capsize=2,elinewidth=1.1,
                label='Random mean ± sample SD (n=3)',zorder=4,clip_on=False)
            ax.plot(x,[float(p[metric]) for p in doe['checkpoints']],linestyle='None',marker='x',
                markersize=7,color='#D55E00',markeredgewidth=1.3,clip_on=False,label='DoE',zorder=5)
            ax.set(xlim=(-.35,12.35),ylim=(0,1),xticks=x,yticks=[0,.2,.4,.6,.8,1])
            ax.tick_params(axis='x',labelbottom=True)
            ax.grid(axis='y',alpha=.25,linewidth=.5);ax.set_axisbelow(True)
            ax.spines['bottom'].set_position(('outward',5));ax.spines['left'].set_position(('outward',3))
            ax.set_title(f"({chr(97+panel)})  {arm} · {REPRESENTATIONS[arm]}",loc='left',pad=12)
            if panel%2==0:ax.set_ylabel(TITLES[metric])
            if len({p[metric] for r in runs for p in r['checkpoints']})==1:
                value=runs[0]['checkpoints'][0][metric]
                ax.text(.5,.15 if value<Decimal('.6') else .75,
                        f'All trajectories coincide at {value:g}',transform=ax.transAxes,
                        ha='center',fontsize=10,color='#444444')
        fig.suptitle(TITLES[metric]+' · retrospective Exp3→Exp5 pilot',y=.985,fontsize=15)
        fig.supxlabel('Number of acquired experimental conditions (proxy cost units)',y=.15,fontsize=11)
        handles,labels=axes[0,0].get_legend_handles_labels()
        # Keep the same legend order in every figure, independent of Matplotlib container ordering.
        wanted=['Random 7','Random 11','Random 19','Random mean ± sample SD (n=3)','DoE']
        lookup=dict(zip(labels,handles))
        fig.legend([lookup[name] for name in wanted],wanted,loc='lower center',
                   bbox_to_anchor=(.5,.045),ncol=3,frameon=False,fontsize=10,columnspacing=1.8)
        fig.text(.5,.012,'Observed checkpoints only · SD describes seed variation, not a confidence interval',
                 ha='center',fontsize=9,color='#444444')
    return fig


def generate(source,figure_dir,result_dir):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    source=Path(source);before=source.read_bytes();data=load_data(source)
    figure_dir=Path(figure_dir);result_dir=Path(result_dir)
    outputs=[result_dir/name for name in ('measured_pilot_plot_data.csv','measured_pilot_summary.csv','measured_pilot_summary.md')]
    outputs += [figure_dir/(stem+ext) for stem in STEMS.values() for ext in ('.png','.pdf')]
    outputs.append(figure_dir/'manifest.json')
    if any(path.resolve()==source.resolve() or path.is_symlink() or
           (path.exists() and path.samefile(source)) for path in outputs):
        raise ValueError('Source/output alias forbidden')
    figure_dir.mkdir(parents=True,exist_ok=True);result_dir.mkdir(parents=True,exist_ok=True)
    write_plot_csv(data,outputs[0]);write_summary(data,result_dir)
    for metric,stem in STEMS.items():
        fig=make_figure(data,metric)
        with plt.rc_context(plotting_style()):
            fig.savefig(figure_dir/(stem+'.png'),dpi=300,metadata={'Software':'Matplotlib aggregate reporting'})
            fig.savefig(figure_dir/(stem+'.pdf'),metadata={'Title':TITLES[metric],
                'Creator':'Measured pilot aggregate reporting','CreationDate':None,'ModDate':None})
        plt.close(fig)
    if source.read_bytes()!=before:raise ValueError('Source JSON changed')
    import numpy
    manifest={'source':'docs/results/exp3-exp5-nes-2026-11-09-aggregate.json',
        'source_sha256':hashlib.sha256(before).hexdigest(),'trajectories':16,'checkpoints':208,'metric_values':624,
        'sd_ddof':1,'n_random_seeds':3,'interpolation':'none; markers at observed checkpoints only',
        'png_dpi':300,'figure_inches':[10,7.8],'python':platform.python_version(),
        'matplotlib':matplotlib.__version__,'numpy':numpy.__version__,
        'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs if p.name!='manifest.json'}}
    (figure_dir/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return {'trajectories':16,'checkpoints':208,'metric_values':624,'source_sha256':manifest['source_sha256']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path('docs/results/exp3-exp5-nes-2026-11-09-aggregate.json'))
    parser.add_argument('--figure-dir',type=Path,default=Path('docs/figures/measured_pilot'))
    parser.add_argument('--result-dir',type=Path,default=Path('docs/results'))
    args=parser.parse_args()
    try:result=generate(args.source,args.figure_dir,args.result_dir)
    except Exception:
        print('{"status":"failed","reason":"aggregate_reporting_validation"}')
        return 2
    print(json.dumps({'status':'generated',**result}))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
