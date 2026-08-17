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

By the standard large-sample result for the $G$-test (Wilks' theorem), under
independence

$$
G\ \xrightarrow{d}\ \chi^2_{(r-1)(c-1)},
\qquad
p=\Pr\!\left\{\chi^2_{(r-1)(c-1)}\geq G_{\mathrm{obs}}\right\}.
$$

Thus $G$ is the observed statistic and the chi-squared distribution is its
reference distribution.


## 6. Why Expanded Welch Cannot Calibrate It

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
information. Under independence, $p_{ij}=p_{i+}p_{+j}$, so

$$
\boxed{
\ell_P(i,j)=0
\ \text{for every cell},
\qquad
V(P)=0.
}
$$

The population first-order variance is therefore zero. MI is at its minimum at
independence, so its first derivative vanishes and its leading random term is
second order. This second-order behaviour produces the chi-squared limit for
$2N\widehat I(P)$; changing Welch degrees of freedom cannot restore a missing
first-order term.

Moreover, $\widehat Q=\widehat P_X\widehat P_Y$ is calculated from the same
table as $\widehat P$. They are not two independent samples, as required by the
two-sample Welch derivation. Expanded Welch therefore applies to regular
equal-MI comparisons away from independence, not to this independence test.

## 7. What Different Constructions of Q Produce

Since the statistic is fixed at $2N\widehat I(P)$, all that remains is the
choice of how to calibrate its null distribution.

| Construction of $\widehat Q$ | Resulting test |
| --- | --- |
| Deterministic, $\widehat q_{ij}=\widehat p_{i+}\widehat p_{+j}$ | Likelihood-ratio statistic $2N\widehat I(P)$ with its $\chi^2_{(r-1)(c-1)}$ limit |
| Shuffle $Y$ against fixed $X$, repeatedly | Conditional permutation test, marginals held fixed |
| Simulate new tables from $\widehat P_X\widehat P_Y$ | Parametric bootstrap, marginals free to vary |
| A separate sampled reference population | Two-sample equal-MI test, not the standard one-table independence test |

A single simulated reference table is not sufficient because it adds Monte
Carlo noise without estimating a null distribution. Repeated shuffling or
simulation gives a valid resampling reference, while the deterministic choice
returns the usual analytic $G$-test.

## 8. Final Interpretation

The independent reference $Q=P_XP_Y$ is well defined, and it satisfies

$$
D_{\mathrm{KL}}(P\|Q)=I(P),
\qquad
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)=2N\widehat I(P).
$$

Constructing it does not create a new two-population test. It reproduces the
classical $G$-test when it is constructed deterministically, or a standard
resampling test when it is repeatedly sampled. Expanded Welch does not apply
because its first-order MI variance vanishes at independence.

The chi-squared reference can still be inaccurate in sparse tables. Improving
that approximation would require a finite-sample, second-order treatment of
$G$, rather than an extension of the current first-order Welch method.
