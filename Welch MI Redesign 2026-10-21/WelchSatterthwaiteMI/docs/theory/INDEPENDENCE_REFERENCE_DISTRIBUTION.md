# Why a Reference Distribution Cannot Turn Expanded Welch into an Independence Test

## Purpose

Let $P$ be the joint distribution of two discrete variables $X$ and $Y$.
The question is whether we can construct a reference distribution $Q$ and
use the Expanded Welch--Satterthwaite test

$$
H_0:I(P)=I(Q)
\qquad\text{against}\qquad
H_1:I(P)>I(Q)
$$

as a test of whether $X$ and $Y$ are independent under $P$.

This document shows that this cannot produce a regular Expanded Welch
independence test without replacing its first-order approximation. The
obstacle is not the choice of $Q$; it is the behaviour of the MI estimator at
independence.

Natural logarithms are used throughout, so MI is measured in nats.

## 1. What the Reference Distribution Would Need to Do

Mutual information satisfies

$$
\begin{aligned}
I(P)&\geq 0,\\
I(P)=0
&\quad\Longleftrightarrow\quad
X\ \text{and}\ Y\ \text{are independent under }P.
\end{aligned}
$$

For the equal-MI null to represent independence, the reference must therefore
have

$$
\boxed{I(Q)=0.}
$$

The desired null is consequently

$$
\boxed{I(P)=I(Q)=0.}
$$

Expanded Welch also requires two independent samples and a nonzero
first-order sampling variance for each MI estimator. The next section shows
that the desired null necessarily violates the variance requirement.

## 2. Why Expanded Welch Fails at Independence

### 2.1 Zero MI gives zero first-order variance

For any joint distribution $R$, define its pointwise mutual information by

$$
\ell_R(x,y)
=
\log\left(\frac{r(x,y)}{r(x)r(y)}\right),
$$

and define the first-order MI variance by

$$
V(R)=\operatorname{Var}_R\{\ell_R(X,Y)\}.
$$

If $I(R)=0$, then $R$ is independent. Hence

$$
r(x,y)=r(x)r(y)
\quad\Longrightarrow\quad
\ell_R(x,y)=\log(1)=0
$$

in every cell with positive probability. It follows that

$$
\boxed{I(R)=0\quad\Longrightarrow\quad V(R)=0.}
$$

Applying this result to the desired null gives

$$
I(P)=I(Q)=0
\quad\Longrightarrow\quad
V(P)=V(Q)=0.
$$

For population $P$, a first-order Taylor expansion of MI as a function of the
cell probabilities gives

$$
\widehat I(P)-I(P)
\approx
\frac{1}{n_P}\sum_{a=1}^{n_P}
\left\{\ell_P(X_a,Y_a)-I(P)\right\}.
$$

At independence, every term inside the sum is

$$
\ell_P(X_a,Y_a)-I(P)=0-0=0.
$$

This first-order Taylor approximation therefore contains no random variation,
and its variance is

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}=0.
$$

The same result holds for $Q$. Expanded Welch places these two variance
estimates in the denominator of

$$
T
=
\frac{
\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)
}{
\sqrt{\widehat V(P)/n_P+\widehat V(Q)/n_Q}
}.
$$

A finite table can still give nonzero $\widehat I(P)$ and $\widehat V(P)$,
but that variation is absent from the first-order Taylor approximation above.
It comes from the second-order Taylor term derived next. The Satterthwaite
correction only changes the degrees of freedom used after forming $T$; it
cannot supply the missing second-order variation.

### 2.2 Why the leading term is quadratic

At independence, MI is at its minimum value of zero. The usual normal
approximation is built from a first-order Taylor expansion and requires a
nonzero slope at this point, but that slope vanishes. The remaining change in
MI is determined by the second-order Taylor term, which describes the local
curvature of the function.

Define the observed departure from independence in cell $(x,y)$ by

$$
\delta(x,y)=\widehat p(x,y)-\widehat p(x)\widehat p(y).
$$

Substituting
$\widehat p(x,y)=\widehat p(x)\widehat p(y)+\delta(x,y)$ into the complete
plug-in MI expression and applying a second-order Taylor approximation gives

$$
\widehat I(X;Y)
\approx
\sum_{x,y}\delta(x,y)
+
\frac{1}{2}\sum_{x,y}
\frac{\delta(x,y)^2}{\widehat p(x)\widehat p(y)}.
$$

The **first-order contribution** is the sum of the signed cell departures:

$$
\sum_{x,y}\delta(x,y)=1-1=0.
$$

The **second-order contribution** is the probability-weighted sum of their
squares:

$$
\frac{1}{2}\sum_{x,y}
\frac{\delta(x,y)^2}{\widehat p(x)\widehat p(y)}.
$$

Only the second-order contribution remains, so

$$
\boxed{
\widehat I(X;Y)
\approx
\frac{1}{2}\sum_{x,y}
\frac{\delta(x,y)^2}{\widehat p(x)\widehat p(y)}.
}
$$

Each $\delta(x,y)$ is a random cell-probability error. Such errors typically
shrink like $1/\sqrt N$ as the sample size grows. In the boxed equation these
errors are squared, so their contribution to MI shrinks like

$$
\left(\frac{1}{\sqrt N}\right)^2=\frac{1}{N}.
$$

Therefore, $\widehat I(X;Y)$ shrinks like $1/N$. Multiplying it by $2N$
cancels this shrinkage. If $O_{xy}$ is the observed count and $E_{xy}$ is the
count expected under independence, the boxed expression becomes

$$
2N\widehat I(X;Y)
\approx
\sum_{x,y}\frac{(O_{xy}-E_{xy})^2}{E_{xy}}.
$$

This is Pearson's chi-squared statistic: each cell's count error is squared,
standardised by its expected count, and then added across the table. Under the
usual large-sample conditions, it has the
$\chi^2_{(r-1)(c-1)}$ limit.

The first-order Taylor contribution shown above is
$\sum_{x,y}\delta(x,y)$. These errors retain their signs, so positive and
negative cell departures cancel and the sum is zero. Expanded Welch relies on
this type of first-order linear behaviour. The chi-squared statistic instead
squares the departures before adding them, so they cannot cancel. Changing
the Student degrees of freedom adjusts the reference distribution for the
first-order statistic, but it does not turn the cancelled linear sum into this
sum of squared errors.

### 2.3 Changing the reference does not avoid the problem

Changing $Q$ does not remove the conflict:

- If $I(Q)>0$, then $I(P)=I(Q)$ tests whether $P$ has that positive MI,
  not whether $P$ is independent.
- If $Q$ is calculated from the same observations as $P$, then the two
  estimates are not independent samples, which also violates the Welch
  derivation.

**Therefore, no construction of $Q$ can make the unmodified, first-order
equal-MI Expanded Welch test a regular test of independence.** A valid method
at this null must instead model the second-order behaviour or obtain the null
distribution by resampling.

## 3. What the Natural Construction Produces

The most natural reference keeps the margins of $P$ but removes its
association:

$$
\boxed{q(x,y)=p(x)p(y).}
$$

This distribution is independent, so $I(Q)=0$. Its divergence from $P$ is

$$
\begin{aligned}
D_{\mathrm{KL}}(P\|Q)
&=\sum_{x,y}p(x,y)\log\left(\frac{p(x,y)}{q(x,y)}\right)\\
&=\sum_{x,y}p(x,y)
\log\left(\frac{p(x,y)}{p(x)p(y)}\right)\\
&=I(P).
\end{aligned}
$$

For an observed table of size $N$, let

$$
O_{xy}=N\widehat p(x,y)
\qquad\text{and}\qquad
E_{xy}=N\widehat p(x)\widehat p(y),
$$

be the observed and independence-expected counts in cell $(x,y)$. The
empirical comparison becomes

$$
\begin{aligned}
2N D_{\mathrm{KL}}(\widehat P\|\widehat Q)
&=2\sum_{x,y}O_{xy}\log\left(\frac{O_{xy}}{E_{xy}}\right)\\
&=2N\widehat I(P).
\end{aligned}
$$

The quantity

$$
G=2\sum_{x,y}O_{xy}\log\left(\frac{O_{xy}}{E_{xy}}\right)
$$

is the classical likelihood-ratio, or $G$-test, statistic. By the standard
large-sample result for this test,

$$
G\xrightarrow{d}\chi^2_{(r-1)(c-1)}
$$

under independence. Thus the natural deterministic construction of $Q$
returns the standard $G$-test; it does not turn Expanded Welch into that
test.

## 4. Available Tests After Constructing $Q$

Once $Q$ represents independence, the remaining choice is how to obtain the
null distribution of $G$:

| Procedure | Result |
| --- | --- |
| Compare $G$ with $\chi^2_{(r-1)(c-1)}$ | Classical analytic $G$-test |
| Repeatedly shuffle $Y$ relative to $X$ | Permutation test |
| Repeatedly simulate tables from $\widehat P_X\widehat P_Y$ | Parametric bootstrap |

A single sampled table from $Q$ is not enough to estimate a null
distribution. Repeated sampling gives a resampling test, while the
deterministic construction gives the analytic $G$-test.

## 5. Conclusion

The proposed reference distribution is mathematically valid, but it cannot
make Expanded Welch a test of independence. Any equal-MI construction that
represents independence forces both population MI values to zero, where the
first-order variances used by Expanded Welch also vanish.

The same-margin construction $Q=P_XP_Y$ instead recovers the classical
$G$-test. Improving inference for sparse tables would therefore require a
better finite-sample treatment of $G$'s second-order null distribution, not
an Expanded Welch degrees-of-freedom correction.
