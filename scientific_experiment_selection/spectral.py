"""Versioned per-spectrum representations; no labels, fitted reference or ML.

Numerical conventions and conservative validity limits: docs/PHASE_A_REVIEW.md.
"""
import copy
import math

GRID = tuple(range(350, 701, 2))
VERSION = 'phase-a-v1'
EPSILON = 1e-12
COMPACT8_NAMES = ('A420', 'A518', 'A420_over_A518', 'centroid_380_580',
                  'spread_380_580', 'absolute_derivative_area_380_580',
                  'derivative_450', 'slope_440_480')


def validate(wavelengths, intensities):
    if tuple(wavelengths) != GRID:
        raise ValueError('Expected exact 176-channel 350:2:700 nm grid')
    if len(intensities) != len(GRID):
        raise ValueError('Expected 176 intensities')
    try:
        y = [float(v) for v in intensities]
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('Intensities must be finite numbers') from exc
    if not all(math.isfinite(v) for v in y):
        raise ValueError('Intensities must be finite numbers')
    return y


def _epsilon(epsilon):
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError('epsilon must be finite and positive')


def _trap(y):
    # Fixed 2 nm spacing: each trapezoid is y[i] + y[i+1].
    return math.fsum(a + b for a, b in zip(y, y[1:]))


def area_factor(wavelengths, intensities, epsilon=EPSILON):
    _epsilon(epsilon)
    y = validate(wavelengths, intensities)
    area = _trap(y[15:116])
    if not math.isfinite(area) or area <= epsilon:
        raise ValueError('Nonpositive, near-zero or nonfinite 380–580 nm area')
    return area


def sg_derivative(wavelengths, intensities):
    """SG(15, 2, deriv=1, delta=2); polynomial-interpolated boundary windows.

    Symmetric quadratic normal equations give fixed linear filter coefficients;
    first/last seven outputs use the first/last complete 15-point polynomial.
    This is deterministic local signal processing, not a learned ML transform.
    """
    y = validate(wavelengths, intensities)
    t = tuple(2*j for j in range(-7, 8))
    s2 = sum(v*v for v in t)
    s4 = sum(v**4 for v in t)
    result = []
    for i in range(176):
        center = min(max(i, 7), 168)
        window = y[center-7:center+8]
        b = math.fsum(v*z for v, z in zip(t, window)) / s2
        c = (math.fsum(v*v*z for v, z in zip(t, window))
             - s2*math.fsum(window)/15) / (s4-s2*s2/15)
        result.append(b + 2*c*(2*(i-center)))
    if not all(math.isfinite(v) for v in result):
        raise ValueError('Nonfinite derivative')
    return result


def compact8(wavelengths, intensities, epsilon=EPSILON):
    _epsilon(epsilon)
    y = validate(wavelengths, intensities)
    band = y[15:116]
    if any(v < 0 for v in band):
        raise ValueError('Compact8 moments invalid for negative weights in 380–580 nm')
    denominator = math.fsum(band)
    if not math.isfinite(denominator) or denominator <= epsilon:
        raise ValueError('Nonpositive or near-zero centroid denominator')
    if abs(y[84]) <= epsilon:
        raise ValueError('Near-zero A518 ratio denominator')
    weights = [v/denominator for v in band]
    center = math.fsum(x*w for x, w in zip(GRID[15:116], weights))
    variance = math.fsum(w*(x-center)**2 for x,w in zip(GRID[15:116], weights))
    derivative = sg_derivative(GRID,y)
    slope = math.fsum((x-460)*v for x,v in zip(GRID[45:66],y[45:66])) / sum(
        (x-460)**2 for x in GRID[45:66])
    features = [y[35],y[84],y[35]/y[84],center,math.sqrt(variance),
                _trap([abs(v) for v in derivative[15:116]]),derivative[50],slope]
    if not all(math.isfinite(v) for v in features):
        raise ValueError('Nonfinite Compact8 feature')
    return features


def representations(wavelengths, intensities, provenance, epsilon=EPSILON):
    """Return independent branch results/errors and an unchanged provenance copy.

    Metadata is carried only; it never enters feature computation. A failed
    derived branch does not drop a well or erase the valid raw control.
    """
    _epsilon(epsilon)
    y = validate(wavelengths,intensities)
    out = {'version': VERSION, 'epsilon': epsilon, 'provenance': copy.deepcopy(provenance),
           'A': {'values': list(y), 'error': None}, 'area_factor': None}

    def attempt(key, function):
        try:
            values = function()
            if not all(math.isfinite(v) for v in values):
                raise ValueError('Nonfinite transformed values')
            out[key] = {'values': values, 'error': None}
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            out[key] = {'values': None, 'error': str(exc)}

    attempt('B',lambda: compact8(GRID,y,epsilon))
    try:
        out['area_factor'] = area_factor(GRID,y,epsilon)
    except (ValueError, OverflowError) as exc:
        for key in 'CD': out[key] = {'values': None, 'error': str(exc)}
    else:
        normalized = [v/out['area_factor'] for v in y]
        attempt('C',lambda: normalized)
        attempt('D',lambda: compact8(GRID,normalized,epsilon))
    return out
