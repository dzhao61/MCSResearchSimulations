# Archived Original Derivation of the Expanded Welch-Satterthwaite MI Test

## What Expanded Welch Is Trying to Correct

Suppose two independent populations, $P$ and $Q$, describe the same pair of
discrete variables $(X,Y)$. The aim is to test

$$
H_0:I(P)=I(Q)
\qquad\text{against}\qquad
H_1:I(P)\ne I(Q).
$$

All analytic methods considered here begin with the same standardized MI
difference:

$$
T
=\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
}.
$$

The numerator estimates the population MI difference. The denominator
estimates its sampling standard deviation. Normal Wald treats this estimated
denominator as sufficiently reliable and compares $T$ with a standard normal
distribution.

Expanded Welch goes one step further by quantifying the uncertainty of the
estimated variance components $\widehat V(P)$ and $\widehat V(Q)$ inside the
denominator. Each variance component is calculated from the same sampled
table as its MI estimate and is a nonlinear function of the joint
probabilities and both margins.

The architecture comes from Welch's unequal-variance test and
Satterthwaite's approximation for uncertain variance components. Hutcheson
adapted this architecture to comparisons of Shannon diversity. Expanded
Welch applies the same principle to mutual information, but derives the
variance-component uncertainty from the complete MI table functional rather
than assigning ordinary sample-variance degrees of freedom.

### Roadmap

The overall aim is to calculate an MI difference, divide it by its estimated
standard error, and choose a Student reference distribution that reflects how
reliably that standard error has been estimated.

Throughout the document, $P$ and $Q$ denote the two population joint
distributions, while $n_P$ and $n_Q$ denote their sample sizes. Population
quantities are written without a hat; a hat marks a quantity calculated from
a sampled contingency table.

The final statistic is

$$
T
=\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}},
$$

where $\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)$ is the
estimated MI difference and $\widehat V(P)/n_P$ and $\widehat V(Q)/n_Q$ are
the two estimated contributions to its squared standard error. Expanded Welch
compares $T$ with a Student distribution having
$\widehat\nu_{\mathrm{expanded}}$ degrees of freedom. Those degrees of freedom
are defined by the Welch-Satterthwaite equation

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

Here $\widehat\nu_V(P)$ and $\widehat\nu_V(Q)$ describe the reliability of
the two estimated variance components. The roadmap is therefore to calculate
$\widehat I_{\mathrm{BC}}(P)$, $\widehat I_{\mathrm{BC}}(Q)$,
$\widehat V(P)$, $\widehat V(Q)$, $\widehat\nu_V(P)$, and
$\widehat\nu_V(Q)$, then insert them into these two final equations.

1. **Estimate the MI difference.** The pointwise mutual information (PMI)
   $\ell_P(i,j)$ measures the information associated with cell $(i,j)$, and
   its population mean is the mutual information $I(P)$. The observed table
   gives the plug-in estimate $\widehat I(P)$ and its bias-corrected version
   $\widehat I_{\mathrm{BC}}(P)$. Repeating the calculation for $Q$ gives

   $$
   \widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q).
   $$

   Section 1 defines $\ell_P(i,j)$, $I(P)$, and their empirical versions.

2. **Estimate the sampling variance of the MI difference.** The PMI value
   $\ell_P(X,Y)$ is the observation-level quantity whose mean is $I(P)$. Its
   population variance is

   $$
   V(P)=\operatorname{Var}_P\{\ell_P(X,Y)\},
   $$

   so the first-order sampling variance of the MI estimate is

   $$
   \operatorname{Var}\{\widehat I_{\mathrm{BC}}(P)\}
   \approx\frac{V(P)}{n_P}.
   $$

   The observed table gives the plug-in estimate $\widehat V(P)$, so
   $\widehat V(P)/n_P$ is population $P$'s contribution to the squared
   standard error. Section 2 derives $V(P)$ and $\widehat V(P)$. Repeating the
   calculation for $Q$ gives $\widehat V(Q)/n_Q$.

3. **Calculate how reliable each estimated variance is.** The variance
   influence function

   $$
   g_P(x,y)
   =\left.
   \frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
   \right|_{\varepsilon=0}
   $$

   measures how an observation in cell $(x,y)$ changes $V(P)$ to first order.
   Here $P_\varepsilon$ is the population distribution after an infinitesimal
   shift of probability toward that cell. The variance of these effects is

   $$
   \tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}.
   $$

   It determines the sampling variance of $\widehat V(P)$:

   $$
   \operatorname{Var}\{\widehat V(P)\}
   \approx\frac{\tau^2(P)}{n_P}.
   $$

   Section 3 derives $g_P(x,y)$ and $\tau^2(P)$.

4. **Convert that reliability into component degrees of freedom.**
   Satterthwaite represents the sampling distribution of $\widehat V(P)$ by
   a scaled chi-squared distribution because variance estimates are built
   from squared sampling deviations, and sums of squared approximately normal
   deviations naturally have chi-squared distributions. Specifically,

   $$
   \widehat V(P)
   \quad\text{is modelled by}\quad
   V(P)\frac{\chi^2_{\nu_V(P)}}{\nu_V(P)}.
   $$

   A chi-squared variable with $\nu_V(P)$ degrees of freedom has mean
   $\nu_V(P)$ and variance $2\nu_V(P)$. The scaled model therefore has mean
   $V(P)$ and variance

   $$
   \frac{2V(P)^2}{\nu_V(P)}.
   $$

   Matching that mean and variance to those of $\widehat V(P)$ gives the
   Satterthwaite equation

   $$
   \boxed{
   \nu_V(P)
   =\frac{2\left[\operatorname E\{\widehat V(P)\}\right]^2}
   {\operatorname{Var}\{\widehat V(P)\}}.
   }
   $$

   Using

   $$
   \operatorname E\{\widehat V(P)\}\approx V(P),
   \qquad
   \operatorname{Var}\{\widehat V(P)\}
   \approx\frac{\tau^2(P)}{n_P},
   $$

   gives

   $$
   \nu_V(P)
   =\frac{2V(P)^2}{\tau^2(P)/n_P}
   =\frac{2n_PV(P)^2}{\tau^2(P)}.
   $$

   Replacing $V(P)$ and $\tau^2(P)$ with their empirical estimates gives

   $$
   \widehat\nu_V(P)
   =\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
   $$

   Section 4 derives this moment matching. Repeating it for $Q$ gives
   $\widehat\nu_V(Q)$.

5. **Complete the test.** Repeat the calculations for both populations, insert
   the resulting quantities into the equations at the start of this roadmap,
   and compare $T$ with $t_{\widehat\nu_{\mathrm{expanded}}}$. Section 5
   derives the combined degrees of freedom and the final two-sided p-value.

The remainder of the document proves each result used in this roadmap. The
derivation uses natural logarithms, so MI is measured in nats.

## 1. Estimate the Difference in Mutual Information

The first step is to define the population quantity being compared and its
sample estimate.

### 1.1 Start with two independent contingency tables

Let

$$
Z_1^{(P)},\ldots,Z_{n_P}^{(P)}\overset{\mathrm{iid}}{\sim}P,
\qquad
Z_1^{(Q)},\ldots,Z_{n_Q}^{(Q)}\overset{\mathrm{iid}}{\sim}Q,
$$

where each observation is

$$
Z=(X,Y)\in\{1,\ldots,r\}\times\{1,\ldots,c\}.
$$

The samples are independent of one another. Within each sample, observations
are independent draws from one fixed population table. These assumptions will
later allow sampling variances to be added and covariance terms between
observations to be removed.

For population $P$, write

$$
p_{ij}=\Pr_P(X=i,Y=j),
$$

with margins

$$
p_{i+}=\sum_jp_{ij},
\qquad
p_{+j}=\sum_ip_{ij}.
$$

The same definitions apply to $Q$.

### 1.2 Calculate population MI from pointwise mutual information

Under independence with the same margins, cell $(i,j)$ would have probability
$p_{i+}p_{+j}$. Its pointwise mutual information (PMI) is therefore

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

Mutual information is the probability-weighted mean of these PMI values:

$$
\begin{aligned}
I(P)
&=\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\operatorname E_P\{\ell_P(X,Y)\}.
\end{aligned}
$$

This expectation form is important because the sampling error of plug-in MI
will be determined by how individual PMI values vary around their mean.

### 1.3 Estimate MI from the observed counts and correct its leading bias

Let $N_{ij}^{(P)}$ be the observed counts from population $P$. The empirical
probabilities are

$$
\widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P},
\qquad
n_P=\sum_{i,j}N_{ij}^{(P)}.
$$

Recalculate the margins from the same table:

$$
\widehat p_{i+}=\sum_j\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_i\widehat p_{ij}.
$$

The empirical PMI values and plug-in MI are

$$
\widehat\ell_P(i,j)
=\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right),
$$

and

$$
\widehat I(P)
=\sum_{i,j}\widehat p_{ij}\widehat\ell_P(i,j).
$$

For a fixed $r\times c$ alphabet with full population support, the leading
plug-in MI bias is

$$
\operatorname{Bias}\{\widehat I(P)\}
\approx\frac{(r-1)(c-1)}{2n_P}.
$$

This follows from the usual leading plug-in entropy bias applied to
$I(X;Y)=H(X)+H(Y)-H(X,Y)$. Define

$$
d=(r-1)(c-1).
$$

The bias-corrected estimates are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P},
$$

and

$$
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated population difference is

$$
\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

The bias correction improves the centre of the numerator. At fixed sample
sizes and dimensions it is a constant, so the first-order sampling variance
remains unchanged.

## 2. Calculate How Much Estimated MI Varies Between Samples

To standardize the MI difference, we calculate its sampling variance. Because
MI is a nonlinear functional of the whole table, this variance is obtained
from its influence function: the first-order change in MI caused by one
possible observation.

### 2.1 Represent the effect of adding an observation to one cell

Fix a cell $z=(x,y)$ and define the probability-preserving path

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)},
$$

where $\delta_{(x,y)}$ puts probability one on $(x,y)$. Thus

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

This path represents the infinitesimal effect of adding an observation at
$(x,y)$ while preserving total probability. The influence function of a
functional $F$ is the directional derivative

$$
\operatorname{IF}_{F,P}(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}F(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

The derivative is evaluated at zero because the required sensitivity is local
to the original population $P$.

Differentiating the cell and marginal probabilities gives

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

The marginal derivatives are required because changing one joint cell changes
the independence baseline for its entire row and column.

### 2.2 Calculate how that observation changes the PMI values

Along the path,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Using $\mathrm d\log u/\mathrm d\varepsilon=u'/u$,

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

### 2.3 Calculate how that observation changes MI

Since

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j),
$$

the product rule gives

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
&=1
-\frac{\sum_jp_{xj}}{p_{x+}}
-\frac{\sum_ip_{iy}}{p_{+y}}
+\sum_{i,j}p_{ij}\\
&=1-1-1+1\\
&=0.
\end{aligned}
$$

Therefore, the first-order change in MI produced by an observation in cell
$(x,y)$ is

$$
\boxed{
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
=\ell_P(x,y)-I(P).
}
$$

This centred PMI value is the influence function of MI.

### 2.4 Average the observation effects to obtain the variance of estimated MI

The probability-weighted variance of PMI is

$$
\begin{aligned}
V(P)
&=\operatorname{Var}_P\{\ell_P(X,Y)\}\\
&=\sum_{i,j}p_{ij}\{\ell_P(i,j)-I(P)\}^2.
\end{aligned}
$$

Under a fixed finite alphabet, positive support, and finite nonzero $V(P)$,
the functional delta method gives

$$
\widehat I(P)-I(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}
\{\ell_P(Z_k^{(P)})-I(P)\}
+o_p(n_P^{-1/2}).
$$

The leading term is an average of iid, mean-zero contributions. Hence

$$
\begin{aligned}
\operatorname{Var}\{\widehat I(P)\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}
\{\ell_P(Z_k^{(P)})-I(P)\}
\right\}\\
&=\frac{1}{n_P^2}
\sum_{k=1}^{n_P}
\operatorname{Var}_P\{\ell_P(Z_k^{(P)})-I(P)\}\\
&=\frac{1}{n_P^2}n_PV(P)\\
&=\boxed{\frac{V(P)}{n_P}}.
\end{aligned}
$$

The plug-in estimate of $V(P)$ is

$$
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2.
$$

Repeating the calculation for $Q$ and using independence between the two
samples gives

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V(P)}{n_P}
+\frac{\widehat V(Q)}{n_Q}.
$$

The standardized statistic is therefore

$$
T
=\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

This completes the usual normal-Wald construction. Expanded Welch begins at
the point where normal Wald stops: it examines how much
$\widehat V(P)$ and $\widehat V(Q)$ themselves fluctuate across samples.

## 3. Calculate How Much the Estimated MI Variance Changes Between Samples

Satterthwaite needs the first two moments of each estimated variance
component. To first order,

$$
\operatorname E\{\widehat V(P)\}\approx V(P).
$$

The missing quantity is

$$
\operatorname{Var}\{\widehat V(P)\}.
$$

We obtain it by differentiating the variance functional $V(P)$ along the same
cell-contamination path. The resulting influence function is denoted
$g_P(x,y)$.

### 3.1 Rewrite $V(P)$ in a form that can be differentiated

Define

$$
M_2(P)
=\sum_{i,j}p_{ij}\ell_P(i,j)^2.
$$

Then

$$
V(P)=M_2(P)-I(P)^2.
$$

Writing the variance in this two-moment form allows it to be differentiated
directly with the product and chain rules.

### 3.2 Calculate how one observation changes the second moment

Along the path,

$$
M_2(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j)^2.
$$

Differentiating both the probability weight and the squared PMI value gives

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

The first sum is

$$
\ell_P(x,y)^2-M_2(P).
$$

For the second sum, define the probability-weighted PMI means in row
$x$ and column $y$:

$$
R_P(x)
=\frac{\sum_jp_{xj}\ell_P(x,j)}{p_{x+}},
$$

and

$$
C_P(y)
=\frac{\sum_ip_{iy}\ell_P(i,y)}{p_{+y}}.
$$

Substituting the PMI derivative from Section 2.2 gives

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P(i,j)\ell'_P(i,j;x,y)
&=\sum_{i,j}p_{ij}\ell_P(i,j)
\left\{
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1
\right\}\\
&=\ell_P(x,y)
-\frac{\sum_jp_{xj}\ell_P(x,j)}{p_{x+}}
-\frac{\sum_ip_{iy}\ell_P(i,y)}{p_{+y}}
+\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\ell_P(x,y)-R_P(x)-C_P(y)+I(P).
\end{aligned}
$$

Therefore,

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

The row and column terms account for the changes in marginal probabilities
produced by the cell perturbation.

### 3.3 Combine the derivatives to obtain $g_P(x,y)$

Define the influence function of the MI variance functional:

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
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}M_2(P_\varepsilon)
\right|_{\varepsilon=0}\\
&\quad-2I(P)
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Substituting the two derivatives gives

$$
\begin{aligned}
g_P(x,y)
&=\ell_P(x,y)^2-M_2(P)\\
&\quad+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}\\
&\quad-2I(P)\{\ell_P(x,y)-I(P)\}.
\end{aligned}
$$

The first and third lines simplify as follows:

$$
\begin{aligned}
&\ell_P(x,y)^2-M_2(P)
-2I(P)\{\ell_P(x,y)-I(P)\}\\
&\qquad
=\{\ell_P(x,y)-I(P)\}^2
-\{M_2(P)-I(P)^2\}\\
&\qquad
=\{\ell_P(x,y)-I(P)\}^2-V(P).
\end{aligned}
$$

Hence

$$
\boxed{
g_P(x,y)
=\{\ell_P(x,y)-I(P)\}^2-V(P)
+2\{\ell_P(x,y)-R_P(x)-C_P(y)+I(P)\}.
}
$$

The first part measures the direct change in squared MI influence. The second
part measures the indirect change caused by the row and column margins. Their
sum is the complete first-order sensitivity of the MI variance.

The population mean of $g_P$ is zero. The first part has mean zero by the
definition of $V(P)$, while

$$
\operatorname E_P\{\ell_P(X,Y)\}
-\operatorname E_P\{R_P(X)\}
-\operatorname E_P\{C_P(Y)\}
+I(P)
=I(P)-I(P)-I(P)+I(P)=0.
$$

### 3.4 Average the $g_P$ values to obtain the variance of $\widehat V(P)$

Define

$$
\tau^2(P)
=\operatorname{Var}_P\{g_P(X,Y)\}.
$$

The functional delta method now gives

$$
\widehat V(P)-V(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
+o_p(n_P^{-1/2}).
$$

Because the observations are iid and $g_P$ has mean zero,

$$
\begin{aligned}
\operatorname{Var}\{\widehat V(P)\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\left[
\sum_{k=1}^{n_P}\operatorname{Var}_P\{g_P(Z_k^{(P)})\}
+2\sum_{1\le k<l\le n_P}
\operatorname{Cov}_P\{g_P(Z_k^{(P)}),g_P(Z_l^{(P)})\}
\right]\\
&=\frac{1}{n_P^2}\sum_{k=1}^{n_P}\tau^2(P)\\
&=\frac{1}{n_P^2}n_P\tau^2(P)\\
&=\boxed{\frac{\tau^2(P)}{n_P}}.
\end{aligned}
$$

The covariance terms vanish because the observations are independent. This is
the quantity the derivation set out to find. We can now convert denominator
uncertainty into Satterthwaite degrees of freedom.

## 4. Use the Uncertainty of $\widehat V(P)$ to Choose Degrees of Freedom

We have established the first-order moments

$$
\operatorname E\{\widehat V(P)\}\approx V(P),
$$

and

$$
\operatorname{Var}\{\widehat V(P)\}
\approx\frac{\tau^2(P)}{n_P}.
$$

Satterthwaite represents the finite-sample distribution of $\widehat V(P)$ by
a positive distribution with these same two moments.

### 4.1 Why approximate $\widehat V(P)$ with a scaled chi-squared distribution?

The chi-squared model comes from the classical structure of variance
estimation. For normal observations, a sample variance is a sum of squared
independent standardized residuals, giving the exact result

$$
\frac{(n-1)S^2}{\sigma^2}\sim\chi^2_{n-1}.
$$

More general estimated variances often behave like nonnegative quadratic
forms in approximately Gaussian estimation errors. Such a quadratic form is
typically a weighted sum of chi-squared components. Satterthwaite represents
that weighted sum by a single scaled chi-squared variable whose mean and
variance agree with the target variance estimate.

For the MI variance estimator, this scaled chi-squared distribution is a
moment-matched working model. It has nonnegative support, allows finite-sample
right skewness, becomes more symmetric as its degrees of freedom increase,
and connects denominator uncertainty to a Student reference.

### 4.2 Choose the scale so the means match

Let

$$
X\sim\chi^2_{\nu_V(P)}.
$$

Then

$$
\operatorname E(X)=\nu_V(P),
\qquad
\operatorname{Var}(X)=2\nu_V(P).
$$

Dividing by $\nu_V(P)$ gives a variable with mean one. Multiplying by $V(P)$
therefore gives

$$
W_P
=V(P)\frac{X}{\nu_V(P)},
$$

with

$$
\begin{aligned}
\operatorname E(W_P)
&=V(P)\frac{\operatorname E(X)}{\nu_V(P)}\\
&=V(P).
\end{aligned}
$$

Satterthwaite uses the distribution of $W_P$ as the working distribution for
$\widehat V(P)$.

### 4.3 Choose the degrees of freedom so the variances match

The variance of $W_P$ is

$$
\begin{aligned}
\operatorname{Var}(W_P)
&=V(P)^2
\operatorname{Var}\left\{\frac{X}{\nu_V(P)}\right\}\\
&=V(P)^2
\frac{2\nu_V(P)}{\nu_V(P)^2}\\
&=\frac{2V(P)^2}{\nu_V(P)}.
\end{aligned}
$$

Set this equal to the derived sampling variance of $\widehat V(P)$:

$$
\frac{2V(P)^2}{\nu_V(P)}
=\frac{\tau^2(P)}{n_P}.
$$

Solving gives

$$
\boxed{
\nu_V(P)
=\frac{2n_PV(P)^2}{\tau^2(P)}.
}
$$

Equivalently,

$$
\nu_V(P)
=\frac{2}
{\tau^2(P)/\{n_PV(P)^2\}}.
$$

The denominator is the relative sampling variance of the estimated MI
variance. A stable estimate has small relative variance and many effective
degrees of freedom. An unstable estimate has large relative variance and few
effective degrees of freedom. The factor $2$ comes directly from
$\operatorname{Var}(\chi^2_\nu)=2\nu$.

### 4.4 Estimate the component degrees of freedom from the observed table

The population quantities are unknown, so substitute their empirical
counterparts. For population $P$, calculate

$$
\widehat V(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat\ell_P(i,j)-\widehat I(P)\}^2,
$$

$$
\widehat R_P(i)
=\frac{\sum_j\widehat p_{ij}\widehat\ell_P(i,j)}
{\widehat p_{i+}},
$$

and

$$
\widehat C_P(j)
=\frac{\sum_i\widehat p_{ij}\widehat\ell_P(i,j)}
{\widehat p_{+j}}.
$$

Insert these estimates into the derived variance influence function:

$$
\widehat g_P(i,j)
=\{\widehat\ell_P(i,j)-\widehat I(P)\}^2-\widehat V(P)
+2\{\widehat\ell_P(i,j)-\widehat R_P(i)
-\widehat C_P(j)+\widehat I(P)\}.
$$

Although the population influence function has mean zero, explicitly centre
the empirical values:

$$
\overline g_P
=\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j),
$$

$$
\widehat\tau^2(P)
=\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2.
$$

The observed component degrees of freedom are

$$
\boxed{
\widehat\nu_V(P)
=\frac{2n_P\widehat V(P)^2}
{\widehat\tau^2(P)}.
}
$$

The same calculation gives $\widehat\nu_V(Q)$ from the second table.

This plug-in step uses the empirical table as a local representation of its
population. Under fixed dimensions and positive support, consistency of the
empirical distribution establishes this property asymptotically. Extensive
empirical support loss places the calculation outside this smooth
finite-sample regime.

## 5. Combine the Two Populations and Calculate the P-Value

Each population now contributes both an estimated variance component and an
effective reliability for that component. The final step combines them.

### 5.1 Form each population's contribution to the squared standard error

Dividing a variance estimate by a fixed sample size changes its scale while
preserving its Satterthwaite degrees of freedom. For example,

$$
\operatorname E\left\{\frac{\widehat V(P)}{n_P}\right\}
\approx\frac{V(P)}{n_P},
$$

and

$$
\operatorname{Var}\left\{\frac{\widehat V(P)}{n_P}\right\}
\approx\frac{1}{n_P^2}
\frac{\tau^2(P)}{n_P}
=\frac{\tau^2(P)}{n_P^3}.
$$

Therefore,

$$
\begin{aligned}
\frac{
2\left[\operatorname E\{\widehat V(P)/n_P\}\right]^2
}{
\operatorname{Var}\{\widehat V(P)/n_P\}
}
&\approx
\frac{2\{V(P)/n_P\}^2}{\tau^2(P)/n_P^3}\\
&=\frac{2n_PV(P)^2}{\tau^2(P)}\\
&=\nu_V(P).
\end{aligned}
$$

Thus $\widehat V(P)/n_P$ retains component degrees of freedom $\nu_V(P)$,
and $\widehat V(Q)/n_Q$ retains $\nu_V(Q)$.

### 5.2 Choose degrees of freedom for the sum of those contributions

The samples are independent, so

$$
\operatorname{Var}\left\{
\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}
\right\}
=\operatorname{Var}\left\{\frac{\widehat V(P)}{n_P}\right\}
+\operatorname{Var}\left\{\frac{\widehat V(Q)}{n_Q}\right\}.
$$

Under the component scaled chi-squared models,

$$
\operatorname{Var}\left\{\frac{\widehat V(P)}{n_P}\right\}
\approx
\frac{
2\left[\operatorname E\{\widehat V(P)/n_P\}\right]^2
}{\nu_V(P)},
$$

and

$$
\operatorname{Var}\left\{\frac{\widehat V(Q)}{n_Q}\right\}
\approx
\frac{
2\left[\operatorname E\{\widehat V(Q)/n_Q\}\right]^2
}{\nu_V(Q)}.
$$

Moment matching the sum to one scaled chi-squared variable gives

$$
\nu_{\mathrm{expanded}}
=\frac{
\left[
\operatorname E\{\widehat V(P)/n_P\}
+\operatorname E\{\widehat V(Q)/n_Q\}
\right]^2
}{
\left[\operatorname E\{\widehat V(P)/n_P\}\right]^2/\nu_V(P)
+\left[\operatorname E\{\widehat V(Q)/n_Q\}\right]^2/\nu_V(Q)
}.
$$

Replacing the unknown expectations and degrees of freedom with their observed
estimates gives

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

The squared weights appear because the variance of a scaled random variable
depends on the square of its scale.

### 5.3 Compare the statistic with a Student distribution

The final statistic remains

$$
T
=\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}
{\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}}.
$$

In classical normal theory, a standard normal numerator divided by the square
root of an independent normalized chi-squared variance estimate has an exact
Student distribution. That normal-over-estimated-variance structure explains
why the scaled chi-squared denominator model leads to a Student reference.

Expanded Welch uses this Student distribution as a finite-sample reference.
The numerator is asymptotically normal, and the two denominator components
are combined by moment matching. The resulting statistic is interpreted
using a Student distribution with $\widehat\nu_{\mathrm{expanded}}$ degrees
of freedom. The two-sided p-value is

$$
\boxed{
p_{\mathrm{expanded}}
=2\left[
1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)
\right].
}
$$

When the denominator is stable, the effective degrees of freedom are large
and the Student reference approaches the normal reference. When it is
unstable, the degrees of freedom fall and the reference acquires heavier
tails.

## 6. Summary of the Calculation

The complete calculation is:

$$
\begin{aligned}
\ell_P(i,j)
&=\log\frac{p_{ij}}{p_{i+}p_{+j}},\\[3pt]
I(P)
&=\operatorname E_P\{\ell_P(X,Y)\},\\[3pt]
V(P)
&=\operatorname{Var}_P\{\ell_P(X,Y)\},\\[3pt]
\operatorname{Var}\{\widehat I(P)\}
&\approx\frac{V(P)}{n_P},\\[3pt]
g_P(i,j)
&=\{\ell_P(i,j)-I(P)\}^2-V(P)
+2\{\ell_P(i,j)-R_P(i)-C_P(j)+I(P)\},\\[3pt]
\tau^2(P)
&=\operatorname{Var}_P\{g_P(X,Y)\},\\[3pt]
\operatorname{Var}\{\widehat V(P)\}
&\approx\frac{\tau^2(P)}{n_P},\\[3pt]
\nu_V(P)
&=\frac{2n_PV(P)^2}{\tau^2(P)},\\[3pt]
\widehat\nu_{\mathrm{expanded}}
&=\frac{
\left\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\right\}^2
}{
\left\{\widehat V(P)/n_P\right\}^2/\widehat\nu_V(P)
+\left\{\widehat V(Q)/n_Q\right\}^2/\widehat\nu_V(Q)
},\\[3pt]
p_{\mathrm{expanded}}
&=2\left[
1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)
\right].
\end{aligned}
$$

The formulas from $\ell_P$ through $\operatorname{Var}\{\widehat I(P)\}$
describe the MI estimate and its sampling variance. The formulas from $g_P$
through $\nu_V(P)$ describe the uncertainty of the estimated variance. The
final formulas combine the two populations and calibrate the standardized MI
difference.

## 7. Assumptions and Limitations

The argument relies on several conditions introduced at the points where they
are needed.

### 7.1 Fixed finite alphabet and positive population support

The influence derivatives assume $r$ and $c$ remain fixed as sample sizes
increase and that modelled population cells have positive probability. These
conditions keep the logarithms finite and the MI and variance functionals
smooth. Structural zeros require defining a smaller fixed support before
applying the derivation.

Observed zero-count cells are assigned zero weight under $0\log 0=0$. For an
empty empirical row or column, the implementation assigns zero to the unused
conditional PMI mean because every cell in that margin also has zero weight.
These conventions keep the calculation finite. The smooth population
approximation applies when the sampled support remains sufficiently stable.

### 7.2 Independent observations and independent samples

The $1/n$ variance derivations use iid observations. The addition of the $P$
and $Q$ variance components uses independence between samples. Paired,
clustered, longitudinal, or overlapping samples require covariance terms and
a different derivation.

### 7.3 Nondegenerate first-order MI variance

At exact independence,

$$
p_{ij}=p_{i+}p_{+j},
$$

so every PMI value and $V(P)$ are zero. The first-order normal expansion
then degenerates. This test concerns regular comparisons of two MI values with
a positive combined first-order variance. Testing independence itself requires
second-order theory.

### 7.4 Which parts are approximations

The formulas for the influence functions are directional derivatives on
positive support. The formulas $V(P)/n_P$ and $\tau^2(P)/n_P$ are first-order
functional delta-method results. The scaled chi-squared and Student
distributions provide moment-matched finite-sample references.

The leading bias correction is the first-order full-support correction for
fixed table dimensions. Its configured dimensions are chosen before observing
the data.

### 7.5 What the simulations show about the limits

Direct simulation found that the scaled chi-squared model was close to the
finite-sample distribution of $\widehat V(P)$ when supplied with the correct
moments, with mean KS distance 0.0199 across the focused grid. It was
especially effective for upper-tail calibration and for $5\times5$ and
$10\times10$ tables. It was less accurate in some $2\times2$ cases.

The complete expanded-Welch test improved calibration in sparse, skewed, and
unequal-sample regimes when sampled support remained mostly informative. In
well-sampled tables and under widespread support loss, normal Wald or simple
Welch was often better calibrated. These results characterize expanded Welch
as a targeted finite-sample correction for the regimes in which estimated
variance uncertainty is consequential.

## 8. Runtime and Source Code

Once the two count tables have been formed, every quantity is calculated by a
fixed number of cell scans and row or column reductions:

$$
\boxed{
\text{time complexity }O(rc),
\qquad
\text{memory complexity }O(rc).
}
$$

If the input consists of raw observations, constructing the two tables first
costs $O(n_P+n_Q)$. No permutations, bootstrap samples, or Monte Carlo tables
are needed by the test itself.

The implementation is in
[`src/welch_differential_mi/welch.py`](../src/welch_differential_mi/welch.py).

| Mathematical quantity | Implementation name |
| --- | --- |
| $\widehat I(G)$ | `plugin_mi(...)` |
| $d$ | `mi_df` |
| $\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)$ | `delta` |
| $\widehat V(P),\widehat V(Q)$ | `variance_p`, `variance_q` |
| $\widehat V(P)/n_P,\widehat V(Q)/n_Q$ | `component_p`, `component_q` |
| $T$ | `statistic` |
| $\widehat R_G(i)$ | `row_score_mean` |
| $\widehat C_G(j)$ | `column_score_mean` |
| $\widehat g_G(i,j)$ | `variance_influence` |
| $\widehat\tau^2(G)$ | `influence_variance` inside `_variance_influence_component_df` |
| $\widehat\nu_V(P),\widehat\nu_V(Q)$ | `expanded_df_p`, `expanded_df_q` |
| $\widehat\nu_{\mathrm{expanded}}$ | `expanded_df` |
| $p_{\mathrm{expanded}}$ | `expanded_p` |

The direct scaled chi-squared validation is reported in
[`../results/scaled_chi_square_validation/REPORT.md`](../results/scaled_chi_square_validation/REPORT.md).

## References

- Hutcheson, K. (1970). *A Test for Comparing Diversities Based on the
  Shannon Formula*. Journal of Theoretical Biology, 29, 151-154.
  <https://doi.org/10.1016/0022-5193(70)90124-4>
- Satterthwaite, F. E. (1946). *An Approximate Distribution of Estimates of
  Variance Components*. Biometrics Bulletin, 2, 110-114.
  <https://doi.org/10.2307/3002019>
- Welch, B. L. (1947). *The Generalization of Student's Problem When Several
  Different Population Variances Are Involved*. Biometrika, 34, 28-35.
  <https://doi.org/10.1093/biomet/34.1-2.28>
