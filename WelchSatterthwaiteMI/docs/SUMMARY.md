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

### 6.1 Begin with the Welch-Satterthwaite equation

For independent variance estimates $s_i^2$, positive weights $k_i$, and
component degrees of freedom $\nu_i$, the original Welch-Satterthwaite
equation is

$$
\nu
=
\frac{
\left(\sum_i k_i s_i^2\right)^2
}{
\sum_i (k_i s_i^2)^2/\nu_i
}.
$$

For two MI estimates this becomes

$$
\nu
=
\frac{
(k_Ps_P^2+k_Qs_Q^2)^2
}{
(k_Ps_P^2)^2/\nu_P+(k_Qs_Q^2)^2/\nu_Q
}.
$$

The derivation therefore has two tasks. First, identify the variance
contributions $k_Ps_P^2$ and $k_Qs_Q^2$. Second, calculate the component
degrees of freedom $\nu_P$ and $\nu_Q$ that describe the reliability of those
variance estimates.

### 6.2 Identify the MI variance contributions

For population $P$, define pointwise mutual information, MI, and the variance
of pointwise mutual information by

$$
\ell_P(i,j)
=
\log\!\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right),
\qquad
I(P)=\sum_{i,j}p_{ij}\ell_P(i,j),
$$

and

$$
V(P)
=
\operatorname{Var}_P\{\ell_P(X,Y)\}
=
\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2.
$$

A first-order Taylor expansion of plug-in MI gives

$$
\widehat I(P)-I(P)
\approx
\sum_{i,j}\ell_P(i,j)(\widehat p_{ij}-p_{ij})
=
\frac{1}{n_P}
\sum_{a=1}^{n_P}
\{\ell_P(Z_a^{(P)})-I(P)\}.
$$

The terms in this average are independent and each has variance $V(P)$.
Consequently,

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)\}
&\approx
\operatorname{Var}\!\left[
\frac{1}{n_P}\sum_{a=1}^{n_P}
\{\ell_P(Z_a^{(P)})-I(P)\}
\right]\\
&=
\frac{1}{n_P^2}\sum_{a=1}^{n_P}V(P)
=
\frac{V(P)}{n_P}.
\end{aligned}
$$

The observed table replaces $V(P)$ by $\widehat V(P)$. Thus the quantities
in the original Welch-Satterthwaite equation are

$$
s_P^2=\widehat V(P),
\qquad
k_P=\frac{1}{n_P},
\qquad
k_Ps_P^2
=
\frac{\widehat V(P)}{n_P}
=
\widehat{\operatorname{Var}}\{\widehat I(P)\}.
$$

The two independent samples therefore give

$$
\widehat{\operatorname{SE}}^2
=
k_Ps_P^2+k_Qs_Q^2
=
\frac{\widehat V(P)}{n_P}
+
\frac{\widehat V(Q)}{n_Q}.
$$

### 6.3 Express each component degree of freedom by moment matching

The remaining quantity for population $P$ is $\nu_P$. Satterthwaite models
the positive variance estimate $\widehat V(P)$ by

$$
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_P}}{\nu_P}.
$$

A chi-squared model is used because classical variance estimators have this
form, while its degrees of freedom directly control the relative variability
of a positive variance estimate. Since

$$
\operatorname E(\chi^2_{\nu_P})=\nu_P,
\qquad
\operatorname{Var}(\chi^2_{\nu_P})=2\nu_P,
$$

the scaled model has

$$
\operatorname E\!\left[
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_P}}{\nu_P}
\right]
=
\operatorname E\{\widehat V(P)\},
$$

and

$$
\operatorname{Var}\!\left[
\operatorname E\{\widehat V(P)\}
\frac{\chi^2_{\nu_P}}{\nu_P}
\right]
=
\frac{2[\operatorname E\{\widehat V(P)\}]^2}{\nu_P}.
$$

Matching this variance to the sampling variance of $\widehat V(P)$ gives

$$
\boxed{
\nu_P
=
\frac{
2[\operatorname E\{\widehat V(P)\}]^2
}{
\operatorname{Var}\{\widehat V(P)\}
}.
}
$$

To first order, $\operatorname E\{\widehat V(P)\}\approx V(P)$. Deriving
$\nu_P$ therefore reduces to finding
$\operatorname{Var}\{\widehat V(P)\}$.

### 6.4 Calculate the effect of one observation

Move a small amount of probability toward cell $(x,y)$ through

$$
P_\varepsilon
=
(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

For any cell $(i,j)$,

$$
p_{ij}(\varepsilon)
=
(1-\varepsilon)p_{ij}
+
\varepsilon\mathbf 1\{i=x,j=y\},
$$

so the joint and marginal probability changes at $\varepsilon=0$ are

$$
\left.\frac{\mathrm d}{\mathrm d\varepsilon}
p_{ij}(\varepsilon)\right|_{\varepsilon=0}
=
\mathbf 1\{i=x,j=y\}-p_{ij},
$$

$$
\left.\frac{\mathrm d}{\mathrm d\varepsilon}
p_{i+}(\varepsilon)\right|_{\varepsilon=0}
=
\mathbf 1\{i=x\}-p_{i+},
\qquad
\left.\frac{\mathrm d}{\mathrm d\varepsilon}
p_{+j}(\varepsilon)\right|_{\varepsilon=0}
=
\mathbf 1\{j=y\}-p_{+j}.
$$

Differentiating the three logarithms in PMI gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}
=
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-
\frac{\mathbf 1\{i=x\}}{p_{i+}}
-
\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
$$

When MI is differentiated, the probability changes contribute

$$
\sum_{i,j}\ell_P(i,j)
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}
=
\ell_P(x,y)-I(P),
$$

while the probability-weighted PMI derivatives sum to
$1-1-1+1=0$. Therefore,

$$
\boxed{
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=
\ell_P(x,y)-I(P).
}
$$

### 6.5 Differentiate the MI variance

Write the PMI variance as

$$
V(P)=M_2(P)-I(P)^2,
\qquad
M_2(P)=\operatorname E_P\{\ell_P(X,Y)^2\}.
$$

The change in $V(P)$ caused by an observation in cell $(x,y)$ is

$$
\begin{aligned}
g_P(x,y)
&=
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}\\
&=
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-
2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Differentiate

$$
M_2(P_\varepsilon)
=
\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j)^2
$$

with the product rule:

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&
\sum_{i,j}
\left.\frac{\mathrm d p_{ij}(\varepsilon)}{\mathrm d\varepsilon}
\right|_{\varepsilon=0}
\ell_P(i,j)^2\\
&+
2\sum_{i,j}p_{ij}\ell_P(i,j)
\left.\frac{\mathrm d\ell_{P_\varepsilon}(i,j)}
{\mathrm d\varepsilon}\right|_{\varepsilon=0}.
\end{aligned}
$$

The first sum is

$$
\ell_P(x,y)^2-M_2(P).
$$

Substituting the PMI derivative into the second sum gives

$$
\begin{aligned}
&\sum_{i,j}p_{ij}\ell_P(i,j)
\left.\frac{\mathrm d\ell_{P_\varepsilon}(i,j)}
{\mathrm d\varepsilon}\right|_{\varepsilon=0}\\
&\qquad=
\ell_P(x,y)
-\operatorname E_P\{\ell_P(X,Y)\mid X=x\}
-\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}
+I(P).
\end{aligned}
$$

Combining these results with the MI derivative produces

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

The conditional row and column means account for the marginal probabilities
that change when one cell changes.

### 6.6 Convert variance sensitivity into component degrees of freedom

The variability of the observation-level effects is

$$
\tau^2(P)
=
\operatorname{Var}_P\{g_P(X,Y)\}.
$$

A first-order expansion of the complete variance estimate gives

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}
\sum_{a=1}^{n_P}g_P(Z_a^{(P)}).
$$

The observations are independent, so

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&\approx
\frac{1}{n_P^2}
\sum_{a=1}^{n_P}\operatorname{Var}_P\{g_P(Z_a^{(P)})\}\\
&=
\frac{n_P\tau^2(P)}{n_P^2}
=
\frac{\tau^2(P)}{n_P}.
\end{aligned}
$$

Substitution into the component moment-matching equation gives

$$
\boxed{
\nu_P
\approx
\frac{2n_PV(P)^2}{\tau^2(P)}.
}
$$

Thus a stable estimate of $V(P)$ has large component degrees of freedom,
whereas an estimate that changes strongly between samples has small component
degrees of freedom.

### 6.7 Calculate the component degrees of freedom from the table

Replace the population quantities by values calculated from the observed
table. For each occupied cell $\widehat p_{ij}>0$, calculate

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
\right].
\end{aligned}
$$

Then calculate

$$
\overline g_P
=
\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j),
$$

$$
\widehat\tau^2(P)
=
\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2,
$$

and

$$
\boxed{
\widehat\nu_P
=
\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
}
$$

Applying the same calculation to the second table gives $\widehat\nu_Q$.

### 6.8 Combine the components and complete the test

Substitute the MI variance contributions and their component degrees of
freedom into the original Welch-Satterthwaite equation:

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=
\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_P
+
\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_Q
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

Large component degrees of freedom make the Student reference approach the
normal reference. Greater uncertainty in either MI variance estimate lowers
the effective degrees of freedom and gives the reference distribution heavier
tails.

The calculation is deterministic, requires $O(rc)$ time, and cost
approximately 1.9 times Normal Wald in the unified benchmark while remaining
below 0.2 ms per table pair for the tested tables up to $8\times8$.

The complete cell-by-cell derivation and theoretical justification are given
in [Expanded Welch-Satterthwaite Derivation](EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md).

## 7. Experimental Design

### 7.1 Repeated-sampling experiment

For every configuration, two fixed $r\times c$ population tables satisfy

$$
H_0:I(P)=I(Q)=0.10\ \text{nats},
$$

while $P$ and $Q$ remain different joint distributions. Independent sampled
count tables are generated by

$$
N^{(P)}\sim\operatorname{Multinomial}(n_P,P),
\qquad
N^{(Q)}\sim\operatorname{Multinomial}(n_Q,Q).
$$

The three methods analyse the same table pair in every replicate. They use
the same bias-corrected MI difference and standard error; only their reference
calibration differs. The primary significance level is $\alpha=0.05$, so a
calibrated test should reject about 5% of null replicates.

### 7.2 Sixteen pre-specified configurations

The design crosses four table shapes with four sampling conditions:

$$
(2,2),\ (3,3),\ (5,5),\ (8,8).
$$

- **Balanced control:** uniform row and column margins and equal sample sizes.
- **Moderate sparsity:** one row and one column each have probability 0.70;
  the remaining probability is divided equally among the other categories.
- **Ultra-sparsity:** the dominant row and column probabilities increase to
  0.90, with equal sample sizes.
- **Ultra-sparsity with imbalance:** the same 0.90 margins, but $n_Q=5n_P$.

The exact sample sizes are fixed in advance:

| Shape | Balanced control | Moderate sparsity | Ultra-sparsity | Ultra-sparsity with imbalance |
| --- | ---: | ---: | ---: | ---: |
| $2\times2$ | $(100,100)$ | $(50,50)$ | $(50,50)$ | $(50,250)$ |
| $3\times3$ | $(135,135)$ | $(72,72)$ | $(50,50)$ | $(50,250)$ |
| $5\times5$ | $(375,375)$ | $(200,200)$ | $(75,75)$ | $(75,375)$ |
| $8\times8$ | $(960,960)$ | $(512,512)$ | $(192,192)$ | $(192,960)$ |

Each entry is $(n_P,n_Q)$. All sample sizes lie between 50 and 1,000.

For a given margin template, an ordinal, checkerboard, or cyclic interaction
is scaled numerically until MI equals 0.10 nats. Rows and columns are then
relabelled independently for $P$ and $Q$. Accepted pairs have strictly
positive probabilities, differ by at least 0.05 in $L^1$ distance, and have
positive first-order MI variance. Across the accepted populations, the
largest numerical error in $I(P)-I(Q)$ was $6.8\times10^{-14}$ nats.

The planned observations-per-cell value controls total sample size, but
skewed margins make the expected cell counts highly unequal. The following
diagnostics describe the smaller sample. The minimum expected count is the
median across the ten population repetitions; the last two columns are the
mean fractions of cells below the stated thresholds.

| Shape | Condition | Minimum expected count | Fraction $E_{ij}<1$ | Fraction $E_{ij}<5$ |
| --- | --- | ---: | ---: | ---: |
| $2\times2$ | Balanced control | 14.010 | 0.000 | 0.000 |
| $2\times2$ | Moderate sparsity | 5.714 | 0.000 | 0.000 |
| $2\times2$ | Ultra-sparsity | 1.917 | 0.000 | 0.750 |
| $2\times2$ | Ultra-sparsity with imbalance | 1.917 | 0.000 | 0.750 |
| $3\times3$ | Balanced control | 6.967 | 0.000 | 0.000 |
| $3\times3$ | Moderate sparsity | 1.160 | 0.089 | 0.622 |
| $3\times3$ | Ultra-sparsity | 0.109 | 0.456 | 0.889 |
| $3\times3$ | Ultra-sparsity with imbalance | 0.174 | 0.422 | 0.889 |
| $5\times5$ | Balanced control | 7.937 | 0.000 | 0.016 |
| $5\times5$ | Moderate sparsity | 0.531 | 0.224 | 0.700 |
| $5\times5$ | Ultra-sparsity | 0.015 | 0.800 | 0.960 |
| $5\times5$ | Ultra-sparsity with imbalance | 0.016 | 0.800 | 0.960 |
| $8\times8$ | Balanced control | 5.032 | 0.000 | 0.028 |
| $8\times8$ | Moderate sparsity | 0.417 | 0.303 | 0.770 |
| $8\times8$ | Ultra-sparsity | 0.011 | 0.867 | 0.984 |
| $8\times8$ | Ultra-sparsity with imbalance | 0.011 | 0.866 | 0.984 |

The exact probability tables and diagnostics are retained in
[`population_scenarios.csv`](../results/supervisor_16_config/population_scenarios.csv).

### 7.3 Replication and reported metrics

Each of the 16 configurations uses ten independently seeded population-pair
constructions and sampling streams. Every population pair receives 5,000
sampled table pairs:

$$
16\times10\times5{,}000=800{,}000\ \text{null table pairs}.
$$

The configuration-level result is the equal-weight mean of its ten
population-specific rejection rates. At a true rejection probability of
0.05, the Monte Carlo standard error for one 5,000-replicate population is
approximately 0.0031; pooling 50,000 replicates in one configuration gives a
reference value of approximately 0.0010. Population-level standard
deviations and standard errors are retained rather than treating all
replicates as one undifferentiated sample.

The reported metrics are:

- **False-positive rate (FPR):** the fraction of valid null replicates with
  p-value at or below $\alpha$.
- **Absolute calibration error:** $|\widehat{\mathrm{FPR}}-\alpha|$; lower is
  better.
- **95% coverage:** the fraction of valid null confidence intervals that
  contain the true MI difference, zero.
- **Valid rate:** the fraction of replicates producing a finite statistic,
  p-value, and required degrees of freedom.
- **Power:** the fraction of valid alternative replicates correctly rejected
  at $\alpha=0.05$.

The primary comparison is at $\alpha=0.05$. Results at 0.10 and 0.01 are
secondary checks. Rejection-calibration curves evaluate 101 nominal levels
from 0 to 0.10; their bands show the 10th and 90th percentiles across
population repetitions. Seeds, software versions, and the experiment-script
hash are recorded in
[`run_metadata.json`](../results/supervisor_16_config/run_metadata.json).

### 7.4 Power and runtime designs

The power experiment uses $3\times3$ tables. Population $P$ has uniform row
and column margins $(1/3,1/3,1/3)$ and $I(P)=0.05$. Population $Q$ has row
and column margins $(0.9,0.05,0.05)$ and a larger MI. Both use the same
ordinal interaction pattern. The five alternatives are:

| Purpose | $I(P)$ | $I(Q)$ | $n_P$ | $n_Q$ | Minimum $n_Pp_{ij}$ | Minimum $n_Qq_{ij}$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Effect size 0.02 | 0.05 | 0.07 | 300 | 300 | 18.217 | 1.543 |
| Effect size 0.05 | 0.05 | 0.10 | 300 | 300 | 18.217 | 1.853 |
| Effect size 0.10 | 0.05 | 0.15 | 300 | 300 | 18.217 | 1.143 |
| Smaller sample | 0.05 | 0.10 | 150 | 150 | 9.108 | 0.926 |
| Larger sample | 0.05 | 0.10 | 600 | 600 | 36.433 | 3.705 |

Each alternative receives 10,000 replicates. Power is the fraction of valid
replicates rejected at $\alpha=0.05$. The power experiment therefore contains
50,000 independently sampled table pairs.

The runtime experiment measures one complete method call after the count
tables have been constructed. It uses $(r,c,n_P,n_Q)$ equal to
$(2,2,100,100)$, $(3,3,135,135)$, $(5,5,375,375)$, and
$(8,8,960,960)$. Each method is warmed up and then timed 200 times on
each fixed table pair; the reported value is the median. This gives 2,400
timed complete method calls.

## 8. Results

### 8.1 Rejection calibration

![Rejection calibration across nominal significance levels](../results/supervisor_16_config/rejection_calibration.png)

The diagonal is perfect calibration. Curves above it are liberal and curves
below it are conservative. Each curve is the equal-weight mean over the 40
population repetitions in a sampling condition, while the shaded region
shows their 10th to 90th percentiles.

The balanced curves remain close to the diagonal. Expanded Welch becomes
more conservative in the moderate condition, moves the mean ultra-sparse
curve toward the diagonal, and substantially reduces the inflation caused by
combining ultra-sparsity with a 5:1 sample-size ratio. It does not completely
calibrate that final condition.

### 8.2 Results in every configuration

Each entry is the mean FPR over ten population repetitions. The target is
0.05.

![False-positive rates for all configurations](../results/supervisor_16_config/configuration_fpr.png)

| Shape | Condition | $(n_P,n_Q)$ | Normal Wald | Simple Welch | Expanded Welch |
| --- | --- | ---: | ---: | ---: | ---: |
| $2\times2$ | Balanced control | $(100,100)$ | 0.04872 | 0.04726 | 0.04148 |
| $2\times2$ | Moderate sparsity | $(50,50)$ | 0.04886 | 0.04464 | 0.03928 |
| $2\times2$ | Ultra-sparsity | $(50,50)$ | 0.06350 | 0.05868 | 0.04944 |
| $2\times2$ | Ultra-sparsity with imbalance | $(50,250)$ | 0.11756 | 0.11420 | 0.06391 |
| $3\times3$ | Balanced control | $(135,135)$ | 0.04774 | 0.04678 | 0.04226 |
| $3\times3$ | Moderate sparsity | $(72,72)$ | 0.05384 | 0.05126 | 0.04386 |
| $3\times3$ | Ultra-sparsity | $(50,50)$ | 0.07711 | 0.07031 | 0.05755 |
| $3\times3$ | Ultra-sparsity with imbalance | $(50,250)$ | 0.13560 | 0.13294 | 0.09572 |
| $5\times5$ | Balanced control | $(375,375)$ | 0.04716 | 0.04688 | 0.04522 |
| $5\times5$ | Moderate sparsity | $(200,200)$ | 0.04466 | 0.04406 | 0.04084 |
| $5\times5$ | Ultra-sparsity | $(75,75)$ | 0.07320 | 0.07020 | 0.06180 |
| $5\times5$ | Ultra-sparsity with imbalance | $(75,375)$ | 0.17472 | 0.17188 | 0.12447 |
| $8\times8$ | Balanced control | $(960,960)$ | 0.04756 | 0.04740 | 0.04674 |
| $8\times8$ | Moderate sparsity | $(512,512)$ | 0.03632 | 0.03604 | 0.03470 |
| $8\times8$ | Ultra-sparsity | $(192,192)$ | 0.04112 | 0.04058 | 0.03734 |
| $8\times8$ | Ultra-sparsity with imbalance | $(192,960)$ | 0.24616 | 0.24368 | 0.22340 |

The strongest result is in the difficult, unequal-sample configurations.
Expanded Welch lowers FPR in all four shapes, including 0.11756 to 0.06391
for $2\times2$ and 0.17472 to 0.12447 for $5\times5$. The correction becomes
less sufficient as the table widens: the $8\times8$ FPR remains 0.22340.

For equal-size ultra-sparse tables, Expanded Welch improves the $2\times2$,
$3\times3$, and $5\times5$ results. The $8\times8$ case is already
conservative under Normal Wald, so Expanded Welch moves it farther below
0.05. The balanced and moderate conditions show the same tradeoff on a
smaller scale: the correction is usually unnecessary and introduces modest
conservatism.

### 8.3 Results averaged by sampling condition

Mean absolute error is averaged over the 40 population repetitions in each
condition, so liberal and conservative errors cannot cancel.

| Condition | Normal FPR | Simple FPR | Expanded FPR | Normal mean error | Expanded mean error | Expanded valid rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced control | 0.04780 | 0.04708 | 0.04393 | 0.00346 | 0.00627 | 1.00000 |
| Moderate sparsity | 0.04592 | 0.04400 | 0.03967 | 0.00677 | 0.01033 | 1.00000 |
| Ultra-sparsity | 0.06373 | 0.05994 | 0.05153 | 0.01817 | 0.00866 | 0.99036 |
| Ultra-sparsity with imbalance | 0.16851 | 0.16568 | 0.12687 | 0.11851 | 0.07687 | 0.99498 |

Expanded Welch approximately halves mean absolute error in the equal-size
ultra-sparse condition and reduces it by about one third under ultra-sparse
5:1 imbalance. The control conditions establish the cost of that heavier-tail
calibration: mean absolute error increases by roughly 0.003 when Normal Wald
is already close to nominal. Simple Welch makes only a small change in every
condition.

The Expanded Welch valid rate is 1.0 in the control conditions. It falls to
0.99036 in equal-size ultra-sparse tables because some sampled tables have
degenerate empirical variance components. Validity is therefore reported
separately from FPR.

Complete population-level results, including Monte Carlo intervals,
effective degrees of freedom, and sparsity diagnostics, are in
[`scenario_results.csv`](../results/supervisor_16_config/scenario_results.csv).

### 8.4 Power

The table repeats the exact alternative settings alongside the resulting
power at $\alpha=0.05$.

| $I(P)$ | $I(Q)$ | $(n_P,n_Q)$ | Minimum expected counts $(P,Q)$ | Normal Wald | Simple Welch | Expanded Welch |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.07 | $(300,300)$ | $(18.217,1.543)$ | 0.0768 | 0.0759 | 0.0689 |
| 0.05 | 0.10 | $(150,150)$ | $(9.108,0.926)$ | 0.1523 | 0.1498 | 0.1402 |
| 0.05 | 0.10 | $(300,300)$ | $(18.217,1.853)$ | 0.2775 | 0.2761 | 0.2652 |
| 0.05 | 0.10 | $(600,600)$ | $(36.433,3.705)$ | 0.5161 | 0.5151 | 0.5063 |
| 0.05 | 0.15 | $(300,300)$ | $(18.217,1.143)$ | 0.7449 | 0.7437 | 0.7362 |

Power increases with both the true MI difference and sample size. Simple
Welch is almost indistinguishable from Normal Wald. Expanded Welch loses
1.02 percentage points of power on average and at most 1.23 percentage
points. All methods are valid in every power replicate, and 95% coverage
ranges from 0.9453 to 0.9614.

### 8.5 Computational cost

| Shape | $(n_P,n_Q)$ | Normal Wald | Simple Welch | Expanded Welch |
| ---: | ---: | ---: | ---: | ---: |
| $2\times2$ | $(100,100)$ | 0.0858 ms | 0.1000 ms | 0.1638 ms |
| $3\times3$ | $(135,135)$ | 0.0803 ms | 0.0944 ms | 0.1524 ms |
| $5\times5$ | $(375,375)$ | 0.0810 ms | 0.0947 ms | 0.1532 ms |
| $8\times8$ | $(960,960)$ | 0.0811 ms | 0.0949 ms | 0.1540 ms |

Expanded Welch takes 1.89-1.91 times as long as Normal Wald in this benchmark
but remains below 0.2 ms per table pair. All three methods are deterministic
and require $O(rc)$ time; none requires resampling.

## 9. Conclusion for Supervisor Discussion

The pre-specified 16-configuration experiment supports a narrow but coherent
story:

1. **Normal Wald remains strong in ordinary settings.** Its balanced-control
   mean FPR is 0.04780, leaving little room for correction.
2. **Simple Welch changes very little.** Ordinary $n-1$ degrees of freedom do
   not capture much additional uncertainty for the MI variance estimator.
3. **Expanded Welch helps in its intended regime.** In equal-size
   ultra-sparse tables it changes mean FPR from 0.06373 to 0.05153. Under
   ultra-sparse 5:1 imbalance it changes 0.16851 to 0.12687.
4. **Expanded Welch has clear limits.** It is mildly conservative when the
   correction is unnecessary and does not solve the widest sparse,
   unequal-sample tables. Its equal-size ultra-sparse valid rate is 0.99036.
5. **The computational cost is negligible.** The method is deterministic,
   $O(rc)$, and approximately 0.15 ms per tested table pair.

A defensible thesis claim is therefore:

> For testing equality of two positive mutual informations, an MI-specific
> Welch-Satterthwaite correction improves finite-sample calibration in several
> ultra-sparse positive-MI settings, particularly when sample sizes are
> unequal. It retains near-Wald power and deterministic sub-millisecond
> runtime, but is conservative in some easier settings and remains imperfect
> for wide ultra-sparse tables.

The main supervisor question is therefore not whether the correction is
uniformly better; the experiment shows that it is not. The question is
whether its deterministic improvement in sparse, unequal-sample comparisons
is a sufficiently useful and clearly delimited thesis contribution. The
complete results are available in
[`REPORT.md`](../results/supervisor_16_config/REPORT.md) and the accompanying
CSV files.

## Appendix A: Validation of the Scaled Chi-Squared Working Model

The scaled chi-squared step was also tested in a separate mechanism audit,
distinct from the bounded primary experiment above. The audit fixed 64
populations covering $2\times2$, $3\times3$, $5\times5$, and $10\times10$
tables across an earlier broad regime set. For each of the 128 population components, 10,000
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
