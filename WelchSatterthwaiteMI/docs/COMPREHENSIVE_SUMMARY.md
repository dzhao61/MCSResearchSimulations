# Comprehensive Summary: Welch-Type Testing for Differential Mutual Information

## 1. Research Story

The research question is

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are joint distributions estimated from two independent
categorical samples.

The idea is analogous to Welch's $t$-test. Classical Welch testing compares
two population means by:

1. estimating the difference between the means;
2. dividing that difference by its estimated standard error;
3. using a Student distribution with effective degrees of freedom that reflect
   uncertainty in the two variance estimates.

Here, the two means are replaced by two mutual information estimates:

| Welch's $t$-test | Differential-MI test |
| --- | --- |
| Sample mean | Bias-corrected MI |
| Sample variance | MI influence variance |
| Difference in means | Difference in MI |
| Welch-Satterthwaite degrees of freedom | Simple or MI-specific degrees of freedom |

Four analytic methods form the comparison:

| Method | How $T$ is calibrated |
| --- | --- |
| Normal Wald | Standard normal distribution |
| Simple Welch-Satterthwaite | Student distribution using $n-1$ component degrees of freedom |
| Expanded Welch-Satterthwaite | Student distribution using MI-specific variance-influence degrees of freedom |
| Custom Welch | Expanded Welch for sample-size ratios of at least $4{:}1$ when valid; normal Wald otherwise |

The expanded Welch-Satterthwaite method supplies the MI-specific finite-df
calculation. Custom Welch adds a guarded decision rule so that calculation is
used in the unequal-sample regime where it helped, while normal Wald is
retained where the correction could become unnecessarily conservative.

## 2. Quick Literature Review

**Welch (1947) and Satterthwaite (1946).** Welch's $t$-test handles two
means with unequal and estimated variances. Satterthwaite's approximation
replaces several uncertain variance components with one effective number of
degrees of freedom.

**Hutcheson (1970).** Hutcheson applied the same broad idea to comparing two
Shannon diversity values. This is the closest direct predecessor because
Shannon diversity is an entropy functional. It means that using a
Welch-Satterthwaite architecture for an information quantity is not itself
new.

**Miller (1955) and later MI estimation work.** Plug-in entropy and MI
estimates have finite-sample bias. For an $r\times c$ table with fixed
positive support, the leading MI bias is

$$
\frac{(r-1)(c-1)}{2n}.
$$

This correction is important when comparing groups with different sample
sizes.

**Mora and Ruiz-Castillo (2009, 2011).** Their work studies estimation and
comparison of an MI-based segregation index. It establishes clear prior work
for comparing MI-type quantities between populations.

The simple Welch method is therefore best viewed as a direct transport of
existing ideas. The potentially novel part is the expanded
Welch-Satterthwaite calculation: deriving effective degrees of freedom from
the full influence function of the discrete-MI variance estimator, then
testing that calculation across broad finite-sample regimes.

Key references:

- Welch: <https://doi.org/10.1093/biomet/34.1-2.28>
- Satterthwaite: <https://doi.org/10.2307/3002019>
- Hutcheson: <https://doi.org/10.1016/0022-5193(70)90124-4>
- Mora and Ruiz-Castillo:
  <https://doi.org/10.1111/j.1467-9531.2011.01237.x>

## 3. Shared Data and Effect Estimate

All four methods begin with the same two count tables:

$$
N^P=(N^P_{ij}),
\qquad
N^Q=(N^Q_{ij}),
$$

with sample sizes $n_P$ and $n_Q$. The rows and columns represent the same
aligned categories in both groups.

### 3.1 Estimate MI

For group $P$, calculate empirical cell and marginal probabilities:

$$
\widehat p_{ij}=\frac{N^P_{ij}}{n_P},
\qquad
\widehat p_{i+}=\sum_j\widehat p_{ij},
\qquad
\widehat p_{+j}=\sum_i\widehat p_{ij}.
$$

Plug-in MI in nats is

$$
\widehat I(P)
=\sum_{i=1}^{r}\sum_{j=1}^{c}
\widehat p_{ij}
\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The same calculation gives $\widehat I(Q)$.

### 3.2 Correct the leading bias

Let

$$
d=(r-1)(c-1).
$$

The corrected MI estimates are

$$
\widehat I_{\mathrm{BC}}(P)
=\widehat I(P)-\frac{d}{2n_P},
\qquad
\widehat I_{\mathrm{BC}}(Q)
=\widehat I(Q)-\frac{d}{2n_Q}.
$$

The estimated MI difference is

$$
\widehat\Delta_{\mathrm{BC}}
=\widehat I_{\mathrm{BC}}(P)
-\widehat I_{\mathrm{BC}}(Q).
$$

### 3.3 Estimate the standard error

Define the local-information score for a cell:

$$
\widehat\ell_{ij}
=\log\!\left(
\frac{\widehat p_{ij}}
{\widehat p_{i+}\widehat p_{+j}}
\right).
$$

The MI influence variance for group $P$ is

$$
\widehat V_P
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I(P)\right)^2.
$$

Define $\widehat V_Q$ in the same way. Because the groups are independent,

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}.
$$

Every method uses the same standardized statistic:

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\widehat{\operatorname{SE}}}.
$$

The methods differ only in how they decide whether the observed magnitude
$|T|$ is unusual.

The working assumptions are independent observations within each group,
independent groups, fixed aligned alphabets, positive population support, and
a positive first-order influence variance.

## 4. Method 1: Normal Wald

### How it works

Normal Wald treats the estimated standard error as sufficiently accurate and
compares $T$ with a standard normal variable:

$$
p_{\mathrm{normal}}
=2\Pr\{Z\ge |T|\},
\qquad
Z\sim N(0,1).
$$

A $100(1-\alpha)\%$ confidence interval is

$$
\widehat\Delta_{\mathrm{BC}}
\ \pm\
z_{1-\alpha/2}\widehat{\operatorname{SE}}.
$$

### Interpretation

Normal Wald is the simplest analytic baseline. It is asymptotically valid
under regular fixed-support conditions. Its weakness is finite-sample
calibration: it does not account for uncertainty in $\widehat V_P$ and
$\widehat V_Q$.

### Cost

It requires one pass over the table:

$$
O(rc).
$$

## 5. Method 2: Simple Welch-Satterthwaite

### How it works

Define the two estimated variance contributions:

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Simple Welch treats the MI influence variances like ordinary sample variances
and assigns

$$
\nu_P=n_P-1,
\qquad
\nu_Q=n_Q-1.
$$

Satterthwaite combines them:

$$
\nu_{\mathrm{simple}}
=\frac{(a+b)^2}
{a^2/(n_P-1)+b^2/(n_Q-1)}.
$$

The p-value becomes

$$
p_{\mathrm{simple}}
=2\Pr\{t_{\nu_{\mathrm{simple}}}\ge |T|\}.
$$

### Interpretation

A Student distribution has heavier tails than a normal distribution. Simple
Welch therefore produces slightly larger p-values and wider confidence
intervals than normal Wald.

The limitation is that $n-1$ is exact for a conventional sample variance
under classical assumptions, but $\widehat V$ is a nonlinear function of
the full contingency table. Changing one observation changes cell
probabilities, marginal probabilities, local-information scores, MI, and its
estimated variance.

### Cost

The extra Satterthwaite arithmetic is constant time after $\widehat V_P$ and
$\widehat V_Q$ are available. Overall cost remains

$$
O(rc).
$$

## 6. Method 3: Expanded Welch-Satterthwaite

### Source and adaptation

This method is inspired by **Hutcheson's (1970) test for comparing two
Shannon diversities**. Hutcheson used the same broad architecture as Welch's
test: subtract two estimated information quantities, divide by their combined
estimated standard error, and use effective degrees of freedom for the
uncertain variance terms.

The present method adapts that architecture from Shannon entropy to mutual
information. The simple version assigns ordinary $n-1$ component degrees of
freedom. The expanded version adds the MI-specific step: it derives how the
complete nonlinear MI variance estimator changes when the probability of one
cell changes, then uses that sensitivity to estimate the component degrees of
freedom. Hutcheson supplies the conceptual template; the variance-influence
derivation below supplies the MI-specific expansion.

Reference: K. Hutcheson, *A Test for Comparing Diversities Based on the
Shannon Formula*, Journal of Theoretical Biology 29 (1970), 151-154,
<https://doi.org/10.1016/0022-5193(70)90124-4>.

### Why expand the simple method?

The test statistic contains the estimated variance terms $\widehat V_P$ and
$\widehat V_Q$. Simple Welch assigns each of them ordinary $n-1$ degrees of
freedom. That assignment is appropriate for a conventional sample variance,
but $\widehat V$ is a nonlinear function of the full contingency table.

Expanded Welch instead estimates how variable $\widehat V$ is under repeated
sampling. It then converts that variability into component degrees of
freedom using the usual Satterthwaite moment-matching argument. The MI
estimate, bias correction, standard error, and observed statistic are not
changed.

Here, **IF means influence function**: the first-order change in a statistical
functional after a small perturbation of the underlying distribution.

### 6.1 Write MI and its variance as functionals of $P$

Let $Z=(X,Y)\sim P$. For a cell $(i,j)$, define its local-information score

$$
\ell_P(i,j)
=\log\!\left(\frac{p_{ij}}{p_{i+}p_{+j}}\right).
$$

Write

$$
\mu_P=I(P)=\operatorname E_P\{\ell_P(Z)\},
\qquad
m_{2,P}=\operatorname E_P\{\ell_P(Z)^2\}.
$$

The influence function of MI is

$$
\psi_P(i,j)=\ell_P(i,j)-\mu_P.
$$

Consequently, the first-order variance governing the MI estimator is

$$
V(P)
=\operatorname{Var}_P\{\psi_P(Z)\}
=m_{2,P}-\mu_P^2.
$$

The ordinary Wald standard error uses an empirical estimate $\widehat V_P$.
Expanded Welch asks a second question: **how uncertain is that estimate of
variance?**

### 6.2 Define $g_P(x,y)$ through cell contamination

Increase the probability of cell $(x,y)$ by an infinitesimal amount while
renormalizing the rest of the table:

$$
P_\varepsilon
=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}.
$$

The variance influence function is defined by

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V(P_\varepsilon)
\right|_{\varepsilon=0}.
$$

Thus, $g_P(x,y)$ is the first-order change in the complete MI variance after
slightly increasing the probability of cell $(x,y)$. It includes more than
the direct effect on that cell: changing one cell also changes its row
margin, its column margin, every affected local-information score, and MI
itself.

### 6.3 Differentiate the local-information score

For an arbitrary cell $(i,j)$,

$$
\ell_{P_\varepsilon}(i,j)
=\log p_{ij}(\varepsilon)
-\log p_{i+}(\varepsilon)
-\log p_{+j}(\varepsilon).
$$

Differentiating the three logarithms along the contamination path gives

$$
\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
\ell_{P_\varepsilon}(i,j)
\right|_{\varepsilon=0}
=
\frac{\mathbf 1\{(i,j)=(x,y)\}}{p_{ij}}
-\frac{\mathbf 1\{i=x\}}{p_{i+}}
-\frac{\mathbf 1\{j=y\}}{p_{+j}}
+1.
$$

Multiplying this derivative by $p_{ij}\ell_P(i,j)$ and summing over the table
produces

$$
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P.
$$

This is the row-and-column adjustment that is absent if the local scores are
incorrectly treated as fixed observations.

### 6.4 Differentiate the complete variance

The formula for $g_P$ is not chosen heuristically. It follows by applying the
chain rule to

$$
V(P)=m_{2,P}-\mu_P^2.
$$

First differentiate the second moment:

$$
\begin{aligned}
\operatorname{IF}_{m_2,P}(x,y)
={}&\ell_P(x,y)^2-m_{2,P}\\
&+2\Big[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P
\Big].
\end{aligned}
$$

The MI influence function is

$$
\operatorname{IF}_{\mu,P}(x,y)
=\ell_P(x,y)-\mu_P.
$$

Applying the derivative of $V(P)=m_{2,P}-\mu_P^2$ gives

$$
g_P(x,y)
=\operatorname{IF}_{m_2,P}(x,y)
-2\mu_P\operatorname{IF}_{\mu,P}(x,y),
$$

or, in full,

$$
\boxed{
\begin{aligned}
g_P(x,y)={}&
\ell_P(x,y)^2-m_{2,P}\\
&+2\Big[
\ell_P(x,y)
-\operatorname E_P\{\ell_P(Z)\mid X=x\}
-\operatorname E_P\{\ell_P(Z)\mid Y=y\}
+\mu_P
\Big]\\
&-2\mu_P\big[\ell_P(x,y)-\mu_P\big].
\end{aligned}}
$$

The three pieces have direct meanings:

- $\ell_P(x,y)^2-m_{2,P}$ is the direct effect of moving probability mass;
- the middle term captures changes to the cell, row, and column scores;
- the final term accounts for the fact that the variance is centred around
  the estimated MI.

### 6.5 Convert $g_P$ into component degrees of freedom

Define

$$
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\}.
$$

First-order influence-function theory then gives

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite approximates the positive variance estimator by a scaled
chi-squared variable:

$$
\widehat V_P
\ \dot\sim\
V(P)\frac{\chi^2_{\nu_{V,P}}}{\nu_{V,P}}.
$$

This approximation has mean $V(P)$ and variance $2V(P)^2/\nu_{V,P}$.
Matching that variance to $\tau_P^2/n_P$ gives

$$
\frac{2V(P)^2}{\nu_{V,P}}
=\frac{\tau_P^2}{n_P}
\quad\Longrightarrow\quad
\boxed{
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}}.
$$

In practice, the population quantities are replaced by table estimates. In
particular,

$$
\widehat\tau_P^2
=\sum_{i,j:\widehat p_{ij}>0}
\widehat p_{ij}
\left(
\widehat g_P(i,j)
-\sum_{u,v}\widehat p_{uv}\widehat g_P(u,v)
\right)^2,
$$

and

$$
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2}.
$$

The same calculation gives $\widehat\nu_{V,Q}$.

### 6.6 Combine the two components

Recall

$$
a=\frac{\widehat V_P}{n_P},
\qquad
b=\frac{\widehat V_Q}{n_Q}.
$$

Scaling a variance component does not change its component degrees of
freedom. The usual Satterthwaite combination therefore gives

$$
\boxed{
\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}+b^2/\widehat\nu_{V,Q}}}.
$$

The final p-value is

$$
p_{\mathrm{expanded}}
=2\Pr\{t_{\nu_{\mathrm{expanded}}}\ge |T|\}.
$$

Nothing before this final calibration changes: expanded Welch uses the same
bias-corrected MI difference, standard error, and statistic $T$ as normal
Wald and simple Welch. The derivation changes only the reference degrees of
freedom.

### Interpretation

If an MI variance estimate is stable, $\widehat\tau^2$ is small and the
method assigns many degrees of freedom. If it is highly sample-dependent,
$\widehat\tau^2$ is large, the degrees of freedom fall, and the Student
reference becomes more conservative.

The expanded calculation targets the main weakness of simple Welch. It is
still an approximation. Unlike an ordinary normal-sample variance,
$\widehat V_P$ is not exactly scaled chi-squared, and $T$'s numerator and
denominator are estimated from the same tables and can be correlated. The
derivation therefore justifies the moment-matched degrees of freedom; it does
not claim that the resulting Student distribution is an exact finite-sample
law.

### Cost

The influence calculation requires additional row, column, and cell
reductions, but still scans the table only a fixed number of times:

$$
O(rc).
$$

In the unified benchmark it cost approximately 1.9 times normal Wald, while
remaining below 0.2 ms per table pair for tables up to $20\times20$.

## 7. Method 4: Custom Welch

Custom Welch does not introduce another estimator or degrees-of-freedom
formula. It selects between normal Wald and expanded Welch, both of which
have already been defined. Let the sample-size ratio be

$$
R_n=\frac{\max(n_P,n_Q)}{\min(n_P,n_Q)}.
$$

The decision rule is

$$
\boxed{
p_{\mathrm{custom}}
=
\begin{cases}
p_{\mathrm{expanded}},
&R_n\geq4\text{ and expanded Welch is valid},\\
p_{\mathrm{normal}},
&\text{otherwise}.
\end{cases}}
$$

Thus, Custom Welch uses the MI-specific finite-df correction when the larger
sample contains at least four times as many observations as the smaller
sample. For equal samples and ratios below $4{:}1$, it uses the standard
normal reference. If the expanded component degrees of freedom are undefined,
it also falls back to normal Wald, provided the shared Wald statistic remains
valid.

The reason for this rule comes directly from the development experiment.
Expanded Welch consistently helped at ratios of $4{:}1$, $10{:}1$, and
$20{:}1$, where the standardized statistic was too heavy-tailed for the
normal reference. At $1{:}1$ and $2{:}1$, it often added conservatism without
solving the more fundamental problems caused by widespread support loss.
The rule therefore limits the correction to the regime matching its observed
strength.

The route depends only on the two fixed sample sizes and whether the expanded
calculation is mathematically defined. It does not depend on the sign,
magnitude, or p-value of the observed MI difference. Consequently, it does
not choose the more favourable answer after seeing the test result.

The cutoff of 4 was chosen after inspecting the current development grid. It
is therefore a candidate rule rather than independently confirmed evidence.
The appropriate next experiment is to freeze this exact rule and evaluate it
without modification on newly generated scenarios.

The existing grid also does not fully cross $4{:}1$ or greater imbalance with
support instability. The fallback behavior is unit-tested, but its
calibration in that combined boundary regime is not yet established.

### Subsequent routing audit

A targeted development/holdout audit later crossed every population regime
with sample-size ratios $1$, $2$, $3$, $4$, $6$, $10$, and $20$, assigning
the smaller sample to both populations in turn. The calibration benefit of
expanded Welch began at $2{:}1$. Both independently generated cohorts selected
$R_n\geq2$ as the best tested ratio threshold, and it significantly improved
on the original $R_n\geq4$ rule under clustered bootstrap comparison.

Observed-support, observations-per-cell, and estimated-variance-share guards
did not add a meaningful holdout benefit. Severe support instability also
showed that neither normal Wald nor expanded Welch is calibrated when rows or
columns repeatedly disappear, particularly under unequal sample sizes. That
case should be identified as outside the first-order method's supported
domain rather than automatically routed to normal Wald.

The $2{:}1$ cutoff is now the evidence-backed revision candidate, while the
software retains the original $4{:}1$ rule until one frozen confirmation run
is completed. See the
[Custom Welch decision audit](CUSTOM_WELCH_DECISION_AUDIT.md) for the full
design, results, and recommendation.

Custom Welch remains deterministic and $O(rc)$. Its runtime follows the route
selected: approximately normal-Wald cost below the threshold and
expanded-Welch cost at or above it.

## 8. Method Map

| Feature | Normal Wald | Simple Welch | Expanded Welch | Custom Welch |
| --- | --- | --- | --- | --- |
| Effect estimate | Same bias-corrected MI difference | Same | Same | Same |
| Standard error | MI influence variance | Same | Same | Same |
| Reference | Normal | Student | Student | Normal or expanded Student |
| Variance uncertainty | Ignored | Approximated by $n-1$ | Derived from MI variance influence | Included only when $R_n\geq4$ and valid |
| Deterministic | Yes | Yes | Yes | Yes |
| Complexity | $O(rc)$ | $O(rc)$ | $O(rc)$ | $O(rc)$ |
| Main role | Analytic baseline | Simple finite-df correction | MI-specific correction | Guarded practical candidate |

## 9. Experimental Design

The redesigned validation uses one grid rather than several overlapping
experiments:

$$
12\ \text{table shapes}
\times18\ \text{population designs}
=216\ \text{equal-MI population pairs}.
$$

The eighteen designs comprise nine interpretable regimes, with two
population variants in each regime.

The shapes are

$$
2\times2,\ 2\times5,\ 3\times3,\ 3\times7,\ 4\times6,\ 5\times5,
\ 5\times10,\ 8\times8,\ 8\times12,\ 10\times10,\ 10\times15,
\ 20\times20.
$$

For every pair, $P$ and $Q$ are different joint distributions constructed to
satisfy $I(P)=I(Q)$ numerically. The largest absolute true MI difference over
the generated grid was $1.2\times10^{-13}$ nats.

### 9.1 Nine regimes

| Regime | Target MI | Sample-size ratio | Sparsity control | Purpose |
| --- | ---: | ---: | ---: | --- |
| Well sampled | 0.03 | $1{:}1$ | Average of 100 or 200 observations per cell | Check ordinary tables, including a skewed but densely sampled variant |
| Moderate | 0.07 | $1{:}2$ | Average of 20 or 50 observations per cell | Check moderate imbalance and heterogeneous margins |
| Sparse and imbalanced | 0.15 | $1{:}4$ | Average of 10 or 25 observations per cell | Target low average counts and strongly unequal sample sizes |
| Highly skewed and sparse | 0.10 or 0.15 | $1{:}1$ or $1{:}4$ | $1\leq E_{\min}<5$ in both populations | Test cells that are observed only a few times on average |
| Ultra-skewed and sparse | 0.10 or 0.15 | $1{:}1$ or $1{:}4$ | $0<E_{\min}<1$ in both populations | Test rare cells that are more likely to be empty than observed |
| Widespread sparsity | 0.03 | $1{:}1$ | 25-50% of cells have expected counts below 1 and at least 50% are below 5 in both populations | Test broad support sparsity rather than one isolated rare cell |
| Equal-MI shape mismatch | 0.07 or 0.15 | $1{:}1$ | Near-uniform margins in $P$ and strongly skewed margins in $Q$ | Compare differently shaped populations with exactly equal MI |
| Extreme sample imbalance | 0.07 or 0.15 | $1{:}10$ or $1{:}20$ | Average of 25 or 10 observations per cell in the smaller sample | Stress the unequal-variance combination directly |
| Support instability | 0.02 | $1{:}1$ | One row or column has expected total between 0.20 and 1 in both populations | Make complete sampled margins disappear frequently |

For a population with joint probabilities $p_{ij}$ and sample size $n$, the
minimum true expected cell count is

$$
E_{\min}=\min_{i,j}\{n p_{ij}\}.
$$

For a pair of populations, the stated interval must hold separately for both
$P$ and $Q$. This is stricter than classifying a table from the average
$n/(rc)$: a table may have a large sample overall while still containing a
very rare cell. The ultra-sparse generator targets expected minima between
0.20 and 1 internally, rather than values arbitrarily close to zero, while
still satisfying the reported $0<E_{\min}<1$ definition.

A minimum sample size of 120 is applied to the main designs. The explicitly
labelled support-instability boundary allows sample sizes down to 30 because
a binary margin that is likely to disappear cannot otherwise sustain the
target positive MI. Within each regime, the two variants use different random
margins and association patterns. Near-independence remains outside the main
scope.

### 9.2 Replication and fairness

Each population pair receives 10,000 independently sampled pairs of
multinomial tables:

$$
216\times10{,}000=2{,}160{,}000\ \text{null replicates}.
$$

Normal Wald, simple Welch, expanded Welch, and Custom Welch are calculated on
exactly the same table pairs. All four use the same bias-corrected difference,
$\widehat{\Delta}_{\mathrm{BC}}$, and standard error. Only the reference
calibration differs. Each method's false-positive rate is calculated among
the replicates for which that method returns a valid result; validity is
reported separately so boundary failures are not hidden by conditioning on a
common subset.

The experiment records false-positive rates at $\alpha=0.10$, $0.05$, and
$0.01$; 95% confidence-interval coverage; valid calculation rates; effective
degrees of freedom; sample sparsity; power over five alternatives; and
end-to-end runtime. Replicates are processed in chunks, so no large replicate
file is required.

## 10. Results

### 10.1 Accuracy metric

For a nominal level $\alpha$, a calibrated method should reject
approximately an $\alpha$ fraction of true null cases. For each scenario,

$$
\operatorname{FPR\ error}
=|\operatorname{FPR}-\alpha|.
$$

The tables report mean absolute FPR error across each set. Lower is better.
This calibration error must be interpreted together with the valid rate.

### 10.2 Null calibration

| Regime | Method | Error at $0.10$ | Error at $0.05$ | Error at $0.01$ | Valid rate | 95% coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Well sampled | Normal Wald | **0.00482** | **0.00326** | **0.00148** | 1.00000 | 0.95260 |
| Well sampled | Simple Welch | 0.00487 | 0.00332 | 0.00151 | 1.00000 | 0.95267 |
| Well sampled | Expanded Welch | 0.00650 | 0.00466 | 0.00199 | 1.00000 | 0.95418 |
| Well sampled | Custom Welch | **0.00482** | **0.00326** | **0.00148** | 1.00000 | 0.95260 |
| Moderate | Normal Wald | 0.00571 | 0.00370 | **0.00153** | 1.00000 | 0.95174 |
| Moderate | Simple Welch | **0.00560** | **0.00365** | 0.00155 | 1.00000 | 0.95196 |
| Moderate | Expanded Welch | 0.00602 | 0.00419 | 0.00172 | 1.00000 | 0.95407 |
| Moderate | Custom Welch | 0.00571 | 0.00370 | **0.00153** | 1.00000 | 0.95174 |
| Sparse and imbalanced | Normal Wald | 0.00830 | 0.00615 | 0.00286 | 1.00000 | 0.94424 |
| Sparse and imbalanced | Simple Welch | 0.00764 | 0.00565 | 0.00252 | 1.00000 | 0.94474 |
| Sparse and imbalanced | Expanded Welch | **0.00580** | **0.00395** | **0.00145** | 1.00000 | 0.94668 |
| Sparse and imbalanced | Custom Welch | **0.00580** | **0.00395** | **0.00145** | 1.00000 | 0.94668 |
| Highly skewed and sparse | Normal Wald | 0.00315 | 0.00275 | 0.00162 | 1.00000 | 0.94915 |
| Highly skewed and sparse | Simple Welch | 0.00303 | 0.00262 | 0.00156 | 1.00000 | 0.94931 |
| Highly skewed and sparse | Expanded Welch | **0.00255** | **0.00217** | **0.00124** | 1.00000 | 0.94977 |
| Highly skewed and sparse | Custom Welch | 0.00278 | 0.00239 | 0.00136 | 1.00000 | 0.94952 |
| Ultra-skewed and sparse | Normal Wald | 0.00431 | 0.00312 | 0.00133 | 1.00000 | 0.94767 |
| Ultra-skewed and sparse | Simple Welch | 0.00416 | 0.00296 | 0.00125 | 1.00000 | 0.94785 |
| Ultra-skewed and sparse | Expanded Welch | **0.00343** | **0.00248** | **0.00098** | 1.00000 | 0.94850 |
| Ultra-skewed and sparse | Custom Welch | 0.00409 | 0.00296 | 0.00126 | 1.00000 | 0.94783 |
| Widespread sparsity | Normal Wald | 0.01457 | **0.01064** | 0.00500 | 0.99980 | 0.94737 |
| Widespread sparsity | Simple Welch | **0.01453** | 0.01076 | 0.00504 | 0.99980 | 0.94808 |
| Widespread sparsity | Expanded Welch | 0.02131 | 0.01439 | **0.00463** | 0.99143 | 0.96087 |
| Widespread sparsity | Custom Welch | 0.01457 | **0.01064** | 0.00500 | 0.99980 | 0.94737 |
| Equal-MI shape mismatch | Normal Wald | 0.00690 | **0.00420** | 0.00153 | 1.00000 | 0.94695 |
| Equal-MI shape mismatch | Simple Welch | **0.00688** | 0.00424 | **0.00149** | 1.00000 | 0.94715 |
| Equal-MI shape mismatch | Expanded Welch | 0.00715 | 0.00443 | 0.00158 | 1.00000 | 0.94847 |
| Equal-MI shape mismatch | Custom Welch | 0.00690 | **0.00420** | 0.00153 | 1.00000 | 0.94695 |
| Extreme sample imbalance | Normal Wald | 0.01177 | 0.00876 | 0.00497 | 1.00000 | 0.94384 |
| Extreme sample imbalance | Simple Welch | 0.01108 | 0.00801 | 0.00452 | 1.00000 | 0.94467 |
| Extreme sample imbalance | Expanded Welch | **0.00880** | **0.00582** | **0.00205** | 1.00000 | 0.94890 |
| Extreme sample imbalance | Custom Welch | **0.00880** | **0.00582** | **0.00205** | 1.00000 | 0.94890 |
| Support instability | Normal Wald | **0.02162** | **0.01465** | **0.00415** | 0.97569 | 0.96119 |
| Support instability | Simple Welch | 0.02274 | 0.01606 | 0.00445 | 0.97569 | 0.96262 |
| Support instability | Expanded Welch | 0.03405 | 0.02074 | 0.00544 | 0.90405 | 0.96839 |
| Support instability | Custom Welch | **0.02162** | **0.01465** | **0.00415** | 0.97569 | 0.96119 |

Expanded Welch continued to improve the three original sparse regimes and
was especially useful under extreme sample imbalance. At $\alpha=0.05$, it
reduced error relative to normal Wald by 35.8% in sparse-and-imbalanced
tables, 21.2% in the highly sparse set, 20.5% in the ultra-sparse set, and
33.6% under $1{:}10$ or $1{:}20$ imbalance. At $\alpha=0.01$, the respective
reductions were 49.2%, 23.6%, 26.2%, and 58.7%.

The additional regimes also identify the boundary. Under widespread
sparsity, expanded Welch became too conservative at $\alpha=0.05$ and its
mean valid rate fell to 0.99143. Under support instability it had 0.90405 mean
validity, with a worst scenario valid rate of 0.2947, and was less calibrated
than normal Wald when it did return a result. Shape mismatch alone produced
similar accuracy for all four methods and no advantage for expanded Welch.

The correction was also not beneficial in well-sampled tables,
expanded Welch rejected too rarely and increased mean error at
$\alpha=0.05$ from 0.00326 to 0.00466. Simple Welch remained very close to
normal Wald across all regimes because its effective degrees of freedom were
usually large.

All calculations were valid outside the widespread-sparsity and
support-instability regimes. Across scenarios, median simple-Welch degrees of
freedom ranged from 30 to approximately 1,584,000, while median expanded-Welch
degrees of freedom ranged from 3.6 to 301,000. Very small expanded degrees of
freedom correctly signal instability, but in the support boundary they can
also make the method undefined or excessively conservative.

Custom Welch followed normal Wald in the well-sampled, moderate,
widespread-sparsity, shape-mismatch, and support-instability regimes. It
followed expanded Welch throughout the $4{:}1$, $10{:}1$, and $20{:}1$
designs, while the mixed highly sparse and ultra-sparse regimes used one route
for each sample-size variant. Across all 216 scenarios, its mean absolute FPR
error was 0.00573 at $\alpha=0.05$ and 0.00220 at $\alpha=0.01$. The
corresponding Wald errors were 0.00636 and 0.00272, while expanded-Welch errors
were 0.00698 and 0.00234. Custom Welch retained Wald's mean valid rate of
0.99728 rather than expanded Welch's 0.98839.

### 10.3 Power

The power experiment uses five $3\times3$ alternatives that vary the true MI
difference and sample size.

| True MI difference | Sample size per group | Normal | Simple Welch | Expanded Welch | Custom Welch |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.02 | 300 | 0.0768 | 0.0759 | 0.0689 | 0.0768 |
| 0.05 | 300 | 0.2775 | 0.2761 | 0.2652 | 0.2775 |
| 0.10 | 300 | 0.7449 | 0.7437 | 0.7362 | 0.7449 |
| 0.05 | 150 | 0.1523 | 0.1498 | 0.1402 | 0.1523 |
| 0.05 | 600 | 0.5161 | 0.5151 | 0.5063 | 0.5161 |

Simple Welch lost 0.0014 power on average relative to normal Wald. Expanded
Welch lost 0.0102 on average and at most 0.0123. This is the expected cost of
its heavier tails. These five alternatives all used equal sample sizes, so
Custom Welch selected normal Wald and had identical power. Unequal-sample
power remains a necessary confirmatory check.

### 10.4 Runtime

The four methods were timed through the same implementation path. The runtime
scenarios had a $2{:}1$ ratio, so Custom Welch selected its normal-Wald route.

| Shape | Normal Wald | Simple Welch | Expanded Welch | Custom Welch |
| --- | ---: | ---: | ---: | ---: |
| $2\times2$ | 0.089 ms | 0.105 ms | 0.168 ms | 0.089 ms |
| $5\times5$ | 0.089 ms | 0.105 ms | 0.169 ms | 0.090 ms |
| $10\times10$ | 0.090 ms | 0.106 ms | 0.170 ms | 0.091 ms |
| $20\times20$ | 0.096 ms | 0.112 ms | 0.182 ms | 0.098 ms |

Expanded Welch was approximately 1.9 times the cost of normal Wald, but the
absolute cost remained below 0.2 ms per table pair in these measurements.
Custom Welch cost approximately normal Wald on the measured route. When it
selects expanded Welch, its cost is approximately the expanded value because
the decision itself is constant-time.

## 11. Final Interpretation

**Normal Wald** is the best default in well-sampled conditions. It is the
fastest method and already has good calibration there, but it becomes liberal
in the target sparse and imbalanced regime.

**Simple Welch-Satterthwaite** adds a small conservative correction with
almost no computational cost. Its $n-1$ assumption does not accurately
describe uncertainty in the nonlinear MI variance estimate, so its hard-case
improvement is limited.

**Expanded Welch-Satterthwaite** directly models uncertainty in the MI
variance estimator. It remains deterministic and $O(rc)$ and gives the best
calibration when isolated rare cells or unequal sample sizes make variance
estimation unstable but the sampled support remains mostly intact. Its
heavier tails make it conservative in well-sampled tables and fail to repair
widespread support loss.

**Custom Welch** uses that correction only for sample-size ratios of at least
$4{:}1$ and otherwise retains normal Wald. It had the lowest aggregate
calibration error in the current grid, preserved Wald's validity, and avoided
the equal-sample power loss of applying expanded Welch universally. The rule
is still exploratory because its threshold was selected from these same
results. A new frozen holdout must confirm it before the aggregate improvement
is treated as independent evidence.

The defensible conclusion is deliberately specific:

> Expanded Welch supplies an MI-specific finite-sample correction, and Custom
> Welch guards its use according to sample-size imbalance. The guarded rule is
> the strongest practical candidate from the development grid, but its fixed
> $4{:}1$ threshold now requires independent confirmation.

This is a simpler and stronger claim than treating the method as a universal
replacement. The complete reproducible output is in
[`results/supervisor_full/REPORT.md`](../results/supervisor_full/REPORT.md).

## Appendix A: Intuition Behind Expanded Welch-Satterthwaite

The test statistic is

$$
T
=\frac{\widehat I_{\mathrm{BC}}(P)-\widehat I_{\mathrm{BC}}(Q)}
{\sqrt{\widehat V_P/n_P+\widehat V_Q/n_Q}}.
$$

The denominator estimates how much the MI difference should fluctuate under
repeated sampling. The difficulty is that $\widehat V_P$ and $\widehat V_Q$
are themselves estimated and can be unstable in finite samples.

Normal Wald treats this remaining denominator uncertainty as negligible.
Simple Welch allows for it, but assumes each MI variance behaves like an
ordinary sample variance with $n-1$ degrees of freedom. That assumption is
questionable because

$$
\widehat V
=\sum_{i,j}\widehat p_{ij}
\left(\widehat\ell_{ij}-\widehat I\right)^2
$$

is a nonlinear function of the complete table. Changing one cell also
changes its row margin, column margin, local-information scores, MI, and
therefore the complete variance estimate.

Expanded Welch measures this sensitivity directly. For each cell, define

$$
g_P(x,y)
=\left.
\frac{\mathrm d}{\mathrm d\varepsilon}
V\!\left((1-\varepsilon)P+\varepsilon\delta_{(x,y)}\right)
\right|_{\varepsilon=0}.
$$

Thus, $g_P(x,y)$ measures how strongly cell $(x,y)$ can perturb the MI
variance. The variability of these cell sensitivities,

$$
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\},
$$

determines the first-order uncertainty of the estimated variance:

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite moment matching converts this uncertainty into component
degrees of freedom:

$$
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
$$

The interpretation is direct:

- if $g_P$ varies little across cells, $\widehat V_P$ is stable, the degrees
  of freedom are large, and the reference remains close to normal;
- if some cells have much greater influence, $\widehat V_P$ is unstable, the
  degrees of freedom fall, and the reference has heavier Student tails.

The two component degrees of freedom are then combined using the usual
Satterthwaite formula. Expanded Welch changes neither the estimated MI
difference nor its standard error; it changes only how cautiously the
observed statistic is interpreted.

This is why the method helps in sparse and skewed tables. It responds to the
actual table-dependent instability of the variance estimate rather than
assigning degrees of freedom from sample size alone. In the validation grid,
it reduced sparse-regime calibration error relative to normal Wald by about
39% at $\alpha=0.05$ and 51% at $\alpha=0.01$.

The improvement is not universal. In well-sampled tables, normal Wald is
already accurate and expanded Welch can become mildly conservative. It is
therefore best interpreted as a targeted finite-sample correction rather
than a universal replacement for normal Wald.

## Appendix B: Which Variance Does Each Method Calculate?

The easiest way to understand the calculation is to imagine repeating the
entire experiment many times. There are three levels of variation.

### B.1 Variation between individual observations

Each observation can push the estimated MI up or down. That contribution is
represented by the MI influence function:

$$
\psi_P(x,y)
=\log\!\left(\frac{p_{xy}}{p_{x+}p_{+y}}\right)-I(P).
$$

Its variance is

$$
V(P)=\operatorname{Var}_P\{\psi_P(X,Y)\}.
$$

This answers the question:

> How different are the MI contributions of individual observations?

The population quantity $V(P)$ is estimated by $\widehat V_P$.

### B.2 Variation of the estimated MI

A dataset contains $n_P$ observations. Averaging many observations reduces
variability, so

$$
\operatorname{Var}\{\widehat I(P)\}
\approx\frac{V(P)}{n_P}.
$$

This is estimated as

$$
\widehat{\operatorname{Var}}\{\widehat I(P)\}
=\frac{\widehat V_P}{n_P}.
$$

It answers the question:

> If we repeatedly collected complete datasets, how much would the estimated
> MI change?

The corresponding standard error is

$$
\operatorname{SE}\{\widehat I(P)\}
=\sqrt{\frac{\widehat V_P}{n_P}}.
$$

For two independent populations, the variances add:

$$
\widehat{\operatorname{SE}}^2
=\frac{\widehat V_P}{n_P}
+\frac{\widehat V_Q}{n_Q}.
$$

This is the estimated sampling variance of the MI difference. Normal Wald,
simple Welch, and expanded Welch all use this same quantity in the denominator
of

$$
T
=\frac{\widehat\Delta_{\mathrm{BC}}}
{\sqrt{\widehat V_P/n_P+\widehat V_Q/n_Q}}.
$$

### B.3 Variation of the estimated variance

The values $\widehat V_P$ and $\widehat V_Q$ are not known population values.
They are calculated from finite tables. If the complete experiment were
repeated, each dataset would produce a different value of $\widehat V_P$.
Therefore, the variance estimate has its own sampling variance:

$$
\operatorname{Var}(\widehat V_P).
$$

This answers the question:

> How much would our estimated MI variance change between repeated datasets?

This is a variance of a variance estimate. It measures how reliable the
estimated standard error is.

#### Simple Welch-Satterthwaite

Simple Welch assumes approximately

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{2V(P)^2}{n_P-1}.
$$

This is the conventional sample-variance assumption. Equivalently, simple
Welch assigns

$$
\nu_{V,P}=n_P-1.
$$

#### Expanded Welch-Satterthwaite

Expanded Welch derives the uncertainty of the complete MI variance estimator:

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P},
$$

where $\tau_P^2$ measures how sensitive the complete MI variance calculation
is to individual cells. This produces the MI-specific component degrees of
freedom

$$
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
$$

### B.4 Numerical example

Suppose

$$
\widehat V_P=0.8,
\qquad
n_P=100,
$$

and

$$
\widehat V_Q=1.2,
\qquad
n_Q=150.
$$

The estimated variance of the MI difference is

$$
\begin{aligned}
\widehat{\operatorname{SE}}^2
&=\frac{0.8}{100}+\frac{1.2}{150}\\
&=0.008+0.008\\
&=0.016.
\end{aligned}
$$

Therefore,

$$
\widehat{\operatorname{SE}}
=\sqrt{0.016}
\approx0.126.
$$

Normal Wald, simple Welch, and expanded Welch all use this same standard
error. They differ only in how confident they are in the estimated values
$0.8$ and $1.2$:

- normal Wald treats them as sufficiently reliable;
- simple Welch uses the generic $n-1$ reliability rule;
- expanded Welch calculates their reliability from the MI table.

### B.5 Complete map

| Level | Quantity | Question |
| --- | --- | --- |
| Individual observation | $V(P)$ | How variable are individual MI contributions? |
| MI estimator | $V(P)/n_P$ | How variable is $\widehat I(P)$? |
| Variance estimator | $\operatorname{Var}(\widehat V_P)$ | How reliable is the estimated MI variance? |
| MI difference | $V(P)/n_P+V(Q)/n_Q$ | How variable is $\widehat I(P)-\widehat I(Q)$? |

The crucial distinction is

$$
\widehat V_P
\ne
\operatorname{Var}(\widehat V_P).
$$

The first quantity is an estimated variance used to construct the MI standard
error. The second quantity measures how uncertain that estimated variance is.
Expanded Welch specifically improves the calculation of the second quantity.
