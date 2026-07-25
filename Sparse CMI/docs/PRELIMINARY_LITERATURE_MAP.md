# Preliminary Literature Map

This is an initial novelty screen, not a systematic review.

The more detailed, updated claim analysis is in
`NOVELTY_AUDIT_AND_CLAIM_BOUNDARY.md`. In particular, that audit incorporates
Niu, Ray Choudhury, and Katsevich (2024) and `spaCRT`, which substantially
narrow the defensible saddlepoint novelty claim.

## Closest established work

### Exact conditional independence in multidimensional tables

Kreiner (1987), *Analysis of Multidimensional Contingency Tables by Exact
Conditional Tests: Techniques and Strategies*, explicitly describes exact
conditional tests of zero partial association using the ordinary likelihood
ratio, Pearson statistic, or another chosen statistic. It also emphasizes the
failure of usual approximate p-values in large sparse tables.

Source:
https://biostat.ku.dk/DIGRAM/Kreiner%201987%20analysis%20of%20contingency%20tables%20by%20exact%20tests%20of%20cond%20indep.pdf

This means the exact fixed-margin conditional-independence construction and
the use of a likelihood-ratio statistic are not novel.

### Nearly exact Monte Carlo conditional tests

Kim and Agresti (1997), *Nearly exact tests of conditional independence and
marginal homogeneity for sparse contingency tables*, develops Monte Carlo
estimates of exact conditional p-values for sparse three-way tables.

Source:
https://users.stat.ufl.edu/~aa/articles/CSDA_1997.pdf

This means conditional table Monte Carlo as the sparse baseline is also not
novel.

### Stratified product-hypergeometric exact tests

Work on stratified Fisher tests states that, after conditioning on the margins,
each stratum's free count is hypergeometric and exact inference combines many
strata.

Source:
https://pmc.ncbi.nlm.nih.gov/articles/PMC3884832/

The exact stratum decomposition is classical, even though those tests often
target a common directional association rather than the summed two-sided CMI
likelihood-ratio statistic.

### Gaussian likelihood-ratio approximations in sparse tables

Koehler (1986), *Goodness-of-Fit Tests for Log-Linear Models in Sparse
Contingency Tables*, proves asymptotic normality of likelihood-ratio
goodness-of-fit statistics when the number of categories grows and reports
that a normal approximation can outperform chi-square in sparse tables.

Source:
https://doi.org/10.1080/01621459.1986.10478294

This is very close to the project's broad motivation. A new theorem must
clearly differ through its conditional product-hypergeometric setup, exact
observable cumulants, assumptions, or finite-sample error control.

### Mutual information and Gaussian approximation

Harremoes (2014), *Mutual Information of Contingency Tables and Related
Inequalities*, identifies `G^2` with twice empirical mutual information,
studies fixed-margin hypergeometric tables, and relates signed
log-likelihood to a standard Gaussian.

Source:
https://arxiv.org/abs/1402.0092

This prevents a novelty claim based only on interpreting the contingency-table
likelihood ratio as mutual information or using a Gaussian approximation.

### Saddlepoint methods for sequences of 2x2 tables

Saddlepoint approximations have been developed for approximately exact
inference in sequences of independent 2x2 tables, including common-odds-ratio
problems.

Source:
https://doi.org/10.1080/01621459.1998.10473790

A later saddlepoint fallback would need to distinguish its target statistic
and null from this literature.

## Plausible remaining contribution

A defensible novelty claim may still combine:

1. exact finite-sample cumulants of the summed binary-CMI likelihood-ratio
   statistic under separate fixed margins in every conditioning state;
2. a conditional triangular-array CLT or Berry-Esseen result stated using
   observable per-stratum quantities;
3. a higher-order CMI tail approximation with empirically validated routing
   diagnostics;
4. a software comparison against correctly constructed within-stratum
   permutation, including the null mismatch in JIDT's default CMI shuffle.

The contribution must not be described as inventing exact conditional
independence tests, product-hypergeometric inference, sparse-statistic
normality, Edgeworth correction, or the identity between CMI and a
likelihood-ratio statistic.

## Novelty status

**Unresolved and high risk.**

The empirical method is promising, but the central statistical ingredients
have close classical precedents. Before selecting the thesis title, perform a
systematic citation search around Kreiner (1987), Koehler (1986), Kim and
Agresti (1997), exact logistic regression, and saddlepoint inference for
stratified 2x2 tables.
