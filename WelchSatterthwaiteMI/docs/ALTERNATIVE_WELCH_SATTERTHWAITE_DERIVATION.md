# An Alternative Derivation of the Expanded Welch-Satterthwaite MI Test

## Purpose

This document derives the expanded Welch-Satterthwaite mutual-information
test by starting from the general Welch-Satterthwaite equation and identifying
each of its inputs for two independent contingency tables.

The central question is how the generic quantities

$$
k_i,
\qquad
s_i^2,
\qquad
\nu_i
$$

should be defined when the estimated quantities being compared are mutual
informations rather than ordinary sample means.

The derivation proceeds in the following order:

1. estimate the difference $I(P)-I(Q)$;
2. state the general Welch-Satterthwaite equation;
3. derive the MI variance estimates that play the role of $s_i^2$;
4. derive the weights $k_i$ that convert them into sampling variances;
5. derive the MI-specific component degrees of freedom $\nu_i$;
6. substitute all three quantities into the general equation.

Natural logarithms are used throughout, so mutual information is measured in
nats.

## 1. Estimate the Difference in Mutual Information

### 1.1 Define the two populations

Suppose two independent populations, $P$ and $Q$, describe the same pair of
discrete variables $(X,Y)$. The aim is to test

$$
H_0:I(P)=I(Q)
\qquad\text{against}\qquad
H_1:I(P)\ne I(Q).
$$

The two samples are

$$
Z_1^{(P)},\ldots,Z_{n_P}^{(P)}\overset{\mathrm{iid}}{\sim}P,
\qquad
Z_1^{(Q)},\ldots,Z_{n_Q}^{(Q)}\overset{\mathrm{iid}}{\sim}Q,
$$

where each observation is

$$
Z=(X,Y)\in\{1,\ldots,r\}\times\{1,\ldots,c\}.
$$

For population $P$, write the joint and marginal probabilities as

$$
p_{ij}=\Pr_P(X=i,Y=j),
$$

$$
p_{i+}=\sum_jp_{ij},
\qquad
p_{+j}=\sum_ip_{ij}.
$$

The corresponding probabilities for population $Q$ are denoted by $q_{ij}$,
$q_{i+}$, and $q_{+j}$.

### 1.2 Define pointwise mutual information and population MI

The pointwise mutual information (PMI) for cell $(i,j)$ under population $P$
is

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

Mutual information is the probability-weighted mean of the PMI values:

$$
\begin{aligned}
I(P)
&=\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\operatorname E_P\{\ell_P(X,Y)\}.
\end{aligned}
$$

The same definitions give $\ell_Q(i,j)$ and $I(Q)$ for population $Q$.

### 1.3 Estimate MI from each contingency table

Let $N_{ij}^{(P)}$ be the observed count in cell $(i,j)$ of the first table.
The empirical probabilities are

$$
\widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P},
\qquad
n_P=\sum_{i,j}N_{ij}^{(P)},
$$

with empirical margins

$$
\widehat p_{i+}=\sum_j\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_i\widehat p_{ij}.
$$

The empirical PMI values and plug-in MI estimate are

$$
\widehat\ell_P(i,j)
=\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right),
$$

$$
\widehat I(P)
=\sum_{i,j}\widehat p_{ij}\widehat\ell_P(i,j).
$$

Terms with $\widehat p_{ij}=0$ contribute zero under the convention
$0\log 0=0$.

### 1.4 Correct the leading plug-in bias

For a fixed $r\times c$ alphabet with full population support, the leading
plug-in bias is

$$
\operatorname{Bias}\{\widehat I(P)\}
\approx\frac{(r-1)(c-1)}{2n_P}.
$$

Define

$$
d=(r-1)(c-1).
$$

The bias-corrected MI estimates are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P},
$$

$$
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated MI difference is therefore

$$
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q).
$$

At fixed sample sizes and table dimensions, the bias corrections are
constants. They change the centre of the estimated difference while leaving
its first-order sampling variance unchanged.

## 2. Start from the General Welch-Satterthwaite Equation

The presentation in this section follows the general statement of the
[Welch-Satterthwaite equation](https://en.wikipedia.org/wiki/Welch%E2%80%93Satterthwaite_equation).

Suppose there are $m$ independent estimated variances

$$
s_1^2,\ldots,s_m^2,
$$

where $s_i^2$ has $\nu_i$ component degrees of freedom. Let $k_i>0$ be the
weight applied to the $i$th estimated variance. Their weighted sum is

$$
\chi'=\sum_{i=1}^m k_i s_i^2.
$$

The exact distribution of this sum generally has no simple closed form when
the components have different scales. Welch-Satterthwaite approximates it by
a single scaled chi-squared variable. The effective degrees of freedom are

$$
\boxed{
\nu_{\chi'}
\approx
\frac{
\left(\displaystyle\sum_{i=1}^m k_i s_i^2\right)^2
}{
\displaystyle\sum_{i=1}^m
\frac{(k_i s_i^2)^2}{\nu_i}
}.
}
$$

This equation does not require the underlying population variances to be
equal. It requires a set of independent estimated variance components, their
weights, and a component degrees-of-freedom value for each one.

For two MI populations, there are exactly two components. The required
mapping is

| Generic quantity | Population $P$ | Population $Q$ | Statistical role |
| --- | --- | --- | --- |
| $s_i^2$ | $\widehat V(P)$ | $\widehat V(Q)$ | Estimated observation-level variance governing plug-in MI |
| $k_i$ | $1/n_P$ | $1/n_Q$ | Converts observation-level variance into variance of an MI estimate |
| $k_i s_i^2$ | $\widehat V(P)/n_P$ | $\widehat V(Q)/n_Q$ | Contribution to the squared standard error |
| $\nu_i$ | $\widehat\nu_V(P)$ | $\widehat\nu_V(Q)$ | Effective reliability of the estimated MI variance |

The remaining sections derive every entry in this table.

## 3. Derive the Variance Estimates $s_i^2$

### 3.1 Identify the observation-level quantity governing MI

The population MI is the mean of the random PMI value:

$$
I(P)=\operatorname E_P\{\ell_P(X,Y)\}.
$$

The first-order change in MI produced by an observation in cell $(x,y)$ is

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P),
$$

where

$$
P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

The variance of these centred PMI values is

$$
\boxed{
V(P)
=\operatorname{Var}_P\{\ell_P(X,Y)\}
=\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2.
}
$$

The functional delta method then gives

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}.
$$

### 3.2 Estimate $V(P)$ from the sampled table

Replacing the population probabilities and PMI values with their empirical
counterparts gives

$$
\boxed{
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2.
}
$$

This is the first estimated variance required by the generic equation.
Therefore,

$$
\boxed{s_P^2=\widehat V(P).}
$$

Repeating the calculation for the second table gives

$$
\boxed{s_Q^2=\widehat V(Q).}
$$

The notation $s_P^2$ and $s_Q^2$ is used only to identify the generic
Welch-Satterthwaite inputs. The MI notation remains $\widehat V(P)$ and
$\widehat V(Q)$ in the final test.

## 4. Derive the Weights $k_i$

### 4.1 Add the sampling variances of the two MI estimates

The samples from $P$ and $Q$ are independent. Therefore,

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)-\widehat I(Q)\}
&=\operatorname{Var}\{\widehat I(P)\}
+\operatorname{Var}\{\widehat I(Q)\}\\
&\approx\frac{V(P)}{n_P}+\frac{V(Q)}{n_Q}.
\end{aligned}
$$

The empirical squared standard error is consequently

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

### 4.2 Match this sum to $\sum_i k_i s_i^2$

The generic weighted sum for two components is

$$
\chi'=k_Ps_P^2+k_Qs_Q^2.
$$

Using

$$
s_P^2=\widehat V(P),
\qquad
s_Q^2=\widehat V(Q),
$$

and matching $\chi'$ to the squared standard error gives

$$
k_P\widehat V(P)+k_Q\widehat V(Q)
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

The weights are therefore

$$
\boxed{k_P=\frac{1}{n_P},}
\qquad
\boxed{k_Q=\frac{1}{n_Q}.}
$$

The weighted components entering the final denominator are

$$
\boxed{k_Ps_P^2=\frac{\widehat V(P)}{n_P},}
\qquad
\boxed{k_Qs_Q^2=\frac{\widehat V(Q)}{n_Q}.}
$$

## 5. Derive the Component Degrees of Freedom $\nu_i$

The component degrees of freedom must describe the sampling reliability of
$\widehat V(P)$ and $\widehat V(Q)$. This requires the sampling variance of
each estimated MI variance.

### 5.1 Express $V(P)$ using two moments

Define the second PMI moment

$$
M_2(P)
=\operatorname E_P\{\ell_P(X,Y)^2\}
=\sum_{i,j}p_{ij}\ell_P(i,j)^2.
$$

Because variance equals the second moment minus the squared mean,

$$
V(P)=M_2(P)-I(P)^2.
$$

This form lets us differentiate the complete variance functional directly.

### 5.2 Define the cell perturbation

For a selected cell $(x,y)$, define

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

For an arbitrary cell $(i,j)$,

$$
\left.p_{ij}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{i=x,j=y\}-p_{ij}.
$$

The marginal derivatives are

$$
\left.p_{i+}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{i=x\}-p_{i+},
$$

$$
\left.p_{+j}'(\varepsilon)\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

### 5.3 Differentiate the PMI values

Along the perturbation path,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Using $(\log u)'=u'/u$ gives

$$
\boxed{
\ell_P'(i,j;x,y)
=\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
}
$$

### 5.4 Differentiate MI

Start from

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)\ell_{P_\varepsilon}(i,j).
$$

The product rule gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\sum_{i,j}p_{ij}'(0)\ell_P(i,j)
+\sum_{i,j}p_{ij}\ell_P'(i,j;x,y).
$$

The first sum is

$$
\ell_P(x,y)-I(P).
$$

For the second sum,

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P'(i,j;x,y)
&=\frac{p_{xy}}{p_{xy}}
-\frac{\sum_jp_{xj}}{p_{x+}}
-\frac{\sum_ip_{iy}}{p_{+y}}
+\sum_{i,j}p_{ij}\\
&=1-1-1+1\\
&=0.
\end{aligned}
$$

Therefore,

$$
\boxed{
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P).
}
$$

### 5.5 Differentiate the second PMI moment

The second moment under the perturbed distribution is

$$
M_2(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j)^2.
$$

Applying the product rule and $(\ell^2)'=2\ell\ell'$ gives

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\sum_{i,j}p_{ij}'(0)\ell_P(i,j)^2\\
&+2\sum_{i,j}p_{ij}\ell_P(i,j)\ell_P'(i,j;x,y).
\end{aligned}
$$

The first sum is

$$
\ell_P(x,y)^2-M_2(P).
$$

Define the probability-weighted mean PMI values within row $x$ and column $y$:

$$
R_P(x)
=\frac{1}{p_{x+}}\sum_jp_{xj}\ell_P(x,j),
$$

$$
C_P(y)
=\frac{1}{p_{+y}}\sum_ip_{iy}\ell_P(i,y).
$$

Substituting the PMI derivative into the second sum gives

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P(i,j)\ell_P'(i,j;x,y)
={}&\ell_P(x,y)-R_P(x)-C_P(y)+I(P).
\end{aligned}
$$

Hence,

$$
\boxed{
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\ell_P(x,y)^2-M_2(P)\\
&+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}.
\end{aligned}
}
$$

### 5.6 Derive the variance influence function $g_P(x,y)$

Define

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Since $V(P)=M_2(P)-I(P)^2$,

$$
\begin{aligned}
g_P(x,y)
={}&\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}\\
&-2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Substituting the derivatives gives

$$
\boxed{
\begin{aligned}
g_P(x,y)
={}&\{\ell_P(x,y)-I(P)\}^2-V(P)\\
&+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}.
\end{aligned}
}
$$

This quantity measures how one possible observation changes the complete MI
variance, including the changes to the joint probabilities, row margins,
column margins, PMI values, and MI itself.

### 5.7 Derive the sampling variance of $\widehat V(P)$

Define

$$
\boxed{
\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}.
}
$$

To first order,

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)}).
$$

The observations are independent, so

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\sum_{k=1}^{n_P}\operatorname{Var}_P\{g_P(Z_k^{(P)})\}\\
&=\frac{1}{n_P^2}n_P\tau^2(P)\\
&=\boxed{\frac{\tau^2(P)}{n_P}}.
\end{aligned}
$$

### 5.8 Convert this uncertainty into $\nu_P$

Satterthwaite represents the sampling distribution of $\widehat V(P)$ by the
scaled chi-squared model

$$
\widehat V(P)
\quad\text{is modelled by}\quad
V(P)\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}.
$$

This model is used because variance estimates are built from squared sampling
deviations, and sums of squared approximately normal deviations naturally
lead to chi-squared distributions.

The scaled model has mean and variance

$$
V(P)
\qquad\text{and}\qquad
\frac{2V(P)^2}{\nu_V(P)}.
$$

Matching its variance to the derived sampling variance of $\widehat V(P)$
gives

$$
\frac{2V(P)^2}{\nu_V(P)}
=\frac{\tau^2(P)}{n_P}.
$$

Solving for the component degrees of freedom gives

$$
\boxed{
\nu_V(P)
=\frac{2n_PV(P)^2}{\tau^2(P)}.
}
$$

The observed table supplies the plug-in estimates $\widehat V(P)$ and
$\widehat\tau^2(P)$, producing

$$
\boxed{
\widehat\nu_V(P)
=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
}
$$

Therefore, the generic component degrees of freedom for population $P$ are

$$
\boxed{\nu_P=\widehat\nu_V(P).}
$$

Repeating the derivation for $Q$ gives

$$
\boxed{\nu_Q=\widehat\nu_V(Q).}
$$

## 6. Substitute the MI Quantities into Welch-Satterthwaite

The generic two-component equation is

$$
\nu_{\chi'}
\approx
\frac{(k_Ps_P^2+k_Qs_Q^2)^2}
{(k_Ps_P^2)^2/\nu_P+(k_Qs_Q^2)^2/\nu_Q}.
$$

The derived MI inputs are

$$
k_P=\frac{1}{n_P},
\qquad
s_P^2=\widehat V(P),
\qquad
\nu_P=\widehat\nu_V(P),
$$

and

$$
k_Q=\frac{1}{n_Q},
\qquad
s_Q^2=\widehat V(Q),
\qquad
\nu_Q=\widehat\nu_V(Q).
$$

Substitution gives the expanded Welch-Satterthwaite degrees of freedom:

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_V(P)
+\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_V(Q)
}.
}
$$

The test statistic is

$$
\boxed{
T
=\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
}.
}
$$

Expanded Welch compares $T$ with a Student distribution having
$\widehat\nu_{\mathrm{expanded}}$ degrees of freedom. The two-sided p-value is

$$
\boxed{
p_{\mathrm{expanded}}
=2\left[
1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)
\right].
}
$$

## 7. Bias-Corrected Welch-Satterthwaite Combination

The Wikipedia article also reports a recent fourth-moment correction to the
generic combination formula:

$$
\nu_{\chi'}^{(\mathrm{corr})}
\approx
\frac{
\left(\displaystyle\sum_{i=1}^m k_i s_i^2\right)^2
}{
\displaystyle\sum_{i=1}^m
\frac{(k_i s_i^2)^2}{\nu_i+2}
}
-2.
$$

Using the same MI inputs gives

$$
\boxed{
\widehat\nu_{\mathrm{corrected}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/
\{\widehat\nu_V(P)+2\}
+\left\{\widehat V(Q)/n_Q\right\}^2/
\{\widehat\nu_V(Q)+2\}
}
-2.
}
$$

This correction was tested on 192 null configurations with 10,000 simulated
table pairs per configuration. It reduced aggregate mean absolute
false-positive-rate error by 2.6%, 1.7%, and 1.2% at alpha levels 0.10, 0.05,
and 0.01. Almost all of that improvement came from the widespread-sparsity
regime. Outside that regime it was effectively tied and slightly worse,
including in the sparse and skewed target regimes. The primary method
therefore retains the original expanded Welch-Satterthwaite combination.

The complete comparison is recorded in
[`../results/corrected_satterthwaite_full/REPORT.md`](../results/corrected_satterthwaite_full/REPORT.md).

## 8. Final Mapping

The complete connection between the general equation and the MI test is

| General input | MI definition | How it is obtained |
| --- | --- | --- |
| $s_P^2$ | $\widehat V(P)$ | Probability-weighted variance of empirical PMI values |
| $s_Q^2$ | $\widehat V(Q)$ | Same calculation for population $Q$ |
| $k_P$ | $1/n_P$ | Variance of a sample mean is observation-level variance divided by sample size |
| $k_Q$ | $1/n_Q$ | Same calculation for population $Q$ |
| $\nu_P$ | $\widehat\nu_V(P)=2n_P\widehat V(P)^2/\widehat\tau^2(P)$ | Satterthwaite moment matching for $\widehat V(P)$ |
| $\nu_Q$ | $\widehat\nu_V(Q)=2n_Q\widehat V(Q)^2/\widehat\tau^2(Q)$ | Same calculation for population $Q$ |
| $\chi'$ | $\widehat V(P)/n_P+\widehat V(Q)/n_Q$ | Estimated sampling variance of the MI difference |
| $\nu_{\chi'}$ | $\widehat\nu_{\mathrm{expanded}}$ | Effective degrees of freedom of the combined denominator |

In compact form,

$$
\boxed{
\begin{aligned}
s_P^2&=\widehat V(P),
&k_P&=\frac{1}{n_P},
&\nu_P&=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)},\\[4pt]
s_Q^2&=\widehat V(Q),
&k_Q&=\frac{1}{n_Q},
&\nu_Q&=\frac{2n_Q\widehat V(Q)^2}{\widehat\tau^2(Q)}.
\end{aligned}
}
$$

These six quantities are the complete MI-specific input to the general
Welch-Satterthwaite equation.

## 9. Assumptions

The derivation uses:

- independent observations within each table;
- independence between the samples from $P$ and $Q$;
- fixed finite table dimensions;
- positive population support for the differentiability calculations;
- a nonzero first-order MI variance;
- first-order functional delta-method approximations for $\widehat I$ and
  $\widehat V$;
- a scaled chi-squared working model for each estimated variance component;
- a Student reference distribution after combining the components.

Widespread empirical support loss places the calculation outside the smooth
finite-sample regime represented by these approximations.

## References

- Wikipedia contributors. [Welch-Satterthwaite equation](https://en.wikipedia.org/wiki/Welch%E2%80%93Satterthwaite_equation).
- Satterthwaite, F. E. (1946). *An Approximate Distribution of Estimates of
  Variance Components*. Biometrics Bulletin, 2(6), 110-114.
  <https://doi.org/10.2307/3002019>.
- Welch, B. L. (1947). *The Generalization of Student's Problem When Several
  Different Population Variances Are Involved*. Biometrika, 34(1/2), 28-35.
  <https://doi.org/10.2307/2332510>.
- Hutcheson, K. (1970). *A Test for Comparing Diversities Based on the Shannon
  Formula*. Journal of Theoretical Biology, 29, 151-154.
  <https://doi.org/10.1016/0022-5193(70)90124-4>.
- von Davier, M. (2025). *An Improved Satterthwaite (1941, 1946) Effective df
  Approximation*. Journal of Educational and Behavioral Statistics.
  <https://doi.org/10.3102/10769986241309329>.
- von Davier, M. (2026). *A Corrected Welch Satterthwaite Equation*.
  <https://arxiv.org/abs/2602.20912>.
