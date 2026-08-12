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

### 7.1 Question and repeated-sampling experiment

The null hypothesis is

$$
H_0:I(P)=I(Q),
$$

where MI is measured in nats. For every scenario, $P$ and $Q$ are fixed
$r\times c$ population probability tables. Independent count tables are then
drawn as

$$
N^{(P)}\sim\operatorname{Multinomial}(n_P,P),
\qquad
N^{(Q)}\sim\operatorname{Multinomial}(n_Q,Q).
$$

Normal Wald, Simple Welch, and Expanded Welch analyse the same two sampled
tables in every replicate. They use the same bias-corrected MI difference and
the same estimated standard error; only the reference distribution changes.
The primary significance level is $\alpha=0.05$. Under the null, a calibrated
test should reject in approximately 5% of repeated samples.

### 7.2 Common table grid and population construction

Every regime uses six practical table shapes:

$$
(2,2),\ (2,5),\ (3,3),\ (3,5),\ (5,5),\ (8,8).
$$

Each regime has two variants, giving

$$
6\ \text{shapes}\times5\ \text{regimes}\times2\ \text{variants}
=60\ \text{fixed population pairs}.
$$

Every generated scenario is required to satisfy

$$
50\le n_P\le1000,
\qquad
50\le n_Q\le1000.
$$

The two variants in every regime use the same positive-MI targets,
$I(P)=I(Q)=0.10$ and $0.15$ nats. This keeps the comparison away from the
near-zero boundary and prevents MI magnitude from being confounded with the
sampling regime.

For each population, the row and column margins are drawn independently from
a symmetric Dirichlet distribution with concentration $a_P$ or $a_Q$. A
large concentration, such as 50, produces margins close to uniform; values
below 1 produce increasingly uneven margins with rare categories. A random
log-linear interaction pattern is then scaled numerically until the joint
table has the required MI. The two tables use independently generated
margins and interactions, but both are tuned to the same target:

$$
I(P)=I(Q).
$$

Accepted pairs have strictly positive population probabilities, differ by at
least 0.05 in $L^1$ distance, and have nondegenerate first-order MI variance.
The largest numerical difference between $I(P)$ and $I(Q)$ in the accepted
grid was $8.5\times10^{-14}$ nats.

For fixed-density designs, the sample sizes are

$$
n_P=\max(n_{\min},drc),
\qquad
n_Q=\rho n_P,
$$

where $d$ is the planned number of observations per cell in the smaller
sample, $n_{\min}$ is the regime-specific lower bound, and
$\rho=n_Q/n_P$. Every design is chosen so that $n_Q\le1000$.

For the expected-count designs, define the true expected count in cell
$(i,j)$ by

$$
E^{(P)}_{ij}=n_Pp_{ij},
\qquad
E^{(Q)}_{ij}=n_Qq_{ij}.
$$

The sample sizes are chosen after the two population tables are generated so
that their minimum expected counts, or their fractions of low-count cells,
satisfy the stated constraints.

### 7.3 Exact regime specifications

The complete generating settings are shown below. The pair $(a_P,a_Q)$ gives
the two Dirichlet concentrations, $\rho$ is the sample-size ratio
$n_Q:n_P$, and $d$ is used in the fixed-density formula above.

| Regime and variant | $I(P)=I(Q)$ | $(a_P,a_Q)$ | $n_Q:n_P$ | Sample-size or sparsity rule |
| --- | ---: | ---: | ---: | --- |
| Well sampled 1 | 0.10 | $(50,50)$ | $1{:}1$ | $d=15$, $n_{\min}=200$ |
| Well sampled 2 | 0.15 | $(50,50)$ | $1{:}1$ | $d=15$, $n_{\min}=200$ |
| Moderate 1 | 0.10 | $(8,4)$ | $1{:}1$ | $d=8$, $n_{\min}=100$ |
| Moderate 2 | 0.15 | $(8,2)$ | $2{:}1$ | $d=6$, $n_{\min}=100$ |
| Highly skewed and sparse 1 | 0.10 | $(2,2)$ | $1{:}1$ | Both minimum expected counts in $[1,5)$ |
| Highly skewed and sparse 2 | 0.15 | $(10,2)$ | $2{:}1$ | Both minimum expected counts in $[1,5)$ |
| Ultra-skewed and sparse 1 | 0.10 | $(0.8,0.8)$ | $1{:}1$ | Both minimum expected counts in $[0.05,1)$ |
| Ultra-skewed and sparse 2 | 0.15 | $(10,0.8)$ | $10{:}1$ | Both minimum expected counts in $[0.05,1)$ |
| Widespread sparsity 1 | 0.10 | $(0.35,0.35)$ | $1{:}1$ | In both tables, 25-50% of cells have $E_{ij}<1$ and at least 50% have $E_{ij}<5$ |
| Widespread sparsity 2 | 0.15 | $(1,0.35)$ | $2{:}1$ | Same cell-wide constraints with unequal samples |

The first four regimes form the main practical comparison. Widespread
sparsity is retained as a boundary check because losing support in many cells
can make the first-order variance calculation undefined.

### 7.4 Realized sample sizes and expected counts

The previous table states the construction rules. The following table reports
the values actually realized across the six shapes in each variant. The final
column is

$$
\min_{i,j}\{n_Pp_{ij},n_Qq_{ij}\},
$$

the smallest true joint expected count across the two populations.

| Regime and variant | Realized $n_P$ | Realized $n_Q$ | $n_P/(rc)$ | Smallest expected count |
| --- | ---: | ---: | ---: | ---: |
| Well sampled 1 | 200-960 | 200-960 | 15.00-50.00 | 2.140-18.228 |
| Well sampled 2 | 200-960 | 200-960 | 15.00-50.00 | 1.385-15.015 |
| Moderate 1 | 100-512 | 100-512 | 8.00-25.00 | 0.790-6.927 |
| Moderate 2 | 100-384 | 200-768 | 6.00-25.00 | 0.057-1.178 |
| Highly skewed and sparse 1 | 52-975 | 52-975 | 13.00-30.78 | 1.025-4.072 |
| Highly skewed and sparse 2 | 54-460 | 108-920 | 7.19-48.11 | 1.096-4.201 |
| Ultra-skewed and sparse 1 | 64-604 | 64-604 | 7.11-35.67 | 0.052-0.413 |
| Ultra-skewed and sparse 2 | 51-75 | 510-750 | 1.17-12.75 | 0.057-0.632 |
| Widespread sparsity 1 | 50-435 | 50-435 | 3.67-17.40 | $<0.001$-0.042 |
| Widespread sparsity 2 | 50-414 | 100-828 | 4.23-16.56 | $<0.001$-0.312 |

The exact $P$, $Q$, $n_P$, and $n_Q$ for every shape are recorded in
[`population_scenarios.csv`](../results/supervisor_practical/population_scenarios.csv).

### 7.5 Replication and reported metrics

Each of the 60 fixed population pairs receives 10,000 independently sampled
table pairs:

$$
60\times10{,}000=600{,}000\ \text{null replicates}.
$$

Each replicate contains one table from $P$ and one from $Q$, so this is
600,000 table pairs, or 1.2 million individual sampled tables.

The population-generation seed is 2,026,080,501 and the sampling seed is
2,026,080,502. Scenario-specific seeds are derived deterministically from
these values, so the complete experiment is reproducible. The seeds,
replicate counts, software versions, and experiment-script hash are recorded
in [`run_metadata.json`](../results/supervisor_practical/run_metadata.json).

At a true rejection probability of 0.05, 10,000 replicates give a Monte Carlo
standard error of approximately 0.00218 for an individual scenario. The
following quantities are reported:

- **Scenario false-positive rate:** the fraction of valid null replicates
  with p-value below $\alpha$.
- **Regime mean false-positive rate:** the arithmetic mean of the 12 scenario
  rates in that regime. Every shape and variant receives equal weight.
- **Mean absolute calibration error:** the mean, over the 12 scenarios, of
  $|\widehat{\mathrm{FPR}}-\alpha|$. This avoids cancellation between liberal
  and conservative scenarios.
- **95% coverage:** the fraction of valid null replicates whose method-specific
  95% confidence interval contains the true difference, zero.
- **Valid rate:** the fraction of replicates with a finite statistic and
  p-value and, where required, positive finite effective degrees of freedom.

The primary comparison uses $\alpha=0.05$. The tabulated checks at 0.10 and
0.01 use the same replicates. Rejection-calibration curves evaluate nominal
levels from 0 to 0.10 in increments of 0.001; their bands show the 10th and
90th percentiles of the 12 scenario-specific rejection rates.

### 7.6 Power and runtime designs

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
$(2,2,200,200)$, $(3,3,200,200)$, $(5,5,375,375)$, and
$(8,8,960,960)$. Each method is warmed up and then timed 200 times on
each fixed table pair; the reported value is the median. This gives 2,400
timed complete method calls.

## 8. Results

### 8.1 Calibration across regimes

![Rejection calibration across nominal significance levels](../results/supervisor_practical/rejection_calibration.png)

The diagonal represents perfect calibration. Each method's line is the mean
rejection rate across the 12 population pairs in that regime, and the shaded
band spans the 10th to 90th percentiles across those populations. A curve
above the diagonal is liberal; a curve below it is conservative. The vertical
dashed line marks the primary level $\alpha=0.05$.

The curves show the complete lower-tail result rather than only three selected
significance levels. Expanded Welch changes little in the well-sampled
control and moves the moderate and sparse curves toward the diagonal.

The regime table reports two complementary quantities at $\alpha=0.05$.
Mean FPR describes the overall direction of calibration, while mean absolute
error measures scenario-by-scenario accuracy without allowing liberal and
conservative errors to cancel. In the final column, a positive percentage
means Expanded Welch reduced mean absolute error relative to Normal Wald.

| Regime | Normal FPR | Simple FPR | Expanded FPR | Normal mean error | Expanded mean error | Error change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Well sampled | 0.05174 | 0.05112 | 0.04913 | 0.00317 | 0.00332 | $-4.5\%$ |
| Moderate | 0.06158 | 0.06025 | 0.05623 | 0.01158 | 0.00720 | $+37.8\%$ |
| Highly skewed and sparse | 0.05547 | 0.05445 | 0.05198 | 0.00645 | 0.00456 | $+29.3\%$ |
| Ultra-skewed and sparse | 0.07504 | 0.07208 | 0.06305 | 0.02504 | 0.01340 | $+46.5\%$ |
| Widespread sparsity | 0.07431 | 0.07096 | 0.05689 | 0.02431 | 0.01278 | $+47.4\%$ |

Normal Wald is already well calibrated in the well-sampled control. Expanded
Welch changes its mean FPR from 0.05174 to 0.04913, but its scenario-level
mean absolute error is 4.5% larger because the correction is not needed in
every control table.

Expanded Welch reduces mean absolute error by 37.8% in the moderate regime,
29.3% when minimum expected counts are between 1 and 5, and 46.5% when the
minimum expected count is below 1. At $\alpha=0.01$, the corresponding
reductions are 54.2%, 51.6%, and 66.3%.

Under widespread sparsity, Expanded Welch reduces error among valid results,
but its valid rate falls to 0.97450. This remains a boundary regime rather
than evidence of universally reliable operation. Simple Welch improves only
part of the calibration error and remains closer to Normal Wald than to
Expanded Welch.

### 8.2 Calibration by regime variant

Each entry below is the mean FPR across the six table shapes for one fully
specified variant in Section 7.3. The target remains 0.05.

| Regime and variant | $I(P)=I(Q)$ | $n_Q:n_P$ | Normal Wald | Simple Welch | Expanded Welch |
| --- | ---: | ---: | ---: | ---: | ---: |
| Well sampled 1 | 0.10 | $1{:}1$ | 0.04942 | 0.04882 | 0.04612 |
| Well sampled 2 | 0.15 | $1{:}1$ | 0.05407 | 0.05342 | 0.05215 |
| Moderate 1 | 0.10 | $1{:}1$ | 0.05772 | 0.05647 | 0.05222 |
| Moderate 2 | 0.15 | $2{:}1$ | 0.06545 | 0.06403 | 0.06025 |
| Highly skewed and sparse 1 | 0.10 | $1{:}1$ | 0.05185 | 0.05077 | 0.04797 |
| Highly skewed and sparse 2 | 0.15 | $2{:}1$ | 0.05908 | 0.05813 | 0.05598 |
| Ultra-skewed and sparse 1 | 0.10 | $1{:}1$ | 0.05775 | 0.05638 | 0.05267 |
| Ultra-skewed and sparse 2 | 0.15 | $10{:}1$ | 0.09233 | 0.08778 | 0.07343 |
| Widespread sparsity 1 | 0.10 | $1{:}1$ | 0.07148 | 0.06672 | 0.05058 |
| Widespread sparsity 2 | 0.15 | $2{:}1$ | 0.07714 | 0.07520 | 0.06320 |

Expanded Welch improves both variants of the moderate, highly sparse,
ultra-sparse, and widespread regimes. Its largest remaining error is the
$10{:}1$ ultra-sparse variant, where it reduces FPR from 0.09233 to 0.07343
but does not restore nominal calibration.

Complete scenario-level results, including Wilson intervals and validity
diagnostics, are available in
[`scenario_results.csv`](../results/supervisor_practical/scenario_results.csv).

### 8.3 Power

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

### 8.4 Computational cost

| Shape | $(n_P,n_Q)$ | Normal Wald | Simple Welch | Expanded Welch |
| ---: | ---: | ---: | ---: | ---: |
| $2\times2$ | $(200,200)$ | 0.0880 ms | 0.1033 ms | 0.1688 ms |
| $3\times3$ | $(200,200)$ | 0.0875 ms | 0.1029 ms | 0.1666 ms |
| $5\times5$ | $(375,375)$ | 0.0875 ms | 0.1027 ms | 0.1666 ms |
| $8\times8$ | $(960,960)$ | 0.0883 ms | 0.1038 ms | 0.1685 ms |

Expanded Welch takes 1.89-1.91 times as long as Normal Wald in this benchmark
but remains below 0.2 ms per table pair. All three methods are deterministic
and require $O(rc)$ time; none requires resampling.

## 9. Conclusion for Supervisor Discussion

The experiment supports a narrow but coherent story:

1. **Normal Wald remains the appropriate baseline.** It already performs
   well in ordinary, adequately sampled tables.
2. **Simple Welch changes very little.** Ordinary $n-1$ degrees of freedom do
   not capture much additional uncertainty for the MI variance estimator.
3. **Expanded Welch helps in its intended regime.** It improves calibration
   when isolated rare cells or unequal sample sizes make the estimated MI
   variance unstable, while sacrificing little power.
4. **Expanded Welch has clear limits.** The most difficult $10{:}1$
   ultra-sparse variant remains liberal, and its valid rate falls to 0.97450
   under widespread sparsity. It improves rather than solves these cases.
5. **The computational cost is negligible.** The method is deterministic,
   $O(rc)$, and below 0.2 ms per tested table pair.

A defensible thesis claim is therefore:

> For testing equality of two positive mutual informations, an MI-specific
> Welch-Satterthwaite correction can improve finite-sample calibration in
> sparse, skewed, or unequal-sample settings when sampled support remains
> sufficiently stable. It retains near-Wald power and deterministic
> sub-millisecond runtime. It is a targeted correction rather than a complete
> solution for every sparse-table configuration.

The main question for supervisor discussion is whether this targeted regime
is sufficiently important for the thesis contribution, and whether the next
experiment should be a pre-specified confirmatory grid restricted to the
regular positive-MI setting. The complete results remain available in
[`REPORT.md`](../results/supervisor_practical/REPORT.md) and the accompanying CSV
files.

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
