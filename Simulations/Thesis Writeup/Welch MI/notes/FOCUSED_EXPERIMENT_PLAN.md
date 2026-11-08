# Focused Experiment and Thesis Revision Plan

Agreed direction: 6 October 2026. Implementation, the complete simulations,
manuscript revision and independent package verification are complete.
Scientific tests, raw-record audits, figure regeneration and clean source
compilation pass. See SUBMISSION_CHECK.md for the final acceptance record.

This is the active experimental plan for the Master of Computer Science
thesis. It supersedes the earlier requirement to report every completed
experiment family. The previous manuscript is preserved in
archive/pre_focused_20261006/ and the earlier simulation archives remain
intact. Replacement evidence is in WelchSatterthwaiteMI/results/focused_study/.

The bounded extension agreed on 10 October is specified separately in
[UNEQUAL_SAMPLE_CHECK_PLAN.md](UNEQUAL_SAMPLE_CHECK_PLAN.md). It reuses two
balanced settings and adds four unequal-sample settings, giving 236 unique
settings overall. The original 232-setting populations, records and plan
below are unchanged; the new check does not restore the broad imbalance grid.

The subsequent bounded construction extension is specified in
[LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md](LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md).
It adds four matched 16 x 16 first-block transfer settings to check the
strongest sparse-table finding. The combined study has 240 unique settings,
70 population pairs and 4800000 distinct sampled pairs. The original design
below and both methods remain unchanged; no third comparator is added.

## 1. Purpose and narrative

Evaluate when Expanded Welch provides a useful change to Normal Wald for
comparing the MI of two independent categorical populations. Keep the
mathematical derivation and the two main thesis research questions. Organise
the empirical evaluation around three connected questions:

1. How do sample size, table size and margins affect false positives and the
   ability to calculate the tests?
2. How does the strength of association affect the degrees-of-freedom
   adjustment and the resulting false-positive rate?
3. What does the adjustment mean for detecting a true MI difference?

Estimation diagnostics explain the patterns, and a small construction check
tests whether a representative finding depends on the copying mechanism.
The questions determine the comparisons; the results determine the answers.
Do not prescribe a positive finding for either method.

The thesis should move from performance under equal MI, to an explanation of
that performance, to detection when MI differs. Interpret each figure beside
the evidence, rather than leaving the first interpretation to a later
discussion chapter. Depth comes from checked derivations, controlled
comparisons and explanations of mechanisms, not the number of plots or pages.

## 2. Shared populations and sampling

### Table sizes and margins

Use square tables of sizes 2 x 2, 4 x 4, 8 x 8 and 16 x 16. This gives 4, 16,
64 and 256 cells. Category labels are 1 through k for a k x k table.

Use the same marginal vector for X and Y within each population. For a
dominant category probability rho, set

\[
a_k(\rho)=\left(\rho,\frac{1-\rho}{k-1},\ldots,
                    \frac{1-\rho}{k-1}\right).
\]

The three regimes are:

| Margin regime | P: rows and columns | Q: rows and columns |
| --- | --- | --- |
| Uniform | Each category has probability 1/k | Each category has probability 1/k |
| Same skew | a_k(0.8) | a_k(0.8) |
| Different skew | a_k(0.7) | a_k(0.8) |

Uniform versus same skew compares equal and uneven category frequencies.
Different skew additionally allows the populations to have different margins.
Do not describe these three regimes as an ordered scale of increasing skewness.

### Copying construction

For one population with marginal vector a:

1. Draw X with category probabilities a.
2. With probability lambda, set Y = X.
3. Otherwise draw Y independently with category probabilities a.

The resulting cell probabilities are

\[
p_{ij}(\lambda)=(1-\lambda)a_i a_j
                  +\lambda a_i\mathbf{1}_{\{i=j\}},
\qquad 0\leq\lambda<1.
\]

Both branches give Y the same margins a, so their mixture preserves the
specified row and column margins. Increasing the copying probability changes
association while keeping category frequencies fixed. At lambda = 0, X and Y
are independent. At lambda = 1, Y = X and MI equals the entropy of a; this
endpoint is used to check feasibility, not to construct a sampled population.

Choose lambda separately for P and Q to reach each target MI. Matching MI does
not generally mean matching lambda. Under uniform or same-skew margins, equal
MI produces P = Q in this construction. Under different-skew margins, equal
MI produces different joint tables.

For each target, solve I(p(lambda)) = target on [0, 1] using Brent's method,
with root tolerances xtol = 1e-15 and rtol = 1e-14. Before sampling, require
strictly positive cells, a total probability within 1e-12 of one, marginal
errors no larger than 1e-12, and MI error no larger than
1e-12 + 1e-8 times the target. Record the achieved probabilities, lambda and
MI, rather than reconstructing samples from rounded manuscript matrices.

Mathematical preflight checks have verified these properties for all planned
population pairs. Their population MI variances and variance-sensitivity
variances are positive. The largest target MI is 0.22 nats; the smallest
entropy endpoint among the chosen margins is approximately 0.5004 nats.
These checks establish feasible populations, not the statistical performance
of the tests. Unit tests of the new implementation are still required.

### Sampling and methods

For every distinct statistical setting, draw 20,000 independent pairs of
multinomial count tables from the fixed P and Q. Samples from P and Q are
independent; copying introduces dependence between X and Y within an
observation. Apply both methods to the same count-table pair.

Use Normal Wald and Expanded Welch only, with a two-sided threshold of 0.05.
Keep the implemented MI estimator, bias correction, standard error,
degrees-of-freedom calculation and numerical validity rules unchanged.
Use the full declared dimensions in the bias correction and retain negative
bias-corrected MI estimates. All sample sizes are equal between populations,
so the two deterministic bias corrections cancel in the estimated difference.
Unequal finite-sample bias between the populations can nevertheless remain.

The thesis sign convention remains Delta = I(P) - I(Q). In detection studies,
Q has the higher MI, so Delta is negative. Plot the true nonnegative magnitude
|Delta|, not the magnitude of a sampled estimate.

## 3. Study 1: sample size, table size and margins

**Question:** when do the methods return usable results, and how close are
their false-positive rates to the intended 5%?

Use all four sizes and all three margin regimes. Set I(P) = I(Q) = 0.02 nats.
For each of these twelve fixed population pairs, vary only sample size:

\[
n_P=n_Q\in\{10,20,50,100,250,500,1000,2500,10000,50000\}.
\]

This gives 120 settings. The larger sample sizes are part of the same sweep,
not a separate convergence experiment. Keep the smallest listed settings even
if validity or rejection is low; exclude n = 1, 2 and 5 from the new study.

Main comparisons:

- Compare the four sizes under different skew, holding target MI and the
  margin rule fixed. Explain how spreading observations over more cells
  relates to empty cells, validity and estimation error.
- Compare all three margin regimes at 4 x 4 and 16 x 16. These preselected
  sizes show the contrast in a middle-sized and a larger table, including
  whether the effect of margins changes with table size.

The full crossed design is retained even though the main figures select
particular comparisons. Appendix C presents the remaining four size-margin
curves and a complete 120-setting rejection-and-validity table. Do not replace
individual results with an overall average or a tally of which method wins.

Explain that holding the dominant probability fixed while increasing k spreads
the remaining mass across more categories. Table size therefore changes the
cell probabilities as well as their number; it is a controlled comparison
within this margin rule, not an isolated effect of dimension under unchanged
probabilities.

## 4. Study 2: association strength and degrees of freedom

**Question:** how does moving towards independence affect the adjustment?

Use 4 x 4 tables under different skew as the representative setting. Keep
the size, margins and copying construction fixed. Set equal population MI at

\[
I(P)=I(Q)\in\{0.0001,0.0003,0.001,0.003,0.01,0.02,0.05\}
\]

and repeat at n = 100 and n = 1000. These fourteen settings include two
settings already present in Study 1, so they add twelve distinct settings.

Show false-positive rates and the distribution of estimated combined degrees
of freedom. Report the median and 5th-95th percentile range, with the fraction
of Expanded Welch results to which those summaries apply. A range across
repetitions is not a Monte Carlo confidence interval for the median.

Link the degrees of freedom to the cutoff from the Student t distribution:
smaller degrees of freedom require a larger absolute statistic for rejection.
Use the estimation diagnostics below to assess whether this change addresses
the observed problem or makes an already low rejection rate lower.

The targets are positive. Do not treat this study as an evaluation at exact
independence, and do not generalise its mechanism findings to every table
size without supporting evidence.

## 5. Study 3: detecting an MI difference

**Question:** how does detection increase with the population MI difference,
and what changes when the Expanded Welch adjustment is used?

Fix I(P) = 0.02 nats and set I(Q) = 0.02 + d, where

\[
d=|\Delta|\in\{0,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2\}.
\]

Use n = 1000 and n = 10000 for two controlled comparisons:

- All four sizes under different skew.
- All three margin regimes at 4 x 4.

The 4 x 4, different-skew comparison is shared. There are six distinct
size-margin combinations, giving 108 settings before removing the twelve
zero-difference settings already in Study 1. This study adds 96 settings.

Keep the zero-difference point in every detection comparison. Interpret
rejection at nonzero differences alongside each method's null rate and
validity. A smaller detection rate is not itself an improvement, and a larger
rate is not sufficient if false positives are excessive.

Use the same difference grid for every planned comparison. The largest
target, 0.22 nats, is feasible across the copying populations. Show the full
range but provide a common small-difference view so that the first nonzero
points are not compressed by the 0.2-nat endpoint. Prefer an inset or clearly
identified companion view of the same data, not another experimental family.

## 6. Improvement 1: explain estimation error

This improvement uses the existing planned repetitions. It adds no population
pairs or statistical settings. Compute diagnostics for every setting, then
present a preselected subset where they answer the central questions.

Retain per-repetition plug-in and corrected MI for each population, the signed
corrected difference, component variance estimates, squared standard error,
statistic, component and combined degrees of freedom, p-values, validity
flags and reasons. Retain sufficient empty-cell/row/column summaries to
describe sparse sampling. Keep scalar outputs in manageable chunks; there
is no requirement to retain every full count-table pair.

The diagnostics are:

| Diagnostic | Quantity and purpose |
| --- | --- |
| Bias of the estimated difference | Mean corrected difference minus the known Delta; assesses systematic displacement from the true difference. |
| Individual MI bias | Mean corrected MI minus population MI for P and Q separately; explains how unequal bias can enter their difference. |
| Observed sampling variance | Sample variance of corrected differences across repetitions; measures their actual spread. |
| Estimated sampling variance | Mean squared standard error; compare with observed sampling variance to assess the estimated uncertainty. |
| Population first-order variance | V(P)/n_P + V(Q)/n_Q; compare with observed sampling variance to assess the linear approximation separately from estimating its inputs. |
| Degrees of freedom | Median and 5th-95th percentile range among Expanded-valid repetitions; relates the adjustment to its rejection cutoff. |
| Validity and empty counts | Valid-result frequency and empty-cell/row/column summaries; distinguish numerical failure from a low rejection rate. |

For M finite differences, calculate the empirical variance with denominator
M - 1, centred at their sample mean, not at the known Delta. Bias is measured
separately. Compare mean squared standard error with that empirical variance;
do not square the mean standard error. Report the ratio as undefined if the
empirical variance is zero.

Use all finite MI differences for the primary bias and variance summaries,
including repetitions with invalid test outputs. For the estimated/observed
variance comparison, use the same matched subset with finite difference and
finite squared standard error; retain finite zero variance estimates. Report
the included fraction and distinguish these diagnostics from rates
conditioned on valid p-values. Summarise degrees of freedom on Expanded-valid
outputs, not an unspecified collection of finite numbers.

Main presentation: one compact diagnostic table for different-skew 4 x 4 and
16 x 16 null populations at n = 1000 and n = 10000. These four settings are
chosen before seeing the new results. Report difference bias, observed
standard deviation, the square root of the mean estimated variance, the
estimated/observed variance ratio and validity.
Use full diagnostic records to check other claims.

Report the Monte Carlo standard error of difference bias as the observed
standard deviation divided by sqrt(M). Treat a variance ratio as an estimated
diagnostic; if a conclusion depends on a small departure from one, quantify
its simulation uncertainty by resampling the matched per-repetition
difference/variance records together, rather than generating another
population grid.

Supporting presentation: the 4 x 4 association-strength sweep, plus the
different-skew 4 x 4 and 16 x 16 null results at n = 50000, in Appendix C.
These support the near-independence and large-sample explanations without
adding a second main landscape.

Interpret diagnostic agreement or disagreement as evidence about a possible
mechanism. Bias, estimated uncertainty, dependence and the reference cutoff
can act together; a variance ratio or degrees-of-freedom curve does not
apportion their causal contributions. Do not transfer the old construction's
numerical mechanism findings into this redesigned study. If a further
dependence diagnostic is needed, use saved outputs and label any
outcome-motivated analysis as exploratory.

## 7. Improvement 2: small alternative-construction check

**Question:** does a representative finding persist when association is
concentrated in four cells rather than generated by copying?

Use 4 x 4 tables under different skew. Construct an independence table from
the prescribed margins, then add t to cells (1,1) and (2,2), and subtract t
from cells (1,2) and (2,1). Keep every other probability unchanged.

Choose t separately for each population to match its target MI, with positive
cells and the same construction checks used above. Solve on
0 <= t < a_1 a_2, using the endpoint only for feasibility and
root bracketing. This is the existing first-block construction, not a new
statistical method.

Match the copying study at:

- I(P) = I(Q) = 0.02 nats, with n = 1000 and n = 10000.
- I(P) = 0.02 and I(Q) = 0.03 nats, with n = 1000 and n = 10000.

This adds four settings and two population pairs. Compare rejection,
validity and the same estimation diagnostics with their copying counterparts.
Keep the cross-construction Monte Carlo intervals based on independent
simulation streams; within each construction, Wald and Expanded Welch remain
paired on the same samples.

Place one compact comparison in Appendix C and discuss its implication once
in the main synthesis. Agreement supports that specific cross-construction
comparison; disagreement narrows the recommendation. Neither outcome
establishes performance across all association patterns. Do not extend this
check into another full grid.

## 8. Outcome measures and uncertainty

For each method, report rejection divided by all 20,000 repetitions and the
fraction producing a valid p-value. Invalid outputs contribute no rejection
to this primary rate, but do not represent evidence for equal MI.

Also retain rejection conditional on that method being valid and rejection
on the subset where both methods are valid. Use these supporting rates when
they explain whether invalid outputs account for a performance difference.
Report their denominators; a zero denominator gives an undefined rate.

Use the current method-specific validity rules. Normal Wald requires a
finite corrected difference, finite positive standard error, a finite
p-value, and estimated V(P) + V(Q) greater than 1e-14. Expanded Welch also
requires finite positive component and combined degrees of freedom and a
finite p-value. Do not add smoothing, trim empty rows, clip corrected MI,
change the zero-component rule or introduce an expected-count eligibility
filter. Record invalid reasons even where categories overlap.

Use Wilson 95% intervals for individual rejection and validity rates, and
report their Monte Carlo standard errors. For a proportion p, the approximate
standard error is sqrt(p(1-p)/20000). At p = 0.05 this is about 0.00154,
giving an approximate 95% half-width of 0.00302. This justifies the planned
precision without treating very small numerical differences as meaningful.

For the within-setting Wald-minus-Expanded rejection contrast, use the sample
variance of the paired indicators R_Wald - R_Expanded divided by the number
of pairs, with the existing approximate 95% interval. Preserve disagreement
counts so this calculation can be checked independently. Apply the relevant
validity denominator when presenting a conditional contrast. The intervals
describe simulation uncertainty at fixed populations, not an average over
all possible tables.

Keep the 90% valid-result marker convention if useful, explain it once, and
do not interpret it as a validated safety threshold. Do not claim improvement
merely because rejection decreases, and do not call the detection comparison
power at equal achieved false-positive rates.

## 9. Figures and chapter changes

### Main results sequence

Plan approximately five lead figures and one short diagnostic table:

| Display | Fixed setting / variation | Question and discussion |
| --- | --- | --- |
| Figure 1 | Different skew, equal MI 0.02; four table sizes; sample-size sweep | How table size changes false positives and valid-result frequency as more observations become available. |
| Figure 2 | Equal MI 0.02; 4 x 4 and 16 x 16; all three margins; sample-size sweep | Whether equal or different uneven margins alter the size-related findings. |
| Figure 3 | 4 x 4, different skew; common-MI sweep at n = 100 and 1000 | How association strength relates to estimated degrees of freedom and false positives. |
| Diagnostic table | 4 x 4 and 16 x 16, different skew, equal MI 0.02; n = 1000 and 10000 | Whether bias and estimated uncertainty help explain the observed rates. |
| Figure 4 | Different skew; all four sizes; difference sweep at n = 1000 and 10000 | How detection grows and whether the adjustment changes the practical trade-off. |
| Figure 5 | 4 x 4; all three margins; the same difference sweep and sample sizes | Whether the detection finding changes when category frequencies are equal or uneven. |

Show both methods together in each relevant panel. Use a labelled logarithmic
sample-size axis and a labelled logarithmic common-MI axis; keep comparable
scales and visual encodings consistent. Put false-positive and detection
settings in ordinary text beside the plots, not long captions.

Null figures must expose low validity through matching strips or adjacent
compact displays, with the full rates in Appendix C. Study 2 distinguishes
the spread of degrees of freedom from simulation uncertainty. Detection
figures need a readable small-difference view as well as the full range.
Use shared printed-size templates, readable labels and text-margin bounds.
Four panels can use a two-column layout; do not force every factor and metric
into a single oversized or illegible grid.

The interpretation beside each display should establish the observation,
give numerical evidence, explain the relevant diagnostic or calculation,
state its practical meaning, and lead to the next question. Use that as a
flexible guide, not five mandatory sentences. Distinguish observations from
proposed explanations, and avoid repeating the same explanation at every
curve. Planned settings remain visible whether the results help either
method or not.

### Chapter 5: Experimental Design

Use sections for the evaluation questions, constructing populations, the
three controlled studies and supporting check, and sampling/outcome measures.
Begin with why known population MI is needed, then explain copying using the
binary example and extend it to larger tables. Explain how the copying
probability is chosen; give a checked numerical example before the grids.
Keep a plain question/settings/purpose table, without bracketed products or
a catalogue of old experiment families.

### Chapter 6: Experimental Results and Discussion

Mirror the three studies: sample size and population structure, association
strength and adjustment, then detection. Integrate the diagnostic table with
the first two discussions. End with a short practical synthesis and the
meaning of the supporting construction check, rather than another first
reading of every plot.

### Remaining chapters and appendices

- Keep the two main research questions and the mathematical substance in
  Chapters 2-4; update construction references and examples where needed.
- Rewrite Chapter 7 around the redesigned evidence, its practical scope and
  limitations. Do not retain obsolete numerical diagnostics or conclusions.
- Update the Introduction, abstract and Conclusion only after the new results
  are checked. Restate contributions, impact, limitations and future work.
- Appendix A retains supporting calculations and the independence-boundary
  explanation. Reconcile any numerical illustrations with their stated data.
- Appendix B gives the complete copying and four-cell formulas, target search,
  exact parameter grids, sampling algorithm, estimators, validity and interval
  formulas. A reader must be able to reconstruct the study without code.
- Appendix C holds the remaining Study 1 curves, all 120 main null settings,
  focused diagnostic detail and the four-setting construction comparison.
  Keep alternative-result tables compact; do not move every old family here.
- Retain a concise computational-complexity discussion and a small timing
  table relevant to the Master of Computer Science context. Time the two
  methods on the same pre-generated inputs from the four different-skew,
  equal-MI populations at n = 1000, excluding generation and construction.
  Use 200 table pairs, 20 warm-up calls and five timed passes per method;
  report units, median, interquartile range and the measurement environment.
  This is a timing check, not an additional statistical experiment family.

Remove the old main-text families for imbalance, rectangular tables,
alternative log-linear constructions, association-location sweeps, extreme
skew and exact-independence simulation. Keep the existing records internally.
The new results do not support conclusions about unequal sample sizes,
arbitrary association patterns or an empirical exact-independence boundary.

Keep the manuscript standalone and at an accessible honours/master's level:
complete statistical names, concrete mechanisms, useful intermediate steps,
developed paragraphs and short captions. Do not include project paths,
configuration IDs, version-control history or protocol administration in it.
Leave the working draft unchanged unless the user requests a later sync.

## 10. Scope and implementation order

### Statistical scope

| Part | Distinct settings added |
| --- | ---: |
| Study 1: sample size, size and margins | 120 |
| Study 2: common MI, excluding settings shared with Study 1 | 12 |
| Study 3: detection, excluding settings shared with Study 1 | 96 |
| Four-cell construction check | 4 |
| Total | 232 |

The study contains 68 distinct population pairs and 4,640,000 sampled table
pairs at 20,000 repetitions per setting. The estimation diagnostics require
no extra statistical samples. Pilot and timing samples are separate and are
not included in these statistical totals. Shared settings are simulated once
and reused in the displays that need them.

### Implementation sequence

1. Implement a separate focused-study specification and copying constructor.
   Build a deterministic manifest of all 232 settings and 68 population
   pairs. Preserve the current archives and scientific methods.
2. Add tests for margins, positivity, MI endpoints and target solving; the
   binary equivalence to the four-cell transfer; population assumptions;
   scope counts; shared-setting reuse; sign conventions; and unchanged
   method-specific validity. Check scalar and batched calculations agree.
3. Use a documented master seed of 20261006, stable per-setting seed
   derivation and separate P/Q streams. Ensure checkpointing and batch size
   do not change outcomes or duplicate repetitions. Record dependencies and
   seed information in the reproduction record.
4. Run a technical pilot of 200 repetitions per setting. Check sampling,
   output fields, finite quantities, validity accounting, memory and runtime,
   including 16 x 16 at the largest n. Use this to choose batch sizes and
   estimate execution time, not to remove poor-performing configurations.
   Keep pilot samples separate from the final 20,000 repetitions.
5. Run the complete 232-setting study with checkpoints and chunked scalar
   output. Collect the two methods on each shared table pair and retain the
   diagnostics above. Check every requested setting has exactly 20,000
   repetitions. Do not pool the old first-block runs into the copying study.
6. Independently audit population definitions, method outputs, counts, rates,
   Wilson and paired intervals, diagnostic masks and the source of every
   displayed value. Verify common-valid Expanded rejection is a subset of
   Wald rejection, up to numerical tolerance. Recompute selected statistics
   from saved repetitions, not only from summary tables.
7. Generate the planned main and supporting figures plus the diagnostic and
   null tables. Review readability at printed size. Write the results from
   this evidence, including unfavourable or uninformative findings.
8. Revise Chapters 5-8 and the relevant earlier text, appendices and front
   matter. Recheck literature claims and cite imported methods where used.
   Keep the reporting questions separate from any exploratory follow-up.
9. Run the mathematical and scientific regression tests, evidence audit,
   clean LaTeX build and complete-page visual review. Rebuild the final
   delivery package and its verification record only after the replacement
   evidence and manuscript agree.

### Completion criteria

The revision is complete when all planned settings have audited results,
the diagnostics and construction check have been interpreted, the exact
study is reproducible from the manuscript and Appendix B, every main figure
answers its stated question, and the empirical claims throughout the thesis
use the new evidence and its actual scope. Tests and a clean build must pass,
and figure sizes and explanations must meet the writing preferences in
AGENTS.md and THESIS_GOAL.md. There is no minimum page count and no requirement
for Expanded Welch to outperform Wald.

## 11. Sources informing the design

- Morris, White and Crowther (2019), [*Using simulation studies to evaluate
  statistical methods*](https://onlinelibrary.wiley.com/doi/10.1002/sim.8086),
  Statistics in Medicine, DOI 10.1002/sim.8086,
  informs question-led design, performance measures, factor interactions and
  Monte Carlo uncertainty.
- Berrett and Samworth (2021), [*USP: an independence test that improves on
  Pearson's chi-squared and the G-test*](https://pmc.ncbi.nlm.nih.gov/articles/PMC8652272/),
  Proceedings of the Royal Society A, DOI 10.1098/rspa.2021.0549,
  supplies the four-cell construction example and a model for combining
  estimator diagnostics with false-positive and detection comparisons. Its
  independence-testing problem differs from the equal-MI hypothesis here.
- [EXEMPLAR_REVIEW_NOTES.md](EXEMPLAR_REVIEW_NOTES.md) and
  [DLI_EXEMPLAR_REVIEW_NOTES.md](DLI_EXEMPLAR_REVIEW_NOTES.md) record the supplied
  thesis comparisons. Follow their question-to-evidence correspondence and
  integrated interpretation, not their page counts or every stylistic choice.
