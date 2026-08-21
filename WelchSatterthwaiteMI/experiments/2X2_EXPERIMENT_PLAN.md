# Expanded Welch-Satterthwaite: 2x2 Experiment Plan and Record

## 1. Purpose

This document defines and records the next experimental phase for the
Expanded Welch-Satterthwaite differential mutual information test. The
research question is

$$
H_0:I(P)=I(Q),
$$

where $P$ and $Q$ are two joint distributions sampled independently. The
experiment asks when Expanded Welch improves finite-sample inference over the
Normal Wald and Simple Welch references, and where it ceases to work.

The first phase uses only $2\times2$ tables. Their mutual-information model has

$$
d=(2-1)(2-1)=1
$$

association degree of freedom, so the population distributions can be
specified exactly and interpreted without averaging over random table shapes.
Here $d=1$ also makes the leading MI bias correction $1/(2n)$. It does **not**
force the final Student reference to have one degree of freedom; the
Welch-Satterthwaite degrees of freedom remain estimated from the two variance
components.

The plan directly implements the supervisor's three requests:

1. remove every expected-count floor and retain difficult samples;
2. examine fixed, interpretable subcases until the method breaks down; and
3. vary the true MI difference and sample size to measure detection power at a
   fixed significance level.

## 2. Methods Compared

Every simulated pair of count tables is analysed by the same three methods:

| Method | Reference distribution for the shared statistic $T$ |
| --- | --- |
| Normal Wald | Standard normal |
| Simple Welch-Satterthwaite | Student with ordinary $n_P-1$ and $n_Q-1$ component degrees of freedom |
| Expanded Welch-Satterthwaite | Student with MI-specific variance-influence component degrees of freedom |

All methods use the same bias-corrected MI difference,

$$
\widehat\Delta_{\mathrm{BC}}
=
\left\{\widehat I(P)-\frac{1}{2n_P}\right\}
-
\left\{\widehat I(Q)-\frac{1}{2n_Q}\right\},
$$

the same estimated standard error,

$$
\widehat{\operatorname{SE}}^2
=
\frac{\widehat V(P)}{n_P}
+
\frac{\widehat V(Q)}{n_Q},
$$

and therefore the same statistic

$$
T=\frac{\widehat\Delta_{\mathrm{BC}}}
        {\widehat{\operatorname{SE}}}.
$$

Only the reference distribution used to convert $T$ into a p-value changes.
This makes the experiment a direct test of the finite-degrees-of-freedom
correction rather than a comparison of different MI estimators.

Repeated sampling from known $P$ and $Q$ supplies the accuracy reference. An
ordinary label-permutation test is not used because $I(P)=I(Q)$ does not imply
$P=Q$; exchangeability need not hold under this weak null.

### 2.1 Decision outcomes

The simulation knows whether $H_0$ is true, so each valid test decision falls
into one of four categories:

| Population truth | Test rejects $H_0$ | Test does not reject $H_0$ |
| --- | --- | --- |
| $I(P)=I(Q)$ | False positive | True negative |
| $I(P)\ne I(Q)$ | True positive | False negative |

The corresponding rates are

$$
\operatorname{FPR}
=\frac{\mathrm{FP}}{\mathrm{FP}+\mathrm{TN}},
\qquad
\operatorname{TNR}
=\frac{\mathrm{TN}}{\mathrm{FP}+\mathrm{TN}}
=1-\operatorname{FPR},
$$

and

$$
\operatorname{TPR}
=\frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}
=\text{power},
\qquad
\operatorname{FNR}
=\frac{\mathrm{FN}}{\mathrm{TP}+\mathrm{FN}}
=1-\text{power}.
$$

At significance level $\alpha=0.05$, a calibrated method should have an FPR
near 0.05 and a true-negative rate near 0.95 when the null is true. When the
null is false, a useful method should have a high true-positive rate and a low
false-negative rate. Rejecting a false null is therefore a true positive, not
a true negative.

## 3. Deterministic 2x2 Populations

### 3.1 Parameterization

Let

$$
u=\Pr(X=1),
\qquad
v=\Pr(Y=1),
$$

and let $\delta$ control their association. The population table is

$$
P(u,v,\delta)
=
\begin{pmatrix}
(1-u)(1-v)+\delta & (1-u)v-\delta\\
u(1-v)-\delta & uv+\delta
\end{pmatrix}.
$$

The row and column margins are fixed by $u$ and $v$. Independence occurs at
$\delta=0$. Positive $\delta$ increases the two diagonal cells, while negative
$\delta$ increases the off-diagonal cells. Valid cell probabilities require

$$
-\min\{uv,(1-u)(1-v)\}
<\delta<
\min\{(1-u)v,u(1-v)\}.
$$

For any table $R=(r_{ij})$, its population MI is

$$
I(R)=\sum_{i,j}r_{ij}
\log\!\left(\frac{r_{ij}}{r_{i+}r_{+j}}\right).
$$

Given $(u,v)$, an association direction, and a target $I_0$, a one-dimensional
root solver chooses $\delta$ so that

$$
I\{P(u,v,\delta)\}=I_0.
$$

The root is solved on one side of independence and kept inside the valid
probability interval. Population generation is deterministic: no Dirichlet
margins or random interaction patterns are used in this phase.

### 3.2 Fixed equal-MI null cases

The initial null cases are listed below. A plus or minus sign specifies the
association branch used when solving for $\delta$. The final column is the
approximate smallest population cell probability across $P$ and $Q$; the
actual generated probabilities will be saved at full precision.

| ID | Purpose | Margins $(u_P,v_P)$ | Margins $(u_Q,v_Q)$ | Directions $(P,Q)$ | $I(P)=I(Q)$ | Smallest cell probability |
| --- | --- | --- | --- | --- | ---: | ---: |
| N0 | Identical-population control | $(0.50,0.50)$ | $(0.50,0.50)$ | $(+,+)$ | 0.1000 | 0.14010 |
| N1 | Same margins, different association pattern | $(0.50,0.50)$ | $(0.50,0.50)$ | $(+,-)$ | 0.1000 | 0.14010 |
| N2 | Mild margin mismatch | $(0.50,0.50)$ | $(0.30,0.40)$ | $(+,+)$ | 0.1000 | 0.08000 |
| N3 | One skewed population | $(0.30,0.40)$ | $(0.10,0.30)$ | $(+,+)$ | 0.0300 | 0.03460 |
| N4 | Two sparse, differently shaped populations | $(0.10,0.10)$ | $(0.05,0.20)$ | $(+,+)$ | 0.0100 | 0.02366 |
| N5 | Extreme rare categories | $(0.02,0.02)$ | $(0.01,0.05)$ | $(+,+)$ | 0.0050 | 0.00349 |
| N6 | Sparse margins and opposite association | $(0.10,0.10)$ | $(0.05,0.20)$ | $(+,-)$ | 0.0050 | 0.00243 |
| N7 | Ultra-rare categories | $(0.005,0.005)$ | $(0.002,0.010)$ | $(+,+)$ | 0.0005 | 0.00028 |

These cases change one major feature at a time: equality of the full
distributions, association direction, marginal mismatch, skewness, and rare
cell probabilities. They are fixed before simulation and are not selected
according to which method performs best.

### 3.3 Unit of analysis and reporting

The unit of analysis is one fully specified configuration:

$$
\mathcal C=(P,Q,n_P,n_Q).
$$

For a power experiment, $\Delta_I$ is also part of the configuration. Two
configurations are distinct if they differ in either population table, either
sample size, association direction, or true MI value.

Results from distinct configurations will not be averaged into a regime-level
performance number. Each configuration receives its own row in the result
tables and remains individually identifiable in every plot. Independent
simulation blocks for the **same** configuration may be combined because they
are repeated estimates of the same rejection probability, but their
block-level values are retained as a reproducibility check.

For interpretation, every fixed population pair will have a case sheet
containing:

1. the complete $P$ and $Q$ probability matrices;
2. their margins, $\delta$ values, association directions, and true MI;
3. separate rows for every $(n_P,n_Q)$ setting and its eight true expected
   cell counts;
4. configuration-specific false-positive rate, coverage, and validity for each
   method;
5. effective degrees-of-freedom summaries; and
6. a short conclusion limited to that exact configuration.

The labels N0-N7 are navigation labels only. They are not groups over which
results are pooled.

## 4. Common Simulation Rules

For every configuration,

$$
N^{(P)}\sim\operatorname{Multinomial}(n_P,P),
\qquad
N^{(Q)}\sim\operatorname{Multinomial}(n_Q,Q),
$$

independently. The following rules apply throughout:

- Every method receives exactly the same sampled table pair.
- Every output row carries a unique configuration identifier linking it to the
  exact $P$, $Q$, $n_P$, and $n_Q$ values.
- MI is measured in nats.
- No minimum expected cell count is imposed.
- No sampled table is discarded because a cell count is small or zero.
- No pseudocount, smoothing, or post-generation clipping is applied.
- The aligned `2x2` alphabet is retained even when a sampled row or column is
  empty.
- Undefined statistics and degrees of freedom are recorded as method failures,
  not silently converted into non-rejections.
- Calibration among valid results and the unconditional valid-result rate are
  reported together.
- Population construction, null simulation, and alternative simulation use
  separate fixed seeds.
- Confirmatory runs use seeds not examined during screening.

The true expected count in cell $(i,j)$ is $n_Pp_{ij}$ or $n_Qq_{ij}$. These
values are diagnostics, not admission criteria.

## 5. Correctness Checks

Before calibration or power experiments, verify that:

1. each generated population sums to one and has strictly positive cells;
2. its row and column margins equal the requested $(u,v)$ values;
3. the solved MI differs from its target by at most $10^{-10}$ nats;
4. manual plug-in MI and the production implementation agree;
5. the `2x2` bias correction is exactly $1/(2n)$;
6. scalar and vectorized method calls agree;
7. swapping $P$ and $Q$ changes only the sign of $T$, not two-sided p-values;
8. simultaneous row or column relabelling leaves all results unchanged; and
9. invalid cases return explicit validity flags rather than finite-looking
   p-values.

Failure of any correctness check blocks the larger runs.

## 6. Null Calibration Experiments

### 6.1 Sample-size sweep

Run all eight fixed null cases with equal sample sizes

$$
n_P=n_Q=n,
\qquad
n\in\{10,20,30,50,100,200,500,1000\}.
$$

This sweep does not choose $n$ from the expected counts. Consequently, the
smallest expected count ranges from ordinary values to far below one. For
example, N7 has a smallest expected count of approximately 0.0028 at $n=10$
and 0.28 at $n=1000$.

The main question is how calibration and validity change with $n$ for each
fixed population pair.

### 6.2 Sample-size imbalance

Use N0, N3, N5, and N7 with

$$
n_P\in\{10,20,50,100,200\},
\qquad
\frac{n_Q}{n_P}\in\{1,2,5,10\}.
$$

Repeat every unequal configuration after swapping $n_P$ and $n_Q$. This
separates sample-size imbalance from the arbitrary naming of the two
populations.

### 6.3 Near-zero MI boundary

The first-order MI variance becomes small as the population approaches
independence. To distinguish this effect from sparse cell counts, use two
fixed margin pairs,

$$
(u_P,v_P)=(0.50,0.50),
\qquad
(u_Q,v_Q)\in\{(0.50,0.50),(0.30,0.40)\},
$$

and target

$$
I(P)=I(Q)
\in
\{0,10^{-4},5\times10^{-4},10^{-3},5\times10^{-3},
  10^{-2},5\times10^{-2},10^{-1}\}.
$$

For each target, use

$$
n_P=n_Q\in\{20,50,100,200,500,1000\}.
$$

The exact-zero case is a known nonregular boundary and is reported as a
negative control, not as evidence for or against Expanded Welch. Positive
targets show how quickly the regular first-order approximation becomes
usable away from that boundary.

### 6.4 Rare-cell breakdown ladder

To push rare cells downward systematically, define

$$
s\in\{0.20,0.10,0.05,0.02,0.01,0.005,0.002,0.001\},
$$

with margins

$$
(u_P,v_P)=(s,s),
\qquad
(u_Q,v_Q)=(s/2,2s).
$$

Use the same positive-association branch in both populations and solve for
equal target MI. The primary ladder fixes

$$
I(P)=I(Q)=10^{-4}
$$

throughout. A secondary ladder uses $I(P)=I(Q)=0.005$ wherever that target is
mathematically attainable. Each population pair is sampled at

$$
n_P=n_Q\in\{10,20,50,100,200,500,1000\}.
$$

No configuration is removed because its expected counts are low. A
configuration may be omitted only when the requested target MI lies outside
the attainable range for its fixed margins, and that infeasibility is
recorded.

This ladder continues until validity or calibration fails; it does not stop at
the conventional expected-count thresholds of one or five.

## 7. Power Experiments

### 7.1 Effect parameter

Power is studied under

$$
I(Q)=I(P)+\Delta_I,
$$

where the true MI difference $\Delta_I$ is the parameter controlling departure
from the null. This is preferable to an arbitrary table-distance parameter
because it is exactly the quantity tested by the method.

For every alternative, $P$ remains fixed. The margins and association
direction of $Q$ also remain fixed, while its $\delta_Q$ is solved so that its
MI equals the requested value. Thus only the strength of association in $Q$
changes along each power curve.

### 7.2 Power families

Use three deterministic families:

| Family | $P$ margins | $Q$ margins | $I(P)$ | Values of $\Delta_I$ |
| --- | --- | --- | ---: | --- |
| Balanced/mild | $(0.50,0.50)$ | $(0.30,0.40)$ | 0.050 | $-0.040,-0.025,-0.010,-0.005,0,0.005,0.010,0.025,0.050,0.100$ |
| Sparse | $(0.10,0.10)$ | $(0.05,0.20)$ | 0.010 | $-0.009,-0.005,-0.002,0,0.002,0.005,0.010,0.020,0.040$ |
| Extreme rare | $(0.02,0.02)$ | $(0.01,0.05)$ | 0.001 | $-0.0009,-0.0005,0,0.0005,0.001,0.002,0.005,0.010$ |

All values are in nats. Any mathematically infeasible endpoint is identified
before simulation rather than clipped to the feasible range.

Use

$$
n_P=n_Q\in\{10,20,30,50,100,200,500,1000\}.
$$

For a smaller imbalance study, repeat the nonnegative effects with
$n_Q/n_P\in\{2,5,10\}$ at $n_P\in\{20,50,100\}$.

The primary threshold is

$$
\alpha=0.05.
$$

Power is the probability that a method rejects $H_0$ when
$\Delta_I\ne0$. Results at $\alpha=0.10$ and $0.01$ are secondary.

### 7.3 Fair power comparison

Two power quantities are reported:

1. **Nominal power:** rejection using each method's ordinary p-value threshold
   of 0.05. This describes operational performance.
2. **Size-adjusted power:** rejection using a method-specific critical value
   estimated from an independent null simulation for the same margins and
   sample sizes. This separates genuine sensitivity from inflated or
   conservative false-positive rates.

Null and alternative replicates used for size adjustment must be independent.

## 8. Diagnostics and Metrics

### 8.1 Null metrics

For every fixed configuration and method, report:

- false-positive and true-negative counts;
- false-positive rates at $\alpha=0.10$, $0.05$, and $0.01$;
- true-negative rates at the same significance levels;
- Wilson confidence intervals for those rates;
- absolute calibration error $|\widehat{\mathrm{FPR}}-\alpha|$;
- 95% confidence-interval coverage;
- valid-result rate and the reason for every invalid result;
- mean and standard deviation of $\widehat\Delta_{\mathrm{BC}}$;
- empirical standard deviation of $\widehat\Delta_{\mathrm{BC}}$ compared with
  the estimated standard error;
- the distribution of $T$;
- simple and expanded effective degrees of freedom; and
- frequencies of zero cells, empty rows or columns, and zero estimated MI
  variance.

Both the FPR among valid results and the unconditional rejection fraction are
saved. A low FPR accompanied by many invalid results is not interpreted as
good calibration.

These metrics are calculated separately for every exact $(P,Q,n_P,n_Q)$
combination. A mean across N0-N7, across sample sizes, or across nearby rare-cell
settings is not used to describe method accuracy.

### 8.2 Power metrics

For every alternative, report true-positive and false-negative counts,
true-positive rate (power), false-negative rate, size-adjusted power, Monte
Carlo confidence intervals, valid-result rate, and the exact values of $I(P)$,
$I(Q)$, and $\Delta_I$.

### 8.3 Mechanism diagnostics

To explain rather than merely rank the methods, save the following quantities
for selected replicates:

- $\widehat V(P)$ and $\widehat V(Q)$;
- the two variance-component contributions
  $\widehat V(P)/n_P$ and $\widehat V(Q)/n_Q$;
- the variance-influence estimates used by Expanded Welch;
- component and combined effective degrees of freedom; and
- the difference between Normal Wald, Simple Welch, and Expanded Welch
  critical values.

These diagnostics identify whether a failure comes from the MI estimator, the
standard error, the estimated degrees of freedom, or loss of first-order
validity.

## 9. Replication and Reproducibility

Use independent replicate blocks rather than one monolithic random stream.

| Stage | Replicates per configuration | Independent blocks | Purpose |
| --- | ---: | ---: | --- |
| Smoke | 500 | 1 | Verify code and outputs |
| Screening | 10,000 | 5 blocks of 2,000 | Map behaviour and locate transitions |
| Confirmatory | 50,000 | 5 new blocks of 10,000 | Confirm selected ordinary, transition, and failure cases |

At a true rejection rate of 0.05, 10,000 replicates have Monte Carlo standard
error approximately 0.00218; 50,000 have standard error approximately 0.00097.
Block-level results are retained so sensitivity to random seeds is visible.

The screening results may determine which already-defined configurations are
sent to confirmation, but they must not be used to alter the test formula.
The selection rule and confirmatory seeds are frozen before confirmation.

## 10. Planned Figures

1. **Case sheets:** one self-contained result section for every fixed
   population pair, with separate unpooled rows for all sample-size settings.
2. **FPR against sample size:** one separate panel per fixed population pair,
   with no averaging across pairs and a horizontal line at 0.05.
3. **Calibration-error heatmap:** every cell represents one exact null-case and
   sample-size combination; no cell is an average over configurations.
4. **Rejection-calibration curves:** actual rejection rate against nominal
   alpha. A separate curve file is saved for every configuration; selected
   examples may also be placed side by side for presentation.
5. **Validity plot:** valid-result rate against minimum expected cell count,
   with every point labelled by its configuration identifier.
6. **Null p-value ECDF:** empirical p-value distribution against the uniform
   reference, saved separately for every configuration.
7. **Studentized-statistic diagnostic:** empirical quantiles of $T$ compared
   with each method's reference quantiles for one configuration at a time.
8. **Power curves:** rejection probability against $|\Delta_I|$, drawn
   separately for each fixed population family and sample-size pair.
9. **Degrees-of-freedom plot:** expanded and simple effective degrees of
   freedom against sample size and minimum expected count; individual
   configurations remain identifiable.
10. **Standard-error diagnostic:** empirical standard deviation of the
    corrected MI difference divided by its estimated standard error for each
    configuration.

Overview figures may arrange multiple exact cases into panels, but their data
are never pooled. The complete case sheets and curves are retained
even when a smaller selection is used in a supervisor presentation.

## 11. Interpretation Rules

The experiment is exploratory about the location of breakdown but strict
about reporting it.

- A method is well calibrated when its FPR confidence interval contains the
  nominal level and its absolute error is practically small.
- Expanded Welch is an improvement only when it reduces absolute calibration
  error without creating a material loss of validity.
- Differences smaller than Monte Carlo uncertainty are reported as ties.
- A method that is conservative because many replicates are invalid is not
  treated as successful.
- Raw power is not used to claim superiority when null rejection rates differ;
  size-adjusted power is examined first.
- Results are reported for every predefined configuration, including cases
  that contradict the expected story.
- A conclusion about one configuration is not generalized to another merely
  because both have been given the same descriptive label.
- The exact-zero-MI boundary is separated from positive-MI failures because
  the current first-order theory is known to degenerate at independence.

No aggregate mean across population pairs, sample sizes, sparsity levels, or
power families is used as the primary accuracy result.

## 12. Saved Outputs

Each run should create:

```text
configurations.csv
correctness_checks.csv
infeasible_configurations.csv
null_summary.csv
power_summary.csv
power_null_thresholds.csv
rejection_curves.csv.gz
mechanism_diagnostics.csv
replicate_blocks.csv
run_metadata.json
REPORT.md
case_sheets/
figures/
```

`configurations.csv` records the full-precision $P$ and $Q$ probabilities,
margins, solved association parameters, true MI values, sample sizes, expected
cell counts, and seeds. `run_metadata.json` records software versions, command
arguments, and hashes of the experiment runner and imported statistical code.

`REPORT.md` is organized by fixed population pair rather than by an averaged
regime. `case_sheets/` contains one concise Markdown or HTML record
for each population pair, with every exact sample-size configuration linked
back to its rows in the CSV outputs.

## 13. Experiment Log

| ID | Experiment | Status | Output | Main conclusion |
| --- | --- | --- | --- | --- |
| C0 | Population and implementation correctness | Complete | `correctness_checks.csv` | All 158 confirmatory checks passed |
| C1 | Equal-size null calibration | Complete | Screening and holdout null summaries | Expanded Welch helps at some small samples, ties asymptotically, and overcorrects in other sparse cases |
| C2 | Sample-size imbalance | Complete | Screening and holdout null summaries | Clearest success: FPR near 0.05 in two cases where Wald FPR was about 0.17 |
| C3 | Near-zero MI boundary | Complete | Screening and holdout null summaries | All first-order tests become conservative near independence; Expanded Welch is most conservative |
| C4 | Rare-cell breakdown ladder | Complete | Screening and holdout null summaries | Expanded Welch reduces liberal rejection but can overcorrect or become invalid |
| P1 | Equal-size power curves | Complete | `power_summary.csv` | Expanded Welch has lower nominal but modestly higher size-adjusted power in selected regular cases |
| P2 | Unequal-size power curves | Complete | `power_summary.csv` | Size-adjusted results favor Expanded Welch in selected regular cases; the extreme-rare case breaks down |
| H1 | Confirmatory holdout | Complete | `results/2x2_confirmatory/` | Independent 50,000-replicate runs confirmed both the main improvements and limitations |

## 14. Order of Work

1. Implement the deterministic `2x2` population constructor and root solver.
2. Add the correctness tests in Section 5.
3. Implement one experiment runner that supports smoke, screening, and
   confirmatory profiles.
4. Run the smoke profile and correct implementation or output errors only.
5. Freeze configurations, metrics, plots, and screening seeds.
6. Run C1-C4 and identify ordinary, transition, and failure configurations.
7. Run P1-P2 and compare nominal with size-adjusted power.
8. Freeze the holdout selection rule and new seeds.
9. Run H1 and update this document with the results.
10. Decide which findings should next be tested in larger table shapes.
