# Custom Welch Decision Audit

## Question

Does the current rule, Expanded Welch at sample-size ratios of at
least 4 and normal Wald otherwise, generalize when population shape,
sparsity, ratio, and allocation direction are crossed rather than
confounded?

## Design

The audit used `3,000` null replicates for each
of `2,808` allocation configurations. It crossed
the same equal-MI population pair with ratios 1, 2, 3, 4, 6, 10, and
20, assigning the smaller sample to both P and Q. Six table shapes and
all nine regimes were included. A development cohort and a separately
generated holdout cohort used different population-generation seeds.

All routing rules fall back to normal Wald when Expanded Welch is
undefined, except the explicitly labelled no-fallback baseline. The
selection score averages relative FPR error at alpha 0.05 and 0.01,
giving the two levels equal weight.

## Main Results

| Cohort | Decision rule | MAE 0.05 | MAE 0.01 | P90 error 0.05 | Valid rate | Expanded route | Relative-error score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| development | Always Normal Wald | 0.03818 | 0.02492 | 0.08057 | 0.99930 | 0.00000 | 1.62761 |
| development | Always Expanded Welch | 0.02696 | 0.01481 | 0.03646 | 0.98826 | 1.00000 | 1.01012 |
| development | Expanded with Wald fallback | 0.03177 | 0.01937 | 0.04523 | 0.99930 | 0.98858 | 1.28633 |
| development | Expanded if ratio >= 2 | 0.03167 | 0.01937 | 0.04523 | 0.99930 | 0.91289 | 1.28522 |
| development | Expanded if ratio >= 3 | 0.03199 | 0.01963 | 0.05203 | 0.99930 | 0.76093 | 1.30140 |
| development | Expanded if ratio >= 4 | 0.03269 | 0.02019 | 0.05473 | 0.99930 | 0.60882 | 1.33632 |
| development | Expanded if ratio >= 6 | 0.03367 | 0.02097 | 0.05990 | 0.99930 | 0.45665 | 1.38538 |
| development | Expanded if ratio >= 10 | 0.03496 | 0.02205 | 0.06533 | 0.99930 | 0.30443 | 1.45194 |
| development | Ratio >= 4 and minimum margin >= 2 | 0.03614 | 0.02341 | 0.07860 | 0.99930 | 0.47000 | 1.53171 |
| development | Ratio >= 4 and minimum margin >= 5 | 0.03699 | 0.02392 | 0.08057 | 0.99930 | 0.41938 | 1.56576 |
| development | Ratio >= 4 and smaller-sample share >= 0.50 | 0.03313 | 0.02079 | 0.05707 | 0.99930 | 0.60612 | 1.37065 |
| development | Ratio >= 4 and smaller-sample share >= 0.60 | 0.03336 | 0.02112 | 0.05857 | 0.99930 | 0.60387 | 1.38961 |
| development | Ratio >= 4, minimum margin >= 2, and smaller-sample share >= 0.50 | 0.03633 | 0.02360 | 0.07947 | 0.99930 | 0.46923 | 1.54327 |
| holdout | Always Normal Wald | 0.04055 | 0.02805 | 0.07807 | 0.99916 | 0.00000 | 1.80808 |
| holdout | Always Expanded Welch | 0.03038 | 0.01897 | 0.03832 | 0.98946 | 1.00000 | 1.25216 |
| holdout | Expanded with Wald fallback | 0.03392 | 0.02230 | 0.04233 | 0.99916 | 0.98980 | 1.45426 |
| holdout | Expanded if ratio >= 2 | 0.03391 | 0.02231 | 0.04213 | 0.99916 | 0.91388 | 1.45475 |
| holdout | Expanded if ratio >= 3 | 0.03428 | 0.02258 | 0.04323 | 0.99916 | 0.76169 | 1.47207 |
| holdout | Expanded if ratio >= 4 | 0.03507 | 0.02319 | 0.04723 | 0.99916 | 0.60940 | 1.51008 |
| holdout | Expanded if ratio >= 6 | 0.03600 | 0.02397 | 0.05233 | 0.99916 | 0.45708 | 1.55847 |
| holdout | Expanded if ratio >= 10 | 0.03733 | 0.02505 | 0.06157 | 0.99916 | 0.30472 | 1.62568 |
| holdout | Ratio >= 4 and minimum margin >= 2 | 0.03889 | 0.02683 | 0.07523 | 0.99916 | 0.45028 | 1.73055 |
| holdout | Ratio >= 4 and minimum margin >= 5 | 0.03960 | 0.02730 | 0.07557 | 0.99916 | 0.39985 | 1.76127 |
| holdout | Ratio >= 4 and smaller-sample share >= 0.50 | 0.03570 | 0.02402 | 0.05090 | 0.99916 | 0.60615 | 1.55814 |
| holdout | Ratio >= 4 and smaller-sample share >= 0.60 | 0.03595 | 0.02432 | 0.05133 | 0.99916 | 0.60405 | 1.57572 |
| holdout | Ratio >= 4, minimum margin >= 2, and smaller-sample share >= 0.50 | 0.03899 | 0.02695 | 0.07523 | 0.99916 | 0.44961 | 1.73754 |

## Interpretation

- On holdout, the current ratio-4 rule had MAE `0.03507` at alpha 0.05 and `0.02319` at alpha 0.01.
- Holdout normal-Wald MAE was `0.04055` and `0.02805`; expanded-with-fallback MAE was `0.03392` and `0.02230`.
- The best ratio threshold on development was `Expanded if ratio >= 2`. The best threshold when inspected post hoc on holdout was `Expanded if ratio >= 2`.
- Agreement between those thresholds supports a stable ratio decision;
  disagreement indicates that a sharp cutoff is not yet reliable.
- Support and variance-share guards are shown in the same table. A guard
  is useful only if it improves holdout error, not merely development
  error.

## Domain Sensitivity

The all-regime average includes a support-instability boundary where
neither first-order reference is calibrated. The restricted summaries
show whether routing conclusions survive after that known failure domain
is removed. `regular_support` additionally removes widespread sparsity.

| Domain | Decision rule | MAE 0.05 | MAE 0.01 | P90 error 0.05 | Relative-error score |
| --- | --- | --- | --- | --- | --- |
| all | Always Normal Wald | 0.04055 | 0.02805 | 0.07807 | 1.80808 |
| all | Expanded with Wald fallback | 0.03392 | 0.02230 | 0.04233 | 1.45426 |
| all | Expanded if ratio >= 2 | 0.03391 | 0.02231 | 0.04213 | 1.45475 |
| all | Expanded if ratio >= 4 | 0.03507 | 0.02319 | 0.04723 | 1.51008 |
| all | Ratio >= 4 and minimum margin >= 2 | 0.03889 | 0.02683 | 0.07523 | 1.73055 |
| all | Ratio >= 4 and smaller-sample share >= 0.50 | 0.03570 | 0.02402 | 0.05090 | 1.55814 |
| exclude_support_instability | Always Normal Wald | 0.01419 | 0.00758 | 0.03767 | 0.52100 |
| exclude_support_instability | Expanded with Wald fallback | 0.01018 | 0.00430 | 0.01910 | 0.31686 |
| exclude_support_instability | Expanded if ratio >= 2 | 0.01021 | 0.00433 | 0.01910 | 0.31852 |
| exclude_support_instability | Expanded if ratio >= 4 | 0.01084 | 0.00482 | 0.02133 | 0.34957 |
| exclude_support_instability | Ratio >= 4 and minimum margin >= 2 | 0.01239 | 0.00625 | 0.02700 | 0.43621 |
| exclude_support_instability | Ratio >= 4 and smaller-sample share >= 0.50 | 0.01091 | 0.00505 | 0.02233 | 0.36151 |
| regular_support | Always Normal Wald | 0.00871 | 0.00449 | 0.01700 | 0.31177 |
| regular_support | Expanded with Wald fallback | 0.00680 | 0.00286 | 0.01167 | 0.21112 |
| regular_support | Expanded if ratio >= 2 | 0.00684 | 0.00289 | 0.01167 | 0.21300 |
| regular_support | Expanded if ratio >= 4 | 0.00715 | 0.00316 | 0.01297 | 0.22959 |
| regular_support | Ratio >= 4 and minimum margin >= 2 | 0.00728 | 0.00332 | 0.01330 | 0.23884 |
| regular_support | Ratio >= 4 and smaller-sample share >= 0.50 | 0.00714 | 0.00318 | 0.01297 | 0.23025 |

Negative paired differences favour the candidate. Confidence intervals
use a cluster bootstrap over population pairs, keeping the thirteen
allocations of each population together.

| Domain | Candidate | Reference | Paired difference | 95% CI low | 95% CI high | Candidate better |
| --- | --- | --- | --- | --- | --- | --- |
| all | ratio_ge_4 | normal | -0.29800 | -0.43420 | -0.18560 | 0.39103 |
| all | ratio_ge_2 | normal | -0.35333 | -0.51163 | -0.22314 | 0.55484 |
| all | ratio_ge_2 | ratio_ge_4 | -0.05533 | -0.07665 | -0.03656 | 0.16382 |
| all | expanded_fallback | ratio_ge_2 | -0.00049 | -0.00242 | 0.00136 | 0.02707 |
| exclude_support_instability | ratio_ge_4 | normal | -0.17143 | -0.24926 | -0.10473 | 0.36298 |
| exclude_support_instability | ratio_ge_2 | normal | -0.20248 | -0.29377 | -0.12380 | 0.51522 |
| exclude_support_instability | ratio_ge_2 | ratio_ge_4 | -0.03105 | -0.04478 | -0.01926 | 0.15224 |
| exclude_support_instability | expanded_fallback | ratio_ge_2 | -0.00166 | -0.00368 | 0.00020 | 0.03045 |
| regular_support | ratio_ge_4 | normal | -0.08217 | -0.11811 | -0.05058 | 0.32875 |
| regular_support | ratio_ge_2 | normal | -0.09877 | -0.14131 | -0.06089 | 0.46337 |
| regular_support | ratio_ge_2 | ratio_ge_4 | -0.01660 | -0.02479 | -0.00944 | 0.13462 |
| regular_support | expanded_fallback | ratio_ge_2 | -0.00188 | -0.00365 | -0.00028 | 0.03114 |

The oracle table is not an implementable method. It chooses the better
reference after observing each configuration's simulated calibration and
therefore measures only the maximum room available for routing.

| cohort | configurations | mean_oracle_selection_score | oracle_selects_expanded_fraction |
| --- | --- | --- | --- |
| development | 1404 | 1.27235 | 0.57336 |
| holdout | 1404 | 1.44459 | 0.58191 |

## Evidence Status

The holdout populations are independent of the development populations,
but this remains a simulation study using the same generator family.
Any revised rule selected after reading this report needs another frozen
confirmation run. Data-dependent support and variance-share guards also
need particular caution because their route can be correlated with the
test statistic.

## Files

- `configuration_results.csv`: every allocation-rule result.
- `rule_summary.csv`: aggregate decision-rule comparison.
- `domain_summary.csv`: all, support-excluded, and regular-support views.
- `paired_rule_comparisons.csv`: clustered paired uncertainty estimates.
- `ratio_summary.csv`: results separated by sample-size ratio.
- `regime_summary.csv`: results separated by generating regime.
- `oracle_summary.csv`: unattainable scenario-level routing benchmark.
- `threshold_sensitivity.png`: development and holdout threshold curves.
