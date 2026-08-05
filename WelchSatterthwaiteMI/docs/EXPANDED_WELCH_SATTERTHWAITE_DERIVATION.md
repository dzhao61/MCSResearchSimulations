# A Direct Derivation of the Expanded Welch-Satterthwaite MI Test

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

Its immediate inspiration is Hutcheson's test for comparing two Shannon
diversities. The present construction carries that Welch-style idea into a
mutual-information setting, where the quantity being compared depends on a
joint table and both of its margins.

The important difference is that mutual information is a nonlinear function
of a complete joint probability table. Its estimated variance therefore
changes when a cell, row margin, or column margin changes. The expanded method
measures this table-specific instability and converts it into effective
degrees of freedom.

The derivation follows one continuous chain:

$$
\ell_P
\longrightarrow
\psi_P
\longrightarrow
V(P)
\longrightarrow
g_P
\longrightarrow
\tau_P^2
\longrightarrow
\nu_{V,P}.
$$

Each quantity is introduced only when it is needed. The aim is to explain
where the method comes from and what each step means, rather than to present
every equivalent algebraic form.

The derivation below is written for natural logarithms, so MI is measured in
nats.

## 1. Statistical Setting

The comparison is based on two contingency tables obtained from separate
populations. Each observation records one value of $X$ and one value of $Y$,
so a population is described by a joint distribution over the common
$r\times c$ alphabet. Using the same alphabet for both groups ensures that
the two MI values describe the same variables on the same category space.

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

The independent and identically distributed (iid) assumption allows the
observations within each group to be treated as repeated draws from one fixed
distribution. Independence between the two groups will later allow their
sampling variances to be added without a covariance term.

Write the population cell probabilities as

$$
p_{ij}=\Pr_P(X=i,Y=j),
\qquad
q_{ij}=\Pr_Q(X=i,Y=j).
$$

MI compares each joint probability with the probability expected from its
row and column margins under independence. For population $P$, these margins
are

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

For cell $(i,j)$, independence would assign probability $p_{i+}p_{+j}$.
The ratio $p_{ij}/(p_{i+}p_{+j})$ therefore measures how much more or less
often the cell occurs than independence predicts. Taking its logarithm gives
the local-information score

$$
\ell_P(i,j)
=\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

The score is positive for a cell occurring more often than the independence
baseline, negative for a cell occurring less often, and zero when the two
probabilities agree. Mutual information averages these cell-level scores
using the actual joint probabilities as weights:

$$
\begin{aligned}
I(P)
&=\sum_{i=1}^{r}\sum_{j=1}^{c}
p_{ij}\log\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right)\\
&=\operatorname E_P\{\ell_P(X,Y)\}.
\end{aligned}
$$

For compact notation, set

$$
\mu_P=I(P).
$$

Writing MI as $I(P)$ emphasizes that it is a
functional: its input is the complete probability table $P$, rather than a
single scalar parameter. The subscript on $\ell_P$ is equally important.
If $P$ changes, the joint probability, both relevant margins, and therefore
every affected local score change as well. This dependence is the reason the
later derivative must account for more than the perturbed cell alone.

## 3. Plug-In Estimation

The population probabilities are unknown, but the table counts provide
their empirical proportions. The plug-in principle estimates a functional
by replacing its unknown distribution with the empirical distribution. For
MI, this means evaluating exactly the same formula using observed relative
frequencies.

Let $N_{ij}^{(P)}$ be the observed count in cell $(i,j)$ of the first table.
Then

$$
n_P=\sum_{i=1}^{r}\sum_{j=1}^{c}N_{ij}^{(P)},
\qquad
\widehat p_{ij}=\frac{N_{ij}^{(P)}}{n_P}.
$$

The row and column margins must be recomputed from the same empirical table,
because they form the independence baseline for the empirical joint
probabilities:

$$
\widehat p_{i+}=\sum_{j=1}^{c}\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_{i=1}^{r}\widehat p_{ij}.
$$

The resulting empirical local scores are

$$
\widehat\ell_{ij}
=\log\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

Their probability-weighted average is the plug-in MI estimator:

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

MI is nonlinear in the cell probabilities. Replacing population
probabilities by noisy empirical proportions therefore introduces
finite-sample bias. For discrete plug-in MI, the leading bias is upward: random
table fluctuations create apparent dependence even when the underlying
association is weaker. Correcting this leading term improves the centre of
the estimated MI difference before its sampling variability is assessed.

### 4.1 Bias of plug-in entropy

The MI bias is most directly obtained from the standard plug-in entropy bias,
because MI is a sum and difference of three entropies. For a discrete
variable with $k$ positive-probability categories, the leading bias of the
plug-in entropy estimator is

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

The factor $(r-1)(c-1)$ is also the number of free association directions in
an $r\times c$ table after the row and column margins are accounted for. To
keep later expressions compact, define

$$
d=(r-1)(c-1).
$$

### 4.2 Bias-corrected MI difference

Each group is corrected using its own sample size, because the leading bias
is larger for the smaller sample. The corrected estimators are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P}
$$

and

$$
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The parameter of interest is the signed contrast $I(P)-I(Q)$, so its estimate
is formed by subtracting the two corrected MI values:

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

The standard error requires the sampling variance of $\widehat I$. Because
MI is a nonlinear function of the whole table, this variance is obtained by
first measuring how a small change in the distribution changes MI. That
first-order sensitivity is the influence function.

### 5.1 A probability-preserving cell perturbation

Changing one cell probability while leaving every other probability fixed
would make the table sum to something other than one. A valid derivative on
the probability simplex must preserve total probability. Fixing a cell
$z=(x,y)$, the path

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_z,
$$

does so by shrinking the original table by the factor $1-\varepsilon$ and
placing the released mass on cell $z$. Here $\delta_z$ places probability one
on $z$. At $\varepsilon=0$ the distribution is $P$; increasing
$\varepsilon$ moves probability toward $(x,y)$ while the table continues to
sum to one.

For an arbitrary cell $(i,j)$,

$$
p_{ij}(\varepsilon)
=(1-\varepsilon)p_{ij}
+\varepsilon\mathbf 1\{i=x,j=y\}.
$$

Its derivative records the instantaneous change in each cell:

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{i=x,j=y\}-p_{ij}.
$$

The perturbation also changes the margins used inside MI. Summing over
columns gives the perturbed row probability

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

The column margin changes in the same way:

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{+j}(\varepsilon)
\right|_{\varepsilon=0}
=\mathbf 1\{j=y\}-p_{+j}.
$$

### 5.2 Differentiate the local-information score

The local score contains one joint probability and two marginal
probabilities. All three may change along the perturbation path, so each term
must be differentiated. Under $P_\varepsilon$,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

The required logarithmic derivative is

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

Combining the joint, row, and column derivatives with their original signs
gives

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

The four terms have a direct interpretation. The first records whether the
target cell is $(i,j)$; the next two record whether the target lies in row
$i$ or column $j$; and the final $+1$ is the normalization effect created by
shrinking the original distribution.

### 5.3 Differentiate MI directly

The contamination path converts the effect of one cell into an ordinary
derivative with respect to $\varepsilon$. This sensitivity will become the
contribution of one observation to the sampling error of $\widehat I$.

Under the perturbed distribution,

$$
I(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\ell_{P_\varepsilon}(i,j).
$$

Both parts of each summand change with $\varepsilon$:

- $p_{ij}(\varepsilon)$ changes because probability mass is being moved;
- $\ell_{P_\varepsilon}(i,j)$ changes because the cell, row, and column
  probabilities in its logarithm change.

The product rule must therefore include both effects:

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
={}&
\sum_{i,j}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}p_{ij}(\varepsilon)
\right|_{\varepsilon=0}
\ell_P(i,j)\\
&+
\sum_{i,j}p_{ij}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}.
\end{aligned}
$$

Using the notation already derived, this becomes

$$
\begin{aligned}
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}
={}&
\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\ell_P(i,j)\\
&+\sum_{i,j}p_{ij}\dot\ell_P(i,j;z).
\end{aligned}
$$

The first sum measures the direct effect of moving probability toward cell
$(x,y)$:

$$
\begin{aligned}
\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\ell_P(i,j)
&=\ell_P(x,y)-\sum_{i,j}p_{ij}\ell_P(i,j)\\
&=\ell_P(x,y)-\mu_P.
\end{aligned}
$$

The second sum measures the indirect effect of changing all affected local
scores. Using the score derivative from Section 5.2 gives

$$
\begin{aligned}
\sum_{i,j}p_{ij}\dot\ell_P(i,j;z)
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

The indirect effects cancel exactly after averaging over the table. The
local scores change, but their total first-order contribution to the MI
average is zero. The remaining effect is therefore the target cell's score
relative to the population-average score. This derivative is the MI
influence function, denoted by $\psi_P$:

$$
\boxed{
\begin{aligned}
\psi_P(x,y)
&=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}I(P_\varepsilon)
\right|_{\varepsilon=0}\\
&=\ell_P(x,y)-\mu_P.
\end{aligned}
}
$$

### 5.4 Interpretation of the MI influence function

The quantity $\psi_P(x,y)$ is the first-order effect on MI of moving a very
small amount of probability toward cell $(x,y)$:

- if $\ell_P(x,y)>\mu_P$, then $\psi_P(x,y)>0$ and the cell pushes MI upward;
- if $\ell_P(x,y)<\mu_P$, then $\psi_P(x,y)<0$ and the cell pushes MI downward;
- the farther the local score is from the average MI, the more influential
  the cell is.

The influence function is centred under $P$:

$$
\begin{aligned}
\operatorname E_P\{\psi_P(X,Y)\}
&=\operatorname E_P\{\ell_P(X,Y)-\mu_P\}\\
&=\mu_P-\mu_P\\
&=0.
\end{aligned}
$$

Thus, $\psi_P$ describes the observation-level fluctuations around the true
MI value. The next step converts those fluctuations into the sampling
variance of the complete MI estimator.

### 5.5 From the influence function to a standard error

Section 5.3 derived $\psi_P(z)$ from the change in MI caused by moving
probability toward one cell $z$. The same derivative determines the leading
sampling error in an actual random sample.

#### From cell sensitivity to sample error

The empirical distribution can be written as

$$
\widehat P
=\frac{1}{n_P}\sum_{k=1}^{n_P}\delta_{Z_k^{(P)}},
$$

where $\delta_{Z_k^{(P)}}$ places all its probability on the cell containing
observation $k$. Thus, every observation contributes probability mass
$1/n_P$ to its observed cell.

Section 5.3 showed that moving probability toward a cell $z$ changes MI at
first-order rate $\psi_P(z)$. An observation has weight $1/n_P$, so its
first-order contribution to the MI estimation error is
$\psi_P(Z_k^{(P)})/n_P$. Adding the contributions from all observations gives

$$
I(\widehat P)-I(P)
\approx\frac{1}{n_P}\sum_{k=1}^{n_P}\psi_P(Z_k^{(P)}).
$$

This is the distributional analogue of the ordinary Taylor approximation
$f(a+h)-f(a)\approx f'(a)h$. The input is now the whole probability table,
and $\psi_P$ supplies the relevant derivative for each cell.

More formally,

$$
I(\widehat P)-I(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}\psi_P(Z_k^{(P)})
+o_p(n_P^{-1/2}).
$$

The remainder $o_p(n_P^{-1/2})$ contains higher-order effects that become
small relative to the leading sampling error as $n_P$ increases.

#### Sampling variance of plug-in MI

For a random observation $Z\sim P$, define

$$
\begin{aligned}
V(P)
&=\operatorname{Var}_P\{\psi_P(Z)\}\\
&=\operatorname E_P\left[\{\ell_P(Z)-\mu_P\}^2\right].
\end{aligned}
$$

Thus, $V(P)$ measures how different the cell-level MI influences are across
the population. If all cells have similar influence, $V(P)$ is small. If
some cells push MI much more strongly than others, $V(P)$ is large.

The leading MI error is an average of $n_P$ independent influence values.
Each has variance $V(P)$, so

$$
\begin{aligned}
\operatorname{Var}\left\{
\frac{1}{n_P}\sum_{k=1}^{n_P}\psi_P(Z_k^{(P)})
\right\}
&=\frac{1}{n_P^2}
\sum_{k=1}^{n_P}\operatorname{Var}_P\{\psi_P(Z_k^{(P)})\}\\
&=\frac{1}{n_P^2}\{n_PV(P)\}\\
&=\frac{V(P)}{n_P},
\end{aligned}
$$

where the middle equality uses independence. This is the standard variance
formula for an average of iid contributions: the variance of one contribution
is divided by the sample size. Consequently,

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P},
$$

and the corresponding first-order standard error is

$$
\operatorname{SE}\{\widehat I(P)\}
\approx\sqrt{\frac{V(P)}{n_P}}.
$$

#### Normal approximation

The values
$\psi_P(Z_1^{(P)}),\ldots,\psi_P(Z_{n_P}^{(P)})$ are independent, have mean
zero, and have variance $V(P)$. The central limit theorem therefore gives an
approximately normal average for sufficiently large $n_P$. Equivalently,

$$
\widehat I(P)
\mathrel{\dot\sim}
N\left\{I(P),\frac{V(P)}{n_P}\right\},
$$

or, in the usual asymptotic notation,

$$
\sqrt{n_P}\left\{\widehat I(P)-I(P)\right\}
\overset{d}{\longrightarrow}
N\{0,V(P)\}.
$$

#### Effect of the bias correction

At fixed $n_P$, $r$, and $c$, the bias correction
$d/(2n_P)$ is a constant rather than a new random estimate. Subtracting a
constant shifts the centre of a random variable but does not change its
spread:

$$
\operatorname{Var}(X-c)=\operatorname{Var}(X).
$$

Therefore, the bias-corrected MI estimate has the same first-order variance:

$$
\operatorname{Var}\{\widehat I_{\mathrm{BC}}(P)\}
\approx\frac{V(P)}{n_P}.
$$

## 6. The Two-Sample Standardized Statistic

Section 5 gives a first-order variance for each estimated MI. The test,
however, concerns their difference. Under the null hypothesis, the corrected
difference is centred near zero, and its sampling variance determines how
large a chance difference should be expected.

For the second population, define $V(Q)$ in the same way as $V(P)$. The two
samples are independent, so the covariance between their MI estimators is
zero. The variance of their difference is therefore the sum

$$
\operatorname{Var}(\widehat\Delta_{\mathrm{BC}})
\approx
\frac{V(P)}{n_P}+\frac{V(Q)}{n_Q}.
$$

Neither $V(P)$ nor $V(Q)$ is known. The same plug-in principle used for MI
estimates each one by the empirical variance of its local influence values.
For group $P$,

$$
\widehat V_P
=\sum_{i,j}\widehat p_{ij}
\left\{\widehat\ell_{ij}-\widehat I(P)\right\}^2.
$$

The estimate $\widehat V_Q$ is calculated analogously. It is useful to name
the two contributions to the squared standard error

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Their sum estimates the variance of the corrected difference, so taking its
square root gives the estimated standard error:

$$
\widehat{\operatorname{SE}}
=\sqrt{a+b}
=\sqrt{
\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}
}.
$$

Dividing the estimated difference by this standard error expresses the
difference in units of its expected sampling fluctuation:

$$
\boxed{
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\sqrt{\widehat V_P/n_P+\widehat V_Q/n_Q}}.
}
$$

This is a signed, one-dimensional contrast. If $V(P)$ and $V(Q)$ were known,
the asymptotic normal results from Section 5 would give $T$ a standard normal
reference under $H_0$. Equivalently, $T^2$ would have a one-degree-of-freedom
chi-squared reference. The table dimension $(r-1)(c-1)$ does not appear here
because the hypothesis imposes one scalar restriction, $I(P)-I(Q)=0$, rather
than testing every association parameter separately.

In practice, the denominator contains the estimated quantities
$\widehat V_P$ and $\widehat V_Q$. Treating them as known ignores an
additional source of finite-sample uncertainty. The expanded
Welch-Satterthwaite construction measures that uncertainty and uses it to
replace the normal reference with an appropriately heavier-tailed Student
reference.

## 7. Deriving the Influence Function of the MI Variance

### 7.1 Sampling variation in the estimated MI variance

The statistic $T$ uses $\widehat V_P$ and $\widehat V_Q$ in its denominator.
These are estimates calculated from finite tables, so they also change from
sample to sample. A stable variance estimate supports a reference close to
the normal distribution; an unstable variance estimate requires heavier
tails. Its stability can be measured by deriving the first-order change in
$V(P)$ produced by one cell perturbation, using the same path as in Section 5.

Recall that the observation-level influence on MI is

$$
\psi_P(x,y)=\ell_P(x,y)-\mu_P,
$$

and its variance is

$$
V(P)=\operatorname E_P\{\psi_P(X,Y)^2\}.
$$

The corresponding sensitivity is

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Thus, $g_P(x,y)$ is the influence function of the MI variance: it measures
how strongly probability placed near cell $(x,y)$ changes the variance used
in the denominator of $T$.

### 7.2 Differentiate the variance directly

Under the perturbed distribution,

$$
V(P_\varepsilon)
=\sum_{i,j}p_{ij}(\varepsilon)
\psi_{P_\varepsilon}(i,j)^2.
$$

As in the MI derivation, both the probability weights and the values being
averaged change. The first part of the product rule changes the weights. The
second changes the squared influence values; differentiating a square
produces the factor $2\psi_P\dot\psi_P$. Hence,

$$
\begin{aligned}
g_P(x,y)
={}&\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\psi_P(i,j)^2\\
&+2\sum_{i,j}p_{ij}\psi_P(i,j)\dot\psi_P(i,j;z).
\end{aligned}
$$

The first sum replaces the population-average squared influence with the
squared influence of the target cell. It therefore reduces to

$$
\sum_{i,j}
\left[\mathbf 1\{i=x,j=y\}-p_{ij}\right]\psi_P(i,j)^2
=\psi_P(x,y)^2-V(P).
$$

The centred influence $\psi_P=\ell_P-\mu_P$ changes because both the local
score and its population mean change:

$$
\dot\psi_P(i,j;z)
=\dot\ell_P(i,j;z)-\dot\mu_P(x,y).
$$

The derivative $\dot\mu_P(x,y)$ is common to every cell. Its contribution is
multiplied by the weighted sum of $\psi_P$, which is zero because $\psi_P$ is
centred:

$$
\sum_{i,j}p_{ij}\psi_P(i,j)=0.
$$

Consequently, a common shift in the mean does not directly change the
variance. Only the changes in the local scores remain:

$$
g_P(x,y)
=\psi_P(x,y)^2-V(P)
+2\sum_{i,j}p_{ij}\psi_P(i,j)\dot\ell_P(i,j;z).
$$

### 7.3 The row-and-column adjustment

The remaining term describes how the target cell changes local scores across
the table:

$$
\sum_{i,j}p_{ij}\psi_P(i,j)\dot\ell_P(i,j;z).
$$

The derivative $\dot\ell_P$ from Section 5.2 contains a cell contribution, a
row contribution, a column contribution, and a normalization contribution.
After weighting by $p_{ij}\psi_P(i,j)$, these become respectively

$$
\begin{aligned}
\sum_{i,j}p_{ij}\psi_P(i,j)\dot\ell_P(i,j;z)
={}&\psi_P(x,y)
-\operatorname E_P\{\psi_P(X,Y)\mid X=x\}\\
&-\operatorname E_P\{\psi_P(X,Y)\mid Y=y\}
+\operatorname E_P\{\psi_P(X,Y)\}.
\end{aligned}
$$

The conditional expectations appear because changing the target cell also
changes the entire row $x$ and column $y$. To express them in terms of the
original local scores, define the row and column means

$$
R_P(x)=\operatorname E_P\{\ell_P(X,Y)\mid X=x\},
\qquad
C_P(y)=\operatorname E_P\{\ell_P(X,Y)\mid Y=y\}.
$$

Since $\psi_P=\ell_P-\mu_P$,

$$
\operatorname E_P(\psi_P)=0,
\qquad
\operatorname E_P(\psi_P\mid X=x)=R_P(x)-\mu_P,
$$

and similarly

$$
\operatorname E_P(\psi_P\mid Y=y)=C_P(y)-\mu_P.
$$

The row-and-column contribution is therefore

$$
\sum_{i,j}p_{ij}\psi_P(i,j)\dot\ell_P(i,j;z)
=\ell_P(x,y)-R_P(x)-C_P(y)+\mu_P.
$$

Combining it with the direct squared-influence contribution from Section 7.2
gives the complete variance influence:

$$
\boxed{
g_P(x,y)
=\psi_P(x,y)^2-V(P)
+2\{\ell_P(x,y)-R_P(x)-C_P(y)+\mu_P\}.
}
$$

This formula has two intuitive parts. The term
$\psi_P(x,y)^2-V(P)$ measures whether the cell's squared MI influence is
larger or smaller than average. The second term accounts for the fact that
changing one cell also changes the local-information scores in its entire
row and column.

The two parts have zero weighted mean, so $g_P$ is centred under $P$:

$$
\operatorname E_P\{g_P(X,Y)\}=0.
$$

## 8. Sampling Uncertainty of $\widehat V_P$

The role of $g_P$ for $\widehat V_P$ is exactly parallel to the role of
$\psi_P$ for $\widehat I(P)$. Each sampled observation contributes mass
$1/n_P$ to its cell, so its first-order contribution to the error in
$\widehat V_P$ is $g_P(Z_k^{(P)})/n_P$.

The plug-in MI variance estimate is

$$
\widehat V_P=V(\widehat P).
$$

The first-order sampling error is therefore the average

$$
V(\widehat P)-V(P)
=\frac{1}{n_P}\sum_{k=1}^{n_P}g_P(Z_k^{(P)})
+o_p(n_P^{-1/2}).
$$

The spread of the cell-level sensitivities is

$$
\boxed{
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\}.
}
$$

Since $g_P$ is centred, its variance equals its second moment:

$$
\tau_P^2
=\operatorname E_P\{g_P(X,Y)^2\}.
$$

The same sample-average variance rule used in Section 5 now gives

$$
\boxed{
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
}
$$

The quantity $\tau_P^2/n_P$ is therefore the first-order sampling uncertainty
of the variance estimate itself. A large value means that the denominator of
$T$ is sensitive to which cells happen to be observed; a small value means
that the estimated denominator is comparatively stable.

## 9. Empirical Variance-Influence Calculation

Sections 7 and 8 used population quantities to derive the result. A real test
has only the observed count tables, so every population quantity is now
replaced by its empirical version. This produces a deterministic calculation
from the observed table; no resampling is needed.

### 9.1 Estimate the MI influence variance

The empirical MI is the centre of the observed local scores:

$$
\widehat\mu_P
=\sum_{i,j}\widehat p_{ij}\widehat\ell_{ij}.
$$

Subtracting this centre gives the empirical influence of each cell:

$$
\widehat\psi_P(i,j)
=\widehat\ell_{ij}-\widehat\mu_P.
$$

Their weighted variance estimates the sampling-variance numerator $V(P)$:

$$
\widehat V_P
=\sum_{i,j}\widehat p_{ij}\widehat\psi_P(i,j)^2.
$$

### 9.2 Estimate the row-and-column adjustment

The formula for $g_P$ also requires the mean score in each row and column.
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

These quantities measure how much of a cell's local score is shared with its
row and column. The empirical variance influence for each cell is then

$$
\widehat g_P(i,j)
=\widehat\psi_P(i,j)^2-\widehat V_P
+2\{\widehat\ell_{ij}-\widehat R_P(i)
-\widehat C_P(j)+\widehat\mu_P\}.
$$

### 9.3 Estimate the uncertainty of $\widehat V_P$

The population influence function is centred, and its empirical counterpart
has weighted mean zero in exact arithmetic. Computing the mean explicitly
removes any small floating-point residual:

$$
\overline g_P
=\sum_{i,j}\widehat p_{ij}\widehat g_P(i,j).
$$

The weighted variance of the centred cell sensitivities estimates
$\tau_P^2$:

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

If the standard error in $T$ were known, the normal approximation from
Section 6 would be sufficient. It is instead estimated from the same finite
tables. A Student reference accounts for this additional uncertainty by
linking the heaviness of its tails to the reliability of the variance
estimate.

For normally distributed observations, an ordinary sample variance has an
exact scaled chi-squared distribution. The MI variance estimator is not an
ordinary sample variance, so that exact result cannot be used. However,
Sections 8 and 9 provide the two quantities needed for Satterthwaite moment
matching:

$$
\operatorname E(\widehat V_P)\approx V(P),
\qquad
\operatorname{Var}(\widehat V_P)\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite represents $\widehat V_P$ by a scaled chi-squared variable with
the same approximate mean and variance. This preserves the relevant amount
of variance-estimation uncertainty without claiming an exact chi-squared
law.

### 10.1 Scaled chi-squared representation

A chi-squared random variable $U\sim\chi^2_\nu$ has

$$
\operatorname E(U)=\nu,
\qquad
\operatorname{Var}(U)=2\nu.
$$

Scaling it to have mean $m>0$ gives

$$
Y=m\frac{U}{\nu},
$$

with

$$
\operatorname E(Y)=m,
\qquad
\operatorname{Var}(Y)=\frac{2m^2}{\nu}.
$$

Its relative variance is

$$
\frac{\operatorname{Var}(Y)}{\operatorname E(Y)^2}
=\frac{2}{\nu}.
$$

Thus, $\nu$ controls the uncertainty relative to the size of the estimated
quantity. A large $\nu$ represents a tightly concentrated variance estimate;
a small $\nu$ represents a more variable estimate. Solving for $\nu$ gives
the Satterthwaite moment-matching rule

$$
\boxed{
\nu=\frac{2m^2}{\operatorname{Var}(Y)}.
}
$$

### 10.2 MI-specific component degrees of freedom

For $\widehat V_P$, the target mean is $V(P)$ and the derived variance is
$\tau_P^2/n_P$. The corresponding scaled chi-squared representation is

$$
\widehat V_P
\mathrel{\dot\sim}
V(P)\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

Here $\mathrel{\dot\sim}$ denotes an approximate distributional model.
Matching its variance $2V(P)^2/\nu_{V,P}$ to $\tau_P^2/n_P$ gives

$$
\boxed{
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
}
$$

The population quantities are unknown, so the observed table supplies their
plug-in estimates:

$$
\boxed{
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2}.
}
$$

The same calculation for group $Q$ gives

$$
\boxed{
\widehat\nu_{V,Q}
=\frac{2n_Q\widehat V_Q^2}{\widehat\tau_Q^2}.
}
$$

### 10.3 Invariance under deterministic scaling

The squared standard error contains $\widehat V_P/n_P$ rather than
$\widehat V_P$. Dividing by the fixed sample size changes the magnitude of
the variance component but not its relative uncertainty. Algebraically,

$$
A=\frac{\widehat V_P}{n_P},
$$

and the scaled representation becomes

$$
A
\mathrel{\dot\sim}
\frac{V(P)}{n_P}
\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

The random chi-squared factor is unchanged, so the component retains
$\nu_{V,P}$ degrees of freedom. The same argument applies to

$$
B=\frac{\widehat V_Q}{n_Q}.
$$

## 11. Effective Degrees of Freedom for the Combined Denominator

The squared standard error is the sum of two independently estimated
components,

$$
S^2=A+B,
\qquad
A=\frac{\widehat V_P}{n_P},
\qquad
B=\frac{\widehat V_Q}{n_Q}.
$$

Each component has its own scale and effective degrees of freedom, whereas a
single Student reference requires one degrees-of-freedom value for the whole
denominator. Satterthwaite obtains it by matching the mean and variance of
$S^2$.

The population means of the two components are

$$
a_0=\frac{V(P)}{n_P},
\qquad
b_0=\frac{V(Q)}{n_Q}.
$$

Their scaled chi-squared representations imply

$$
\operatorname{Var}(A)\approx\frac{2a_0^2}{\nu_{V,P}},
\qquad
\operatorname{Var}(B)\approx\frac{2b_0^2}{\nu_{V,Q}}.
$$

Because the samples are independent, these component uncertainties add:

$$
\operatorname{Var}(S^2)
\approx
\frac{2a_0^2}{\nu_{V,P}}
+\frac{2b_0^2}{\nu_{V,Q}}.
$$

Representing the complete squared standard error by

$$
S^2
\mathrel{\dot\sim}
(a_0+b_0)\frac{\chi^2_{\nu}}{\nu}
$$

gives it the correct mean $a_0+b_0$. Matching its variance
$2(a_0+b_0)^2/\nu$ to the component variance above yields

$$
\nu
=\frac{(a_0+b_0)^2}
{a_0^2/\nu_{V,P}+b_0^2/\nu_{V,Q}}.
$$

The unknown population values are replaced by the observed components

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q},
$$

which gives the expanded Welch-Satterthwaite degrees of freedom

$$
\boxed{
\widehat\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}
+b^2/\widehat\nu_{V,Q}}.
}
$$

The weighting in this formula follows the contribution of each group to the
squared standard error. If one component dominates, the combined degrees of
freedom lie close to that component's value. If both components are stable,
the combined value is larger and the Student reference approaches the normal
reference.

## 12. The Final Reference Distribution and P-Value

Under $H_0$, the numerator of $T$ is approximately normal and centred at
zero. The denominator is estimated, with its relative uncertainty summarized
by $\widehat\nu_{\mathrm{expanded}}$. A Student distribution uses precisely
this structure: lower degrees of freedom give heavier tails when the
denominator is less reliable, while large degrees of freedom recover the
normal reference.

The observed statistic is

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}{\sqrt{a+b}}.
$$

The alternative permits either $I(P)>I(Q)$ or $I(P)<I(Q)$, so the test is
two-sided. Its p-value is the probability, under the Student reference, of a
magnitude at least as large as $|T|$:

$$
\boxed{
p_{\mathrm{expanded}}
=2\left[1-F_{t_{\widehat\nu_{\mathrm{expanded}}}}
(|T|)\right].
}
$$

Here $F_{t_\nu}$ denotes the cumulative distribution function of a Student
random variable with $\nu$ degrees of freedom. At significance level
$\alpha$, reject $H_0:I(P)=I(Q)$ when

$$
p_{\mathrm{expanded}}<\alpha,
$$

or equivalently when

$$
|T|>
t_{1-\alpha/2,\widehat\nu_{\mathrm{expanded}}}.
$$

## 13. Complete Calculation from Two Count Tables

The complete practical calculation is collected here in the order it is
performed, with the role of each stage stated before its formula.

### Step 1: Convert counts to probabilities

Normalizing the counts removes the raw sample-size scale and estimates each
group's joint distribution. For $G\in\{P,Q\}$,

$$
\widehat p^{(G)}_{ij}=\frac{N^{(G)}_{ij}}{n_G}.
$$

### Step 2: Calculate row and column marginals

The margins provide the independence probability against which each joint
cell is compared.

$$
\widehat p^{(G)}_{i+}=\sum_j\widehat p^{(G)}_{ij},
\qquad
\widehat p^{(G)}_{+j}=\sum_i\widehat p^{(G)}_{ij}.
$$

### Step 3: Calculate local-information scores

Each score records the cell's log departure from its independence baseline.

$$
\widehat\ell^{(G)}_{ij}
=\log\left(
\frac{\widehat p^{(G)}_{ij}}
{\widehat p^{(G)}_{i+}\widehat p^{(G)}_{+j}}
\right).
$$

### Step 4: Calculate plug-in MI

The probability-weighted average of the local scores gives the estimated MI.

$$
\widehat I(G)
=\sum_{i,j}\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij}.
$$

### Step 5: Correct the leading bias

Subtract the leading upward plug-in bias separately for each sample size.

$$
\widehat I_{\mathrm{BC}}(G)
=\widehat I(G)-\frac{(r-1)(c-1)}{2n_G}.
$$

### Step 6: Form the estimated difference

The signed difference estimates the target contrast $I(P)-I(Q)$.

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

### Step 7: Calculate the centred score and its variance

The centred scores are the empirical MI influence values. Their weighted
variance supplies each group's contribution to the standard error. For each
group,

$$
\widehat\mu_G
=\sum_{i,j}\widehat p^{(G)}_{ij}
\widehat\ell^{(G)}_{ij},
$$

$$
\widehat\psi_G(i,j)
=\widehat\ell^{(G)}_{ij}-\widehat\mu_G,
$$

and

$$
\widehat V_G
=\sum_{i,j}\widehat p^{(G)}_{ij}
\widehat\psi_G(i,j)^2.
$$

### Step 8: Calculate conditional score means

The row and column means quantify the marginal-score changes created when a
cell probability changes.

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

Combining the direct squared-influence effect with the marginal adjustment
gives the sensitivity of $\widehat V_G$ to each cell.

$$
\widehat g_G(i,j)
=\widehat\psi_G(i,j)^2-\widehat V_G
+2\left\{
\widehat\ell^{(G)}_{ij}
-\widehat R_G(i)-\widehat C_G(j)+\widehat\mu_G
\right\}.
$$

### Step 10: Calculate variance-influence variability

The weighted spread of these sensitivities measures how uncertain the
estimated MI variance is across repeated samples.

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

Satterthwaite moment matching converts this variance uncertainty into a
degrees-of-freedom measure of reliability.

$$
\widehat\nu_{V,G}
=\frac{2n_G\widehat V_G^2}{\widehat\tau_G^2}.
$$

### Step 12: Calculate the two standard-error components

Dividing each MI influence variance by its sample size gives its contribution
to the variance of the estimated MI difference.

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

### Step 13: Calculate the standard error and statistic

The square root of the combined variance is the standard error; dividing the
estimated contrast by it produces a dimensionless test statistic.

$$
\widehat{\operatorname{SE}}=\sqrt{a+b},
$$

$$
T=\frac{\widehat\Delta_{\mathrm{BC}}}
{\widehat{\operatorname{SE}}}.
$$

### Step 14: Combine the component degrees of freedom

The two component reliability measures are combined in proportion to their
contributions to the squared standard error.

$$
\widehat\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}
+b^2/\widehat\nu_{V,Q}}.
$$

### Step 15: Calculate the two-sided p-value

The Student reference converts the magnitude of the standardized contrast
into evidence against equal population MI in either direction.

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

Equivalently,

$$
\widehat\nu_{V,P}
=\frac{2n_P}{\widehat\tau_P^2/\widehat V_P^2}.
$$

The ratio $\widehat\tau_P^2/\widehat V_P^2$ is the variance estimator's
instability relative to its squared magnitude. The effective degrees of
freedom therefore increase with sample size and decrease with relative
instability across cells.

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

Using $n_P-1$ for MI is therefore an analogy to the normal-sample result. It
treats $\widehat V_P$ as though it were an ordinary sample variance with a
fixed underlying score. In fact, the local-information scores are themselves
functions of the estimated joint table and margins, so the uncertainty of
$\widehat V_P$ need not follow that conventional pattern.

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

The construction combines smooth differentiation of the MI functional, a
first-order central limit theorem, and Satterthwaite moment matching. The
following conditions identify where those three ingredients apply.

### 16.1 Fixed finite alphabet

The asymptotic expansions assume that $r$ and $c$ remain fixed as the sample
sizes increase. This keeps the probability table finite-dimensional while
the empirical cell probabilities converge at the usual $n^{-1/2}$ rate. The
derivation does not establish validity when the alphabet grows with sample
size.

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

Once the two count tables have been constructed, every quantity in the test
is obtained by a fixed number of passes over their $r\times c$ cells:

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

If the input consists of raw observation pairs, constructing the tables first
requires $O(n_P+n_Q)$ work. This aggregation is performed once and is also
required by ordinary plug-in MI estimation. The subsequent significance test
depends on the table dimensions rather than repeatedly processing or
shuffling the raw observations. No permutations, bootstrap samples, or Monte
Carlo tables are required.

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

The purpose of each quantity in the derivation can be summarized as follows.

| Quantity | Role in the construction |
| --- | --- |
| $\ell_P(i,j)$ | Measures the cell's log departure from independence. |
| $\mu_P=I(P)$ | Averages the local scores to obtain population MI. |
| $\psi_P(i,j)=\ell_P(i,j)-\mu_P$ | Measures the first-order effect of the cell on MI. |
| $V(P)=\operatorname{Var}_P(\psi_P)$ | Determines the first-order sampling variance of $\widehat I(P)$. |
| $g_P(i,j)$ | Measures the first-order effect of the cell on $V(P)$. |
| $\tau_P^2=\operatorname{Var}_P(g_P)$ | Determines the sampling uncertainty of $\widehat V_P$. |
| $\nu_{V,P}=2n_PV(P)^2/\tau_P^2$ | Expresses that variance-estimation uncertainty as component degrees of freedom. |

These roles form the mathematical chain

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
g_P
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

The first influence function converts cell-level MI sensitivity into a
standard error. The second converts cell-level variance sensitivity into the
uncertainty of that standard error. Satterthwaite moment matching then
expresses the second uncertainty as effective degrees of freedom, allowing
the standardized MI difference to be interpreted with a Student reference.

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
