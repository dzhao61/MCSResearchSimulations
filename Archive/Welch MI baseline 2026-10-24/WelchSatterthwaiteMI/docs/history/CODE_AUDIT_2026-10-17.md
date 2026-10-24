# Current Thesis Code Audit

Date: 17 October 2026.

Scope: the current Welch MI thesis pipeline, its executed dependencies,
supporting checks, practical application, reporting and delivery scripts.
The scientific code, saved scientific results, thesis and historical drafts
were not edited during this audit.

## Verdict

One result-affecting numerical bug needs correction before treating the
small-sample results as final. It concerns enforcement of the existing
zero-component validity rule, not the MI derivation or the experiment's
population construction. Four further findings concern audit safeguards,
report generation and reproducibility materials.

The original results reproduce, but reproduction alone did not expose the
numerical bug. The new checks compared the implementation with exact
integer properties of the input tables as well as independent formulas.

## Findings

### 1. P1: Floating-point residue makes exactly degenerate components appear valid

Locations: `DifferentialMI/src/differential_mi/statistics.py:93-96`;
`WelchSatterthwaiteMI/src/welch_differential_mi/welch.py:170-176` and
`:290-298`.

The MI variance and variance sensitivity can be exactly zero for an observed
table, while floating-point calculations leave tiny positive residuals.
The component degrees-of-freedom calculation accepts any positive sensitivity
variance. Dividing two residuals can then produce an ordinary-looking,
positive degrees of freedom, and `expanded_valid` becomes true.

The combined variance threshold does not prevent this when the other table
has a genuine positive variance. This conflicts with the manuscript's
declared rule that both component degrees of freedom must be defined,
positive and finite.

A simple reproduction is:

```python
import numpy as np
from welch_differential_mi.welch import differential_mi_pvalues

p = np.array([[1, 1], [4, 4]])
q = np.array([[7, 0], [0, 3]])
values = differential_mi_pvalues(
    p, q, include_simple=False, include_unbiased_sensitivity=False
)
print(values["influence_variance_p"])
print(values["variance_influence_variance_p"])
print(values["expanded_component_degrees_of_freedom_p"])
print(values["expanded_valid"])
```

The empirical distribution of `p` is exactly independent: its rows are
`(0.2, 0.8)` and its columns are `(0.5, 0.5)`. Its pointwise MI, MI variance
and variance sensitivity are all exactly zero. The current implementation
instead returns approximately:

```text
variance_p = 1.9721522630525296e-33
sensitivity_variance_p = 8.751115234492231e-66
component_df_p = 8.888888888888888
expanded_valid = True
```

The resulting finite Expanded Welch p-value is not consistent with the
implemented-and-disclosed policy for genuinely zero components. Normal Wald
can remain usable because `q` supplies a positive variance contribution.

#### Measured impact

I regenerated all saved inputs for the 66 core settings with sample size at
most 250. A table has exactly constant pointwise MI on its occupied cells
if, for an occupied reference cell `(a,b)`, every occupied `(i,j)` satisfies

```text
N[i,j] * row_total[a] * column_total[b]
    == N[a,b] * row_total[i] * column_total[j].
```

This uses integer arithmetic, not a floating-point tolerance. Constant
pointwise MI implies exactly zero empirical MI variance and, under the
occupied-cell calculation used here, zero sensitivity variance.

Results:

- 12,318 currently valid Expanded Welch outputs contain such an exactly
  degenerate component, across 28 core null settings.
- Those outputs include 859 currently counted rejections.
- Transposing both input tables changes Expanded Welch validity for 2,405
  sampled pairs and rejection decisions for 394 pairs across the checked
  settings. Exchanging the roles of the two variables should not do this.
- The largest rejection-rate reduction from merely excluding the identified
  outputs is 0.0081. The largest validity-rate reduction is 0.17525.

Illustrative mask-only impact calculations:

| Setting | Current rejections | Identified degenerate rejections | Remaining rejections | Rate before / after exclusion |
| --- | ---: | ---: | ---: | --- |
| 2 x 2, uniform, n=10 | 510 | 141 | 369 | 0.0255 / 0.0185 |
| 4 x 4, different skew, n=10 | 985 | 56 | 929 | 0.0493 / 0.0465 |
| 8 x 8, different skew, n=10 | 2,144 | 162 | 1,982 | 0.1072 / 0.0991 |
| 16 x 16, different skew, n=10 | 2,517 | 138 | 2,379 | 0.1259 / 0.1190 |

These are diagnostic exclusions, not replacement results from a corrected
implementation. In the 2 x 2 uniform n=10 setting, validity would fall from
19,631/20,000 to 16,126/20,000 under this exclusion, crossing the figure's
90% marker threshold.

A scan of the saved scalar records across the core and both extensions
found no positive near-zero component marked valid in the larger-sample
settings outside the identified small-sample group. The large-sample power
comparisons, the main 16 x 16 n=1,000 bias result, and the full-data shopping
application did not show the issue. The highlighted 4 x 4 uniform n=20
and 8 x 8 different-skew n=100 improvements are not among the affected
settings.

The practical exploration's subsample analysis has the same problem in
260 outputs across seven subset settings, including three rejections.
Those subset-stability results are not presented in the current thesis;
the six full-data comparisons remain independently verified.

Why existing checks missed it: ordinary formula comparisons accept errors
of this very small absolute size, while the validity predicate depends on
whether those values are strictly greater than zero. Existing tests cover
some degenerate tables, but not these equivalent independence patterns or
invariance of the validity mask under transposition and relabelling.

Recommended correction: implement consistent numerical-zero handling for
each component, with stable score/variance calculations and explicit
degeneracy checks. Preserve the disclosed zero-component policy rather than
silently introducing a different test. Add exact-degeneracy and label-
invariance regressions, then re-evaluate the saved deterministic inputs and
regenerate affected rates, diagnostics and figures. Do not edit result CSVs
manually or simply increase a tolerance without measuring its effects.

### 2. P2: The main independent auditor does not authenticate the experimental labels

Location: `WelchSatterthwaiteMI/experiments/audit_focused_study.py:32-47`.

The auditor checks the scientific source fingerprint, run phase, repetition
count, summary sizes, population moments and numerical outputs. It does not
compare the saved configuration/display manifests with `build_design()`,
check the current manifests against the stored design digest, or verify
each base checkpoint's identity against the run identity.

In a temporary copy, changing one configuration's `profile` to an invalid
experimental label still produces `all_pass: true`. The number calculations
remain internally consistent because the configuration ID and stored arrays
are unchanged, but the scientific condition has been mislabelled.

No such corruption was found in the actual study. I separately compared
every current base configuration, display assignment, population definition
and population array with the reconstructed design; they match exactly.
The supporting runners already perform stronger explicit scope/provenance
checks than the base auditor.

Recommended correction: authenticate the full base manifest, display
mapping, population definitions/arrays and checkpoint identities before
checking the numerical summaries. Add mutation tests that alter labels,
targets, identifiers and checkpoint provenance.

### 3. P2: The main reporter accepts changed summaries after a previous successful audit

Location: `WelchSatterthwaiteMI/experiments/report_focused_study.py:245-252`.

The reporter only checks the stored boolean `verification.json["all_pass"]`
before reading its CSV inputs. That flag is not tied to the current CSV
hashes and does not trigger fresh numerical verification.

In a temporary copy, changing the 4 x 4 different-skew n=1,000 null bias to
the invented value `0.12345` while keeping the old verification file caused
the reporter to export `0.12345` into the manuscript table without error.
The original results were not changed. This demonstrates a stale-evidence
guard failure, not an observed erroneous bias in the delivered tables.

Recommended correction: run the strengthened independent audit before
export, or require a verification artifact bound to hashes of every input
used by the reporter. The supporting reporters already do more checking.

### 4. P2: The delivered supplement omits the practical application

Location: `Thesis Writeup/Welch MI/package_deliverables.py:59-103`.

The package includes the simulation code and four simulation/diagnostic
result directories, but no `PracticalMIExploration` files. I checked the
actual delivered ZIP as well as the packaging function.

Consequently, that supplement cannot reproduce Chapter 6.5's shopping
application or Appendix C.7's six-comparison Holm correction from the
supplied files, even though the relevant implementation, raw archives,
count tables and verification exist in the workspace.

This is a completeness gap in the optional reproducibility materials, not
an error in the application results or a dependency of the standalone PDF.
Include the application runner, source/protocol metadata, count tables,
full-data results and tests. Either include the appropriately attributed
raw archives or provide a download-and-hash-verification procedure. The
150,000 exploratory subsets need not be bundled to reproduce the thesis's
full-data application.

### 5. P3: Bundled README verification instructions still point to the previous study

Locations: `WelchSatterthwaiteMI/README.md:87-104` and
`WelchSatterthwaiteMI/experiments/README.md:3-13`.

The first README correctly introduces the focused study, but its verification
and regeneration commands still target the old thesis redesign. The
experiment index also calls that old 3,111-setting experiment current.
The delivered supplement omits `run_thesis_redesign.py`,
`test_thesis_redesign.py` and `test_thesis_mechanism_check.py`, so the old
commands cannot run from the delivered archive.

`EXPERIMENT_SUPPLEMENT_README.md` has the correct focused-study instructions.
Replace the conflicting commands and mark the old experiment as historical.
No scientific rerun is needed for this documentation correction.

## Formula And Parameter Review

Apart from finding 1, the executed formulas agree with the manuscript and
with independently calculated reference values.

| Area | Checks and assessment |
| --- | --- |
| MI and units | Natural logarithms throughout; empirical joint/row/column probabilities use the same observations; zero cells have zero weight. |
| Bias correction | Uses the fixed declared alphabet, `(r-1)(c-1)/(2n)`. Equal-n terms cancel; unequal allocations give the stated +/-0.0084375 offset for 4 x 4 tables. Negative corrected estimates are retained. |
| Shared statistic | Difference is P minus Q. Variance is `V_p/n_p + V_q/n_q`; the two-sided normal reference uses a survival function, avoiding upper-tail subtraction. |
| Variance sensitivity | Both changes in probability weights and changes in the pointwise MI values/margins are included. The sensitivity is centred before its empirical variance is calculated. |
| Expanded degrees of freedom | The factor `2*n*V**2/tau2` and its two-sample combination are correct away from the numerical degeneracy above. The equivalent denominator uses `tau_p/(2*n_p**3) + tau_q/(2*n_q**3)`. |
| Copying construction | Convex mixture of independent draws and copying; margins are preserved. Targets are solved inside the feasible entropy endpoint, not clipped. |
| Four-cell construction | Equal positive/negative transfers preserve margins. Endpoint feasibility, positivity, normalisation and target MI are checked. |
| Population assumptions | All 70 chosen pairs have positive cells, positive population MI variance and positive population sensitivity variance. |
| Sampling | Independent multinomial P/Q samples; both methods receive the same pair. Distinct population pairs/allocations have distinct deterministic streams. |
| Invalid outputs | Remain in the unconditional denominator, with validity separately reported. The numerical enforcement of the zero-component case needs the correction above. |
| Estimation diagnostics | Bias and observed sample variance are separated. Estimated/observed variance ratios use matched finite subsets; finite zero estimates remain included. |
| Uncertainty | Wilson intervals for individual rates; paired indicator intervals for within-sample method contrasts. Cross-construction comparisons do not reuse paired-contrast assumptions. |
| Degrees-of-freedom summaries | Medians and 5th/95th percentiles use valid Expanded Welch outputs; these describe output spread, not confidence intervals for a median. |
| Jackknife | Deletes observations with cell-count weighting, recalculates margins, retains negative estimates, and replaces rather than adds to the analytic correction. Original standard errors are retained. |
| Output bootstraps | Resample paired saved diagnostic quantities to measure Monte Carlo precision. They are not substituted for a bootstrap MI test. |
| Runtime | Full method calls use matching optional-calculation flags; sampling/construction are excluded; warm-up and alternating method order are present. |
| Practical data | Group labels, category alignment, exclusions, raw archive hashes and count-table construction verify. No smoothing or category dropping is introduced. |
| Holm correction | Uses all six original full-data comparisons, separately for each method; sorted cumulative maxima and family multipliers are correct. |

### Exact Experimental Settings

| Component | Parameters verified |
| --- | --- |
| Core sizes | 2 x 2, 4 x 4, 8 x 8, 16 x 16. |
| Margins | Uniform; same skew with dominant probability 0.8 in both populations; different skew with 0.7 in P and 0.8 in Q. Remaining mass is shared equally. |
| Null study | MI=0.02 in both populations; n=10,20,50,100,250,500,1000,2500,10000,50000; 120 settings. |
| Common-MI study | 4 x 4 different skew; common MI=0.0001,0.0003,0.001,0.003,0.01,0.02,0.05; n=100,1000; 14 displayed settings. |
| Power study | P MI=0.02; Q MI=0.02 plus difference 0,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2; n=1000,10000; all sizes under different skew plus the other two 4 x 4 margin regimes; 108 displayed settings. |
| Core construction check | Four-cell 4 x 4 different-skew tables, MI pairs (0.02,0.02)/(0.02,0.03), n=1000/10000; four settings. |
| Allocation check | Same two copying 4 x 4 pairs; allocations (1000,1000), (400,1600), (1600,400); two reused balanced settings and four new settings. |
| Large construction check | Matched 16 x 16 different-skew four-cell tables; two MI pairs and n=1000/10000; four new settings and two new population pairs. |
| Jackknife diagnostic | Four existing 16 x 16 copying settings; 80,000 original sample pairs; no new experimental settings. |
| Main simulation controls | Seed 20261006; 20,000 repetitions per setting; alpha=0.05; chunks of 1000; default calculation batches of 250; separate pilot phase with 200 repetitions. |
| Construction tolerances | Absolute MI error 1e-12 plus 1e-8 times target; total/margin error 1e-12; root tolerances 1e-15 absolute and 1e-14 relative. |
| Runtime controls | n=1000, 200 generated pairs per size, 20 warm-up calls per method, five passes and 1000 timed calls per method/size. |
| Practical controls | Six full comparisons; subset sizes 50,100,200,500,1000,2000,5000 when feasible; seed 20261010; 5000 repetitions per subset setting; sampling without replacement within each subset. |

Deduplication is correct: the core has 232 distinct settings and 68 pairs.
The allocation extension contributes four new settings and no new pairs;
the construction extension contributes four settings and two pairs.
Combined totals are 240 settings, 70 pairs and 4,800,000 distinct sampled
table pairs. The two copied balanced settings are not counted twice.

## Verification Performed

- Read 126 function definitions in total: all definitions in 16 active
  source files, plus seven used helpers in two older dependency modules.
  The primary files contain 3305 lines. The function/source-hash ledger is
  supplied with this report.
- Ran all 224 existing workspace tests: 181 Welch project, 27 shared
  DifferentialMI and 16 practical-application tests. All pass; finding 1 is
  a newly demonstrated coverage gap, not an existing failing unit test.
- Compared 1296 independently generated table pairs, including sparse and
  rectangular tables, with a separate long-double scalar calculation.
  Maximum absolute errors away from classification boundaries were about
  2.1e-15 for the corrected difference, 2.3e-15 for MI variance, 2.9e-15
  for sensitivity variance and 1.2e-13 for p-values.
- Compared 100 jackknife cases with literally removing each observation.
- Checked calculation-batch invariance at every one of the 232 core
  settings, not just one representative population.
- Checked a two-chunk run, exact resumed outputs, recovery when a checksum
  write was interrupted, and equivalence between serial and two-worker
  execution on the same inputs.
- Reran the core, allocation and large-construction raw-result audits.
  These validate all saved scalar records/checksums and recalculate p-values,
  summaries, masks and intervals; they also regenerate initial input pairs.
- Reran the full jackknife audit, regenerating all 80,000 original pairs
  and reproducing the diagnostic records and summaries.
- Reconstructed all six practical count tables and full-data comparisons;
  verified all 150,000 saved subset pairs against their deterministic
  sampling streams, finite-population bounds and recalculated outputs.
- Checked exact current manifests and population arrays against the
  constructors independently of the weak base-audit safeguards.
- Ran the altered-label and altered-diagnostic mutation checks described
  above using temporary copies only.
- Tested the actual extracted supplement: 95 Welch tests were discovered,
  with four expected skips because the thesis source is supplied separately;
  the other 91 and all 27 shared-library tests pass. This does not cover
  the omitted application.

## Coverage Boundary

The review covers the active scientific paths and all functions in their
current runner/reporting modules. Older modules are included for the
constructor and interval helpers that the current study actually calls.
Package initialisers and required local imports were also checked.

Unrelated historical research projects, discontinued comparator algorithms,
inactive old figure generators and external library internals are not
claimed as fully audited. Existing tests exercise some historical APIs, but
that is not a substitute for a separate source audit of those projects.

## Recommended Next Work

1. Correct numerical-zero handling while preserving the current declared
   zero-component rule. Add regressions for the exact example, constant-
   score tables, empty margins and relabelling/transposition invariance.
2. Re-evaluate the deterministic existing inputs under a new recorded code
   version. Regenerate the affected summaries, validity markers and tables;
   preserve the original results as provenance. No broader experiment or
   new scientific comparator is needed for this correction.
3. Strengthen the base auditor and bind reporting to current verified
   inputs. Add the demonstrated mutation checks as regressions.
4. Include the full-data application in the reproducibility materials and
   replace stale README instructions. Rebuild and test the delivery bundle
   after scientific outputs and manuscript references are updated.

The current large-sample bias, direction-reversal and power findings remain
supported by the checks performed. The unresolved numerical validity bug
does mean that the small-sample tables and curves should be repaired before
the final submission is described as fully checked.

## Audit Evidence

The adjacent `CODE_AUDIT_2026-10-17/` directory contains:

- `function-coverage.json`: reviewed function locations and source hashes.
- `numerical-audit.json`: independent numerical checks and scalar-record
  near-zero screening.
- `degeneracy-impact.csv`: exact-degeneracy and transposition impact by
  core setting. One additional row has a transposition issue without a
  degenerate component currently counted valid; there are 29 rows but 28
  settings with currently valid exact-zero components.
- `exploratory-degeneracy-impact.csv`: affected practical subset settings.
- `integration-audit.json`: raw-audit outcomes, current-manifest check,
  mutation findings, application verification and bundle omissions.

Diagnostic rates in this report have not been substituted into the thesis
or saved result directories.
