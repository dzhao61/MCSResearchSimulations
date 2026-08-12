# Derivation of the Expanded Welch-Satterthwaite MI Test

## Purpose

This document derives the expanded Welch-Satterthwaite mutual-information
test directly from the general Welch-Satterthwaite equation. The general
equation combines independent estimated variances. To apply it to two mutual
information estimates, we must determine exactly what its variance estimates,
weights, and component degrees of freedom mean for two contingency tables.

For two independent variance estimates, the general equation is

$$
\nu
=
\frac{(k_Ps_P^2+k_Qs_Q^2)^2}
{(k_Ps_P^2)^2/\nu_P+(k_Qs_Q^2)^2/\nu_Q}.
$$

The derivation will calculate each input in the order in which it is needed:

1. The two tables give the estimated MI difference in the numerator of the
   test statistic.
2. The variability of pointwise mutual information and the sample sizes give
   the two variance contributions $k_Ps_P^2$ and $k_Qs_Q^2$.
3. The sampling variability of the two estimated MI variances gives the
   component degrees of freedom $\nu_P$ and $\nu_Q$.
4. These quantities determine the Student degrees of freedom and the final
   p-value.

Each section completes one of these calculations before the next calculation
begins. Population quantities are written without a hat, and quantities
calculated from observed tables are written with a hat.

Natural logarithms are used throughout, so mutual information is measured in
nats.

## 1. Estimate the Difference in Mutual Information

The numerator of the final test statistic is

$$
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q).
$$

It is obtained from the plug-in estimates $\widehat I(P)$ and
$\widehat I(Q)$ after correcting their leading biases.

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

The second table gives $\widehat I(Q)$ by the same calculation with its
empirical probabilities $\widehat q_{ij}$. Zero-probability terms contribute
zero under the convention $0\log 0=0$.

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

## 2. State the Welch-Satterthwaite Equation We Need to Complete

The general construction follows the
[Welch-Satterthwaite equation](https://en.wikipedia.org/wiki/Welch%E2%80%93Satterthwaite_equation).
Suppose $s_1^2,\ldots,s_m^2$ are independent estimated variances. The $i$th
variance is multiplied by a positive weight $k_i$ and has component degrees
of freedom $\nu_i$. Their weighted sum is

$$
\chi'=\sum_{i=1}^m k_i s_i^2.
$$

Welch-Satterthwaite approximates the sampling distribution of this sum by one
scaled chi-squared distribution. Its effective degrees of freedom are

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

For the present problem, the squared standard error of the MI difference has
one contribution from population $P$ and one from population $Q$. There are
therefore two terms, so the equation becomes

$$
\boxed{
\nu_{\mathrm{expanded}}
=
\frac{(k_Ps_P^2+k_Qs_Q^2)^2}
{(k_Ps_P^2)^2/\nu_P+(k_Qs_Q^2)^2/\nu_Q}.
}
$$

Evaluating this expression requires the variance estimates $s_P^2$ and
$s_Q^2$, their weights $k_P$ and $k_Q$, and their component degrees of
freedom $\nu_P$ and $\nu_Q$.

## 3. Calculate the Variance Contributions and Weights

Population $P$ contributes the term $k_Ps_P^2$ to the squared standard
error. We will show that

$$
\boxed{
k_Ps_P^2
=\widehat{\operatorname{Var}}\{\widehat I(P)\}
=\frac{\widehat V(P)}{n_P},
}
$$

where $\widehat V(P)$ estimates the variance of the pointwise mutual
information values and $n_P$ is the sample size.

### 3.1 Calculate the variance of pointwise mutual information

For a random observation $(X,Y)\sim P$, the pointwise mutual information is
$\ell_P(X,Y)$. Its first moment is

$$
\begin{aligned}
\operatorname E_P\{\ell_P(X,Y)\}
&=\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=I(P),
\end{aligned}
$$

and its second moment is

$$
\operatorname E_P\{\ell_P(X,Y)^2\}
=\sum_{i,j}p_{ij}\ell_P(i,j)^2.
$$

Therefore,

$$
\begin{aligned}
V(P)
&=\operatorname{Var}_P\{\ell_P(X,Y)\}\\
&=\operatorname E_P\{\ell_P(X,Y)^2\}
-\left[\operatorname E_P\{\ell_P(X,Y)\}\right]^2\\
&=\sum_{i,j}p_{ij}\ell_P(i,j)^2-I(P)^2\\
&=\sum_{i,j}p_{ij}\ell_P(i,j)^2
-2I(P)\sum_{i,j}p_{ij}\ell_P(i,j)
+I(P)^2\sum_{i,j}p_{ij}\\
&=\sum_{i,j}p_{ij}
\left\{\ell_P(i,j)^2-2I(P)\ell_P(i,j)+I(P)^2\right\}\\
&=\boxed{
\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2
}.
\end{aligned}
$$

### 3.2 Calculate the sampling variance of $\widehat I(P)$

The target is

$$
\operatorname{Var}\{\widehat I(P)\}
=\operatorname{Var}\{\widehat I(P)-I(P)\},
$$

because $I(P)$ is a fixed population value. We first express the estimation
error $\widehat I(P)-I(P)$ in terms of the cell-probability errors. Write MI
as

$$
I(P)
=\sum_{i,j}p_{ij}\log p_{ij}
-\sum_i p_{i+}\log p_{i+}
-\sum_j p_{+j}\log p_{+j}.
$$

Using $(u\log u)'=\log u+1$, the first-order Taylor expansion of the three
sums is

$$
\begin{aligned}
\widehat I(P)-I(P)
&\approx
\sum_{i,j}(\log p_{ij}+1)(\widehat p_{ij}-p_{ij})\\
&\quad-\sum_i(\log p_{i+}+1)(\widehat p_{i+}-p_{i+})\\
&\quad-\sum_j(\log p_{+j}+1)(\widehat p_{+j}-p_{+j}).
\end{aligned}
$$

The row- and column-margin errors are sums of the cell errors:

$$
\widehat p_{i+}-p_{i+}
=\sum_j(\widehat p_{ij}-p_{ij}),
\qquad
\widehat p_{+j}-p_{+j}
=\sum_i(\widehat p_{ij}-p_{ij}).
$$

Substituting these margin errors and collecting the coefficient of each
$\widehat p_{ij}-p_{ij}$ gives

$$
\begin{aligned}
\widehat I(P)-I(P)
&\approx\sum_{i,j}
\left\{
(\log p_{ij}+1)
-(\log p_{i+}+1)
-(\log p_{+j}+1)
\right\}
(\widehat p_{ij}-p_{ij})\\
&=\sum_{i,j}\{\ell_P(i,j)-1\}
(\widehat p_{ij}-p_{ij}).
\end{aligned}
$$

Both probability tables sum to one, so

$$
\sum_{i,j}\{\widehat p_{ij}-p_{ij}\}=1-1=0.
$$

The constant $-1$ therefore contributes zero, leaving

$$
\widehat I(P)-I(P)
\approx\sum_{i,j}\ell_P(i,j)(\widehat p_{ij}-p_{ij}).
$$

Each empirical cell probability is a sample average, so

$$
\widehat p_{ij}-p_{ij}
=\frac{1}{n_P}\sum_{a=1}^{n_P}
\left[\mathbf 1\{Z_a^{(P)}=(i,j)\}-p_{ij}\right].
$$

Substituting this expression gives

$$
\begin{aligned}
\widehat I(P)-I(P)
&\approx\sum_{i,j}\ell_P(i,j)
\left\{
\frac{1}{n_P}\sum_{a=1}^{n_P}
[\mathbf 1\{Z_a^{(P)}=(i,j)\}-p_{ij}]
\right\}\\
&=\frac{1}{n_P}\sum_{a=1}^{n_P}
\left\{
\sum_{i,j}\ell_P(i,j)\mathbf 1\{Z_a^{(P)}=(i,j)\}
-\sum_{i,j}p_{ij}\ell_P(i,j)
\right\}\\
&=\frac{1}{n_P}\sum_{a=1}^{n_P}
\{\ell_P(Z_a^{(P)})-I(P)\}.
\end{aligned}
$$

The observations are independent, and each centred PMI value has variance
$V(P)$. Thus

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)\}
&\approx
\operatorname{Var}\left[
\frac{1}{n_P}\sum_{a=1}^{n_P}
\{\ell_P(Z_a^{(P)})-I(P)\}
\right]\\
&=\frac{1}{n_P^2}
\sum_{a=1}^{n_P}
\operatorname{Var}_P\{\ell_P(Z_a^{(P)})-I(P)\}\\
&=\frac{1}{n_P^2}
\sum_{a=1}^{n_P}
\operatorname{Var}_P\{\ell_P(Z_a^{(P)})\}\\
&=\frac{1}{n_P^2}
\sum_{a=1}^{n_P}V(P)\\
&=\frac{1}{n_P^2}\,n_PV(P)\\
&=\boxed{\frac{V(P)}{n_P}}.
\end{aligned}
$$

### 3.3 Estimate the variance and identify $s_P^2$ and $k_P$

The observed table estimates $V(P)$ by

$$
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2.
$$

The estimated sampling variance is therefore

$$
\widehat{\operatorname{Var}}\{\widehat I(P)\}
=\frac{\widehat V(P)}{n_P}.
$$

Comparing this with the generic component $k_Ps_P^2$ gives

$$
\boxed{s_P^2=\widehat V(P),}
\qquad
\boxed{k_P=\frac{1}{n_P},}
$$

and therefore

$$
\boxed{
k_Ps_P^2
=\widehat{\operatorname{Var}}\{\widehat I(P)\}
=\frac{\widehat V(P)}{n_P}.
}
$$

### 3.4 Combine the two variance contributions

The same calculation for the second population gives

$$
k_Qs_Q^2=\frac{\widehat V(Q)}{n_Q}.
$$

Because the two samples are independent,

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)-\widehat I(Q)\}
&=\operatorname{Var}\{\widehat I(P)\}
+\operatorname{Var}\{\widehat I(Q)\}\\
&\approx\frac{V(P)}{n_P}+\frac{V(Q)}{n_Q}.
\end{aligned}
$$

The squared standard error is consequently

$$
\boxed{
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
}
$$

The Welch-Satterthwaite equation becomes

$$
\boxed{
\nu_{\mathrm{expanded}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\nu_P
+\left\{\widehat V(Q)/n_Q\right\}^2/\nu_Q
}.
}
$$

## 4. Derive the Component Degrees of Freedom $\nu_P$ and $\nu_Q$

Section 3 produced the estimated squared standard error

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}.
$$

Because $\widehat V(P)$ and $\widehat V(Q)$ are estimated from data, their
sampling uncertainty must be reflected in the Student reference
distribution. The component degrees of freedom $\nu_P$ and $\nu_Q$ provide
that adjustment. We derive $\nu_P$ first; the same calculation then gives
$\nu_Q$.

The derivation has four stages:

1. Use Satterthwaite moment matching to identify which properties of
   $\widehat V(P)$ determine $\nu_P$.
2. Derive how one observation in cell $(x,y)$ changes $V(P)$. This
   observation-level change is denoted by $g_P(x,y)$.
3. Use the variability of $g_P(X,Y)$ to obtain the sampling variance of
   $\widehat V(P)$ and hence $\nu_P$.
4. Estimate the required quantities from the two observed tables and combine
   $\nu_P$ and $\nu_Q$ in the Welch-Satterthwaite equation.

### 4.1 Express $\nu_P$ using the moments of $\widehat V(P)$

The first step is to express $\nu_P$ in terms of the mean and sampling
variance of $\widehat V(P)$. Satterthwaite approximates this positive variance
estimate by the scaled chi-squared model

$$
\widehat V(P)
\quad\text{is modelled by}\quad
\frac{\operatorname E\{\widehat V(P)\}}{\nu_P}
\chi^2_{\nu_P}.
$$

A variance estimate is nonnegative, and ordinary sample variances have exact
scaled chi-squared distributions under normal sampling. Satterthwaite uses
the same family as a working approximation for a more general variance
estimate.

For a chi-squared variable with $\nu_P$ degrees of freedom,

$$
\operatorname E\{\chi^2_{\nu_P}\}=\nu_P,
\qquad
\operatorname{Var}\{\chi^2_{\nu_P}\}=2\nu_P.
$$

The scale factor is chosen so that the model has the same mean as
$\widehat V(P)$:

$$
\operatorname E\left\{
\frac{\operatorname E\{\widehat V(P)\}}{\nu_P}
\chi^2_{\nu_P}
\right\}
=\frac{\operatorname E\{\widehat V(P)\}}{\nu_P}\nu_P
=\operatorname E\{\widehat V(P)\}.
$$

Its variance is

$$
\begin{aligned}
\operatorname{Var}\left\{
\frac{\operatorname E\{\widehat V(P)\}}{\nu_P}
\chi^2_{\nu_P}
\right\}
&=\frac{\left[\operatorname E\{\widehat V(P)\}\right]^2}
{\nu_P^2}
2\nu_P\\
&=\frac{2\left[\operatorname E\{\widehat V(P)\}\right]^2}
{\nu_P}.
\end{aligned}
$$

The means already agree. Equating the model variance to the sampling variance
of $\widehat V(P)$ gives

$$
\frac{2\left[\operatorname E\{\widehat V(P)\}\right]^2}
{\nu_P}
=\operatorname{Var}\{\widehat V(P)\},
$$

and hence

$$
\nu_P
=\frac{
2\left[\operatorname E\{\widehat V(P)\}\right]^2
}{
\operatorname{Var}\{\widehat V(P)\}
}.
$$

The first-order mean is $\operatorname E\{\widehat V(P)\}\approx V(P)$.
The remaining quantity required by this equation is therefore
$\operatorname{Var}\{\widehat V(P)\}$.

### 4.2 Plan the calculation of $\operatorname{Var}\{\widehat V(P)\}$

The target is

$$
\operatorname{Var}\{\widehat V(P)\}
=\operatorname{Var}\{\widehat V(P)-V(P)\},
$$

because $V(P)$ is a fixed population quantity. To first order, this estimation
error is an average of the effects of individual observations. The next
subsections derive one such effect and then calculate its variance.

### 4.3 Represent the effect of one observation on the table

An observation affects $\widehat V(P)$ by changing the empirical cell
probabilities. To represent the corresponding population-level change for an
observation in cell $(x,y)$, define the perturbation

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

This shifts an $\varepsilon$-fraction of the probability toward cell $(x,y)$;
$\varepsilon=0$ gives the original distribution. Define the resulting
first-order change in $V(P)$ by

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Calculating $g_P(x,y)$ requires the resulting changes in the cell
probabilities, PMI values, and MI. This subsection supplies the probability
changes. For any cell $(i,j)$,

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

Differentiating the joint probability and its margins at $\varepsilon=0$
gives

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
&=\mathbf 1\{i=x,j=y\}-p_{ij},\\
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{i+}(\varepsilon)
\right|_{\varepsilon=0}
&=\mathbf 1\{i=x\}-p_{i+},\\
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
&=\mathbf 1\{j=y\}-p_{+j}.
\end{aligned}
$$

### 4.4 Calculate the resulting change in each PMI value

The PMI derivative is needed because every term in $V(P)$ contains a PMI
value. The PMI in cell $(i,j)$ along the perturbation is

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon),
$$

so applying $\mathrm d(\log u)/\mathrm d\varepsilon=u'/u$ gives

$$
\begin{aligned}
\ell'_P(i,j;x,y)
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}\\
&=\frac{\mathbf 1\{i=x,j=y\}-p_{ij}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}-p_{i+}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}-p_{+j}}{p_{+j}}\\
&=\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
\end{aligned}
$$

### 4.5 Calculate the resulting change in MI

The MI derivative is needed because $I(P)$ is the mean PMI and therefore
appears in $V(P)$. Along the same path, MI is

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)\log p_{ij}(\varepsilon)
-\sum_i p_{i+}(\varepsilon)\log p_{i+}(\varepsilon)
-\sum_j p_{+j}(\varepsilon)\log p_{+j}(\varepsilon).
$$

Differentiating the three sums using $(u\log u)'=\log u+1$ gives

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}(\log p_{ij}+1)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}\\
&\quad-\sum_i(\log p_{i+}+1)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{i+}(\varepsilon)
\right|_{\varepsilon=0}\\
&\quad-\sum_j(\log p_{+j}+1)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Each marginal change is the sum of its corresponding cell changes. Rewriting
all three terms as sums over cells and collecting their coefficients gives

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}
\{(\log p_{ij}+1)-(\log p_{i+}+1)-(\log p_{+j}+1)\}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}\\
&=\sum_{i,j}
\{\ell_P(i,j)-1\}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Since $\sum_{i,j}p_{ij}(\varepsilon)=1$,

$$
\sum_{i,j}\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
=\frac{\mathrm d}{\mathrm d\varepsilon}
\sum_{i,j}p_{ij}(\varepsilon)
=\frac{\mathrm d}{\mathrm d\varepsilon}1
=0.
$$

The constant $-1$ therefore drops out. Substituting the cell-probability
derivative gives

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}\ell_P(i,j)
\left.\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}\\
&=\sum_{i,j}\ell_P(i,j)
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\\
&=\ell_P(x,y)-\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\boxed{\ell_P(x,y)-I(P)}.
\end{aligned}
$$

### 4.6 Rewrite $V(P)$ in a form that can be differentiated

Along the perturbation,

$$
V(P_\varepsilon)=M_2(P_\varepsilon)-I(P_\varepsilon)^2,
$$

where

$$
M_2(P_\varepsilon)
=\operatorname E_{P_\varepsilon}
\{\ell_{P_\varepsilon}(X,Y)^2\}
=\sum_{i,j}p_{ij}(\varepsilon)\ell_{P_\varepsilon}(i,j)^2.
$$

We now differentiate the variance identity along the perturbation, which we
define as $g_P(x,y)$:

$$
\begin{aligned}
g_P(x,y)
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}\\
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\{M_2(P_\varepsilon)-I(P_\varepsilon)^2\}
\right|_{\varepsilon=0}\\
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)^2
\right|_{\varepsilon=0}\\
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Section 4.5 calculated
$\left.\mathrm d I(P_\varepsilon)/\mathrm d\varepsilon\right|_{\varepsilon=0}$,
so the only remaining quantity is
$\left.\mathrm d M_2(P_\varepsilon)/\mathrm d\varepsilon\right|_{\varepsilon=0}$.

### 4.7 Calculate the change in the second PMI moment

Applying the product rule gives

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\ell_P(i,j)^2\\
&\quad+2\sum_{i,j}p_{ij}\ell_P(i,j)
\ell'_P(i,j;x,y).
\end{aligned}
$$

The first sum comes from the changing probability weights:

$$
\begin{aligned}
\sum_{i,j}
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\ell_P(i,j)^2
&=\ell_P(x,y)^2
-\sum_{i,j}p_{ij}\ell_P(i,j)^2\\
&=\ell_P(x,y)^2-M_2(P).
\end{aligned}
$$

The second sum comes from the changing PMI values. Inserting the PMI
derivative gives

$$
\begin{aligned}
&\sum_{i,j}p_{ij}\ell_P(i,j)\ell'_P(i,j;x,y)\\
&\quad=\sum_{i,j}p_{ij}\ell_P(i,j)
\left\{
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1
\right\}\\
&\quad=\ell_P(x,y)
-\frac{\sum_jp_{xj}\ell_P(x,j)}{p_{x+}}
-\frac{\sum_ip_{iy}\ell_P(i,y)}{p_{+y}}
+\sum_{i,j}p_{ij}\ell_P(i,j)\\
&\quad=\ell_P(x,y)
-\operatorname E_P\{\ell_P(X,Y)\mid X=x\}
-\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}
+I(P).
\end{aligned}
$$

Combining the two product-rule terms gives

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
&=\ell_P(x,y)^2-M_2(P)\\
&\quad+2\bigl[\ell_P(x,y)
-\operatorname E_P\{\ell_P(X,Y)\mid X=x\}\\
&\qquad-\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}+I(P)\bigr].
\end{aligned}
$$

### 4.8 Combine the two changes to obtain $g_P(x,y)$

From Section 4.6,

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
-2I(P)\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Substituting the two derivatives in this order gives

$$
\begin{aligned}
g_P(x,y)
&=\ell_P(x,y)^2-M_2(P)\\
&\quad+2\ell_P(x,y)+2I(P)\\
&\quad-2\operatorname E_P\{\ell_P(X,Y)\mid X=x\}\\
&\quad-2\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}\\
&\quad-2I(P)\{\ell_P(x,y)-I(P)\}.
\end{aligned}
$$

The first and final lines simplify as

$$
\begin{aligned}
&\ell_P(x,y)^2-M_2(P)
-2I(P)\{\ell_P(x,y)-I(P)\}\\
&\qquad=\{\ell_P(x,y)-I(P)\}^2
-\{M_2(P)-I(P)^2\}\\
&\qquad=\{\ell_P(x,y)-I(P)\}^2-V(P).
\end{aligned}
$$

Therefore,

$$
\boxed{
\begin{aligned}
g_P(x,y)
&=\{\ell_P(x,y)-I(P)\}^2-V(P)\\
&\quad+2\ell_P(x,y)+2I(P)\\
&\quad-2\operatorname E_P\{\ell_P(X,Y)\mid X=x\}\\
&\quad-2\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}.
\end{aligned}
}
$$

### 4.9 Calculate the variability of the one-observation effect

Define the variance of these observation-level effects by

$$
\boxed{
\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}.
}
$$

Thus $\tau^2(P)$ measures the variability of the observation-level changes
in $V(P)$.

To calculate it, use

$$
\tau^2(P)
=\operatorname E_P\{g_P(X,Y)^2\}
-\left[\operatorname E_P\{g_P(X,Y)\}\right]^2.
$$

We first calculate $\operatorname E_P\{g_P(X,Y)\}$ by taking the expectation
of each of the four lines in $g_P(X,Y)$.

The expectation of the first line is

$$
\begin{aligned}
&\operatorname E_P\left[
\{\ell_P(X,Y)-I(P)\}^2-V(P)
\right]\\
&\qquad=\operatorname E_P\left[
\{\ell_P(X,Y)-I(P)\}^2
\right]-V(P)\\
&\qquad=\operatorname{Var}_P\{\ell_P(X,Y)\}-V(P)\\
&\qquad=V(P)-V(P)\\
&\qquad=0.
\end{aligned}
$$

The expectation of the second line is

$$
\begin{aligned}
\operatorname E_P\{2\ell_P(X,Y)+2I(P)\}
&=2I(P)+2I(P)\\
&=4I(P).
\end{aligned}
$$

The expectation of the third line is

$$
\begin{aligned}
&\operatorname E_P\left[
-2\operatorname E_P\{\ell_P(X,Y)\mid X\}
\right]\\
&\qquad=-2\operatorname E_P\{\ell_P(X,Y)\}\\
&\qquad=-2I(P).
\end{aligned}
$$

The expectation of the fourth line is

$$
\begin{aligned}
&\operatorname E_P\left[
-2\operatorname E_P\{\ell_P(X,Y)\mid Y\}
\right]\\
&\qquad=-2\operatorname E_P\{\ell_P(X,Y)\}\\
&\qquad=-2I(P).
\end{aligned}
$$

Adding the four expectations gives

$$
\operatorname E_P\{g_P(X,Y)\}
=0+4I(P)-2I(P)-2I(P)
=0.
$$

Therefore,

$$
\begin{aligned}
\tau^2(P)
&=\operatorname E_P\{g_P(X,Y)^2\}\\
&=\sum_{i,j}p_{ij}g_P(i,j)^2.
\end{aligned}
$$

### 4.10 Calculate the sampling variance of $\widehat V(P)$

The target is

$$
\operatorname{Var}\{\widehat V(P)\}
=\operatorname{Var}\{\widehat V(P)-V(P)\},
$$

because $V(P)$ is a fixed population value. We first express the estimation
error using a first-order Taylor expansion of $V$ over the cell
probabilities:

$$
\widehat V(P)-V(P)
\approx\sum_{i,j}g_P(i,j)(\widehat p_{ij}-p_{ij}).
$$

This retains only terms that are linear in the cell-probability errors.

Each empirical cell probability is a sample average. Substituting

$$
\widehat p_{ij}-p_{ij}
=\frac{1}{n_P}\sum_{a=1}^{n_P}
\left[\mathbf 1\{Z_a^{(P)}=(i,j)\}-p_{ij}\right]
$$

into the Taylor expansion gives

$$
\begin{aligned}
\widehat V(P)-V(P)
&\approx\frac{1}{n_P}\sum_{a=1}^{n_P}
\left[g_P(Z_a^{(P)})-\operatorname E_P\{g_P(X,Y)\}\right]\\
&=\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)})
-\frac{1}{n_P}\sum_{a=1}^{n_P}\operatorname E_P\{g_P(X,Y)\}\\
&=\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)})
-\operatorname E_P\{g_P(X,Y)\}\\
&=\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)}),
\end{aligned}
$$

where the final equality uses $\operatorname E_P\{g_P(X,Y)\}=0$ from Section
4.9.

The observations are independent, and each $g_P(Z_a^{(P)})$ has variance
$\tau^2(P)$. Thus

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\sum_{a=1}^{n_P}\operatorname{Var}_P\{g_P(Z_a^{(P)})\}\\
&=\frac{1}{n_P^2}\sum_{a=1}^{n_P}\tau^2(P)\\
&=\frac{1}{n_P^2}\,n_P\tau^2(P)\\
&=\boxed{\frac{\tau^2(P)}{n_P}}.
\end{aligned}
$$

This supplies the sampling variance required by the Satterthwaite equation
in Section 4.1.

### 4.11 Obtain the component degrees of freedom $\nu_P$

The first-order mean and sampling variance of the variance estimate are now

$$
\operatorname E\{\widehat V(P)\}\approx V(P),
\qquad
\operatorname{Var}\{\widehat V(P)\}
\approx\frac{\tau^2(P)}{n_P}.
$$

Substituting these moments into the Satterthwaite equation from Section 4.1
gives

$$
\begin{aligned}
\nu_P
&=\frac{
2\left[\operatorname E\{\widehat V(P)\}\right]^2
}{
\operatorname{Var}\{\widehat V(P)\}
}\\
&\approx\frac{2V(P)^2}{\tau^2(P)/n_P}\\
&=\boxed{\frac{2n_PV(P)^2}{\tau^2(P)}}.
\end{aligned}
$$

Thus $\nu_P$ is large when $\widehat V(P)$ has little sampling variation
relative to its squared size, and small when the estimated variance is
unstable between samples.

### 4.12 Calculate the component degrees of freedom from the table

For table $P$, substitute each table estimate into $\widehat\nu_P$ one step
at a time:

$$
\begin{aligned}
\widehat\nu_P
&=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}\\[4pt]
&=\frac{2n_P\widehat V(P)^2}
{\displaystyle\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2}\\[6pt]
&=\frac{2n_P\widehat V(P)^2}
{\displaystyle\sum_{i,j}\widehat p_{ij}
\left\{\widehat g_P(i,j)
-\sum_{a,b}\widehat p_{ab}\widehat g_P(a,b)\right\}^2}\\[6pt]
&=\boxed{
\frac{
2n_P\left[
\displaystyle\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2
\right]^2
}{
\displaystyle\sum_{i,j}\widehat p_{ij}
\left\{\widehat g_P(i,j)
-\sum_{a,b}\widehat p_{ab}\widehat g_P(a,b)\right\}^2
}
}.
\end{aligned}
$$

The remaining cell value in the final line is calculated entirely from the
same table:

$$
\boxed{
\begin{aligned}
\widehat g_P(i,j)
&=\{\widehat\ell_P(i,j)-\widehat I(P)\}^2
-\sum_{a,b}\widehat p_{ab}
\{\widehat\ell_P(a,b)-\widehat I(P)\}^2\\
&\quad+2\widehat\ell_P(i,j)+2\widehat I(P)\\
&\quad-2\frac{\sum_b\widehat p_{ib}\widehat\ell_P(i,b)}
{\widehat p_{i+}}\\
&\quad-2\frac{\sum_a\widehat p_{aj}\widehat\ell_P(a,j)}
{\widehat p_{+j}}.
\end{aligned}
}
$$

Apply the same substitutions to table $Q$ to obtain

$$
\boxed{
\widehat\nu_Q
=\frac{2n_Q\widehat V(Q)^2}{\widehat\tau^2(Q)}.
}
$$

### 4.13 Combine the two component degrees of freedom

The estimated squared standard error contains the independent components
$\widehat V(P)/n_P$ and $\widehat V(Q)/n_Q$. The Welch-Satterthwaite equation
combines their component degrees of freedom as

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_P
+\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_Q
}.
}
$$

## 5. Complete the Test

Dividing the estimated MI difference by its estimated standard error gives

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

The numerator is asymptotically normal. The denominator is an estimated
standard deviation whose two variance components have been represented by
scaled chi-squared distributions and combined through the
Welch-Satterthwaite equation. This normal-over-estimated-variance structure
leads to a Student reference distribution.

Expanded Welch therefore compares $T$ with a Student distribution having
$\widehat\nu_{\mathrm{expanded}}$ degrees of freedom. The two-sided p-value is

$$
\boxed{
p_{\mathrm{expanded}}
=2\left[
1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)
\right].
}
$$

## 6. Summary of the Derived Inputs

The complete connection between the general equation and the MI test is

| General input | MI definition | How it is obtained |
| --- | --- | --- |
| $s_P^2$ | $\widehat V(P)$ | Probability-weighted variance of empirical PMI values |
| $s_Q^2$ | $\widehat V(Q)$ | Same calculation for population $Q$ |
| $k_P$ | $1/n_P$ | Variance of a sample mean is observation-level variance divided by sample size |
| $k_Q$ | $1/n_Q$ | Same calculation for population $Q$ |
| $\nu_P$ | $\widehat\nu_P=2n_P\widehat V(P)^2/\widehat\tau^2(P)$ | Satterthwaite moment matching for $\widehat V(P)$ |
| $\nu_Q$ | $\widehat\nu_Q=2n_Q\widehat V(Q)^2/\widehat\tau^2(Q)$ | Same calculation for population $Q$ |
| $\chi'$ | $\widehat V(P)/n_P+\widehat V(Q)/n_Q$ | Estimated sampling variance of the MI difference |
| $\nu_{\chi'}$ | $\widehat\nu_{\mathrm{expanded}}$ | Effective degrees of freedom of the combined denominator |

In compact form,

$$
\boxed{
\begin{aligned}
s_P^2&=\widehat V(P),
&k_P&=\frac{1}{n_P},
&\widehat\nu_P&=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)},\\[4pt]
s_Q^2&=\widehat V(Q),
&k_Q&=\frac{1}{n_Q},
&\widehat\nu_Q&=\frac{2n_Q\widehat V(Q)^2}{\widehat\tau^2(Q)}.
\end{aligned}
}
$$

These six quantities are the complete MI-specific input to the general
Welch-Satterthwaite equation.

## 7. Assumptions

The derivation uses:

- independent observations within each table;
- independence between the samples from $P$ and $Q$;
- fixed finite table dimensions;
- positive population support for the differentiability calculations;
- a nonzero first-order MI variance;
- first-order Taylor approximations for the distribution-dependent quantities
  $\widehat I$ and $\widehat V$;
- a scaled chi-squared working model for each estimated variance component;
- a Student reference distribution after combining the components.

Widespread empirical support loss places the calculation outside the smooth
finite-sample regime represented by these approximations.

## Appendix A. Optional Bias-Corrected Combination Formula

A proposed fourth-moment correction changes only the final rule for combining
the two variance components; it does not change $\widehat V(P)$,
$\widehat\tau^2(P)$, $\widehat\nu_P$, or any corresponding quantity for $Q$.
The corrected general formula is

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
\{\widehat\nu_P+2\}
+\left\{\widehat V(Q)/n_Q\right\}^2/
\{\widehat\nu_Q+2\}
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
