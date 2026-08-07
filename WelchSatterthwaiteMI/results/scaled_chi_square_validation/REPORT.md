# Scaled Chi-Squared Validation for the MI Variance Estimator

## Question

Across repeated multinomial samples, is the distribution of the plug-in
MI influence-variance estimator well represented by the scaled
chi-squared model used by expanded Welch-Satterthwaite?

## Design

Profile: `focused`. The experiment evaluated `128`
population components from `64` fixed
scenarios, using `10,000` independent tables to
estimate the oracle moments and another independent
`10,000` tables to evaluate each model. Population
and simulation seeds were fixed before the run.

Two comparisons were kept separate:

- **Oracle shape comparison:** chi-squared, normal, and lognormal models
  all receive the empirical mean and variance. Differences therefore
  measure distributional shape and tail fit rather than moment error.
- **Population first-order chi-squared:** uses population `V` and the derived
  `tau^2 / n`. This tests the complete theoretical approximation.

KS distance measures whole-distribution disagreement; lower is better.
Tail error is the absolute difference between the observed exceedance
rate and its target probability.

## Overall Results

| Model | Mean KS | Median KS | Tail error 0.05 | Tail error 0.01 | Oracle win rate |
| --- | --- | --- | --- | --- | --- |
| Oracle scaled chi-squared | 0.0199 | 0.0143 | 0.0045 | 0.0026 | 0.4219 |
| Oracle normal | 0.0196 | 0.0143 | 0.0054 | 0.0038 | 0.4688 |
| Oracle lognormal | 0.0291 | 0.0227 | 0.0062 | 0.0040 | 0.1094 |
| Population first-order chi-squared | 0.1622 | 0.0822 | 0.0765 | 0.0345 | NA |

## Results by Regime

| Regime | Components | Mean ratio | Variance ratio | Plug-in df ratio | Oracle chi2 KS | Chi2 win rate | IF chi2 KS | IF tail error 0.05 | IF tail error 0.01 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Well sampled | 16 | 1.0511 | 1.0199 | 0.9585 | 0.0166 | 0.5625 | 0.2172 | 0.0960 | 0.0360 |
| Moderate | 16 | 1.0442 | 0.9787 | 0.9546 | 0.0231 | 0.5000 | 0.2065 | 0.0963 | 0.0379 |
| Sparse and imbalanced | 16 | 1.0082 | 0.9649 | 0.9649 | 0.0188 | 0.3125 | 0.1488 | 0.0622 | 0.0215 |
| Highly skewed and sparse | 16 | 1.0000 | 1.0044 | 0.9946 | 0.0164 | 0.2500 | 0.0462 | 0.0128 | 0.0042 |
| Ultra-skewed and sparse | 16 | 0.9999 | 0.9874 | 1.0036 | 0.0173 | 0.2500 | 0.0786 | 0.0150 | 0.0044 |
| Widespread sparsity | 16 | 1.1826 | 0.9957 | 0.8522 | 0.0272 | 0.8125 | 0.3081 | 0.2042 | 0.1224 |
| Equal-MI shape mismatch | 16 | 1.0138 | 0.9783 | 0.9658 | 0.0236 | 0.4375 | 0.1437 | 0.0609 | 0.0260 |
| Extreme sample imbalance | 16 | 1.0025 | 0.9815 | 0.9881 | 0.0161 | 0.2500 | 0.1483 | 0.0648 | 0.0239 |
| All regimes | 128 | 1.0106 | 0.9871 | 0.9703 | 0.0199 | 0.4219 | 0.1622 | 0.0765 | 0.0345 |

## Results by Table Size

| Rows | Columns | Chi2 KS | Normal KS | Chi2 tail error 0.05 | Normal tail error 0.05 | Empirical skew | Chi2 skew | Plug-in df ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 2 | 0.0354 | 0.0273 | 0.0080 | 0.0075 | 0.1920 | 0.5663 | 0.9895 |
| 3 | 3 | 0.0209 | 0.0197 | 0.0056 | 0.0058 | 0.2095 | 0.4477 | 0.9695 |
| 5 | 5 | 0.0128 | 0.0176 | 0.0026 | 0.0044 | 0.1827 | 0.2527 | 0.9658 |
| 10 | 10 | 0.0105 | 0.0137 | 0.0017 | 0.0038 | 0.1071 | 0.1251 | 0.9568 |

## Interpretation

- The lowest average KS distance was obtained by **Oracle normal**.
- The oracle scaled chi-squared model was the best of the three
  moment-matched shape families in `42.2%` of components.
- Scaled chi-squared had lower average upper-tail error than normal:
  `0.0045` versus `0.0054` at 0.05 and
  `0.0026` versus `0.0038` at 0.01.
- The chi-squared model generally overstates skewness for small tables
  but tracks it more closely as the table dimension increases.
- The gap between oracle and population first-order chi-squared results
  separates shape error from errors in the first-order predicted moments.
- A good oracle fit but poor population first-order fit indicates that the
  chi-squared family is plausible but its plug-in moments need refinement.
- Poor oracle fit means that matching only mean and variance does not
  capture the finite-sample shape, regardless of moment estimation.
- The median plug-in component df was `0.970` times the
  empirical moment df, so the implemented plug-in df is substantially
  closer than the population first-order distribution fit alone suggests.

This audit evaluates the variance component in isolation. It does not
make the final Student reference exact because the MI contrast and its
estimated denominator can remain dependent.

## Output Map

- `component_results.csv`: every population-component diagnostic.
- `model_summary.csv`: overall comparison of candidate shapes and tails.
- `regime_summary.csv`: diagnostics aggregated by sampling regime.
- `shape_summary.csv`: diagnostics aggregated by table dimensions.
- `population_scenarios.csv`: fixed generating populations.
- `distribution_fit_summary.png`: visual shape and tail comparison.
- `run_metadata.json`: seeds, versions, settings, and runtime.
