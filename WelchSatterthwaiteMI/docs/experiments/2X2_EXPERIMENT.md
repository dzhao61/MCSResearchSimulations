# Expanded Welch-Satterthwaite: 2x2 Experiment

## 1. Purpose

This experiment compares three analytical tests of

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are independently sampled $2\times2$ contingency tables.

| Method | Reference distribution |
| --- | --- |
| Normal Wald | Standard normal |
| Simple Welch | Student $t$ with ordinary Welch-Satterthwaite degrees of freedom |
| Expanded Welch | Student $t$ with MI-specific degrees of freedom |

All three methods use the same bias-corrected MI difference and estimated
standard error. They differ only in the distribution used to convert the test
statistic into a $p$-value.

## 2. Measurements

The significance level is $\alpha=0.05$.

| Measure | Meaning | Desired result |
| --- | --- | ---: |
| False-positive rate | Rejecting $H_0$ when $I(P)=I(Q)$ | 0.05 |
| True-negative rate | Not rejecting $H_0$ when $I(P)=I(Q)$ | 0.95 |
| Power | Rejecting $H_0$ when $I(P)\ne I(Q)$ | As high as possible |
| False-negative rate | Not rejecting $H_0$ when $I(P)\ne I(Q)$ | As low as possible |
| Valid-result rate | Fraction of samples for which the test can be calculated | 1.00 |

A false-positive rate above 0.05 means the test is **liberal** and reports too
many differences. A rate below 0.05 means it is **conservative** and may miss
real differences.

Power uses each analytical test directly at the fixed threshold
$p\leq0.05$. It is interpreted alongside the false-positive rate from the
matching null configuration.

## 3. Experiment design

The experiment uses the same 13 configurations under both hypotheses. Each
configuration fixes the margins and sample sizes, then is simulated in two
forms:

$$
H_0:I(P)=I(Q)=I_0,
$$

and

$$
H_1:I(P)=I_0,\qquad I(Q)=I_0+0.005\text{ nats}.
$$

Thus, every false-positive result in Section 4 has a directly corresponding
power result in Section 5. The alternative changes only the association in
table $Q$; the margins and sample sizes remain unchanged. Each form uses
50,000 independently simulated table pairs, and no results are averaged across
configurations. The 0.005-nat increment is a round common effect that is
feasible for all 13 fixed-margin configurations; an increment of 0.01 nats
would not be feasible for the sparse opposite-association case.

Counts are sampled directly from the stated population tables. No minimum
expected-count rule or smoothing is applied.

For the table below, $(u,v)$ denotes the two binary margins
$u=\Pr(X=1)$ and $v=\Pr(Y=1)$. The minimum expected count[^minimum-expected]
is the smallest expected count among all cells in both sampled tables.

| Configuration | Margins for $P$ | Margins for $Q$ | $I_0$ | $(n_P,n_Q)$ | Minimum expected count under $H_0$ | Minimum expected count under $H_1$ |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Balanced, very small sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(10,10)$ | 1.4010 | 1.3749 |
| Balanced, moderate sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(50,50)$ | 7.0051 | 6.8744 |
| Balanced, large sample | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(1000,1000)$ | 140.1027 | 137.4889 |
| One skewed population | $(0.30,0.40)$ | $(0.10,0.30)$ | 0.0300 | $(50,50)$ | 1.7298 | 1.5871 |
| Sparse, smaller sample | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0050 | $(100,100)$ | 0.2426 | 0.0312 |
| Sparse, larger sample | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0050 | $(200,200)$ | 0.4853 | 0.0624 |
| Ultra-rare categories | $(0.005,0.005)$ | $(0.002,0.010)$ | 0.0005 | $(1000,1000)$ | 0.2799 | 0.3054 |
| Balanced, unequal samples | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.1000 | $(20,200)$ | 2.8021 | 2.8021 |
| Skewed, unequal samples | $(0.30,0.40)$ | $(0.10,0.30)$ | 0.0300 | $(500,50)$ | 1.7298 | 1.5871 |
| Rare and highly unequal | $(0.02,0.02)$ | $(0.01,0.05)$ | 0.0050 | $(200,2000)$ | 0.6988 | 0.6988 |
| Near independence | $(0.50,0.50)$ | $(0.50,0.50)$ | 0.0050 | $(1000,1000)$ | 225.0209 | 214.7037 |
| Rare-cell case A | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.0001 | $(100,100)$ | 1.1250 | 1.1294 |
| Rare-cell case B | $(0.05,0.05)$ | $(0.025,0.10)$ | 0.0001 | $(500,500)$ | 1.5934 | 1.5989 |

[^minimum-expected]: This is calculated as
    $\min\{\min_{i,j}(n_Pp_{ij}),\min_{i,j}(n_Qq_{ij})\}$: first calculate
    every cell's expected count, then select the smallest. It is not the
    expected value of the minimum observed cell count.

## 4. False-positive calibration ($H_0$ true)

The target false-positive rate is 0.05. Values closer to 0.05 are better.
The final column reports how often Expanded Welch produced a valid result.

| Configuration | Normal Wald | Simple Welch | Expanded Welch | Expanded valid rate |
| --- | ---: | ---: | ---: | ---: |
| Balanced, very small sample | 0.1330 | 0.0988 | **0.0476** | 0.9722 |
| Balanced, moderate sample | **0.0472** | 0.0438 | 0.0379 | 0.9998 |
| Balanced, large sample | 0.0513 | 0.0513 | **0.0502** | 1.0000 |
| One skewed population | **0.0303** | 0.0276 | 0.0181 | 0.9946 |
| Sparse, smaller sample | **0.0649** | 0.0624 | 0.0065 | 0.9945 |
| Sparse, larger sample | 0.1396 | 0.1388 | **0.0396** | 1.0000 |
| Ultra-rare categories | **0.0026** | 0.0026 | 0.0000 | 0.8533 |
| Balanced, unequal samples | 0.1686 | 0.1570 | **0.0555** | 0.9985 |
| Skewed, unequal samples | 0.1709 | 0.1673 | **0.0464** | 0.9952 |
| Rare and highly unequal | 0.4906 | 0.4905 | **0.2085** | 0.9650 |
| Near independence | **0.0270** | 0.0268 | 0.0139 | 1.0000 |
| Rare-cell case A | **0.0586** | 0.0559 | 0.0037 | 0.9933 |
| Rare-cell case B | 0.1216 | 0.1213 | **0.0162** | 1.0000 |

Bold identifies the value closest to 0.05, but the distance from 0.05 remains
important. For example, 0.2085 is better than 0.4906 but is still far too
liberal.

![False-positive calibration and validity](../../results/2x2_mirrored_confirmatory/figures/CONFIRM_null_calibration_and_validity.png)

### Main calibration findings

- **Balanced tables:** Expanded Welch corrects the severe false-positive
  inflation at $n=10$. Normal Wald is already accurate at $n=50$, while all
  methods are accurate at $n=1000$.
- **Unequal sample sizes:** Expanded Welch gives the clearest improvement. It
  reduces the false-positive rate from 0.1686 to 0.0555 in the balanced case
  and from 0.1709 to 0.0464 in the skewed case.
- **Sparse tables:** Performance is inconsistent. Expanded Welch improves the
  $n=200$ case but becomes much too conservative in the $n=100$ case.
- **Ultra-rare tables:** None of the methods works well. Expanded Welch also
  becomes invalid in about 15% of samples.
- **Near independence:** All three methods are conservative, with Expanded
  Welch furthest below the 0.05 target.

## 5. Detection power ($H_1$ true)

These are the same 13 configurations as Section 4, in the same order. Their
MI difference is fixed at $\lvert I(P)-I(Q)\rvert=0.005$ nats.

This is the probability that each analytical method detects the MI difference
using the fixed $p\leq0.05$ rule.

| Configuration | Normal Wald | Simple Welch | Expanded Welch | Expanded valid rate |
| --- | ---: | ---: | ---: | ---: |
| Balanced, very small sample | 0.1364 | 0.1005 | 0.0494 | 0.9712 |
| Balanced, moderate sample | 0.0500 | 0.0460 | 0.0398 | 0.9999 |
| Balanced, large sample | 0.0592 | 0.0591 | 0.0583 | 1.0000 |
| One skewed population | 0.0358 | 0.0331 | 0.0210 | 0.9949 |
| Sparse, smaller sample | 0.0844 | 0.0814 | 0.0099 | 0.9946 |
| Sparse, larger sample | 0.2142 | 0.2130 | 0.0646 | 1.0000 |
| Ultra-rare categories | 0.0329 | 0.0329 | 0.0097 | 0.8544 |
| Balanced, unequal samples | 0.1736 | 0.1624 | 0.0538 | 0.9984 |
| Skewed, unequal samples | 0.1503 | 0.1467 | 0.0428 | 0.9945 |
| Rare and highly unequal | 0.4962 | 0.4962 | 0.4189 | 0.9649 |
| Near independence | 0.1195 | 0.1191 | 0.0866 | 1.0000 |
| Rare-cell case A | 0.0327 | 0.0310 | 0.0032 | 0.9943 |
| Rare-cell case B | 0.0238 | 0.0236 | 0.0044 | 1.0000 |

Power must be read beside the matching false-positive rate. For
example, Normal Wald rejects 13.30% of null samples and 13.64% of alternative
samples in the very-small-sample case. Its apparently high power is therefore
almost entirely false-positive inflation.

![Detection power](../../results/2x2_mirrored_confirmatory/figures/CONFIRM_detection_power.png)

## 6. Conclusion

The mirrored design distinguishes genuine detection from liberal rejection.
Expanded Welch substantially improves calibration in the very-small and
unequal-sample cases, but a fixed difference of 0.005 nats is often too small
to detect reliably.

Expanded Welch remains unreliable for some extremely sparse tables, where it
can be overly conservative or invalid. A later power-curve experiment should
retain these same configurations while varying the MI difference above and
below 0.005 nats.

## 7. Data files

| Data | File |
| --- | --- |
| Population configurations | [`configurations.csv`](../../results/2x2_mirrored_confirmatory/configurations.csv) |
| False-positive and validity results | [`null_summary.csv`](../../results/2x2_mirrored_confirmatory/null_summary.csv) |
| Power results | [`power_summary.csv`](../../results/2x2_mirrored_confirmatory/power_summary.csv) |
| Detailed experiment report | [`REPORT.md`](../../results/2x2_mirrored_confirmatory/REPORT.md) |
