# Focused large-table construction check

Approved 10 October 2026. Keep Normal Wald and Expanded Welch as the only
methods. Do not restore the old broad design or expand the mathematical
derivations merely to strengthen the marking case.

## Question and fixed scope

Does the sparse 16 x 16 different-skew failure seen under copying persist
when association is concentrated in the first four cells instead?

- Four new settings: 16 x 16; P margins m_16(0.7), Q margins m_16(0.8),
  identical row and column margins within each population.
- MI pairs (0.02, 0.02) and (0.02, 0.03) nats, each at equal sample sizes
  1000 and 10000.
- Use the existing first-block four-cell transfer and target-MI search.
  Match margins, MI targets and sample sizes to the four copying comparisons.
- 20000 repetitions per new setting, independently sampled between
  constructions. Apply both unchanged methods to each sampled pair.
- Preserve the original focused-study and allocation records. Save this
  extension separately. Combined scope: 240 unique settings, 70 population
  pairs and 4800000 distinct sampled pairs.

This check addresses the null excess and the estimated direction at one
alternative. It does not test the full shape of the detection curve or every
possible arrangement of association.

## Measures and interpretation

Report all eight matched comparisons, irrespective of their results:
unconditional rejection with Wilson intervals, validity, difference bias
and its Monte Carlo standard error, observed SD, estimated/observed variance
ratio, and opposite-sign rejection counts and fractions for the alternative.
Retain paired within-method contrasts in the experimental records.

If the failure persists, describe agreement at these matched settings. If
the pattern changes, explain the dependence on association arrangement and
narrow the practical interpretation. Do not require identical rejection
rates across constructions with different probability tables.

## Manuscript and verification

1. Add the exact construction and four new settings to Chapter 5 and
   Appendix B, retaining a readable general first-block transfer formula.
2. Put one compact comparison table and interpretation in Appendix C, and
   discuss its implication beside the main sparse-table result.
3. Sharpen the contribution statements and conclusion: distinguish the
   automatic rejection reduction from the measured calibration, bias and
   direction findings. Keep mathematical originality bounded to the
   MI-specific sensitivity and its use in the established framework.
4. Check each research question against its explicit answer and supporting
   evidence. Do not turn the limited comparisons into universal sample-size
   advice or claims of a generally superior test.
5. Test scope, population reconstruction, fixed-stream batching/resume,
   summaries, direction counts and generated table. Independently audit
   all raw outputs and regenerate sampled inputs.
6. Build and visually inspect the revised PDF; refresh and independently
   verify its source and supplement packages. Preserve all older working
   drafts, original statistical code and original records.

## Examiner-focused consistency check

| Claim or question | Evidence and location | Judgement |
| --- | --- | --- |
| RQ1: derive MI-specific degrees of freedom | Chapter 4 sensitivity and first-order variance calculation, worked example, Appendix A and derivative tests | The contribution is the MI-specific input, not invention of Welch--Satterthwaite theory or exact Student t calibration. |
| RQ2: useful improvement over Wald | Chapter 6 null and alternative comparisons, validity, diagnostics and paired differences; Chapters 7-8 answer | No general replacement is supported; reducing rejection is distinguished from improving calibration. |
| Large-table estimation failure | Chapter 6 bias/direction evidence and Appendix C matched construction table | Positive difference bias, null excess and opposite estimated direction occur under both tested constructions at n=1000. |
| Dependence on population structure | Different margins/sizes in the main studies and changed detection under the matched construction | Matching MI and margins does not match sampling precision; no universal sample-size threshold is claimed. |
| Originality and citations | Sections 2.4-2.5 identify MI variance and entropy/regression precedents; Chapter 4 locates the remaining calculation | Existing verified sources suffice for the targeted edits. No new global-priority or causal-share claim is introduced. |
| Reproduction and scope | Chapter 5 and Appendix B give both constructions, exact grids, estimators, validity and uncertainty rules | 240 settings, 70 pairs and 4800000 distinct samples agree across active manuscript statements. |

The four-cell null rates at n=1000 are 0.30945 and 0.29770. At the
alternative, opposite-sign counts are 2493/2494 for Wald and 2350/2351
for Expanded Welch. At n=10000 the four-cell null rates are 0.04990 and
0.04910 and all alternative rejections have the correct sign. Detection
differs between constructions (Wald 0.69920 versus 0.63230), consistent
with a change in observed sampling precision. The interpretation reports
both the agreement and this difference.

Status: implementation, scientific checks and rendered-page review complete.
All 179 workspace tests and three raw-record audits pass. The PDF has
93 pages with 54 main-text pages. Package verification is recorded in
SUBMISSION_CHECK.md. Original study/method hashes and all older working
drafts are unchanged.
