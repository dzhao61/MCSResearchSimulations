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

### Statistical objective

All three analytic methods use the same statistic:

$$
T=\frac{\widehat\Delta_{\mathrm{BC}}}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

Method 3 changes only the reference distribution used for $T$. Its objective
is to calculate MI-specific effective degrees of freedom for the estimated
variance components $\widehat V(P)$ and $\widehat V(Q)$ in the denominator.

For population $P$, Satterthwaite moment matching requires two properties of
$\widehat V(P)$:

$$
\operatorname E(\widehat V(P))
\quad\text{and}\quad
\operatorname{Var}(\widehat V(P)).
$$

To first order, $\operatorname E(\widehat V(P))\approx V(P)$. The central
problem is therefore to calculate the sampling variance
$\operatorname{Var}(\widehat V(P))$. Once that variance is known,
Satterthwaite converts it into component degrees of freedom through

$$
\nu_V(P)
\approx
\frac{2V(P)^2}{\operatorname{Var}(\widehat V(P))}.
$$

The derivation that follows exists to calculate the denominator of this
expression for an MI variance estimator.

### Source and adaptation

The method is inspired by **Hutcheson's (1970) test for comparing two Shannon
diversities**. Hutcheson used the same broad architecture as Welch's test:
subtract two estimated information quantities, divide by their combined
estimated standard error, and use effective degrees of freedom for uncertain
variance terms.

Expanded Welch adapts that architecture from Shannon entropy to mutual
information. Simple Welch assigns ordinary $n-1$ component degrees of
freedom. Expanded Welch derives the sampling uncertainty of the complete
nonlinear MI variance estimator and uses that uncertainty in the
Satterthwaite calculation.

Reference: K. Hutcheson, *A Test for Comparing Diversities Based on the
Shannon Formula*, Journal of Theoretical Biology 29 (1970), 151-154,
<https://doi.org/10.1016/0022-5193(70)90124-4>.

### Derivation roadmap

The calculation proceeds through six linked questions:

| Step | Question | Quantity produced |
| ---: | --- | --- |
| 1 | What population variance governs the sampling error of MI? | $V(P)$ |
| 2 | How does that variance change when the underlying table changes slightly? | $g_P(x,y)$ |
| 3 | How variable are those cell-level changes across the population? | $\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}$ |
| 4 | What does that imply for the sampling variance of $\widehat V(P)$? | $\operatorname{Var}(\widehat V(P))\approx\tau^2(P)/n_P$ |
| 5 | What scaled-chi-squared variable has the same first two moments? | $\nu_V(P)=2n_PV(P)^2/\tau^2(P)$ |
| 6 | How are the $P$ and $Q$ components combined? | $\widehat\nu_{\mathrm{expanded}}$ |

The dependency chain is

$$
V(P)
\xrightarrow{\text{differentiate}}
g_P
\xrightarrow{\text{take its variance}}
\tau^2(P)
\xrightarrow{\text{divide by }n_P}
\operatorname{Var}(\widehat V(P))
\xrightarrow{\text{moment match}}
\nu_V(P).
$$

The same chain is calculated for $Q$, after which the two component degrees
of freedom are combined. Here, an **influence function** is the first-order
change in a statistical functional after a small perturbation of the
underlying distribution.

### 6.1 Identify the variance estimator in the denominator

Let $Z=(X,Y)\sim P$. For a cell $(i,j)$, define its pointwise mutual
information (PMI)

$$
\ell_P(i,j)
=\log\!\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

The MI and its second PMI moment are

$$
I(P)=\operatorname E_P\{\ell_P(Z)\},
\qquad
M_2(P)=\operatorname E_P\{\ell_P(Z)^2\}.
$$

The symbol \(M_2(P)\) is introduced because a variance can be written as a
second moment minus a squared mean. This form makes it possible to
differentiate \(V(P)\) by differentiating two explicit sums.

Consequently, the first-order variance governing the MI estimator is the
variance of the PMI values:

$$
V(P)
=\operatorname{Var}_P\{\ell_P(Z)\}
=M_2(P)-I(P)^2.
$$

This quantity appears in the ordinary first-order sampling variance

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}.
$$

The denominator of $T$ uses the plug-in estimate
$\widehat V(P)=V(\widehat P)$. The first roadmap step has therefore identified
the estimator whose sampling uncertainty must be calculated.

### 6.2 Measure how $V(P)$ responds to a cell perturbation

One observation changes the empirical table by adding probability to its
observed cell while all probabilities continue to sum to one. The
population-level analogue is to increase the probability of cell $(x,y)$ by
an infinitesimal amount while renormalizing the rest of the table:

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
margin, its column margin, every affected PMI value, and MI
itself.

Once $g_P$ is known, first-order influence-function theory represents the
sampling error of $\widehat V(P)$ as an average of these cell sensitivities:

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)}).
$$

Consequently,

$$
\operatorname{Var}(\widehat V(P))
\approx
\frac{\operatorname{Var}_P\{g_P(X,Y)\}}{n_P}.
$$

This relation explains why the next two sections derive $g_P(x,y)$.

### 6.3 Calculate the derivatives required for $g_P$

The quantity we want is

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Since

$$
V(P_\varepsilon)
=M_2(P_\varepsilon)-I(P_\varepsilon)^2,
$$

the chain rule shows exactly what must be calculated:

$$
g_P(x,y)
=\left.\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-2I(P)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

We therefore need the derivative of the MI mean $I(P)$ and the derivative
of the second moment $M_2(P)$. Both contain the PMI value, so
we first record how that PMI value changes.

Along the contamination path,

$$
\left.p_{ij}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{(i,j)=(x,y)\}-p_{ij},
$$

with corresponding derivatives

$$
\left.p_{i+}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{i=x\}-p_{i+},
\qquad
\left.p_{+j}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

For an arbitrary cell $(i,j)$,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Using $(\log u)'=u'/u$ gives

$$
\ell_P'(i,j;x,y)
=
\frac{\mathbf 1\{(i,j)=(x,y)\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
$$

The derivatives of $I(P)$ and $M_2(P)$ follow by substituting this PMI
derivative into their defining probability-weighted sums.

#### Derivative of the MI mean

Start from the quantity being differentiated:

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)\ell_{P_\varepsilon}(i,j).
$$

The product rule gives

$$
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}p_{ij}'(0)\ell_P(i,j)
+\sum_{i,j}p_{ij}\ell_P'(i,j;x,y).
$$

The first sum is

$$
\begin{aligned}
\sum_{i,j}
\big[\mathbf 1\{(i,j)=(x,y)\}-p_{ij}\big]\ell_P(i,j)
&=\ell_P(x,y)-\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\ell_P(x,y)-I(P).
\end{aligned}
$$

For the second sum, substitute the formula for $\ell_P'$:

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P'(i,j;x,y)
&=\frac{p_{xy}}{p_{xy}}
-\frac{\sum_j p_{xj}}{p_{x+}}
-\frac{\sum_i p_{iy}}{p_{+y}}
+\sum_{i,j}p_{ij}\\
&=1-1-1+1\\
&=0.
\end{aligned}
$$

The four values come respectively from the selected cell, row $x$, column
$y$, and the normalization term. Hence,

$$
\boxed{
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P).
}
$$

#### Derivative of the second moment

The second moment under the contaminated distribution is

$$
M_2(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)\ell_{P_\varepsilon}(i,j)^2.
$$

Applying the product rule and $(\ell^2)'=2\ell\ell'$ gives

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\sum_{i,j}p_{ij}'(0)\ell_P(i,j)^2\\
&+2\sum_{i,j}p_{ij}\ell_P(i,j)\ell_P'(i,j;x,y).
\end{aligned}
$$

The first sum changes the probability weights and simplifies to

$$
\begin{aligned}
\sum_{i,j}
\big[\mathbf 1\{(i,j)=(x,y)\}-p_{ij}\big]\ell_P(i,j)^2
&=\ell_P(x,y)^2-\sum_{i,j}p_{ij}\ell_P(i,j)^2\\
&=\ell_P(x,y)^2-M_2(P).
\end{aligned}
$$

The second sum changes the PMI values. Substituting
$\ell_P'(i,j;x,y)$ directly gives

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P(i,j)\ell_P'(i,j;x,y)
={}&\ell_P(x,y)\\
&-\frac{1}{p_{x+}}\sum_j p_{xj}\ell_P(x,j)\\
&-\frac{1}{p_{+y}}\sum_i p_{iy}\ell_P(i,y)\\
&+\sum_{i,j}p_{ij}\ell_P(i,j).
\end{aligned}
$$

The second and third terms in the preceding expansion are the
probability-weighted mean PMI values within row $x$ and column
$y$. Define them by

$$
\begin{aligned}
R_P(x)
&=\frac{1}{p_{x+}}\sum_j p_{xj}\ell_P(x,j)
=\operatorname E_P\{\ell_P(X,Y)\mid X=x\},\\[4pt]
C_P(y)
&=\frac{1}{p_{+y}}\sum_i p_{iy}\ell_P(i,y)
=\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}.
\end{aligned}
$$

The second-moment derivative is therefore

$$
\boxed{
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\ell_P(x,y)^2-M_2(P)\\
&+2\big[\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\big].
\end{aligned}}
$$

### 6.4 Assemble the variance influence function $g_P$

Differentiating $V(P)=M_2(P)-I(P)^2$ gives

$$
\begin{aligned}
g_P(x,y)
&=\left.\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}\\
&=\left.\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-2I(P)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Substituting the derivatives of $M_2(P)$ and $I(P)$ gives

$$
\boxed{
\begin{aligned}
g_P(x,y)={}&
\ell_P(x,y)^2-M_2(P)\\
&+2\big[\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\big]\\
&-2I(P)\big[\ell_P(x,y)-I(P)\big].
\end{aligned}}
$$

Each line comes from a particular part of the original variance:

- $\ell_P(x,y)^2-M_2(P)$ comes from changing the probability weights in
  the second moment;
- $2[\ell_P(x,y)-R_P(x)-C_P(y)+I(P)]$ comes from changing the PMI values
  inside the second moment;
- $-2I(P)[\ell_P(x,y)-I(P)]$ comes from differentiating the centring term
  $-I(P)^2$.

### 6.5 Convert variance-estimation uncertainty into degrees of freedom

The function $g_P(x,y)$ measures how much one cell can change $V(P)$. Its
variance measures how differently the cells affect $V(P)$:

$$
\tau^2(P)
=\operatorname{Var}_P\{g_P(X,Y)\}.
$$

A small $\tau^2(P)$ means that the cells have similar effects and
$\widehat V(P)$ is comparatively stable. A large $\tau^2(P)$ means that the
estimated variance is sensitive to which cells appear in the sample.

#### Sampling variance of $\widehat V(P)$

To first order, the error in $\widehat V(P)$ is the average variance influence
of the $n_P$ observations:

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)}).
$$

The observations are independent and each $g_P(Z_k^{(P)})$ has variance
$\tau^2(P)$. Therefore,

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&=\operatorname{Var}\{\widehat V(P)-V(P)\}\\
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\operatorname{Var}\left\{
\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
\right\}\\
&=\frac{1}{n_P^2}\left[
\sum_{k=1}^{n_P}\operatorname{Var}_P\{g_P(Z_k^{(P)})\}
+2\sum_{1\le k<l\le n_P}\operatorname{Cov}_P
\{g_P(Z_k^{(P)}),g_P(Z_l^{(P)})\}
\right]\\
&=\frac{1}{n_P^2}
\sum_{k=1}^{n_P}\operatorname{Var}_P\{g_P(Z_k^{(P)})\}\\
&=\frac{1}{n_P^2}\,n_P\tau^2(P)\\
&=\frac{\tau^2(P)}{n_P}.
\end{aligned}
$$

#### Satterthwaite moment matching

We now know the approximate first two moments of the variance estimator:

$$
\operatorname E\{\widehat V(P)\}\approx V(P),
\qquad
\operatorname{Var}\{\widehat V(P)\}
\approx\frac{\tau^2(P)}{n_P}.
$$

The complete finite-sample distribution of $\widehat V(P)$ is not known.
Satterthwaite replaces it with a convenient positive distribution and chooses
its degrees of freedom so that its mean and variance match the two moments
above.

A chi-squared variable with $\nu_V(P)$ degrees of freedom satisfies

$$
\operatorname E\{\chi^2_{\nu_V(P)}\}=\nu_V(P),
\qquad
\operatorname{Var}\{\chi^2_{\nu_V(P)}\}=2\nu_V(P).
$$

Dividing by $\nu_V(P)$ normalizes its mean to one:

$$
\begin{aligned}
\operatorname E\left\{
\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right\}
&=\frac{\nu_V(P)}{\nu_V(P)}=1,\\[4pt]
\operatorname{Var}\left\{
\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right\}
&=\frac{2\nu_V(P)}{\nu_V(P)^2}
=\frac{2}{\nu_V(P)}.
\end{aligned}
$$

Multiplying this normalized variable by $V(P)$ gives it the required mean:

$$
\begin{aligned}
\operatorname E\left\{
V(P)\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right\}
&=V(P),\\[4pt]
\operatorname{Var}\left\{
V(P)\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}
\right\}
&=V(P)^2\frac{2}{\nu_V(P)}
=\frac{2V(P)^2}{\nu_V(P)}.
\end{aligned}
$$

Satterthwaite therefore uses the working approximation

$$
\widehat V(P)
\ \dot\sim\
V(P)\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)},
$$

Its mean already matches $V(P)$. Matching its variance to the derived sampling
variance of $\widehat V(P)$ gives

$$
\begin{aligned}
\frac{2V(P)^2}{\nu_V(P)}
&=\frac{\tau^2(P)}{n_P},\\
2n_PV(P)^2
&=\nu_V(P)\tau^2(P),\\
\nu_V(P)
&=\frac{2n_PV(P)^2}{\tau^2(P)}.
\end{aligned}
$$

Equivalently,

$$
\nu_V(P)
=\frac{2}{\tau^2(P)/\left\{n_PV(P)^2\right\}},
$$

so $\nu_V(P)$ is inversely related to the relative sampling variance of
$\widehat V(P)$. Stable variance estimation produces large $\nu_V(P)$;
unstable variance estimation produces small $\nu_V(P)$ and a heavier-tailed
Student reference. This is only a moment-matching approximation, not a claim
that $\widehat V(P)$ is exactly chi-squared.

#### Calculation from the observed table

The population quantities are unknown, so the observed table supplies their
plug-in estimates. First calculate the weighted mean of the estimated cell
sensitivities:

$$
\overline g_P
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}\widehat g_P(i,j).
$$

Then calculate their weighted variance:

$$
\widehat\tau^2(P)
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left[\widehat g_P(i,j)-\overline g_P\right]^2.
$$

The resulting component degrees of freedom are

$$
\widehat\nu_V(P)
=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
$$

The same calculation gives $\widehat\nu_V(Q)$.

### 6.6 Combine the two populations and calibrate $T$

Scaling a variance component does not change its component degrees of
freedom. The usual Satterthwaite combination therefore gives

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_V(P)
+\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_V(Q)
}}.
$$

The final p-value is

$$
p_{\mathrm{expanded}}
=2\Pr\{t_{\widehat\nu_{\mathrm{expanded}}}\ge |T|\}.
$$

Nothing before this final calibration changes: expanded Welch uses the same
bias-corrected MI difference, standard error, and statistic $T$ as normal
Wald and simple Welch. The derivation changes only the reference degrees of
freedom.

### Interpretation

If an MI variance estimate is stable, $\widehat\tau^2(P)$ is small and the
method assigns many degrees of freedom. If it is highly sample-dependent,
$\widehat\tau^2(P)$ is large, the degrees of freedom fall, and the Student
reference becomes more conservative.

The expanded calculation targets the main weakness of simple Welch. It is
still an approximation. Unlike an ordinary normal-sample variance,
$\widehat V(P)$ is not exactly scaled chi-squared, and $T$'s numerator and
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
| Main role | Analytic baseline | Simple finite-df correction | MI-specific correction |

## 8. Experimental Design

The redesigned validation uses one grid rather than several overlapping
experiments:

$$
12\ \text{table shapes}
\times16\ \text{population designs}
=192\ \text{equal-MI population pairs}.
$$

The sixteen designs comprise eight interpretable regimes, with two
population variants in each regime.

The shapes are

$$
2\times2,\ 2\times5,\ 3\times3,\ 3\times7,\ 4\times6,\ 5\times5,
\ 5\times10,\ 8\times8,\ 8\times12,\ 10\times10,\ 10\times15,
\ 20\times20.
$$

For every pair, $P$ and $Q$ are different joint distributions constructed to
satisfy $I(P)=I(Q)$ numerically. The largest absolute true MI difference over
the generated grid was $1.1\times10^{-13}$ nats.

### 8.1 Eight regimes

| Regime | Target MI | Sample-size ratio | Sparsity control | Purpose |
| --- | ---: | ---: | ---: | --- |
| Well sampled | 0.03 | $1{:}1$ | Average of 100 or 200 observations per cell | Check ordinary tables, including a skewed but densely sampled variant |
| Moderate | 0.07 | $1{:}2$ | Average of 20 or 50 observations per cell | Check moderate imbalance and heterogeneous margins |
| Sparse and imbalanced | 0.15 | $1{:}4$ | Average of 10 or 25 observations per cell | Target low average counts and strongly unequal sample sizes |
| Highly skewed and sparse | 0.10 or 0.15 | $1{:}1$ or $1{:}4$ | $1\leq E_{\min}<5$ in both populations | Test cells that are observed only a few times on average |
| Ultra-skewed and sparse | 0.10 or 0.15 | $1{:}1$ or $1{:}4$ | $0<E_{\min}<1$ in both populations | Test rare cells that are more likely to be empty than observed |
| Widespread sparsity | 0.03 | $1{:}1$ | 25-50% of cells have expected counts below 1 and at least 50% are below 5 in both populations | Test broad support sparsity rather than one isolated rare cell |
| Equal-MI shape mismatch | 0.07 or 0.15 | $1{:}1$ | Near-uniform margins in $P$ and strongly skewed margins in $Q$ | Compare differently shaped populations with exactly equal MI |
| Extreme sample imbalance | 0.07 or 0.15 | $1{:}10$ or $1{:}20$ | Average of 25 or 10 observations per cell in the smaller sample | Stress the unequal-variance combination directly |

For a population with joint probabilities $p_{ij}$ and sample size $n$, the
minimum true expected cell count is

$$
E_{\min}=\min_{i,j}\{n p_{ij}\}.
$$

For a pair of populations, the stated interval must hold separately for both
$P$ and $Q$. This is stricter than classifying a table from the average
$n/(rc)$: a table may have a large sample overall while still containing a
very rare cell. The ultra-sparse generator targets expected minima between
0.20 and 1 internally, rather than values arbitrarily close to zero, while
still satisfying the reported $0<E_{\min}<1$ definition.

A minimum sample size of 120 is applied to all designs. Within each regime,
the two variants use different random margins and association patterns.
Near-independence remains outside the main scope.

### 8.2 Replication and fairness

Each population pair receives 10,000 independently sampled pairs of
multinomial tables:

$$
192\times10{,}000=1{,}920{,}000\ \text{null replicates}.
$$

Normal Wald, simple Welch, and expanded Welch are calculated on exactly the
same table pairs. All three use the same bias-corrected difference,
$\widehat{\Delta}_{\mathrm{BC}}$, and standard error. Only the reference
calibration differs. Each method's false-positive rate is calculated among
the replicates for which that method returns a valid result; validity is
reported separately so boundary failures are not hidden by conditioning on a
common subset.

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
This calibration error must be interpreted together with the valid rate.

### 9.2 Null calibration

| Regime | Method | Error at $0.10$ | Error at $0.05$ | Error at $0.01$ | Valid rate | 95% coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Well sampled | Normal Wald | **0.00440** | **0.00377** | **0.00154** | 1.00000 | 0.95340 |
| Well sampled | Simple Welch | 0.00444 | 0.00384 | 0.00157 | 1.00000 | 0.95347 |
| Well sampled | Expanded Welch | 0.00612 | 0.00516 | 0.00217 | 1.00000 | 0.95495 |
| Moderate | Normal Wald | 0.00538 | **0.00363** | 0.00167 | 1.00000 | 0.95135 |
| Moderate | Simple Welch | **0.00530** | 0.00366 | 0.00163 | 1.00000 | 0.95160 |
| Moderate | Expanded Welch | 0.00592 | 0.00411 | **0.00152** | 1.00000 | 0.95355 |
| Sparse and imbalanced | Normal Wald | 0.00777 | 0.00631 | 0.00299 | 1.00000 | 0.94402 |
| Sparse and imbalanced | Simple Welch | 0.00721 | 0.00581 | 0.00271 | 1.00000 | 0.94455 |
| Sparse and imbalanced | Expanded Welch | **0.00537** | **0.00410** | **0.00155** | 1.00000 | 0.94650 |
| Highly skewed and sparse | Normal Wald | 0.00330 | 0.00298 | 0.00153 | 1.00000 | 0.94937 |
| Highly skewed and sparse | Simple Welch | 0.00318 | 0.00288 | 0.00146 | 1.00000 | 0.94950 |
| Highly skewed and sparse | Expanded Welch | **0.00274** | **0.00245** | **0.00114** | 1.00000 | 0.94998 |
| Ultra-skewed and sparse | Normal Wald | 0.00375 | 0.00270 | 0.00125 | 1.00000 | 0.94757 |
| Ultra-skewed and sparse | Simple Welch | 0.00364 | 0.00257 | 0.00116 | 1.00000 | 0.94776 |
| Ultra-skewed and sparse | Expanded Welch | **0.00331** | **0.00220** | **0.00086** | 1.00000 | 0.94841 |
| Widespread sparsity | Normal Wald | 0.01586 | **0.01036** | **0.00392** | 0.99980 | 0.95268 |
| Widespread sparsity | Simple Welch | **0.01566** | 0.01041 | 0.00415 | 0.99980 | 0.95335 |
| Widespread sparsity | Expanded Welch | 0.02455 | 0.01730 | 0.00559 | 0.99154 | 0.96327 |
| Equal-MI shape mismatch | Normal Wald | **0.00727** | **0.00459** | 0.00168 | 1.00000 | 0.94743 |
| Equal-MI shape mismatch | Simple Welch | 0.00732 | 0.00463 | **0.00163** | 1.00000 | 0.94763 |
| Equal-MI shape mismatch | Expanded Welch | 0.00802 | 0.00535 | 0.00193 | 1.00000 | 0.94905 |
| Extreme sample imbalance | Normal Wald | 0.01084 | 0.00850 | 0.00450 | 1.00000 | 0.94372 |
| Extreme sample imbalance | Simple Welch | 0.01028 | 0.00785 | 0.00399 | 1.00000 | 0.94444 |
| Extreme sample imbalance | Expanded Welch | **0.00805** | **0.00546** | **0.00184** | 1.00000 | 0.94878 |

Expanded Welch continued to improve the three original sparse regimes and
was especially useful under extreme sample imbalance. At $\alpha=0.05$, it
reduced error relative to normal Wald by 35.0% in sparse-and-imbalanced
tables, 17.9% in the highly sparse set, 18.4% in the ultra-sparse set, and
35.8% under $1{:}10$ or $1{:}20$ imbalance. At $\alpha=0.01$, the respective
reductions were 48.2%, 25.1%, 31.2%, and 59.1%.

The additional regimes also identify the boundary. Under widespread
sparsity, expanded Welch became too conservative at $\alpha=0.05$ and its
mean valid rate fell to 0.99154. Shape mismatch alone produced similar
accuracy for all three methods and no advantage for expanded Welch.

The correction was also not beneficial in well-sampled tables,
expanded Welch rejected too rarely and increased mean error at
$\alpha=0.05$ from 0.00377 to 0.00516. Simple Welch remained very close to
normal Wald across all regimes because its effective degrees of freedom were
usually large.

All calculations were valid in seven regimes. Under widespread sparsity,
mean valid rates were 0.99980 for normal and simple Welch and 0.99154 for
expanded Welch.

Across all 192 scenarios, mean absolute FPR error at $\alpha=0.05$ was
0.00535 for normal Wald, 0.00521 for simple Welch, and 0.00577 for expanded
Welch. At $\alpha=0.01$, expanded Welch had the lowest aggregate error at
0.00207, compared with 0.00229 for simple Welch and 0.00239 for normal Wald.
Expanded Welch's mean valid rate was 0.99894, compared with 0.99998 for the
other two methods. These aggregate results reinforce the need to state its
regime-specific benefits and limitations together.

### 9.3 Where each method works well

| Method | Most suitable regimes | Statistical reason | Main limitation |
| --- | --- | --- | --- |
| Normal Wald | Well sampled and moderate tables; equal-MI shape mismatch | With stable plug-in MI and variance estimates, the studentized difference is already close to its asymptotic standard normal reference. | It does not account for the additional finite-sample uncertainty in the estimated MI variance and can therefore reject too often under sparsity or severe sample imbalance. |
| Simple Welch-Satterthwaite | Approximately the same regimes as normal Wald, with modest protection in some unequal-sample cases | The ordinary $n_P-1$ and $n_Q-1$ component degrees of freedom introduce a small, familiar Student-tail correction. | Those degrees of freedom describe conventional sample variances, not the nonlinear MI variance estimator, so the correction is usually too weak to resolve the difficult cases. |
| Expanded Welch-Satterthwaite | Sparse and imbalanced tables, isolated highly or ultra-skewed cells, and extreme sample imbalance | Its component degrees of freedom estimate how uncertain the complete MI variance estimate is. This produces heavier tails precisely when variance-estimation noise makes normal Wald liberal. | It can overcorrect when the normal approximation is already adequate, and its first-order influence calculation does not repair widespread loss of sampled cells. |

In well-sampled and moderate tables, the estimated standard error changes
little between repeated samples. Normal Wald therefore provides the cleanest
reference. Simple Welch remains almost indistinguishable from it because its
effective degrees of freedom are generally large. Expanded Welch adds a
tail correction that is not needed and consequently becomes mildly
conservative.

The sparse-and-imbalanced, highly sparse, ultra-sparse, and extreme-imbalance
regimes have a different failure mechanism. Their sampled support remains
mostly informative, but the uncertainty of the MI variance estimate is no
longer negligible. Expanded Welch models this second layer of uncertainty
and reduced error consistently across all three tested significance levels.

Equal-MI shape mismatch changes the geometry of the two populations without
necessarily making either variance estimate especially unreliable. A
degrees-of-freedom correction does not directly address that mismatch, so
normal Wald and simple Welch remained at least as accurate as expanded
Welch.

Widespread sparsity is not a positive result for any method. Normal Wald and
simple Welch were the least inaccurate, but their mean absolute errors were
still among the largest in the experiment. When many cells have expected
counts below one, different cells appear in different samples and the
plug-in MI, its bias correction, and its variance estimate move together.
The expanded calculation interprets the unstable variance estimate as a
need for very heavy Student tails, overcorrects, and rejects too rarely.

This regime map describes the assumptions under which each approximation is
credible; it is not a post-hoc method-selection rule. A practical analysis
should choose and report its calibration procedure before examining the
result, using the sampling design and expected support structure as
justification.

### 9.4 Power

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
its heavier tails. Unequal-sample power remains a necessary confirmatory
check.

### 9.5 Runtime

The three methods were timed through the same implementation path.

| Shape | Normal Wald | Simple Welch | Expanded Welch |
| --- | ---: | ---: | ---: |
| $2\times2$ | 0.091 ms | 0.107 ms | 0.173 ms |
| $5\times5$ | 0.087 ms | 0.102 ms | 0.167 ms |
| $10\times10$ | 0.086 ms | 0.101 ms | 0.163 ms |
| $20\times20$ | 0.096 ms | 0.111 ms | 0.183 ms |

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
calibration when isolated rare cells or unequal sample sizes make variance
estimation unstable but the sampled support remains mostly intact. Its
heavier tails make it conservative in well-sampled tables and fail to repair
widespread support loss.

The defensible conclusion is deliberately specific:

> Expanded Welch supplies an MI-specific finite-sample correction that
> improves calibration in sparse, skewed, or unequal-sample regimes when
> sampled support remains sufficiently stable. It is not a universal
> replacement for normal Wald.

The complete reproducible output is in
[`results/supervisor_full/REPORT.md`](../results/supervisor_full/REPORT.md).

## Appendix A: Intuition Behind Expanded Welch-Satterthwaite

The test statistic is

$$
T
=\frac{\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

The denominator estimates how much the MI difference should fluctuate under
repeated sampling. The difficulty is that $\widehat V(P)$ and $\widehat V(Q)$
are themselves estimated and can be unstable in finite samples.

Normal Wald treats this remaining denominator uncertainty as negligible.
Simple Welch allows for it, but assumes each MI variance behaves like an
ordinary sample variance with $n-1$ degrees of freedom. That assumption is
questionable because

$$
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\left\{\widehat\ell_P(i,j)-\widehat I(P)\right\}^2
$$

is a nonlinear function of the complete table. Changing one cell also
changes its row margin, column margin, PMI values, MI, and
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
\tau^2(P)
=\operatorname{Var}_P\{g_P(X,Y)\},
$$

determines the first-order uncertainty of the estimated variance:

$$
\operatorname{Var}(\widehat V(P))
\approx\frac{\tau^2(P)}{n_P}.
$$

Satterthwaite moment matching converts this uncertainty into component
degrees of freedom:

$$
\nu_V(P)
=\frac{2n_PV(P)^2}{\tau^2(P)}.
$$

The interpretation is direct:

- if $g_P$ varies little across cells, $\widehat V(P)$ is stable, the degrees
  of freedom are large, and the reference remains close to normal;
- if some cells have much greater influence, $\widehat V(P)$ is unstable, the
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

## Appendix B: Which Variance Does Each Method Calculate?

The easiest way to understand the calculation is to imagine repeating the
entire experiment many times. There are three levels of variation.

### B.1 Variation between individual observations

Each observation can push the estimated MI up or down. That contribution is
represented by the MI influence function:

$$
\psi_P(x,y)
=\log\!\left(\frac{p_{xy}}{p_{x+}p_{+y}}\right)-I(P).
$$

Its variance is

$$
V(P)=\operatorname{Var}_P\{\psi_P(X,Y)\}.
$$

This answers the question:

> How different are the MI contributions of individual observations?

The population quantity $V(P)$ is estimated by $\widehat V(P)$.

### B.2 Variation of the estimated MI

A dataset contains $n_P$ observations. Averaging many observations reduces
variability, so

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}.
$$

This is estimated as

$$
\widehat{\operatorname{Var}}\{\widehat I(P)\}
=\frac{\widehat V(P)}{n_P}.
$$

It answers the question:

> If we repeatedly collected complete datasets, how much would the estimated
> MI change?

The corresponding standard error is

$$
\operatorname{SE}\{\widehat I(P)\}
=\sqrt{\frac{\widehat V(P)}{n_P}}.
$$

For two independent populations, the variances add:

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

This is the estimated sampling variance of the MI difference. Normal Wald,
simple Welch, and expanded Welch all use this same quantity in the denominator
of

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

### B.3 Variation of the estimated variance

The values $\widehat V(P)$ and $\widehat V(Q)$ are not known population values.
They are calculated from finite tables. If the complete experiment were
repeated, each dataset would produce a different value of $\widehat V(P)$.
Therefore, the variance estimate has its own sampling variance:

$$
\operatorname{Var}(\widehat V(P)).
$$

This answers the question:

> How much would our estimated MI variance change between repeated datasets?

This is a variance of a variance estimate. It measures how reliable the
estimated standard error is.

#### Simple Welch-Satterthwaite

Simple Welch assumes approximately

$$
\operatorname{Var}(\widehat V(P))
\approx\frac{2V(P)^2}{n_P-1}.
$$

This is the conventional sample-variance assumption. Equivalently, simple
Welch assigns

$$
\nu_V(P)=n_P-1.
$$

#### Expanded Welch-Satterthwaite

Expanded Welch derives the uncertainty of the complete MI variance estimator:

$$
\operatorname{Var}(\widehat V(P))
\approx\frac{\tau^2(P)}{n_P},
$$

where $\tau^2(P)$ measures how sensitive the complete MI variance calculation
is to individual cells. This produces the MI-specific component degrees of
freedom

$$
\nu_V(P)
=\frac{2n_PV(P)^2}{\tau^2(P)}.
$$

### B.4 Numerical example

Suppose

$$
\widehat V(P)=0.8,
\qquad
n_P=100,
$$

and

$$
\widehat V(Q)=1.2,
\qquad
n_Q=150.
$$

The estimated variance of the MI difference is

$$
\begin{aligned}
\widehat{\operatorname{SE}}^2
&=\frac{0.8}{100}+\frac{1.2}{150}\\
&=0.008+0.008\\
&=0.016.
\end{aligned}
$$

Therefore,

$$
\widehat{\operatorname{SE}}
=\sqrt{0.016}
\approx0.126.
$$

Normal Wald, simple Welch, and expanded Welch all use this same standard
error. They differ only in how confident they are in the estimated values
$0.8$ and $1.2$:

- normal Wald treats them as sufficiently reliable;
- simple Welch uses the generic $n-1$ reliability rule;
- expanded Welch calculates their reliability from the MI table.

### B.5 Complete map

| Level | Quantity | Question |
| --- | --- | --- |
| Individual observation | $V(P)$ | How variable are individual MI contributions? |
| MI estimator | $V(P)/n_P$ | How variable is $\widehat I(P)$? |
| Variance estimator | $\operatorname{Var}(\widehat V(P))$ | How reliable is the estimated MI variance? |
| MI difference | $V(P)/n_P+V(Q)/n_Q$ | How variable is $\widehat I(P)-\widehat I(Q)$? |

The crucial distinction is

$$
\widehat V(P)
\ne
\operatorname{Var}(\widehat V(P)).
$$

The first quantity is an estimated variance used to construct the MI standard
error. The second quantity measures how uncertain that estimated variance is.
Expanded Welch specifically improves the calculation of the second quantity.

## Appendix C: Validation of the Scaled Chi-Squared Working Model

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
