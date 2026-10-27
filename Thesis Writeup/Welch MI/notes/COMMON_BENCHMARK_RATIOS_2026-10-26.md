# Common denominators and explicit axis labels — 26 October 2026

The user approved a common benchmark as denominator throughout the approximation comparisons. This supersedes the earlier observed/predicted display rule. The complete preceding manuscript, PDF, figure assets and reporting sources are preserved in `archive/before_common_benchmark_ratios_2026-10-26.zip`.

| Comparison | Numerator | Benchmark denominator |
| --- | --- | --- |
| Mean coefficient | E(Vhat) | Population V |
| Population variance prediction | tau²/n | Observed Var(Vhat) |
| Average sample-based variance prediction | E(tauhat²)/n | The same observed Var(Vhat) |
| Population component df | nu | Moment target nu_mom |
| Mean sample-based component df | E(nuhat) | The same moment target nu_mom |
| Shared estimated difference variance | E(SEhat²) | Observed Var(Deltahat) |

A value above one means the assessed quantity exceeds its benchmark; below one means it falls short. Benchmarks remain specific to each population and setting. Distinct population tables should retain their own V, sampling variance and moment target.

The two population panels in each row of Figures 6.1–6.2 and the companion moment plots share a vertical scale. The generic “Ratio” labels are replaced with “Variance prediction / Var(Vhat)” and “Degrees of freedom / nu_mom”; mathematical legends identify the two numerators without inventing a new symbol.

The review updates both reporters, their shared module, affected tables and numerical examples, Chapter 5 definitions, Chapter 7 interpretation, Appendix B inclusion/uncertainty descriptions and its exact df decomposition, and Appendix C diagnostic definitions. The sampling-based df curve still requires every component estimate to be positive and finite, so a conditional mean is never silently plotted as an unconditional mean.

The common denominators already used by the primary rejection rates (all simulation repetitions) and the power axes (a fixed independently fitted null SD within each focus setting) remain appropriate. Bias/SD, raw moment levels, rejection directions and paired power differences retain their separate scientific definitions. No extra ratio columns or notation are introduced.

The original CSV ratio definitions already match this convention. Plotted values and intervals are read directly from the unrounded summaries; reciprocal transformations are removed. The explanatory 16×16 P example at n=1,000 has population-prediction/observed variance ratio 0.756 and average sample-prediction/observed variance ratio 1.67. The df identity now expresses nu_FO/nu_mom as the reciprocal of the product of the squared mean ratio and the variance-prediction ratio.

Final tests, preservation checks, rendered-page review, source build and packaging verification are recorded in `REDESIGN_VERIFICATION.json`.

Finite zero variance estimates remain in the moment calculations. A zero prediction or estimated difference variance can produce a zero ratio when the observed benchmark is positive; only the benchmark must be positive for these direct variance ratios. Positive-finite inclusion rules for estimated degrees of freedom remain unchanged.

The final 228-test experiment suite and eight packaging tests pass. All 11,877 numerical result/evidence files are byte-identical; only reporting provenance changes. Chapters 2–4 and Appendix A remain byte-identical. All changed manuscript pages and the full companion moment plot were rendered and reviewed. The final thesis remains 103 pages (64 pages of main text; Chapter 6 is 17 pages), with no LaTeX warnings. The packaged source builds independently and produces identical extracted text. The delivery verification passes, and the packaged display helper reproduces all ten outputs; both figure renders are pixel-identical.
