# Power family: Sparse

P margins: `(0.1, 0.1)`; Q margins: `(0.05, 0.2)`.
Baseline I(P): `0.01` nats.

## Configuration-level rejection results

| configuration_id | experiment | n_p | n_q | effect_delta_i_q_minus_p | method_label | truth | nominal_rejection_rate_05 | size_adjusted_rejection_rate | valid_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1_sparse_di0p02_n200 | P1 | 200 | 200 | 0.02 | Expanded Welch | alternative | 0.064641 | 0.25315 | 0.99998 |
| P1_sparse_di0p02_n200 | P1 | 200 | 200 | 0.02 | Normal Wald | alternative | 0.09914 | 0.2359 | 1 |
| P1_sparse_di0p02_n200 | P1 | 200 | 200 | 0.02 | Simple Welch | alternative | 0.09682 | 0.2359 | 1 |
| P2_sparse_di0p02_np50_nq500 | P2 | 50 | 500 | 0.02 | Expanded Welch | alternative | 0.22301 | 0.2257 | 0.98972 |
| P2_sparse_di0p02_np50_nq500 | P2 | 50 | 500 | 0.02 | Normal Wald | alternative | 0.35954 | 0.21112 | 1 |
| P2_sparse_di0p02_np50_nq500 | P2 | 50 | 500 | 0.02 | Simple Welch | alternative | 0.35732 | 0.2109 | 1 |
