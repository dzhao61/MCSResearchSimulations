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

The conclusion of this document is that the construction is well defined but
does not produce a new two-sample test. Specifically:

1. The reference $Q=P_XP_Y$ exists and has $I(Q)=0$, so the proposed null
   $I(P)=I(Q)$ is the ordinary null of independence in $P$ (Sections 1-2).
2. The comparison of $P$ with $Q$ is exactly mutual information, and on an
   observed table it returns exactly the classical likelihood-ratio statistic
   $G=2N\widehat I(P)$ (Sections 3-5).
3. The Expanded Welch reference cannot calibrate it, because the first-order
   MI variance is identically zero at independence (Section 6).
4. What remains is a choice of null distribution for a classical statistic:
   asymptotic, permutation, or bootstrap (Section 7).

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


## 6. Why Expanded Welch Cannot Calibrate It

Sections 1 to 5 settle what the construction *is*. It remains to ask whether
the Expanded Welch reference could be used to calibrate it, since that
reference is designed for exactly this statistic's numerator. It cannot, and
the reason needs no new machinery.

The differential-MI test statistic is

$$
T
=
\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
},
\qquad
V(P)=\operatorname{Var}_P\{\ell_P(X,Y)\}.
$$

Its denominator is built from the variance of the pointwise mutual
information. Section 2.3 already showed that a table which factorises has
$\ell=\log(1)=0$ in every cell. Under the null that argument applies to $P$
itself, so

$$
\boxed{
\ell_P(i,j)=0
\ \text{for every cell},
\qquad
V(P)=0.
}
$$

The estimated standard error is therefore zero and $T$ is undefined. This is
not a matter of choosing better degrees of freedom: the Welch construction
adjusts the *reference distribution* for a statistic whose denominator is
assumed positive, and here the denominator degenerates before any reference
is chosen. A finite-df correction has nothing to act on.

Two further points follow.

The degeneracy is unavoidable rather than incidental. Mutual information
satisfies $I\geq0$ with equality exactly at independence, so an independent
table is a global minimum of $I$. A differentiable function has zero
derivative at an interior minimum, so the first-order term of any expansion
of MI about independence is necessarily absent. No reparametrisation or
alternative variance estimator recovers it. The correct leading behaviour is
quadratic, which is why the classical reference for $2N\widehat I(P)$ is a
chi-squared law on the $N$ scale rather than a normal or Student law on the
$\sqrt N$ scale.

There is also no second independent sample. Because
$\widehat Q=\widehat P_X\widehat P_Y$ is computed from the same observations
as $\widehat P$, treating the two as independent Welch components would
violate the derivation even if the variances were positive.

Expanded Welch therefore applies to the regular weak null $I(P)=I(Q)>0$, but
not to $I(P)=I(Q)=0$.

## 7. What Different Constructions of Q Produce

Since the statistic is fixed at $2N\widehat I(P)$, all that remains is the
choice of null distribution. How $\widehat Q$ is built determines which
classical test is recovered.

| Construction of $\widehat Q$ | Resulting test |
| --- | --- |
| Deterministic, $\widehat q_{ij}=\widehat p_{i+}\widehat p_{+j}$ | Likelihood-ratio statistic $2N\widehat I(P)$ with its $\chi^2_{(r-1)(c-1)}$ limit |
| Shuffle $Y$ against fixed $X$, repeatedly | Conditional permutation test, marginals held fixed |
| Simulate new tables from $\widehat P_X\widehat P_Y$ | Parametric bootstrap, marginals free to vary |
| A genuinely separate population | Two-sample test, but see below |

Two caveats attach to this table.

Using only a *single* simulated reference table adds simulation noise without
providing a calibrated null distribution, and both MI estimates still have
second-order behaviour when their population MIs are zero, so the ordinary
two-sample Student argument does not apply.

For an external reference population the two samples genuinely are
independent. But if the scientific null requires $I(P)=I(Q)=0$, both
estimators sit at the same degeneracy of Section 6. If instead $I(Q)>0$, the
regular differential-MI framework applies, but equality with $Q$ is no longer
a test of independence.

## 8. Final Interpretation

The independent reference $Q=P_XP_Y$ is well defined, and it satisfies

$$
D_{\mathrm{KL}}(P\|Q)=I(P),
\qquad
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)=2N\widehat I(P).
$$

Constructing it does not create a new two-population test. It reproduces the
classical independence test, and the inferential method chosen in Section 7
determines which form that test takes. The Welch architecture is unavailable
because the quantity it calibrates, the first-order MI variance, is exactly
zero at independence.

This does not rule out a different deterministic approximation. The classical
chi-squared reference is itself a large-sample approximation, and it degrades
when expected cell counts are small, which is the regime of interest
elsewhere in this project. A better finite-sample reference for
$2N\widehat I(P)$ in sparse tables remains open, but it would require a
second-order derivation; it would not be an extension of the current
first-order Expanded Welch method.
