# Measured pilot endpoint summary

Source: published aggregate JSON, no model reruns. Random entries show mean ± sample SD
(ddof=1, n=3); Δ is paired final minus initial for each seed. SD is descriptive, not a CI.
DoE is deterministic (no seed SD). Source scores retain all JSON precision in plot-data CSV;
full computed precision (50-digit Decimal arithmetic) is retained in the summary CSV.
This display rounds to six decimal places. Endpoint equality does not imply equal intermediate curves.

| Arm | Metric | Random k=0 | Random k=12 | Random Δ | DoE k=0 | DoE k=12 | DoE Δ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | balanced_accuracy | 0.933333 ± 0.000000 | 0.833333 ± 0.000000 | -0.100000 ± 0.000000 | 0.933333 | 0.833333 | -0.100000 |
| A | sensitivity | 1.000000 ± 0.000000 | 0.666667 ± 0.000000 | -0.333333 ± 0.000000 | 1.000000 | 0.666667 | -0.333333 |
| A | specificity | 0.866667 ± 0.000000 | 1.000000 ± 0.000000 | 0.133333 ± 0.000000 | 0.866667 | 1.000000 | 0.133333 |
| B | balanced_accuracy | 0.500000 ± 0.000000 | 0.500000 ± 0.000000 | 0.000000 ± 0.000000 | 0.500000 | 0.500000 | 0.000000 |
| B | sensitivity | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| B | specificity | 1.000000 ± 0.000000 | 1.000000 ± 0.000000 | 0.000000 ± 0.000000 | 1.000000 | 1.000000 | 0.000000 |
| C | balanced_accuracy | 0.900000 ± 0.000000 | 0.600000 ± 0.000000 | -0.300000 ± 0.000000 | 0.900000 | 0.600000 | -0.300000 |
| C | sensitivity | 1.000000 ± 0.000000 | 0.333333 ± 0.000000 | -0.666667 ± 0.000000 | 1.000000 | 0.333333 | -0.666667 |
| C | specificity | 0.800000 ± 0.000000 | 0.866667 ± 0.000000 | 0.066667 ± 0.000000 | 0.800000 | 0.866667 | 0.066667 |
| D | balanced_accuracy | 0.500000 ± 0.000000 | 0.500000 ± 0.000000 | 0.000000 ± 0.000000 | 0.500000 | 0.500000 | 0.000000 |
| D | sensitivity | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 ± 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| D | specificity | 1.000000 ± 0.000000 | 1.000000 ± 0.000000 | 0.000000 ± 0.000000 | 1.000000 | 1.000000 | 0.000000 |
