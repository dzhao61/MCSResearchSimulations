# Derivation of the Constrained Likelihood-Ratio Test for Equal Mutual Information

## Purpose

This document derives a likelihood-ratio test for comparing the mutual
information of two independent discrete populations. The null hypothesis is

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are the joint distributions of the same pair of discrete
variables in two populations.

The test compares two multinomial models:

1. An unrestricted model in which $P$ and $Q$ are fitted separately.
2. A constrained model in which they are fitted subject to $I(P)=I(Q)$.

If $\ell_{\mathrm{free}}$ and $\ell_0$ are the maximised log-likelihoods of
these models, the likelihood-ratio statistic is

$$
\boxed{
D=2\{\ell_{\mathrm{free}}-\ell_0\}.
}
$$

The null imposes one scalar restriction. Under the regular large-sample
conditions derived below,

$$
D\overset{H_0}{\approx}\chi_1^2,
$$

so the analytic p-value is

$$
\boxed{
p_{\mathrm{LR}}=\Pr\{\chi_1^2\geq D_{\mathrm{obs}}\}.
}
$$

The derivation will calculate each part in the order in which it is needed:

1. Define the two populations, their mutual informations, and the observed
   contingency tables.
2. Derive the unrestricted multinomial maximum-likelihood estimates and
   $\ell_{\mathrm{free}}$.
3. Define the equal-MI constrained maximum and derive its first-order
   conditions.
4. Derive the LR statistic and show that it is a weighted sum of two
   Kullback-Leibler divergences.
5. Derive the one degree of freedom and the $\chi_1^2$ reference.
6. Derive the probability parameterisation and gradients used to calculate
   the constrained fit numerically.

Population quantities are written without a hat. Unrestricted empirical
estimates are written with a hat, and constrained estimates are written with
a tilde. Natural logarithms are used throughout, so MI is measured in nats.

The corresponding empirical evidence is reported for
[2x2 tables](../experiments/CONSTRAINED_LR_2X2_VALIDATION.md) and
[larger alphabets](../experiments/CONSTRAINED_LR_MULTIALPHABET_VALIDATION.md).

## 1. Define the Two Populations and the Hypothesis

### 1.1 Define the populations and samples

Suppose two independent populations, $P$ and $Q$, describe the same pair of
discrete variables $(X,Y)$, where

$$
X\in\{1,\ldots,r\},
\qquad
Y\in\{1,\ldots,c\}.
$$

The two independent samples are

$$
Z_1^{(P)},\ldots,Z_{n_P}^{(P)}\overset{\mathrm{iid}}{\sim}P,
\qquad
Z_1^{(Q)},\ldots,Z_{n_Q}^{(Q)}\overset{\mathrm{iid}}{\sim}Q,
$$

where each observation is the category pair

$$
Z=(X,Y).
$$

For population $P$, write the joint probabilities as

$$
p_{ij}=\Pr_P(X=i,Y=j),
$$

with margins

$$
p_{i+}=\sum_jp_{ij},
\qquad
p_{+j}=\sum_ip_{ij}.
$$

The corresponding quantities for population $Q$ are $q_{ij}$, $q_{i+}$,
and $q_{+j}$. Each probability table satisfies

$$
p_{ij}\geq0,
\qquad
\sum_{i,j}p_{ij}=1,
$$

and similarly for $Q$.

### 1.2 Define pointwise mutual information and MI

The pointwise mutual information (PMI) in cell $(i,j)$ under population $P$
is

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

The population mutual information is the probability-weighted mean of these
PMI values:

$$
\begin{aligned}
I(P)
&=\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\sum_{i,j}p_{ij}
\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
\end{aligned}
$$

The same definitions give $\ell_Q(i,j)$ and $I(Q)$.

### 1.3 Define the hypothesis

The test concerns one scalar difference:

$$
I(P)-I(Q).
$$

The hypotheses are

$$
\boxed{
H_0:I(P)=I(Q)
}
$$

against

$$
\boxed{
H_1:I(P)\ne I(Q).
}
$$

The null does not require $P=Q$. Their cell probabilities, margins, and
association patterns may differ, provided their scalar MI values are equal.

### 1.4 Define the observed count tables

Let $N_{ij}^{(P)}$ and $N_{ij}^{(Q)}$ be the observed counts in cell $(i,j)$.
Their totals are

$$
n_P=\sum_{i,j}N_{ij}^{(P)},
\qquad
n_Q=\sum_{i,j}N_{ij}^{(Q)}.
$$

The two observed contingency tables contain all information needed for the
multinomial likelihood.

## 2. Derive the Unrestricted Maximum Likelihood

The unrestricted model allows $P$ and $Q$ to vary independently. This section
derives their maximum-likelihood estimates and the best attainable
log-likelihood $\ell_{\mathrm{free}}$.

### 2.1 Write the joint likelihood

For the first multinomial sample,

$$
L_P(P)
=\frac{n_P!}{\prod_{i,j}N_{ij}^{(P)}!}
\prod_{i,j}p_{ij}^{N_{ij}^{(P)}}.
$$

Similarly,

$$
L_Q(Q)
=\frac{n_Q!}{\prod_{i,j}N_{ij}^{(Q)}!}
\prod_{i,j}q_{ij}^{N_{ij}^{(Q)}}.
$$

The two samples are independent, so their combined likelihood is the product

$$
L(P,Q)=L_P(P)L_Q(Q).
$$

Taking logarithms gives

$$
\begin{aligned}
\ell(P,Q)
&=C
+\sum_{i,j}N_{ij}^{(P)}\log p_{ij}
+\sum_{i,j}N_{ij}^{(Q)}\log q_{ij},
\end{aligned}
$$

where $C$ contains the multinomial coefficients. It depends only on the
observed counts, so it is identical in the unrestricted and constrained
models and cancels from the likelihood ratio. We can therefore work with

$$
\boxed{
\ell(P,Q)
=\sum_{i,j}N_{ij}^{(P)}\log p_{ij}
+\sum_{i,j}N_{ij}^{(Q)}\log q_{ij}.
}
$$

### 2.2 Derive the unrestricted estimate of $P$

The part of the log-likelihood involving $P$ is

$$
\ell_P(P)=\sum_{i,j}N_{ij}^{(P)}\log p_{ij}.
$$

Maximise it subject to $\sum_{i,j}p_{ij}=1$. Introduce a Lagrange multiplier
$a_P$:

$$
\mathcal L_P
=\sum_{i,j}N_{ij}^{(P)}\log p_{ij}
+a_P\left(\sum_{i,j}p_{ij}-1\right).
$$

Differentiating with respect to $p_{ij}$ gives

$$
\frac{\partial\mathcal L_P}{\partial p_{ij}}
=\frac{N_{ij}^{(P)}}{p_{ij}}+a_P.
$$

At the maximum,

$$
\frac{N_{ij}^{(P)}}{p_{ij}}+a_P=0,
$$

so

$$
p_{ij}=-\frac{N_{ij}^{(P)}}{a_P}.
$$

Summing over the table and using $\sum_{i,j}p_{ij}=1$ gives

$$
\begin{aligned}
1
&=-\frac{1}{a_P}\sum_{i,j}N_{ij}^{(P)}\\
&=-\frac{n_P}{a_P}.
\end{aligned}
$$

Therefore,

$$
a_P=-n_P,
$$

and the unrestricted maximum-likelihood estimate is

$$
\boxed{
\widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P}.
}
$$

This is the observed cell proportion. A zero observed count gives
$\widehat p_{ij}=0$, with zero log-likelihood contribution under the
convention $0\log0=0$.

### 2.3 Derive the unrestricted estimate of $Q$

The same calculation for the second table gives

$$
\boxed{
\widehat q_{ij}=\frac{N_{ij}^{(Q)}}{n_Q}.
}
$$

The unrestricted model therefore fits each table exactly at its empirical
cell proportions.

### 2.4 Calculate the unrestricted log-likelihood

Substituting the two unrestricted estimates into the log-likelihood gives

$$
\boxed{
\ell_{\mathrm{free}}
=\sum_{i,j}N_{ij}^{(P)}\log\widehat p_{ij}
+\sum_{i,j}N_{ij}^{(Q)}\log\widehat q_{ij}.
}
$$

The unrestricted empirical MI values are

$$
\widehat I(P)
=\sum_{i,j}\widehat p_{ij}
\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right),
$$

and similarly for $\widehat I(Q)$. These values determine whether the
unrestricted fit already satisfies the equal-MI null.

## 3. Derive the Equal-MI Constrained Model

The null model uses the same multinomial likelihood but restricts the fitted
probability tables to have equal MI.

### 3.1 Define the constrained maximum

Define the constrained estimates by

$$
\boxed{
(\widetilde P,\widetilde Q)
=\underset{P,Q}{\operatorname{argmax}}\ \ell(P,Q)
}
$$

subject to

$$
\boxed{
I(P)-I(Q)=0,
}
$$

and the two probability constraints

$$
\sum_{i,j}p_{ij}=1,
\qquad
\sum_{i,j}q_{ij}=1.
$$

The resulting log-likelihood is

$$
\boxed{
\ell_0=\ell(\widetilde P,\widetilde Q).
}
$$

Because the constrained parameter set is contained within the unrestricted
parameter set,

$$
\ell_0\leq\ell_{\mathrm{free}}.
$$

### 3.2 Differentiate mutual information with respect to one cell probability

The first-order conditions for the constrained maximum require the derivative
of MI. Rewrite MI as

$$
I(P)
=\sum_{i,j}p_{ij}\log p_{ij}
-\sum_i p_{i+}\log p_{i+}
-\sum_j p_{+j}\log p_{+j}.
$$

Using

$$
\frac{\mathrm d}{\mathrm du}(u\log u)=\log u+1,
$$

differentiate the three terms with respect to $p_{ij}$:

$$
\begin{aligned}
\frac{\partial I(P)}{\partial p_{ij}}
&=(\log p_{ij}+1)
-(\log p_{i+}+1)
-(\log p_{+j}+1)\\
&=\log p_{ij}-\log p_{i+}-\log p_{+j}-1\\
&=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)-1\\
&=\boxed{\ell_P(i,j)-1}.
\end{aligned}
$$

The derivative depends on the joint probability and both margins. Changing
one cell therefore affects the equal-MI constraint through the complete
probability table.

### 3.3 Derive the constrained first-order conditions

Introduce multipliers $a_P$, $a_Q$, and $\lambda$ for the two normalisation
constraints and the equal-MI constraint:

$$
\begin{aligned}
\mathcal L_0(P,Q)
&=\ell(P,Q)
+a_P\left(\sum_{i,j}p_{ij}-1\right)
+a_Q\left(\sum_{i,j}q_{ij}-1\right)\\
&\quad+\lambda\{I(P)-I(Q)\}.
\end{aligned}
$$

For a cell of $P$,

$$
\begin{aligned}
\frac{\partial\mathcal L_0}{\partial p_{ij}}
&=\frac{N_{ij}^{(P)}}{p_{ij}}
+a_P
+\lambda\frac{\partial I(P)}{\partial p_{ij}}\\
&=\frac{N_{ij}^{(P)}}{p_{ij}}
+a_P
+\lambda\{\ell_P(i,j)-1\}.
\end{aligned}
$$

The corresponding first-order condition is

$$
\boxed{
\frac{N_{ij}^{(P)}}{p_{ij}}
+a_P
+\lambda\{\ell_P(i,j)-1\}=0.
}
$$

For a cell of $Q$, the sign of the MI term is reversed because the constraint
is $I(P)-I(Q)$:

$$
\boxed{
\frac{N_{ij}^{(Q)}}{q_{ij}}
+a_Q
-\lambda\{\ell_Q(i,j)-1\}=0.
}
$$

These equations must hold together with

$$
\sum_{i,j}p_{ij}=1,
\qquad
\sum_{i,j}q_{ij}=1,
\qquad
I(P)=I(Q).
$$

### 3.4 Explain why the constrained estimates require numerical fitting

In the unrestricted model, the multiplier is effectively $\lambda=0$, and
the equations reduce to the observed-proportion estimates. Under the null
constraint, however, each PMI value depends on

$$
p_{ij},\quad p_{i+},\quad p_{+j}
$$

or the corresponding quantities for $Q$. The unknown probabilities therefore
appear both outside and inside logarithms in the first-order conditions.

Consequently, the equations do not reduce to a closed-form expression such as
$N_{ij}/n$. The constrained probability tables must be found by nonlinear
numerical optimisation.

If the unrestricted estimates happen to satisfy

$$
\widehat I(P)=\widehat I(Q),
$$

then they are also feasible under the null. In that case,

$$
(\widetilde P,\widetilde Q)=(\widehat P,\widehat Q),
\qquad
\ell_0=\ell_{\mathrm{free}}.
$$

## 4. Derive the Likelihood-Ratio Statistic

The unrestricted model gives the best fit without the equal-MI restriction.
The constrained model gives the best fit among probability-table pairs that
satisfy the restriction. The likelihood ratio compares these two maxima.

### 4.1 Define the likelihood ratio

The maximised likelihood ratio is

$$
\Lambda
=\frac{L(\widetilde P,\widetilde Q)}
{L(\widehat P,\widehat Q)}.
$$

Since the unrestricted likelihood is at least as large as the constrained
likelihood,

$$
0<\Lambda\leq1.
$$

The conventional LR statistic is

$$
\begin{aligned}
D
&=-2\log\Lambda\\
&=-2\log\left{
\frac{L(\widetilde P,\widetilde Q)}
{L(\widehat P,\widehat Q)}
\right}\\
&=2\left[
\log L(\widehat P,\widehat Q)
-\log L(\widetilde P,\widetilde Q)
\right]\\
&=\boxed{2\{\ell_{\mathrm{free}}-\ell_0\}}.
\end{aligned}
$$

It follows that $D\geq0$.

### 4.2 Expand the statistic over the observed cells

Substituting the two log-likelihoods gives

$$
\begin{aligned}
D
&=2\sum_{i,j}N_{ij}^{(P)}
\{\log\widehat p_{ij}-\log\widetilde p_{ij}\}\\
&\quad+2\sum_{i,j}N_{ij}^{(Q)}
\{\log\widehat q_{ij}-\log\widetilde q_{ij}\}\\
&=2\sum_{i,j}N_{ij}^{(P)}
\log\left(\frac{\widehat p_{ij}}{\widetilde p_{ij}}\right)\\
&\quad+2\sum_{i,j}N_{ij}^{(Q)}
\log\left(\frac{\widehat q_{ij}}{\widetilde q_{ij}}\right).
\end{aligned}
$$

Since $N_{ij}^{(P)}=n_P\widehat p_{ij}$ and
$N_{ij}^{(Q)}=n_Q\widehat q_{ij}$,

$$
\begin{aligned}
D
&=2n_P\sum_{i,j}\widehat p_{ij}
\log\left(\frac{\widehat p_{ij}}{\widetilde p_{ij}}\right)\\
&\quad+2n_Q\sum_{i,j}\widehat q_{ij}
\log\left(\frac{\widehat q_{ij}}{\widetilde q_{ij}}\right).
\end{aligned}
$$

### 4.3 Express the statistic as two KL divergences

For two discrete probability tables $A=(a_{ij})$ and $B=(b_{ij})$, the
Kullback-Leibler divergence is

$$
D_{\mathrm{KL}}(A\Vert B)
=\sum_{i,j}a_{ij}\log\left(\frac{a_{ij}}{b_{ij}}\right).
$$

Therefore,

$$
\boxed{
D
=2n_P D_{\mathrm{KL}}(\widehat P\Vert\widetilde P)
+2n_Q D_{\mathrm{KL}}(\widehat Q\Vert\widetilde Q).
}
$$

This form gives the direct interpretation of the statistic:

- $D_{\mathrm{KL}}(\widehat P\Vert\widetilde P)$ measures how far the first
  empirical table must move to participate in the best equal-MI fit.
- $D_{\mathrm{KL}}(\widehat Q\Vert\widetilde Q)$ measures the corresponding
  movement of the second table.
- The sample sizes weight these two losses because a given probability change
  has more likelihood cost when it contradicts more observations.

If the equal-MI restriction requires little movement, $D$ is small. If it
requires substantial movement from one or both empirical tables, $D$ is
large.

## 5. Derive the Chi-Squared Reference Distribution

The LR statistic becomes a significance test once its null reference
distribution is specified.

### 5.1 Count the unrestricted parameters

Let

$$
K=rc
$$

be the number of cells in each table. A probability table contains $K$
probabilities, but they must sum to one. Population $P$ therefore has

$$
K-1=rc-1
$$

free parameters. Population $Q$ has the same number. The unrestricted model
dimension is

$$
\boxed{
d_{\mathrm{free}}=2(rc-1).
}
$$

For example, two $2\times2$ tables have

$$
d_{\mathrm{free}}=2(4-1)=6
$$

free parameters.

### 5.2 Count the constrained parameters

The equal-MI null adds one scalar equation:

$$
I(P)-I(Q)=0.
$$

When this equation is smooth and its gradient is nonzero, it removes one
free direction from the parameter space. The null model dimension is then

$$
\boxed{
d_0=2(rc-1)-1.
}
$$

The difference in dimensions is

$$
\begin{aligned}
d_{\mathrm{free}}-d_0
&=2(rc-1)-\{2(rc-1)-1\}\\
&=\boxed{1}.
\end{aligned}
$$

The result is one degree of freedom for any fixed table dimensions because
the null tests one scalar MI equality.

### 5.3 Apply Wilks' theorem

Wilks' theorem states that, under a regular null hypothesis and as the sample
sizes increase,

$$
-2\log\Lambda
\overset{d}{\longrightarrow}
\chi^2_{d_{\mathrm{free}}-d_0}.
$$

Since the dimension difference is one,

$$
\boxed{
D\overset{H_0}{\approx}\chi_1^2.
}
$$

The p-value is consequently

$$
\boxed{
p_{\mathrm{LR}}
=1-F_{\chi_1^2}(D_{\mathrm{obs}})
=\Pr\{\chi_1^2\geq D_{\mathrm{obs}}\}.
}
$$

At significance level $\alpha$, reject $H_0$ when

$$
p_{\mathrm{LR}}\leq\alpha,
$$

or equivalently when

$$
D_{\mathrm{obs}}\geq\chi^2_{1,1-\alpha}.
$$

### 5.4 Explain why the degrees of freedom are not $(r-1)(c-1)$

The value $(r-1)(c-1)$ belongs to the ordinary independence test for one
contingency table. That null imposes all restrictions needed to factorise the
joint probabilities as

$$
p_{ij}=p_{i+}p_{+j}.
$$

The present null does not impose independence and does not set MI to zero. It
imposes only

$$
I(P)-I(Q)=0.
$$

This is one scalar restriction, so its regular LR reference has one degree of
freedom.

## 6. Derive the Numerical Constrained Fit

The statistical derivation defines $(\widetilde P,\widetilde Q)$ as a
constrained maximum. This section derives the parameterisation and gradients
used to calculate that maximum.

### 6.1 Represent each probability table by reference-cell logits

Flatten the $r\times c$ cells into indices $1,\ldots,K$, where $K=rc$. For
population $P$, introduce $K-1$ real-valued parameters

$$
\eta_1^{(P)},\ldots,\eta_{K-1}^{(P)}.
$$

Use the final cell as the reference. Define

$$
p_k
=\frac{\exp\{\eta_k^{(P)}\}}
{1+\sum_{m=1}^{K-1}\exp\{\eta_m^{(P)}\}},
\qquad k=1,\ldots,K-1,
$$

and

$$
p_K
=\frac{1}
{1+\sum_{m=1}^{K-1}\exp\{\eta_m^{(P)}\}}.
$$

Every resulting probability is positive and

$$
\sum_{k=1}^Kp_k=1.
$$

The implementation bounds each fitted logit to the interval $[-32,32]$ to
avoid numerically extreme probabilities. This retains an effectively interior
probability table while making the optimization stable.

The same transformation uses $K-1$ parameters for $Q$. The full numerical
problem therefore has

$$
2(K-1)=2(rc-1)
$$

unconstrained real-valued parameters and one equal-MI constraint.

### 6.2 Derive the likelihood gradient in logit coordinates

For one table, write the negative log-likelihood as

$$
J_P(\eta^{(P)})
=-\sum_{m=1}^KN_m^{(P)}\log p_m.
$$

The softmax log-probability derivative is

$$
\frac{\partial\log p_m}{\partial\eta_k^{(P)}}
=\mathbf1\{m=k\}-p_k.
$$

Therefore,

$$
\begin{aligned}
\frac{\partial J_P}{\partial\eta_k^{(P)}}
&=-\sum_{m=1}^KN_m^{(P)}
\{\mathbf1\{m=k\}-p_k\}\\
&=-N_k^{(P)}+p_k\sum_{m=1}^KN_m^{(P)}\\
&=\boxed{n_Pp_k-N_k^{(P)}}.
\end{aligned}
$$

The same calculation gives

$$
\frac{\partial J_Q}{\partial\eta_k^{(Q)}}
=n_Qq_k-N_k^{(Q)}.
$$

The complete objective is

$$
\boxed{
J(\eta^{(P)},\eta^{(Q)})
=-\ell(P,Q)=J_P(\eta^{(P)})+J_Q(\eta^{(Q)}).
}
$$

### 6.3 Derive the MI gradient in logit coordinates

Section 3.2 gave the derivative with respect to a cell probability:

$$
\frac{\partial I(P)}{\partial p_m}
=\ell_P(m)-1.
$$

The probability derivative under the reference-cell softmax is

$$
\frac{\partial p_m}{\partial\eta_k^{(P)}}
=p_m\{\mathbf1\{m=k\}-p_k\}.
$$

Apply the chain rule:

$$
\begin{aligned}
\frac{\partial I(P)}{\partial\eta_k^{(P)}}
&=\sum_{m=1}^K
\frac{\partial I(P)}{\partial p_m}
\frac{\partial p_m}{\partial\eta_k^{(P)}}\\
&=\sum_{m=1}^K
\{\ell_P(m)-1\}
p_m\{\mathbf1\{m=k\}-p_k\}\\
&=p_k\{\ell_P(k)-1\}
-p_k\sum_{m=1}^Kp_m\{\ell_P(m)-1\}.
\end{aligned}
$$

Since

$$
\begin{aligned}
\sum_{m=1}^Kp_m\{\ell_P(m)-1\}
&=\sum_{m=1}^Kp_m\ell_P(m)-\sum_{m=1}^Kp_m\\
&=I(P)-1,
\end{aligned}
$$

the gradient simplifies to

$$
\begin{aligned}
\frac{\partial I(P)}{\partial\eta_k^{(P)}}
&=p_k\{\ell_P(k)-1\}-p_k\{I(P)-1\}\\
&=\boxed{p_k\{\ell_P(k)-I(P)\}}.
\end{aligned}
$$

For the equal-MI constraint

$$
g(\eta^{(P)},\eta^{(Q)})=I(P)-I(Q),
$$

the complete constraint gradient is therefore

$$
\boxed{
\nabla g
=\left[
\left\{p_k(\ell_P(k)-I(P))\right\}_{k=1}^{K-1},
-\left\{q_k(\ell_Q(k)-I(Q))\right\}_{k=1}^{K-1}
\right].
}
$$

This analytic gradient lets the optimiser account for the effect of every
cell on the joint probabilities and both margins.

### 6.4 State the numerical optimisation problem

The numerical problem is

$$
\boxed{
\underset{\eta^{(P)},\eta^{(Q)}}{\operatorname{minimise}}
\ J(\eta^{(P)},\eta^{(Q)})
}
$$

subject to

$$
\boxed{
g(\eta^{(P)},\eta^{(Q)})=I(P)-I(Q)=0.
}
$$

The implementation supplies both $\nabla J$ and $\nabla g$ to the SLSQP
constrained optimiser.

### 6.5 Use multiple starting points

Equal MI does not determine the sign or shape of association. Different
probability-table pairs can satisfy the same MI equality, so one numerical
start may converge to a local constrained solution rather than the largest
constrained likelihood.

The implementation therefore fits up to five starting pairs:

1. The two smoothed empirical tables.
2. The same pooled table for both populations.
3. The smoothed first table for both populations.
4. The smoothed second table for both populations.
5. The uniform table for both populations.

For the empirical starts, $0.5$ is added to every cell before normalisation.
This keeps the starting probabilities inside the simplex when an observed
cell count is zero.

Each acceptable fit must have:

- successful numerical convergence;
- a finite objective value;
- an equal-MI residual no larger than the numerical acceptance threshold
  $\max(10\,\text{tolerance},10^{-7})$;
- a constrained objective no better than the unrestricted objective, apart
  from numerical tolerance.

Among the acceptable fits, the implementation selects the one with the
smallest negative log-likelihood, equivalently the largest constrained
likelihood.

### 6.6 Calculate the statistic from the fitted objective

Let

$$
J_{\mathrm{free}}=-\ell_{\mathrm{free}},
\qquad
J_0=-\ell_0.
$$

Then

$$
\begin{aligned}
D
&=2\{\ell_{\mathrm{free}}-\ell_0\}\\
&=2\{-J_{\mathrm{free}}+J_0\}\\
&=\boxed{2\{J_0-J_{\mathrm{free}}\}}.
\end{aligned}
$$

The implementation sets numerically negligible negative gaps to zero and
then calculates

$$
p_{\mathrm{LR}}=\Pr\{\chi_1^2\geq D\}.
$$

## 7. Complete Test Algorithm

For two observed $r\times c$ count tables, the complete usable test is:

1. Calculate the unrestricted probabilities

   $$
   \widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P},
   \qquad
   \widehat q_{ij}=\frac{N_{ij}^{(Q)}}{n_Q}.
   $$

2. Calculate the unrestricted log-likelihood

   $$
   \ell_{\mathrm{free}}=\ell(\widehat P,\widehat Q).
   $$

3. Numerically maximise the same likelihood subject to

   $$
   I(P)=I(Q)
   $$

   to obtain $(\widetilde P,\widetilde Q)$ and

   $$
   \ell_0=\ell(\widetilde P,\widetilde Q).
   $$

4. Calculate

   $$
   D=2\{\ell_{\mathrm{free}}-\ell_0\}.
   $$

5. Calculate

   $$
   p_{\mathrm{LR}}=\Pr\{\chi_1^2\geq D\}.
   $$

6. Reject equal MI at significance level $\alpha$ when

   $$
   p_{\mathrm{LR}}\leq\alpha.
   $$

## 8. Summary of the Derived Quantities

| Quantity | Definition | Statistical role |
| --- | --- | --- |
| $\widehat P,\widehat Q$ | Observed cell proportions | Unrestricted multinomial estimates |
| $\widetilde P,\widetilde Q$ | Maximum-likelihood tables subject to $I(P)=I(Q)$ | Best-fitting null model |
| $\ell_{\mathrm{free}}$ | $\ell(\widehat P,\widehat Q)$ | Best fit without equal MI |
| $\ell_0$ | $\ell(\widetilde P,\widetilde Q)$ | Best fit with equal MI |
| $\Lambda$ | $L(\widetilde P,\widetilde Q)/L(\widehat P,\widehat Q)$ | Relative fit of the null model |
| $D$ | $-2\log\Lambda$ | Loss of fit caused by equal MI |
| Reference law | $\chi_1^2$ | Regular large-sample null approximation |
| $p_{\mathrm{LR}}$ | $\Pr(\chi_1^2\geq D)$ | Significance of the observed loss of fit |

The complete logic is

$$
\begin{aligned}
\text{observed counts}
&\longrightarrow (\widehat P,\widehat Q)
\longrightarrow \ell_{\mathrm{free}},\\
\text{equal-MI restriction}
&\longrightarrow (\widetilde P,\widetilde Q)
\longrightarrow \ell_0,\\
\text{likelihood loss}
&\longrightarrow D=2(\ell_{\mathrm{free}}-\ell_0)
\longrightarrow \chi_1^2\text{ p-value}.
\end{aligned}
$$

## 9. Why This Construction Differs from Expanded Welch

Expanded Welch begins with the estimated scalar difference

$$
\widehat I(P)-\widehat I(Q)
$$

and divides it by an estimated standard error. It must therefore derive the
sampling variance of estimated MI and the uncertainty of that variance
estimate.

The LR test instead compares two full multinomial models. It asks how much
likelihood is lost when the fitted probability tables are forced to satisfy

$$
I(P)=I(Q).
$$

Consequently, the LR statistic does not contain:

- an MI standard error;
- a PMI variance estimate;
- a Welch-Satterthwaite degrees-of-freedom calculation;
- a Student reference distribution.

It also does not subtract the leading plug-in MI bias from the two empirical
MI values. The empirical MI values are features of the unrestricted
multinomial maximum-likelihood estimates, while inference is based on the
likelihood difference between the unrestricted and constrained models.
Finite-sample bias can still affect the accuracy of the asymptotic reference,
but it is not corrected by altering the two model likelihoods.

## 10. Assumptions and Scope

### 10.1 Statistical assumptions

The derivation uses:

- independent observations within each sample;
- independence between the samples from $P$ and $Q$;
- multinomial sampling conditional on $n_P$ and $n_Q$;
- fixed finite table dimensions;
- a smooth interior null parameter;
- a nonzero gradient of the equal-MI constraint;
- sufficiently large samples for Wilks' theorem;
- a correctly obtained global constrained maximum.

The current implementation requires the two observed tables to have matching
dimensions.

### 10.2 Nonregular cases

The $\chi_1^2$ result requires the null constraint to remove one locally
identifiable direction. This can fail near independence. At an independent
distribution,

$$
\ell_P(i,j)=0,
\qquad
I(P)=0,
$$

so the logit gradient derived in Section 6.3 becomes

$$
\frac{\partial I(P)}{\partial\eta_k^{(P)}}
=p_k\{\ell_P(k)-I(P)\}=0.
$$

The MI constraint then has no nonzero first-order direction, and the ordinary
one-restriction version of Wilks' theorem need not apply. Probability
boundaries and widespread empirical zeros can cause related failures of the
smooth interior approximation.

These cases can make the raw $\chi_1^2$ LR conservative or liberal in finite
samples. They do not change the definition of $D$, but they can change its
null distribution away from the regular asymptotic reference.

### 10.3 Computational scope

For $K=rc$ cells, the numerical fit has

$$
2(K-1)=2(rc-1)
$$

parameters. A likelihood or gradient evaluation requires $O(rc)$ work, but
the current SLSQP implementation solves a dense constrained optimisation from
multiple starts. Its total cost therefore grows much faster than the $O(rc)$
closed-form Expanded Welch calculation.

The method is computationally practical for the current $2\times2$ through
$8\times8$ experiments. Median measured time per table pair increased from
approximately 5--8 ms for $2\times2$ to 151--169 ms for $8\times8$, with some
difficult $8\times8$ fits taking more than one second. The five deterministic
starts reduce observed local-optimum failures, but they do not prove that the
global constrained maximum has been found. Larger tables or high-throughput
use may require a specialised optimiser that exploits the single equal-MI
constraint.

## References

- Kullback, S., and Leibler, R. A. (1951). *On Information and Sufficiency*.
  The Annals of Mathematical Statistics, 22(1), 79-86.
- Wilks, S. S. (1938). *The Large-Sample Distribution of the Likelihood Ratio
  for Testing Composite Hypotheses*. The Annals of Mathematical Statistics,
  9(1), 60-62.
- Self, S. G., and Liang, K.-Y. (1987). *Asymptotic Properties of Maximum
  Likelihood Estimators and Likelihood Ratio Tests under Nonstandard
  Conditions*. Journal of the American Statistical Association, 82(398),
  605-610.
