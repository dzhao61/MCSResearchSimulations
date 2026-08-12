# An Alternative Derivation of the Expanded Welch-Satterthwaite MI Test

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

The only quantities still missing from the Welch-Satterthwaite equation are
$\nu_P$ and $\nu_Q$. We derive $\nu_P$ from the sampling distribution of
$\widehat V(P)$; the same calculation gives $\nu_Q$.

### 4.1 State the moment-matching target

Satterthwaite approximates the positive variance estimate $\widehat V(P)$ by
the scaled chi-squared model

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
The remaining task is to calculate
$\operatorname{Var}\{\widehat V(P)\}$ by determining how one observation
changes $V(P)$.

### 4.2 Calculate how one observation changes PMI and MI

For an observation in cell $(x,y)$, define

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

For an arbitrary cell $(i,j)$,

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

The changes in the joint and marginal probabilities at the original
distribution are

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x,j=y\}-p_{ij},
$$

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{i+}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x\}-p_{i+},
$$

and

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

Along this path,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon),
$$

so

$$
\begin{aligned}
\ell'_P(i,j;x,y)
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}\\
&=\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
\end{aligned}
$$

The Taylor expansion in Section 3.2 gives the corresponding first-order
change in MI:

$$
\boxed{
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P).
}
$$

### 4.3 Calculate how one observation changes $V(P)$

To differentiate the PMI variance, write it in terms of the first and second
PMI moments. The first moment is $I(P)$; define the second moment by

$$
M_2(P)
=\operatorname E_P\{\ell_P(X,Y)^2\}
=\sum_{i,j}p_{ij}\ell_P(i,j)^2.
$$

Expanding the variance of PMI gives

$$
\begin{aligned}
V(P)
&=\operatorname E_P\left[
\{\ell_P(X,Y)-I(P)\}^2
\right]\\
&=\operatorname E_P\{\ell_P(X,Y)^2\}
-2I(P)\operatorname E_P\{\ell_P(X,Y)\}
+I(P)^2\\
&=M_2(P)-2I(P)^2+I(P)^2\\
&=\boxed{M_2(P)-I(P)^2}.
\end{aligned}
$$

The derivative of $V(P)$ therefore requires the derivatives of $M_2(P)$ and
$I(P)$. Section 4.2 supplied the derivative of $I(P)$, so we next calculate
the derivative of $M_2(P)$.

Along the cell perturbation,

$$
M_2(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j)^2.
$$

Both factors depend on $\varepsilon$. Applying the product rule and
$\mathrm d(\ell^2)/\mathrm d\varepsilon=2\ell\ell'$ gives

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

The first sum changes only the probability weights:

$$
\begin{aligned}
\sum_{i,j}
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\ell_P(i,j)^2
&=\ell_P(x,y)^2
-\sum_{i,j}p_{ij}\ell_P(i,j)^2\\
&=\ell_P(x,y)^2-M_2(P).
\end{aligned}
$$

To evaluate the second sum, define the probability-weighted mean PMI in row
$x$ and column $y$:

$$
R_P(x)
=\frac{\sum_jp_{xj}\ell_P(x,j)}{p_{x+}},
$$

$$
C_P(y)
=\frac{\sum_ip_{iy}\ell_P(i,y)}{p_{+y}}.
$$

Inserting the PMI derivative gives

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
&\quad=\ell_P(x,y)-R_P(x)-C_P(y)+I(P).
\end{aligned}
$$

Combining the two sums gives

$$
\boxed{
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}
&=\ell_P(x,y)^2-M_2(P)\\
&\quad+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}.
\end{aligned}
}
$$

With both required derivatives available, define the first-order effect of
cell $(x,y)$ on the complete MI variance by

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Since $V(P)=M_2(P)-I(P)^2$, the chain rule gives

$$
\begin{aligned}
g_P(x,y)
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}\\
&\quad-2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Inserting the derivatives of $M_2(P)$ and $I(P)$ gives

$$
\begin{aligned}
g_P(x,y)
&=\ell_P(x,y)^2-M_2(P)\\
&\quad+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}\\
&\quad-2I(P)\{\ell_P(x,y)-I(P)\}.
\end{aligned}
$$

The terms in the first and third lines simplify as

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
&\quad+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}.
\end{aligned}
}
$$

### 4.4 Calculate the sampling variance of $\widehat V(P)$ and obtain $\nu_P$

The population mean of $g_P(X,Y)$ is zero. For the first line of $g_P$,

$$
\operatorname E_P\left[
\{\ell_P(X,Y)-I(P)\}^2-V(P)
\right]
=V(P)-V(P)=0.
$$

For the second line,

$$
\begin{aligned}
&\operatorname E_P\{\ell_P(X,Y)-R_P(X)-C_P(Y)+I(P)\}\\
&\qquad=I(P)-I(P)-I(P)+I(P)\\
&\qquad=0.
\end{aligned}
$$

Define the variance of these observation-level effects by

$$
\boxed{
\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}.
}
$$

The first-order error of $\widehat V(P)$ is the average of the $g_P$ values:

$$
\widehat V(P)-V(P)
\approx
\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)}).
$$

The observations are independent and each term has variance $\tau^2(P)$.
Hence

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{a=1}^{n_P}g_P(Z_a^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\sum_{a=1}^{n_P}\operatorname{Var}_P\{g_P(Z_a^{(P)})\}\\
&=\frac{1}{n_P^2}\,n_P\tau^2(P)\\
&=\boxed{\frac{\tau^2(P)}{n_P}}.
\end{aligned}
$$

We now have the two moments needed to describe the sampling distribution of
the variance estimate:

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

### 4.5 Estimate the component degrees of freedom and combine them

The population quantities in the preceding formula are unknown. Calculate
their empirical versions directly from the observed table:

$$
\widehat R_P(i)
=\frac{\sum_j\widehat p_{ij}\widehat\ell_P(i,j)}
{\widehat p_{i+}},
$$

$$
\widehat C_P(j)
=\frac{\sum_i\widehat p_{ij}\widehat\ell_P(i,j)}
{\widehat p_{+j}},
$$

$$
\begin{aligned}
\widehat g_P(i,j)
&=\{\widehat\ell_P(i,j)-\widehat I(P)\}^2-\widehat V(P)\\
&\quad+2\{\widehat\ell_P(i,j)-\widehat R_P(i)
-\widehat C_P(j)+\widehat I(P)\}.
\end{aligned}
$$

Centre the empirical $\widehat g_P$ values and calculate their
probability-weighted variance:

$$
\overline g_P
=\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j),
$$

$$
\widehat\tau^2(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2.
$$

Replacing $V(P)$ and $\tau^2(P)$ by $\widehat V(P)$ and
$\widehat\tau^2(P)$ gives the observed component degrees of freedom

$$
\boxed{
\widehat\nu_P
=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
}
$$

The same calculation for the second table gives

$$
\boxed{
\widehat\nu_Q
=\frac{2n_Q\widehat V(Q)^2}{\widehat\tau^2(Q)}.
}
$$

Combining the two component degrees of freedom gives

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
