# Balanced RQ2 design and results revision

Authorised on 1 November 2026. Replace the submitted RQ2's baseline-plus-
follow-ups presentation with a balanced common-MI grid. Preserve existing
experiments and evidence internally. This task does not request a PDF build.

## Scientific design fixed before the new run

Question: how close are the tests' false-positive rates to 5% as sample
size, table size, margin regime and the common population MI change?

- Equal MI: I(P) = I(Q) in {0.005, 0.02, 0.30} nats; Delta = 0 throughout.
  These levels cover weaker association, the baseline of the power study,
  and stronger association near the previous 0.28/0.33 checks. Confirm all
  targets lie inside every copying population's feasible MI range.
- All four table sizes (2, 4, 8, 16 categories), all three margin profiles
  (uniform, same skew 0.8/0.8, different skew 0.7/0.8), and the existing
  ten equal sample sizes (10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000,
  50,000) at each MI level: 360 settings, 100,000 repetitions each.
- Reuse the 120 existing common-MI-0.02 settings without changing or copying
  raw records. Sample 240 new settings (24 million new pairs), giving
  36 million distinct pairs in the combined null study.
- Same copying constructor, target/margin/positivity tolerances, production
  statistical calculations, 0.05 nominal thresholds and validity rules.
  Both methods use the same two sampled tables in each repetition.
- Invalid results count as non-rejections; show valid fractions separately.
  Use pointwise Wilson 95% intervals. No fitted cutoffs, size matching,
  additional constructions or outcome-based screening.
- New records use PCG64 seed 20261101 with setting/chunk/population streams;
  reused records retain seed 20261021 and their original stream identities.

## Presentation and evidence

- Three figures: uniform, same-skew, different-skew. Use the power figures'
  sample-size axis and four table-size panels, with colour for common MI
  and line/marker style for method. Draw the 5% reference and validity
  strips. Include every setting, all conspicuous failures and full ranges.
- Retain only one short diagnostic comparison in the main results. Select
  its three existing common-MI-0.02 cases now, from the established mechanism
  evidence: uniform 4-by-4 at n=20; same-skew 16-by-16 at n=1,000;
  different-skew 16-by-16 at n=1,000. They illustrate underestimated variance,
  overestimated variance without appreciable bias, and difference bias.
  They are explanatory examples, not a representative performance sample.
- The diagnostic table names settings directly and combines Bias/SD,
  average SE-squared / observed difference variance, and both rejection
  rates. Explain the quantities and unpack the three mechanisms locally.
- Retire the A/B/C narrative, separate stronger-common-MI follow-up, large
  case-rate table and threshold-based closer/farther count table from the
  submitted results. Preserve their original evidence and passages.
- Remove the detailed rank-correlation investigation and step-by-step
  account of every shoulder/trough from the main narrative. Keep the broad
  patterns and supported explanations without claiming a complete causal
  decomposition of each finite-sample feature.

## Implementation and verification

1. Add a separate null runner and output directory. Reuse the tested
   production sampler/summariser; preserve previous runner fingerprints.
2. Smoke-test all new MI/size/profile combinations at boundary/intermediate
   sample sizes. Check populations, independent scalar formulas and masks.
3. Run all new settings; audit raw hashes, dimensions, scalar calculations,
   validity/rejection nesting and denominators. Reconstruct the original
   null records from their original streams and verify reused rates.
4. Combine summaries with explicit source provenance; validate all 720
   primary Wilson intervals independently and check complete grid coverage.
5. Render and inspect all three plots. Keep labels readable; use consistent
   scales within comparisons and state scale changes if necessary.
6. Rewrite Section 5.3 and its grid table; replace Section 6.2 with three
   margin subsections and one compact mechanism subsection. Keep stable
   cross-reference aliases needed by the power discussion where appropriate.
7. Update RQ2, introduction, abstract, conclusions and Appendix B to the new
   study. Remove claims based on retired display counts/selected follow-ups.
   The historical stronger-MI evidence remains preserved, not hidden by a
   general claim of validity at other untested MI values.
8. Reconcile Section 6.3's references to the new null figures/diagnostics
   without changing the completed power experiment, values or conclusions.
9. Update source/evidence packaging inventories and current documentation,
   without rebuilding archives or PDFs until explicitly requested.
10. Check statistical tests, all active references/figures/environments,
    retired-study references and paragraph style. Confirm RQ1, Appendix A,
    Chapter 4, power records/plots and application are preserved.

## Writing standard

Follow the consolidated prose and Chapter 6 results guides. Introduce the
question, fixed/changing populations and plot encodings before interpretation.
Complete one margin comparison at a time. Explain the main direction of the
method effect, broad common-MI/sample-size patterns and important exceptions.
Use named quantities and connected explanatory sentences; retain necessary
short definitions. Keep captions descriptive and put settings/interpretation
in body text. Choose a few useful numerical anchors, not a prose inventory
of every curve. Distinguish matching 5% from simply lowering rejection.

## Completion record

Implemented on 1 November 2026.

### Experiments and evidence

- Added `WelchSatterthwaiteMI/experiments/balanced_null_study.py` without
  changing the existing sampling runners. All targets are feasible and
  all constructed cells positive, with the required margins and MI.
- The smoke run covered 72 new boundary/intermediate settings with 200
  pairs each. Independent reconstruction checked 576 pairs.
- The full run completed all 240 new settings at 100,000 pairs each.
  The combined study has 360 settings and 36 million distinct pairs:
  24 million new pairs and 12 million reused original pairs.
- `results/balanced_null_2026-11-01/combined_audit.json` passes. It checks
  original population arrays, source/seed identities, raw hashes,
  unchanged original rejection/validity counts, paired nesting and
  denominators. The combined audit independently reconstructs 2,880
  pairs using scalar formulas. All 720 primary Wilson intervals also
  agree with independent SciPy calculations.
- All 360 settings appear in the three new figures. There is no
  selection based on the newly observed rejection rates. The three
  mechanism examples are the existing cases specified above before
  sampling. Older results and exact preceding RQ2 passages are preserved;
  see `PRESERVED_RQ2_PASSAGES_2026-11-01.md`.

### Resulting manuscript

- Section 5.3 states the question, three common MI levels, full grid,
  paired sampling and rejection/validity measures. The design table
  includes the null grid explicitly. The equal-sample-size bias-correction
  paragraph now sits with the shared evaluation rules because it also
  applies to power.
- Section 6.2 follows uniform, same-skew and different-skew margins,
  then explains the main estimation errors in one compact subsection.
  The three figures share sample-size axes, method styles and common-MI
  colours. Scales are consistent across margin figures for each table
  size. One three-row diagnostic table replaces the larger case tables.
- The text retains severe failures. At common MI 0.005 in different-skew
  16-by-16 tables with n=1,000, Wald rejects in 36.38% of repetitions
  and Expanded Welch in 34.38%, despite complete validity. At the same
  common MI and n=50,000, both methods remain below 4% in all three
  16-by-16 margin regimes. The narrative distinguishes method agreement
  from correct calibration and explains why simply lowering rejection
  can worsen conservative results.
- Removed the main-text A/B/C narrative, tolerance-based improvement
  counts, separate stronger-common-MI follow-up, rank-correlation
  investigation and detailed account of individual shoulders. Essential
  variance/bias explanations remain beside their evidence.
- Introduction, abstract, RQ2 conclusion and Appendix B agree with the
  new design. The Chapter 6 guide records the new organisation. The
  existing power discussion retains its resolved reference to the compact
  mechanism subsection, with its experiment and source text unchanged.

### Verification and build boundary

- All 32 tests across the balanced-null, MI-gap-power, fixed-gap-power,
  approximation-redesign and thesis-consistency suites pass.
- Active-source checks pass for 18 TeX files: 137 unique labels, 160
  resolved references, 46 resolved citation keys and 10 existing figures.
  Braces and environments balance, and retired RQ2 labels are absent.
  The shared paragraph-style check passes.
- All three final figure layouts were rendered and visually inspected.
  The diagnostic table was compiled separately using the thesis preamble
  and inspected; every setting fits on one line, with no overfull boxes.
- Read-only packaging checks find 111 source files and 37,649 experiment
  files, all existing with unique archive paths. The inventories include
  the new runner, tests, combined evidence, plots and table.
- SHA-256/source comparisons confirm Chapter 4, Appendix A, RQ1
  (including near-independence), the Chapter 6 power section, application,
  main PDF and named thesis PDF are unchanged by this revision.
- The main/named thesis PDFs and delivery archives were not rebuilt.
  The latest 105-page PDF predates both the MI-gap extension and this
  RQ2 revision. A future explicit rebuild must include both source changes
  and inspect their final page breaks and display placement.
