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
3. Expanding MI around independence has no first-order term, so the estimator
   is quadratic in the departure from independence and lives on the $N$ scale
   rather than the $\sqrt N$ scale.
4. That second-order term produces the usual chi-squared limit, and its
   absence at first order is why the Welch construction cannot apply.
   Constructing $Q$ by shuffling or repeated simulation instead produces a
   permutation or bootstrap test.

Sections 1 to 9 give the argument; Appendix A collects the algebra.

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

## 6. The Asymptotic Null and Where Its Approximations Enter

Section 5 showed that the deterministic reference returns the classical
statistic $G=2N\widehat I(P)$ exactly. Its asymptotic null distribution is the
familiar

$$
2N\widehat I(P)
\xrightarrow{d}
\chi^2_{(r-1)(c-1)},
$$

whose practical appeal is that the reference is fixed once the alphabet sizes
are known. That simplicity rests on approximations that are only reliable in
a large-sample regime. This section steps through the key stages, with the
full algebra in Appendix A.

### 6.1 Measure the departure from independence

Under the null the joint distribution factorises as $p_{ij}=p_{i+}p_{+j}$, so
the plug-in estimator measures how far the empirical joint table departs from
the product of its own empirical marginals. Define the empirical deviation
from independence in each cell:

$$
\boxed{
\delta_{ij}
=\widehat p_{ij}-\widehat p_{i+}\widehat p_{+j}.
}
$$

Both $\widehat p_{ij}$ and the fitted product $\widehat p_{i+}\widehat p_{+j}$
are probability tables, so the deviations always cancel:

$$
\sum_{i,j}\delta_{ij}=1-1=0.
$$

This is an identity for any table, not an approximation.

### 6.2 Expand to second order

Substituting $\delta_{ij}$ into the plug-in estimator and expanding around
independence gives (Appendix A.1)

$$
\boxed{
\widehat I(P)
\approx
\frac{1}{2}\sum_{i,j}
\frac{\delta_{ij}^2}
{\widehat p_{i+}\widehat p_{+j}}.
}
$$

Two features of this expansion carry the whole argument.

**There is no first-order term.** The linear contribution is
$\sum_{i,j}\delta_{ij}$, which vanishes identically by Section 6.1. The
cancellation is also unavoidable for a deeper reason: $I\geq0$ with equality
exactly at independence, so an independent table is a global minimum of MI,
and a differentiable function has zero derivative at an interior minimum. No
reparametrisation removes this. Appendix A.3 gives the influence-function
form of the same statement.

**The leading term is quadratic.** MI grows with the *square* of the
departure from independence, so the estimator sits on a different sampling
scale than in the regular case. With $\delta_{ij}=O_p(N^{-1/2})$,

$$
\widehat I(P)=O_p(N^{-1}),
\qquad\text{so}\qquad
2N\widehat I(P)=O_p(1).
$$

### 6.3 Recover the chi-squared reference

Multiplying the expansion by $2N$,

$$
2N\widehat I(P)
\approx
N\sum_{i,j}
\frac{\delta_{ij}^2}
{\widehat p_{i+}\widehat p_{+j}}.
$$

The right-hand side is Pearson's $\chi^2$ statistic written in probability
notation; the two are algebraically identical, not merely close
(Appendix A.2). The degrees of freedom are the $(r-1)(c-1)$ association
directions in which a table can depart from independence (Appendix A.4).
Hence

$$
\boxed{
2N\widehat I(P)
\xrightarrow{d}
\chi^2_{(r-1)(c-1)}.
}
$$

### 6.4 Where the approximation fails

The expansion requires $\delta_{ij}/(\widehat p_{i+}\widehat p_{+j})$ to be
small in every cell, so each fitted cell probability must stay away from
zero. Two regimes break it:

- **Sparse tables.** When expected counts $N\widehat p_{i+}\widehat p_{+j}$
  are small, the neglected cubic term is no longer negligible relative to the
  quadratic one. In the limit of an empty row or column the fitted
  probability is zero and the ratio is undefined.
- **Large alphabets at fixed $N$.** Increasing $rc$ shrinks the average
  expected count, which is the same failure reached from a different
  direction.

This is the boundary the rest of this project is concerned with, and it is
also why the chi-squared reference and the Welch construction of Section 7
fail for related but distinct reasons: the chi-squared limit degrades
gradually as cells empty, whereas the Welch construction is unavailable at
independence for any sample size.

## 7. Why Expanded Welch Does Not Transfer Directly

The differential-MI test statistic

$$
T
=
\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
}
$$

is built on the first-order variances $V(P)$ and $V(Q)$. Appendix A.3 shows
that these are exactly zero at independence, and Section 6.2 explains why
this is forced rather than incidental: the expansion is taken at a global
minimum of $I$, so its first-order term is necessarily absent. Changing the
effective degrees of freedom cannot repair that. The failure occurs before
the Student reference is chosen, because the first-order statistic is not
the correct asymptotic representation of the functional.

A second, independent obstacle is that $\widehat Q=\widehat P_X\widehat P_Y$
is computed from the same observations as $\widehat P$. Treating the two as
independent Welch components would violate the derivation even without the
degeneracy.

Expanded Welch therefore applies to the regular weak null $I(P)=I(Q)>0$, but
not directly to $I(P)=I(Q)=0$.

## 8. What Different Constructions of Q Produce

How $\widehat Q$ is built determines which classical test is recovered. In
every case the quantity being referenced is the same, $\widehat I(P)$; only
the null distribution changes.

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
estimators sit at the same first-order degeneracy of Section 6.2. If instead
$I(Q)>0$, the regular differential-MI framework applies, but equality with
$Q$ is no longer a test of independence.

## 9. Final Interpretation

The independent reference $Q=P_XP_Y$ is well defined, and it satisfies

$$
D_{\mathrm{KL}}(P\|Q)=I(P),
\qquad
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)=2N\widehat I(P).
$$

Constructing it does not, however, create a new two-population test. It
reproduces the classical independence test, and the inferential method chosen
in Section 8 determines which form that test takes.

The reason is the expansion of Section 6: at independence the
first-order term vanishes identically, so the whole first-order Welch
architecture, including its effective degrees of freedom, has nothing to act
on. The leading behaviour is quadratic and lives on the $N$ scale.

This does not rule out a different deterministic approximation. One could
seek a more accurate finite-sample approximation to the second-order null
distribution for sparse or skewed tables. That would require a new
second-order derivation; it would not be an extension of the current
first-order Expanded Welch method.

## Appendix A. Algebraic Details

### A.1 The second-order expansion

Write the fitted independence table and the deviation as

$$
\widehat m_{ij}
=\widehat p_{i+}\widehat p_{+j},
\qquad
\delta_{ij}
=\widehat p_{ij}-\widehat m_{ij},
$$

so that $\widehat p_{ij}=\widehat m_{ij}+\delta_{ij}$. The plug-in estimator
is

$$
\widehat I(P)
=\sum_{i,j}\widehat p_{ij}
\log\left(\frac{\widehat p_{ij}}{\widehat m_{ij}}\right)
=\sum_{i,j}
(\widehat m_{ij}+\delta_{ij})
\log\left(1+\frac{\delta_{ij}}{\widehat m_{ij}}\right).
$$

Apply $\log(1+u)=u-u^2/2+O(u^3)$ with $u=\delta_{ij}/\widehat m_{ij}$:

$$
\begin{aligned}
(\widehat m_{ij}+\delta_{ij})
\left\{
\frac{\delta_{ij}}{\widehat m_{ij}}
-\frac{\delta_{ij}^2}{2\widehat m_{ij}^2}
+O(u^3)
\right\}
&=\delta_{ij}
+\frac{\delta_{ij}^2}{\widehat m_{ij}}
-\frac{\delta_{ij}^2}{2\widehat m_{ij}}
+O\!\left(\frac{\delta_{ij}^3}{\widehat m_{ij}^2}\right)\\
&=\delta_{ij}
+\frac{\delta_{ij}^2}{2\widehat m_{ij}}
+O\!\left(\frac{\delta_{ij}^3}{\widehat m_{ij}^2}\right).
\end{aligned}
$$

Summing over cells and using $\sum_{i,j}\delta_{ij}=0$ removes the linear
term, leaving

$$
\widehat I(P)
=\frac{1}{2}\sum_{i,j}
\frac{\delta_{ij}^2}{\widehat m_{ij}}
+O\!\left(\sum_{i,j}
\frac{\delta_{ij}^3}{\widehat m_{ij}^2}\right).
$$

The neglected term makes the accuracy condition explicit: the expansion is
reliable only while $|\delta_{ij}|\ll\widehat m_{ij}$ in every cell.

### A.2 The Pearson identity

The quadratic form is not merely close to Pearson's statistic; it is equal to
it. With observed and expected counts

$$
N_{ij}=N\widehat p_{ij},
\qquad
E_{ij}=N\widehat m_{ij}
=\frac{N_{i+}N_{+j}}{N},
$$

the count residual is $N_{ij}-E_{ij}=N\delta_{ij}$. Therefore

$$
\begin{aligned}
\sum_{i,j}\frac{(N_{ij}-E_{ij})^2}{E_{ij}}
&=\sum_{i,j}\frac{N^2\delta_{ij}^2}{N\widehat m_{ij}}\\
&=N\sum_{i,j}\frac{\delta_{ij}^2}{\widehat m_{ij}}.
\end{aligned}
$$

The same conclusion follows from the likelihood-ratio form of Section 5.
Writing $R_{ij}=N_{ij}-E_{ij}$ and applying $\log(1+x)\approx x-x^2/2$,

$$
\begin{aligned}
G
&=2\sum_{i,j}(E_{ij}+R_{ij})
\log\left(1+\frac{R_{ij}}{E_{ij}}\right)\\
&\approx
2\sum_{i,j}R_{ij}
+\sum_{i,j}\frac{R_{ij}^2}{E_{ij}}.
\end{aligned}
$$

Observed and expected tables share the same total, so $\sum_{i,j}R_{ij}=0$
and $G\approx\sum_{i,j}(N_{ij}-E_{ij})^2/E_{ij}$.

### A.3 Influence-function form of the degeneracy

Section 6.2 stated that the first-order term is absent. The same fact can be
written in the influence-function language used by the differential-MI Welch
test, which is what Section 7 needs.

Perturb a population $P$ along a direction $H=(h_{ij})$ with
$\sum_{i,j}h_{ij}=0$, setting $P_\varepsilon=P+\varepsilon H$. Writing MI as
three separable sums and using $(u\log u)'=\log u+1$, the constants cancel
and the marginal sums fold back over cells, giving

$$
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}h_{ij}\ell_P(i,j),
$$

where $\ell_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}$ is the pointwise mutual
information. Differentiating once more, with each increment constant in
$\varepsilon$ and $(u\log u)''=1/u$,

$$
\left.\frac{\mathrm d^2}{\mathrm d\varepsilon^2}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}\frac{h_{ij}^2}{p_{ij}}
-\sum_i\frac{h_{i+}^2}{p_{i+}}
-\sum_j\frac{h_{+j}^2}{p_{+j}}.
$$

At independence every $\ell_P(i,j)=\log(1)=0$, so the first derivative
vanishes for every direction $H$. The MI influence function and its variance
collapse with it:

$$
\psi_P(i,j)=\ell_P(i,j)-I(P)=0,
\qquad
V(P)=\operatorname{Var}_P\{\psi_P(X,Y)\}=0.
$$

The first-order standard error $\sqrt{V(P)/N}$ is therefore exactly zero
under the null. This is the population-level counterpart of the missing
linear term in Appendix A.1, and it is what Section 7 uses.

### A.4 Degrees of freedom

Substituting $p_{ij}=a_ib_j$ into the second derivative of Appendix A.3 and
simplifying gives

$$
\left.\frac{\mathrm d^2}{\mathrm d\varepsilon^2}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}\frac{d_{ij}^2}{a_ib_j},
\qquad
d_{ij}=h_{ij}-b_jh_{i+}-a_ih_{+j},
$$

where $d_{ij}$ is the association residual left after the row and column
movement is removed. Moving the margins of an independent table leaves it
independent, so those directions keep $I=0$ and form the null space of the
quadratic form. Counting dimensions:

$$
\underbrace{rc-1}_{\text{perturbations}}
-\underbrace{\{(r-1)+(c-1)\}}_{\text{marginal directions}}
=(r-1)(c-1).
$$

The usual parameter count agrees: an unrestricted $r\times c$ table has
$rc-1$ free probability parameters and the independence model fixes
$(r-1)+(c-1)$ of them through the margins. Both routes count the same thing,
the association directions in which a table can depart from independence,
which is why that number reappears as the degrees of freedom of the limiting
distribution.
