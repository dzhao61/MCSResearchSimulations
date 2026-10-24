# Matched Same-Skew Extension

Approved by the user on 19 October 2026, before generating the new results.

## Question and scope

Include same skew as a matched baseline in all three main studies and both
supporting checks. Retain every original setting and result. Same-skew margins
are m_k(0.8) in both populations; different-skew margins remain m_k(0.7) and
m_k(0.8). No change to those values is authorised by this extension.

- Main null study: already complete; add no settings.
- Population-MI sweep: add same skew at all seven existing MI targets and
  n = 100 and 1000. Two settings already exist, so add twelve.
- Power study: add same skew at sizes 2, 8 and 16, using the same nine
  differences and two sample sizes. Six null settings already exist, so add 48.
- Construction check: add same-skew four-cell populations at sizes 4 and 16,
  both MI pairs and both sample sizes, adding eight settings. Their copying
  matches are reused from the main null and power studies.
- Allocation check: add same skew using the two existing MI pairs and three
  allocations. Reuse two balanced settings and add four unequal allocations.

The extension adds 72 settings and 34 previously unused population pairs.
The combined design has 312 unique settings, 104 population pairs and
6,240,000 sampled table pairs at 20,000 repetitions per setting.

## Execution and interpretation

Use the existing estimators, validity rules, significance level, sampling
algorithm, stable setting identifiers and random-stream convention. Save new
records separately, authenticate the original evidence, and deduplicate shared
settings when assembling the combined results. Run a separate 200-repetition
technical pilot, then all planned full settings regardless of outcomes.

Review estimated degrees of freedom across all five comparisons using existing
and new records. Retain validity denominators. Examine median and 5th--95th
percentiles alongside rejection rates, bias and estimated/observed variance;
degrees of freedom alone do not identify causes of calibration errors.

Same-skew equal-MI populations are identical within each tested construction.
Expected biases cancel only when sample sizes also match. Unequal allocation
can produce unequal residual biases even when population tables match.
At nonzero MI differences, same margins do not imply identical populations or
equal biases.

Report all added settings. Use the existing five-part experimental structure,
short main-text comparisons and appendix evidence. Update exact totals, grids,
scope statements, results, conclusions where affected, reproducibility records,
tests and delivery packaging. Do not imply the original study contained the
added settings or that this extension was planned before the original results.
Leave the deferred 0.7/0.9 sensitivity experiment and historical drafts alone.

## Results And Verification

Completed on 19 October 2026. The separate 200-repetition technical pilot
and all 72 full settings passed. All new method outputs are valid. The
original evidence was authenticated and left unchanged. The independent
audit regenerated 17 input pairs per new setting and checked every saved
chunk, summary, population, variance formula, degrees of freedom, p-value,
rejection count and interval. Combined manifests deduplicate all 312 settings.

Key results retained in the manuscript:

- The same-skew population-MI sweep reproduces the conservative
  near-independence pattern. At n=1000, the median degrees of freedom rise
  from 8.23 at MI 0.0001 to 74.42 at MI 0.05, similar to different skew.
- At size 16 and n=1000, the matched same-skew power curve lacks the sharp
  initial decrease seen under different skew. At a 0.01-nat difference,
  Wald rejects 370/20000 times, including 14 opposite-direction rejections;
  Expanded Welch rejects 339 times, including 12 opposite-direction cases.
  Difference bias is 0.00092 nats, not the different-skew 0.03061 nats.
  Small Monte Carlo fluctuations in the earliest same-skew curve points
  are not described as a strictly monotone population power curve.
- Same-skew sparse null rejection remains conservative under both copying
  and four-cell constructions. At size 16 and n=1000, Wald rates are
  0.00645 and 0.01070. Matching category frequencies removes the expected
  null difference bias at equal n, not the uncertainty-estimation problem.
- Same-skew unequal allocations leave residual null biases despite identical
  populations. Median degrees of freedom fall from 33.45 under balance to
  about 11.3 under imbalance. Under the alternative, allocating more to Q
  slightly increases Wald power but not Expanded Welch power relative to
  balance, so no universal claim that imbalance lowers both methods' power
  is made.
- Degrees of freedom were examined across all five comparisons. The
  variance ratios, bias and direction results show why their size alone
  does not establish reliable calibration or explain every power difference.

The abstract, design, results, discussion, conclusion, appendix grids,
reproduction instructions, tests and packaging were reconciled. Detailed
comparisons remain in Appendix C, with short interpretations in Chapter 6.
The current manuscript is 112 pages versus 103 before the extension: three
additional main-text pages and six additional appendix pages. All 251
scientific/application tests and 8 packaging tests pass. The source archive
builds independently with extracted text identical to the active PDF; the
delivery consistency check passes. Historical drafts are unchanged.
