# Three explanatory expansions, 6 November 2026

The user authorised the three substantive expansions identified in the
compression review. The changes explain missing mathematical connections.
The optional proof relating positive MI to positive pointwise-MI variance
was explained in chat and is not included in this revision.

## Changes

1. Appendix B.6 now maps the two-variable Taylor formula to the estimated
   sampling mean and variance. An exact centring identity explains why
   squared deviations supply the first-order variance error. Substitution
   gives the average of repetition-level contributions, followed by the
   implemented Monte Carlo standard error and an explanation of the
   covariance retained within each contribution. A general ratio expansion
   and the sample-based variance-ratio contribution replace the previous
   one-sentence reference to the same calculation.
2. Appendix B.4 defines the population-based linear contribution and its
   remainder, displays their exact variance decomposition, and explains
   the covariance term. An existing 10,000-repetition diagnostic at shared
   MI 0.02, different-skew 16 by 16 tables and n=50 supplies the example
   for population P: 18.7%, 87.3% and -6.0% of observed variance. Section
   6.1.1 connects the interpretation to this decomposition. The empirical
   identity uses sample variances and covariance on the same repetitions;
   it is not presented as an exact equality between an empirical variance
   and the known population prediction.
3. Appendix A.2 explains the association dimension after removing marginal
   changes, the sum of squared coordinates with limiting normal
   distributions, and the population shifts producing noncentrality.
   Applying the quadratic MI expansion to the population departure from
   the product of its margins connects the squared shift to 2nI(P).
   The text distinguishes the approaching population in this local
   argument from a fixed-population large-sample comparison.

## Verification

- The five existing thesis-consistency tests pass.
- Independent numerical checks confirm the exact finite-M centring
  identity, the Monte Carlo standard-error formula against the production
  moment-summary function, and the covariance decomposition. The new
  percentages reproduce the saved mechanism evidence without rerunning
  an experiment.
- A numerical check confirms the rank and covariance of the association
  projection under independence and the quadratic MI scaling used for
  the noncentrality explanation. The existing Brillinger and Banerjee
  references were also checked for the cited limiting results.
- Active source references and citations resolve, original displayed
  equations are preserved, and braces and environments balance.
  Paragraph-style, Australian-English spelling and whitespace checks pass.
- Of 634 preserved inputs, only the three approved manuscript files
  change. The other 631 hashes match, including Chapter 3, the abstract,
  conclusion, bibliography, figures, historical files, current PDFs,
  delivery archives, inspected code and the separate study guide.

No LaTeX build, delivery refresh, commit or push was requested or performed.
The current PDF therefore predates these source expansions. Equation
numbering, page breaks and visual layout will be checked at the next
explicitly requested rebuild.
