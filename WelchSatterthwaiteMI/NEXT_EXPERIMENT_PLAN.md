# Final Thesis Experiment Protocol: Differential Mutual Information

**Status: final design, awaiting implementation freeze.** The protocol must be
encoded in a machine-readable configuration file, reviewed, and committed
before the full simulation is run. Smoke tests may be used to find software
errors, but their results are not thesis evidence. After the freeze, changes
to factors, outcomes, or reporting rules must be documented as protocol
deviations rather than silently incorporated.

The experiment evaluates three deterministic tests of

\[
H_0:I(P)=I(Q)
\]

for two independently sampled categorical populations. It is organized around
four experimental questions:

1. **Controls:** Do all methods behave correctly in well-sampled settings and
   under the strong null $P=Q$?
2. **Calibration and breakdown:** When $I(P)=I(Q)$, how do false-positive
   rate and numerical validity change with sample size, alphabet size,
   skewness, and distributional shape?
3. **Detection:** When $I(P)\ne I(Q)$, how does power increase with the true
   MI difference and sample size?
4. **Robustness:** Do the conclusions persist under alternative dependence
   patterns and unequal sample sizes?

The main comparison is between Normal Wald, Simple Welch, and Expanded Welch.
Constrained likelihood-ratio and resampling procedures address different,
secondary questions and are not part of the confirmatory sweep.

---

## 1. Statistical question and primary comparison

Let $P$ and $Q$ be two independently sampled joint distributions for
categorical pairs $(X,Y)$. Define

\[
\Delta_I = I(Q)-I(P).
\]

Each method performs the two-sided test

\[
H_0:\Delta_I=0
\qquad\text{against}\qquad
H_1:\Delta_I\ne 0.
\]

The experiment varies a nonnegative effect parameter $e$:

- At $e=0$, $I(P)=I(Q)$. Rejection is a false positive.
- At $e>0$, $I(Q)>I(P)$. Rejection is a true positive, and the rejection
  rate is the detection power.

The primary significance level is $\alpha=0.05$. Results at
$\alpha=0.10$ and $\alpha=0.01$ are secondary sensitivity analyses.

The primary method contrast is **Expanded Welch versus Normal Wald** under the
equal-MI, different-shape null. For every exact configuration, compare their
absolute false-positive-rate errors,

\[
\left|\widehat{\mathrm{FPR}}-0.05\right|.
\]

Simple Welch is retained to show whether any improvement comes from an
ordinary Student correction or from the MI-specific Expanded Welch degrees of
freedom. Identical-distribution nulls, power, secondary significance levels,
and robustness blocks are supporting analyses. No single pooled average may
replace the configuration-level results.

---

## 2. Evidence status and scope

The existing 72-pair supervisor experiment is preliminary evidence that
motivated this design. It remains reproducible, but it is not the final
confirmatory experiment because its configurations and summaries were refined
while results were being examined.

The experiment in this document is the primary thesis validation. Before it is
run:

1. Encode every factor level, seed rule, population rule, outcome, and output
   path in `experiments/FINAL_PROTOCOL.json`.
2. Commit the protocol, implementation, and unit tests together.
3. Record their Git commit and SHA-256 hashes in the run metadata.
4. Store results in `results/detection_breakdown_sweep/`; do not overwrite any
   preliminary result directory.

The scope is positive-MI differential testing. The independence boundary
$I(P)=I(Q)=0$ is excluded because the first-order MI variance used by all
three tests is degenerate there. Observations are independent multinomial
draws, and the two samples are independent of one another.

---

## 3. Methods compared

Every simulated table pair is evaluated by the same three analytic methods:

| Method | Reference distribution | Purpose in the comparison |
| --- | --- | --- |
| Normal Wald | Standard normal | Existing analytic baseline |
| Simple Welch | Student $t$, ordinary Welch-Satterthwaite degrees of freedom | Direct Welch adaptation |
| Expanded Welch | Student $t$, MI-specific variance-influence degrees of freedom | Proposed method |

All methods use the same bias-corrected MI difference and the same estimated
standard error. They differ only in the reference distribution and effective
degrees of freedom.

The implementation must call `differential_mi_pvalues` from
`src/welch_differential_mi/welch.py`. The formulas must not be reimplemented in
the experiment script.

---

## 4. Population construction

The construction must produce exact, inspectable population tables before any
sampling occurs. No population is selected according to its simulated test
performance.

### 4.1 Margins

For an alphabet of size $r$, define a one-dominant-category margin

\[
m_r(d)=\left(d,\frac{1-d}{r-1},\ldots,
                 \frac{1-d}{r-1}\right).
\]

The four skewness levels are

| Label | Row margin | Column margin |
| --- | --- | --- |
| Balanced | Uniform, (1/r) and (1/c) | Uniform |
| Mild | (m_r(0.70)) | (m_c(0.70)) |
| Strong | (m_r(0.90)) | (m_c(0.90)) |
| Ultra | (m_r(0.95)) | (m_c(0.95)) |

These are deterministic margins. Dirichlet draws are not used in the main
sweep, so each reported configuration has one exact interpretation.

### 4.2 Dependence paths

The primary population $P$ uses the ordinal interaction returned by
`interaction_pattern(r, c, "ordinal")`.

The different-shape $Q$ path uses:

- row margins obtained by rolling the $P$ row margin by one position;
- column margins obtained by rolling the $P$ column margin by minus one
  position; and
- the negative ordinal interaction.

Changing the interaction is essential in the balanced case because rolling a
uniform margin leaves it unchanged.

For every generated null pair, verify

\[
|I(P)-I(Q)| \le 10^{-10}
\]

and, for the different-shape construction,

\[
\lVert P-Q\rVert_1 > 10^{-8}.
\]

The second condition only verifies that the populations are not identical. No
minimum $L^1$ distance is used to select populations.

### 4.3 Measure the shared reachable MI range

The entropy quantity

\[
\min\{H(X),H(Y)\}
\]

is an upper bound on MI. It is not necessarily reachable by a chosen
one-parameter log-linear interaction path. Therefore it must not be used
directly as the effect scale.

For each shape and skewness level, estimate the stable reachable MI range of
both the $P$ and different-shape $Q$ paths before defining any target MI:

1. Evaluate `association_table_from_interaction` at association strengths
   (0,0.25,0.5,1,2,4,8,16,32,64,128).
2. Stop a path at the first numerical construction failure.
3. Confirm that achieved MI is nondecreasing up to numerical tolerance
   $10^{-10}$. If it is not, record the construction as invalid.
4. Let $M_P$ and $M_Q$ be the largest successfully achieved MI values.
5. Define the shared reachable scale

\[
M=\min(M_P,M_Q).
\]

All requested targets are kept at or below (0.8M), leaving a 20% buffer
below the largest demonstrated reachable value. The entropy upper bound,
$M_P$, $M_Q$, and $M$ must all be saved.

If $M\le 10^{-8}$, do not manufacture a population. Record the construction
and reason in `infeasible_configurations.csv`.

A development preflight successfully constructed the shared reachable range
for all 32 primary shape-by-skewness combinations. The frozen runner must
repeat this check and save the achieved ranges; the development preflight is
not a substitute for the recorded full-run validation.

### 4.4 Baseline MI and effect sizes

For both comparison constructions, set

\[
I(P)=0.20M
\]

and use

\[
e\in\{0,0.01,0.025,0.05,0.10,0.20,0.40,0.60\}.
\]

The $Q$ target is

\[
I(Q)=(0.20+e)M.
\]

Thus the largest target is (0.80M), and the true MI difference is

\[
\Delta_I=eM.
\]

Save both $e$ and the absolute difference $\Delta_I$. The relative effect
makes curves comparable across different MI ranges, while the absolute value
shows the actual size of the difference being detected.

### 4.5 Identical and different-shape comparisons

Two population relationships are evaluated:

1. **Identical-distribution baseline.** At $e=0$, set $Q=P$ exactly. At
   $e>0$, construct $Q$ on the same margin and interaction path as $P$,
   at the larger target MI.
2. **Equal-MI, different-shape baseline.** Construct $Q$ using the rolled
   margins and negative interaction from Section 4.2. At $e=0$, the two
   distributions differ but have equal MI. At $e>0$, retain that $Q$ path
   and increase only its target MI.

The same shared scale $M$ is used for both relationships. This keeps the
baseline MI and absolute effect sizes identical when comparing the two
relationships.

---

## 5. Confirmatory experiment sequence

The same population definitions are reused across the experiments below. This
provides a direct progression from known controls, through null calibration,
to power and robustness, while avoiding a single undifferentiated factorial
summary.

### 5.1 Shared primary factors

| Factor | Exact levels |
| --- | --- |
| Shape | `2x2`, `2x3`, `3x3`, `3x5`, `4x4`, `4x8`, `5x5`, `8x8` |
| Skewness | balanced, mild, strong, ultra |
| Population relationship | identical-distribution, different-shape |
| Calibration sample size, $n_P=n_Q=n$ | 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50, 75, 100, 150, 250, 500, 1000 |
| Power sample size, $n_P=n_Q=n$ | 5, 10, 20, 50, 100, 250, 500, 1000 |
| Positive relative effect $e$ | 0.01, 0.025, 0.05, 0.10, 0.20, 0.40, 0.60 |
| Replicates | 10,000 independently sampled table pairs per cell |

### 5.2 Experiment 1: controls

The control analysis uses predeclared subsets of the calibration experiment;
it does not require separately generated data.

1. **Strong-null control:** $P=Q$, balanced margins, all shapes, and
   $n\in\{50,250,1000\}$.
2. **Weak-null control:** $P\ne Q$ but $I(P)=I(Q)$, balanced margins, all
   shapes, and $n\in\{50,250,1000\}$.
3. **Large-sample control:** compare all three methods at $n=1000$, where
   their reference distributions should be close.

These controls establish that the implementation behaves sensibly before the
low-count results are interpreted.

### 5.3 Experiment 2: null calibration and breakdown

Set $e=0$ and cross all eight shapes, four skewness levels, two population
relationships, and 18 calibration sample sizes. This produces

\[
8\times4\times2\times18=1{,}152
\]

exact cells, or 11.52 million simulated table pairs. The outcome is the
false-positive rate at each sample size. This experiment identifies where each
method is calibrated, liberal, conservative, or numerically invalid.

Very small samples are intentional. Values such as
$n<\max(r,c)$ will often produce empty observed margins and undefined
analytic statistics. These rows define a structural breakdown region and are
reported separately from the ordinary operating region
$n\ge\max(r,c)$.

### 5.4 Experiment 3: detection power

For the eight predeclared power sample sizes, cross the same shapes,
skewness levels, and population relationships with the seven positive values
of $e$. This produces

\[
8\times4\times2\times8\times7=3{,}584
\]

exact cells, or 35.84 million simulated table pairs. The outcome is power as a
function of the true absolute MI difference
$\Delta_I=eM$. The null result at the same configuration is always shown
beside its power curve so that liberal size is not mistaken for better
detection.

### 5.5 Reporting exact configurations

The confirmatory experiments contain 4,736 exact cells and 47.36 million
simulated table pairs before the targeted robustness blocks. The main report
must not average away shape, skewness, sample size, population relationship,
or effect. Compact win/tie/loss counts and median paired differences may be
reported only after the exact results are available in tables and linked
appendix figures.

---

## 6. Targeted robustness blocks

The full sweep uses one interpretable interaction pair. Two smaller blocks test
whether its conclusions depend on that choice or on equal sample sizes.

### 6.1 Interaction-pattern robustness

Run the following additional configurations:

| Factor | Exact levels |
| --- | --- |
| Shape | `3x3`, `3x5`, `5x5`, `8x8` |
| Skewness | balanced, strong, ultra |
| Interaction pair | checkerboard/cyclic; fixed-random-A/fixed-random-B |
| Population relationship | different-shape only |
| $n_P=n_Q$ | 5, 10, 20, 50, 100, 250 |
| Relative effect $e$ | 0, 0.10, 0.40, 0.60 |
| Replicates | 10,000 |

The random interactions are generated once from stable, documented seeds and
then treated as fixed population definitions. Results for each interaction
pair are reported separately. They are not combined into an unnamed average.

The shared reachable scale is recalculated for every interaction pair using
Section 4.3. This block has 576 simulation cells, or 5.76 million table pairs.

### 6.2 Unequal-sample robustness

Run a focused imbalance block using the primary ordinal/negative-ordinal
population construction:

| Factor | Exact levels |
| --- | --- |
| Shape | `2x2`, `3x3`, `5x5`, `8x8` |
| Skewness | strong, ultra |
| Population relationship | different-shape only |
| Smaller sample $n_P$ | 5, 10, 20, 50, 100 |
| Ratio $n_Q:n_P$ | 2:1, 5:1, 10:1 |
| Relative effect $e$ | 0, 0.10, 0.40 |
| Replicates | 10,000 |

This block contains 360 simulation cells, or 3.6 million table pairs. It
tests sample imbalance without crossing that factor through the entire main
grid.

Together, the confirmatory experiments and both robustness blocks contain
5,672 exact cells and 56.72 million simulated table pairs.

---

## 7. Simulation procedure

For every population/sample-size/effect configuration:

1. Construct and validate $P$ and $Q$ before sampling.
2. Draw independent multinomial count tables from $P$ and $Q$.
3. Compute all three methods on the same table pair.
4. Process replicates in blocks of at most 2,000 to bound memory use.
5. Use a stable seed derived from the master seed and the complete
   configuration identifier. Changing execution order or worker count must not
   change a configuration's simulated data.
6. Aggregate counts online. Do not save all simulated contingency tables.

The complete list of configurations is generated from the frozen protocol
before any full-run outcomes are examined. A configuration cannot be added,
removed, or rerun selectively because of its observed performance.

Population construction failures must catch and record both `ValueError` and
`RuntimeError`, including the target MI, achieved path range, interaction,
shape, skewness, and error message. A failed construction is not silently
replaced by a different population.

No minimum expected-count filter is applied. Population probabilities need
only be finite, nonnegative, sum to one, and remain numerically usable by the
constructor. A fixed cutoff such as $p_{ij}>10^{-12}$ must not be used to
select easier populations.

The existing per-replicate `variance > 1e-14` numerical guard remains part of
the method's validity definition. It prevents ratios of floating-point noise
near degenerate first-order variance. It is recorded through the validity rate,
not used to remove a population from the design.

---

## 8. Outcomes and denominators

### 8.1 Primary operational rejection rate

The primary rate is unconditional:

\[
\widehat R_{\mathrm{uncond}}
=\frac{\text{valid rejections}}{\text{all simulated replicates}}.
\]

An invalid result counts as a non-rejection. This measures how the method
operates when applied without replacing failed results by another procedure.

At $e=0$, this is the operational false-positive rate. At $e>0$, it is the
operational detection power.

### 8.2 Validity diagnostics

Also report:

\[
\widehat v
=\frac{\text{valid replicates}}{\text{all replicates}},
\]

\[
\widehat R_{\mathrm{cond}}
=\frac{\text{rejections}}{\text{replicates valid for that method}},
\]

and

\[
\widehat R_{\mathrm{common}}
=\frac{\text{rejections on common-valid replicates}}
       {\text{replicates valid for all three methods}}.
\]

Conditional rates may use different replicate subsets for different methods.
Common-valid rates condition on a potentially easier subset. They are therefore
diagnostics, not replacements for the primary unconditional rate.

### 8.3 Calibration

For $e=0$, report for every method and $\alpha$:

- false-positive rate under all three denominators;
- absolute calibration error
  ( |\widehat{\mathrm{FPR}}-\alpha| );
- Wilson 95% interval;
- Monte Carlo standard error; and
- valid rate.

At 10,000 replicates, the approximate Monte Carlo standard error is 0.00218
when the true rate is 0.05 and 0.00100 when it is 0.01.

### 8.4 Detection power

For $e>0$, power is the fraction of simulated alternatives rejected. Report
the three denominators, Wilson interval, Monte Carlo standard error, and valid
rate.

Power must be interpreted together with the $e=0$ false-positive rate. A
method that rejects more alternatives because it is already too liberal under
the null is not considered more accurate. Size-adjusted power is not included
in this experiment.

### 8.5 Paired method comparisons

All methods see the same simulated table pairs. For each configuration, record
the numbers of replicates on which:

- both methods reject;
- neither method rejects;
- only method A rejects; and
- only method B rejects.

These discordant counts support paired rejection-rate differences and McNemar
comparisons without storing replicate-level tables.

For the primary contrast, also report the paired difference in rejection rate
between Expanded Welch and Normal Wald with a 95% confidence interval. Under
the null, interpret this difference together with both methods' distances from
0.05; a lower rejection rate is an improvement only when it moves the method
toward the nominal level rather than farther below it.

---

## 9. Breakdown diagnostics

For Expanded Welch, save the following on valid replicates:

- component degrees of freedom for $P$ and $Q$;
- combined degrees of freedom;
- median, 5th percentile, and 95th percentile of each;
- fraction below 1; and
- fraction above $10^4$.

These thresholds are descriptive flags only:

- small degrees of freedom produce a very heavy-tailed Student reference and
  can make rejection difficult;
- very large degrees of freedom make the Student reference close to normal.

Neither event is automatically a mathematical failure. It becomes evidence of
breakdown only when accompanied by poor validity, calibration, or power.

For every method, also save:

- minimum true expected cell count, separately for $P$ and $Q$;
- fractions of true expected cell counts below 1 and below 5;
- mean observed zero-cell fraction;
- probability of at least one empty row;
- probability of at least one empty column; and
- reasons for invalid results where available.

Here the expected count in cell $(i,j)$ is $n_Pp_{ij}$ or $n_Qq_{ij}$.
It is not the expected count obtained after fitting an independence model.

---

## 10. Descriptive operating frontiers

The primary frontier uses $\alpha=0.05$. For each method and exact population
construction, report the first tested sample size at which a criterion holds
at that size and the next two tested sample sizes. Validity, calibration, and
operational frontiers use the 18-point calibration grid; the detection
frontier uses the eight-point power grid:

1. **Validity frontier:** valid rate at least 0.90.
2. **Calibration frontier:** unconditional FPR lies within Bradley's liberal
   interval ([0.025,0.075]).
3. **Operational frontier:** both validity and calibration criteria hold.
4. **Detection frontier:** the operational criterion holds and unconditional
   power at $e=0.60$ is at least 0.50.

If no such run of three sample sizes exists, record `not_reached`. Requiring
three consecutive grid points makes the descriptive frontier less sensitive to
one Monte Carlo fluctuation. The complete per-sample results remain primary;
the frontier is only a compact summary.

Degrees-of-freedom thresholds are not included in these pass/fail rules.

Bradley's interval is a broad descriptive adequacy rule, not evidence that two
methods are equivalent. Exact FPR, absolute error, and confidence intervals
must remain visible.

---

## 11. Outputs

### 11.1 Data files

- `population_definitions.csv`: margins, interactions, entropy upper bound,
  $M_P$, $M_Q$, shared reachable $M$, target MI, achieved MI, absolute MI
  difference, and $L^1$ distance.
- `cell_results.csv`: one row per exact configuration, method, and alpha,
  containing all rejection rates, intervals, validity, sparsity, and
  degrees-of-freedom diagnostics.
- `paired_method_results.csv`: paired discordant rejection counts and
  rejection-rate differences.
- `breakdown_frontier.csv`: the four descriptive frontiers from Section 10.
- `infeasible_configurations.csv`: every failed population construction and
  its reason.
- `run_metadata.json`: profile, master seed, replicate counts, dependency
  versions, start and end times, worker count, and SHA-256 hash of the script.

No raw contingency-table file is required.

### 11.2 Main-text figures

The main thesis figures follow the order of the experimental questions:

1. **Control plot:** FPR against sample size for the strong and weak balanced
   null controls.
2. **Breakdown plot:** FPR at $\alpha=0.05$ against sample size, faceted by
   shape and skewness, with a horizontal line at 0.05 and Wilson intervals.
3. **Validity heatmap:** sample size against alphabet shape, separately by
   skewness and method.
4. **Power curves:** absolute MI difference against unconditional power, with
   all three methods on the same axes and the corresponding null rejection
   rate shown at $\Delta_I=0$.
5. **Operating-frontier plot:** minimum sustained usable sample size against
   table shape, with exact skewness labels.
6. **Robustness plot:** paired Expanded-Welch-minus-Wald calibration and power
   differences for the named interaction and sample-imbalance cases.

To keep the main chapter readable, the fixed core panel uses shapes `2x2`,
`3x3`, `3x5`, `5x5`, and `8x8`, and skewness levels balanced, strong, and
ultra. This panel is chosen before the full run. Mild-skewness results,
additional rectangular shapes, secondary significance levels, calibration
curves over the full alpha range, and degrees-of-freedom diagnostics appear in
the appendix. All exact cells remain in the CSV outputs.

Plots covering very small $n$ must visually distinguish
$n<\max(r,c)$. Comparable panels use shared axes; if a separate scale is
necessary, it must be labelled prominently. Every figure must identify the
exact result rows from which it was produced.

`REPORT.md` presents controls first, calibration and breakdown second, power
third, and robustness last. Configuration-level evidence precedes aggregate
win/tie/loss summaries.

---

## 12. Verification

### 12.1 Unit tests

Add tests for:

1. entropy upper-bound calculation;
2. stable reachable-range calculation and monotonicity checking;
3. all target MIs lying at or below (0.8M);
4. achieved target MI within $10^{-10}$;
5. identical-distribution $e=0$ producing $P=Q$;
6. different-shape $e=0$ producing equal MI but nonidentical tables;
7. balanced margins remaining distinguishable through the interaction change;
8. all three rejection-rate denominators;
9. paired discordant-count accumulation;
10. sustained-frontier logic;
11. stable per-configuration seeds;
12. both `ValueError` and `RuntimeError` construction failures; and
13. square and rectangular table shapes;
14. exact generation of all 5,672 protocol cells without duplicates; and
15. separation of calibration and power sample-size grids.

Run the complete project suite after adding these tests.

### 12.2 Smoke profile

Before the full run, use:

- shapes `2x2` and `3x5`;
- balanced and ultra skewness;
- (n\in\{2,5,20,100});
- (e\in\{0,0.10,0.60});
- both population relationships; and
- 200 replicates.

The smoke run must create every output file and figure without changing the
primary result directory.

### 12.3 Numerical checks

The full run must verify:

- achieved population MI differs from its target by at most $10^{-10}$;
- all p-values marked valid are finite and lie in $[0,1]$;
- unconditional rejection count never exceeds valid count;
- conditional, unconditional, and common-valid rates agree whenever all three
  methods have valid rate 1;
- $n=2$ reproduces zero Expanded-Welch validity;
- row/column relabeling and swapping $(P,Q)$ do not change two-sided p-values
  beyond numerical tolerance; and
- power reversals larger than three combined Monte Carlo standard errors are
  flagged for investigation rather than automatically treated as code errors.

The old `2x2` anchor should be rerun separately with its original population,
sample size, and effect definitions. That is a regression check against the
existing result, not an expected exact match to a newly normalized sweep cell.

---

## 13. Execution sequence

1. Resolve and archive or commit the preliminary result state.
2. Implement population preflight and generate the complete configuration
   manifest.
3. Resolve construction failures without examining simulated method outcomes.
4. Implement the runner, figures, and tests; then complete the smoke profile.
5. Discard smoke outcomes and freeze the protocol, implementation, tests,
   configuration manifest, and master seed in one commit.
6. Run Experiments 1-3 and both predeclared robustness blocks without changing
   the protocol between blocks.
7. Run all numerical and completeness checks before interpreting results.
8. Generate the final report, main figures, and appendix figures only from the
   saved aggregate CSV files.
9. Record every deviation, failed cell, or rerun and its reason in the final
   report.

The full-run runtime must be estimated from the smoke profile. The previous
two-to-four-minute estimate is not treated as guaranteed because computation
depends on table shape, validity, batching, and output generation.

---

## 14. Interpretation rules

The experiment is intended to characterize, not force, a positive result.

- Expanded Welch is better calibrated in a configuration only when its
  absolute FPR error is smaller than Wald's on the same population and its
  validity remains acceptable.
- Greater raw power is beneficial only when the method also has acceptable
  null calibration.
- A low unconditional rejection rate accompanied by a low valid rate is an
  operational failure, not evidence of conservatism alone.
- A very small or very large effective degrees of freedom is explanatory
  evidence, not a failure by itself.
- Conclusions about interaction structure must come from the named robustness
  configurations, not from averaging unlike populations.
- Failure at extremely small $n$ is a useful boundary result. It should not
  be generalized to ordinary sample sizes without examining the operating
  frontier.

This design will support a clear conclusion about where Expanded Welch helps,
where it behaves like Wald, and where its validity or finite-sample reference
breaks down.

---

## 15. Scope and threats to validity

The final thesis interpretation must state the following limits:

- **Statistical scope:** the study concerns positive-MI comparisons under the
  weak null $I(P)=I(Q)$, not testing independence at $I=0$.
- **Sampling model:** observations are independent and identically distributed
  multinomial draws. Temporal dependence, clustering, and measurement error
  are outside the design.
- **Population coverage:** one-dominant margins and a finite set of interaction
  paths provide controlled stress tests, but they do not represent every joint
  distribution.
- **Finite grid:** operating frontiers are defined only over the tested sample
  sizes and should not be interpreted as exact universal thresholds.
- **Monte Carlo precision:** differences smaller than their paired simulation
  uncertainty are treated as practically unresolved.
- **External demonstration:** an applied example may illustrate use of the
  method, but it cannot establish calibration because the true population MI
  values are unknown.
