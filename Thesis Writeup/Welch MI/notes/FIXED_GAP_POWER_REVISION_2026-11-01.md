# Fixed-gap power study and manuscript revision

Authorised on 1 November 2026. This replaces the submitted focused nominal
and calibrated power study with a direct counterpart to the broad null
comparison. Previous experiments, outputs and historical manuscripts remain
preserved. This instruction does not request a thesis PDF rebuild.

## Scientific question and fixed design

How often do the two proposed tests detect a population MI difference of
0.01 nats, and how does detection change with sample size, table size and
margin regime?

- Copying populations: I(P) = 0.02 and I(Q) = 0.03 nats; Delta = -0.01 nats.
- Table sizes: 2, 4, 8 and 16 categories per variable.
- Margins: uniform, same skew (0.8/0.8), different skew (0.7/0.8), using
  the existing margin profiles and construction tolerances.
- Equal sample sizes: 10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000,
  50,000 observations per population.
- All 120 combinations, with 100,000 independent sampled table pairs per
  combination (12 million pairs). No outcome-based selection or grid changes.
- Same two tables for both methods, the existing bias correction, standard
  error, validity rules and usual p-value threshold 0.05.
- Invalid calculations count as non-rejections. Show valid fractions
  separately, with pointwise Wilson 95% intervals for power.
- Fresh PCG64 streams, master seed 20261101, separated by setting, chunk
  and population. No fitting batches, empirical thresholds, fitted null SDs,
  standardised alternatives or calibration bootstraps.

## Interpretation fixed before the new run

The rejection nesting implies Expanded Welch cannot have higher nominal
power. Quantify the detection cost and its changes with sample size, alongside
the existing null rejection evidence. Do not describe nominal power as a
comparison at matched false-positive rates or infer general superiority.
Report nonmonotonic behaviour and severe failures if present. One absolute
MI gap and one direction define the scope; neither is a representative survey
of all alternatives.

## Implementation and checks

1. Add a separate runner and results directory, reusing the checked copying
   constructor and production statistical calculations. Keep old outputs
   immutable. Store populations, all configurations, random-stream identities,
   chunked scalar records, summaries and an evidence audit.
2. Before the full run, verify all populations are positive, have the required
   margins and MI, and exactly match Section 5.3's grid. Check smoke samples
   against independent scalar formulas and the validity/rejection nesting.
3. Run every setting. Verify checkpoints, denominators, Wilson intervals,
   paired decisions, all-repetition rates and independent scalar calculations.
4. Plot all three margin regimes with the same four table-size panels and
   sample-size axis. Retain readable labels and validity strips. Include all
   regimes in the submitted results rather than selecting the best curves.
5. Explain only patterns supported by the new records. Use bias, sampling
   spread and rejection-direction summaries to check an explanation when a
   curve's shape requires them, without creating a new diagnostic study.

## Manuscript changes

- Chapter 1: change RQ3 to power at a fixed MI gap; remove calibrated-power
  contributions. Keep the mathematical contribution and full null findings.
- Chapter 5: replace Section 5.4 with purpose, fixed alternative, shared grid,
  rejection rule and interpretation alongside false positives. Add the power
  row to the parameter table. Remove fitting/evaluation batch taxonomy and
  calibration-specific performance measures and uncertainty.
- Chapter 6: replace Section 6.3 completely with the new full-grid findings;
  introduce each figure and explain it before switching regimes. Remove all
  calibrated power curves, contrasts and validation results. Keep Section 6.2's
  stronger-common-MI evidence; its tested populations need to be specified
  independently of the removed fitted-SD design.
- Chapter 7 and abstract: replace old power findings with verified new ones;
  state the fixed gap and joint interpretation with false-positive rates.
- Appendix B: remove alternative construction from fitted SDs, empirical
  calibration and bootstrap rules. Retain construction, validity and uncertainty
  required by the remaining studies. Specify the two scientific seeds.
- Keep A/B/C only where needed for the existing null diagnostics; define their
  settings there and give stronger-common-MI values directly. Remove references
  to deleted power-setting tables and equations.
- Update active writing-guide mappings; preserve old examples as historical
  lessons rather than instructions to restore calibration.
- Preserve the user's presentation PDF and prior Chapter 4 edits.

## Writing and acceptance

Follow the consolidated prose guide and Chapter 6 interpretation guide:
introduce settings and axes before interpretation, complete one comparison at
a time, connect observations to their supported explanation, name referents,
keep necessary short definitions and avoid numerical inventories or repeated
caveats. Use concise captions and ordinary body paragraphs for interpretation.

Check all active TeX inputs for stale calibration/fitted-SD references and
undefined labels, confirm preserved sections and previous edits, run paragraph
style checks and relevant statistical tests, and visually inspect new plots.
Leave main.pdf and named deliverables unchanged until a rebuild is requested.

## Completion record

Completed on 1 November 2026.

- `experiments/fixed_gap_power_study.py` ran all 120 settings and 12 million
  table pairs. Raw scalar records and independent streams are preserved in
  `WelchSatterthwaiteMI/results/fixed_gap_power_2026-11-01/`.
- A 36-setting smoke run passed before the full run. The full audit passed
  population/MI/margin checks, chunk hashes/dimensions, probability formulas
  reconstructed independently for 960 table pairs, variance/difference
  identities, validity rules and rejection nesting. All 240 primary rate
  intervals were checked against SciPy's independent Wilson calculation.
- Three plots cover all 120 settings, with readable common power scales,
  pointwise intervals and validity strips. All three PDFs were rendered and
  visually inspected. They preserve the null figures' panel geometry.
- Chapter 5's design, shared evaluation and parameter grid were simplified;
  Chapter 6.3 was rewritten around uniform, same-skew and different-skew
  margins. RQ3, the introduction, abstract, conclusions and Appendix B now
  describe the fixed-gap study. Both favourable calibrated gains and adverse
  calibration sensitivity were removed together.
- At n = 10,000, observed method power gaps are 0.076--0.313 percentage
  points; at n = 50,000, observed power is at least 99.959% for every method
  and population pair. The large-sample gap is small, but this does not
  establish power superiority at matched false-positive rates.
- The different-skew 16-by-16 case at n = 1,000 has difference bias
  0.0306714 nats against true Delta = -0.01. Expanded Welch rejects 9,662
  times, of which 9,659 have the wrong positive sign. The manuscript explains
  this fact and the later dip rather than presenting early rejection as
  reliable directional discrimination.
- The near-independence/RQ1 results and Appendix A, all existing null
  diagnostic and stronger-common-MI tables, production estimators, historical
  results and the user's presentation PDF remain unchanged by this pass.
  The earlier approved Chapter 4 edits are preserved.
- The previous focused/calibrated passages are preserved in
  `notes/PRESERVED_FOCUSED_POWER_PASSAGES_2026-11-01.md`; old experiment
  code, output records and figure assets remain intact.
- Nineteen relevant statistical/manuscript tests passed. Active TeX input,
  reference, label, environment, figure-existence and retired-study checks
  passed. Paragraph-style and `git diff --check` passed. A forward reference
  to undefined setting B was replaced by its sample size after deleting
  the old power-setting table.
- Source and evidence packaging now include the new figures, runner, tests
  and results. The initial source pass left archives and PDFs unchanged. The subsequent
  requested rebuild on 1 November produced the 105-page main/named PDF and
  refreshed both archives and checksums. Compilation and reference checks
  passed without warnings; 34 changed or boundary pages were rendered and
  visually checked. An independent build of the 100-file source archive
  reproduced the main PDF's extracted text and page breaks exactly.
- The user's existing presentation still reflects the previous power study;
  it was not edited by this task.
