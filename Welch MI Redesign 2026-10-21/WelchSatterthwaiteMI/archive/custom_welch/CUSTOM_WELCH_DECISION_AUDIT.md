# Custom Welch Decision Audit

## 1. Decision being studied

Custom Welch chooses between two calibrations of the same differential-MI
statistic:

1. **Normal Wald** compares the standardized statistic with a standard normal
   distribution.
2. **Expanded Welch** compares the same statistic with a Student distribution
   whose effective degrees of freedom reflect uncertainty in the estimated MI
   variance.

The effect estimate, bias correction, standard error, and test statistic are
identical. Only the reference distribution changes. The routing question is
therefore not which MI estimate to use, but when uncertainty in the estimated
standard error is large enough to justify the heavier Student tails.

The original Custom Welch rule used expanded Welch when

$$
R_n=\frac{\max(n_P,n_Q)}{\min(n_P,n_Q)}\geq 4
$$

and normal Wald otherwise. That cutoff was suggested by an experiment in
which regime and sample-size ratio were partly confounded. The present audit
crosses those factors directly.

## 2. Why sample-size ratio is a plausible routing variable

The estimated squared standard error is

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V_P}{n_P}+\frac{\widehat V_Q}{n_Q}.
$$

When the sample sizes are similar, the two variance components contribute on
similar scales. When one sample is much smaller, its component is amplified
by $1/n$ and often dominates the standard error. The final statistic then
depends strongly on one noisily estimated variance component. Expanded Welch
is designed for precisely this problem: it reduces the effective degrees of
freedom when the estimated variance is unstable.

Sample-size ratio also has an important methodological advantage. It is fixed
by the study design before the two tables are observed. Routing on it cannot
select a more favorable p-value after seeing the result.

## 3. Audit design

The audit generated independent development and holdout cohorts with
different population seeds. Each cohort contained 108 equal-MI population
pairs covering:

- six table shapes from $2\times2$ to $20\times20$;
- all nine experimental regimes;
- sample-size ratios $1$, $2$, $3$, $4$, $6$, $10$, and $20$;
- both directions of imbalance, with either $P$ or $Q$ receiving the smaller
  sample.

There were 2,808 allocation configurations in total and 3,000 independently
simulated table pairs per configuration, giving 8.424 million null table
pairs. The same simulated replicate was evaluated by every routing rule.
Paired uncertainty intervals clustered all 13 allocations of a population
pair together.

The primary calibration score was the mean of relative false-positive-rate
errors at $\alpha=0.05$ and $\alpha=0.01$:

$$
S=\frac{1}{2}
\left(
\frac{|\widehat{\operatorname{FPR}}_{0.05}-0.05|}{0.05}
+
\frac{|\widehat{\operatorname{FPR}}_{0.01}-0.01|}{0.01}
\right).
$$

Using relative errors prevents the more permissive $0.05$ level from
dominating the stricter $0.01$ level.

## 4. Candidate rules

The audit compared the following pre-specified choices:

- always use normal Wald;
- always use expanded Welch, with and without Wald fallback;
- use expanded Welch at ratios of at least 2, 3, 4, 6, or 10;
- require a minimum observed row or column total before using expanded Welch;
- require the smaller sample to contribute a minimum share of the estimated
  variance;
- combine the support and variance-share guards.

A further post-audit sensitivity check used the smaller sample's average
observations per cell, $\min(n_P,n_Q)/(rc)$. This checked whether an
interpretable density condition improved on the ratio rule.

For a fair threshold comparison, the audited ratio rules used normal Wald
when expanded Welch was undefined. Otherwise, a rule could appear better
merely by dropping its hardest replicates. The final implementation is more
conservative about validity: when $R_n\geq2$ requires expanded Welch and that
calculation is undefined, it reports no Custom Welch p-value.

## 5. Main result

The ratio threshold behaved monotonically: delaying expanded Welch made
calibration progressively worse in both development and holdout data.

| Rule | Holdout MAE at 0.05 | Holdout MAE at 0.01 | Relative-error score |
| --- | ---: | ---: | ---: |
| Always normal Wald | 0.04055 | 0.02805 | 1.80808 |
| Expanded if $R_n\geq2$ | **0.03391** | 0.02231 | 1.45475 |
| Expanded if $R_n\geq3$ | 0.03428 | 0.02258 | 1.47207 |
| Expanded if $R_n\geq4$ | 0.03507 | 0.02319 | 1.51008 |
| Expanded if $R_n\geq6$ | 0.03600 | 0.02397 | 1.55847 |
| Expanded if $R_n\geq10$ | 0.03733 | 0.02505 | 1.62568 |
| Expanded with Wald fallback | 0.03392 | **0.02230** | **1.45426** |

Development and holdout both selected $R_n\geq2$ as the best discrete ratio
threshold. Relative to the original $R_n\geq4$ rule, its paired score
improvement on holdout was $0.05533$, with a clustered 95% bootstrap interval
from $0.03656$ to $0.07665$. The improvement remained after removing support
instability and widespread sparsity.

Always-expanded-with-Wald-fallback and the $R_n\geq2$ rule were effectively
tied overall. Their holdout score difference was only $0.00049$, and its 95%
interval included zero. In the regular-support subset, always expanded was
slightly better on average, but the absolute difference was small.

The practical reason to retain routing is protection at equal sample sizes.
At $R_n=1$, expanded Welch was unnecessarily conservative for some
well-sampled, ultra-sparse, and support-instability populations. At
$R_n\geq2$, its average benefit increased with imbalance. The ratio-2 rule
therefore captures nearly all of always-expanded's gain while retaining the
simpler normal reference in the main regime where expanded Welch can hurt.

Applying the final no-fallback validity rule to the saved holdout audit gives
a mean valid rate of 0.99023 across all regimes, 0.99951 after excluding
support instability, and 0.99996 in the regular-support subset. The loss is
therefore concentrated at the deliberately adversarial support boundary. It
must be reported alongside conditional false-positive-rate accuracy rather
than hidden by a Wald substitution.

## 6. Why more elaborate guards were rejected

Observed minimum-margin guards substantially worsened holdout calibration.
For example, adding a minimum-margin requirement of 2 to the ratio-4 rule
increased holdout MAE from 0.03507 to 0.03889 at $\alpha=0.05$. Estimated
variance-share guards also worsened both tested significance levels.

These guards fail for two related reasons. First, they frequently route cases
back to normal Wald in precisely the unequal-sample regimes where normal Wald
has tails that are too light. Second, the observed support and variance share
are calculated from the same tables as the test statistic. Their random
variation can therefore be associated with the magnitude of the statistic,
making the selection mechanism harder to justify and calibrate.

The observations-per-cell sensitivity rule gave only a negligible holdout
improvement over $R_n\geq2$. Its best development threshold changed the
relative-error score by less than 0.001 on holdout. This is too little benefit
to justify another cutoff or a more complicated explanation.

## 7. The support-instability boundary

The audit deliberately crossed severe sample imbalance with populations in
which a row or column frequently disappears. Neither reference distribution
was calibrated there. At a ratio of 20, holdout false-positive rates at
nominal $\alpha=0.05$ were approximately 0.418 for normal Wald and 0.376 for
expanded Welch.

This failure is not primarily a standard-error scale problem. Across the
support-instability configurations, the mean estimated standard error was
close to the empirical standard deviation. The standardized absolute bias of
the corrected MI difference, however, rose from about 0.24 at equal sample
sizes to 1.39 at ratio 20. Changing from normal to Student tails cannot repair
a statistic whose numerator is centered roughly one standard deviation away
from zero.

The first-order MI bias correction still helped. Across holdout
support-instability configurations, it reduced mean standardized centering
error from approximately 1.47 for the uncorrected plug-in difference to 1.07.
It was simply insufficient when sampled support changed repeatedly and the
sample sizes were unequal.

Consequently, a disappearing row or column should be treated as a domain
warning, not as evidence that normal Wald is a valid fallback. Routing cannot
solve the failure of the first-order effect approximation itself.

## 8. Recommended decision rule

The evidence supports the following revision candidate:

$$
p_{\mathrm{custom}}
=
\begin{cases}
p_{\mathrm{expanded}},
&R_n\geq2\text{ and expanded Welch is defined},\\
p_{\mathrm{normal}},
&R_n<2,\\
\text{unsupported-domain result},
&\text{the shared first-order calculation fails because support collapses}.
\end{cases}
$$

This is preferable to the original $4{:}1$ cutoff because the correction was
already beneficial at $2{:}1$ and $3{:}1$ in both independent cohorts. It is
preferable to a complex adaptive selector because the tested support, density,
and variance-share rules did not provide a meaningful holdout gain.

This routing proposal was subsequently removed from the active project
because its regime-selection logic added more complexity than the thesis
required. The audit is retained as a complete research record rather than as
the recommended production method.

## 9. Reproducibility

The executable audit is
[`investigate_custom_welch_decision.py`](investigate_custom_welch_decision.py).
The complete result tables, metadata, plot, and generated report are in
[`results/`](results/).
