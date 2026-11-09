"""Optional pinned LR adapter. Fits synthetic groups only; lazy ML imports."""
from dataclasses import dataclass
from importlib.metadata import version, PackageNotFoundError
import math
from .selection import TrainingGroup, Replicate
from .nes_protocol import ARMS, feature_rows

PINS={'numpy':'2.2.6','scipy':'1.15.3','scikit-learn':'1.7.2','joblib':'1.5.2','threadpoolctl':'3.6.0'}
MODEL_CONFIG={'penalty':'l2','C':1.0,'class_weight':None,'solver':'lbfgs',
              'max_iter':5000,'random_state':0,'tol':1e-4,'fit_intercept':True,
              'warm_start':False}


def dependency_versions():
    try: versions={name:version(name) for name in PINS}
    except PackageNotFoundError as exc:
        raise RuntimeError('Install optional requirements/logistic.txt') from exc
    if versions!=PINS:
        raise RuntimeError('Optional dependency versions must match requirements/logistic.txt')
    return versions


@dataclass(frozen=True)
class FitRecord:
    fit_number: int
    group_ids: tuple[str,...]
    sample_count: int
    feature_width: int
    group_total_weights: tuple[float,...]
    scaler_mean: tuple[float,...]
    n_iter: int
    converged: bool


class LogisticAdapter:
    def __init__(self,arm='B'):
        if arm not in ARMS:raise ValueError('Expected fixed representation A/B/C/D')
        self.arm=arm
        self.fit_trace=()
        self.scaler_=None;self.classifier_=None

    def fit(self,groups):
        # Fail closed; a failed refit cannot leave an old usable estimator.
        self.scaler_=None;self.classifier_=None
        dependency_versions()
        import numpy as np
        if not groups or any(type(g) is not TrainingGroup for g in groups):
            raise ValueError('Synthetic grouped training view required')
        if len({g.group_id for g in groups})!=len(groups):raise ValueError('Duplicate training group')
        if any(not g.batch.startswith('synthetic-') or not g.replicates
               or any(type(r) is not Replicate for r in g.replicates) for g in groups):
            raise ValueError('Synthetic nonempty groups only')
        n=sum(len(g.replicates) for g in groups)
        for g in groups:
            expected=n/(len(groups)*len(g.replicates))
            if len(g.sample_weights)!=len(g.replicates) or any(
                    not math.isfinite(w) or not math.isclose(w,expected,rel_tol=1e-12,abs_tol=1e-12)
                    for w in g.sample_weights):
                raise ValueError('Expected recomputed condition-equal training sample weights')
            if len({r.label for r in g.replicates})!=1:raise ValueError('Contradictory group labels')
        spectra=tuple(r.spectrum for g in groups for r in g.replicates)
        x=np.asarray(feature_rows(spectra,self.arm),dtype=float)
        y=np.asarray([r.label for g in groups for r in g.replicates],dtype=int)
        if set(y.tolist())!={0,1}:raise ValueError('Both synthetic training classes required')
        w=np.asarray([v for g in groups for v in g.sample_weights],dtype=float)
        from ._logistic_core import fit_weighted_logistic
        scaler,classifier=fit_weighted_logistic(x,y,w)
        self.scaler_=scaler;self.classifier_=classifier
        self.fit_trace=self.fit_trace+(FitRecord(len(self.fit_trace)+1,tuple(g.group_id for g in groups),
            n,x.shape[1],tuple(sum(g.sample_weights) for g in groups),tuple(float(v) for v in scaler.mean_),
            int(max(classifier.n_iter_)),True),)

    def predict(self,spectra):
        if self.scaler_ is None or self.classifier_ is None:raise ValueError('Synthetic adapter not fitted')
        from threadpoolctl import threadpool_limits
        with threadpool_limits(limits=1):
            predictions=self.classifier_.predict(self.scaler_.transform(feature_rows(spectra,self.arm)))
        return tuple(int(p) for p in predictions)
