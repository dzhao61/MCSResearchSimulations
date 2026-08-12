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
2. The variability of pointwise mutual information within each population
   gives $s_P^2$ and $s_Q^2$.
3. Averaging over $n_P$ and $n_Q$ observations gives the weights $k_P$ and
   $k_Q$.
4. The sampling variability of the two estimated MI variances gives the
   component degrees of freedom $\nu_P$ and $\nu_Q$.
5. These quantities determine the Student degrees of freedom and the final
   p-value.

Each section completes one of these calculations before the next calculation
begins. Population quantities are written without a hat, and quantities
calculated from observed tables are written with a hat.

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

For the second table, define

$$
\widehat q_{ij}=\frac{N_{ij}^{(Q)}}{n_Q},
\qquad
\widehat\ell_Q(i,j)
=\log\left(
\frac{\widehat q_{ij}}
{\widehat q_{i+}\widehat q_{+j}}
\right),
$$

and calculate

$$
\widehat I(Q)
=\sum_{i,j}\widehat q_{ij}\widehat\ell_Q(i,j).
$$

Terms with $\widehat p_{ij}=0$ contribute zero under the convention
$0\log 0=0$; the same convention applies to $\widehat q_{ij}=0$.

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

This is the equation that the rest of the derivation will complete. Section 3
derives $s_P^2$ and $s_Q^2$. Section 4 derives $k_P$ and $k_Q$ and thereby
constructs the squared standard error. Section 5 derives $\nu_P$ and $\nu_Q$
from the uncertainty of the two variance estimates. At the end of each
section, the newly derived quantities are inserted into this equation
immediately.

## 3. Derive the Variance Estimates $s_P^2$ and $s_Q^2$

The first unknowns in the two-population Welch-Satterthwaite equation are the
estimated variances $s_P^2$ and $s_Q^2$. Here, $s_P^2$ is the variance of the
pointwise mutual information contributed by individual observations from
population $P$. We derive it by calculating the first-order effect of an
observation in cell $(x,y)$. The calculation for $s_Q^2$ is identical.

### 3.1 Represent the effect of one observation

Fix a cell $(x,y)$. Move an infinitesimal amount of probability toward that
cell while preserving total probability:

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

For an arbitrary cell $(i,j)$, this means

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

Differentiating at the original distribution, where $\varepsilon=0$, gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x,j=y\}-p_{ij}.
$$

Summing this expression over columns and rows gives the corresponding changes
in the margins:

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{i+}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x\}-p_{i+},
$$

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

These marginal changes must be included because the PMI of every cell uses
both a joint probability and its row and column probabilities.

### 3.2 Calculate how that observation changes PMI

Along the perturbation path, the PMI in cell $(i,j)$ is

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Using $\mathrm d\log u/\mathrm d\varepsilon=u'/u$ and the three derivatives
from Section 3.1,

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

### 3.3 Calculate how that observation changes MI

MI under the perturbed distribution is

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)\ell_{P_\varepsilon}(i,j).
$$

Both the probability weights and the PMI values change, so the product rule
gives

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
&=\sum_{i,j}
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\ell_P(i,j)\\
&\quad+\sum_{i,j}p_{ij}\ell'_P(i,j;x,y).
\end{aligned}
$$

The first sum is

$$
\begin{aligned}
\sum_{i,j}
\{\mathbf 1\{i=x,j=y\}-p_{ij}\}\ell_P(i,j)
&=\ell_P(x,y)-\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\ell_P(x,y)-I(P).
\end{aligned}
$$

Substituting the PMI derivative into the second sum gives

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell'_P(i,j;x,y)
&=\sum_{i,j}p_{ij}
\left\{
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1
\right\}\\
&=\frac{p_{xy}}{p_{xy}}
-\frac{\sum_jp_{xj}}{p_{x+}}
-\frac{\sum_ip_{iy}}{p_{+y}}
+\sum_{i,j}p_{ij}\\
&=1-1-1+1\\
&=0.
\end{aligned}
$$

Therefore, an observation in cell $(x,y)$ changes MI to first order by

$$
\boxed{
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P).
}
$$

### 3.4 Use those observation effects to obtain $s_P^2$

The possible first-order effects are the centred PMI values
$\ell_P(X,Y)-I(P)$. Their population variance is

$$
\boxed{
V(P)
=\operatorname{Var}_P\{\ell_P(X,Y)\}
=\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2.
}
$$

The observed table estimates this variance by replacing each population
quantity with its empirical counterpart:

$$
\boxed{
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2.
}
$$

This is the estimated variance associated with population $P$ in the general
Welch-Satterthwaite equation. Thus

$$
\boxed{s_P^2=\widehat V(P).}
$$

Applying the same calculation to the empirical PMI values from the second
table gives

$$
\widehat V(Q)
=\sum_{i,j}\widehat q_{ij}
\{\widehat\ell_Q(i,j)-\widehat I(Q)\}^2,
$$

and therefore

$$
\boxed{s_Q^2=\widehat V(Q).}
$$

At this point, the two-population equation has become

$$
\nu_{\mathrm{expanded}}
=
\frac{
\{k_P\widehat V(P)+k_Q\widehat V(Q)\}^2
}{
\{k_P\widehat V(P)\}^2/\nu_P
+\{k_Q\widehat V(Q)\}^2/\nu_Q
}.
$$

The next section determines the two remaining weights.

## 4. Derive the Weights $k_P$ and $k_Q$

The quantities $\widehat V(P)$ and $\widehat V(Q)$ describe variation at the
level of one observation. The denominator of the test requires the sampling
variance of each complete MI estimate. The weights convert the
observation-level variances into those sampling variances.

### 4.1 Calculate the sampling variance of $\widehat I(P)$

The first-order expansion from Section 3 writes the error of the MI estimate
as an average of the observation effects:

$$
\widehat I(P)-I(P)
\approx
\frac{1}{n_P}\sum_{a=1}^{n_P}
\{\ell_P(Z_a^{(P)})-I(P)\}.
$$

The observations are independent, and each centred PMI value has variance
$V(P)$. Therefore,

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
&=\frac{1}{n_P^2}\,n_PV(P)\\
&=\boxed{\frac{V(P)}{n_P}}.
\end{aligned}
$$

The same argument gives

$$
\operatorname{Var}\{\widehat I(Q)\}
\approx\frac{V(Q)}{n_Q}.
$$

### 4.2 Calculate the sampling variance of the MI difference

The samples from $P$ and $Q$ are independent, so their covariance is zero.
Consequently,

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)-\widehat I(Q)\}
&=\operatorname{Var}\{\widehat I(P)\}
+\operatorname{Var}\{\widehat I(Q)\}\\
&\approx\frac{V(P)}{n_P}+\frac{V(Q)}{n_Q}.
\end{aligned}
$$

Replacing the unknown population variances with their table estimates gives
the squared standard error

$$
\boxed{
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
}
$$

### 4.3 Read the weights directly from the squared standard error

The weighted sum in the general equation is

$$
k_Ps_P^2+k_Qs_Q^2.
$$

Section 3 established $s_P^2=\widehat V(P)$ and
$s_Q^2=\widehat V(Q)$. The weighted sum must equal the squared standard error,
so

$$
k_P\widehat V(P)+k_Q\widehat V(Q)
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

The coefficients of the two variance estimates give the weights:

$$
\boxed{k_P=\frac{1}{n_P},}
\qquad
\boxed{k_Q=\frac{1}{n_Q}.}
$$

After inserting both the variance estimates and their weights, the
Welch-Satterthwaite equation is

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

Only $\nu_P$ and $\nu_Q$ remain to be derived.

## 5. Derive the Component Degrees of Freedom $\nu_P$ and $\nu_Q$

The denominator contains the estimated variances $\widehat V(P)$ and
$\widehat V(Q)$. Their component degrees of freedom must describe how much
these variance estimates would change if new samples were drawn. We derive
that sampling uncertainty for $\widehat V(P)$ and then convert it into
$\nu_P$. The calculation for $Q$ is identical.

### 5.1 Rewrite $V(P)$ so its sampling sensitivity can be calculated

The first moment of PMI is MI itself. Define its second moment by

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

This identity separates $V(P)$ into two quantities whose derivatives can be
calculated directly. Section 3.3 has already derived the derivative of
$I(P)$. We now calculate the derivative of $M_2(P)$ along the same path
$P_\varepsilon$.

### 5.2 Calculate how one observation changes $M_2(P)$

Under the cell perturbation from Section 3.1,

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

Now insert the PMI derivative from Section 3.2:

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

### 5.3 Calculate how one observation changes $V(P)$

Define the first-order effect of cell $(x,y)$ on the complete MI variance by

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

Insert the derivative of $M_2(P)$ from Section 5.2 and the derivative of
$I(P)$ from Section 3.3:

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

### 5.4 Use the $g_P$ values to obtain the sampling variance of $\widehat V(P)$

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

### 5.5 Moment-match those two quantities to obtain $\nu_P$

Satterthwaite models a positive estimated variance by a scaled chi-squared
variable. The chi-squared family is used because classical variance estimates
are sums of squared approximately normal sampling errors. Its degrees of
freedom provide a single parameter that controls the relative variability of
the variance estimate.

Let

$$
X_P\sim\chi^2_{\nu_P}.
$$

Since

$$
\operatorname E(X_P)=\nu_P,
\qquad
\operatorname{Var}(X_P)=2\nu_P,
$$

the scaled variable

$$
W_P=V(P)\frac{X_P}{\nu_P}
$$

has mean

$$
\begin{aligned}
\operatorname E(W_P)
&=\frac{V(P)}{\nu_P}\operatorname E(X_P)\\
&=\frac{V(P)}{\nu_P}\nu_P\\
&=V(P),
\end{aligned}
$$

which matches the first-order mean of $\widehat V(P)$. Its variance is

$$
\begin{aligned}
\operatorname{Var}(W_P)
&=\frac{V(P)^2}{\nu_P^2}\operatorname{Var}(X_P)\\
&=\frac{V(P)^2}{\nu_P^2}\,2\nu_P\\
&=\frac{2V(P)^2}{\nu_P}.
\end{aligned}
$$

Match this variance to the sampling variance derived in Section 5.4:

$$
\frac{2V(P)^2}{\nu_P}
=\frac{\tau^2(P)}{n_P}.
$$

Solving one step at a time,

$$
2n_PV(P)^2=\nu_P\tau^2(P),
$$

and therefore

$$
\boxed{
\nu_P
=\frac{2n_PV(P)^2}{\tau^2(P)}.
}
$$

Thus $\nu_P$ is large when $\widehat V(P)$ has little sampling variation
relative to its squared size, and small when the estimated variance is
unstable between samples.

### 5.6 Calculate $\widehat\nu_P$ and $\widehat\nu_Q$ from the observed tables

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

For the second table, calculate

$$
\widehat R_Q(i)
=\frac{\sum_j\widehat q_{ij}\widehat\ell_Q(i,j)}
{\widehat q_{i+}},
$$

$$
\widehat C_Q(j)
=\frac{\sum_i\widehat q_{ij}\widehat\ell_Q(i,j)}
{\widehat q_{+j}},
$$

$$
\begin{aligned}
\widehat g_Q(i,j)
&=\{\widehat\ell_Q(i,j)-\widehat I(Q)\}^2-\widehat V(Q)\\
&\quad+2\{\widehat\ell_Q(i,j)-\widehat R_Q(i)
-\widehat C_Q(j)+\widehat I(Q)\},
\end{aligned}
$$

$$
\overline g_Q
=\sum_{i,j}\widehat q_{ij}\widehat g_Q(i,j),
$$

and

$$
\widehat\tau^2(Q)
=\sum_{i,j}\widehat q_{ij}
\{\widehat g_Q(i,j)-\overline g_Q\}^2.
$$

The resulting component degrees of freedom are

$$
\boxed{
\widehat\nu_Q
=\frac{2n_Q\widehat V(Q)^2}{\widehat\tau^2(Q)}.
}
$$

Inserting these two quantities into the equation completed in Section 4 gives
the final expanded degrees of freedom:

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

## 6. Complete the Test

Section 1 produced the estimated MI difference. Section 4 produced its
estimated squared standard error. Combining them gives

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

## 7. Optional Bias-Corrected Combination Formula

The derivation above defines the primary expanded Welch test. A proposed
fourth-moment correction changes only the final rule for combining the two
variance components; it does not change $\widehat V(P)$,
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

## 8. Summary of the Derived Inputs

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
