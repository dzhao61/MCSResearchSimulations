# Summary: Welch-Type Testing for Differential Mutual Information

## 1. Research Story

The research question is

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are joint distributions estimated from two independent
categorical samples.

The idea is analogous to Welch's $t$-test. Classical Welch testing compares
two population means by:

1. estimating the difference between the means;
2. dividing that difference by its estimated standard error;
3. using a Student distribution with effective degrees of freedom that reflect
   uncertainty in the two variance estimates.

Here, the two means are replaced by two mutual information estimates:

| Welch's $t$-test | Differential-MI test |
| --- | --- |
| Sample mean | Bias-corrected MI |
| Sample variance | MI influence variance |
| Difference in means | Difference in MI |
| Welch-Satterthwaite degrees of freedom | Simple or MI-specific degrees of freedom |

Three analytic methods form the comparison:

| Method | How $T$ is calibrated |
| --- | --- |
| Normal Wald | Standard normal distribution |
| Simple Welch-Satterthwaite | Student distribution using $n-1$ component degrees of freedom |
| Expanded Welch-Satterthwaite | Student distribution using MI-specific variance-influence degrees of freedom |

The expanded Welch-Satterthwaite method supplies the MI-specific finite-df
calculation evaluated in this study.

## 2. Quick Literature Review

**Welch (1947) and Satterthwaite (1946).** Welch's $t$-test handles two
means with unequal and estimated variances. Satterthwaite's approximation
replaces several uncertain variance components with one effective number of
degrees of freedom.

**Hutcheson (1970).** Hutcheson applied the same broad idea to comparing two
Shannon diversity values. This is the closest direct predecessor because
Shannon diversity is an entropy functional. It means that using a
Welch-Satterthwaite architecture for an information quantity is not itself
new.

**Miller (1955) and later MI estimation work.** Plug-in entropy and MI
estimates have finite-sample bias. For an $r\times c$ table with fixed
positive support, the leading MI bias is

$$
\frac{(r-1)(c-1)}{2n}.
$$

This correction is important when comparing groups with different sample
sizes.

**Mora and Ruiz-Castillo (2009, 2011).** Their work studies estimation and
comparison of an MI-based segregation index. It establishes clear prior work
for comparing MI-type quantities between populations.

The simple Welch method is therefore best viewed as a direct transport of
existing ideas. The potentially novel part is the expanded
Welch-Satterthwaite calculation: deriving effective degrees of freedom from
the full influence function of the discrete-MI variance estimator, then
testing that calculation across broad finite-sample regimes.

Key references:

- Welch: <https://doi.org/10.1093/biomet/34.1-2.28>
- Satterthwaite: <https://doi.org/10.2307/3002019>
- Hutcheson: <https://doi.org/10.1016/0022-5193(70)90124-4>
- Mora and Ruiz-Castillo:
  <https://doi.org/10.1111/j.1467-9531.2011.01237.x>

## 3. Shared Data and Effect Estimate

### Notation convention

The notation distinguishes a population quantity from its sample estimate in
one consistent way. For any statistical functional $F$, $F(P)$ is its value
under population $P$, and $\widehat F(P)=F(\widehat P)$ is the value calculated
from $P$'s empirical table. Thus, $I(P)$ and $V(P)$ are population quantities,
whereas $\widehat I(P)$ and $\widehat V(P)$ are estimates. Subscripts are used
only where they carry a different meaning, such as the sample size $n_P$ or a
cell-level function $\ell_P(i,j)$.

All three methods begin with the same two count tables:

$$
N^P=(N^P_{ij}),
\qquad
N^Q=(N^Q_{ij}),
$$

with sample sizes $n_P$ and $n_Q$. The rows and columns represent the same
aligned categories in both groups.

### 3.1 Estimate MI

For group $P$, calculate empirical cell and marginal probabilities:

$$
\widehat p_{ij}=\frac{N^P_{ij}}{n_P},
\qquad
\widehat p_{i+}=\sum_j\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_i\widehat p_{ij}.
$$

Plug-in MI in nats is

$$
\widehat I(P)
=\sum_{i=1}^{r}\sum_{j=1}^{c}
\widehat p_{ij}
\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The same calculation gives $\widehat I(Q)$.

### 3.2 Correct the leading bias

Let

$$
d=(r-1)(c-1).
$$

The corrected MI estimates are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P},
\qquad
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated MI difference is

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

### 3.3 Estimate the standard error

Define the pointwise mutual information (PMI) for a cell:

$$
\widehat\ell_P(i,j)
=\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The MI influence variance for group $P$ is

$$
\widehat V(P)
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left\{\widehat\ell_P(i,j)-\widehat I(P)\right\}^2.
$$

Define $\widehat V(Q)$ in the same way. Because the groups are independent,

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

Every method uses the same standardized statistic:

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\widehat{\operatorname{SE}}}.
$$

The methods differ only in how they decide whether the observed magnitude
$|T|$ is unusual.

The working assumptions are independent observations within each group,
independent groups, fixed aligned alphabets, positive population support, and
a positive first-order influence variance.

## 4. Method 1: Normal Wald

### How it works

Normal Wald treats the estimated standard error as sufficiently accurate and
compares $T$ with a standard normal variable:

$$
p_{\mathrm{normal}}
=2\Pr\{Z\ge |T|\},
\qquad
Z\sim N(0,1).
$$

A $100(1-\alpha)\%$ confidence interval is

$$
\widehat\Delta_{\mathrm{BC}}
\ \pm\
z_{1-\alpha/2}\widehat{\operatorname{SE}}.
$$

### Interpretation

Normal Wald is the simplest analytic baseline. It is asymptotically valid
under regular fixed-support conditions. Its weakness is finite-sample
calibration: it does not account for uncertainty in $\widehat V(P)$ and
$\widehat V(Q)$.

### Cost

It requires one pass over the table:

$$
O(rc).
$$

## 5. Method 2: Simple Welch-Satterthwaite

### How it works

Simple Welch treats the MI influence variances like ordinary sample variances
and assigns them $n_P-1$ and $n_Q-1$ degrees of freedom. Satterthwaite then
combines them:

$$
\widehat\nu_{\mathrm{simple}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/(n_P-1)
+\left\{\widehat V(Q)/n_Q\right\}^2/(n_Q-1)
}.
$$

The p-value becomes

$$
p_{\mathrm{simple}}
=2\Pr\{t_{\widehat\nu_{\mathrm{simple}}}\ge |T|\}.
$$

### Interpretation

A Student distribution has heavier tails than a normal distribution. Simple
Welch therefore produces slightly larger p-values and wider confidence
intervals than normal Wald.

The limitation is that $n-1$ is exact for a conventional sample variance
under classical assumptions, but $\widehat V(P)$ is a nonlinear function of
the full contingency table. Changing one observation changes cell
probabilities, marginal probabilities, PMI values, MI, and its
estimated variance.

### Cost

The extra Satterthwaite arithmetic is constant time after $\widehat V(P)$ and
$\widehat V(Q)$ are available. Overall cost remains

$$
O(rc).
$$

## 6. Method 3: Expanded Welch-Satterthwaite

Expanded Welch uses the same bias-corrected MI difference, standard error, and
statistic $T$ as the preceding methods. It changes only the effective
degrees of freedom used to calibrate $T$.

The method adapts the Welch-Satterthwaite architecture used by Hutcheson
(1970) for comparing Shannon diversities. The adaptation is MI-specific
because it derives the sampling uncertainty of the complete MI variance
estimate $\widehat V(P)$, including the dependence of pointwise mutual
information on the joint and marginal probabilities.

### 6.1 Start from the Satterthwaite target

Satterthwaite approximates the positive variance estimate $\widehat V(P)$
by a scaled chi-squared variable:

$$
\widehat V(P)
\ \text{is modelled by}\
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}.
$$

This family is used because a scaled chi-squared variable is positive and has
an adjustable variance controlled by its degrees of freedom. Its first two
moments are

$$
\operatorname E\!\left[
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right]
=
\operatorname E\{\widehat V(P)\},
$$

and

$$
\operatorname{Var}\!\left[
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right]
=
\frac{2[\operatorname E\{\widehat V(P)\}]^2}{\nu_V(P)}.
$$

Matching this variance to the sampling variance of $\widehat V(P)$ gives

$$
\nu_V(P)
=
\frac{
2[\operatorname E\{\widehat V(P)\}]^2
}{
\operatorname{Var}\{\widehat V(P)\}
}.
$$

To first order, $\operatorname E\{\widehat V(P)\}\approx V(P)$. The remaining
task is therefore to calculate $\operatorname{Var}\{\widehat V(P)\}$.

### 6.2 Calculate how the MI variance changes

For population $P$, pointwise mutual information and its variance are

$$
\ell_P(i,j)
=
\log\!\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right),
\qquad
V(P)
=
\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2.
$$

To measure how $V(P)$ responds to one observation in cell $(x,y)$, move a
small amount of probability toward that cell:

$$
P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

Define the resulting first-order change in $V(P)$ by

$$
g_P(x,y)
=
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Writing

$$
M_2(P)=\operatorname E_P\{\ell_P(X,Y)^2\},
\qquad
V(P)=M_2(P)-I(P)^2,
$$

gives

$$
g_P(x,y)
=
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-
2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

The two derivatives are

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=
\ell_P(x,y)-I(P),
$$

and

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
=
\ell_P(x,y)^2-M_2(P)
+
2\left[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(X,Y)\mid X=x\}
-\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}
+I(P)
\right].
$$

Substitution gives the MI-variance influence function

$$
\boxed{
\begin{aligned}
g_P(x,y)
={}&
\{\ell_P(x,y)-I(P)\}^2-V(P)\\
&+
2\left[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(X,Y)\mid X=x\}
-\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}
+I(P)
\right].
\end{aligned}
}
$$

The conditional row and column means appear because changing one cell changes
both marginal probabilities inside the PMI calculation.

### 6.3 Obtain the component degrees of freedom

Define the population variability of these observation-level changes by

$$
\tau^2(P)
=
\operatorname{Var}_P\{g_P(X,Y)\}.
$$

A first-order Taylor expansion of the variance estimator gives

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}
\sum_{a=1}^{n_P}g_P(Z_a^{(P)}),
$$

so independence of the observations gives

$$
\operatorname{Var}\{\widehat V(P)\}
\approx
\frac{\tau^2(P)}{n_P}.
$$

Substituting this result into the Satterthwaite equation produces the
MI-specific component degrees of freedom:

$$
\boxed{
\nu_V(P)
\approx
\frac{2n_PV(P)^2}{\tau^2(P)}.
}
$$

For calculation from an observed table, replace every population quantity by
its empirical counterpart. For each occupied cell $\widehat p_{ij}>0$, calculate

$$
\begin{aligned}
\widehat g_P(i,j)
={}&
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2-\widehat V(P)\\
&+
2\left[
\widehat\ell_P(i,j)
-\frac{\sum_{j'}\widehat p_{ij'}\widehat\ell_P(i,j')}
       {\widehat p_{i+}}
-\frac{\sum_{i'}\widehat p_{i'j}\widehat\ell_P(i',j)}
       {\widehat p_{+j}}
+\widehat I(P)
\right],
\end{aligned}
$$

followed by

$$
\overline g_P
=
\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j),
\qquad
\widehat\tau^2(P)
=
\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2,
$$

and

$$
\boxed{
\widehat\nu_V(P)
=
\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
}
$$

Apply the same calculation to the second table to obtain
$\widehat\nu_V(Q)$.

### 6.4 Combine the two variance components

The effective degrees of freedom for the complete standard error are

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=
\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_V(P)
+
\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_V(Q)
}.
}
$$

The final two-sided p-value is

$$
p_{\mathrm{expanded}}
=
2\left[
1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)
\right].
$$

If $\widehat V(P)$ and $\widehat V(Q)$ are stable between samples, their
component degrees of freedom are large and the Student reference approaches
the normal reference. Greater variance-estimation uncertainty lowers the
degrees of freedom and produces heavier tails.

The calculation is deterministic, requires $O(rc)$ time, and cost
approximately 1.9 times normal Wald in the unified benchmark while remaining
below 0.2 ms per table pair for tables up to $20\times20$.

The complete cell-by-cell derivation and theoretical justification are given
in [Expanded Welch-Satterthwaite Derivation](EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md).

## 7. Experimental Design

### 7.1 Main question

The main experiment asks a direct question:

> When two independent samples come from populations with the same true MI,
> which analytic method keeps its false-positive rate closest to the nominal
> significance level?

The primary significance level is $\alpha=0.05$. A correctly calibrated test
should therefore reject approximately 5% of the time. A rate above 0.05 is
liberal and produces too many false positives; a rate below 0.05 is
conservative.

All three methods use exactly the same sampled tables, bias-corrected MI
difference, and standard error. They differ only in the reference
distribution used to calculate the p-value. This isolates the effect of the
degrees-of-freedom correction.

### 7.2 Calibration grid

Each null scenario contains two different population tables $P$ and $Q$
constructed so that $I(P)=I(Q)$. The largest numerical discrepancy between
their true MI values was $1.1\times10^{-13}$ nats. Every rejection is
therefore a false positive.

The grid contains 12 table shapes from $2\times2$ to $20\times20$, nine
sampling regimes, and two variants of each regime:

$$
12\times9\times2=216\ \text{fixed population pairs}.
$$

The nine regimes have five clear roles.

| Role in the experiment | Regimes | What they test |
| --- | --- | --- |
| Controls | Well sampled; moderate | Whether a correction harms cases where normal Wald should already work |
| Intended difficult cases | Sparse and imbalanced; highly skewed and sparse; ultra-skewed and sparse; extreme sample imbalance | Whether Expanded Welch improves the low-count or unequal-sample conditions it was designed for |
| Shape robustness | Equal-MI shape mismatch | Whether equal MI remains testable when the two joint distributions have very different shapes |
| Failure stress test | Widespread sparsity | What happens when many cells, rather than a few isolated cells, lose sampled support |
| Boundary diagnostic | Zero MI | What happens at independence, where the first-order MI variance is zero |

The highly sparse regime constrains the smallest expected cell count to lie
between 1 and 5. The ultra-sparse regime places it below 1. In the widespread
sparsity regime, 25-50% of cells have expected counts below 1 and at least
half are below 5. Sample-size ratios range from $1{:}1$ to $1{:}20$.

For each population pair, 10,000 independent pairs of count tables are
sampled. Each pair is analysed by all three methods, producing

$$
216\times10{,}000=2{,}160{,}000\ \text{null replicates}.
$$

The primary result is the false-positive rate at $\alpha=0.05$. Results at
$\alpha=0.10$ and $0.01$, confidence-interval coverage, valid-result rates,
and scenario-level calibration errors are retained as supporting checks.
The exact population tables and all diagnostics are available in
[`population_scenarios.csv`](../results/supervisor_full/population_scenarios.csv).

### 7.3 Power and runtime checks

The power experiment uses five $3\times3$ alternatives with nonzero true MI
differences. It varies the absolute difference through 0.02, 0.05, and 0.10
at 300 observations per group, then varies the sample size through 150, 300,
and 600 at an absolute difference of 0.05. Each alternative receives 10,000
replicates.

The runtime experiment measures complete inference from two count tables.
It tests four table sizes from $2\times2$ to $20\times20$, repeats each method
200 times after warm-up, and reports the median elapsed time. Data loading
and construction of the count tables are excluded.

## 8. Results

### 8.1 Primary calibration result

The table reports the mean false-positive rate at the primary level
$\alpha=0.05$. The target is 0.05.

| Regime | Normal Wald | Simple Welch | Expanded Welch | Main interpretation |
| --- | ---: | ---: | ---: | --- |
| Well sampled | 0.04660 | 0.04653 | 0.04505 | All work; Expanded Welch is slightly conservative |
| Moderate | 0.04865 | 0.04840 | 0.04645 | All three remain close to nominal |
| Sparse and imbalanced | 0.05598 | 0.05545 | 0.05350 | Expanded Welch reduces false-positive inflation |
| Highly skewed and sparse | 0.05063 | 0.05050 | 0.05002 | Expanded Welch is almost exactly nominal |
| Ultra-skewed and sparse | 0.05243 | 0.05224 | 0.05159 | Expanded Welch gives the closest calibration |
| Extreme sample imbalance | 0.05628 | 0.05556 | 0.05122 | Expanded Welch removes most inflation |
| Equal-MI shape mismatch | 0.05257 | 0.05237 | 0.05095 | All are close; no consistent advantage |
| Widespread sparsity | 0.04732 | 0.04665 | 0.03673 | Expanded Welch overcorrects |
| Zero MI | 0.01381 | 0.01373 | 0.00366 | All are conservative; first-order theory is nonregular |

This table gives the central result. Expanded Welch helps in the four
positive-MI regimes it was intended to address: sparse and imbalanced,
highly sparse, ultra-sparse, and extremely unequal sample sizes. At
$\alpha=0.05$, it reduces mean absolute calibration error by approximately
18-36% relative to normal Wald in those regimes. At $\alpha=0.01$, the
corresponding reductions are approximately 25-59%.

The correction is not universal. It is unnecessary in well-sampled tables,
fails when sparsity is spread across much of the table, and is unsuitable at
the exact zero-MI boundary. Simple Welch remains very close to normal Wald
throughout, so using ordinary $n-1$ component degrees of freedom adds little.

Valid-result rates were 1.000 in the regular regimes. The main exception was
Expanded Welch under widespread sparsity, with a valid rate of 0.99154. The
full results at $\alpha=0.10$ and $0.01$, together with coverage and
scenario-level error, are retained in
[`regime_summary.csv`](../results/supervisor_full/regime_summary.csv).

### 8.2 Power

Power is the fraction of non-null replicates rejected at $\alpha=0.05$.

| Absolute MI difference | Sample size per group | Normal Wald | Simple Welch | Expanded Welch |
| ---: | ---: | ---: | ---: | ---: |
| 0.02 | 300 | 0.0768 | 0.0759 | 0.0689 |
| 0.05 | 150 | 0.1523 | 0.1498 | 0.1402 |
| 0.05 | 300 | 0.2775 | 0.2761 | 0.2652 |
| 0.05 | 600 | 0.5161 | 0.5151 | 0.5063 |
| 0.10 | 300 | 0.7449 | 0.7437 | 0.7362 |

Power increases as expected with effect size and sample size. Simple Welch
is almost indistinguishable from normal Wald. Expanded Welch loses 1.02
percentage points of power on average and at most 1.23 percentage points,
consistent with its more conservative calibration. All methods were valid in
every power replicate, and 95% coverage ranged from 0.9453 to 0.9614.

### 8.3 Computational cost

| Method | Median time across tested shapes | Relative to normal Wald |
| --- | ---: | ---: |
| Normal Wald | 0.086-0.094 ms | 1.00 times |
| Simple Welch | 0.101-0.109 ms | 1.16-1.17 times |
| Expanded Welch | 0.164-0.177 ms | 1.88-1.91 times |

Expanded Welch is roughly twice as expensive as normal Wald but remains
below 0.2 ms per table pair. All three methods are deterministic and require
$O(rc)$ time, so runtime is not a practical distinction among them and none
requires resampling.

## 9. Conclusion for Supervisor Discussion

The experiment supports a narrow but coherent story:

1. **Normal Wald remains the appropriate baseline.** It already performs
   well in ordinary, adequately sampled tables.
2. **Simple Welch changes very little.** Ordinary $n-1$ degrees of freedom do
   not capture much additional uncertainty for the MI variance estimator.
3. **Expanded Welch helps in its intended regime.** It improves calibration
   when isolated rare cells or unequal sample sizes make the estimated MI
   variance unstable, while sacrificing little power.
4. **Expanded Welch has clear limits.** It overcorrects under widespread
   support loss and at exact independence. Those cases require different
   theory rather than a stronger degrees-of-freedom correction.
5. **The computational cost is negligible.** The method is deterministic,
   $O(rc)$, and below 0.2 ms per tested table pair.

A defensible thesis claim is therefore:

> For testing equality of two positive mutual informations, an MI-specific
> Welch-Satterthwaite correction can improve finite-sample calibration in
> sparse, skewed, or unequal-sample settings when sampled support remains
> sufficiently stable. It retains near-Wald power and deterministic
> sub-millisecond runtime, but it is not intended for widespread support loss
> or the exact-independence boundary.

The main question for supervisor discussion is whether this targeted regime
is sufficiently important for the thesis contribution, and whether the next
experiment should be a pre-specified confirmatory grid restricted to the
regular positive-MI setting. The complete results remain available in
[`REPORT.md`](../results/supervisor_full/REPORT.md) and the accompanying CSV
files.

## Appendix A: Validation of the Scaled Chi-Squared Working Model

The scaled chi-squared step was tested directly rather than accepted only as
a convenient algebraic assumption. The experiment fixed 64 populations
covering $2\times2$, $3\times3$, $5\times5$, and $10\times10$ tables across
all eight sampling regimes. For each of the 128 population components, 10,000
tables estimated the finite-sample mean and variance of $\widehat V(P)$, and
a separate 10,000 tables evaluated the fitted distributions. The comparison
therefore used 2.56 million tables without reusing the moment-fitting data for
validation.

Three shape models received exactly the same empirical mean and variance:
scaled chi-squared, normal, and lognormal. This isolates the shape assumption
from errors in the first-order formulas for the moments. The average results
were:

| Moment-matched model | Mean KS distance | Mean 5% tail error | Mean 1% tail error |
| --- | ---: | ---: | ---: |
| Scaled chi-squared | 0.01988 | **0.00447** | **0.00258** |
| Normal | **0.01958** | 0.00537 | 0.00375 |
| Lognormal | 0.02915 | 0.00624 | 0.00396 |

The normal and scaled chi-squared models were effectively tied for overall
distributional fit. The normal model had the slightly smaller mean KS
distance, while scaled chi-squared gave the more accurate upper tails. The
scaled chi-squared advantage became clearer for $5\times5$ and $10\times10$
tables. For $2\times2$ tables it generally predicted more positive skewness
than was observed and could be unnecessarily conservative.

The first-order influence calculation predicted the sampling variance of
$\widehat V(P)$ well: the median ratio of empirical to predicted variance was
0.987. Its finite-sample mean approximation was less reliable, particularly
when many cells were simultaneously unobserved. This explains why a
population-centered first-order scaled chi-squared model fitted substantially
worse than the oracle shape comparison. The actual method estimates its
degrees of freedom from each observed table; the median plug-in component
degrees of freedom were 0.970 times the empirical moment degrees of freedom.

Two further runs with independent simulation seeds reproduced the result.
Across the three runs, scaled chi-squared mean KS distance ranged from 0.01988
to 0.02036, 5% tail error from 0.00436 to 0.00471, and 1% tail error from
0.00258 to 0.00275.

The simulation therefore supports scaled chi-squared as a useful
Satterthwaite working model, especially because it preserves positivity and
models upper-tail uncertainty better than the normal alternative. It does
not support treating it as an exact or universally best finite-sample law.
Its weakest cases are small tables and widespread support loss, which agrees
with the final test-calibration results.
