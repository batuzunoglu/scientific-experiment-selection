# Retrospective measured Exp3→Exp5 pilot results

**Evidence type: retrospective measured Exp3→Exp5 model results.** These are
evaluations of the completed local pilot on existing measured spectra, separate
from the earlier synthetic demo. No new wet-lab experiments or chemistry validation.

Publication authority: [researcher instruction on Draft PR #35](https://github.com/batuzunoglu/scientific-experiment-selection/pull/35#issuecomment-6753082959).
Only sanitized aggregate scores are published; private reports and artifacts remain unchanged.

## Frozen protocol and interpretation

- Initial training: 70 Exp3 wells / 18 conditions; acquisition: 35 Exp5 wells / 12 conditions; fixed evaluation: 18 Exp5 wells / 6 conditions.
- Historical labels are provisional analytical references. Exp5 was historically exposed; these are not pristine independent validation scores.
- One positive fixed evaluator condition, `TFA_10`, and five negative conditions. Technical well replicates do not create independent prepared conditions.
- Scoring averages correctness within each condition, then across conditions within each class. Balanced Accuracy = (TFA sensitivity + non-TFA specificity)/2.
- Each whole prepared-condition acquisition costs one **proxy** unit; acquired conditions and cumulative proxy cost both run from 0 to 12.
- Fixed condition-weighted StandardScaler and Logistic Regression L2/C=1/class_weight=None are refitted after each acquisition using training data only. No tuning or new fitting for this export.
- B ran first, then A/C/D. Each arm uses Random seeds 7, 11, 19 and deterministic nominal DoE (`coverage` in the runner). DoE novelty considers acquisition history only.
- Random and DoE are non-model-adaptive policies. No uncertainty/active-learning selector or prospective recommendation is demonstrated.
- These exposed-holdout curves do not establish arm/policy superiority, confidence or generalization. More acquisition need not improve this fixed evaluation score.

## Baseline and final (all policies agree at these endpoints)

| Arm | Representation | Budget / proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| --- | --- | ---: | ---: | ---: | ---: |
| B | Raw/Compact8 | 0 | 0.500000 | 0.000000 | 1.000000 |
| B | Raw/Compact8 | 12 | 0.500000 | 0.000000 | 1.000000 |
| A | Raw/Full | 0 | 0.933333 | 1.000000 | 0.866667 |
| A | Raw/Full | 12 | 0.833333 | 0.666667 | 1.000000 |
| C | Area/Full | 0 | 0.900000 | 1.000000 | 0.800000 |
| C | Area/Full | 12 | 0.600000 | 0.333333 | 0.866667 |
| D | Area/Compact8 | 0 | 0.500000 | 0.000000 | 1.000000 |
| D | Area/Compact8 | 12 | 0.500000 | 0.000000 | 1.000000 |

## Complete trajectories

All 16 predeclared trajectories and all 13 checkpoints follow, including unfavorable outcomes.
Scores are rounded to six decimal places, matching the private original aggregate report.
JSON has the same rounded values; rounding may cause at most 0.000001 BA arithmetic difference.
[Machine-readable aggregate JSON](results/exp3-exp5-nes-2026-11-09-aggregate.json).

### B — Raw/Compact8 — Random — seed 7

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### B — Raw/Compact8 — Random — seed 11

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### B — Raw/Compact8 — Random — seed 19

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### B — Raw/Compact8 — DoE / nominal coverage — seed none (deterministic)

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### A — Raw/Full — Random — seed 7

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.933333 | 1.000000 | 0.866667 |
| 1 | 1 | 0.966667 | 1.000000 | 0.933333 |
| 2 | 2 | 0.833333 | 0.666667 | 1.000000 |
| 3 | 3 | 0.833333 | 0.666667 | 1.000000 |
| 4 | 4 | 0.833333 | 0.666667 | 1.000000 |
| 5 | 5 | 0.833333 | 0.666667 | 1.000000 |
| 6 | 6 | 0.933333 | 1.000000 | 0.866667 |
| 7 | 7 | 0.766667 | 0.666667 | 0.866667 |
| 8 | 8 | 0.766667 | 0.666667 | 0.866667 |
| 9 | 9 | 0.766667 | 0.666667 | 0.866667 |
| 10 | 10 | 0.766667 | 0.666667 | 0.866667 |
| 11 | 11 | 0.833333 | 0.666667 | 1.000000 |
| 12 | 12 | 0.833333 | 0.666667 | 1.000000 |

### A — Raw/Full — Random — seed 11

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.933333 | 1.000000 | 0.866667 |
| 1 | 1 | 0.933333 | 1.000000 | 0.866667 |
| 2 | 2 | 0.766667 | 0.666667 | 0.866667 |
| 3 | 3 | 0.766667 | 0.666667 | 0.866667 |
| 4 | 4 | 0.766667 | 0.666667 | 0.866667 |
| 5 | 5 | 0.766667 | 0.666667 | 0.866667 |
| 6 | 6 | 0.766667 | 0.666667 | 0.866667 |
| 7 | 7 | 0.766667 | 0.666667 | 0.866667 |
| 8 | 8 | 0.833333 | 0.666667 | 1.000000 |
| 9 | 9 | 0.833333 | 0.666667 | 1.000000 |
| 10 | 10 | 0.833333 | 0.666667 | 1.000000 |
| 11 | 11 | 0.766667 | 0.666667 | 0.866667 |
| 12 | 12 | 0.833333 | 0.666667 | 1.000000 |

### A — Raw/Full — Random — seed 19

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.933333 | 1.000000 | 0.866667 |
| 1 | 1 | 0.933333 | 1.000000 | 0.866667 |
| 2 | 2 | 0.933333 | 1.000000 | 0.866667 |
| 3 | 3 | 0.766667 | 0.666667 | 0.866667 |
| 4 | 4 | 0.833333 | 0.666667 | 1.000000 |
| 5 | 5 | 0.833333 | 0.666667 | 1.000000 |
| 6 | 6 | 0.833333 | 0.666667 | 1.000000 |
| 7 | 7 | 0.833333 | 0.666667 | 1.000000 |
| 8 | 8 | 0.833333 | 0.666667 | 1.000000 |
| 9 | 9 | 0.833333 | 0.666667 | 1.000000 |
| 10 | 10 | 0.833333 | 0.666667 | 1.000000 |
| 11 | 11 | 0.833333 | 0.666667 | 1.000000 |
| 12 | 12 | 0.833333 | 0.666667 | 1.000000 |

### A — Raw/Full — DoE / nominal coverage — seed none (deterministic)

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.933333 | 1.000000 | 0.866667 |
| 1 | 1 | 0.933333 | 1.000000 | 0.866667 |
| 2 | 2 | 0.833333 | 0.666667 | 1.000000 |
| 3 | 3 | 0.833333 | 0.666667 | 1.000000 |
| 4 | 4 | 0.833333 | 0.666667 | 1.000000 |
| 5 | 5 | 0.833333 | 0.666667 | 1.000000 |
| 6 | 6 | 0.833333 | 0.666667 | 1.000000 |
| 7 | 7 | 0.833333 | 0.666667 | 1.000000 |
| 8 | 8 | 0.833333 | 0.666667 | 1.000000 |
| 9 | 9 | 0.833333 | 0.666667 | 1.000000 |
| 10 | 10 | 0.833333 | 0.666667 | 1.000000 |
| 11 | 11 | 0.833333 | 0.666667 | 1.000000 |
| 12 | 12 | 0.833333 | 0.666667 | 1.000000 |

### C — Area/Full — Random — seed 7

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.900000 | 1.000000 | 0.800000 |
| 1 | 1 | 0.900000 | 1.000000 | 0.800000 |
| 2 | 2 | 0.600000 | 0.333333 | 0.866667 |
| 3 | 3 | 0.433333 | 0.000000 | 0.866667 |
| 4 | 4 | 0.433333 | 0.000000 | 0.866667 |
| 5 | 5 | 0.466667 | 0.000000 | 0.933333 |
| 6 | 6 | 0.766667 | 0.666667 | 0.866667 |
| 7 | 7 | 0.600000 | 0.333333 | 0.866667 |
| 8 | 8 | 0.600000 | 0.333333 | 0.866667 |
| 9 | 9 | 0.600000 | 0.333333 | 0.866667 |
| 10 | 10 | 0.766667 | 0.666667 | 0.866667 |
| 11 | 11 | 0.600000 | 0.333333 | 0.866667 |
| 12 | 12 | 0.600000 | 0.333333 | 0.866667 |

### C — Area/Full — Random — seed 11

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.900000 | 1.000000 | 0.800000 |
| 1 | 1 | 0.900000 | 1.000000 | 0.800000 |
| 2 | 2 | 0.733333 | 0.666667 | 0.800000 |
| 3 | 3 | 0.733333 | 0.666667 | 0.800000 |
| 4 | 4 | 0.900000 | 1.000000 | 0.800000 |
| 5 | 5 | 0.766667 | 0.666667 | 0.866667 |
| 6 | 6 | 0.766667 | 0.666667 | 0.866667 |
| 7 | 7 | 0.766667 | 0.666667 | 0.866667 |
| 8 | 8 | 0.766667 | 0.666667 | 0.866667 |
| 9 | 9 | 0.633333 | 0.333333 | 0.933333 |
| 10 | 10 | 0.633333 | 0.333333 | 0.933333 |
| 11 | 11 | 0.766667 | 0.666667 | 0.866667 |
| 12 | 12 | 0.600000 | 0.333333 | 0.866667 |

### C — Area/Full — Random — seed 19

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.900000 | 1.000000 | 0.800000 |
| 1 | 1 | 0.900000 | 1.000000 | 0.800000 |
| 2 | 2 | 0.900000 | 1.000000 | 0.800000 |
| 3 | 3 | 0.900000 | 1.000000 | 0.800000 |
| 4 | 4 | 0.600000 | 0.333333 | 0.866667 |
| 5 | 5 | 0.600000 | 0.333333 | 0.866667 |
| 6 | 6 | 0.600000 | 0.333333 | 0.866667 |
| 7 | 7 | 0.600000 | 0.333333 | 0.866667 |
| 8 | 8 | 0.766667 | 0.666667 | 0.866667 |
| 9 | 9 | 0.766667 | 0.666667 | 0.866667 |
| 10 | 10 | 0.600000 | 0.333333 | 0.866667 |
| 11 | 11 | 0.600000 | 0.333333 | 0.866667 |
| 12 | 12 | 0.600000 | 0.333333 | 0.866667 |

### C — Area/Full — DoE / nominal coverage — seed none (deterministic)

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.900000 | 1.000000 | 0.800000 |
| 1 | 1 | 0.900000 | 1.000000 | 0.800000 |
| 2 | 2 | 0.433333 | 0.000000 | 0.866667 |
| 3 | 3 | 0.433333 | 0.000000 | 0.866667 |
| 4 | 4 | 0.433333 | 0.000000 | 0.866667 |
| 5 | 5 | 0.433333 | 0.000000 | 0.866667 |
| 6 | 6 | 0.633333 | 0.333333 | 0.933333 |
| 7 | 7 | 0.633333 | 0.333333 | 0.933333 |
| 8 | 8 | 0.633333 | 0.333333 | 0.933333 |
| 9 | 9 | 0.633333 | 0.333333 | 0.933333 |
| 10 | 10 | 0.633333 | 0.333333 | 0.933333 |
| 11 | 11 | 0.633333 | 0.333333 | 0.933333 |
| 12 | 12 | 0.600000 | 0.333333 | 0.866667 |

### D — Area/Compact8 — Random — seed 7

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### D — Area/Compact8 — Random — seed 11

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### D — Area/Compact8 — Random — seed 19

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

### D — Area/Compact8 — DoE / nominal coverage — seed none (deterministic)

| Acquired conditions | Spent proxy cost | Balanced Accuracy | Sensitivity | Specificity |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.500000 | 0.000000 | 1.000000 |
| 1 | 1 | 0.500000 | 0.000000 | 1.000000 |
| 2 | 2 | 0.500000 | 0.000000 | 1.000000 |
| 3 | 3 | 0.500000 | 0.000000 | 1.000000 |
| 4 | 4 | 0.500000 | 0.000000 | 1.000000 |
| 5 | 5 | 0.500000 | 0.000000 | 1.000000 |
| 6 | 6 | 0.500000 | 0.000000 | 1.000000 |
| 7 | 7 | 0.500000 | 0.000000 | 1.000000 |
| 8 | 8 | 0.500000 | 0.000000 | 1.000000 |
| 9 | 9 | 0.500000 | 0.000000 | 1.000000 |
| 10 | 10 | 0.500000 | 0.000000 | 1.000000 |
| 11 | 11 | 0.500000 | 0.000000 | 1.000000 |
| 12 | 12 | 0.500000 | 0.000000 | 1.000000 |

## Export verification and reproduction

The deterministic exporter reads only the existing private aggregate REVIEW.md and completed
run summary. It constructs an allowlisted output, compares every published score against
both originals at six decimals, and rejects missing/duplicate trajectories, invalid scores,
incomplete checkpoints, wrong costs, BA arithmetic or baseline/final inconsistencies.
No private prose, paths, source hashes, well labels, predictions, spectra, features or models
are copied. Selected-condition sequences are intentionally omitted as unnecessary here.

Configure input variables locally; their values are never printed:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m scientific_experiment_selection.pilot_results_export \
  --review "$PRIVATE_REVIEW" --summary "$PRIVATE_SUMMARY" \
  --markdown docs/MEASURED_PILOT_RESULTS.md \
  --json docs/results/exp3-exp5-nes-2026-11-09-aggregate.json
# Repeat the same command with --check to verify without writing.
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
git diff --check
```

Synthetic exporter tests use fabricated scores and privacy canaries, never these measured
values or private sources. Public CI tests code, not the original private measured run.
See [pilot methodology](MEASURED_PILOT.md) and appended Notebook Entry 035 for execution
and verification notes. Numerical scientific review remains pending; keep PR #35 Draft.
