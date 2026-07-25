# Novelty Audit and Claim Boundary

Date: 25 July 2026

## Status

This is a targeted novelty audit, not a systematic review. It is sufficient to
narrow the thesis claim and identify the closest work, but absence from these
searches is not proof of novelty.

The current recommendation is:

> Proceed as a methods-transfer and algorithm-validation thesis for binary
> conditional mutual information, but do not claim a new general saddlepoint
> theorem or a new exact conditional test.

## Method Being Audited

For binary `X` and `Y` and arbitrary discrete conditioning variable `Z`, the
method conditions on the observed margins in every `Z=z` stratum. If
`(n_z, r_z, s_z)` are fixed, the top-left count has the exact null

```text
A_z | n_z, r_z, s_z ~ Hypergeometric(n_z, s_z, r_z).
```

The CMI likelihood-ratio statistic is a sum of independent finite-support
contributions:

```text
G^2 = 2 N I_hat(X;Y|Z) = sum_z g_z(A_z).
```

The implementation obtains each component's exact finite-support cumulant
generating function, sums those CGFs, solves `K'(s_hat) = G^2_observed`, and
uses the Lugannani-Rice upper-tail formula. A deterministic router uses exact
convolution when guaranteed state and transition-work bounds are small, and
otherwise uses the factorized saddlepoint approximation.

This is a conditional fixed-margin test. It is not bootstrap, permutation, or
Monte Carlo inference once the observed table has been supplied.

## Closest Prior Work

| Established result | Consequence for the thesis |
|---|---|
| Kreiner (1987) develops exact conditional tests of conditional independence in multidimensional contingency tables, including likelihood-ratio statistics. | Exact fixed-margin conditional independence and the choice of `G^2` are not novel. |
| Agresti (1992) surveys exact conditional inference for contingency tables; Kim and Agresti (1997) develop nearly exact Monte Carlo tests for sparse three-way tables. | Conditional table sampling and Monte Carlo exact tests are not novel. |
| Patefield (1981) gives an algorithm for sampling contingency tables with fixed margins. | Direct fixed-margin table sampling is a classical computational baseline, not a new statistical method. |
| Harremoes (2014) studies mutual information as a likelihood-ratio statistic for fixed-margin hypergeometric tables and its Gaussian behavior. | The `G^2 = 2N MI` identity and a Gaussian approximation under fixed margins are not novel. |
| Koehler (1986) studies likelihood-ratio statistics in sparse contingency tables and shows regimes where normal approximation can outperform chi-square. | Sparse-table normality is not itself a new observation. |
| Classical conditional saddlepoint work includes Pedersen (1979), Kolassa (2000), Kolassa and Robinson (2006), and approximately exact inference for sequences of 2x2 tables. | Conditional and discrete saddlepoint approximations are established tools. |
| Niu, Ray Choudhury, and Katsevich's 2024 theory manuscript proves vanishing relative error for Lugannani-Rice approximations to conditional tails of averages of conditionally independent variables, including discrete/non-lattice cases under their assumptions. That manuscript was merged into the current revision of their spaCRT paper in 2025. | A broad new theorem for this project's factorized sum is unlikely to be defensible. Their result should be specialized or cited, not rediscovered. |
| The same authors' `spaCRT` applies saddlepoint approximation to replace expensive conditional-randomization resampling. | "Saddlepoint instead of resampling for conditional independence" is already an active method class. The fixed-margin CMI statistic and finite-support router must distinguish this work. |
| Papapetrou and Kugiumtzis (2013) and SECMI (Kubkowski et al., 2021) develop non-permutation significance approximations involving CMI. | The thesis cannot claim to be the first analytic CMI significance test. |

## What the Search Did Not Find

The targeted search did not identify a paper containing the exact combination
of:

1. separate fixed margins within every conditioning state;
2. the summed plug-in binary CMI likelihood-ratio statistic;
3. exact finite-support per-stratum CGFs;
4. a deterministic exact-convolution/saddlepoint router based on observable
   work bounds;
5. calibration and runtime comparisons against chi-square and a correctly
   constructed within-stratum permutation null; and
6. an audit showing that JIDT's default global CMI shuffle targets a different
   null when `P(X|Z)` varies.

That combination is a plausible master's-level contribution. It should be
described as a CMI-specific construction, implementation, and validation of
established exact-inference and saddlepoint ideas.

## Defensible Claim

A conservative thesis claim is:

> We develop and validate a deterministic finite-sample significance
> procedure for binary discrete conditional mutual information under
> stratum-wise fixed margins. The procedure exploits exact hypergeometric
> component distributions and routes between bounded exact convolution and a
> factorized Lugannani-Rice approximation. Across predeclared sparse regimes,
> it is evaluated against chi-square and the equivalent within-stratum
> permutation test.

Possible secondary contributions are:

- a tractability bound that exploits repeated finite-support components;
- a reproducible regime map for exact, saddlepoint, and asymptotic routes;
- observable failure diagnostics for coarse support and dominant strata;
- an implementation-level audit of the null generated by JIDT's default CMI
  significance method; and
- an open, tested reference implementation.

## Claims to Avoid

Do not claim:

- invention of exact conditional independence testing;
- invention of fixed-margin table sampling;
- invention of saddlepoint or Lugannani-Rice approximation;
- the first use of saddlepoint approximation for a conditional test;
- the first analytic significance test for CMI;
- a general `r x c x |Z|` solution; or
- a new relative-error theorem unless it is formally shown not to follow from
  Niu et al. (2024).

## Generality Boundary

The current exact-CGF construction is general in the number and sizes of
conditioning strata, but `X` and `Y` are binary. In a general `r x c` stratum,
fixed margins leave `(r-1)(c-1)` free counts and the component CGF requires a
sum over a multidimensional table fiber. That is the same combinatorial
difficulty that makes general exact contingency-table inference hard.

Extension to larger alphabets is therefore a separate algorithmic research
problem. Candidate routes include multivariate saddlepoint normalization,
sequential importance sampling, holonomic/recursive normalizing constants, or
a fallback Monte Carlo exact test. The present implementation must not be
marketed as having solved that problem.

## Remaining Novelty Gate

Before fixing the thesis title:

1. Run a citation-chain search forward and backward from Kreiner (1987),
   Koehler (1986), Kim and Agresti (1997), the stratified 2x2 saddlepoint
   literature, Niu et al. (2024), and `spaCRT`.
2. Search statistics and information-theory databases using both vocabularies:
   `conditional mutual information`, `deviance`, `G-test`, `log-linear`,
   `product hypergeometric`, `conditional randomization`, and `saddlepoint`.
3. Ask a supervisor or statistical-methods reviewer whether the algorithmic
   combination and empirical regime map meet the local master's contribution
   standard.
4. Write a one-page comparison against `spaCRT`: null being conditioned on,
   statistic, required model, computational primitive, and theorem used.
5. Decide whether the thesis contribution remains binary CMI or includes a
   genuinely new larger-alphabet approximation.

## Sources

- Kreiner (1987), *Analysis of Multidimensional Contingency Tables by Exact
  Conditional Tests: Techniques and Strategies*:
  https://biostat.ku.dk/DIGRAM/Kreiner%201987%20analysis%20of%20contingency%20tables%20by%20exact%20tests%20of%20cond%20indep.pdf
- Agresti (1992), *A Survey of Exact Inference for Contingency Tables*:
  https://users.stat.ufl.edu/~aa/articles/agresti_1992.pdf
- Kim and Agresti (1997), *Nearly Exact Tests of Conditional Independence and
  Marginal Homogeneity for Sparse Contingency Tables*:
  https://users.stat.ufl.edu/~aa/articles/CSDA_1997.pdf
- Patefield (1981), *Algorithm AS 159: An Efficient Method of Generating Random
  R x C Tables with Given Row and Column Totals*:
  https://doi.org/10.2307/2346669
- Koehler (1986), *Goodness-of-Fit Tests for Log-Linear Models in Sparse
  Contingency Tables*: https://doi.org/10.1080/01621459.1986.10478294
- Harremoes (2014), *Mutual Information of Contingency Tables and Related
  Inequalities*: https://arxiv.org/abs/1402.0092
- Pedersen (1979), *Approximating Conditional Distributions by the Mixed
  Edgeworth-Saddlepoint Expansion*:
  https://doi.org/10.1093/biomet/66.3.597
- Kolassa (2000), *Saddlepoint Approximation at the Edges of a Conditional
  Sample Space*: https://doi.org/10.1016/S0167-7152(00)00101-2
- Kolassa and Robinson (2006), *Conditional Saddlepoint Approximations for
  Non-continuous and Non-lattice Distributions*:
  https://doi.org/10.1016/j.jspi.2005.11.003
- Niu, Ray Choudhury, and Katsevich (2024), historical theory manuscript,
  *The Saddlepoint Approximation for Averages of Conditionally Independent
  Random Variables*:
  https://arxiv.org/abs/2407.08915
- Niu, Ray Choudhury, and Katsevich (2025 revision), *The Conditional
  Saddlepoint Approximation for Fast and Accurate Large-Scale Hypothesis
  Testing*:
  https://arxiv.org/abs/2407.08911
- Papapetrou and Kugiumtzis (2013), *Markov Chain Order Estimation with
  Conditional Mutual Information*: https://arxiv.org/abs/1301.0148
- Kubkowski et al. (2021), *How to Gain on Power: Novel Conditional
  Independence Tests Based on Short Expansion of Conditional Mutual
  Information*: https://www.jmlr.org/papers/v22/19-600.html
