# Constrained Likelihood-Ratio Validation for 2x2 Equal-MI Testing

## 1. Research question

This experiment asks whether equality of two discrete mutual informations can be
tested more reliably by fitting the null hypothesis directly:

\[
H_0:I(P)=I(Q).
\]

The candidate is a constrained likelihood-ratio (LR) test. The validation is limited
to \(2\times2\) tables so that the method can be understood and tested before
considering larger alphabets.

## 2. Method

For observed count tables \(N^{(P)}\) and \(N^{(Q)}\), the unrestricted model
fits the two multinomial distributions separately. Their maximum-likelihood
estimates are the observed cell proportions.

The null model instead maximises the same joint log likelihood subject to

\[
I(P)=I(Q).
\]

If \(\ell_{\mathrm{free}}\) and \(\ell_{0}\) are the unrestricted and
constrained maxima, the statistic is

\[
D=2\{\ell_{\mathrm{free}}-\ell_0\}.
\]

The equality constraint removes one parameter. Under regular large-sample
conditions, the analytic test therefore compares \(D\) with
\(\chi^2_1\). This reference can fail near a probability boundary or near
independence. The experiment evaluates this directly usable analytic version
without population-specific calibration.

## 3. Numerical implementation

Each fitted probability table is represented by three unconstrained logits,
with the fourth cell as the reference. This guarantees positive probabilities
that sum to one. The optimizer uses analytic gradients for the multinomial
likelihood and MI constraint.

Five starting points are fitted for every table pair. This is necessary because
the equal-MI constraint can contain different association branches. A
three-start shortcut was rejected after the audit found LR-statistic errors as
large as 1.43 in sparse cases.

The final implementation passed gradient, group-swap, category-relabeling,
count-scaling, identical-table, and input-validation tests. Repeating audited
full fits produced a maximum statistic difference of zero. Constraint
residuals were below \(10^{-8}\).

## 4. Experiment design

The null experiment used 13 fixed population pairs already selected in the
2x2 study. They include balanced, skewed, sparse, unequal-sample,
near-independence, and rare-cell cases. Every population pair satisfies
\(I(P)=I(Q)\). Each baseline sample size was multiplied by \(0.5\), \(1\), and
\(2\), giving 39 exact configurations.

For every configuration:

- 5,000 null replicates measured false-positive rates;
- all methods used the same simulated tables.

This gives 195,000 null table pairs.

The power experiment used the same 39 configurations with a true MI difference
of 0.005 nats. It also used a difference of 0.05 nats for the 27 configurations
where that MI is attainable with the fixed margins. Each alternative received
5,000 replicates, giving 330,000 alternative table pairs.

## 5. Null calibration

The primary metric is mean absolute false-positive-rate error across the 39
fixed configurations. Lower values are better. The nominal level is 0.05.

| Method | Mean FPR | Mean absolute error | Median absolute error | Worst absolute error | Minimum valid rate |
|---|---:|---:|---:|---:|---:|
| Normal Wald | 0.1073 | 0.0762 | 0.0362 | 0.6404 | 0.9430 |
| Expanded Welch | 0.0360 | 0.0329 | 0.0326 | 0.1676 | 0.5344 |
| Constrained LR, \(\chi^2_1\) | 0.0331 | **0.0210** | **0.0174** | **0.0486** | **0.9990** |

The uncorrected LR had lower absolute error than Wald in 29 of 39
configurations and lower error than Expanded Welch in 24 of 39. It was also
more stable numerically.

Its remaining error is systematic conservatism. The most difficult rare-cell
configurations had false-positive rates between 0.0014 and 0.011 under the
\(\chi^2_1\) threshold. The analytic LR is therefore well calibrated on average
but can reject too rarely in individual sparse configurations.

At the more stringent nominal level 0.01, mean absolute errors were 0.0425 for
Wald, 0.0093 for Expanded Welch, and 0.0051 for constrained LR.

## 6. Power at two fixed effects

Power is the probability of rejecting \(H_0\) when the two population MIs are
different. The table reports ordinary rejection rates at nominal
\(\alpha=0.05\).

| MI difference | Configurations | Normal Wald | Expanded Welch | LR, \(\chi^2_1\) |
|---:|---:|---:|---:|---:|
| 0.005 | 39 | 0.1255 | 0.0593 | 0.0728 |
| 0.050 | 27 | 0.4001 | 0.3417 | 0.4031 |

Wald's small-effect rejection rate is partly inflated by its poor null
calibration. LR loses power in some sparse small-effect cases because its
\(\chi^2_1\) threshold is conservative. At the larger effect, its mean rejection
rate is similar to Wald and higher than Expanded Welch.

This result is not uniform. In a few severe sparse and unequal-sample cases,
LR had weak power for a 0.005-nat difference. The method does not remove the
information limit imposed by rare observations.

## 7. Power over the full feasible MI range

The two-effect experiment does not show whether a method remains useful as the
two population MIs move farther apart. A second experiment therefore used the
13 baseline configurations and every attainable value in the prespecified MI
difference grid, from the equal-MI null to the largest feasible difference.
The fixed margins determine which differences are attainable. This produced
111 exact configurations, each evaluated using 5,000 independent table pairs,
or 555,000 table pairs in total.

![Full feasible-range power curves](../../results/2x2_constrained_lr_full_curves/FULL_FEASIBLE_POWER_CURVES.png)

All panels use the same horizontal and vertical scales. Curves end at the
largest MI difference attainable under each configuration's fixed margins.
Different line styles and markers identify displayed methods whose curves
overlap.

Across all nonzero curve points, the raw LR rejection rate exceeded Expanded
Welch at 77 points and was lower at 16. Its mean rejection rate was 0.202,
compared with 0.184 for Expanded Welch. Relative to nominal Wald, raw LR was
higher at 40 points and lower at 50. This latter comparison is not a fair power
comparison in configurations where Wald already rejects the true null much
more than 5% of the time.

The usable LR was notably stronger than both baselines in the ultra-rare,
skewed unequal-sample, and two rare-cell cases. It was similar in balanced
moderate- and large-sample cases, but weaker in the ordinary sparse and rare
highly unequal-sample cases. It is therefore not uniformly more powerful. A
single average power value would conceal this regime dependence.

## 8. Runtime and validity

Across the final runs, the median complete constrained fit took approximately
5.0 ms under the null and 8.4 ms under the alternatives on this machine. The
LR fit was valid for at least 99.9% of replicates. The 16 invalid fits among
720,000 final table pairs occurred in the smallest balanced-sample family and
were excluded from method-specific denominators.

In the separate full-range experiment, the median fit took 5.8 ms. There were
34 invalid fits among 555,000 table pairs, the minimum configuration-level
valid rate was 0.9984, and repeated full-start fits gave identical statistics.

The method is therefore much more expensive than a closed-form Wald test but
still practical for individual 2x2 tests and potentially much cheaper than a
large per-test resampling procedure.

## 9. Decision

**The usable constrained LR is promising for specific hard 2x2 regimes, but it
is not a uniformly better general test.**

The evidence supports a targeted rather than general conclusion:

1. retain the analytic LR as a candidate for ultra-rare and rare-cell regimes;
2. do not describe it as a universal replacement for Wald or Expanded Welch;
3. investigate why ordinary sparse and rare highly unequal-sample cases lose
   power before extending the method to larger tables.

## 10. Reproducible artefacts

- Implementation: `src/welch_differential_mi/likelihood_ratio.py`
- Calibration runner: `experiments/run_constrained_lr_audit.py`
- Power runner: `experiments/run_constrained_lr_power.py`
- Full-range runner: `experiments/run_constrained_lr_full_curves.py`
- Unit tests: `tests/test_likelihood_ratio.py`
- Final calibration: `results/2x2_constrained_lr_confirmatory_fullstarts/`
- Final power: `results/2x2_constrained_lr_power_fullstarts/`
- Full-range curves: `results/2x2_constrained_lr_full_curves/`
