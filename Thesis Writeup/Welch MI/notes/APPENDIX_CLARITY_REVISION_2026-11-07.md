# Appendix clarity revision, 7 November 2026

The user authorised all appendix items from the consolidated 18-item
review and requested a narrower recommendation for the main chapters.
This revision implements items 16--18 only. The main chapters are unchanged.

## Appendix changes

- Appendix A.2 now illustrates one association direction with a positive
  2 by 2 table whose diagonal probabilities change by epsilon and whose
  off-diagonal probabilities change by minus epsilon. The explanation
  shows why fixing the row and column margins leaves only one free change.
  A scaled diagonal-versus-off-diagonal sample contrast then makes an
  association coordinate concrete: its observation contributions have mean
  zero and variance one under uniform independence, and the central limit
  theorem gives its standard normal limiting distribution. The text then
  returns explicitly to general positive r by c tables.
- Appendix B.6 identifies Equation B.9's decomposition and states which
  sample mean and sample variance replace its population sampling moments.
  This replaces the unexplained term evaluation moments.
- Appendix B.6 displays the exact rearrangement separating the variance
  error into the leading average and two corrections. The explanation
  derives the mean-error scale from Var(X-bar) = v/M, explains why its
  square and S-squared/M have size 1/M, and justifies the larger 1/sqrt(M)
  scale of the leading average. The finite set of count tables at fixed
  sample size supplies the required finite variance of squared deviations.

## Verification

- All five existing thesis-consistency tests pass.
- Independent algebra checks confirm the example's margins, positivity,
  contrast value, contrast mean and variance, and cancellation of marginal
  directions at uniform independence. They also confirm that the quadratic
  association form equals the squared contrast in this example.
- Independent numerical checks confirm the new finite-M rearrangement,
  including constant and zero-valued input cases.
- Every original displayed equation, citation and LaTeX label is preserved.
  Three unnumbered displays are added, leaving existing equation numbering
  unchanged. All 181 source references resolve against 154 unique labels.
- Contextual rereading, braces and environment balance, Australian spelling,
  shared paragraph style and whitespace checks pass.
- Of 636 preservation inputs, only the two appendix sources change. The
  other 634 hashes match, including all main chapters, the abstract,
  conclusion, Chapter 2 derivation benchmark, figures, bibliography,
  current PDFs and delivery archives, historical files, inspected code
  and the separate personal study guide.

No PDF rebuild, delivery refresh, commit or push was requested or performed.
The assembled PDF and new display layouts await a requested rebuild.

## Main-text recommendation remains unimplemented

The narrower recommendation covers original review items 2, 6, 7, 9, 10,
12, 13 and 15: the standardisation explanation, normalised mean overshoot,
the moment target's ambiguous possessive, the informative linear term,
sample size passing through rejection ranges, the power curve's centre,
the conclusion's first RQ1 explanation, and preservation of the equal-MI
hypothesis. The user has requested recommendations rather than edits to
these main-chapter passages.
