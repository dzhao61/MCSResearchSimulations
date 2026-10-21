# Additional simulation displays

These displays accompany the shortened Appendix C. They retain the complete
equal-MI table and two full-range power plots omitted from the manuscript.
No populations, sampled pairs, estimators or simulation results changed.

## Complete equal-MI results

- `complete_null_results.csv` contains all 120 combinations of four table
  sizes, three margin regimes and ten sample sizes. Values reproduce the
  four-decimal rates in `focused_null_table.tex`, also included here.
- Both population MI values are 0.02 nats. Each population has the sample
  size specified in the row, with 20,000 independent sampled table pairs
  per setting. Tests are two-sided at the 5% level.
- Rejection rates divide valid rejections by all 20,000 repetitions.
  Invalid calculations count as non-rejections. The two validity columns
  give proportions, not percentages.
- Margin regimes and the population construction are defined in Chapters 5
  and Appendix B of the thesis. The equal-MI figures in Chapter 6 and
  Appendix C collectively show all twelve size–margin comparisons.

The underlying results, including greater numerical precision and
Monte Carlo intervals, are in
`../results/same_skew_extension/combined_method_results.csv`;
`combined_displays.csv` and `combined_configurations.csv` identify each
setting. Raw per-repetition records remain in their original results
directories, as described in the experiment supplement README.

## Full-range power plots

- `focused_detection_margins_full.pdf` compares uniform, same-skew and
  different-skew 4 × 4 tables at 1,000 and 10,000 observations per
  population. At a 0.2-nat difference both methods reject every sampled
  pair under all three margin regimes at both sample sizes.
- `focused_same_detection_sizes_full.pdf` compares same-skew 2 × 2,
  4 × 4, 8 × 8 and 16 × 16 tables at the same sample sizes. For the
  16 × 16 comparison at n = 1,000, Wald rejection reaches 0.4454 at a
  0.05-nat difference and one at 0.2 nats. The median combined degrees of
  freedom increase from 78.89 at equal MI to 207.47 at a 0.2-nat
  difference. At n = 10,000, both tests reject every sampled 0.05-nat
  difference at all four table sizes.

Both plots fix I(P) = 0.02 and set I(Q) = 0.02 + |Delta|, so the true
signed difference I(P) − I(Q) is negative for nonzero alternatives.
The plotted range extends through 0.2 nats and includes the equal-MI point.
Bands give pointwise Wilson 95% intervals. All test calculations are valid
in these power settings.

The thesis retains the corresponding small-difference comparisons and the
different-skew full-range plot across table sizes, which shows the initial
fall and subsequent rise in sparse-table rejection.

The packaging script includes the original table source and plot PDFs
directly from the thesis figure inputs. The CSV is a readable export of
the displayed table values. The standard reporters listed in the experiment
supplement README regenerate the original table and both plots.
