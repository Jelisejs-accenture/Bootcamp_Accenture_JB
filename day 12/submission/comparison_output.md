# Day 12 - Local vs Cloud Comparison

Difference = cloud minus local; uncertainty = 2 x standard error.

| Metric | n | Local mean +/- 2SE | Cloud mean +/- 2SE | Paired difference +/- 2SE | Verdict |
|---|---:|---:|---:|---:|---|
| Faithfulness | 15 | 0.643 +/- 0.155 | 0.648 +/- 0.198 | 0.004 +/- 0.187 | no clear difference |
| Answer Relevancy | 15 | 0.958 +/- 0.051 | 0.900 +/- 0.145 | -0.058 +/- 0.140 | no clear difference |
| Contextual Relevancy | 15 | 0.438 +/- 0.134 | 0.458 +/- 0.139 | 0.020 +/- 0.089 | no clear difference |
| Contextual Recall | 15 | 0.805 +/- 0.182 | 0.748 +/- 0.205 | -0.057 +/- 0.136 | no clear difference |
| Contextual Precision | 15 | 0.852 +/- 0.103 | 0.883 +/- 0.072 | 0.031 +/- 0.104 | no clear difference |

## Generation statistics

| Measure | Local | Cloud |
|---|---:|---:|
| Median generation time | 41.66 s | 2.10 s |
| Slowest generation time | 69.86 s | 5.55 s |
| Average completion tokens | 208.47 | 118.80 |
| Empty answers | 0.00 | 0.00 |
| Non-stop finishes | 1.00 | 0.00 |

Paired question IDs: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

Completion tokens use provider-reported totals, including reasoning tokens where reported.
Non-stop finishes indicate possible truncation or other incomplete generations.
