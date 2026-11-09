"""Synthetic-only sequential experiment selection. No data readers or real models.

Selectors receive immutable prospective designs and acquisition metadata only.
Oracle outcomes and fixed holdout scores never enter the selector interface.
"""
from dataclasses import dataclass
import copy
import math
import random
from typing import Protocol


def _identifier(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Expected nonempty identifier')


def _batch(value):
    if not isinstance(value, str) or not value.startswith('synthetic-'):
        raise ValueError('Only explicitly synthetic batches are supported')


def _units(value, *, zero=False):
    if type(value) is not int or value < (0 if zero else 1):
        raise ValueError('Budget/cost must be exact integer synthetic units')


@dataclass(frozen=True)
class CandidateExperiment:
    group_id: str
    batch: str
    settings: tuple[tuple[str, str], ...]
    cost: int

    def __post_init__(self):
        _identifier(self.group_id)
        _batch(self.batch)
        _units(self.cost)
        if type(self.settings) is not tuple or not self.settings:
            raise ValueError('Immutable prospective factor-level settings required')
        keys = []
        for item in self.settings:
            if type(item) is not tuple or len(item) != 2:
                raise ValueError('Each setting must be an immutable key/value pair')
            key, value = item
            _identifier(key)
            _identifier(value)
            if any(word in key.lower() for word in (
                    'spectrum', 'feature', 'label', 'response', 'error',
                    'uncertainty', 'prediction', 'observed', 'measured')):
                raise ValueError('Observed/predictive inputs are not prospective settings')
            keys.append(key)
        if len(set(keys)) != len(keys):
            raise ValueError('Duplicate design factor')


@dataclass(frozen=True)
class Replicate:
    spectrum: tuple[float, ...]
    label: int

    def __post_init__(self):
        if (type(self.spectrum) is not tuple or not self.spectrum
                or any(type(v) not in (int, float) or not math.isfinite(v) for v in self.spectrum)):
            raise ValueError('Synthetic spectrum must be a finite immutable numeric tuple')
        if type(self.label) is not int or self.label not in (0, 1):
            raise ValueError('Synthetic binary label must be integer 0 or 1')


@dataclass(frozen=True)
class OutcomeGroup:
    group_id: str
    batch: str
    replicates: tuple[Replicate, ...]

    def __post_init__(self):
        _identifier(self.group_id)
        _batch(self.batch)
        if (type(self.replicates) is not tuple or not self.replicates
                or any(type(r) is not Replicate for r in self.replicates)):
            raise ValueError('Complete immutable synthetic replicate group required')
        if len({r.label for r in self.replicates}) != 1:
            raise ValueError('One synthetic condition must have a consistent binary label')
        if len({len(r.spectrum) for r in self.replicates}) != 1:
            raise ValueError('Inconsistent synthetic spectrum widths')


@dataclass(frozen=True)
class SyntheticScenario:
    designs: tuple[CandidateExperiment, ...]
    outcomes: tuple[OutcomeGroup, ...]
    initial: tuple[OutcomeGroup, ...]
    holdout: tuple[OutcomeGroup, ...]

    def __post_init__(self):
        for values, cls in ((self.designs, CandidateExperiment), (self.outcomes, OutcomeGroup),
                            (self.initial, OutcomeGroup), (self.holdout, OutcomeGroup)):
            if type(values) is not tuple or any(type(x) is not cls for x in values):
                raise ValueError('Scenario requires typed immutable synthetic tuples')
            if len({x.group_id for x in values}) != len(values):
                raise ValueError('Duplicate group ID')
        if not self.initial or not self.holdout:
            raise ValueError('Nonempty synthetic initial and fixed holdout groups required')
        design_map = {d.group_id: d for d in self.designs}
        if set(design_map) != {g.group_id for g in self.outcomes}:
            raise ValueError('Oracle must match exactly the candidate condition IDs')
        for g in self.outcomes:
            if g.batch != design_map[g.group_id].batch:
                raise ValueError('Candidate/oracle batch mismatch')
        all_groups = self.outcomes + self.initial + self.holdout
        if len({g.group_id for g in all_groups}) != len(all_groups):
            raise ValueError('Initial, acquisition and holdout preparations must be disjoint')
        if len({len(r.spectrum) for g in all_groups for r in g.replicates}) != 1:
            raise ValueError('Synthetic spectrum dimensions must agree')


class SyntheticOracle:
    """One-shot group revelation; passed only to engine, never to selector."""
    def __init__(self, designs, outcomes):
        if len({d.group_id for d in designs}) != len(designs):
            raise ValueError('Duplicate candidate group')
        self.__outcomes = {g.group_id: g for g in outcomes}
        if (len(self.__outcomes) != len(outcomes)
                or set(self.__outcomes) != {d.group_id for d in designs}):
            raise ValueError('Oracle/candidate group mismatch')
        self.__revealed = set()

    def reveal(self, group_id):
        if group_id not in self.__outcomes or group_id in self.__revealed:
            raise ValueError('Unknown or already revealed group')
        self.__revealed.add(group_id)
        return self.__outcomes[group_id]


@dataclass(frozen=True)
class BudgetState:
    total: int
    spent: int = 0

    def __post_init__(self):
        _units(self.total, zero=True)
        _units(self.spent, zero=True)
        if self.spent > self.total:
            raise ValueError('Budget exceeded')

    @property
    def remaining(self):
        return self.total - self.spent

    def spend(self, cost):
        _units(cost)
        return BudgetState(self.total, self.spent + cost)


class Selector(Protocol):
    name: str
    seed: int | None

    def choose(self, available_designs: tuple[CandidateExperiment, ...],
               observed_history: tuple[CandidateExperiment, ...], budget_state: BudgetState) -> str: ...


class RandomSelector:
    name = 'random'

    def __init__(self, seed):
        if type(seed) is not int:
            raise ValueError('Explicit integer random seed required')
        self.seed = seed
        self.__rng = random.Random(seed)

    def choose(self, available_designs, observed_history, budget_state):
        return self.__rng.choice(sorted(available_designs, key=lambda d: d.group_id)).group_id


class CoverageSelector:
    """Greedy nominal factor-level novelty; ID tie-break. No hidden outcomes."""
    name = 'coverage'
    seed = None

    def choose(self, available_designs, observed_history, budget_state):
        seen = {setting for d in observed_history for setting in d.settings}
        return min(available_designs, key=lambda d: (-len(set(d.settings) - seen), d.group_id)).group_id


class UncertaintySelector:
    name = 'uncertainty'
    seed = None

    def __init__(self, regime='none'):
        self.regime = regime

    def choose(self, available_designs, observed_history, budget_state):
        # A caller string is NOT a capability grant. Neither regime is approved.
        raise PermissionError('No approved budgeted screening or validated surrogate capability')


@dataclass(frozen=True)
class TrainingGroup:
    group_id: str
    batch: str
    replicates: tuple[Replicate, ...]
    sample_weights: tuple[float, ...]


def _training_view(groups):
    n = sum(len(g.replicates) for g in groups)
    return tuple(TrainingGroup(g.group_id, g.batch, g.replicates,
                 (n / (len(groups) * len(g.replicates)),) * len(g.replicates)) for g in groups)


class ModelAdapter(Protocol):
    def fit(self, groups: tuple[TrainingGroup, ...]): ...
    def predict(self, spectra: tuple[tuple[float, ...], ...]) -> tuple[int, ...]: ...


class SyntheticMeanModel:
    """Fake, spectrum-agnostic binary learner for exercising hooks, not a benchmark model."""
    def fit(self, groups):
        weight = sum(w for g in groups for w in g.sample_weights)
        mean = sum(r.label * w for g in groups for r, w in zip(g.replicates, g.sample_weights)) / weight
        self.__prediction = int(mean >= .5)

    def predict(self, spectra):
        return (self.__prediction,) * len(spectra)


class _Evaluator:
    def __init__(self, holdout):
        self.__holdout = holdout

    def accuracy(self, model):
        # Evaluate a clone: predict-time mutations cannot carry holdout data back
        # to the live training adapter. No metrics/predictions enter selector view.
        evaluation_model = copy.deepcopy(model)
        accuracies = []
        for group in self.__holdout:
            predicted = evaluation_model.predict(tuple(r.spectrum for r in group.replicates))
            if len(predicted) != len(group.replicates) or any(type(p) is not int or p not in (0, 1) for p in predicted):
                raise ValueError('Invalid synthetic model predictions')
            accuracies.append(sum(p == r.label for p, r in zip(predicted, group.replicates)) / len(predicted))
        return sum(accuracies) / len(accuracies)

    def balanced(self, model):
        from .nes_protocol import condition_binary_metrics
        evaluation_model = copy.deepcopy(model)
        predictions = tuple(evaluation_model.predict(tuple(r.spectrum for r in g.replicates))
                            for g in self.__holdout)
        return condition_binary_metrics(self.__holdout, predictions)


@dataclass(frozen=True)
class Action:
    group_id: str
    cost: int
    spent: int
    information: tuple[str, ...] = ('prospective_designs', 'acquisition_history', 'remaining_budget')


@dataclass(frozen=True)
class CurvePoint:
    acquired_conditions: int
    spent: int
    accuracy: float
    balanced_accuracy: float | None = None
    sensitivity: float | None = None
    specificity: float | None = None


@dataclass(frozen=True)
class RunResult:
    policy: str
    seed: int | None
    budget: int
    actions: tuple[Action, ...]
    curve: tuple[CurvePoint, ...]
    stop_reason: str
    data_kind: str = 'synthetic-only'


def run_selection(scenario, selector: Selector, budget, model: ModelAdapter, *, evaluation='accuracy'):
    if type(scenario) is not SyntheticScenario:
        raise ValueError('Only a validated synthetic scenario is supported')
    if evaluation not in ('accuracy', 'condition_balanced'):
        raise ValueError('Unknown synthetic evaluation mode')
    state = BudgetState(budget)
    oracle = SyntheticOracle(scenario.designs, scenario.outcomes)
    evaluator = _Evaluator(scenario.holdout)
    available = {d.group_id: d for d in scenario.designs}
    history = ()
    training = scenario.initial
    actions = []
    def checkpoint(k, spent):
        if evaluation == 'accuracy':
            return CurvePoint(k, spent, evaluator.accuracy(model))
        scores = evaluator.balanced(model)
        # Legacy accuracy remains explicitly condition-equal accuracy, not BA.
        p, n = scores['positive_conditions'], scores['negative_conditions']
        accuracy = (p*scores['sensitivity'] + n*scores['specificity'])/(p+n)
        return CurvePoint(k, spent, accuracy, scores['balanced_accuracy'],
                          scores['sensitivity'], scores['specificity'])
    model.fit(_training_view(training))
    curve = [checkpoint(0, 0)]
    while available:
        affordable = tuple(sorted((d for d in available.values() if d.cost <= state.remaining), key=lambda d: d.group_id))
        if not affordable:
            reason = 'budget_exhausted' if state.remaining == 0 else 'no_affordable_design'
            break
        chosen = selector.choose(affordable, history, state)
        if type(chosen) is not str or chosen not in {d.group_id for d in affordable}:
            raise ValueError('Selector must choose one unselected affordable condition')
        design = available[chosen]
        next_budget = state.spend(design.cost)
        # Only a valid action gets a one-shot reveal, whole-group training update
        # and one cost charge regardless of number of technical replicates.
        revealed = oracle.reveal(chosen)
        training = training + (revealed,)
        state = next_budget
        del available[chosen]
        history = history + (design,)
        actions.append(Action(chosen, design.cost, state.spent))
        model.fit(_training_view(training))
        curve.append(checkpoint(len(actions), state.spent))
    else:
        reason = 'pool_exhausted'
    return RunResult(selector.name, selector.seed, budget, tuple(actions), tuple(curve), reason)


def compare_selectors(scenario, budget, seed):
    """Fresh policies/adapters on identical immutable scenario and cost schedule.

    Curves are reported at actual cumulative budgets; variable-cost policies do
    not necessarily share interior cost checkpoints. No interpolation or tuning.
    """
    return {p.name: run_selection(scenario, p, budget, SyntheticMeanModel())
            for p in (RandomSelector(seed), CoverageSelector())}
