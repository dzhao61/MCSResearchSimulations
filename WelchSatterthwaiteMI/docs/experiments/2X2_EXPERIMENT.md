# Differential Mutual Information: 2x2 Experiments

## 1. Research question

The experiments compare analytical tests of

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are two independently sampled $2\times2$ joint
distributions. Binary tables are used first because they have the simplest
possible dependence structure while still covering small samples, skewed
margins, rare cells, and unequal sample sizes.

All three methods use the same bias-corrected MI difference and estimated
standard error:

$$
T=
\frac{\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

They differ only in the reference distribution used to convert $T$ into a
$p$-value.

| Method | Reference distribution |
| --- | --- |
| Normal Wald | Standard normal distribution |
| Simple Welch | Student $t$ distribution with ordinary Welch-Satterthwaite degrees of freedom |
| Expanded Welch | Student $t$ distribution with MI-specific Welch-Satterthwaite degrees of freedom |

The purpose is to determine whether Expanded Welch improves finite-sample
calibration without an unacceptable loss of power.

## 2. Quantities reported

The significance level is fixed at $\alpha=0.05$. Two measurements answer the
main questions.

| Measurement | Experiment | Interpretation |
| --- | --- | --- |
| False-positive rate | Simulate $I(P)=I(Q)$ | A correctly calibrated test rejects approximately 5% of samples |
| Power | Simulate $I(P)\ne I(Q)$ | A more powerful test detects a real difference more often |

Power must be interpreted together with false-positive calibration. A method
that rejects too often under $H_0$ can appear powerful under $H_1$ simply
because its threshold is too permissive. The true-negative rate and
false-negative rate are not reported separately because they are respectively
$1-\text{false-positive rate}$ and $1-\text{power}$.

A result is invalid when the observed tables produce a zero or non-finite
estimated standard error, or when the required degrees of freedom are not
positive and finite. The valid-result rate records the fraction of replicates
for which a finite $p$-value is produced.

## 3. Experimental configurations

For a binary table, the pair $(u,v)$ denotes

$$
u=\Pr(X=1),\qquad v=\Pr(Y=1).
$$

Each configuration fixes the margins of $P$ and $Q$, their common MI under the
null, and their baseline sample sizes. The table also gives the smallest
expected cell count under $H_0$ and the largest MI difference that is feasible
in the power experiment while retaining the same margins.

| Configuration | Margins of $P$ | Margins of $Q$ | $I(P)=I(Q)$ | $(n_P,n_Q)$ | Minimum expected count[^minimum-expected] | Largest tested $|I(P)-I(Q)|$ |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Balanced, very small sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(10,10)$ | 1.4010 | 0.500 |
| Balanced, moderate sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(50,50)$ | 7.0051 | 0.500 |
| Balanced, large sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(1000,1000)$ | 140.1027 | 0.500 |
| One skewed population | $(0.30,0.40)$ | $(0.10,0.30)$ | 0.0300 | $(50,50)$ | 1.7298 | 0.100 |
| Sparse, smaller sample | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0050 | $(100,100)$ | 0.2426 | 0.005 |
| Sparse, larger sample | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0050 | $(200,200)$ | 0.4853 | 0.005 |
| Ultra-rare categories | $(0.005,0.005)$ | $(0.002,0.010)$ | 0.0005 | $(1000,1000)$ | 0.2799 | 0.005 |
| Balanced, unequal samples | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(20,200)$ | 2.8021 | 0.500 |
| Skewed, unequal samples | $(0.30,0.40)$ | $(0.10,0.30)$ | 0.0300 | $(500,50)$ | 1.7298 | 0.100 |
| Rare and highly unequal | $(0.02,0.02)$ | $(0.01,0.05)$ | 0.0050 | $(200,2000)$ | 0.6988 | 0.020 |
| Near independence | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.0050 | $(1000,1000)$ | 225.0209 | 0.500 |
| Rare-cell case A | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0001 | $(100,100)$ | 1.1250 | 0.050 |
| Rare-cell case B | $(0.05,0.05)$ | $(0.025,0.10)$ | 0.0001 | $(500,500)$ | 1.5934 | 0.050 |

[^minimum-expected]: The minimum expected count is
    $\min\{\min_{i,j}(n_Pp_{ij}),\min_{i,j}(n_Qq_{ij})\}$. It is the
    smallest expected count among the eight cells in the two population
    tables, not the expected value of the smallest observed count.

Counts are sampled directly from the population tables. No expected-count
floor, smoothing rule, or continuity correction is applied.

### 3.1 Null-calibration experiment

Each of the 13 configurations is evaluated at half, baseline, and double its
listed sample sizes. This gives 39 exact null configurations. Each uses
200,000 independent table pairs, for 7.8 million pairs in total.

In addition to the false-positive rates, the experiment calculates

$$
c^*=Q_{0.95}(|T|\mid H_0),
$$

the empirical two-sided critical value that would produce a 5% rejection
rate. Normal Wald uses 1.96. Thus, $c^*>1.96$ indicates that a stricter cutoff
is needed, while $c^*<1.96$ indicates that a less strict cutoff is needed.

### 3.2 Power experiment

The association in $Q$ is changed while its margins remain fixed. The
requested MI differences are

$$
|I(P)-I(Q)|\in
\{0,10^{-5},10^{-4},10^{-3},0.005,0.01,0.02,0.05,
0.1,0.2,0.5,1.0\}\text{ nats}.
$$

The zero point is the matching false-positive rate. Every positive point is
power. The same half, baseline, and double sample-size scales are used.

Binary MI cannot exceed $\log 2\approx0.693$ nats, and fixed skewed margins
can impose a lower maximum. Infeasible differences are omitted without
changing the margins. This leaves 333 feasible configurations from 468
requested combinations. Each uses 50,000 independent table pairs, for 16.65
million pairs in total.

## 4. Null calibration

The table reports the baseline sample sizes from the 200,000-replicate audit.
The target false-positive rate is 0.05, and bold identifies the closest method
within each row. The empirical critical value is a diagnostic, not a fourth
test.

| Configuration | Normal Wald | Simple Welch | Expanded Welch | Expanded valid rate | Empirical $c^*$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Balanced, very small sample | 0.1337 | 0.0993 | **0.0487** | 0.9722 | 2.599 |
| Balanced, moderate sample | **0.0477** | 0.0439 | 0.0383 | 0.9999 | 1.939 |
| Balanced, large sample | 0.0502 | **0.0501** | 0.0492 | 1.0000 | 1.962 |
| One skewed population | **0.0302** | 0.0271 | 0.0171 | 0.9945 | 1.758 |
| Sparse, smaller sample | 0.0651 | **0.0627** | 0.0062 | 0.9939 | 2.059 |
| Sparse, larger sample | 0.1352 | 0.1345 | **0.0379** | 1.0000 | 2.709 |
| Ultra-rare categories | **0.0026** | 0.0026 | 0.0000 | 0.8535 | 1.553 |
| Balanced, unequal samples | 0.1695 | 0.1584 | **0.0559** | 0.9984 | 3.319 |
| Skewed, unequal samples | 0.1711 | 0.1674 | **0.0456** | 0.9946 | 3.241 |
| Rare and highly unequal | 0.4913 | 0.4912 | **0.2097** | 0.9656 | 2.869 |
| Near independence | **0.0280** | 0.0278 | 0.0144 | 1.0000 | 1.783 |
| Rare-cell case A | 0.0602 | **0.0573** | 0.0037 | 0.9938 | 2.029 |
| Rare-cell case B | 0.1227 | 0.1225 | **0.0165** | 1.0000 | 2.918 |

![Critical-value diagnostic](../../results/2x2_critical_value_audit/CRITICAL_VALUE_AUDIT.png)

The results show four distinct behaviours.

1. In the regular balanced cases, Normal Wald is already accurate once the
   sample size is moderate. All methods converge at the large sample size.
2. Expanded Welch corrects much of the liberal rejection in the very small
   balanced case and in the two unequal-sample cases. The rare and highly
   unequal configuration remains severely liberal despite this improvement.
3. Expanded Welch is inconsistent in sparse cases. It improves the larger
   sparse case but severely overcorrects the smaller and rare-cell cases.
4. The ultra-rare configuration is a breakdown case for every method. All
   methods are extremely conservative, and Expanded Welch is invalid in about
   15% of replicates.

Simple Welch generally remains close to Normal Wald. Its ordinary
degrees-of-freedom correction is not large enough to resolve the difficult
unequal-sample cases.

## 5. Power across MI differences

The overview figure shows power at the baseline sample sizes. The dotted
horizontal line is 0.05. A curve beginning above this line is already liberal
under $H_0$, so its positive-effect rejection rates overstate genuine
detection performance.

![Power over MI differences](../../results/2x2_power_curves/figures/POWER_CURVES_overview.png)

[Open the small-effect logarithmic view.](../../results/2x2_power_curves/figures/POWER_CURVES_small_effects.png)

The power experiment gives the following interpretation.

1. Differences from $10^{-5}$ to $10^{-3}$ nats are generally too small to
   detect at the tested sample sizes.
2. In balanced moderate and large samples, power rises as the MI difference
   increases, and the methods become similar as the sample size grows.
3. Expanded Welch usually rejects less often because its Student critical
   value is larger. This is beneficial when it corrects an inflated null
   rejection rate, but it becomes unnecessary power loss when Normal Wald is
   already calibrated or when Expanded Welch overcorrects.
4. The very-small-sample and sparse cases demonstrate the main limitation:
   calibrating through degrees of freedom alone can produce very large
   critical values and poor power.
5. In the most extreme rare and unequal case, high rejection rates do not
   establish good power because the null rejection rate is already far above
   0.05.

The individual case figures report half, baseline, and double sample sizes:
[`figures/cases`](../../results/2x2_power_curves/figures/cases/).

## 6. Why the Expanded correction is inconsistent

The critical-value audit separates an incorrect Student degrees of freedom
from a more general problem with the statistic. Across the 39 null
configurations:

- 21 require a critical value larger than 1.96;
- 15 require a critical value smaller than 1.96; and
- 3 are statistically consistent with 1.96.

A finite-degree Student distribution always has heavier tails than the normal
distribution, so it can only increase the critical value. Expanded Welch can
therefore help many liberal cases, but it cannot correct the 15 cases that
need a smaller threshold.

The estimated MI difference is also strongly related to its estimated
standard error in several sparse and unequal-sample regimes. The absolute
correlation reaches approximately 0.74 to 0.90 in several baseline cases.
Expanded Welch measures variability in the variance estimate, but it does not
model this joint movement of the numerator and denominator.

This diagnosis is supported by the unstudentized result. After oracle
centering and scaling, the median 5% critical value of the bias-corrected MI
difference across the 39 configurations is 1.990, close to the normal value
1.960. Much of the additional distortion appears after division by the
estimated standard error.

The complete diagnostic analysis is given in the
[critical-value audit](2X2_CRITICAL_VALUE_AUDIT.md).

## 7. Overall conclusion

Normal Wald is a strong baseline in regular, moderately sampled binary
tables, but it can be substantially liberal with very small samples, unequal
sample sizes, or sparse cells. Expanded Welch can correct some of these
liberal regimes, particularly the balanced and skewed unequal-sample cases.
It is not a generally superior replacement: in other configurations it is too
conservative, invalid, or less powerful without improving calibration.

The evidence therefore does not support another degrees-of-freedom adjustment
as the main next step. A more promising analytical refinement is to model the
studentized statistic directly, including the dependence between the MI
difference and its estimated standard error. Extreme discrete sparse cases may
still require an exact or resampling fallback.

## 8. Reproducibility files

| Output | File |
| --- | --- |
| Power configurations | [`configurations.csv`](../../results/2x2_power_curves/configurations.csv) |
| Power results and diagnostics | [`power_curves.csv`](../../results/2x2_power_curves/power_curves.csv) |
| Power run metadata | [`run_metadata.json`](../../results/2x2_power_curves/run_metadata.json) |
| Individual power figures | [`figures/cases`](../../results/2x2_power_curves/figures/cases/) |
| All critical-value configurations | [`critical_value_audit.csv`](../../results/2x2_critical_value_audit/critical_value_audit.csv) |
| Baseline critical-value results | [`baseline_critical_value_audit.csv`](../../results/2x2_critical_value_audit/baseline_critical_value_audit.csv) |
| Critical-value figure | [`CRITICAL_VALUE_AUDIT.png`](../../results/2x2_critical_value_audit/CRITICAL_VALUE_AUDIT.png) |
| Critical-value run metadata | [`run_metadata.json`](../../results/2x2_critical_value_audit/run_metadata.json) |
