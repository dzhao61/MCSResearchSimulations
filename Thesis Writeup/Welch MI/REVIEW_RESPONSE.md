# Response to external assessment

Reviewed 20 September 2026 against the active thesis source, frozen results,
implementation and a new explanatory simulation. The assessment is broadly
fair and useful. Its central criticism, that the thesis described the pattern
more clearly than it explained it, is accepted. Some causal and asymptotic
claims were stronger than the evidence supports and have been narrowed below.

## Final narrow review

The later review was also substantially fair, with one attribution qualified
more carefully than proposed. The active manuscript now:

- reports the honest small-sample comparison as 15 of 24 regimes at
  \(n=10,20\), and reports separately that Expanded Welch rejects zero times
  in every \(n=5\) main-null regime;
- adds a validity-below-90% column to the complete null summary, so invalid or
  unstable settings are visible alongside the unconditional rejection bins;
- checks the local-moment prediction in the experiment supplement while
  retaining only the interpretable \(nI\) result in the thesis;
- uses the common local noncentrality form
  \(\lambda\approx nV\approx2nI\), with the equivalence explicitly limited to
  the near-independence expansion;
- contrasts the regression precedents with the upward local MI variance shift
  \(\mathbb E\widehat V\approx V+d/n\);
- removes confidence-interval formulas because coverage was not evaluated;
- replaces manuscript “post-review” labels with “supplementary” or
  “post-protocol,” removes machine-specific reproduction paths, defines the
  Hutcheson variance notation, and corrects the remaining bibliography and
  grammar points.

The requested Bell--McCaffrey attribution was accepted: their official paper
explicitly discusses negatively biased linearisation estimators. The broader
claim that every cited precedent simply corrects a downward-biased variance
was narrowed. Kauermann and Carroll are described according to their published
abstract: sandwich-estimator variability, interval undercoverage and an
adjustment for that undercoverage. The thesis does not attribute unverified
small-df conservatism to Bell and McCaffrey.

## Code-audit disposition

The later code audit is fair in its main conclusion: it found no defect that
changes a thesis result, but identified one latent report bug and several
reproducibility improvements. The following changes were made:

| Audit point | Decision | Response |
| --- | --- | --- |
| The local-moment component df used `n_p` for both populations | Accepted | The report now selects `n_p` for population P and `n_q` for population Q. A targeted unequal-sample test was added. The four published equal-sample rows are unchanged. |
| The supplied runner differs from the hash in the frozen metadata | Accepted as a provenance issue | Appendix E and the supplement README now give both exact hashes. The diff is limited to atlas-count metadata, output hashes for future runs, and corrected failed-preflight handling; the simulation path is unchanged. All other recorded input hashes match. The historical metadata were not rewritten. |
| The 99-versus-106 figure count is unclear | Accepted | The documentation now distinguishes 99 primary atlas figures from seven companion calibration zooms. |
| Repeated Chapter 6 values were hand-entered | Accepted | Headline counts, selected rates, runtimes and the complete null-band table are generated from the frozen CSV files. The evidence audit independently recomputes and checks every generated value. |
| The preflight builder was called twice on failure | Accepted | The runner now partitions the single `build_manifests` return correctly. A fresh preflight is part of final verification. |
| The mechanism script hard-coded 0.05 and used a strict comparison | Accepted | It now reads `alpha` from the frozen protocol and uses the same inclusive rejection rule as the confirmatory runner. Regenerated values are unchanged. |
| The figure-manifest audit hard-coded 20,000 | Accepted | It now reads the replicate count from the frozen protocol. |
| The unused unbiased-sensitivity p-value should have its own validity mask | Not adopted in the frozen core | The observation is structurally reasonable but does not affect either thesis method or any reported result. Changing `welch.py` would unnecessarily break the exact core-implementation hash recorded with the confirmatory run, so the historical implementation is retained. |
| The packaged deliverables were stale | Obsolete at review time, then rechecked | The package had already been rebuilt after the preceding review. It is rebuilt again after these changes and verified from a fresh extraction. |
| Add the severe $8\times8$ imbalance example | Accepted cautiously | Results and Discussion report the rejection-rate change and the large leading-correction difference as evidence of first-order finite-sample stress, not proof that the deterministic offset is the sole cause. |

These changes affect reporting, diagnostics, audit coverage and provenance
documentation. They do not alter the frozen populations, simulation outputs,
confirmatory estimator, or the thesis's substantive conclusions.

## Major points

| Assessment point | Decision | Response |
| --- | --- | --- |
| Wald conservatism is mostly denominator bias | Partly accepted | A separate 809-configuration follow-up with independent null pilots confirms that standard-error estimation is important. In the representative 3x3 weak null at n=100, Wald is 0.0166 and the independent finite-sample SD gives 0.0551. However, the population first-order SD gives 0.0976 because the numerator variance is also 42% above its first-order value. The thesis now presents a combined mechanism and does not attribute the effect to denominator bias alone. |
| Near independence gives component df approximately nI | Accepted with conditions | Chapter 4 now derives V approximately 2I, tau-squared approximately 4V, and component df approximately nI for fixed positive margins. It also derives the omitted quadratic terms. The relevant condition is nV large relative to dimension d, together with adequate expected counts; `nV >> 1` alone is insufficient. |
| Direct Monte Carlo check of the df approximation | Accepted | Independent pilot simulations now compare population first-order, plug-in median and finite-sample moment dfs. The derivative test and approximation-quality test are explicitly distinguished. |
| Missing Simple and kurtosis-only ablations | Accepted | Both were added to the supplementary mechanism study. Simple Welch is generally close to Wald; kurtosis-only lies between Simple and Expanded Welch. This confirms that the complete pointwise and margin derivative drives most of the added conservatism. |
| Literature gap is overstated | Accepted | Chapter 2 and the source audit now engage Pan and Wall, Bell and McCaffrey, Kauermann and Carroll, Hutter, Hutter and Zaffalon, and Roulston. The contribution is now framed as an MI-specific derivation and assessment within an established general small-sample-adjustment literature. |
| Strong and weak nulls are mixed | Accepted | The abstract and Results now say this explicitly. Results separate the 36 different-skew weak-null configurations from the 72 P=Q configurations. |
| All 108 main null results should be visible | Accepted with separation | The thesis reports the complete profile summary, while the exact 108-row table is retained in the experiment supplement to avoid interrupting the main narrative. |
| Add size-adjusted power | Not adopted | This would answer a different question using a population-specific simulated critical value unavailable in practice. The frozen design intentionally reports null calibration and nominal-threshold detection separately. The limitation is now stated directly. |
| Upper panels are flat | Not changed | The common 0--1 scale is deliberate and lets readers compare the complete landscape. Calibration zooms remain available alongside the full-scale panels. |
| Explain nonmonotone convergence | Accepted cautiously | Results now explain that numerator and denominator approximations can change at different rates as support fills in. The text does not claim a monotonic finite-sample convergence theorem. |
| Use the interval 0.025--0.075 | Accepted descriptively | Results report below/inside/above counts separately by margin profile and method. The interval is explicitly not treated as a formal calibration test. |

## Technical and editorial points

- The MI equality statement now says “every cell.” The earlier positive-support wording was unclear, although equality on all positive cells plus normalisation already forces equality on zero cells.
- Proposition 1 now includes a proof based on the normal/chi-squared mixture representation and convexity of the two-sided normal tail.
- Positive variance sensitivity is now a formal regularity assumption.
- The interpretation of the complete variance sensitivity now includes the selected cell and both margins.
- Empty cells use the explicit zero-weight convention.
- An observed-support bias-correction sensitivity was run and is reported as a diagnostic, not a replacement. Its effect can reverse with sample-allocation direction.
- Hampel is now cited for influence curves. Wilson, Brent, and Deming--Stephan are cited for intervals, root finding and iterative proportional fitting.
- The paired interval formula and the meaning of 534 fixed population pairs are now stated.
- Bibliographic capitalisation and the Marinescu--Balcau arXiv identifier were corrected. The Berrett--Samworth pointer is Section 3(b).
- No Brillinger DOI was added because one was not verified from the primary record; the author-hosted paper remains linked.
- The declaration remains unsigned and undated because only the author can attest it. The title-page degree name, Master of Complex Systems, matches the official University of Sydney course title.

## New evidence files

The explanatory follow-up is separate from the frozen confirmatory study:

- `WelchSatterthwaiteMI/results/thesis_mechanism_check/REPORT.md`
- `WelchSatterthwaiteMI/results/thesis_mechanism_check/ablation_rates.csv`
- `WelchSatterthwaiteMI/results/thesis_mechanism_check/denominator_diagnostics.csv`
- `WelchSatterthwaiteMI/results/thesis_mechanism_check/component_diagnostics.csv`
- `WelchSatterthwaiteMI/experiments/run_thesis_mechanism_check.py`
- `WelchSatterthwaiteMI/experiments/report_thesis_mechanism_check.py`

The active manuscript interpretation is intentionally narrower than the
assessment's strongest claims: denominator estimation matters; the complete
df expansion has a measurable effect; neither fact establishes Expanded
Welch as a generally better test or supplies a universal finite-sample fix.
