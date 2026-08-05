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

Four methods form the complete comparison:

| Method | How $T$ is calibrated |
| --- | --- |
| Normal Wald | Standard normal distribution |
| Studentized permutation | Empirical distribution from repeated group-label permutations |
| Simple Welch-Satterthwaite | Student distribution using $n-1$ component degrees of freedom |
| Expanded Welch-Satterthwaite | Student distribution using MI-specific variance-influence degrees of freedom |

The central research contribution is the expanded Welch-Satterthwaite method.
It attempts to retain the speed of an analytic test while improving
calibration in skewed, low-expected-count tables.

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

**Chung and Romano (2013).** Their general permutation theory supports using
a studentized statistic when testing equality of a parameter across
heterogeneous groups. This motivates the studentized permutation benchmark.

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
- Chung and Romano: <https://doi.org/10.1214/13-AOS1090>

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

## 5. Method 2: Studentized Permutation

### How it works

Studentized permutation uses the same observed statistic $T_{\mathrm{obs}}$.
It then:

1. pools the two groups;
2. randomly permutes group labels while preserving $n_P$ and $n_Q$;
3. rebuilds both tables;
4. recomputes the complete bias-corrected, studentized statistic $T_b^*$;
5. repeats this process $B$ times.

The two-sided Monte Carlo p-value is

$$
p_{\mathrm{perm}}
=\frac{
1+\sum_{b=1}^{B}
\mathbf 1\{|T_b^*|\ge |T_{\mathrm{obs}}|\}
}{B+1}.
$$

Studentization is important because the groups may have different
distributions and variance structures even when their MI values are equal.

### Interpretation

Permutation constructs a reference distribution from repeated reallocations
instead of choosing a normal or Student distribution analytically. It can
capture more finite-sample behaviour, but its p-values are random and have
resolution approximately $1/(B+1)$.

### Cost

An optimized table-level implementation costs approximately

$$
O(Brc),
$$

while explicitly shuffling raw observations can add $O(Bn)$ work.

## 6. Method 3: Simple Welch-Satterthwaite

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

## 7. Method 4: Expanded Welch-Satterthwaite

### Why expand the simple method?

The simple method assumes that each MI variance estimate has approximately
$n-1$ degrees of freedom. Empirical diagnostics found that this was much
too large in difficult tables. The expanded method estimates the effective
degrees of freedom from the actual uncertainty of the nonlinear MI variance
functional.

### How it works

Let $V(P)$ be the population MI influence variance. Define $g_P(X,Y)$ as
the influence function of $V(P)$. In plain language, $g_P(x,y)$ measures
how much the complete MI variance would change after a very small increase in
the probability of cell $(x,y)$, including the induced changes to cell,
row, column, and MI terms.

Let

$$
\tau_P^2
=\operatorname{Var}_P\{g_P(X,Y)\}.
$$

First-order theory gives

$$
\operatorname{Var}(\widehat V_P)
\approx\frac{\tau_P^2}{n_P}.
$$

Satterthwaite moment matching approximates $\widehat V_P$ by a scaled
chi-squared variable. Matching its variance gives the MI-specific component
degrees of freedom:

$$
\nu_{V,P}
=\frac{2n_PV(P)^2}{\tau_P^2}.
$$

In practice, the unknown population quantities are replaced by estimates:

$$
\widehat\nu_{V,P}
=\frac{2n_P\widehat V_P^2}{\widehat\tau_P^2},
\qquad
\widehat\nu_{V,Q}
=\frac{2n_Q\widehat V_Q^2}{\widehat\tau_Q^2}.
$$

The final degrees of freedom are

$$
\nu_{\mathrm{expanded}}
=\frac{(a+b)^2}
{a^2/\widehat\nu_{V,P}+b^2/\widehat\nu_{V,Q}},
$$

and

$$
p_{\mathrm{expanded}}
=2\Pr\{t_{\nu_{\mathrm{expanded}}}\ge |T|\}.
$$

### Interpretation

If an MI variance estimate is stable, $\widehat\tau^2$ is small and the
method assigns many degrees of freedom. If it is highly sample-dependent,
$\widehat\tau^2$ is large, the degrees of freedom fall, and the Student
reference becomes more conservative.

The expanded calculation targets the main weakness of simple Welch. It is
still an approximation because $T$'s numerator and denominator are
estimated from the same tables and can be correlated.

### Cost

The influence calculation requires additional row, column, and cell
reductions, but still scans the table only a fixed number of times:

$$
O(rc).
$$

Its exact measured constant-factor overhead has not yet been benchmarked in
the primary implementation.

## 8. Method Map

| Feature | Normal Wald | Permutation | Simple Welch | Expanded Welch |
| --- | --- | --- | --- | --- |
| Effect estimate | Same bias-corrected MI difference | Same statistic recomputed repeatedly | Same | Same |
| Standard error | MI influence variance | Same formula recomputed repeatedly | Same | Same |
| Reference | Normal | Empirical | Student | Student |
| Variance uncertainty | Ignored | Captured through repeated reallocations | Approximated by $n-1$ | Derived from MI variance influence |
| Deterministic | Yes | No | Yes | Yes |
| Complexity | $O(rc)$ | Approximately $O(Brc)$ | $O(rc)$ | $O(rc)$ |
| Main role | Analytic baseline | Resampling baseline | Simple finite-df correction | Proposed analytic method |

## 9. Experimental Sets

### 9.1 Broad sets

A broad population set contains 72 equal-MI pairs:

$$
12\ \text{table shapes}\times6\ \text{sampling designs}=72.
$$

Shapes range from $2\times2$ to $20\times20$, including square and
rectangular tables. The six designs span:

- nearly uniform to heterogeneous margins;
- target MI values 0.03, 0.07, and 0.15 nats;
- sample-size ratios $1{:}1$, $1{:}2$, and $1{:}4$;
- high to low baseline observations per cell.

The broad set intentionally mixes easy, moderate, and difficult conditions.
It checks whether a correction remains safe across ordinary use, not only
whether it works in selected hard cases.

The simple-method validation used two independently generated broad sets,
giving 144 populations with 5,000 table-pair replicates each.

The expanded-method evaluation used one new 72-population broad set with 10,000
replicates per population.

### 9.2 Hard set A

Hard set A contains 12 low-density, unequal-sample population pairs generated
from two separate population seeds. It uses six shapes:

$$
2\times2,\ 2\times5,\ 3\times7,\ 4\times6,\ 5\times5,\ 5\times10.
$$

These configurations use target MI 0.15 nats, a $1{:}4$ sample-size ratio,
heterogeneous margins, and low baseline density.

The expanded-method evaluation generated 20,000 new table pairs for each
population:

$$
12\times20{,}000=240{,}000.
$$

### 9.3 Fresh hard subset B

Fresh hard subset B contains six difficult design-5 populations selected from
the new broad 72-set. It is a subset of the broad set, not an extra set.

Each received 10,000 replicates as part of the broad simulation.

### 9.4 Permutation anchors

The permutation comparison used the 12 hard set A populations. For each
population:

- 1,000 outer table pairs were generated;
- each table pair received 999 studentized permutations.

This experiment compared normal Wald, simple Welch, and permutation on the
same table pairs. The saved permutation experiment did not include expanded
Welch.

### 9.5 Which methods were compared where?

| Experiment | Normal | Permutation | Simple Welch | Expanded Welch |
| --- | ---: | ---: | ---: | ---: |
| Broad and hard simple-method validation | Yes | Hard anchors only | Yes | No |
| 960,000-pair expanded-method evaluation | Yes | No | Yes | Yes |

This separation is important. The current data compare expanded Welch with
normal and simple Welch, but do not yet compare expanded Welch directly with
permutation.

## 10. Results

### 10.1 Accuracy metric

For a nominal level $\alpha$, a calibrated method should reject
approximately an $\alpha$ fraction of true null cases. For each scenario,

$$
\operatorname{FPR\ error}
=|\operatorname{FPR}-\alpha|.
$$

The tables report mean absolute FPR error across each set. Lower is better.

### 10.2 Normal, simple Welch, and expanded Welch

| Population set | $\alpha$ | Normal Wald | Simple Welch | Expanded Welch |
| --- | ---: | ---: | ---: | ---: |
| Hard A, 12 | 0.10 | 0.01677 | 0.01565 | **0.01213** |
| Hard A, 12 | 0.05 | 0.01270 | 0.01169 | **0.00823** |
| Hard A, 12 | 0.01 | 0.00568 | 0.00506 | **0.00266** |
| Fresh hard B, 6 | 0.10 | 0.01553 | 0.01430 | **0.01167** |
| Fresh hard B, 6 | 0.05 | 0.00993 | 0.00912 | **0.00662** |
| Fresh hard B, 6 | 0.01 | 0.00407 | 0.00360 | **0.00232** |
| Broad, 72 | 0.10 | 0.00658 | **0.00640** | 0.00665 |
| Broad, 72 | 0.05 | 0.00463 | **0.00445** | 0.00446 |
| Broad, 72 | 0.01 | 0.00200 | 0.00190 | **0.00173** |

The storyline is clear:

- Normal Wald is already accurate on average in the broad set, but is too
  liberal in the hard sets.
- Simple Welch makes a small conservative improvement in hard cases and
  changes broad performance very little.
- Expanded Welch gives a substantially larger improvement in both hard sets.
- Expanded Welch is effectively tied with simple Welch at broad
  $\alpha=0.05$, slightly worse at broad $\alpha=0.10$, and better at
  broad $\alpha=0.01$.

Relative to simple Welch, expanded Welch reduced hard-regime error by about
18-47%, with its largest gain in the $\alpha=0.01$ tail.

Expanded Welch is therefore strongest in the target difficult regime, but it
is not uniformly best in every broad scenario or at every significance level.

### 10.3 Permutation comparison

On the 12 hard permutation anchors at $\alpha=0.05$:

| Method | Mean FPR | Mean absolute FPR error | In 0.035-0.065 band |
| --- | ---: | ---: | ---: |
| Normal Wald | 0.06208 | 0.01208 | 66.67% |
| Studentized permutation | **0.05458** | **0.00642** | **100.00%** |
| Simple Welch | 0.06083 | 0.01100 | 75.00% |

Permutation was more accurate than normal Wald and simple Welch on these hard
anchors. This establishes permutation as the stronger existing accuracy
benchmark.

It does not yet show whether permutation is more accurate than expanded
Welch, because expanded Welch was not included in this run.

### 10.4 Power

The available power experiment compares normal Wald and simple Welch across
five $3\times3$ alternatives. Simple Welch's mean absolute power loss was
only 0.00154, with a maximum loss of 0.0032.

| True MI difference | Sample size per group | Normal power | Simple Welch power |
| ---: | ---: | ---: | ---: |
| 0.05 | 300 | 0.2776 | 0.2761 |
| 0.10 | 300 | 0.7438 | 0.7419 |

Expanded Welch still needs a comparable power experiment.

### 10.5 Runtime

Measured median single-pair times were:

| Method | Median time |
| --- | ---: |
| Normal Wald | 0.117 ms |
| 999 optimized studentized permutations | 3.006 ms |
| Simple Welch | 0.128 ms |

Simple Welch added about 0.011 ms over normal Wald. Expanded Welch remains
$O(rc)$, but its integrated constant-factor runtime has not yet been
measured. Permutation is slower because it recalculates the test many times.

## 11. Final Interpretation

**Normal Wald** is the clean analytic baseline. It is fast and works well in
many broad regular cases, but it can be liberal in skewed, low-count tables.

**Studentized permutation** produced the best hard-anchor calibration in the
available resampling comparison. It is more computationally expensive and has
not yet been compared directly with expanded Welch.

**Simple Welch-Satterthwaite** adds a small conservative correction with
almost no computational cost. Its $n-1$ assumption does not accurately
describe uncertainty in the nonlinear MI variance estimate, so its hard-case
improvement is limited.

**Expanded Welch-Satterthwaite** directly models uncertainty in the MI
variance estimator. It remains deterministic and $O(rc)$, and it produced
the strongest analytic hard-regime results. Its broad performance is mixed
but close to the simpler methods on average.

The next decisive experiment is therefore straightforward:

> Freeze expanded Welch and compare it head-to-head with normal Wald,
> studentized permutation, and simple Welch on one untouched set of broad and hard
> populations, while measuring calibration, power, and runtime.

That experiment will determine whether expanded Welch provides a useful
analytic middle ground: much faster than permutation while approaching its
finite-sample accuracy in the skewed, low-count regime.
