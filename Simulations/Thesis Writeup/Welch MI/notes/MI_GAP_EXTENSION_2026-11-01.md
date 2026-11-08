# Power study at three absolute MI gaps

Authorised on 1 November 2026 after the fixed-gap PDF rebuild. The user
requested additional MI differences while retaining a simple experiment.
This source/experiment update does not itself request another thesis build.

## Design fixed before running

- Keep I(P) = 0.02 nats. Use I(Q) = 0.025, 0.03 and 0.04 nats, giving
  gap magnitudes 0.005, 0.01 and 0.02 and signed Delta = -0.005, -0.01,
  -0.02 nats. Describe Delta and its magnitude explicitly to avoid a sign
  ambiguity. No fitted-SD scale or calibrated rejection thresholds.
- Apply every gap to all four table sizes, three margin profiles and ten
  sample sizes already used in the broad null and fixed-gap studies.
- 360 settings at 100,000 repetitions each: 36 million distinct table pairs.
  Reuse the verified 12 million pairs at gap 0.01 without copying or changing
  their raw records. Run 24 million new pairs at the other two gaps.
- Same copying construction, MI/margin/positivity tolerances, production
  estimates and validity rules, 0.05 nominal thresholds and all-repetition
  denominators. Both methods use the same pair of tables in each repetition.
- Retain PCG64 master seed 20261101 and setting/chunk/population streams;
  different gap-specific population/setting IDs separate the new streams.
- Preserve the previous runner/results/figures and all historical archives.
  Use a separate extension runner, output directory, combined summaries and
  explicit provenance for the reused gap.

## Display and interpretation

Keep the logarithmic sample-size axis and four table-size panels. Each
margin regime receives one figure showing all gaps and both methods.
Use three colours for gap magnitude and solid/dashed lines for methods,
with separate, explicit legend keys. Keep readable labels and validity
strips. If six curves prove hard to follow, split the display without
shrinking its labels; do not select favourable settings or gaps.

Interpret the effects of increasing sample size, changing the gap and
changing methods separately, then explain any interaction through the
sampled centre, spread and rejection direction. Larger gaps need not give
larger two-sided rejection in sparse biased settings, since increasing the
negative population difference can offset positive bias. Verify actual
patterns before writing that explanation. Distinguish rejection under an
alternative from identifying its direction and compare power with the
existing null rejection results. Do not claim matched-size superiority.

## Checks and writing

Smoke-test boundary sample sizes before the full new run. Check exact grid
coverage for each gap, feasible positive populations, preserved margins and
target MI, independent scalar formulas, raw-checkpoint hashes, reused-data
identity, paired decisions and validity nesting, all denominators and Wilson
intervals. All three gaps must appear in the main figures and discussion.

Update RQ3 and Sections 5.4/6.3, parameter tables, abstract, conclusions,
Appendix B and current internal documentation. Replace one-gap limitations
and global numerical claims that no longer apply. Keep the discussion
focused on the scientific changes, with short captions and developed
paragraphs following the consolidated research-writing and results guides.
Keep near-independence, the broad null results, stronger-common-MI checks,
production estimators, earlier Chapter 4 edits and the presentation unchanged.

Prepare source/evidence packaging for the next requested rebuild. Check
active references, retired-study references, environments, figure files and
paragraph style. Render and inspect all three new figures. Do not overwrite
the already delivered 105-page thesis PDF until a rebuild is requested.

## Completion

Completed on 1 November 2026.

- The 72-setting, 14,400-pair smoke run passed before the full extension.
  The two new gaps ran at every grid setting: 240 settings and 24 million
  new pairs. Combined with 12 million reused pairs, the study has 360
  settings and 36 million distinct pairs. The runner and records are in
  `WelchSatterthwaiteMI/experiments/mi_gap_power_study.py` and
  `WelchSatterthwaiteMI/results/mi_gap_power_2026-11-01/`.
- The combined audit passed raw chunk hashes, population targets/margins,
  validity/rejection nesting and counts, original-evidence fingerprints
  and rate agreement, and independent scalar reconstructions for 2,880
  pairs. All 720 primary Wilson intervals were compared with SciPy's
  independent binomial calculation. No original raw records were altered
  or copied into the new output directory.
- Three replacement figures display every setting with colour for gap
  magnitude and line/marker style for method, with readable common axes,
  pointwise intervals and validity strips. All were rendered and visually
  checked. Existing one-gap figures remain preserved and unreferenced.
- RQ3, the introduction, parameter table, Sections 5.4/6.3, abstract,
  conclusions, Appendix B and current documentation now describe all three
  gaps. One-gap limitations and numerical claims were updated together.
- For uniform 4-by-4 populations at n = 2,500, Expanded Welch power is
  11.138% at gap 0.005 and 78.736% at gap 0.02. At n = 50,000, the
  smallest-gap power ranges from 79.866% to 96.470% across both methods
  and all populations; the larger gaps exceed 99.9% throughout.
- The sparse different-skew 16-by-16 comparison shows the opposite gap
  ordering at n = 1,000: Expanded Welch power is 16.114%, 9.662% and
  3.386% as the magnitude increases. Positive bias stays near 0.03 nats,
  so a more negative population difference moves the positive sampling
  centre towards zero. The discussion explains this behaviour and its
  later reversal rather than asserting that power must always rise with
  gap size.
- Twenty-six relevant statistical/manuscript tests passed, including
  combined-grid/figure coverage, unchanged reused rates and numerical
  manuscript anchors. Active references, retired-study references,
  environments, figure existence, paragraph style and diff checks passed.
- Source/evidence packaging includes the extension runner, tests, all new
  records and combined summaries, and the three new figures. No archives
  or thesis PDFs were rebuilt during this extension. The prior 105-page
  PDF and the presentation remain unchanged.
