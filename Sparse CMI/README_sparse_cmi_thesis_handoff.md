# Sparse Conditional Mutual Information Significance Test

## Handoff brief

This document specifies a proposed thesis project for testing whether a fast finite-sample significance method for **binary discrete conditional mutual information (CMI)** is mathematically valid, empirically calibrated, computationally useful, and sufficiently novel.

The central idea is to import methods from classical sparse contingency-table inference into information theory.

The project should **not** begin by assuming the method works. The first objective is to try to falsify it quickly.

---

## 1. Project objective

Develop and test a significance procedure for

\[
H_0: X \perp Y \mid Z
\]

where:

- \(X \in \{0,1\}\)
- \(Y \in \{0,1\}\)
- \(Z \in \{1,\ldots,K\}\)
- observations \((X_i,Y_i,Z_i)\) are initially assumed i.i.d.

The method should target the **many-sparse-strata regime**, where:

- the number of observed conditioning states \(K\) may be large
- each \(Z=z\) stratum may contain few observations
- the standard chi-squared null for \(2N\widehat I(X;Y\mid Z)\) may be badly calibrated

The proposed procedure should:

1. condition on the observed \(X\)-\(Z\) and \(Y\)-\(Z\) margins
2. calculate the exact finite-sample cumulants of each stratum contribution
3. aggregate the cumulants across strata
4. use a normal or higher-order approximation for the total statistic
5. approach the calibration of conditional permutation testing at much lower computational cost

---

## 2. Main research question

> Can exact conditional cumulants and a higher-order Gaussian approximation provide calibrated, computationally efficient significance tests for binary discrete conditional mutual information when the conditioning space contains many sparsely observed states?

Supporting questions:

1. Under what conditions does the standardised CMI statistic converge to a normal distribution?
2. How much finite-sample error is removed by exact centring and scaling?
3. Does a skewness correction materially improve upper-tail calibration?
4. Can observable diagnostics identify configurations where the approximation is unreliable?
5. How does the method compare with conditional permutation testing in type-I error, power, runtime, and memory?
6. Is the method sufficiently different from existing sparse contingency-table and discrete-CMI methods to constitute a defensible thesis contribution?

---

## 3. Statistical setup

For \(N\) observations, define the empirical CMI in nats as

\[
\widehat I(X;Y\mid Z)
=
\sum_{z=1}^{K}
\frac{n_z}{N}
\widehat I(X;Y\mid Z=z),
\]

where \(n_z\) is the number of observations with \(Z=z\).

The corresponding likelihood-ratio statistic is

\[
G^2
=
2N\widehat I(X;Y\mid Z)
=
\sum_{z=1}^{K}G_z^2,
\]

where

\[
G_z^2
=
2n_z\widehat I(X;Y\mid Z=z).
\]

For binary \(X\) and \(Y\), the standard asymptotic result is approximately

\[
G^2 \sim \chi^2_K
\]

when all \(K\) strata are regular and well populated.

The proposed project targets settings where many strata are too sparse for the per-stratum Wilks approximation to be reliable.

---

## 4. Exact conditional null within one stratum

For a fixed stratum \(z\), write the \(2\times2\) table as

| | \(Y=1\) | \(Y=0\) | Total |
|---|---:|---:|---:|
| \(X=1\) | \(a_z\) | \(r_z-a_z\) | \(r_z\) |
| \(X=0\) | \(s_z-a_z\) | \(n_z-r_z-s_z+a_z\) | \(n_z-r_z\) |
| Total | \(s_z\) | \(n_z-s_z\) | \(n_z\) |

Definitions:

- \(n_z\): stratum size
- \(r_z\): number of \(X=1\) observations
- \(s_z\): number of \(Y=1\) observations
- \(a_z\): number of observations with \(X=1,Y=1\)

Condition on \((n_z,r_z,s_z)\). Under

\[
H_0:X\perp Y\mid Z=z,
\]

the free cell count satisfies

\[
A_z \mid n_z,r_z,s_z
\sim
\operatorname{Hypergeometric}(n_z,s_z,r_z),
\]

with probability mass function

\[
P(A_z=a)
=
\frac{
\binom{s_z}{a}
\binom{n_z-s_z}{r_z-a}
}{
\binom{n_z}{r_z}
},
\]

for

\[
a_{\min,z}
=
\max(0,r_z+s_z-n_z)
\]

through

\[
a_{\max,z}
=
\min(r_z,s_z).
\]

This conditional distribution removes the nuisance probabilities

\[
P(X=1\mid Z=z)
\quad\text{and}\quad
P(Y=1\mid Z=z).
\]

---

## 5. Stratum-level likelihood-ratio contribution

For an attainable value \(a\), define

\[
\begin{aligned}
o_{11}&=a,\\
o_{10}&=r_z-a,\\
o_{01}&=s_z-a,\\
o_{00}&=n_z-r_z-s_z+a.
\end{aligned}
\]

The expected counts under independence are

\[
e_{ij}
=
\frac{o_{i\cdot}o_{\cdot j}}{n_z}.
\]

Define

\[
g_z(a)
=
2\sum_{i,j}
o_{ij}\log\left(\frac{o_{ij}}{e_{ij}}\right),
\]

using the convention

\[
0\log 0 = 0.
\]

Then

\[
G_z^2=g_z(A_z)
\]

is a deterministic transformation of a finite-support hypergeometric random variable.

The observed total statistic is

\[
G_{\mathrm{obs}}^2
=
\sum_z g_z(a_z).
\]

---

## 6. Exact conditional moments and cumulants

For each stratum, calculate raw moments

\[
m_{q,z}
=
E[(G_z^2)^q\mid n_z,r_z,s_z]
=
\sum_{a=a_{\min,z}}^{a_{\max,z}}
P(A_z=a)g_z(a)^q.
\]

At minimum calculate \(q=1,2,3\). Preferably also calculate \(q=4\).

First cumulant:

\[
\kappa_{1,z}
=
\mu_z
=
m_{1,z}.
\]

Second cumulant:

\[
\kappa_{2,z}
=
\sigma_z^2
=
m_{2,z}-m_{1,z}^2.
\]

Third cumulant:

\[
\kappa_{3,z}
=
m_{3,z}
-
3m_{2,z}m_{1,z}
+
2m_{1,z}^3.
\]

Fourth cumulant:

\[
\kappa_{4,z}
=
E[(G_z^2-\mu_z)^4]
-
3\sigma_z^4.
\]

Conditional on all observed stratum margins, the stratum tables are independent. Therefore cumulants add:

\[
\kappa_j
=
\sum_z \kappa_{j,z}.
\]

In particular,

\[
\mu
=
\kappa_1
=
\sum_z\mu_z,
\]

\[
\sigma^2
=
\kappa_2
=
\sum_z\sigma_z^2,
\]

\[
\kappa_3
=
\sum_z\kappa_{3,z}.
\]

Aggregate standardised skewness is

\[
\gamma_1
=
\frac{\kappa_3}{\kappa_2^{3/2}}.
\]

---

## 7. Candidate null approximations

### 7.1 Exact-moment normal approximation

Define

\[
T
=
\frac{G_{\mathrm{obs}}^2-\mu}{\sigma}.
\]

Approximate

\[
T\sim N(0,1).
\]

Approximate upper-tail p-value:

\[
p_{\mathrm{normal}}
=
1-\Phi(T).
\]

This approximation corrects the null mean and variance rather than imposing the chi-squared values \(K\) and \(2K\).

### 7.2 Cornish-Fisher critical value

For upper-tail level \(\alpha\), let \(z_{1-\alpha}\) be the standard normal quantile.

Use

\[
q_{1-\alpha}^{\mathrm{CF}}
=
\mu
+
\sigma
\left[
z_{1-\alpha}
+
\frac{\gamma_1}{6}
\left(z_{1-\alpha}^2-1\right)
\right].
\]

Reject when

\[
G_{\mathrm{obs}}^2
\geq
q_{1-\alpha}^{\mathrm{CF}}.
\]

This is the minimum higher-order extension that should be tested.

### 7.3 Edgeworth p-value

Also test a first-order Edgeworth approximation to the standardised CDF:

\[
F_T(t)
\approx
\Phi(t)
+
\frac{\gamma_1}{6}
(1-t^2)\phi(t).
\]

Then

\[
p_{\mathrm{Edgeworth}}
=
1-F_T(T).
\]

Check monotonicity and clip numerical values to \([0,1]\) only for reporting. Clipping does not repair a theoretically invalid approximation.

### 7.4 Optional saddlepoint fallback

If the normal and skewness-corrected approximations fail in important regimes, construct the exact conditional cumulant-generating function.

For each stratum:

\[
M_z(t)
=
E[e^{tG_z^2}]
=
\sum_a P(A_z=a)e^{tg_z(a)}.
\]

Aggregate:

\[
K(t)
=
\sum_z\log M_z(t).
\]

This may support a Lugannani-Rice saddlepoint approximation to the upper tail.

Do not implement this first. It is a fallback if the simpler method is promising but insufficiently accurate.

---

## 8. Proposed asymptotic result

Let the number of observed conditioning states depend on sample size and be denoted \(K_N\).

Define

\[
W_{Nz}
=
G_{Nz}^2-\mu_{Nz},
\]

and

\[
s_N^2
=
\sum_{z=1}^{K_N}\sigma_{Nz}^2.
\]

Conditional on the observed margins, the \(W_{Nz}\) are independent but generally non-identically distributed.

Define the Lyapunov or Berry-Esseen quantity

\[
L_N
=
\frac{
\sum_{z=1}^{K_N}
E[|W_{Nz}|^3]
}{
s_N^3
}.
\]

A target theorem is:

> If \(s_N^2\to\infty\) and \(L_N\to0\), then, conditional on the observed margins,
>
> \[
> \frac{
> \sum_zG_{Nz}^2-\sum_z\mu_{Nz}
> }{
> \sqrt{\sum_z\sigma_{Nz}^2}
> }
> \overset{d}{\longrightarrow}
> N(0,1).
> \]

A direct Berry-Esseen inequality should have the form

\[
\sup_x
\left|
P\left(
\frac{\sum_zW_{Nz}}{s_N}\leq x
\mid \text{margins}
\right)
-
\Phi(x)
\right|
\leq
C L_N
\]

for a universal constant \(C\).

### Candidate sufficient conditions

Try to prove a useful corollary under assumptions such as:

1. stratum sizes are uniformly bounded, or their maximum grows sufficiently slowly
2. a non-vanishing proportion of strata have positive conditional variance
3. no single stratum dominates total variance
4. total conditional variance diverges

A useful no-dominance diagnostic is

\[
D_N
=
\frac{
\max_z\sigma_{Nz}^2
}{
\sum_z\sigma_{Nz}^2
}.
\]

A sufficient condition should imply

\[
D_N\to0.
\]

The theorem must be stated as a **conditional theorem given the observed margins**.

---

## 9. Required falsification tests

Before investing in a full proof or JIDT implementation, attempt to disprove the practical value of the method.

### Falsification test A: exact enumeration

For small and moderate configurations, enumerate the full joint conditional null exactly.

Because strata are independent, calculate the exact distribution of

\[
G^2=\sum_zG_z^2
\]

by repeated discrete convolution.

Compare:

- exact upper-tail probabilities
- chi-squared approximation
- exact-moment normal approximation
- Cornish-Fisher approximation
- Edgeworth approximation

The method is not promising if corrected upper-tail errors remain large across the intended regime.

### Falsification test B: adversarial heterogeneous strata

Construct mixtures containing:

- many degenerate strata
- a few high-variance strata
- highly unequal \(n_z\)
- highly unequal margins
- one dominant stratum plus many nearly deterministic strata
- mixed balanced and extremely skewed margins

The method should fail when one or a few strata dominate. Verify that proposed diagnostics detect this failure.

### Falsification test C: small number of informative strata

Keep \(K\) large but make only \(2\), \(3\), \(5\), or \(10\) strata informative.

This tests whether nominal \(K\) is misleading and whether total variance and no-dominance diagnostics are more useful.

### Falsification test D: very small significance levels

Test at:

\[
\alpha\in\{0.10,0.05,0.01,0.001\}.
\]

Network inference often requires accurate far-tail probabilities. A method that works only at \(0.05\) may be inadequate.

### Falsification test E: discrete support effects

Determine whether the continuous approximation becomes systematically anti-conservative because the exact null has coarse support.

Compare:

- ordinary upper-tail p-values
- conservative attainable critical values
- mid-p values
- randomised p-values, if theoretically useful

Do not hide discreteness through interpolation without explaining the consequence.

---

## 10. Simulation design

### 10.1 Core null grid

Vary:

- \(K \in \{5,10,20,50,100,200\}\)
- average stratum size in \(\{3,5,10,20,50\}\)
- balanced and skewed \(X\mid Z\) marginals
- balanced and skewed \(Y\mid Z\) marginals
- equal and unequal stratum sizes
- homogeneous and heterogeneous stratum probabilities
- proportions of degenerate strata
- proportions of empty theoretical states

Possible marginal probabilities:

\[
p_X,p_Y\in\{0.05,0.10,0.25,0.50,0.75,0.90,0.95\}.
\]

Do not use only symmetric settings such as \(p_X=p_Y\).

### 10.2 Two ways to condition

Run two distinct simulation families.

#### Fixed-margin conditional simulations

Fix every \((n_z,r_z,s_z)\), then sample

\[
A_z
\sim
\operatorname{Hypergeometric}(n_z,s_z,r_z).
\]

This directly tests the conditional method.

#### Unconditional data-generating simulations

Generate \(Z\), then generate independent \(X\mid Z\) and \(Y\mid Z\). Recalculate the observed margins on every replicate.

This tests the unconditional repeated-sampling behaviour of the conditionally valid procedure.

Keep these interpretations separate.

### 10.3 Alternative distributions for power

Use a stratum odds-ratio alternative.

For fixed margins, generate \(A_z\) from a noncentral hypergeometric distribution with odds ratio \(\theta_z\).

Test:

- common weak dependence
- common moderate dependence
- dependence in only a subset of strata
- heterogeneous dependence strength
- positive association in some strata and negative association in others

Suggested odds ratios:

\[
\theta_z\in\{1.2,1.5,2,3\}
\]

and reciprocals for negative association.

### 10.4 Number of repetitions

Use enough repetitions to estimate tail error meaningfully.

For \(\alpha=0.05\), at least \(10^5\) replicates are desirable for final calibration estimates.

For \(\alpha=0.001\), substantially more may be needed unless exact convolution is used.

Start with smaller exploratory runs, then increase only for selected configurations.

---

## 11. Benchmark methods

Compare against:

1. standard chi-squared null
2. chi-squared using only observed or informative strata
3. Bartlett or Williams-style correction where applicable
4. exact-moment normal approximation
5. Cornish-Fisher correction
6. Edgeworth approximation
7. conditional permutation test within each \(Z\) stratum
8. exact conditional enumeration or convolution where feasible
9. any recent adjusted-degrees-of-freedom discrete-CMI method found in the literature

The standard JIDT discrete CMI permutation implementation should not automatically be treated as the ground truth if it globally shuffles one variable rather than permuting within \(Z\) strata. Verify its null construction before benchmarking against it.

---

## 12. Evaluation metrics

### Calibration

Report:

- empirical type-I error
- absolute size distortion
- relative size distortion
- p-value QQ plots
- rejection calibration curves
- Kolmogorov distance
- upper-tail quantile error
- upper-tail probability error

### Power

Report:

- power at fixed nominal levels
- power relative to exact conditional testing
- whether improved calibration trades off materially against power

### Computation

Report:

- wall-clock runtime
- number of arithmetic operations where useful
- memory usage
- scaling with \(N\)
- scaling with \(K\)
- scaling with total support width

### Diagnostic performance

Test whether these quantities predict approximation error:

\[
L_N
=
\frac{\sum_zE|W_z|^3}{(\sum_z\sigma_z^2)^{3/2}},
\]

\[
D_N
=
\frac{\max_z\sigma_z^2}{\sum_z\sigma_z^2},
\]

\[
|\gamma_1|,
\]

number of informative strata,

\[
K_{\mathrm{info}}
=
\#\{z:\sigma_z^2>0\},
\]

and total variance

\[
\sum_z\sigma_z^2.
\]

The formal Berry-Esseen bound may be too loose for direct practical use. Test empirical predictive value rather than assuming it is a useful certificate.

---

## 13. Computational complexity

For stratum \(z\), the support width is

\[
w_z
=
a_{\max,z}-a_{\min,z}+1.
\]

Exact moment calculation costs approximately

\[
O\left(\sum_zw_z\right).
\]

Since

\[
w_z\leq n_z+1
\]

and

\[
\sum_zn_z=N,
\]

the total cost should be near-linear in \(N\), excluding special-function overhead.

A permutation test with \(B\) resamples generally costs approximately

\[
O(BN).
\]

This expected speed advantage must be benchmarked in real implementations rather than claimed from asymptotic notation alone.

---

## 14. Numerical implementation requirements

### Hypergeometric probabilities

Avoid direct factorial calculations.

Use either:

- log-gamma functions
- a trusted hypergeometric PMF implementation
- a stable recurrence

A useful recurrence is

\[
\frac{P(A=a+1)}{P(A=a)}
=
\frac{
(s-a)(r-a)
}{
(a+1)(n-s-r+a+1)
}.
\]

Normalise probabilities after recurrence to control accumulated floating-point error.

### Likelihood-ratio terms

For every cell count \(o\):

- contribute zero when \(o=0\)
- never evaluate \(\log 0\)
- handle zero expected counts only in degenerate tables where the corresponding observed count must also be zero

### Degenerate strata

A stratum may have zero conditional variance when:

- \(X\) is constant
- \(Y\) is constant
- the margins force a unique table

Such strata should be retained in the observed statistic if they contribute a constant, but excluded from variance and informative-stratum counts.

### Variance guard

If aggregate variance is zero, no stochastic test is available under the conditional null. Return a clearly defined result rather than divide by zero.

### Reproducibility

All Monte Carlo experiments must:

- accept a random seed
- record the seed
- record package versions
- save configuration metadata
- permit exact reproduction of every reported table and figure

---

## 15. Suggested repository structure

```text
sparse-cmi/
├── README.md
├── pyproject.toml
├── requirements.txt
├── src/
│   └── sparse_cmi/
│       ├── __init__.py
│       ├── tables.py
│       ├── statistic.py
│       ├── hypergeom.py
│       ├── moments.py
│       ├── approximations.py
│       ├── exact_convolution.py
│       ├── permutation.py
│       ├── diagnostics.py
│       └── simulation.py
├── tests/
│   ├── test_tables.py
│   ├── test_statistic.py
│   ├── test_hypergeom.py
│   ├── test_moments.py
│   ├── test_exact_convolution.py
│   ├── test_permutation_equivalence.py
│   └── test_edge_cases.py
├── experiments/
│   ├── 01_single_stratum_validation.py
│   ├── 02_exact_convolution_validation.py
│   ├── 03_null_calibration_grid.py
│   ├── 04_adversarial_regimes.py
│   ├── 05_power_grid.py
│   ├── 06_runtime_benchmark.py
│   └── 07_diagnostic_analysis.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── results/
│   ├── raw/
│   ├── processed/
│   ├── figures/
│   └── tables/
└── docs/
    ├── proof_notes.md
    ├── literature_map.md
    └── novelty_assessment.md
```

---

## 16. Minimum API

```python
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Stratum:
    n: int
    r: int
    s: int
    a_observed: int

@dataclass(frozen=True)
class CMIResult:
    g2_observed: float
    cmi_nats: float
    mean: float
    variance: float
    skewness: float
    z_score: float
    p_normal: float
    p_edgeworth: float
    cf_critical_value: float
    informative_strata: int
    lyapunov_ratio: float
    max_variance_share: float

def test_sparse_cmi(
    strata: Sequence[Stratum],
    alpha: float = 0.05,
) -> CMIResult:
    ...
```

Also provide a helper that converts raw arrays into strata:

```python
def build_binary_strata(
    x: Sequence[int],
    y: Sequence[int],
    z: Sequence[int],
) -> list[Stratum]:
    ...
```

---

## 17. Unit tests

At minimum, verify:

1. hypergeometric probabilities sum to one
2. PMF values match a trusted library
3. support bounds are correct
4. \(g_z(a)\geq0\)
5. \(g_z(a)=0\) at the independence table when that table is attainable
6. exact moments match brute-force observation-level permutation for very small cases
7. aggregate moments equal moments from exact discrete convolution
8. cumulants add correctly
9. degenerate strata have zero variance
10. result is invariant to swapping \(X\) and \(Y\)
11. result is invariant to relabelling \(0\leftrightarrow1\)
12. CMI in bits and nats differs only by the appropriate scale
13. fixed-margin direct sampling matches within-stratum permutation
14. normal and Edgeworth p-values remain finite
15. no undefined behaviour occurs for \(n_z=0\), \(1\), or fully degenerate margins

---

## 18. First-stage go/no-go experiment

Complete this before attempting a full thesis derivation.

### Step 1

Implement exact stratum distributions and exact moments.

### Step 2

Implement exact convolution across strata for configurations with manageable support.

### Step 3

Create at least 100 configurations covering:

- \(K=5\) to \(100\)
- stratum sizes \(3\) to \(30\)
- balanced and skewed margins
- homogeneous and heterogeneous strata
- dominant-stratum adversarial cases

### Step 4

For each configuration, compare exact upper-tail probabilities at:

\[
\alpha=0.05,
\quad
0.01,
\quad
0.001.
\]

### Step 5

Measure whether the proposed diagnostics identify poor approximations.

### Go criteria

Proceed with the thesis if:

1. the exact-moment normal approximation materially outperforms chi-squared in the target sparse regime
2. the skewness correction improves upper-tail calibration in a broad, not cherry-picked, set of configurations
3. important failure regimes can be characterised using observable diagnostics
4. the method is substantially faster than conditional permutation for realistic \(N\) and \(K\)
5. a literature search does not reveal the same CMI-specific construction and theorem

### No-go criteria

Pivot if:

1. Cornish-Fisher or Edgeworth corrections are frequently less accurate than the plain normal approximation
2. tail errors remain unacceptable at \(\alpha=0.01\) in most realistic sparse regimes
3. accuracy depends on an oracle choice between approximations
4. exact moment calculation is not materially faster than permutation in realistic software
5. existing literature already contains essentially the same exact conditional cumulant method for discrete CMI
6. the only successful cases are highly artificial fixed-margin configurations

---

## 19. Novelty verification tasks

Search classical statistics and information theory using combinations of:

- conditional mutual information exact moments
- discrete conditional mutual information hypergeometric
- likelihood-ratio statistic product multinomial exact cumulants
- sparse contingency table normal approximation
- stratified \(2\times2\) likelihood-ratio distribution
- hypergeometric transformation cumulants
- conditional independence test fixed margins many strata
- Berry-Esseen likelihood-ratio contingency tables
- Edgeworth conditional mutual information
- Cornish-Fisher mutual information significance
- exact conditional distribution of conditional mutual information
- Mantel-Haenszel versus likelihood-ratio sparse strata
- product hypergeometric likelihood-ratio statistic

The novelty claim should be narrow:

> A CMI-specific conditional finite-sample method that computes exact hypergeometric cumulants by conditioning stratum, proves a many-sparse-strata Gaussian limit, and uses those cumulants for higher-order tail correction.

Do not claim that:

- sparse likelihood-ratio statistics becoming normal is new
- conditional hypergeometric inference is new
- cumulant or Edgeworth corrections are new
- CMI being a likelihood-ratio statistic is new

---

## 20. Relation to transfer entropy

Transfer entropy can be expressed as CMI, but overlapping time-series histories create temporal dependence.

Do not initially claim that the i.i.d. conditional theorem applies directly to transfer entropy.

A safe thesis scope is:

1. prove the method for i.i.d. binary \(X,Y\) with categorical \(Z\)
2. validate it for discrete CMI
3. include symbolic transfer entropy only as an empirical extension
4. explicitly state that dependent-history theory remains future work

A stronger later extension could use:

- non-overlapping blocks
- Markov-chain central limit theory
- mixing conditions
- block permutation or surrogate methods

These are not required for the minimum viable thesis.

---

## 21. Expected thesis contributions

A successful project may claim:

1. **Exact conditional representation**  
   Binary CMI is represented as a sum of independent transformations of hypergeometric variables after conditioning on observed stratum margins.

2. **Finite-sample cumulants**  
   An efficient algorithm calculates exact conditional mean, variance, skewness, and optionally kurtosis.

3. **Sparse-stratum asymptotic result**  
   A conditional central limit theorem is established as the number of informative sparse strata grows and no stratum dominates.

4. **Higher-order significance approximation**  
   Exact cumulants are used in Cornish-Fisher, Edgeworth, or saddlepoint tail approximations.

5. **Regime characterisation**  
   Observable quantities are evaluated as predictors of approximation reliability.

6. **Computational implementation**  
   The method is implemented in Python and, if successful, integrated into JIDT.

---

## 22. Deliverables for the testing agent

The testing agent should return:

### A. Mathematical assessment

- verify the CMI decomposition
- verify the conditional hypergeometric null
- verify conditional independence across strata
- derive the cumulants carefully
- state and prove the strongest feasible CLT or Berry-Esseen result
- identify any hidden assumptions or invalid steps

### B. Novelty assessment

- produce a literature map
- identify the closest existing methods
- explain exactly what remains new
- flag any result that appears already known

### C. Prototype implementation

- implement exact moments
- implement normal, Cornish-Fisher, and Edgeworth methods
- implement exact convolution
- implement conditional permutation
- include unit tests

### D. Empirical falsification report

- calibration results
- adversarial results
- tail results
- diagnostic performance
- runtime comparison
- clear go/no-go recommendation

### E. Thesis feasibility recommendation

Conclude with one of:

- proceed with the exact-cumulant and skewness-corrected CMI thesis
- proceed only with a narrower theoretical contribution
- switch to a saddlepoint version
- abandon the idea and explain why

---

## 23. Context

The original project investigated a finite-sample null for ordinary discrete mutual information under skewed marginals. The revised project should not merely repackage that work. It moves to conditional mutual information because the decomposition across many sparse conditioning states creates a natural setting for product-multinomial or triangular-array central limit theory.

The original literature review is available separately as:

`INFO5993_Assignment_3(3).pdf`

Use it for background on:

- MI, CMI, and transfer entropy
- plug-in estimator bias
- chi-squared asymptotics
- permutation testing in JIDT
- exact contingency-table inference
- effective degrees of freedom
- moment-matched parametric nulls

However, the testing agent should conduct an independent literature search rather than relying on the review's claim that the proposed CMI construction is novel.

---

## 24. Final instruction to the testing agent

Treat this as a hypothesis to test, not a method to defend.

Prioritise:

1. finding counterexamples
2. checking whether the exact construction already exists
3. testing upper-tail calibration
4. determining whether failure can be diagnosed from the observed table
5. deciding whether the remaining contribution is large enough for a master's thesis

Do not proceed to JIDT integration until the statistical method passes the first-stage go/no-go experiment.
