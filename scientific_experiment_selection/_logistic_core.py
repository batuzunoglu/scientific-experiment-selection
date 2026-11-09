"""Shared numeric fit only; callers enforce their distinct data/authority contracts."""
import warnings


def fit_weighted_logistic(x, y, weights):
    from .logistic import dependency_versions, MODEL_CONFIG
    dependency_versions()
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.exceptions import ConvergenceWarning
    from threadpoolctl import threadpool_limits
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=int);weights=np.asarray(weights,dtype=float)
    if (x.ndim!=2 or not len(x) or len(y)!=len(x) or len(weights)!=len(x)
            or set(y.tolist())!={0,1} or not np.isfinite(x).all()
            or not np.isfinite(weights).all() or not (weights>0).all()):
        raise ValueError('Invalid weighted binary training arrays')
    scaler=StandardScaler(with_mean=True,with_std=True)
    classifier=LogisticRegression(**MODEL_CONFIG)
    with threadpool_limits(limits=1),warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always',ConvergenceWarning)
        scaler.fit(x,sample_weight=weights)
        classifier.fit(scaler.transform(x),y,sample_weight=weights)
    if any(issubclass(item.category,ConvergenceWarning) for item in caught):
        raise RuntimeError('Logistic Regression did not converge; stop without tuning/drop')
    if not (np.isfinite(scaler.mean_).all() and np.isfinite(scaler.scale_).all()
            and np.isfinite(classifier.coef_).all() and np.isfinite(classifier.intercept_).all()):
        raise RuntimeError('Nonfinite fitted state')
    return scaler,classifier
