# Testing Independence by Comparing a Joint Distribution with an Independent Reference

## Purpose

Suppose $P$ is the joint distribution of two discrete variables $X$ and $Y$.
The proposed construction forms a second distribution $Q$ in which $X$ and
$Y$ have the same marginal distributions as under $P$, but are independent.
The intended comparison is

$$
H_0:I(P)=I(Q)
\qquad\text{against}\qquad
H_1:I(P)>I(Q).
$$

This document derives the construction step by step. It establishes four main
facts:

1. The independent reference distribution $Q$ can be constructed.
2. Comparing $P$ with this $Q$ is exactly the ordinary MI test of independence.
3. The first-order Taylor expansion used by the differential-MI Welch test
   becomes degenerate under independence.
4. A second-order expansion produces the usual chi-squared limit. Constructing
   $Q$ by shuffling or repeated simulation instead produces a permutation or
   bootstrap test.

Natural logarithms are used throughout, so mutual information is measured in
nats.

## 1. Define the Distribution of Interest

Let $P$ be an $r\times c$ joint probability distribution with cell
probabilities

$$
p_{ij}=\Pr_P(X=i,Y=j),
$$

where

$$
p_{ij}\geq 0,
\qquad
\sum_{i=1}^r\sum_{j=1}^c p_{ij}=1.
$$

Its row and column marginal probabilities are

$$
p_{i+}=\sum_{j=1}^c p_{ij},
\qquad
p_{+j}=\sum_{i=1}^r p_{ij}.
$$

The pointwise mutual information in cell $(i,j)$ is

$$
\ell_P(i,j)
=
\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

Mutual information is its probability-weighted mean:

$$
\begin{aligned}
I(P)
&=\operatorname E_P\{\ell_P(X,Y)\}\\
&=\sum_{i=1}^r\sum_{j=1}^c
p_{ij}\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
\end{aligned}
$$

The aim is to determine whether the association represented by $I(P)$ is
statistically distinguishable from independence.

## 2. Construct the Independent Reference Distribution

Define $Q$ by multiplying the marginal probabilities of $P$:

$$
\boxed{q_{ij}=p_{i+}p_{+j}.}
$$

### 2.1 Verify that $Q$ is a probability distribution

Every cell probability is nonnegative because

$$
q_{ij}=p_{i+}p_{+j}\geq 0.
$$

The probabilities sum to one:

$$
\begin{aligned}
\sum_{i,j}q_{ij}
&=\sum_{i,j}p_{i+}p_{+j}\\
&=\left(\sum_i p_{i+}\right)
  \left(\sum_j p_{+j}\right)\\
&=1\times 1\\
&=1.
\end{aligned}
$$

### 2.2 Verify that $Q$ has the same marginals as $P$

The row margins of $Q$ are

$$
\begin{aligned}
q_{i+}
&=\sum_j q_{ij}\\
&=\sum_j p_{i+}p_{+j}\\
&=p_{i+}\sum_jp_{+j}\\
&=p_{i+}.
\end{aligned}
$$

Similarly,

$$
\begin{aligned}
q_{+j}
&=\sum_i q_{ij}\\
&=\sum_i p_{i+}p_{+j}\\
&=p_{+j}\sum_ip_{i+}\\
&=p_{+j}.
\end{aligned}
$$

Thus $P$ and $Q$ have identical row and column marginals.

### 2.3 Verify independence under $Q$

Under $Q$,

$$
q_{ij}=q_{i+}q_{+j}.
$$

Therefore, $X$ and $Y$ are independent under $Q$. Its pointwise mutual
information is

$$
\ell_Q(i,j)
=\log\left(\frac{q_{ij}}{q_{i+}q_{+j}}\right)
=\log(1)
=0,
$$

and hence

$$
\boxed{I(Q)=0.}
$$

The proposed equal-MI null is consequently

$$
I(P)=I(Q)
\quad\Longleftrightarrow\quad
I(P)=0.
$$

Because mutual information is zero exactly when $X$ and $Y$ are independent,
this is the ordinary null hypothesis of independence in $P$.

## 3. Show that the Comparison Is Exactly Mutual Information

The Kullback-Leibler divergence from $P$ to $Q$ is

$$
D_{\mathrm{KL}}(P\|Q)
=\sum_{i,j}p_{ij}\log\left(\frac{p_{ij}}{q_{ij}}\right).
$$

Substituting $q_{ij}=p_{i+}p_{+j}$ gives

$$
\begin{aligned}
D_{\mathrm{KL}}(P\|Q)
&=\sum_{i,j}p_{ij}
\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)\\
&=I(P).
\end{aligned}
$$

Therefore,

$$
\boxed{D_{\mathrm{KL}}(P\|P_XP_Y)=I(P).}
$$

The distance between the joint distribution and its independent reference is
not merely related to MI; it is the definition of MI.

## 4. Construct the Reference from an Observed Table

Suppose the observed contingency table contains counts $N_{ij}$ with total

$$
N=\sum_{i,j}N_{ij}.
$$

The empirical probabilities are

$$
\widehat p_{ij}=\frac{N_{ij}}{N},
\qquad
\widehat p_{i+}=\frac{N_{i+}}{N},
\qquad
\widehat p_{+j}=\frac{N_{+j}}{N}.
$$

The empirical independent reference is

$$
\boxed{
\widehat q_{ij}
=\widehat p_{i+}\widehat p_{+j}
=\frac{N_{i+}N_{+j}}{N^2}.
}
$$

The expected count under this fitted independence model is

$$
\begin{aligned}
E_{ij}
&=N\widehat q_{ij}\\
&=N\frac{N_{i+}N_{+j}}{N^2}\\
&=\frac{N_{i+}N_{+j}}{N}.
\end{aligned}
$$

The divergence from the empirical joint distribution to the empirical
reference is

$$
\begin{aligned}
D_{\mathrm{KL}}(\widehat P\|\widehat Q)
&=\sum_{i,j}\widehat p_{ij}
\log\left(\frac{\widehat p_{ij}}{\widehat q_{ij}}\right)\\
&=\sum_{i,j}\widehat p_{ij}
\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right)\\
&=\widehat I(P).
\end{aligned}
$$

Thus the empirical reference comparison gives exactly the plug-in MI
estimate.

## 5. Recover the Likelihood-Ratio Statistic

Multiply the empirical divergence by $2N$:

$$
\begin{aligned}
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)
&=2N\sum_{i,j}\frac{N_{ij}}{N}
\log\left(
\frac{N_{ij}/N}{N_{i+}N_{+j}/N^2}
\right)\\
&=2\sum_{i,j}N_{ij}
\log\left(
\frac{N_{ij}}{N_{i+}N_{+j}/N}
\right)\\
&=2\sum_{i,j}N_{ij}
\log\left(\frac{N_{ij}}{E_{ij}}\right).
\end{aligned}
$$

Define

$$
G=2\sum_{i,j}N_{ij}\log\left(\frac{N_{ij}}{E_{ij}}\right).
$$

Then

$$
\boxed{G=2N\widehat I(P).}
$$

This is the likelihood-ratio, or $G$-test, statistic for independence. A
deterministic construction of $\widehat Q$ from the observed marginals
therefore returns the classical independence statistic exactly.

## 6. Derive the First-Order Taylor Expansion of MI

The differential-MI Welch test uses a first-order approximation to the
sampling error of MI. To see what happens under independence, begin by writing
MI as

$$
I(P)
=\sum_{i,j}p_{ij}\log p_{ij}
-\sum_i p_{i+}\log p_{i+}
-\sum_j p_{+j}\log p_{+j}.
$$

### 6.1 Perturb the distribution

Let $H=(h_{ij})$ be a direction satisfying

$$
\sum_{i,j}h_{ij}=0,
$$

so that total probability remains one. Define

$$
P_\varepsilon=P+\varepsilon H,
\qquad
p_{ij}(\varepsilon)=p_{ij}+\varepsilon h_{ij}.
$$

The corresponding marginal changes are

$$
h_{i+}=\sum_jh_{ij},
\qquad
h_{+j}=\sum_ih_{ij},
$$

so

$$
p_{i+}(\varepsilon)=p_{i+}+\varepsilon h_{i+},
\qquad
p_{+j}(\varepsilon)=p_{+j}+\varepsilon h_{+j}.
$$

### 6.2 Differentiate the three terms

Because

$$
\frac{\mathrm d}{\mathrm dx}(x\log x)=\log x+1,
$$

the derivative of MI at $\varepsilon=0$ is

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}h_{ij}(\log p_{ij}+1)\\
&\quad-\sum_i h_{i+}(\log p_{i+}+1)\\
&\quad-\sum_j h_{+j}(\log p_{+j}+1).
\end{aligned}
$$

The constant terms disappear because

$$
\sum_{i,j}h_{ij}
=\sum_i h_{i+}
=\sum_j h_{+j}
=0.
$$

For the row term,

$$
\sum_i h_{i+}\log p_{i+}
=\sum_{i,j}h_{ij}\log p_{i+},
$$

and similarly,

$$
\sum_j h_{+j}\log p_{+j}
=\sum_{i,j}h_{ij}\log p_{+j}.
$$

Therefore,

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}h_{ij}
\left(\log p_{ij}-\log p_{i+}-\log p_{+j}\right)\\
&=\sum_{i,j}h_{ij}
\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)\\
&=\sum_{i,j}h_{ij}\ell_P(i,j).
\end{aligned}
$$

The first-order derivative is therefore a weighted sum of the PMI values.

## 7. Show Why the First-Order Term Vanishes under Independence

If $P$ is independent, then

$$
p_{ij}=p_{i+}p_{+j}.
$$

Consequently,

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)
=0
$$

for every cell. Substitution into the derivative gives

$$
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}h_{ij}\times 0
=0.
$$

Thus

$$
\boxed{
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}=0
\quad\text{under independence.}
}
$$

The usual MI influence function is

$$
\psi_P(i,j)=\ell_P(i,j)-I(P).
$$

Under independence, both terms are zero, so

$$
\psi_P(i,j)=0
$$

for every cell. Its variance is therefore

$$
\begin{aligned}
V(P)
&=\operatorname{Var}_P\{\psi_P(X,Y)\}\\
&=0.
\end{aligned}
$$

The first-order standard-error formula

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{N}
$$

then gives zero under the null. This does not mean that the empirical MI is
exactly zero. It means that its leading sampling variation is not first order.
The second-order term must be retained.

## 8. Derive the Second-Order Term

Let the independent population be

$$
p_{ij}^{(0)}=a_i b_j,
$$

where $a_i>0$ and $b_j>0$ are its row and column marginals. Perturb it by

$$
p_{ij}(\varepsilon)=a_ib_j+\varepsilon h_{ij}.
$$

The perturbed marginals are

$$
p_{i+}(\varepsilon)=a_i+\varepsilon h_{i+},
\qquad
p_{+j}(\varepsilon)=b_j+\varepsilon h_{+j}.
$$

Their independent product is

$$
\begin{aligned}
q_{ij}(\varepsilon)
&=p_{i+}(\varepsilon)p_{+j}(\varepsilon)\\
&=(a_i+\varepsilon h_{i+})(b_j+\varepsilon h_{+j})\\
&=a_ib_j
+\varepsilon(b_jh_{i+}+a_ih_{+j})
+\varepsilon^2h_{i+}h_{+j}.
\end{aligned}
$$

Subtract this reference from the perturbed joint distribution:

$$
\begin{aligned}
p_{ij}(\varepsilon)-q_{ij}(\varepsilon)
&=\varepsilon
\left(h_{ij}-b_jh_{i+}-a_ih_{+j}\right)
+O(\varepsilon^2).
\end{aligned}
$$

Define the first-order association residual

$$
d_{ij}=h_{ij}-b_jh_{i+}-a_ih_{+j}.
$$

The row and column components of the perturbation are removed from $d_{ij}$;
what remains is the part that changes the association between $X$ and $Y$.

### 8.1 Expand the KL divergence

Write the difference between the perturbed joint distribution and its
independent reference as

$$
\Delta_{ij}(\varepsilon)
=p_{ij}(\varepsilon)-q_{ij}(\varepsilon)
=\varepsilon d_{ij}+O(\varepsilon^2).
$$

Because both $P_\varepsilon$ and $Q_\varepsilon$ sum to one,

$$
\sum_{i,j}\Delta_{ij}(\varepsilon)=0.
$$

Now write MI as

$$
I(P_\varepsilon)
=\sum_{i,j}
\left\{q_{ij}(\varepsilon)+\Delta_{ij}(\varepsilon)\right\}
\log\left(
1+\frac{\Delta_{ij}(\varepsilon)}{q_{ij}(\varepsilon)}
\right).
$$

Using the Taylor expansion

$$
\log(1+x)=x-\frac{x^2}{2}+O(x^3),
$$

each summand becomes

$$
\begin{aligned}
\{q_{ij}(\varepsilon)+\Delta_{ij}(\varepsilon)\}
\log\left(1+\frac{\Delta_{ij}(\varepsilon)}
{q_{ij}(\varepsilon)}\right)
&=\{q_{ij}(\varepsilon)+\Delta_{ij}(\varepsilon)\}
\left\{
\frac{\Delta_{ij}(\varepsilon)}{q_{ij}(\varepsilon)}
-\frac{\Delta_{ij}(\varepsilon)^2}
{2q_{ij}(\varepsilon)^2}
\right\}
+O(\varepsilon^3)\\
&=\Delta_{ij}(\varepsilon)
+\frac{\Delta_{ij}(\varepsilon)^2}
{2q_{ij}(\varepsilon)}
+O(\varepsilon^3).
\end{aligned}
$$

Summing over the cells removes the first term because
$\sum_{i,j}\Delta_{ij}(\varepsilon)=0$. Also,

$$
\Delta_{ij}(\varepsilon)^2
=\varepsilon^2d_{ij}^2+O(\varepsilon^3),
$$

and

$$
q_{ij}(\varepsilon)=a_ib_j+O(\varepsilon).
$$

Substitution gives the second-order expansion

$$
\boxed{
I(P_\varepsilon)
=\frac{\varepsilon^2}{2}
\sum_{i,j}\frac{d_{ij}^2}{a_ib_j}
+O(\varepsilon^3).
}
$$

There is no term proportional to $\varepsilon$. MI grows quadratically, rather
than linearly, when a distribution moves away from independence.

## 9. Explain the Change in Sampling Scale

For an empirical contingency table under the independence null,

$$
\widehat p_{ij}-p_{ij}=O_p(N^{-1/2}).
$$

Thus the perturbation size in the preceding expansion is

$$
\varepsilon=O_p(N^{-1/2}).
$$

Because the first nonzero MI term is quadratic,

$$
\widehat I(P)=O_p(\varepsilon^2)=O_p(N^{-1}).
$$

Therefore,

$$
N\widehat I(P)=O_p(1).
$$

Away from independence, a first-order MI error is normally analysed on the
$\sqrt N$ scale. At independence, that first-order term vanishes and MI must
instead be analysed on the $N$ scale. This change of scale is why the normal
or Student reference is replaced by a quadratic-form limit.

## 10. Obtain the Chi-Squared Limit

Under independence, the empirical association residuals are asymptotically
normal. The second-order MI expansion is a weighted sum of their squares.
The same result can be seen directly from the likelihood-ratio statistic.
Define the count residual

$$
R_{ij}=N_{ij}-E_{ij},
$$

so that $N_{ij}=E_{ij}+R_{ij}$. Then

$$
\begin{aligned}
G
&=2\sum_{i,j}(E_{ij}+R_{ij})
\log\left(1+\frac{R_{ij}}{E_{ij}}\right).
\end{aligned}
$$

Using $\log(1+x)\approx x-x^2/2$ gives

$$
\begin{aligned}
G
&\approx
2\sum_{i,j}(E_{ij}+R_{ij})
\left(
\frac{R_{ij}}{E_{ij}}
-\frac{R_{ij}^2}{2E_{ij}^2}
\right)\\
&\approx
2\sum_{i,j}R_{ij}
+\sum_{i,j}\frac{R_{ij}^2}{E_{ij}}.
\end{aligned}
$$

The observed and expected tables have the same total count, so

$$
\sum_{i,j}R_{ij}
=\sum_{i,j}N_{ij}-\sum_{i,j}E_{ij}
=N-N
=0.
$$

Therefore,

$$
\begin{aligned}
G
&\approx\sum_{i,j}\frac{(N_{ij}-E_{ij})^2}{E_{ij}}.
\end{aligned}
$$

The expression on the right is Pearson's chi-squared statistic.

An unrestricted $r\times c$ table has

$$
rc-1
$$

free probability parameters. The independence model has

$$
(r-1)+(c-1)
$$

free marginal parameters. The number of remaining association parameters is

$$
\begin{aligned}
(rc-1)-\{(r-1)+(c-1)\}
&=rc-r-c+1\\
&=(r-1)(c-1).
\end{aligned}
$$

Under the usual large-sample regularity conditions,

$$
\boxed{
2N\widehat I(P)
\xrightarrow{d}
\chi^2_{(r-1)(c-1)}.
}
$$

The chi-squared result is therefore a direct consequence of the second-order
Taylor expansion at the independence boundary.

## 11. Why Expanded Welch Does Not Transfer Directly

For two regular populations with nonzero MI, the current differential-MI test
uses

$$
T
=
\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
}.
$$

The construction depends on the first-order variances $V(P)$ and $V(Q)$. If
$P$ and $Q$ are independent distributions, then

$$
V(P)=V(Q)=0.
$$

The first-order denominator consequently degenerates under the null. Changing
the effective degrees of freedom cannot repair this, because the issue occurs
before the Student reference is chosen: the first-order statistic itself is
not the correct asymptotic representation.

There is also no independent second table when
$\widehat Q=\widehat P_X\widehat P_Y$. The reference is calculated from the
same observations as $\widehat P$, so treating the two quantities as
independent Welch components would introduce a second violation of the
current derivation.

Expanded Welch is therefore appropriate for the regular weak null

$$
I(P)=I(Q)>0,
$$

but not directly for

$$
I(P)=I(Q)=0.
$$

## 12. What Different Constructions of Q Produce

### 12.1 Deterministic empirical reference

Set

$$
\widehat q_{ij}=\widehat p_{i+}\widehat p_{+j}.
$$

Then

$$
D_{\mathrm{KL}}(\widehat P\|\widehat Q)=\widehat I(P),
$$

and the resulting statistic is exactly the likelihood-ratio statistic
$2N\widehat I(P)$. Using its standard asymptotic distribution gives the
classical chi-squared test.

### 12.2 Shuffled reference tables

Hold the observed $X$ values fixed and randomly permute the observed $Y$
values. Each shuffle destroys association while retaining the empirical
marginals. Repeating the shuffle and recomputing MI produces the conditional
permutation null distribution.

This is a permutation test, even if the shuffled observations are first
summarized as a contingency table.

### 12.3 Independently simulated reference tables

Generate new observations from

$$
\widehat Q=\widehat P_X\widehat P_Y.
$$

Repeating this process and recalculating MI gives a parametric bootstrap null
distribution. Unlike permutation, the simulated row and column totals are
generally allowed to vary.

Using only one simulated reference table adds simulation noise without
providing a calibrated reference distribution. Moreover, both empirical MI
values have second-order behaviour when their population MIs are zero, so the
ordinary two-sample Student argument still does not apply.

### 12.4 External reference population

If $Q$ is a genuinely separate real population, the samples from $P$ and $Q$
can be independent. However, if the scientific null requires

$$
I(P)=I(Q)=0,
$$

both MI estimators remain at the same first-order degeneracy. If instead
$I(Q)>0$, the regular differential-MI framework may apply, but equality with
$Q$ is no longer a test of independence.

## 13. Final Interpretation

The independent reference distribution is well defined:

$$
Q=P_XP_Y.
$$

However, this construction does not by itself create a new two-population
test. It gives

$$
D_{\mathrm{KL}}(P\|Q)=I(P)
$$

at the population level and

$$
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)
=2N\widehat I(P)
$$

for an observed table. The inferential method then determines the resulting
test:

- a second-order asymptotic approximation gives the chi-squared test;
- shuffled reference data give a permutation test;
- independently simulated reference data give a parametric bootstrap test.

The construction does not rule out a different deterministic approximation.
For example, one could seek a more accurate finite-sample approximation to
the second-order null distribution for sparse or skewed tables. Such a method
would require a new second-order derivation; it would not be an immediate
extension of the current first-order Expanded Welch method.
