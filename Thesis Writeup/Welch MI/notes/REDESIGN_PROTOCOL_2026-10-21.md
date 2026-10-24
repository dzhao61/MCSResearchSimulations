# Independent approximation and test redesign

Status: fresh simulation, independent audit, calibration bootstrap and manuscript rewrite complete on 22 October 2026; delivery verification complete.

All work is confined to the independent Welch MI Redesign 2026-10-21 copy. Original input hashes are recorded in ORIGINAL_FILES_SHA256.json at the copy root. The original folders and historical working drafts are preserved.

## Scientific scope

RQ1 measures mean and sampling variance accuracy for Vhat, population versus sampling-moment degrees of freedom, the plug-in estimates, and Appendix A.4 predictions. RQ2 compares false positives and nominal/calibrated power with the shared statistic.

Rerun all 312 existing configurations, add the complete 63-point MI sweep (30 additions), and add 24 nonzero SD-scaled power settings. Final scope: 366 evaluation settings, 186 independent null fitting settings, 100,000 pairs each. Total 55,200,000 pairs, excluding technical pilots.

The broad null grid remains 120 settings at common MI .02; the expanded 4x4 MI sweep crosses all three margin regimes, all seven existing MI values and n=100/1000/10000. The focus nulls are A:4x4 uniform n20; B:8x8 different-skew n100; C:4x4 different-skew n10000. Power differences are 0,.5,1,1.5,2,2.5,3,3.5,4 null SDs, keeping I(P)=.02 and increasing I(Q).

Four rules: normal Wald; sample-size df using n_i exactly; unchanged Expanded Welch; fixed independently fitted null moment reference. Keep each null reference fixed across its alternatives. Fit empirical p thresholds for variable-df rules and a common absolute-T threshold for Wald/reference. Strict inequalities exclude boundary ties. Fresh null evaluation validates attained levels.

Finite zeros belong in variance moment calculations. Positive-finite df summaries report their inclusion counts. Report all-attempt, method-valid and four-method common-valid rates. All within-setting method differences are paired. Bootstrap 1,000 fitting/evaluation-output repetitions for focused calibrated-power uncertainty. Effects in nats stay fixed. Practical power tolerance: one percentage point, with pointwise intervals.

Do not assume the mean bias coefficient equals d away from independence, identify large kappa/d as a general failure condition, or interpret replacing random df by fixed df as isolating estimation error. Correlation/shape/bias diagnostics describe mechanisms without establishing isolated causal contributions.

## Implementation and delivery

New modules: redesign_study.py and redesign_report.py. Separate seeded streams for pilot, fitting and evaluation, immutable checkpoint identities, checksummed scalar records and independent reconstruction of count pairs. Technical pilot: 200 pairs per batch, all settings, 4,416 reconstructed pairs. Six new statistical/integrity tests.

Build the copied manuscript through Working Draft v3.tex and the copied package_deliverables.py, delivering Working Draft v3.pdf and separate source/evidence archives. Preserve copied main.pdf and all historical working-draft PDFs. Rewrite Chapters 5/6, reconcile 1/7/8 and abstract, retain Section 2.3 and core derivations, update Appendix B and compact Appendix C. Refresh packages and verify both source and evidence.

## Verified outcomes

All 55.2 million planned pairs are complete. The audit passed, with 4,416 independently reconstructed pairs. A/B nominal rejection is reduced relative to Wald and the sample-size comparator, with a nominal power cost. After independent null calibration Expanded Welch has higher power along the selected A/B paths. B retains a falling-then-rising rejection curve. C calibrated differences are far within the one-percentage-point practical tolerance. The matched 16x16 failure persists under all four rules.

The original-file preservation check passed for all 30,042 recorded files. Section 2.3, Chapters 3/4, Appendix A, the copied main.pdf and historical working drafts remain byte-identical to their snapshots.

Three historical manuscript tests were updated to validate fresh table values and setting coverage; tests of the historical raw evidence remain. The jackknife check and original scalar timing evidence are explicitly identified as earlier separate investigations. One stale pre-copy prose test already referenced a removed appendix passage; it was replaced by fresh source-derived table and calibrated-equivalence checks.

## Final verification

After the full deliverable quality pass, 268 local tests pass (216 experiment, 27 estimator, 17 application, 8 packaging). The extracted delivered supplement and separately extracted thesis source pass 178 bundled tests (134 experiment, 27 estimator, 17 application). The complete fresh experiment audit remains valid: its statistical source, inputs and sampled records are unchanged by the reporting and manuscript work. The isolated source archive builds without warnings, with extracted text identical to the reviewed 109-page PDF. The delivery consistency check passes. REDESIGN_VERIFICATION.json at the copy root records these outcomes. DELIVERABLE_REVIEW_2026-10-22.md records the scientific exposition, uncertainty reporting, figure and discussion improvements made in the quality pass.


## Subsequent readability revision

The user requested a simpler experimental narrative after reviewing the full deliverable. READABILITY_REVISION_2026-10-22.md records the prior-session writing guidance, applied changes and final verification. The current PDF is 104 pages, with Chapters 5–7 reduced from 28 to 22 pages; the core theory and all experimental calculations remain unchanged. The 268 local tests, 178 bundled tests, isolated source build, PDF review and delivery consistency check pass.
