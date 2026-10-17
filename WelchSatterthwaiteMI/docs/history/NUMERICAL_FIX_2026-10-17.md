# Numerical Correction And Flow-On Effects

## Changes

The empirical MI variance is now calculated from centred pointwise MI values,
rather than by subtracting two nearly equal second moments. The variance
sensitivity uses the algebraically equivalent centred expression
`z**2 - V + 2*(z - E[z|X] - E[z|Y])`, followed by centring before its variance
is calculated. These changes preserve the mathematical estimators.

For an integer count table, exactly constant occupied-cell pointwise MI is
identified by integer cross-products. Such a component has variance and
sensitivity variance exactly zero and cannot supply Expanded Welch component
degrees of freedom. Large cross-products use Python integers to avoid overflow.
A relative floating-point screen selects candidates for the exact check; it
does not classify an integer table as degenerate. No new variance tolerance,
pseudocount, sample-size exclusion or statistical method is introduced.

Normal Wald and Simple Welch can still be used when just one component is
zero and the other supplies positive variance. Expanded Welch retains the
existing disclosed requirement that both component degrees of freedom be
positive and finite. A separate regression verifies that a genuinely positive
variance of approximately 1e-24 is not rounded to zero.

The base auditor now authenticates the full configuration and display
manifests, population definitions/arrays and every checkpoint identity against
the reconstructed design. It also checks the validity fractions used for
figure markers. The base reporter runs that independent audit before export,
instead of trusting a previous success flag. Mutation regressions cover
changed experimental labels, targets, identifiers, populations, provenance,
bias summaries and validity fractions.

The experiment supplement now includes the practical runner, protocol,
tests, attributed raw archives, count tables and all six full-data comparisons
with Holm-adjusted p-values. New `full` and `verify-full` modes reproduce
the manuscript application without exploratory subset simulations. Stale
verification instructions now point to the focused experiment.

## Re-Evaluation

All 240 distinct settings were regenerated: 4.8 million table pairs, with
the same configuration identifiers, population arrays, sample sizes,
NumPy version, master seed and per-chunk P/Q streams. The four jackknife
settings and all 150,000 practical subsets were also recalculated using
their original deterministic inputs. The original results and scientific
source were preserved before changing the implementation.

`NUMERICAL_FIX_2026-10-17/evidence.json` and `affected_settings.csv` contain
the machine-generated comparison. Across the 240 distinct settings:

- Normal Wald validity and all rejection decisions are unchanged.
- All population arrays, plug-in/corrected MI values and saved support counts
  are identical to the originals.
- Expanded Welch validity or rejection counts change in 28 small-sample null
  settings. No previously invalid output becomes valid.
- Exactly 12,318 incorrectly accepted Expanded Welch outputs are removed,
  including 859 formerly counted rejections.
- The greatest unconditional rejection-rate reduction is 0.0081, at
  8 by 8 different-skew tables with n=10: 0.1072 becomes 0.0991.
- The largest validity change is at 2 by 2 uniform tables with n=10:
  0.98155 becomes 0.80630. This changes one 90% validity marker.

An independent integer reference checked all 1.32 million core pairs with
n at most 250. Every removed validity decision is explained by an exactly
constant-score component. No such component remains accepted. Transposing
both tables changes neither validity nor rejection in any checked pair.
An exhaustive regression additionally checks row/column relabelling,
transposition and group exchange for all 2 by 2 tables with totals 2 through
20, including empty margins and both zero and nonzero constant MI scores.

The practical exploratory subsets lose 260 accepted Expanded Welch outputs
across seven settings and three rejections. These subset analyses are not
in the thesis. All six full-data comparisons, their displayed p-values,
Holm adjustments and decisions are unchanged at manuscript precision.

## Scientific Interpretation

The correction makes Expanded Welch less usable at the smallest sample sizes;
it does not demonstrate a better rejection cutoff. Its unconditional rates
fall because outputs with undefined component degrees of freedom are now
classified according to the existing policy. Invalid outputs remain in the
20,000-repetition denominator, and valid-only/common-valid comparisons are
recomputed rather than carried forward from the earlier masks.

The main small-sample illustration changes accordingly. For 4 by 4
different-skew tables at n=10, Wald still rejects at 0.1332. Expanded Welch
changes from 0.0493 to 0.0465, while its validity falls from 0.7776 to 0.7588.
The common-valid subset has 15,175 pairs, with rejection rates 0.1029 for
Wald and 0.0612 for Expanded Welch. The interpretation is unchanged: the
Student t distribution reduces rejection on common inputs, while an
unconditional rate near 5% partly reflects unavailable results.

The highlighted 4 by 4 uniform n=20 and 8 by 8 different-skew n=100
improvements are unchanged. All power-study rejection decisions, the large
16 by 16 bias and sign-reversal findings, both construction checks, the
sample-allocation comparisons and the jackknife conclusions are unchanged.
The corrected numerical implementation adds call overhead: renewed median
timings are about 102-112 microseconds for Wald and 187-202 microseconds
for Expanded Welch, a factor of approximately 1.8-1.9.

Only Chapter 6's small-sample numbers and timing summary, the three null
figures and the complete null table require visible manuscript changes.
Other numerical table fragments remain identical. No derivation, research
question, conclusion or literature claim changes. No numerical-maintenance
discussion has been inserted into the manuscript.

## Verification And Preservation

All 236 workspace tests pass: 192 Welch-project tests, 27 shared-library
tests and 17 practical-data tests. The core and extension audits pass, as
does the full regenerated jackknife audit and the practical verification.
The thesis rebuild remains 102 pages without warnings or unresolved
references. The affected result, table and figure pages are visually checked.

The pre-correction simulation directories and scientific source archive are
under `results/archive_before_numerical_fix_20261017/`; practical originals
are under `PracticalMIExploration/results_before_numerical_fix_20261017/`.
The historical thesis archive and every older working draft remain untouched.
The active PDF, source archive, experimental supplement and checksums are
rebuilt from the corrected evidence.

The extracted source archive compiles warning-free to the same 102-page PDF
text as the active manuscript. The extracted supplement discovers 150 tests:
140 execute successfully and ten manuscript-text tests skip because the
thesis source is supplied separately. Its core, allocation and construction
audits pass, as do full-data application verification and a new application
reproduction. Both ZIP CRC checks and all delivery SHA-256 checksums pass.
All 376 historical-archive/working-draft preservation hashes match.
