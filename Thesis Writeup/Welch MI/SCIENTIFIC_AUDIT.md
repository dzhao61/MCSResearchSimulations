# Scientific audit of the active thesis

## Large-table construction check: 10 October 2026

The four new settings in LARGE_TABLE_CONSTRUCTION_CHECK_PLAN.md are complete:
16 x 16 first-block transfers, different-skew margins m_16(0.7)/m_16(0.8),
MI pairs (0.02,0.02)/(0.02,0.03) and n=1000/10000. Both methods and the
original focused/allocation records are unchanged. The combined scope is
240 unique settings, 70 population pairs and 4800000 distinct sampled pairs.

The extension's independent audit checks all 80000 scalar record pairs and
regenerates 68 input pairs. It reconstructs exact transfer populations and
independently checks positivity, margins, MI, variance/sensitivity moments,
statistics, degrees of freedom, distribution p-values, validity, rejection,
Wilson intervals, paired method contrasts and diagnostics. The original
232-setting audit and six-comparison allocation audit also pass.

All 152 Welch-project and 27 DifferentialMI tests pass. Eleven new tests
protect scope and combined counts, independent population moments, matching
controls while changing association, fixed-stream batching and resume,
checkpoint identity, bias/variance summaries, exact saved rejection totals,
independently classified directions, manuscript values and table generation.

At n=1000 the four-cell null bias is 0.03145199 nats, and the Wald/Expanded
false-positive rates are 0.30945/0.29770 with full validity. The alternative
bias is 0.03135981, so its mean corrected difference is approximately
0.02135981 despite true difference -0.01. Opposite-sign rejection counts
are 2493/2494 and 2350/2351. The failures therefore persist under the two
tested constructions, rather than arising only under copying.

At n=10000 the four-cell null rates are 0.04990/0.04910, with bias
-0.00097242. Alternative direction is correct in every rejection under
both constructions, but detection differs numerically: Wald 0.69920 under
copying versus 0.63230 under transfer. Observed alternative SD changes from
0.00433173 to 0.00468424 nats. The text reports this precision contrast;
it does not claim identical performance or validate the full falling curve
under the alternative construction.

Chapter 6 gives the short immediate interpretations; Appendix C contains
all eight matched rows and numerical discussion. Chapter 5 and Appendix B
specify the new settings and a cell-wise transfer formula. Contribution
statements distinguish the automatic rejection reduction from the measured
calibration, approximation and direction findings. The examiner-focused
claim/evidence check is in the extension plan. Original method, core,
population/summary and figure hashes, and older working drafts, are unchanged.
Final build and package verification are in SUBMISSION_CHECK.md.

## Saved-sample mechanism checks: 10 October 2026

Two additional analyses use existing repetitions, without changing either
test, any population, the 236-setting scope or the 4720000 distinct sampled
table pairs. Six different-skew copying null settings compare the observed
sample variance of Vhat with population tau-squared/n and the mean plug-in
prediction, separately for P and Q. Every row includes all 20000 finite
outputs; finite zeros and outputs with invalid tests would be retained.
Population sensitivities are recomputed independently from the probability
arrays and checked against the recorded moments.

At 4 x 4, MI 0.02 and n=10000, both predictions are within 2% of observed
variability. At MI 0.0001 and n=1000, population/observed ratios are 0.047
and 0.051, while plug-in/observed ratios are 1.950 and 2.093. The 16 x 16
comparison shows intermediate errors. These diagnose the variance-estimate
variability calculation, separately from the existing MI sampling-variance
diagnostics. Agreement does not establish a Student t distribution for the
complete test statistic.

Four existing 16 x 16 different-skew alternatives classify estimated direction
among two-sided rejections. At n=1000 and true difference -0.01, opposite-sign
counts are 2009/2010 for Wald and 1905/1906 for Expanded Welch. At -0.02 they
are 713/725 and 669/680. At n=10000, no rejection has the opposite sign in
either comparison. These supplement, rather than redefine, the existing
two-sided detection rates. Rejection under an alternative is not labelled a
false positive, and the test is not recast as a test of direction.

Thirteen new tests check sign classification, rejection denominators,
finite-zero inclusion, independent population moments, paired-output
bootstrap resampling, exact saved counts, numerical interpretations and
generated tables/evidence. All 141 Welch-project and 27 DifferentialMI
workspace tests pass. Both raw-record audits pass. Internal Monte Carlo
precision checks use 1000 deterministic bootstrap resamples of paired saved
variance/sensitivity outputs, not new multinomial samples.

Chapter 6 gives short interpretations; Appendices B-C provide calculations
and two new tables. The abstract, Introduction, practical discussion and
Conclusion agree on the supported contribution and lack of evidence for a
general replacement of Wald. Chapters 2-4, Appendix A, the eight figure assets,
methods, original study records and older working drafts retain their
pre-pass SHA-256 hashes. Final delivery verification is in SUBMISSION_CHECK.md.

## Unequal-sample check: 10 October 2026

The six fixed-total comparisons in UNEQUAL_SAMPLE_CHECK_PLAN.md are complete:
4 x 4 copying populations, different-skew margins, MI pairs (0.02, 0.02)
and (0.02, 0.03), and allocations 1000/1000, 400/1600 and 1600/400.
The two balanced records are byte-identical copies of the original study.
Four new settings add 80000 independent sampled pairs; there are no new
populations or changes to either statistical method. The combined evidence
has 236 distinct settings, 68 population pairs and 4720000 table pairs.

Both independent audits pass: the unchanged 232-setting study and all six
allocation comparisons. The latter verifies checkpoint provenance and exact
design, checks all 120000 scalar record pairs (including reused balance),
and regenerates 102 input pairs. It independently recalculates the unequal
variance weights, component/combined degrees of freedom, distribution
p-values, validity, rejection, Wilson intervals, paired contrasts and
diagnostics. The shared auditor now accepts explicit scope counts; its
original defaults and statistical calculations are unchanged.

All 128 Welch-project and 27 DifferentialMI tests pass. Eight new tests
protect the constant-total scope, unchanged populations, balanced reuse,
unequal corrections, sample weighting, batching/resume, saved results and
the generated allocation table. The correction contribution is -0.0084375
at 400/1600 and +0.0084375 at 1600/400, with remaining bias measured after
that correction.

All allocation results are finite and valid. Null Wald rates for balance,
400/1600 and 1600/400 are 0.0394, 0.0463 and 0.0454. Expanded rates are
0.0331, 0.0306 and 0.02515. Alternative Wald rates are 0.1132, 0.12945
and 0.05395; Expanded rates are 0.1013, 0.0997 and 0.0340. The generated
table rounds half-way rate values upward to four decimal places. It reports
all settings with intervals, validity and estimation diagnostics. The text
does not treat fixed-total detection differences as comparisons at equal
achieved false-positive rates or apportion their causal mechanisms.

Chapters 2-4, Appendix A and all eight figure assets are unchanged. Appendix
B specifies the new settings/corrections; Appendix C contains the full
comparison; Chapter 6 interprets it briefly. Counts and scope statements
in the abstract, Introduction, design, limitations and Conclusion agree.
Build, visual review and package verification are in SUBMISSION_CHECK.md.

## Targeted depth checks: 7 October 2026

The depth pass adds explanations, not experiments or changes to either test.
The independent raw-record audit passes again for all 232 settings, with
3,944 regenerated input pairs. All 120 Welch-project tests and 27
DifferentialMI tests pass. The three added regression checks verify:

- the individual-bias subtraction and mean estimated differences at the
  16x16, different-skew, n=1000 null and two alternatives;
- Student t distribution cutoffs of 2.277 and 1.991 at the reported median
  degrees of freedom 8.62 and 78.24, compared with the normal cutoff 1.960;
- the observed SDs 0.00327, 0.00364 and 0.00361 for the matched 4x4,
  n=10000, 0.01-nat detection contrast across the three margin regimes.

The exact bias identity is stated separately from its empirical numerical
evaluation. The explanation retains the measured change in bias across
alternatives; it does not assume a constant shift. Cutoffs at median degrees
of freedom are illustrations, not replacements for replicate-specific
cutoffs. Near independence, the text distinguishes population and plug-in
first-order variance calculations from observed sampling variance; it does
not claim an additive causal decomposition of rejection errors.

Chapters 3-4 are byte-identical to their pre-pass sources. Appendix B's only
change is the missing backslash in its copying equation. Primary-source
checks for the expanded synthesis are recorded in LITERATURE_SOURCE_CHECK.md.
The statistical implementations, populations, repetition records and figure
assets are unchanged. Packaging verification is recorded in SUBMISSION_CHECK.md.

## Focused-study audit: 6 October 2026

The active manuscript now uses the focused study specified in
`FOCUSED_EXPERIMENT_PLAN.md`, not the earlier broad experiment. All 232
settings, 68 strictly positive population pairs and 4,640,000 sampled table
pairs are complete. The two statistical implementations are unchanged.

`results/focused_study/independent_audit.json` passes. The independent audit
checks every raw chunk checksum and repetition count; reconstructs all
population margins, MI and variance quantities; regenerates 3,944 actual
sampled input pairs; and independently recomputes statistics, component and
combined degrees of freedom, normal and Student t distribution p-values,
validity masks, rejection denominators, Wilson intervals, paired contrasts,
bias, variance and degrees-of-freedom summaries. Checkpoint identity and
batch/resume invariance are covered by tests.

All 117 Welch-project tests and 27 DifferentialMI tests pass. Fifteen new
tests cover the focused construction, scope, sampling and reporting, including
CSV selection, unaltered plotted rates, printed figure geometry and label
bounds. The existing independent mathematical tests continue to verify the
variance sensitivity and worked calculations. No method code changed.

Chapters 5-8 and Appendices B-C were rewritten around the three controlled
questions, estimation diagnostics and four-setting construction check.
The unequal finite-sample bias explanation uses the new population and
repetition records; old numerical mechanism checks are not transferred to
this study. Findings about unequal sample sizes, rectangular tables or
arbitrary association locations are excluded from the new empirical scope.

The manuscript retains 35 active references. Morris, White and Crowther
(2019), checked against the primary Wiley article, supports question-led
simulation design and explicit performance measures. Earlier claim/source
checks remain applicable to the unchanged mathematical and literature
material. Final build, visual and package checks are in `SUBMISSION_CHECK.md`.

## Historical audit of the earlier broad-study manuscript

Initially checked 13 September 2026 and extended through 28 September 2026 against `chapters_rewrite/`,
`WelchSatterthwaiteMI/src/welch_differential_mi/welch.py`, the frozen
`results/thesis_redesign/` outputs, and the primary sources in
`LITERATURE_SOURCE_CHECK.md`. This is an independent derivation and
implementation review, not a claim of formal peer review or an exhaustive
literature search.

The 27-28 September final acceptance refresh reran all 101 tests and the full
source-linked evidence audit successfully. The frozen protocol, simulation
core, method implementation and directly imported statistical dependencies
still have their recorded source hashes; the previously documented
orchestration-only drift is unchanged. The remaining edits improve
presentation and archive completeness, without changing the mathematics or
results. Current build, page-review and package-reproduction evidence is
recorded in `SUBMISSION_CHECK.md`.

## Findings and disposition

| Priority | Finding | Disposition |
| --- | --- | --- |
| Important | Earlier literature already gives the leading categorical/histogram MI bias and sampling variance, and MI-index comparisons predate this thesis. | Chapter 2 now credits Moddemeijer, Brillinger, and Mora--Ruiz-Castillo explicitly. The claimed contribution is narrowed to the variance-estimator sensitivity, its Welch use, and the fixed-regime evaluation. |
| Important | Positive MI variance \(V(P)>0\) does **not** imply positive variance-sensitivity variance \(\tau^2(P)>0\). | Chapter 4 now states the additional condition for its first-order component degrees of freedom. A concrete counterexample is below and is guarded by a regression test. |
| Important | Satterthwaite moment matching of the denominator does not prove an exact Student reference for the ratio. The numerator and estimated variance use the same sample. | Chapter 4 now states their generally nonzero first-order covariance. The thesis correctly describes Student as a working reference and interprets its performance empirically. |
| Important | The original results documented near-independence conservatism without explaining its scale. | Chapter 4 now retains the interpretable local relations `V ≈ 2I`, `tau² ≈ 4V`, and component df `≈ nI`. Higher-order local-moment checks remain in the experiment supplement rather than the main thesis. |
| Important | A derivative check validates the algebra of the expanded df, not the quality of its moment approximation. | A supplementary study now compares population first-order, local-moment, plug-in and finite-sample moment dfs, and uses an independent pilot SD to diagnose the complete standardisation. |
| Important | The empirical contribution lacked direct ablations of the complete variance sensitivity. | Simple Welch and a kurtosis-only frozen-score df were evaluated over 809 selected configurations. They show that the complete pointwise and margin derivative drives most of the additional conservatism. |
| Important | Hutcheson (1970) is a direct information-theoretic Welch predecessor and uses component df (n_i), not (n_i-1). | The history and gap statement were corrected. A separate Hutcheson-style MI arm was added to the supplementary study without modifying the frozen confirmatory run. |
| Important | An earlier sentence said clipping a negative bias-corrected estimate would change the estimand. The estimand remains the population MI difference; clipping changes the estimator. | Chapter 3 now states the correct consequence: clipping creates a different nonlinear estimator with different finite-sample bias and sampling behaviour. |
| Important | The independence appendix stated the quadratic result without defining its perturbation or displaying the Taylor terms. | Appendix D now defines the path and expansion point, separates the zeroth-, first-, and second-order terms, derives both forms of the Hessian, and connects multinomial cell error to the usual chi-squared limit. |
| Checked | The analytic cell-sensitivity expression, plug-in implementation, and saved result summaries agree under the checks below. | No change to the frozen simulations or method implementation was justified. |
| Checked | The current orchestration runner has changed since the recorded run. | The diff contains atlas-count metadata, output-hash additions for future runs, and corrected one-pass handling of a failed preflight. The frozen protocol, simulation core, method implementation, and imported statistical dependencies retain their recorded hashes; population construction, simulation, method evaluation, and the saved results are unaffected. The exact old and current runner hashes are documented in the experiment-supplement README. |

## Strict component-validity convention

The final review identified a useful distinction between the mathematical
combined degrees of freedom and the software validity rule. Substituting the
component expression into the Welch--Satterthwaite combination gives

\[
 \widehat\nu_{\mathrm{expanded}}
 =\frac{\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\}^2}
 {\widehat\tau^2(P)/(2n_P^3)+\widehat\tau^2(Q)/(2n_Q^3)}.
\]

The factors of \(\widehat V^2\) cancel. A direct numerical check agrees with
the component implementation to floating-point precision whenever both
component degrees of freedom are defined. If one table has
\(\widehat V=\widehat\tau^2=0\) and the other supplies a positive denominator
contribution, the direct expression remains defined and reduces to the other
table's contribution. The frozen software does not
evaluate that case directly: it requires both component degrees of freedom to
be positive and finite. The manuscript therefore states that some
Expanded-only invalidity comes from this strict convention. This clarification
does not change the evaluated procedure, its rejection results or its exact
nesting within Wald on valid outputs, so neither a core-code change nor a
confirmatory rerun was warranted.

## Derivation checked independently

Write \(L_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}\). For an observation in
cell \((x,y)\), perturb \(P\) toward a point mass at that cell. The
directional derivative of MI is

\[
  \psi_P(x,y)=L_P(x,y)-I(P),
  \qquad V(P)=E_P\{\psi_P(X,Y)^2\}.
\]

Thus the leading multinomial sampling variance of plug-in MI is \(V(P)/n\).
This is established prior theory, not the new part of the thesis. For the
variance functional, differentiating both the probability weights and the
pointwise log ratios gives

\[
  g_P(x,y)=\psi_P(x,y)^2-V(P)
  +2\left[L_P(x,y)-E_P\{L_P\mid X=x\}
                    -E_P\{L_P\mid Y=y\}+I(P)\right].
\]

In particular, the two conditional-mean terms are necessary because the row
and column margins change when a cell is perturbed. The identity
\(E_Pg_P(X,Y)=0\) follows by averaging the derivative over the point-mass
directions. With \(\tau^2(P)=E_Pg_P(X,Y)^2\), the first-order sampling
variance of the plug-in \(\widehat V(P)\) is \(\tau^2(P)/n\). Matching a
scaled chi-squared variable's mean and variance then gives the working
component degree of freedom \(2nV(P)^2/\tau^2(P)\), provided
\(\tau^2(P)>0\). The code uses the plug-in version of exactly these terms.

`WelchSatterthwaiteMI/tests/test_thesis_derivation_audit.py` evaluates
\(V(P)\) directly from probabilities and differentiates it by symmetric
finite differences, without reusing the analytic `g` formula. It checks
both \(2\times2\) and \(3\times3\) positive tables against the code's
\(\widehat\tau^2\) and component degree of freedom. The existing Welch tests
also check baseline agreement, table swapping, relabelling, validity, and
the large-sample approach to the normal reference.

The 15 September extension adds two checks. First, for a general perturbation
$h$ around a non-uniform independent $2\times3$ table, a centred numerical
second derivative of MI agrees with

\[
 \sum_{i,j}\frac{h_{ij}^2}{p_{ij}}
 -\sum_i\frac{h_{i+}^2}{p_{i+}}
 -\sum_j\frac{h_{+j}^2}{p_{+j}}
 =\sum_{i,j}\frac{a_{ij}^2}{p_{i+}p_{+j}},
\]

where $a_{ij}=h_{ij}-p_{+j}h_{i+}-p_{i+}h_{+j}$. The corresponding numerical
first derivative is zero. Second, the worked examples are now regression
checked as described below.

## Worked examples and displayed calculations

The Chapter 4 count tables were evaluated twice: once by direct substitution
into the displayed equations and once through `differential_mi_pvalues`.
Both routes give

| Quantity | $P$ | $Q$ |
| --- | ---: | ---: |
| Plug-in MI | 0.136927... | 0.258483... |
| $\widehat V$ | 0.271892... | 0.433710... |
| $\widehat\tau^2$ | 0.932122... | 0.820348... |
| Component df | 16.654840... | 45.859569... |

The remaining shared values are
$\widehat\Delta_{\rm BC}=-0.12059256...$,
$\widehat{\rm SE}=0.08322589...$, $T=-1.44897897...$, normal Wald
$p=0.14734345...$, combined df $59.028703...$, and Expanded Welch
$p=0.15263530...$. Every value agrees with the manuscript at its displayed
precision.

The Chapter 5 probability pair was matched to saved population
`pair_416685eb037a66f0`. Its rows and columns are $(0.7,0.3)$ for $P$ and
$(0.8,0.2)$ for $Q$, and direct evaluation gives MI 0.02 and 0.03 nats to
14 decimal places. The rounded matrices in the manuscript now use a
consistent five decimal places and each displayed table sums to one.

## Equation-to-implementation reconciliation

The active derivation and implementation agree on the following points.

- The estimand is $I(P)-I(Q)$, while the leading correction subtracts
  $d/(2n_P)$ and $d/(2n_Q)$ from the two plug-in estimates. Equal-sample
  corrections cancel in the difference; unequal-sample corrections do not.
- $V(P)$ is the observation-level variance of pointwise MI, whereas the
  first-order sampling variance of plug-in MI is $V(P)/n_P$.
- The code's sensitivity includes both conditional row and column means in
  the displayed $g_P$ formula; these terms are not an optional simplification.
- The component formula is $2n_PV(P)^2/\tau^2(P)$. Its interpretation depends
  on the relative variance $\tau^2(P)/(n_PV(P)^2)$, not on the absolute size
  of $\tau^2(P)$ alone.
- The combined degrees of freedom use the same two contributions as the
  squared standard error. The Expanded p-value changes only the reference
  distribution; the corrected difference, standard error and statistic are
  identical to Wald.
- Population samples are independent, but each sample's MI and variance
  estimates are generally dependent. Therefore the Student law is explicitly
  described as a working moment-matched reference.
- The software validation rules now stated in Chapter 4 match `_validate_pair`,
  `base_valid`, and `expanded_valid`: Expanded Welch has additional positive,
  finite component and combined degrees-of-freedom requirements.
- At exact within-table independence, the first-order MI derivative and $V$
  vanish. The surviving quadratic term leads to $2n\widehat I$ and its
  chi-squared limit; constructing $\widehat Q$ from $\widehat P$'s margins
  does not create an independent second sample.

## Counterexample to an overly broad regularity claim

Consider the positive \(2\times2\) family

\[
 P_t=\tfrac14\begin{pmatrix}1+t&1-t\\1-t&1+t\end{pmatrix},
 \qquad 0<t<1.
\]

At \(t\approx0.8335565596\), all cells are positive,
\(I(P_t)\approx0.406579\), and \(V(P_t)\approx0.439229\), but
\(g_{P_t}(x,y)=0\) in every cell. This is an interior stationary point of
the MI-variance functional. To see why, let
\(L_+=\log(1+t)\) and \(L_-=\log(1-t)\). Symmetry makes the conditional
row and column means of pointwise MI equal to \(I(P_t)\). The two possible
sensitivity values therefore differ by
\[
  g_+-g_-=(L_+-L_-)\{L_++L_--2I(P_t)+2\}.
\]
The displayed value of \(t\) solves the zero of the second bracket. Since
\(E_{P_t}g=0\), equal sensitivity values must both be zero. Consequently
\(\tau^2(P_t)=0\) even though
\(V(P_t)>0\). The first-order \(\widehat V\) variance and its finite
component degree-of-freedom formula are degenerate there. This does **not**
invalidate the first-order MI Wald statistic, whose \(V(P_t)\) is positive;
it limits the particular first-order model for the *estimated variance*.

## Why the Student reference is not a theorem here

For one sample, the leading errors have the forms

\[
 \widehat I-I\approx n^{-1}\sum_a\psi_P(Z_a),\qquad
 \widehat V-V\approx n^{-1}\sum_a g_P(Z_a).
\]

Their leading covariance is
\(E_P\{\psi_P(Z)g_P(Z)\}/n\), which need not vanish. For example, at
\(P=\left(\begin{smallmatrix}.36&.14\\.09&.41\end{smallmatrix}\right)\),
direct evaluation gives approximately \(0.34339/n\). The two *population
samples* are independent; the effect estimate and variance estimate
*within either sample* are not generally independent. Hence the
Satterthwaite calculation matches denominator moments only. It does not
imply an exact Student distribution for \(T\), particularly near
independence or with sparse observed support.

The two methods share \(T\) and their standard error. At common-valid
samples a finite-df Student two-sided tail is no smaller than the normal
tail, so Expanded Welch's rejection set is nested within Wald's. The frozen
paired results have zero Expanded-only rejections across 3,111 configurations,
consistent with that theorem. This cannot by itself show superior calibration
or power; rejection falls under both the null and alternatives.

## Supplementary mechanism check

The explanatory follow-up uses the frozen population tables but new random
samples. It contains 809 unique evaluation configurations with 20,000 table
pairs each. Each of 169 null configurations has a separate 20,000-pair pilot,
for 19.56 million new table pairs in total. It is labelled as follow-up evidence
and does not alter the frozen 3,111-configuration confirmatory run.

For the additive first-block 3x3 different-skew null with equal MI 0.02 and
equal sample sizes 100, the evaluation gives Wald rejection 0.0166. Dividing
the numerator by the finite-sample SD estimated from the independent pilot
gives 0.0551, while dividing by the population first-order SD gives 0.0976.
The average estimated squared SE is 1.1699 times the empirical variance, but
the empirical numerator variance is 1.4249 times the population first-order
variance. This supports denominator estimation as an important mechanism and
simultaneously rules out the stronger claim that denominator mean bias alone
explains the regime.

At the same point, the population first-order component dfs are 1.73 and 1.51,
the evaluation medians of the plug-in dfs are 3.14 and 2.43, and independent
pilot moment dfs are 4.84 and 3.77. The first-order variance approximation for
the variance estimator is already within about 10%, so its shifted finite-
sample mean also contributes to the df discrepancy. At n=1000 the three
calculations are substantially closer. These observations support a condition
that `nV` should be large relative to interaction dimension `d`; they do not
prove failure for every small-df population.

The follow-up also compares Hutcheson's component assignment (n_i) with the
ordinary-Welch assignment (n_i-1). Their rejection rates are identical in
494 of 809 configurations, differ by 0.00047 on average in absolute value, and
differ by at most 0.01235 in the extreme 5x5, n=5 alternative. This confirms
that the historical correction matters conceptually but does not overturn the
empirical conclusion about the much stronger Expanded Welch adjustment.

The follow-up also checks the observed-support bias correction. Its effect
changes with the direction of sample imbalance, so it is retained only as a
sensitivity analysis. All exact rates, validity values, Monte Carlo errors,
paired differences, source hashes and deterministic seed rules are stored in
`results/thesis_mechanism_check/`.

## Empirical claim audit

- The source-linked `figures_rewrite/audit_evidence.py` reconstructs the frozen
  protocol and its display, configuration and population manifests exactly.
  It verifies all 4,001 display slots, 3,111 unique configurations, 534
  population pairs, 20,000 replicates per configuration and the complete
  section-level counts.
- The same audit independently reconstructs the exact regime selection for
  each of the 22 thesis figures. It checks equality with every figure-manifest
  configuration list, the two method rows and denominator for each plotted
  configuration, valid probability ranges, the generated evidence macros and
  valid PDF artifacts. Regenerating the figures from the frozen CSVs followed
  by this audit passes.
- Every numerical result stated in Chapter 6 is executable audit evidence:
  main-grid null counts and ranges, both paired examples and Wilson intervals,
  the sparse validity example, baseline-MI and changed-cell null rates,
  unequal-sample direction results, constructor comparison, extreme-skew and
  independence examples, convergence ranges, and all runtime table medians
  and interquartile ranges.
- The displayed null and alternative rates use all 20,000 replicates per
  configuration. Invalid outputs are non-rejections in this **operational**
  rate and are separately reported by validity. They are not valid true
  negatives.
- The empirical comparison is at a fixed nominal 0.05 threshold. Alternative
  rejection rates are not size-adjusted power, so a lower Expanded Welch
  rate cannot be interpreted alone as proof of a worse test.
- Fixed population pairs, not a probability sample of all joint tables,
  underlie the regime landscape. Pointwise Monte Carlo intervals quantify
  simulation error at those pairs, not uncertainty about generalisation to
  untested distributions.
- The experimental protocol was frozen after exploration, not externally
  preregistered. Reused display points are not independent replication.

## Reproduction

From the workspace root:

```bash
.venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests -p 'test_*.py'
.venv/bin/python 'Thesis Writeup/Welch MI/figures_rewrite/audit_evidence.py'
```

The mathematical checks above support the internal consistency of the stated
method; they do not prove the quality of its finite-sample reference. That is
an empirical question addressed by the frozen simulations. Final review should
still challenge the proposed reference as a **working approximation**, the
relevance of the selected fixed-population families to the intended
application, and the narrow contribution statement in Chapter 2.
