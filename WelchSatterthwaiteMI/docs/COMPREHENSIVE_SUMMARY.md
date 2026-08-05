# Comprehensive Summary: Welch-Type Testing for Differential Mutual Information

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

The central research contribution is the expanded Welch-Satterthwaite method.
It attempts to retain the speed of an analytic test while improving
calibration in skewed, low-expected-count tables.

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

Define the local-information score for a cell:

$$
\widehat\ell_{ij}
=\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The MI influence variance for group $P$ is

$$
\widehat V_P
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I(P)\right)^2.
$$

Define $\widehat V_Q$ in the same way. Because the groups are independent,

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}.
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
calibration: it does not account for uncertainty in $\widehat V_P$ and
$\widehat V_Q$.

### Cost

It requires one pass over the table:

$$
O(rc).
$$

## 5. Method 2: Simple Welch-Satterthwaite

### How it works

Define the two estimated variance contributions:

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Simple Welch treats the MI influence variances like ordinary sample variances
and assigns

$$
\nu_P=n_P-1,
\qquad
\nu_Q=n_Q-1.
$$

Satterthwaite combines them:

$$
\nu_{\mathrm{simple}}
=\frac{(a+b)^2}
{a^2/(n_P-1)+b^2/(n_Q-1)}.
$$

The p-value becomes

$$
p_{\mathrm{simple}}
=2\Pr\{t_{\nu_{\mathrm{simple}}}\ge |T|\}.
$$

### Interpretation

A Student distribution has heavier tails than a normal distribution. Simple
Welch therefore produces slightly larger p-values and wider confidence
intervals than normal Wald.

The limitation is that $n-1$ is exact for a conventional sample variance
under classical assumptions, but $\widehat V$ is a nonlinear function of
the full contingency table. Changing one observation changes cell
probabilities, marginal probabilities, local-information scores, MI, and its
estimated variance.

### Cost

The extra Satterthwaite arithmetic is constant time after $\widehat V_P$ and
$\widehat V_Q$ are available. Overall cost remains

$$
O(rc).
$$

## 6. Method 3: Expanded Welch-Satterthwaite

### Source and adaptation

This method is inspired by **Hutcheson's (1970) test for comparing two
Shannon diversities**. Hutcheson used the same broad architecture as Welch's
test: subtract two estimated information quantities, divide by their combined
estimated standard error, and use effective degrees of freedom for the
uncertain variance terms.

The present method adapts that architecture from Shannon entropy to mutual
information. The simple version assigns ordinary $n-1$ component degrees of
freedom. The expanded version adds the MI-specific step: it derives how the
complete nonlinear MI variance estimator changes when the probability of one
cell changes, then uses that sensitivity to estimate the component degrees of
freedom. Hutcheson supplies the conceptual template; the variance-influence
derivation below supplies the MI-specific expansion.

Reference: K. Hutcheson, *A Test for Comparing Diversities Based on the
Shannon Formula*, Journal of Theoretical Biology 29 (1970), 151-154,
<https://doi.org/10.1016/0022-5193(70)90124-4>.

### Why expand the simple method?

The test statistic contains the estimated variance terms $\widehat V_P$ and
$\widehat V_Q$. Simple Welch assigns each of them ordinary $n-1$ degrees of
freedom. That assignment is appropriate for a conventional sample variance,
but $\widehat V$ is a nonlinear function of the full contingency table.

Expanded Welch instead estimates how variable $\widehat V$ is under repeated
sampling. It then converts that variability into component degrees of
freedom using the usual Satterthwaite moment-matching argument. The MI
estimate, bias correction, standard error, and observed statistic are not
changed.

Here, **IF means influence function**: the first-order change in a statistical
functional after a small perturbation of the underlying distribution.

### 6.1 Write MI and its variance as functionals of $P$

Let $Z=(X,Y)\sim P$. For a cell $(i,j)$, define its local-information score

$$
\ell_P(i,j)
=\log\!\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

Write

$$
\mu_P=I(P)=\operatorname E_P\{\ell_P(Z)\},
\qquad
m_{2,P}=\operatorname E_P\{\ell_P(Z)^2\}.
$$

The influence function of MI is

$$
\psi_P(i,j)=\ell_P(i,j)-\mu_P.
$$

Consequently, the first-order variance governing the MI estimator is

$$
V(P)
=\operatorname{Var}_P\{\psi_P(Z)\}
=m_{2,P}-\mu_P^2.
$$

The ordinary Wald standard error uses an empirical estimate $\widehat V_P$.
Expanded Welch asks a second question: **how uncertain is that estimate of
variance?**

### 6.2 Define $g_P(x,y)$ through cell contamination

Increase the probability of cell $(x,y)$ by an infinitesimal amount while
renormalizing the rest of the table:

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

The variance influence function is defined by

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Thus, $g_P(x,y)$ is the first-order change in the complete MI variance after
slightly increasing the probability of cell $(x,y)$. It includes more than
the direct effect on that cell: changing one cell also changes its row
margin, its column margin, every affected local-information score, and MI
itself.

### 6.3 Differentiate the local-information score

For an arbitrary cell $(i,j)$,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Differentiating the three logarithms along the contamination path gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}
=
\frac{\mathbf 1\{(i,j)=(x,y)\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
$$

Multiplying this derivative by $p_{ij}\ell_P(i,j)$ and summing over the table
produces

$$
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P.
$$

This is the row-and-column adjustment that is absent if the local scores are
incorrectly treated as fixed observations.

### 6.4 Differentiate the complete variance

The formula for $g_P$ is not chosen heuristically. It follows by applying the
chain rule to

$$
V(P)=m_{2,P}-\mu_P^2.
$$

First differentiate the second moment:

$$
\begin{aligned}
\operatorname{IF}_{m_2,P}(x,y)
={}&\ell_P(x,y)^2-m_{2,P}\\
&+2\Big[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P
\Big].
\end{aligned}
$$

The MI influence function is

$$
\operatorname{IF}_{\mu,P}(x,y)
=\ell_P(x,y)-\mu_P.
$$

Applying the derivative of $V(P)=m_{2,P}-\mu_P^2$ gives

$$
g_P(x,y)
=\operatorname{IF}_{m_2,P}(x,y)
-2\mu_P\operatorname{IF}_{\mu,P}(x,y),
$$

or, in full,

$$
\boxed{
\begin{aligned}
g_P(x,y)={}&
\ell_P(x,y)^2-m_{2,P}\\
&+2\Big[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P
\Big]\\
&-2\mu_P\big[\ell_P(x,y)-\mu_P\big].
\end{aligned}}
$$

The three pieces have direct meanings:

- $\ell_P(x,y)^2-m_{2,P}$ is the direct effect of moving probability mass;
- the middle term captures changes to the cell, row, and column scores;
- the final term accounts for the fact that the variance is centred around
  the estimated MI.

### 6.5 Convert $g_P$ into component degrees of freedom

Define

$$
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\}.
$$

First-order influence-function theory then gives

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite approximates the positive variance estimator by a scaled
chi-squared variable:

$$
\widehat V_P
\ \dot\sim\
V(P)\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

This approximation has mean $V(P)$ and variance $2V(P)^2/\nu_{V,P}$.
Matching that variance to $\tau_P^2/n_P$ gives

$$
\frac{2V(P)^2}{\nu_{V,P}}
=\frac{\tau_P^2}{n_P}
\quad\Longrightarrow\quad
\boxed{
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}}.
$$

In practice, the population quantities are replaced by table estimates. In
particular,

$$
\widehat\tau_P^2
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left(
\widehat g_P(i,j)
-\sum_{u,v}\widehat p_{uv}\widehat g_P(u,v)
\right)^2,
$$

and

$$
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2}.
$$

The same calculation gives $\widehat\nu_{V,Q}$.

### 6.6 Combine the two components

Recall

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Scaling a variance component does not change its component degrees of
freedom. The usual Satterthwaite combination therefore gives

$$
\boxed{
\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}+b^2/\widehat\nu_{V,Q}}}.
$$

The final p-value is

$$
p_{\mathrm{expanded}}
=2\Pr\{t_{\nu_{\mathrm{expanded}}}\ge |T|\}.
$$

Nothing before this final calibration changes: expanded Welch uses the same
bias-corrected MI difference, standard error, and statistic $T$ as normal
Wald and simple Welch. The derivation changes only the reference degrees of
freedom.

### Interpretation

If an MI variance estimate is stable, $\widehat\tau^2$ is small and the
method assigns many degrees of freedom. If it is highly sample-dependent,
$\widehat\tau^2$ is large, the degrees of freedom fall, and the Student
reference becomes more conservative.

The expanded calculation targets the main weakness of simple Welch. It is
still an approximation. Unlike an ordinary normal-sample variance,
$\widehat V_P$ is not exactly scaled chi-squared, and $T$'s numerator and
denominator are estimated from the same tables and can be correlated. The
derivation therefore justifies the moment-matched degrees of freedom; it does
not claim that the resulting Student distribution is an exact finite-sample
law.

### Cost

The influence calculation requires additional row, column, and cell
reductions, but still scans the table only a fixed number of times:

$$
O(rc).
$$

In the unified benchmark it cost approximately 1.9 times normal Wald, while
remaining below 0.2 ms per table pair for tables up to $20\times20$.

## 7. Method Map

| Feature | Normal Wald | Simple Welch | Expanded Welch |
| --- | --- | --- | --- |
| Effect estimate | Same bias-corrected MI difference | Same | Same |
| Standard error | MI influence variance | Same | Same |
| Reference | Normal | Student | Student |
| Variance uncertainty | Ignored | Approximated by $n-1$ | Derived from MI variance influence |
| Deterministic | Yes | Yes | Yes |
| Complexity | $O(rc)$ | $O(rc)$ | $O(rc)$ |
| Main role | Analytic baseline | Simple finite-df correction | Proposed analytic method |

## 8. Experimental Design

The redesigned validation uses one grid rather than several overlapping
experiments:

$$
12\ \text{table shapes}
\times3\ \text{sampling regimes}
\times2\ \text{population variants}
=72\ \text{equal-MI population pairs}.
$$

The shapes are

$$
2\times2,\ 2\times5,\ 3\times3,\ 3\times7,\ 4\times6,\ 5\times5,
\ 5\times10,\ 8\times8,\ 8\times12,\ 10\times10,\ 10\times15,
\ 20\times20.
$$

For every pair, $P$ and $Q$ are different joint distributions constructed to
satisfy $I(P)=I(Q)$ numerically. The largest absolute true MI difference over
the generated grid was $1.2\times10^{-13}$ nats.

### 8.1 Three regimes

| Regime | Target MI | Sample-size ratio | Baseline observations per cell | Purpose |
| --- | ---: | ---: | ---: | --- |
| Well sampled | 0.03 | $1{:}1$ | 100 or 200 | Check ordinary tables, including a skewed but densely sampled variant |
| Moderate | 0.07 | $1{:}2$ | 20 or 50 | Check moderate imbalance and heterogeneous margins |
| Sparse and imbalanced | 0.15 | $1{:}4$ | 10 or 25 | Target low-count and strongly unequal-sample conditions |

A minimum sample size of 120 is applied to very small tables. Within each
regime, the two variants use different random margins and association
patterns. This prevents the conclusion from depending on one particular
table structure.

### 8.2 Replication and fairness

Each population pair receives 10,000 independently sampled pairs of
multinomial tables:

$$
72\times10{,}000=720{,}000\ \text{null replicates}.
$$

Normal Wald, simple Welch, and expanded Welch are calculated on exactly the
same table pairs. All three use the same bias-corrected difference,
$\widehat{\Delta}_{\mathrm{BC}}$, and standard error. Only the reference
calibration differs.

The experiment records false-positive rates at $\alpha=0.10$, $0.05$, and
$0.01$; 95% confidence-interval coverage; valid calculation rates; effective
degrees of freedom; sample sparsity; power over five alternatives; and
end-to-end runtime. Replicates are processed in chunks, so no large replicate
file is required.

## 9. Results

### 9.1 Accuracy metric

For a nominal level $\alpha$, a calibrated method should reject
approximately an $\alpha$ fraction of true null cases. For each scenario,

$$
\operatorname{FPR\ error}
=|\operatorname{FPR}-\alpha|.
$$

The tables report mean absolute FPR error across each set. Lower is better.

### 9.2 Null calibration

| Regime | Method | Error at $0.10$ | Error at $0.05$ | Error at $0.01$ | 95% coverage |
| --- | --- | ---: | ---: | ---: | ---: |
| Well sampled | Normal Wald | **0.00570** | **0.00369** | **0.00137** | 0.95349 |
| Well sampled | Simple Welch | 0.00576 | 0.00375 | 0.00143 | 0.95355 |
| Well sampled | Expanded Welch | 0.00729 | 0.00510 | 0.00197 | 0.95493 |
| Moderate | Normal Wald | 0.00587 | 0.00395 | 0.00158 | 0.95210 |
| Moderate | Simple Welch | **0.00580** | **0.00391** | **0.00154** | 0.95231 |
| Moderate | Expanded Welch | 0.00672 | 0.00473 | 0.00176 | 0.95457 |
| Sparse and imbalanced | Normal Wald | 0.00760 | 0.00589 | 0.00278 | 0.94444 |
| Sparse and imbalanced | Simple Welch | 0.00698 | 0.00538 | 0.00248 | 0.94496 |
| Sparse and imbalanced | Expanded Welch | **0.00515** | **0.00358** | **0.00138** | 0.94694 |

In the sparse and imbalanced regime, expanded Welch reduced mean calibration
error relative to normal Wald by 32.1% at $\alpha=0.10$, 39.2% at
$\alpha=0.05$, and 50.6% at $\alpha=0.01$. It improved 22 of 24 sparse
scenarios at $\alpha=0.05$.

The correction was not uniformly beneficial. In well-sampled tables,
expanded Welch rejected too rarely and increased mean error at
$\alpha=0.05$ from 0.00369 to 0.00510. Simple Welch remained very close to
normal Wald across all regimes because its effective degrees of freedom were
usually large.

All 720,000 null replicates produced valid calculations. Across scenarios,
median simple-Welch degrees of freedom ranged from approximately 154 to
159,967, while median expanded-Welch degrees of freedom ranged from 27 to
5,250. The expanded reference is therefore meaningfully heavier-tailed in
finite samples.

### 9.3 Power

The power experiment uses five $3\times3$ alternatives that vary the true MI
difference and sample size.

| True MI difference | Sample size per group | Normal | Simple Welch | Expanded Welch |
| ---: | ---: | ---: | ---: | ---: |
| 0.02 | 300 | 0.0768 | 0.0759 | 0.0689 |
| 0.05 | 300 | 0.2775 | 0.2761 | 0.2652 |
| 0.10 | 300 | 0.7449 | 0.7437 | 0.7362 |
| 0.05 | 150 | 0.1523 | 0.1498 | 0.1402 |
| 0.05 | 600 | 0.5161 | 0.5151 | 0.5063 |

Simple Welch lost 0.0014 power on average relative to normal Wald. Expanded
Welch lost 0.0102 on average and at most 0.0123. This is the expected cost of
its heavier tails.

### 9.4 Runtime

The three methods were timed through the same implementation path.

| Shape | Normal Wald | Simple Welch | Expanded Welch |
| --- | ---: | ---: | ---: |
| $2\times2$ | 0.085 ms | 0.100 ms | 0.161 ms |
| $5\times5$ | 0.086 ms | 0.101 ms | 0.163 ms |
| $10\times10$ | 0.087 ms | 0.102 ms | 0.164 ms |
| $20\times20$ | 0.093 ms | 0.108 ms | 0.175 ms |

Expanded Welch was approximately 1.9 times the cost of normal Wald, but the
absolute cost remained below 0.2 ms per table pair in these measurements.

## 10. Final Interpretation

**Normal Wald** is the best default in well-sampled conditions. It is the
fastest method and already has good calibration there, but it becomes liberal
in the target sparse and imbalanced regime.

**Simple Welch-Satterthwaite** adds a small conservative correction with
almost no computational cost. Its $n-1$ assumption does not accurately
describe uncertainty in the nonlinear MI variance estimate, so its hard-case
improvement is limited.

**Expanded Welch-Satterthwaite** directly models uncertainty in the MI
variance estimator. It remains deterministic and $O(rc)$ and gives the best
calibration in sparse, skewed, and sample-imbalanced tables. Its heavier tails
also make it mildly conservative in well-sampled tables and reduce power by
about one percentage point in the tested alternatives.

The defensible conclusion is deliberately specific:

> Expanded Welch is a low-cost finite-sample correction for difficult
> differential-MI comparisons. It improves the target sparse regime, but it
> is not uniformly more accurate than normal Wald across all table regimes.

This is a simpler and stronger claim than treating the method as a universal
replacement. The complete reproducible output is in
[`results/supervisor_full/REPORT.md`](../results/supervisor_full/REPORT.md).

## Appendix A: Intuition Behind Expanded Welch-Satterthwaite

The test statistic is

$$
T
=\frac{\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)}
{\sqrt{\widehat V_P/n_P+\widehat V_Q/n_Q}}.
$$

The denominator estimates how much the MI difference should fluctuate under
repeated sampling. The difficulty is that $\widehat V_P$ and $\widehat V_Q$
are themselves estimated and can be unstable in finite samples.

Normal Wald treats this remaining denominator uncertainty as negligible.
Simple Welch allows for it, but assumes each MI variance behaves like an
ordinary sample variance with $n-1$ degrees of freedom. That assumption is
questionable because

$$
\widehat V
=\sum_{i,j}\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I\right)^2
$$

is a nonlinear function of the complete table. Changing one cell also
changes its row margin, column margin, local-information scores, MI, and
therefore the complete variance estimate.

Expanded Welch measures this sensitivity directly. For each cell, define

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V\!\left((1-\varepsilon)P+\varepsilon\delta_{(x,y)}\right)
\right|_{\varepsilon=0}.
$$

Thus, $g_P(x,y)$ measures how strongly cell $(x,y)$ can perturb the MI
variance. The variability of these cell sensitivities,

$$
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\},
$$

determines the first-order uncertainty of the estimated variance:

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite moment matching converts this uncertainty into component
degrees of freedom:

$$
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
$$

The interpretation is direct:

- if $g_P$ varies little across cells, $\widehat V_P$ is stable, the degrees
  of freedom are large, and the reference remains close to normal;
- if some cells have much greater influence, $\widehat V_P$ is unstable, the
  degrees of freedom fall, and the reference has heavier Student tails.

The two component degrees of freedom are then combined using the usual
Satterthwaite formula. Expanded Welch changes neither the estimated MI
difference nor its standard error; it changes only how cautiously the
observed statistic is interpreted.

This is why the method helps in sparse and skewed tables. It responds to the
actual table-dependent instability of the variance estimate rather than
assigning degrees of freedom from sample size alone. In the validation grid,
it reduced sparse-regime calibration error relative to normal Wald by about
39% at $\alpha=0.05$ and 51% at $\alpha=0.01$.

The improvement is not universal. In well-sampled tables, normal Wald is
already accurate and expanded Welch can become mildly conservative. It is
therefore best interpreted as a targeted finite-sample correction rather
than a universal replacement for normal Wald.
