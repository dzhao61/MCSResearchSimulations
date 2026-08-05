# Full Derivation of the Expanded Welch-Satterthwaite MI Test

## Purpose

This chapter derives a deterministic test for comparing the mutual
information of two independent discrete populations. The null hypothesis is

$$
H_0:I(P)=I(Q).
$$

The construction follows the broad logic of Welch's test:

1. estimate the difference between two population quantities;
2. divide that difference by its estimated standard error;
3. account for uncertainty in the estimated standard error by using a
   Student distribution with Satterthwaite effective degrees of freedom.

The important difference is that mutual information is a nonlinear
functional of a complete joint probability table. Its variance estimator is
therefore not an ordinary sample variance. The expanded method derives the
first-order sampling uncertainty of that complete variance functional and
uses it to calculate MI-specific component degrees of freedom.

The derivation below is written for natural logarithms, so MI is measured in
nats.

## 1. Statistical Setting

Let

$$
Z_1^{(P)},\ldots,Z_{n_P}^{(P)}\overset{\mathrm{iid}}{\sim}P,
\qquad
Z_1^{(Q)},\ldots,Z_{n_Q}^{(Q)}\overset{\mathrm{iid}}{\sim}Q,
$$

where every observation is a pair

$$
Z=(X,Y)\in\{1,\ldots,r\}\times\{1,\ldots,c\}.
$$

The two samples are independent. Write the population cell probabilities as

$$
p_{ij}=\Pr_P(X=i,Y=j),
\qquad
q_{ij}=\Pr_Q(X=i,Y=j).
$$

For population $P$, define the marginal probabilities

$$
p_{i+}=\sum_{j=1}^{c}p_{ij},
\qquad
p_{+j}=\sum_{i=1}^{r}p_{ij}.
$$

The corresponding definitions apply to $Q$.

The regular derivation assumes a fixed finite alphabet and positive
population support:

$$
p_{ij}>0,
\qquad
q_{ij}>0
$$

for all modelled cells. This makes the logarithms and derivatives below
well-defined. Section 16 explains what changes when observed cells are empty
or the population is at independence.

## 2. Mutual Information as a Functional

For a distribution $P$, define the local-information score of cell $(i,j)$
by

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

The population mutual information is

$$
\begin{aligned}
I(P)
&=\sum_{i=1}^{r}\sum_{j=1}^{c}
p_{ij}\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)\\
&=\operatorname E_P\{\ell_P(X,Y)\}.
\end{aligned}
$$

For notational convenience, write

$$
\mu_P=I(P).
$$

The subscript on $\ell_P$ matters. The score is not a fixed value attached
to a cell independently of the distribution. If $P$ changes, the joint
probability, both relevant marginal probabilities, and therefore the score
all change.

## 3. Plug-In Estimation

Let $N_{ij}^{(P)}$ be the observed count in cell $(i,j)$ of the first table.
Then

$$
n_P=\sum_{i=1}^{r}\sum_{j=1}^{c}N_{ij}^{(P)},
\qquad
\widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P}.
$$

The empirical marginals are

$$
\widehat p_{i+}=\sum_{j=1}^{c}\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_{i=1}^{r}\widehat p_{ij}.
$$

The plug-in local-information score and plug-in MI are

$$
\widehat\ell_{ij}
=\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right)
$$

and

$$
\widehat I(P)
=\sum_{i=1}^{r}\sum_{j=1}^{c}
\widehat p_{ij}\widehat\ell_{ij}.
$$

Equivalently, if $\widehat P$ is the empirical distribution, then

$$
\widehat I(P)=I(\widehat P).
$$

The same calculations produce $\widehat I(Q)$ from the second table.

## 4. Leading Bias Correction

### 4.1 Bias of plug-in entropy

For a discrete variable with $k$ positive-probability categories, the
leading bias of the plug-in entropy estimator is

$$
\operatorname E(\widehat H)-H
=-\frac{k-1}{2n}+O(n^{-2}).
$$

Mutual information can be written as

$$
I(X;Y)=H(X)+H(Y)-H(X,Y).
$$

Under full support, $X$ has $r$ categories, $Y$ has $c$ categories, and the
joint variable $(X,Y)$ has $rc$ categories. Applying the entropy bias formula
to these three terms gives

$$
\begin{aligned}
\operatorname{Bias}(\widehat I)
&\approx
-\frac{r-1}{2n}
-\frac{c-1}{2n}
-\left(-\frac{rc-1}{2n}\right)\\
&=\frac{rc-r-c+1}{2n}\\
&=\frac{(r-1)(c-1)}{2n}.
\end{aligned}
$$

Define

$$
d=(r-1)(c-1).
$$

### 4.2 Bias-corrected MI difference

The leading-bias-corrected estimators are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P}
$$

and

$$
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated population difference is

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

Expanding this expression gives

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I(P)-\widehat I(Q)
-\frac{d}{2n_P}+\frac{d}{2n_Q}.
$$

For fixed table dimensions and fixed sample sizes, the correction terms are
constants. They change the estimated difference but do not add sampling
variance and do not change the influence function derived next.

## 5. Deriving the Influence Function of MI

### 5.1 Contaminate one cell

Fix a cell $z=(x,y)$. Define a path of distributions

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_z,
$$

where $\delta_z$ places probability one on cell $z$. At $\varepsilon=0$ the
distribution is $P$. Increasing $\varepsilon$ moves a small amount of
probability toward cell $(x,y)$ while preserving total probability one.

For an arbitrary cell $(i,j)$,

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

Therefore,

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x,j=y\}-p_{ij}.
$$

Summing over columns gives

$$
p_{i+}(\varepsilon)
=(1-\varepsilon)p_{i+}
+\varepsilon\mathbf 1\{i=x\},
$$

so

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{i+}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x\}-p_{i+}.
$$

Likewise,

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

### 5.2 Differentiate the local-information score

Under $P_\varepsilon$, the score of cell $(i,j)$ is

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Use

$$
\frac{\mathrm d}{\mathrm d\varepsilon}\log u(\varepsilon)
=\frac{u'(\varepsilon)}{u(\varepsilon)}.
$$

The derivative of the joint-probability term at zero is

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}\log p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
&=\frac{\mathbf 1\{i=x,j=y\}-p_{ij}}{p_{ij}}\\
&=\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}-1.
\end{aligned}
$$

Similarly,

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}\log p_{i+}(\varepsilon)
\right|_{\varepsilon=0}
=\frac{\mathbf 1\{i=x\}}{p_{i+}}-1
$$

and

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}\log p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
=\frac{\mathbf 1\{j=y\}}{p_{+j}}-1.
$$

Subtracting the two marginal derivatives from the joint derivative gives

$$
\boxed{
\dot\ell_P(i,j;z)
=
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1,
}
$$

where

$$
\dot\ell_P(i,j;z)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}.
$$

### 5.3 A derivative rule for distribution-dependent expectations

Suppose

$$
F(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)h_{P_\varepsilon}(i,j),
$$

where both the probabilities and the values $h_{P_\varepsilon}$ depend on
$\varepsilon$. The product rule gives

$$
\begin{aligned}
\left.\frac{\mathrm d}{\mathrm d\varepsilon}F(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]h_P(i,j)\\
&+\sum_{i,j}p_{ij}\dot h_P(i,j;z).
\end{aligned}
$$

The first sum is

$$
h_P(x,y)-\operatorname E_P\{h_P(X,Y)\}.
$$

Therefore,

$$
\boxed{
\operatorname{IF}_{F,P}(z)
=h_P(z)-\operatorname E_P(h_P)
+\operatorname E_P\{\dot h_P(Z;z)\}.
}
$$

The last term is essential whenever the quantity being averaged changes with
the underlying distribution.

### 5.4 Apply the rule to MI

For MI, take

$$
h_P(i,j)=\ell_P(i,j).
$$

We first evaluate the expectation of the score derivative:

$$
\begin{aligned}
\operatorname E_P\{\dot\ell_P(Z;z)\}
={}&\sum_{i,j}p_{ij}
\left[
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1
\right]\\
={}&1
-\frac{\sum_j p_{xj}}{p_{x+}}
-\frac{\sum_i p_{iy}}{p_{+y}}
+\sum_{i,j}p_{ij}\\
={}&1-1-1+1\\
={}&0.
\end{aligned}
$$

The derivative rule therefore yields

$$
\begin{aligned}
\operatorname{IF}_{I,P}(x,y)
&=\ell_P(x,y)-\operatorname E_P(\ell_P)+0\\
&=\ell_P(x,y)-\mu_P.
\end{aligned}
$$

Define

$$
\boxed{
\psi_P(x,y)=\ell_P(x,y)-\mu_P.
}
$$

This is the influence function of mutual information.

### 5.5 First-order sampling variance of plug-in MI

The empirical distribution satisfies a first-order functional expansion:

$$
I(\widehat P)-I(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}\psi_P(Z_k^{(P)})
+o_p(n_P^{-1/2}).
$$

Because

$$
\operatorname E_P\{\psi_P(Z)\}=0,
$$

the central limit theorem gives

$$
\sqrt{n_P}\left\{\widehat I(P)-I(P)\right\}
\overset{d}{\longrightarrow}
N\{0,V(P)\},
$$

where

$$
\begin{aligned}
V(P)
&=\operatorname{Var}_P\{\psi_P(Z)\}\\
&=\operatorname E_P\left[\{\ell_P(Z)-\mu_P\}^2\right].
\end{aligned}
$$

Consequently,

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}.
$$

The bias correction in Section 4 is a fixed constant at a given sample size,
so it has the same first-order variance:

$$
\operatorname{Var}\{\widehat I_{\mathrm{BC}}(P)\}
\approx\frac{V(P)}{n_P}.
$$

## 6. The Two-Sample Standardized Statistic

Define the corresponding influence variance $V(Q)$ for the second
population. Independence of the two samples implies

$$
\operatorname{Var}(\widehat\Delta_{\mathrm{BC}})
\approx
\frac{V(P)}{n_P}+\frac{V(Q)}{n_Q}.
$$

To estimate $V(P)$, define

$$
m_{2,P}=\operatorname E_P\{\ell_P(Z)^2\}.
$$

Since $\mu_P=\operatorname E_P(\ell_P)$,

$$
V(P)=m_{2,P}-\mu_P^2.
$$

Its plug-in estimate is

$$
\begin{aligned}
\widehat V_P
&=\sum_{i,j}\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I(P)\right)^2\\
&=\sum_{i,j}\widehat p_{ij}\widehat\ell_{ij}^2
-\widehat I(P)^2.
\end{aligned}
$$

Define $\widehat V_Q$ analogously. The two estimated contributions to the
variance of the difference are

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

The estimated standard error is

$$
\widehat{\operatorname{SE}}
=\sqrt{a+b}
=\sqrt{
\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}
}.
$$

The standardized statistic is

$$
\boxed{
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\sqrt{\widehat V_P/n_P+\widehat V_Q/n_Q}}.
}
$$

If $V(P)$ and $V(Q)$ were known, a standard normal reference would follow
from the two independent asymptotic expansions. In practice, both variances
are estimated. Expanded Welch-Satterthwaite estimates the uncertainty in
those variance estimates rather than treating the denominator as known.

## 7. Deriving the Influence Function of the MI Variance

### 7.1 The target variance functional

Recall that

$$
V(P)=m_{2,P}-\mu_P^2,
$$

where

$$
m_{2,P}=\operatorname E_P\{\ell_P(Z)^2\},
\qquad
\mu_P=\operatorname E_P\{\ell_P(Z)\}.
$$

The goal is to differentiate $V(P_\varepsilon)$ along the same contamination
path used in Section 5. Define

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

This $g_P$ is the influence function of the complete MI variance functional.

### 7.2 Differentiate the second moment

Under $P_\varepsilon$,

$$
m_2(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j)^2.
$$

Differentiate using the product rule:

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}m_2(P_\varepsilon)
\right|_{\varepsilon=0}
={}&\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\ell_P(i,j)^2\\
&+\sum_{i,j}p_{ij}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)^2
\right|_{\varepsilon=0}.
\end{aligned}
$$

For the first sum,

$$
\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\ell_P(i,j)^2
=\ell_P(x,y)^2-m_{2,P}.
$$

For the second sum, the chain rule gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)^2
\right|_{\varepsilon=0}
=2\ell_P(i,j)\dot\ell_P(i,j;z).
$$

Therefore,

$$
\operatorname{IF}_{m_2,P}(x,y)
=\ell_P(x,y)^2-m_{2,P}
+2\sum_{i,j}p_{ij}\ell_P(i,j)\dot\ell_P(i,j;z).
$$

### 7.3 Evaluate the score-derivative sum

Substitute the expression for $\dot\ell_P$:

$$
\begin{aligned}
&\sum_{i,j}p_{ij}\ell_P(i,j)\dot\ell_P(i,j;z)\\
={}&\sum_{i,j}p_{ij}\ell_P(i,j)
\left[
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1
\right].
\end{aligned}
$$

Evaluate the four terms separately.

The cell term is

$$
\sum_{i,j}p_{ij}\ell_P(i,j)
\frac{\mathbf 1\{i=x,j=y\}}{p_{ij}}
=\ell_P(x,y).
$$

The row term is

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P(i,j)
\frac{\mathbf 1\{i=x\}}{p_{i+}}
&=\frac{1}{p_{x+}}\sum_j p_{xj}\ell_P(x,j)\\
&=\operatorname E_P\{\ell_P(X,Y)\mid X=x\}.
\end{aligned}
$$

Define

$$
R_P(x)
=\operatorname E_P\{\ell_P(X,Y)\mid X=x\}.
$$

The column term is

$$
\begin{aligned}
\sum_{i,j}p_{ij}\ell_P(i,j)
\frac{\mathbf 1\{j=y\}}{p_{+j}}
&=\frac{1}{p_{+y}}\sum_i p_{iy}\ell_P(i,y)\\
&=\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}.
\end{aligned}
$$

Define

$$
C_P(y)
=\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}.
$$

Finally, the constant term is

$$
\sum_{i,j}p_{ij}\ell_P(i,j)=\mu_P.
$$

Remembering the minus signs on the row and column terms,

$$
\boxed{
\sum_{i,j}p_{ij}\ell_P(i,j)\dot\ell_P(i,j;z)
=\ell_P(x,y)-R_P(x)-C_P(y)+\mu_P.
}
$$

It follows that

$$
\boxed{
\begin{aligned}
\operatorname{IF}_{m_2,P}(x,y)
={}&\ell_P(x,y)^2-m_{2,P}\\
&+2\{\ell_P(x,y)-R_P(x)-C_P(y)+\mu_P\}.
\end{aligned}
}
$$

### 7.4 Differentiate the squared mean

From Section 5,

$$
\operatorname{IF}_{\mu,P}(x,y)
=\ell_P(x,y)-\mu_P.
$$

The ordinary chain rule for $u^2$ gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\mu(P_\varepsilon)^2
\right|_{\varepsilon=0}
=2\mu_P\operatorname{IF}_{\mu,P}(x,y).
$$

Therefore,

$$
\boxed{
\operatorname{IF}_{\mu^2,P}(x,y)
=2\mu_P\{\ell_P(x,y)-\mu_P\}.
}
$$

### 7.5 Combine the derivatives

Because

$$
V(P)=m_{2,P}-\mu_P^2,
$$

linearity of differentiation gives

$$
g_P(x,y)
=\operatorname{IF}_{m_2,P}(x,y)
-\operatorname{IF}_{\mu^2,P}(x,y).
$$

Substituting the two expressions above yields

$$
\boxed{
\begin{aligned}
g_P(x,y)={}&
\ell_P(x,y)^2-m_{2,P}\\
&+2\{\ell_P(x,y)-R_P(x)-C_P(y)+\mu_P\}\\
&-2\mu_P\{\ell_P(x,y)-\mu_P\}.
\end{aligned}
}
$$

This is the complete variance-influence formula used by the expanded method.
No local score is treated as fixed: the middle line accounts for changes to
the joint cell, its row marginal, its column marginal, and the overall MI.

### 7.6 Verify that the influence function has mean zero

An influence function should be centred under its defining distribution. We
can verify this directly.

For the first line,

$$
\operatorname E_P\{\ell_P(Z)^2-m_{2,P}\}=m_{2,P}-m_{2,P}=0.
$$

For the middle line, the law of iterated expectations gives

$$
\operatorname E_P\{R_P(X)\}
=\operatorname E_P[\operatorname E_P\{\ell_P(Z)\mid X\}]
=\mu_P
$$

and

$$
\operatorname E_P\{C_P(Y)\}=\mu_P.
$$

Hence,

$$
\begin{aligned}
\operatorname E_P\{\ell_P(Z)-R_P(X)-C_P(Y)+\mu_P\}
&=\mu_P-\mu_P-\mu_P+\mu_P\\
&=0.
\end{aligned}
$$

For the final line,

$$
\operatorname E_P[-2\mu_P\{\ell_P(Z)-\mu_P\}]
=-2\mu_P(\mu_P-\mu_P)
=0.
$$

Combining the three results,

$$
\boxed{
\operatorname E_P\{g_P(X,Y)\}=0.
}
$$

## 8. Sampling Uncertainty of the Estimated MI Variance

The plug-in variance estimator can be written as the empirical functional

$$
\widehat V_P=V(\widehat P).
$$

Because $g_P$ is the influence function of $V$, its first-order expansion is

$$
V(\widehat P)-V(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
+o_p(n_P^{-1/2}).
$$

Define

$$
\boxed{
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\}.
}
$$

Since $\operatorname E_P(g_P)=0$, this can also be written as

$$
\tau_P^2
=\operatorname E_P\{g_P(X,Y)^2\}.
$$

Taking the variance of the leading term in the expansion gives

$$
\begin{aligned}
\operatorname{Var}\{\widehat V_P\}
&\approx
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
\right\}\\
&=\frac{1}{n_P^2}
\sum_{k=1}^{n_P}\operatorname{Var}_P\{g_P(Z_k^{(P)})\}\\
&=\frac{1}{n_P^2}(n_P\tau_P^2)\\
&=\boxed{\frac{\tau_P^2}{n_P}}.
\end{aligned}
$$

The covariance terms vanish because observations within the sample are
independent.

This result answers the key question: $\tau_P^2/n_P$ is the first-order
sampling variance of the estimated MI influence variance $\widehat V_P$.

## 9. Estimate the Variance-Influence Quantities

All population quantities are replaced by their empirical versions. For the
first table, calculate

$$
\widehat\mu_P
=\sum_{i,j}\widehat p_{ij}\widehat\ell_{ij},
$$

$$
\widehat m_{2,P}
=\sum_{i,j}\widehat p_{ij}\widehat\ell_{ij}^2,
$$

and

$$
\widehat V_P
=\widehat m_{2,P}-\widehat\mu_P^2.
$$

For each nonempty row and column, calculate

$$
\widehat R_P(i)
=\frac{\sum_j\widehat p_{ij}\widehat\ell_{ij}}
{\widehat p_{i+}}
$$

and

$$
\widehat C_P(j)
=\frac{\sum_i\widehat p_{ij}\widehat\ell_{ij}}
{\widehat p_{+j}}.
$$

For every cell, evaluate

$$
\begin{aligned}
\widehat g_P(i,j)={}&
\widehat\ell_{ij}^2-\widehat m_{2,P}\\
&+2\{\widehat\ell_{ij}-\widehat R_P(i)
-\widehat C_P(j)+\widehat\mu_P\}\\
&-2\widehat\mu_P
\{\widehat\ell_{ij}-\widehat\mu_P\}.
\end{aligned}
$$

In exact arithmetic the weighted mean of $\widehat g_P$ is zero. The
implementation nevertheless centres it explicitly for numerical stability:

$$
\overline g_P
=\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j).
$$

Then

$$
\boxed{
\widehat\tau_P^2
=\sum_{i,j}\widehat p_{ij}
\{\widehat g_P(i,j)-\overline g_P\}^2.
}
$$

Repeat the complete calculation for table $Q$ to obtain
$\widehat V_Q$ and $\widehat\tau_Q^2$.

## 10. Satterthwaite Moment Matching for One Variance Component

### 10.1 The scaled chi-squared approximation

A chi-squared random variable $U\sim\chi^2_\nu$ has

$$
\operatorname E(U)=\nu,
\qquad
\operatorname{Var}(U)=2\nu.
$$

Therefore,

$$
Y=m\frac{U}{\nu}
$$

has

$$
\operatorname E(Y)
=\frac{m}{\nu}\operatorname E(U)
=m
$$

and

$$
\begin{aligned}
\operatorname{Var}(Y)
&=\frac{m^2}{\nu^2}\operatorname{Var}(U)\\
&=\frac{m^2}{\nu^2}(2\nu)\\
&=\frac{2m^2}{\nu}.
\end{aligned}
$$

Solving the last equation for $\nu$ gives the general Satterthwaite
moment-matching rule

$$
\boxed{
\nu=\frac{2m^2}{\operatorname{Var}(Y)}.
}
$$

### 10.2 Apply the rule to $\widehat V_P$

Approximate the positive variance estimator by

$$
\widehat V_P
\mathrel{\dot\sim}
V(P)\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

The scaled chi-squared approximation has

$$
\operatorname E(\widehat V_P)\approx V(P)
$$

and

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{2V(P)^2}{\nu_{V,P}}.
$$

Section 8 independently derived

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Equating the two approximations gives

$$
\frac{2V(P)^2}{\nu_{V,P}}
=\frac{\tau_P^2}{n_P}.
$$

Multiply both sides by $n_P\nu_{V,P}$:

$$
2n_PV(P)^2
=\nu_{V,P}\tau_P^2.
$$

Divide by $\tau_P^2$:

$$
\boxed{
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
}
$$

The empirical component degrees of freedom are therefore

$$
\boxed{
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2}.
}
$$

Likewise,

$$
\boxed{
\widehat\nu_{V,Q}
=\frac{2n_Q\widehat V_Q^2}{\widehat\tau_Q^2}.
}
$$

### 10.3 Why dividing by sample size does not change component degrees of freedom

The denominator of $T$ uses

$$
A=\frac{\widehat V_P}{n_P},
$$

not $\widehat V_P$ itself. From the scaled chi-squared approximation,

$$
A
\mathrel{\dot\sim}
\frac{V(P)}{n_P}
\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

Only the scale has changed. The chi-squared degrees of freedom remain
$\nu_{V,P}$. The same argument applies to

$$
B=\frac{\widehat V_Q}{n_Q}.
$$

## 11. Combine the Two Variance Components

The estimated squared standard error is

$$
S^2=A+B
=\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}.
$$

Let the approximate means of the two components be

$$
a_0=\frac{V(P)}{n_P},
\qquad
b_0=\frac{V(Q)}{n_Q}.
$$

Under the component approximations,

$$
\operatorname{Var}(A)
\approx\frac{2a_0^2}{\nu_{V,P}}
$$

and

$$
\operatorname{Var}(B)
\approx\frac{2b_0^2}{\nu_{V,Q}}.
$$

Because the $P$ and $Q$ samples are independent, $A$ and $B$ are
independent. Thus,

$$
\begin{aligned}
\operatorname{Var}(S^2)
&=\operatorname{Var}(A+B)\\
&=\operatorname{Var}(A)+\operatorname{Var}(B)\\
&\approx
\frac{2a_0^2}{\nu_{V,P}}
+\frac{2b_0^2}{\nu_{V,Q}}.
\end{aligned}
$$

Now approximate the sum by one scaled chi-squared variable:

$$
S^2
\mathrel{\dot\sim}
(a_0+b_0)\frac{\chi^2_{\nu}}{\nu}.
$$

This approximation has variance

$$
\operatorname{Var}(S^2)
\approx\frac{2(a_0+b_0)^2}{\nu}.
$$

Match the two variance expressions:

$$
\frac{2(a_0+b_0)^2}{\nu}
=
\frac{2a_0^2}{\nu_{V,P}}
+\frac{2b_0^2}{\nu_{V,Q}}.
$$

Cancel the factor of two:

$$
\frac{(a_0+b_0)^2}{\nu}
=
\frac{a_0^2}{\nu_{V,P}}
+\frac{b_0^2}{\nu_{V,Q}}.
$$

Solve for $\nu$:

$$
\nu
=\frac{(a_0+b_0)^2}
{a_0^2/\nu_{V,P}+b_0^2/\nu_{V,Q}}.
$$

Finally, replace the population components and component degrees of freedom
by their estimates:

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

The expanded Welch-Satterthwaite degrees of freedom are

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}
+b^2/\widehat\nu_{V,Q}}.
}
$$

## 12. The Final Reference Distribution and P-Value

The expanded method compares the observed statistic

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}{\sqrt{a+b}}
$$

with a Student distribution having
$\widehat\nu_{\mathrm{expanded}}$ degrees of freedom. The two-sided p-value is

$$
\boxed{
p_{\mathrm{expanded}}
=2\left[1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}
(|T|)\right],
}
$$

where $F_{t_\nu}$ is the cumulative distribution function of a Student
random variable with $\nu$ degrees of freedom.

At significance level $\alpha$, reject $H_0:I(P)=I(Q)$ when

$$
p_{\mathrm{expanded}}<\alpha.
$$

Equivalently, reject when

$$
|T|>
t_{1-\alpha/2,\widehat\nu_{\mathrm{expanded}}}.
$$

## 13. Complete Calculation from Two Count Tables

For clarity, the entire procedure is collected here without omitting any
intermediate quantity.

### Step 1: Convert counts to probabilities

For each group $G\in\{P,Q\}$,

$$
\widehat p^{(G)}_{ij}=\frac{N^{(G)}_{ij}}{n_G}.
$$

### Step 2: Calculate row and column marginals

$$
\widehat p^{(G)}_{i+}=\sum_j\widehat p^{(G)}_{ij},
\qquad
\widehat p^{(G)}_{+j}=\sum_i\widehat p^{(G)}_{ij}.
$$

### Step 3: Calculate local-information scores

$$
\widehat\ell^{(G)}_{ij}
=\log\left(
\frac{\widehat p^{(G)}_{ij}}
{\widehat p^{(G)}_{i+}\widehat p^{(G)}_{+j}}
\right).
$$

### Step 4: Calculate plug-in MI

$$
\widehat I(G)
=\sum_{i,j}\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij}.
$$

### Step 5: Correct the leading bias

$$
\widehat I_{\mathrm{BC}}(G)
=\widehat I(G)-\frac{(r-1)(c-1)}{2n_G}.
$$

### Step 6: Form the estimated difference

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

### Step 7: Calculate the first two score moments

For each group,

$$
\widehat\mu_G
=\sum_{i,j}\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij},
$$

$$
\widehat m_{2,G}
=\sum_{i,j}\widehat p^{(G)}_{ij}
\left(\widehat\ell^{(G)}_{ij}\right)^2,
$$

and

$$
\widehat V_G
=\widehat m_{2,G}-\widehat\mu_G^2.
$$

### Step 8: Calculate conditional score means

$$
\widehat R_G(i)
=\frac{\sum_j\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij}}
{\widehat p^{(G)}_{i+}},
$$

$$
\widehat C_G(j)
=\frac{\sum_i\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij}}
{\widehat p^{(G)}_{+j}}.
$$

### Step 9: Calculate the variance influence in each cell

$$
\begin{aligned}
\widehat g_G(i,j)={}&
\left(\widehat\ell^{(G)}_{ij}\right)^2
-\widehat m_{2,G}\\
&+2\left\{
\widehat\ell^{(G)}_{ij}
-\widehat R_G(i)-\widehat C_G(j)+\widehat\mu_G
\right\}\\
&-2\widehat\mu_G
\left\{\widehat\ell^{(G)}_{ij}-\widehat\mu_G\right\}.
\end{aligned}
$$

### Step 10: Calculate variance-influence variability

$$
\overline g_G
=\sum_{i,j}\widehat p^{(G)}_{ij}\widehat g_G(i,j),
$$

$$
\widehat\tau_G^2
=\sum_{i,j}\widehat p^{(G)}_{ij}
\left\{\widehat g_G(i,j)-\overline g_G\right\}^2.
$$

### Step 11: Calculate component degrees of freedom

$$
\widehat\nu_{V,G}
=\frac{2n_G\widehat V_G^2}{\widehat\tau_G^2}.
$$

### Step 12: Calculate the two standard-error components

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

### Step 13: Calculate the standard error and statistic

$$
\widehat{\operatorname{SE}}=\sqrt{a+b},
$$

$$
T=\frac{\widehat\Delta_{\mathrm{BC}}}
{\widehat{\operatorname{SE}}}.
$$

### Step 14: Combine the component degrees of freedom

$$
\widehat\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}
+b^2/\widehat\nu_{V,Q}}.
$$

### Step 15: Calculate the two-sided p-value

$$
p_{\mathrm{expanded}}
=2\left[1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}(|T|)\right].
$$

## 14. Interpretation of the Effective Degrees of Freedom

The component formula is

$$
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2}.
$$

Its numerator contains sample size and the squared magnitude of the MI
variance. Its denominator measures how strongly that estimated variance
changes when probability mass moves among cells.

If the cell sensitivities $\widehat g_P(i,j)$ are similar, then
$\widehat\tau_P^2$ is small. The estimated variance is relatively stable,
the component degrees of freedom are large, and the Student reference is
close to a normal reference.

If a small number of cells have unusually large sensitivities, then
$\widehat\tau_P^2$ is large. The estimated variance is less stable, the
component degrees of freedom are smaller, and the Student reference develops
heavier tails. For a fixed observed $|T|$, heavier tails produce a larger,
more cautious p-value.

This mechanism is table-dependent. Unlike the simple assignment
$\nu_{V,P}=n_P-1$, it can respond to skewness, sparse empirical support, and
unequal influence among cells.

## 15. Relationship to Ordinary Welch-Satterthwaite

An ordinary Welch test uses sample variances whose exact scaled chi-squared
distributions are available under normal sampling. A conventional component
with sample size $n_P$ is assigned $n_P-1$ degrees of freedom, leading to

$$
\widehat\nu_{\mathrm{simple}}
=\frac{(a+b)^2}
{a^2/(n_P-1)+b^2/(n_Q-1)}.
$$

Expanded Welch keeps the same Satterthwaite combination but replaces the
ordinary component degrees of freedom with quantities derived from the MI
variance functional:

$$
n_P-1
\quad\longrightarrow\quad
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2},
$$

and similarly for $Q$.

Thus, the expansion is not a different standard error and not a second bias
correction. It is an MI-specific calculation of how uncertain each estimated
variance component is.

## 16. Regularity Conditions and Limits of the Derivation

### 16.1 Fixed finite alphabet

The asymptotic expansions assume that $r$ and $c$ remain fixed as the sample
sizes increase. The derivation does not establish validity when the alphabet
grows with sample size.

### 16.2 Positive population support

The derivatives of $\log p_{ij}$ require positive population probabilities.
The mathematical derivation therefore applies to cells in the fixed positive
support of the population. Structural-zero models require a separate support
definition and a corresponding bias dimension.

In computation, an observed zero-count cell contributes zero to
probability-weighted sums under the convention $0\log 0=0$. This keeps the
plug-in calculation finite, but it does not remove the underlying smoothness
assumption. Very sparse tables remain a finite-sample stress regime rather
than a setting in which the approximation becomes exact.

### 16.3 Nondegenerate first-order MI variance

At exact independence,

$$
p_{ij}=p_{i+}p_{+j},
$$

so

$$
\ell_P(i,j)=0,
\qquad
\psi_P(i,j)=0,
\qquad
V(P)=0.
$$

The first-order normal approximation then degenerates. The statistic in this
chapter requires a positive combined first-order variance and is intended for
regular differential-MI comparisons away from this degeneracy. A test whose
null is independence requires second-order theory and is not supplied by this
derivation.

### 16.4 Independent samples

The variance addition and the Satterthwaite combination use independence of
the $P$ and $Q$ samples. Paired, clustered, repeated-measures, or otherwise
dependent samples require covariance terms and a different derivation.

### 16.5 Fixed table dimensions in the bias correction

The implemented leading correction uses

$$
d=(r-1)(c-1)
$$

from the configured table dimensions. If categories are selected or removed
after observing the data, the nominal bias calculation and the sampling
analysis can change.

### 16.6 The Student reference is an approximation

The derivation establishes first-order moments for the variance estimator and
uses Satterthwaite moment matching. It does not prove that
$\widehat V_P$ is exactly scaled chi-squared. It also does not make the MI
numerator exactly independent of its estimated denominator.

Consequently,

$$
T\not\equiv t_{\widehat\nu_{\mathrm{expanded}}}
$$

as an exact finite-sample identity. The Student distribution is a calibrated
working reference motivated by the derived variance uncertainty. Its
finite-sample accuracy must be established empirically.

### 16.7 Numerical validity conditions

The calculation requires finite positive values for

$$
\widehat V_P+\widehat V_Q,
\qquad
\widehat\tau_P^2,
\qquad
\widehat\tau_Q^2,
$$

and for the resulting component and combined degrees of freedom. If these
conditions fail, the implementation reports the expanded result as invalid
rather than manufacturing a p-value.

## 17. Computational Complexity

Each quantity is obtained by a fixed number of operations over an $r\times c$
table:

- cell probabilities and local scores require $O(rc)$ work;
- row and column reductions require $O(rc)$ work;
- $\widehat V$, $\widehat g$, and $\widehat\tau^2$ require $O(rc)$ work;
- combining the two components requires constant work.

Therefore, the complete two-table method has

$$
\boxed{
\text{time complexity }O(rc),
\qquad
\text{memory complexity }O(rc).
}
$$

No permutations, bootstrap samples, or Monte Carlo tables are required.

## 18. Correspondence with the Implementation

The implementation is in
[`src/welch_differential_mi/welch.py`](../src/welch_differential_mi/welch.py).
Its main quantities correspond to the derivation as follows.

| Mathematical quantity | Implementation name |
| --- | --- |
| $\widehat I$ | `plugin_mi(...)` |
| $d$ | `mi_df` |
| $\widehat\Delta_{\mathrm{BC}}$ | `delta` |
| $\widehat V_P,\widehat V_Q$ | `variance_p`, `variance_q` |
| $a,b$ | `component_p`, `component_q` |
| $T$ | `statistic` |
| $\widehat R(i)$ | `row_score_mean` |
| $\widehat C(j)$ | `column_score_mean` |
| $\widehat g(i,j)$ | `variance_influence` |
| $\widehat\tau^2$ | `influence_variance` inside `_variance_influence_component_df` |
| $\widehat\nu_{V,P},\widehat\nu_{V,Q}$ | `expanded_df_p`, `expanded_df_q` |
| $\widehat\nu_{\mathrm{expanded}}$ | `expanded_df` |
| $p_{\mathrm{expanded}}$ | `expanded_p` |

## 19. Derivation in One Chain

The complete mathematical chain is

$$
P
\longrightarrow
\ell_P
\longrightarrow
I(P)=\mu_P
\longrightarrow
\psi_P=\ell_P-\mu_P
\longrightarrow
V(P)=\operatorname{Var}_P(\psi_P)
$$

followed by

$$
V(P)
\longrightarrow
g_P=\operatorname{IF}_{V,P}
\longrightarrow
\tau_P^2=\operatorname{Var}_P(g_P)
\longrightarrow
\nu_{V,P}=\frac{2n_PV(P)^2}{\tau_P^2}.
$$

After repeating the chain for $Q$,

$$
(\nu_{V,P},\nu_{V,Q})
\longrightarrow
\nu_{\mathrm{expanded}}
\longrightarrow
t_{\nu_{\mathrm{expanded}}}
\longrightarrow
p_{\mathrm{expanded}}.
$$

The method therefore uses one influence function to estimate the sampling
variance of MI and a second influence function to estimate the sampling
uncertainty of that variance. Satterthwaite moment matching converts the
second uncertainty calculation into the effective degrees of freedom used to
interpret the standardized MI difference.

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
