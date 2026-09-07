# Thesis Experiment Redesign: Wald and Expanded Welch

**Status: completed.** Protocol version 1.0.0 was frozen after successful
preflight and smoke testing. The full run, verification, runtime study and
standardized report are complete. The executable protocol and manifest
implement the design below; earlier studies are not observations from this run.

## 1. Purpose and reading order

The question is: **when does Expanded Welch's reduction in false positives
justify its loss of detection power, compared with Normal Wald?** We are not
trying to select populations that make either method win.

Both methods test whether two independently sampled populations have the same
mutual information (MI):

\[
H_0:I(P)=I(Q),\qquad H_1:I(P)\ne I(Q).
\]

The redesigned study has three layers:

1. **Main comparison:** change table size, marginal probabilities and sample
   size using one simple population construction.
2. **Focused comparisons:** change baseline MI, where cell probabilities are
   modified, sample allocation, or construction, while matching the other
   settings wherever the comparison permits.
3. **Limits and practicality:** deliberately sparse and independence cases,
   large-sample behaviour, and computation time.

Each power curve includes its own zero-difference point. That point measures
false-positive rate; positive differences measure power. There will not be a
separate, differently populated null experiment that cannot be matched to the
power experiment. Large-sample null diagnostics are the explicit exception.

The previous [combined results](archive/EXPERIMENTAL_RESULTS.md) remain a
historical record. The separate [construction check](CONSTRUCTION_CHECK.md)
motivates this redesign: explicit additive tables retained both the benefits
and costs of Expanded Welch, while larger-table performance could change with
construction even at matched MI and margins. These findings motivate checks;
they do not predetermine the new conclusions.

## 2. What changes and what stays fixed

| Decision | Redesigned study |
| --- | --- |
| Main population construction | An independence table plus specified additions and subtractions in cells |
| Main effect definition | Actual population MI difference in nats, fixed before sampling |
| Construction-dependent maximum M | Removed from target selection and graph labels; feasibility bounds remain internal construction diagnostics |
| Methods | Normal Wald and Expanded Welch, using the existing definitions and identical sampled inputs |
| Significance level | Two-sided alpha = 0.05, stated once in the report introduction |
| Population selection | Explicit deterministic settings, not random draws followed by acceptance filtering |
| Reporting unit | One exact population-pair/sample-size regime per graph panel; no averaging across regimes |
| Failure handling | Retain every sampled pair; report failures as well as rejection rates |
| Additional calibration methods | No LR, oracle thresholds, size-adjusted power, or fitted correction in this study |

The existing bias correction, variance estimator, Expanded Welch degrees of
freedom and invalidity rules must be inspected and recorded before reuse.
Do not change them to accommodate difficult configurations. A discovered bug
requires a documented correction, fresh tests and a new protocol version.

## 3. Constructing the probability tables

### 3.1 Margins: the row and column probabilities

For a marginal distribution with k categories, define

\[
u_k=(1/k,\ldots,1/k),\qquad
m_k(d)=\left(d,\frac{1-d}{k-1},\ldots,\frac{1-d}{k-1}\right).
\]

For an r by c table, use the stated r-category vector for row probabilities
and the stated c-category vector for column probabilities.

| Profile | P row / column probabilities | Q row / column probabilities | Role |
| --- | --- | --- | --- |
| Uniform | u_r / u_c | u_r / u_c | Simple balanced control |
| Same skew | m_r(0.8) / m_c(0.8) | m_r(0.8) / m_c(0.8) | Skewed control with matching margins |
| Different skew | m_r(0.7) / m_c(0.7) | m_r(0.8) / m_c(0.8) | Equal-MI nulls with genuinely different margins |

At the null, matching margins and matching construction give P=Q. These are
useful controls, not evidence that two distinct distributions have been tested.
The different-skew profile supplies that comparison without category relabelling.

In the results document, expand these formulas into the actual numerical vectors
under each figure. Do not make readers look up u or m in another subsection.

### 3.2 Explicit changes to four cells

For either population, let a and b be its chosen row and column probabilities.
Start with independence, B_ij=a_i b_j, and set

\[
R_{ij}(t)=a_i b_j+tH_{ij},\qquad t\geq 0.
\]

The main construction uses

\[
H_{11}=H_{22}=1,\qquad H_{12}=H_{21}=-1,
\]

with every other entry zero. Increasing t adds probability to cells (1,1)
and (2,2), and removes the same amount from (1,2) and (2,1). Every row and
column sum of H is zero, so the margins do not change. The population table
is already normalized: no proportional fitting is needed.

For example, with both margins (0.7,0.3),

\[
R(t)=
\begin{pmatrix}
0.49+t&0.21-t\\
0.21-t&0.09+t
\end{pmatrix}.
\]

Choose t separately for P and Q to obtain the required MI. Their t values
need not match because their margins may differ. The implementation must add
one worked numerical P,Q example with achieved MI and row/column sums to the
results introduction, calculated from saved populations rather than hand-rounded inputs.

This four-cell construction is adapted from the benchmark identified in the
[construction check](CONSTRUCTION_CHECK.md). Matching two positive MI values
is our extension; an independence-testing benchmark does not itself validate
the null distribution of a two-population equal-MI test.

### 3.3 Feasibility and target matching

The nonnegative interval has endpoint

\[
t_{\max}=\min_{H_{ij}<0}\frac{a_i b_j}{-H_{ij}}.
\]

Compute the endpoint MI using the convention 0 log 0 = 0. This is the endpoint
of this specified family, not the maximum MI over all possible tables with
those margins. Main-study populations must use t strictly below this endpoint.
There is no arbitrary 0.95 endpoint multiplier and no expected-count filter.

MI along this positive branch starts at zero and increases. A useful validation
identity, while probabilities are positive, is

\[
\frac{d^2 I(R(t))}{dt^2}=\sum_{i,j}\frac{H_{ij}^2}{R_{ij}(t)}>0,
\qquad I'(R(0))=0.
\]

Use a bracketed one-dimensional solve for each target. Validate the derivative
and MI implementation independently; do not rely only on this description.
Accept MI error at most 1e-12 + 1e-8 times the target, and marginal and
normalization errors at most 1e-12. Tiny targets need cancellation-safe
evaluation, not rounding negative probabilities to zero or adding pseudocounts.

Before sampling, enumerate and validate every requested population. A target
outside a family's range is **infeasible**, not an invalid test replicate.
Record it explicitly. Do not lower its target, rescale its effect, choose a
different population, or silently drop the regime. The intended grids below
must pass preflight; otherwise revise and explain the design before freezing it.
A numerical fitting failure for a feasible target is a software problem to resolve.

### 3.4 Fixed populations, then random samples

For the main direction, choose baseline MI B and difference Delta:

\[
I(P)=B,\qquad I(Q)=B+\Delta.
\]

Hold these probability tables fixed and independently draw

\[
N^{(P)}\sim\operatorname{Multinomial}(n_P,P),\qquad
N^{(Q)}\sim\operatorname{Multinomial}(n_Q,Q).
\]

The x-axis is Delta, set by construction. Sampling changes the estimated MI
and variance, not the true MI difference. Both methods receive the same two
count tables in every replicate. Different population definitions are never
averaged into one point.

## 4. Main comparison

**Question:** how do the two methods behave as alphabet size, skew and sample
size change, for the same baseline MI and the same actual MI differences?

| Factor | Exact settings |
| --- | --- |
| Square table sizes | 2x2, 3x3, 5x5, 8x8 |
| Margins | Uniform, same skew, different skew, defined in Section 3.1 |
| Cell changes in both populations | Main four-cell block in rows 1,2 and columns 1,2 |
| Baseline MI | B=0.02 nats |
| Actual MI differences | Delta={0,0.001,0.002,0.005,0.01,0.02} nats |
| Equal sample sizes | n_P=n_Q in {2,5,10,20,50,100,250,500,1000} |

This is 648 configurations before any reuse by later sections. Every one has
both methods; no minimum expected count is imposed. There is no separate
"well sampled" selection based on realized or expected counts.

Create a separate figure set for each alphabet size. Rows are the three
margin profiles, in the same order throughout. Columns are sample sizes.
Split nine columns into consecutive groups {2,5,10}, {20,50,100}, and
{250,500,1000}, giving readable 3x3-panel figures. Each panel is one exact regime.

Use linear x limits 0 to 0.02 nats and y limits 0 to 1 throughout this section.
Keeping actual differences matched makes the comparison direct; the chosen
range is not a claim to cover every possible MI difference.

## 5. Focused comparisons

These are prespecified additions, not cases chosen after inspecting rejection
rates. Reuse identical configurations rather than simulating them again.

### 5.1 Baseline dependence

**Question:** does the comparison change when the starting MI is closer to zero?

Use all four square sizes and all three profiles, the main four-cell block,
baseline B={0.0001,0.001,0.02}, equal n={20,100,1000}, and the entire main
Delta grid. Rows are baseline MI and columns are n, separately for each
size/profile. Margins, sample sizes and absolute differences match across rows.
Use the main axes. B=0.02 points are reused from Section 4.

These are positive-MI cases, not independence nulls. Their small baseline
does not guarantee an accurate first-order approximation at these sample sizes.

### 5.2 Where the probabilities change

**Question:** does performance depend on concentrating the changes in common
cells, rare cells, or spreading them over the table?

Use sizes 3x3, 5x5 and 8x8, the different-skew profile, B=0.0001,
equal n={20,100,1000}, and Delta={0,0.0001,0.00025,0.0005,0.001,0.002}.
The smaller fixed grid allows the rare-cell populations to be matched without
redefining the effect separately for each construction.

| Pattern | Exact H for both populations |
| --- | --- |
| First block | The main four-cell block in rows 1,2 and columns 1,2 |
| Rare block | The same signs in the last two rows and last two columns |
| Spread | H_ij=s_i s_j, with s_i=-1+2(i-1)/(k-1) for a k by k table |

Use all three patterns for 5x5 and 8x8. For 3x3, use only the first and rare
blocks: the spread construction is a relabelling of the first block under
these margins. Likewise, do not inflate the design with three duplicate 2x2
patterns or treat uniform first/last blocks as different rarity regimes.

Rows are patterns, columns are n, separately for each size. Use x limits
0 to 0.002 and y limits 0 to 1. The pattern changes can alter individual cell
probabilities and sparsity even at matched MI; report those quantities rather
than describing this as an isolated causal effect of cell location.

### 5.3 Unequal samples and which population has greater MI

**Question:** does the result depend on which population receives more data
or which population has greater dependence?

Use all four square sizes, all three profiles, the main block, B=0.02 and
the main Delta grid. Use sample pairs
{(50,50),(50,100),(100,50),(50,250),(250,50),(50,500),(500,50),(500,500)}.
Construct both directions: (I(P),I(Q))=(B,B+Delta) and (B+Delta,B).

Keep P's margins attached to P and Q's to Q. Changing sample allocation is
not the same as swapping the entire populations. Reuse the common null at
Delta=0. For identical margins, use exact exchange-symmetry checks to identify
equivalent configurations; do not present duplicated evidence as independent.

For each size/profile, show the two MI directions as rows and matched
allocations as columns, split into readable groups of at most four columns.
Use the main axes. Include the two equal-sample controls with the same format.

### 5.4 Larger effects and rectangular tables

**Question:** are the main curves merely too short, or specific to square tables?

For larger effects use 2x2 and 3x3, all three profiles, the main block,
B=0.02, equal n={20,100,1000}, and
Delta={0,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2}.
Use x limits 0 to 0.2 for every panel in this explicitly labelled broad-effect
section; reuse all matching earlier points. Do not stretch larger-table
families beyond their feasible range to make lines reach the same endpoint.

For rectangular tables use 2x3 and 3x5, all three profiles, the main block,
B=0.02, equal n={20,100,1000}, and the main Delta grid and axes. For each
dimension, construct its margins using Section 3.1. These are separate
generalisability checks, not additional observations to average with square tables.

### 5.5 Alternative construction

**Question:** do the conclusions depend on using additive cell changes?

Use 3x3, 5x5 and 8x8; uniform and different-skew profiles; B={0.0001,0.02};
equal n={20,100,1000}; and the main Delta grid. Compare the main additive
block with an ordinal log-linear table having the same margins and target MI.
Define ordinal scores s_i=-1+2(i-1)/(r-1), z_j=-1+2(j-1)/(c-1), and use

\[
R_{ij}(\lambda)=A_i B_j a_i b_j\exp(\lambda s_i z_j),\qquad\lambda\geq0,
\]

where positive row/column multipliers enforce the chosen margins. Solve for
lambda to match MI. Use numerically stable fitting and explicit convergence
checks; do not define targets from the first failed numerical probe.

Show the two constructors as rows, n as columns, separately for each
size/profile/baseline. Use the main axes. Save exact tables, fitting residuals
and population variances for both constructors. This is a matched alternative
family check, not a claim that the two constructors sample all possible tables.
Reconstruct 2x2 examples by the independent one-parameter formula as a unit
test, not as another supposedly independent family comparison.

## 6. Limits and computation

### 6.1 Extreme skew and very small samples

Use 2x2, 3x3 and 8x8 with the main block and dominant marginal pairs
(d_P,d_Q)={(0.9,0.95),(0.99,0.995),(0.999,0.9995)}. Apply each d to both
row and column margins. Set B=0.00001 and
Delta={0,0.00001,0.00005,0.0001,0.0002}; equal n={1,2,5,20,100,1000,10000}.
Rows are marginal pairs, columns are n; split columns into readable groups.
Use x limits 0 to 0.0002 and y limits 0 to 1.

Add a rare-block check for 3x3 and 8x8 with (d_P,d_Q)=(0.9,0.95),
B=0.00001, Delta={0,0.00001,0.000025,0.00005,0.0001}, and the same n grid.
Use x limits 0 to 0.0001. Compare it to the main block at these exact targets
and margins, adding missing main-block points rather than interpolating.

n=1 is a defined failure-boundary diagnostic, not a promise that either test
can operate. Preserve zero observed cells, empty margins, tiny population
probabilities and all invalid outcomes. No expected-count floor or sample-size
rescue is allowed. This remains a finite tested range, not "all skewness" or
"no lower bound whatsoever". Report the actual smallest probabilities and counts.

### 6.2 Exact independence boundary

Use 2x2 and 8x8, uniform and different-skew margins, the main block, B=0,
equal n={2,20,100,1000}, and the main Delta grid. Show complete curves with
the main axes. At Delta=0 both populations are independent and the usual
positive first-order MI-variance condition fails. Label this a boundary
diagnostic; a finite plug-in variance does not restore that population condition.
Do not silently classify these as regular positive-MI nulls or substitute a G test.

### 6.3 Large-sample null behaviour

Use all four square sizes, all three profiles, the main block,
B={0.0001,0.02}, Delta=0, and equal
n={1000,2500,10000,50000}. Reuse existing n=1000 points.
Keep each population pair fixed as n grows. Also include the different-skew
rare-block nulls from Section 5.2 at these n values.

Here x is sample size on a log scale, not MI difference. Use identical limits
and ticks across panels, a main y range 0 to 1, and a companion calibration
zoom from 0 to 0.1 with off-scale points flagged. Report every value. Reaching
50,000 does not prove convergence; persistent discrepancies require diagnosis.

### 6.4 Runtime

Time the complete public test call on already constructed count tables,
separately from population construction, simulation and plotting. Include
2x2, 3x3, 5x5, 8x8 and 3x5; uniform and different-skew profiles;
n={20,100,1000}; B=0.02; Delta={0,0.02}; and the main block.

For each exact regime, generate 200 independent input pairs from a separate
timing stream and use the identical inputs for both methods. Warm up with 20
calls per method; then time five passes over the 200 inputs, alternating
method order between passes. Take the median time per input across passes,
then report the median, interquartile range and paired runtime ratio across
the 200 inputs, with validity rates. Time
invalid returns too, but separate valid and invalid timings in supporting data.
Record hardware and package versions once. Do not compare vectorized Wald
against scalar Welch or include fitting costs for only one method.

## 7. Simulation and performance records

Use 20,000 independent table pairs per unique configuration, in bounded
batches. Near rejection probability 0.05 this gives Monte Carlo standard error
about 0.00154; near 0.5, about 0.00354. This is simulation uncertainty, not
uncertainty about the actual populations. Use 95% Wilson intervals for each rate.

| Record | Definition / reporting rule |
| --- | --- |
| Rejection rate over all pairs | Rejections divided by 20,000; invalid results count as non-rejections for this operational metric |
| False-positive rate | That rate at Delta=0; target 0.05 |
| Power | That rate at Delta>0; probability of detecting a true MI difference |
| Valid rate | Valid test outputs divided by all pairs |
| Conditional rejection | Rejections divided by valid outputs; undefined if none are valid |
| Common-valid comparison | Both methods evaluated on the subset where both return valid outputs; supporting diagnostic only |
| Paired difference | Difference of rejection indicators on the same samples; retain discordant counts and its paired Monte Carlo standard error |
| Population sparsity | Minimum n_P p_ij and n_Q q_ij separately, and fractions of cells with expected count below 1 and below 5 |
| Sample sparsity | Frequencies of observed zero cells, empty rows and empty columns |
| Invalidity | Counts by explicit reason, including variance and degrees-of-freedom failures |
| Other diagnostics | Population first-order MI variance, estimated standard-error summaries, Expanded Welch degrees-of-freedom summaries |

"Minimum expected count" means the minimum of the population expected cell
counts, not the expectation of the smallest observed cell count. Include this
one-sentence footnote wherever that table heading first appears.

Use stable configuration-specific streams, independent across distinct
configurations, and shared sampled inputs across methods. Reuse saved outputs
for identical configurations appearing in multiple sections. Define identity
from full-precision populations, sample sizes and method/protocol version,
not a section label or rounded display values. Store stream keys and hashes
in machine-readable provenance rather than repeated report tables.

Report the paired Monte Carlo uncertainty of method differences. Pointwise
intervals are not simultaneous guarantees across the landscape. Do not
declare a winner by counting how many intervals happen to cross 0.05.
No result-driven replication stopping or selective extra sampling is planned.

## 8. Standardized results document

Create one new main report, `docs/experiments/THESIS_EXPERIMENTS.md`.
Begin with a short roadmap, how to read the curves, definitions, and the
worked population construction. Follow Sections 4, 5 and 6 of this plan in
order. Put reproducibility details last. Keep the separate historical
construction check outside this main narrative.

Every figure subsection must follow exactly this sequence:

1. A descriptive title naming size and the comparison, not a claimed winner.
2. One sentence stating the question.
3. The graph, including every prescribed regime and both methods.
4. A self-contained specification table using the schema below.
5. A compact table of every null-point rejection rate and valid rate.
6. An expandable table of every plotted point: Delta, method, rejection,
   interval, valid rate, conditional rejection and minimum expected counts.
7. At most two factual interpretation sentences, written only after results exist.

| Specification row | Required contents |
| --- | --- |
| Table size | Exact row and column counts |
| Horizontal graph regime specifications (columns) | Complete ordered list of sample pairs or other column settings |
| Vertical graph regime specifications (rows) | Complete ordered settings; actual row and column probability vectors for P and Q in each row |
| Probability changes | Explicit affected cells and signs, or the full rule for the spread/log-linear case, for both P and Q |
| MI settings | Actual baseline(s), which population has the higher MI, and the full actual Delta grid |
| Horizontal axis within each graph | Quantity, units, fixed limits and ticks |
| Vertical axis within each graph | Rejection rate, fixed limits 0 to 1, and all-pairs denominator |
| Replicates | 20,000 per unique point |

Do not include repeated "Methods" or "Test and significance level" rows.
Do not repeat "equal MI at the first point" in each table: explain it once
at the start. Do not refer readers to previous subsection tables for settings.
For large probability vectors, exact repetition notation such as
(0.8, 0.2/7 repeated 7 times) is acceptable and clearer than rounded entries
that no longer sum to one.

Graph rules:

- Wald: blue solid line with circles. Expanded Welch: magenta dashed line
  with squares. Use one consistent legend and z-order; overlapping curves must
  be identifiable from the markers and accompanying numbers.
- Shade pointwise intervals lightly and show the horizontal 0.05 reference.
- Use linear actual-MI axes, not a regime-specific maximum or log axis that
  cannot include zero. Different effect windows are separate labelled sections;
  axes are identical within every declared comparison. Do not secretly autoscale.
- Display all x tick labels, including upper rows of panel grids. Split wide
  grids rather than shrinking labels until unreadable.
- A hollow marker flags valid rate below 0.9; exact validity is always available.
  An entirely invalid method is visibly labelled, not presented as successful
  zero false positives. Missing or infeasible points are labelled, not connected.
- Never extend a curve horizontally beyond observed points, extrapolate to
  an unattainable MI, or suppress a falling power curve.
- Show probabilities and MI to approximately four significant figures, retain
  simple exact grid values, and use scientific notation for tiny values.
  Report rates and interval endpoints consistently to four decimal places.
- Use plain words before notation. Say "row probabilities", "changes in four
  cells", and "MI difference", rather than unexplained population-path jargon.

Changing from the previous scaled axis is deliberate: this redesign matches
actual MI values across regimes. One universal axis would hide the tiny-effect
stress curves. Separate, explicitly fixed effect windows preserve readability
without implying that differently sized actual effects are the same.

## 9. Implementation sequence and acceptance checks

### Stage A: inspect and implement without sampling

Read the current theory derivation and method implementations. Reuse tested
statistics, not the previous M-based population selection. Useful starting
points are `experiments/run_construction_check.py` and
`experiments/run_detection_breakdown_sweep.py`; inspect their interfaces and
validity rules rather than copying them blindly.

Create a new runner, protocol and results namespace, suggested as
`experiments/run_thesis_redesign.py`, `experiments/THESIS_REDESIGN_PROTOCOL.json`
and `results/thesis_redesign/`. Implement separate preflight, smoke, simulation,
verification, timing and report-only modes with resumable per-configuration
checkpoints. Preserve all historical files and source-result provenance.

Generate the full requested grid, exact population tables and feasibility
report. Enumerate duplicates and the final number of unique configurations,
replicates, method evaluations and figures. Estimate runtime from smoke tests;
do not invent a total before manifest deduplication. Every figure slot must
map to an explicit configuration identifier or an explained infeasibility.

### Stage B: independent checks and smoke tests

- Check normalization, strict positivity, exact margins and target MI for
  every population, including the smallest targets and most extreme margins.
- For 2x2, independently recover the table from its margins and association
  parameter; cross-check MI with a separate direct implementation.
- Check H row/column sums, analytic feasibility bounds, endpoint handling,
  and monotonic MI on the chosen branch. Test infeasible requests explicitly.
- Verify category-permutation invariance and P/Q exchange symmetry with sample
  sizes exchanged, including the expected sign change of the statistic.
- Verify methods receive identical samples, use the same numerator and standard
  error where valid, and Expanded Welch cannot reject when Wald does not on
  common-valid inputs. Investigate any violation before simulation.
- Test zero cells, empty margins, n=1, degenerate variance, nonfinite degrees
  of freedom and exact independence. No warnings may silently discard samples.
- Cross-check a small batched simulation against scalar method calls on the
  identical count tables. Validate rejection counts, denominators and intervals.
- Confirm report-only mode cannot run simulations; resume cannot duplicate or
  overwrite completed configurations from another protocol.
- Smoke every distinct construction/profile/size family, all effect endpoints
  and sample boundaries with 200 pairs, using separate output and random streams.
  Use smoke outcomes to diagnose code, not to choose favourable regimes.
- Render representative figures from smoke outputs, including tiny effects,
  coincident lines and all-invalid panels; inspect labels and table formatting.

### Stage C: freeze, execute and verify

After preflight and smoke pass, freeze the protocol, full manifest, population
definitions, code/dependency hashes and reporting rules. This is a prospective
run after exploratory design work, not a claim that no previous results were
seen. Record any feasibility-driven changes before the freeze.

Run all unique configurations with fresh streams. Report progress as completed
configurations and sampled pairs, not merely "running". Checkpoint results
atomically. Run the separate timing experiment, verify complete coverage and
all invariants, then generate the report from saved outputs.

If checks fail, preserve the failure record and fix the cause. Do not label
the study complete while jobs remain unfinished or replace missing results
with old-study points. Any post-freeze change requires a versioned deviation
and identification of affected outputs.

### Stage D: deliverables and interpretation

Deliver the new report, frozen executable protocol, complete configuration
manifest, full-precision P/Q tables, per-method and paired result files,
timing results, verification record, and reproducible plotting code.
Validate every local link, graph count, specification-to-data match and table.
Keep verbose fitting diagnostics, streams and hardware records in supporting
files, accessible from the final reproducibility section.

Conclusions must distinguish improved false-positive control, excessive
conservatism, loss of power and failure to return a usable result. Higher power
with inflated false positives is not automatically better; lower false
positives caused by invalidity are not successful calibration. Since these
methods share the statistic, Expanded Welch's contribution is a threshold
trade-off, not a source of additional information.

Report the complete landscape before selecting examples. Do not average over
regimes, claim uniform superiority, infer a universal sample-size threshold,
or equate fixed sample size with fixed sparsity across alphabets. The scope
is a transparent, reproducible set of regular and deliberately difficult
categorical populations, not every distribution that could exist.

## 10. Completion record

Preflight produced 4,001 display points, deduplicated to 3,111 unique
configurations and 534 fixed population pairs. All population targets were
feasible. The independent smoke run covered 449 boundary configurations and
89,800 sampled pairs before the protocol was frozen.

The full run completed 62.22 million independently sampled table pairs and
124.44 million method evaluations. All simulation and report checks passed.
The final output contains 99 primary figures, seven companion calibration
zooms, exact result tables, paired comparisons, runtime measurements and
full-precision population definitions. Start with the
[reader-facing results](THESIS_EXPERIMENTS.md); machine-readable records are
under [`../../results/thesis_redesign/`](../../results/thesis_redesign/).
