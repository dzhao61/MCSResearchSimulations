# Section 6.1.1: interpret the graph directly — 26 October 2026

The reader questioned the value of the aggregate range table and found that the following paragraph did not unpack Figure 6.1. The table mixed minimum/maximum values across different table dimensions, margin regimes and populations, whereas the adjacent figure describes different-skew populations. It supplied extra numbers without identifying their settings or explaining the plotted patterns.

The preceding manuscript, main PDF, thesis README, verification record and relevant figure/table source are preserved in `archive/before_section_6_1_1_graph_interpretation_2026-10-26.zip`. Previously uncommitted shading edits are included in that preserved version and retained in the current manuscript.

## Changes

- Remove the aggregate range table and its introduction from the printed manuscript. Retain the generated table source, underlying CSV results and other figure assets unchanged; do not add another appendix table.
- Replace the generic summary with three paragraphs interpreting the plotted quantities. Explain that top-row ratios above one imply that V(P) underestimates the mean of its estimate. Identify the larger relative mean errors in larger tables and the initial rise before decline.
- Explain that bottom-row solid ratios below one imply underestimation of the sampling variance of the variance estimate. Use the same population and sample size to compare the dashed prediction, showing how substituting sample proportions can reverse the error.
- Explain that at large sample sizes the sampling-variance predictions can be close while the mean approximation retains error. Keep the discussion confined to the different-skew populations shown, with the companion margin plots referenced separately.

One consistent example follows the 16×16 P population: at n=1,000, the observed mean is about 3.24V(P), the population sampling-variance prediction is 0.756 of the observed variance, and the mean sample-based prediction is 1.67 times that variance. At n=50,000, the mean remains approximately 7% above V(P). These rounded values were checked against the exact null-grid rows used to draw Figure 6.1, rather than other simulation batches involving the same population.

## Preservation and review

All figure/table assets are byte-identical to the preceding version, including the 40% band opacity. All Chapter 6 source before the removed table and after the start of Section 6.1.2 is unchanged. The scientific data, derivation, figure dimensions, uncertainty intervals and later results are unchanged. No simulations, calibration fitting or bootstrap sampling were rerun.

The explanation and graph fit together on printed page 45. The thesis remains 102 pages, with unchanged chapter spans and 63 pages of main text. LaTeX automatically renumbers the later Chapter 6 tables. The new Table 6.2 is the pre-existing detailed component comparison, not the removed aggregate range table.

The final build has no LaTeX warnings, unresolved references or overfull/underfull boxes. Physical pages 8–9 and 53–56 were visually reviewed, including the final graph/explanation page and renumbered list of tables. Delivery verification passes. The independently extracted source archive builds without warnings and produces identical PDF text. Main, build and delivery PDFs are byte-identical. These completed checks are recorded in the root verification file. No Git commit was requested or performed.
