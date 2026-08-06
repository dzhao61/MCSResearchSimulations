# Testing Equality of Mutual Information Between Two Populations

For a longer first-principles explanation, see
[COMPREHENSIVE_SUMMARY.md](COMPREHENSIVE_SUMMARY.md).

## Research Question

Suppose two independent populations have discrete joint distributions $P$
and $Q$. The goal is to test

$$
H_0:I(P)=I(Q).
$$

The populations may have different joint distributions and different
marginal probabilities. The null hypothesis only says that their strength of
dependence, measured by mutual information (MI), is equal.

The idea follows Welch's $t$-test. Welch divides a difference in sample
means by its estimated standard error and uses Satterthwaite effective degrees
of freedom. Here, sample means are replaced by bias-corrected MI estimates and
ordinary sample variances are replaced by MI influence variances.

## Literature

- **Hutcheson (1970)** developed a Welch-Satterthwaite test for comparing two
  Shannon entropies. It is the closest classical template for comparing two
  estimated information quantities.
- **Mora and Ruiz-Castillo (2009, 2011)** studied estimation and statistical
  comparison of mutual-information-based segregation indices.
- **Allen et al. (2015)** demonstrated the importance of bias correction,
  asymptotic inference, and bootstrap validation when comparing segregation
  indices between populations.
- **Palma et al. (2022)** studied bootstrap-$t$ confidence intervals for
  Shannon diversity, making bootstrap-$t$ a relevant resampling benchmark.

The research gap is a fast, deterministic test of $I(P)=I(Q)$ for two
independent discrete populations. The potentially novel contribution is an
MI-specific calculation of uncertainty in the estimated variance, followed
by Satterthwaite moment matching. The literature search found the surrounding
components, but not this exact test.

Key references:

- Hutcheson: <https://doi.org/10.1016/0022-5193(70)90124-4>
- Mora and Ruiz-Castillo: <https://doi.org/10.1111/j.1467-9531.2011.01237.x>
- Allen et al.: <https://doi.org/10.1111/ectj.12039>
- Palma et al.: <https://arxiv.org/abs/2204.10073>

## Method

### 1. Estimate mutual information

The input is two independent $r\times c$ count tables with sample sizes
$n_P$ and $n_Q$. Convert the counts to estimated cell probabilities and
compute plug-in MI in nats:

$$
\widehat I
=\sum_{i=1}^{r}\sum_{j=1}^{c}
\widehat p_{ij}
\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

Here, $\widehat p_{ij}$ is an estimated joint probability. The corresponding
row and column marginals are

$$
\widehat p_{i+}=\sum_{j=1}^{c}\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_{i=1}^{r}\widehat p_{ij}.
$$

### 2. Correct the leading bias

Plug-in MI is positively biased in finite samples. For a positive
$r\times c$ table, its leading bias is approximately

$$
\operatorname{Bias}(\widehat I)
\approx \frac{d}{2n},
\qquad
d=(r-1)(c-1).
$$

Apply this correction separately to both tables:

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P},
\qquad
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated difference is

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

Under $H_0$, this difference should be close to zero.

### 3. Estimate the uncertainty of each MI value

For every cell, define its local-information score:

$$
\widehat\ell_{ij}
=\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The influence variance is the probability-weighted spread of these scores
around the estimated MI:

$$
\widehat V
=\sum_{i=1}^{r}\sum_{j=1}^{c}
\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I\right)^2.
$$

A larger $\widehat V$ means that the MI estimate is more sensitive to which
observations happened to appear in the sample.

### 4. Form the test statistic

Define the two contributions to the variance of the MI difference:

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Because the samples are independent, their variances add:

$$
\widehat{\operatorname{SE}}
=\sqrt{a+b}
=\sqrt{
\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}
}.
$$

The standardized test statistic is

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\widehat{\operatorname{SE}}}.
$$

Thus, $T$ is the estimated MI difference measured in standard-error units.
Large positive or negative values provide evidence against equal MI.

### 5. Choose the effective degrees of freedom

The p-value compares $T$ with a Student $t$ distribution. Fewer degrees
of freedom produce heavier tails and a more conservative test. Here,
effective degrees of freedom measure how reliably the standard error has been
estimated; they are not the number of rows, columns, or cells.

Two deterministic calculations are considered.

#### Simple Welch approximation

Treat $\widehat V_P$ and $\widehat V_Q$ like ordinary sample variances:

$$
\nu_P=n_P-1,
\qquad
\nu_Q=n_Q-1.
$$

Combine them using the Satterthwaite formula:

$$
\nu_{\mathrm{simple}}
=\frac{(a+b)^2}
{a^2/(n_P-1)+b^2/(n_Q-1)}.
$$

This is easy to calculate, but its assumption is imperfect for MI. In an
ordinary variance calculation, the value attached to each observation is
fixed. For MI, every local-information score depends on probabilities
estimated from the full table. Changing one observation changes a cell
probability and its associated row and column marginals.

#### Expanded Welch-Satterthwaite

This is an adaptation of Hutcheson's (1970) Welch-style test for comparing
two Shannon diversities. Hutcheson supplies the basic template of comparing
two estimated information quantities using their combined variance and
effective degrees of freedom. The expanded MI method adds a new step: it
derives the influence function of the complete nonlinear MI variance
estimator rather than assigning that estimator ordinary $n-1$ degrees of
freedom. See [COMPREHENSIVE_SUMMARY.md](COMPREHENSIVE_SUMMARY.md) for the
cell-contamination derivation.

This version measures how much the complete variance estimate
$\widehat V$ changes after a small change in the table. This first-order
sensitivity is the variance influence function.

For a population $P$, define

$$
\ell_{xy}=\log\!\left(\frac{p_{xy}}{p_{x+}p_{+y}}\right),
\qquad
\mu=I(P),
\qquad
m_2=\operatorname E_P(\ell^2).
$$

The influence function of the MI variance is

$$
\begin{aligned}
g_P(x,y)={}&\ell_{xy}^2-m_2 \\
&+2\left\{
\ell_{xy}
-\operatorname E_P(\ell\mid X=x)
-\operatorname E_P(\ell\mid Y=y)
+\mu
\right\} \\
&-2\mu(\ell_{xy}-\mu).
\end{aligned}
$$

Its variability determines the component degrees of freedom:

$$
\tau_P^2
=\operatorname{Var}_P\!\left\{g_P(X,Y)\right\},
\qquad
\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2},
$$

with the same calculation for $Q$.

The interpretation is straightforward:

- Stable variance estimate: $\widehat\tau^2$ is small and $\nu_V$ is
  large.
- Unstable variance estimate: $\widehat\tau^2$ is large and $\nu_V$ is
  small.
- Smaller $\nu_V$: heavier Student tails and less overconfident p-values.

The calculation is analytic. It evaluates $g$ from the observed cells and
margins rather than repeatedly removing observations or resampling. If a
small change in a rare cell strongly changes the cell, row, or column scores,
$\widehat\tau^2$ increases and the method assigns fewer degrees of freedom.

Finally, combine the two variance-component degrees of freedom:

$$
\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\nu_{V,P}+b^2/\nu_{V,Q}}.
$$

### 6. Calculate the p-value

Using either $\nu_{\mathrm{simple}}$ or $\nu_{\mathrm{expanded}}$, the
two-sided p-value is

$$
p
=2\Pr\!\left(t_\nu\ge |T|\right).
$$

Both methods use the same bias-corrected MI difference, variance estimate,
standard error, and test statistic. They differ only in the estimated
uncertainty of the variance.

Both methods are deterministic and require $O(rc)$ time and memory. The
expanded calculation performs more arithmetic per cell, but it does not
change the complexity order.

## Results

The simplified evaluation uses one grid of 216 population pairs:

$$
12\ \text{table shapes}\times18\ \text{population designs}=216.
$$

Shapes range from $2\times2$ to $20\times20$. Every pair satisfies
$I(P)=I(Q)$ while allowing $P\ne Q$. Each population pair receives 10,000
independently simulated table pairs, giving 2,160,000 null replicates in
total.

The nine regimes have direct interpretations. In addition to the original
five, the adversarial extension includes:

- **Well sampled:** equal sample sizes and high average observations per cell;
- **Moderate:** a $2{:}1$ sample-size ratio and moderate average observations
  per cell;
- **Sparse and imbalanced:** a $4{:}1$ ratio, low average observations per
  cell, and heterogeneous margins;
- **Highly skewed and sparse:** both populations have minimum true expected
  cell counts $1\leq E_{\min}<5$;
- **Ultra-skewed and sparse:** both populations have minimum true expected
  cell counts $0<E_{\min}<1$;
- **Widespread sparsity:** 25-50% of cells have expected counts below 1;
- **Equal-MI shape mismatch:** balanced $P$ and strongly skewed $Q$ have the
  same true MI;
- **Extreme sample imbalance:** sample-size ratios are $1{:}10$ or $1{:}20$;
- **Support instability:** a complete row or column has expected total below
  1 and frequently disappears from the sampled table.

Here $E_{\min}=\min_{i,j}(n p_{ij})$. Unlike average observations per cell,
this quantity detects rare cells even when the total sample size is large.

Accuracy is measured by mean absolute false-positive-rate error among valid
calculations. For example,
if a nominal $\alpha=0.05$ test rejects 6% of true null cases, its error is
$|0.06-0.05|=0.01$. Lower values are better.

The normal baseline uses the same $\widehat\Delta_{\mathrm{BC}}$,
$\widehat{\operatorname{SE}}$, and $T$, but compares $T$ with a standard
normal distribution instead of a Student distribution. Validity is a
separate performance measure because the support-instability regime can make
an analytical calculation undefined.

| Regime | Normal error at $0.05$ | Simple error | Expanded error | Expanded valid rate |
| --- | ---: | ---: | ---: | ---: |
| Well sampled | **0.00326** | 0.00332 | 0.00466 | 1.00000 |
| Moderate | 0.00370 | **0.00365** | 0.00419 | 1.00000 |
| Sparse and imbalanced | 0.00615 | 0.00565 | **0.00395** | 1.00000 |
| Highly skewed and sparse | 0.00275 | 0.00262 | **0.00217** | 1.00000 |
| Ultra-skewed and sparse | 0.00312 | 0.00296 | **0.00248** | 1.00000 |
| Widespread sparsity | **0.01064** | 0.01076 | 0.01439 | 0.99143 |
| Equal-MI shape mismatch | **0.00420** | 0.00424 | 0.00443 | 1.00000 |
| Extreme sample imbalance | 0.00876 | 0.00801 | **0.00582** | 1.00000 |
| Support instability | **0.01465** | 0.01606 | 0.02074 | 0.90405 |

Expanded Welch improved the isolated-sparsity regimes and reduced error by
33.6% under extreme sample imbalance. It did not improve shape mismatch by
itself. Under widespread sparsity it became too conservative, and under
support instability it was both less accurate and less often defined.

Across five power scenarios, expanded Welch lost 0.0102 power on average and
at most 0.0123 relative to normal Wald. Its median runtime was 0.16-0.18 ms
per table pair, approximately 1.9 times normal Wald. All methods were fully
valid outside the two support-degradation regimes.

## Conclusion

Normal Wald remains the best default in well-sampled tables. Simple Welch is
almost identical to it because its effective degrees of freedom are usually
large. Expanded Welch is useful when isolated rare cells or unequal sample
sizes make variance estimation unstable while the sampled support remains
mostly intact. It should not be used as a remedy for widespread empty cells
or disappearing rows and columns.

The clean thesis claim is therefore regime-specific: expanded Welch improves
calibration in difficult finite samples at negligible absolute computational
cost, but it should not be described as uniformly more accurate than normal
Wald. The complete reproducible output is in
[`results/supervisor_full/REPORT.md`](../results/supervisor_full/REPORT.md).
