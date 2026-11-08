# Approximation plot simplification — 26 October 2026

The user approved the three related plotting recommendations: split both variance predictions into their own rows, split population and estimated component df into their own rows, and simplify the near-independence df panel while preserving its full diagnostics in the experiment supplement.

The preceding 102-page manuscript and reporting sources are preserved in `archive/before_approximation_plot_simplification_2026-10-26.zip`.

## Figures and interpretation

- Figure 6.1 has three rows: E(Vhat)/V, population sampling-variance prediction / observed variance, and average sample-based prediction / the same observed variance. The two variance rows share the same scale across P and Q. Colour indicates table size; all curves are solid. The original mean and population-prediction Monte Carlo bands remain in the first two rows. The 1.3% relative half-width bound applies to those bands.
- Figure 6.2 has two rows: population first-order component df / moment target, and mean estimated component df / the same moment target. Both rows and both populations share one scale. The original Monte Carlo bands remain on the population comparison. The sample-based row still requires all component df estimates to be positive and finite.
- Figure 6.3 retains four bottom-row curves: mean estimated df, the near-independence prediction of that mean, the observed moment target and the population first-order df. Labels name the calculation rather than saying “A.4”. The main 4×4, n=1,000 different-skew comparison includes all 100,000 component estimates at every MI.
- Nine full diagnostic plots in `WelchSatterthwaiteMI/supplementary_displays/near_independence_diagnostics/` retain the median, fifth–95th percentile band and near-independence moment-target prediction. Their titles state the sample size and margin regime. Source-field definitions, inclusion rules and regeneration instructions are in the folder README.
- Section 6.1 now explains the top/middle/bottom rows and the near-independence calculation explicitly. The worked numerical examples and benchmark denominators remain unchanged. Appendix B identifies the middle-row population variance ratio in the df decomposition.
- Existing notation, point estimates, interval values and table entries are preserved. Mathematical y labels are larger for readability, ordinary numeric logarithmic ticks are used, and line-style legends are replaced by one table-size legend where the rows now identify the calculation.

The plotting helper separates figure construction into testable functions. Two additional tests check each row against the original unrounded data, common scales, missing df summaries, the four main near-independence curves and all six supporting curves. The optional `--diagnostics` output location keeps auxiliary plots separate from main figure exports.

The final main manuscript has 103 pages (64 pages of main text; Chapter 6 is 17 pages). The extra page accommodates the taller split figures. Final tests, preservation checks, rendered-page review, packaged reproduction and source-build checks are recorded in `REDESIGN_VERIFICATION.json`.

All 230 experiment tests and eight packaging tests pass. All 11,878 saved scientific evidence files are byte-identical, including existing reporting provenance. The existing table sources and unaffected figure assets are byte-identical; Chapters 2–4 and Appendix A are unchanged. The PDF builds without warnings and its packaged source rebuilds independently to identical extracted text. The delivered helper reproduces all 11 main outputs and nine full diagnostic plots from packaged inputs. All 12 regenerated PDF renders are pixel-identical. Final delivery checks pass. The main plots, full diagnostic layout and affected manuscript pages were visually reviewed.
