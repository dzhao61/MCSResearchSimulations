# Narrative Review

11 October 2026. Review of the active thesis before further editing.

## Overall Assessment

The thesis has a coherent overall argument, but several passages still make
the reader carry more information than the current question requires. The
remaining problem is mainly sequencing and repetition, not a lack of
explanation or a need to replace the whole structure.

The central argument is straightforward: compare population MI using sampled
tables; define the Normal Wald baseline; derive MI-specific degrees of freedom
for Expanded Welch; test its false-positive rates and power; explain where
estimation errors undermine both tests; draw practical conclusions and identify
future work. The chapters broadly follow that sequence. Some paragraphs take
unnecessary detours within it, particularly when supporting checks interrupt
the explanation of a primary result.

The earlier preference can be described as **direct, mechanism-led exposition
with a continuous logical chain**. Each passage should answer the question the
reader currently has, explain the quantity that changes and its consequences,
and introduce the next question only when the present one is resolved. The
goal is lower reader workload, not fewer words at any cost.

Several improvements from earlier sessions are working well:

- The Introduction moves from one computing example to sampling variation,
  the equal-MI hypotheses, Wald and Expanded Welch. It does not need another
  wholesale rewrite.
- Section 2.3 and the central Chapter 4 derivation explain the mathematical
  operations rather than merely naming them. Their useful intermediate steps
  should remain.
- The copying construction now has an explanation before its numerical example.
  The example develops the method instead of presenting unexplained matrices.
- The main figures answer identifiable questions and receive interpretation
  beside their evidence. The problem is no longer an aimless catalogue of plots.
- The shopping application is largely self-contained, and the Conclusion
  clearly separates contributions, limitations and future work.

I did not find a remaining pattern of manuscript references to version control,
frozen protocols, saved-file inventories or rounding assurances. The most
noticeable residual padding is scientific framing repeated after the point has
already been explained. Runtime environment details are a separate placement
issue: they have a reproducibility purpose and should not simply be deleted.

## Recommended Changes

### 1. Complete Each Explanation

**High priority.** In Section 6.1.2, the copying-population bias is explained,
then the four-cell construction is introduced, then the text returns to the
copying population's inaccurate standard error. A reader has just learned why
the estimated difference is shifted and is ready to ask whether its uncertainty
is also wrong. The construction change intervenes before that question is
answered.

Locations: [bias explanation](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:107>),
[construction check](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:131>) and
[return to uncertainty](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:141>).

Finish the copying explanation first: difference bias, standard-error error,
and improvement with more observations. Then give the construction check as
corroborating evidence. Preserve its finding; change where it appears.

A similar interruption occurs in Section 6.3.1. The text explains wrong-direction
rejections under copying, inserts exact four-cell rejection counts, then returns
to the larger-sample copying result. Complete the small-sample versus
large-sample story before adding the supporting construction result. The
jackknife paragraph is relevant because it answers whether changing the MI
estimate helps; keep it brief and explicitly connected to that question.

Location: [wrong-direction and larger-sample results](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:300>).

### 2. Reduce Supporting Detail

**High priority.** Section 6.3.2 moves from margin-related power and precision
to the four-cell check, then to unequal allocation. The allocation paragraph
reintroduces its design and gives numerous null and alternative rates. Those
results matter, but their detailed treatment makes a section about margins
end as a section about sample allocation.

Location: [supporting checks after the margin comparison](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:366>).

Keep the main-text conclusion: allocating fewer observations to Q lowers power
in this comparison, and Expanded Welch still lowers already-conservative null
rates. Give one illustrative comparison if needed and point to Appendix C.6
for the other numbers. Likewise, shorten the four-cell summary to its substantive
finding rather than restating what agreement between constructions permits us
to claim. This retains both checks without making them competing main studies.

Chapter 5 also introduces the jackknife between the definitions of estimation
diagnostics and the degrees-of-freedom summaries. Put its short introduction
beside the other supporting checks, or after the diagnostic definitions are
complete, rather than splitting that explanation.

Location: [jackknife pointer within diagnostics](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:304>).

### 3. Consolidate The Gap

**Medium priority.** Section 2.5 repeatedly explains that the remaining task is
to calculate how the estimated MI variance changes, use that variability to
choose degrees of freedom, and compare the resulting test with Wald. The
paragraph beginning "A new observation changes..." repeats the preceding
paragraph's contribution rather than advancing it.

Location: [Section 2.5](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:675>).

Consolidate the repeated explanation while preserving three distinct points:
what prior work supplies, the MI-specific calculation this thesis adds, and
why the experiment must examine the shared MI estimates as well as rejection
rates. The distinction between sampling variance and variability of its
estimate is important; it does not need to be introduced several times in
the same closing passage.

### 4. Delay Result Previews

**Medium priority.** The regression-precedent paragraph in Section 2.4 jumps
from explaining prior variance corrections to the thesis's small-MI diagnostic
result: the plug-in standard error overestimates observed variance and the
larger cutoff makes rejection still more conservative. The reader has not
yet reached the experimental design or the figure behind this comparison.

Location: [regression precedents and result preview](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:564>).

Keep the literature explanation and the reason the principle is relevant to
MI. Leave the measured overestimation and its interpretation in Chapter 6.
If a bridge is needed here, state the question: whether the larger cutoff
improves the MI comparison depends on the estimation errors present. This
keeps the motivation without asking the reader to absorb a result early.

### 5. Remove Repeated Motivation

**Medium priority.** The second study is specified in one paragraph and then
largely explained again in the next. "Repeating this sweep... separates the
effect of common population MI from a change in sample size" is followed by
"Holding table size and margins fixed shows how... change with population MI"
and another explanation of the two sample sizes. These are descriptions of
the same controlled comparison.

Location: [population-MI study](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:173>).

State the settings once, then use the remaining explanation for the substantive
reason for the sweep: small positive MI approaches the region where first-order
variance becomes small, while larger MI tests behaviour away from it. Do not
shorten the actual parameter grid or remove the positive-MI boundary condition.

There is similar repetition in the power-study rationale: the connection to
the null settings and the purpose of retaining the zero point are both
explained more than once. Keep one explanation of each. The generic sentence
"Holding the other stated factors fixed makes each change easier to interpret"
in Section 5.1 adds little beyond the concrete design that follows.

Locations: [power-study rationale](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:201>) and
[generic design framing](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:20>).

### 6. Separate Chapter Roles

**Medium priority.** Section 7.1 retells the larger-cutoff mechanism, unequal
bias, validity versus calibration, and interpretation of p-values. These
points are necessary, but most have just received detailed explanation in
Chapter 6. The first part of the Conclusion then revisits several again,
including repeated reminders that a cutoff does not change the shared estimates.

Locations: [Section 7.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/07_discussion.tex:6>) and
[concluding findings](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/08_conclusion.tex:18>).

Give the chapters distinct jobs. Chapter 6 explains observations and mechanisms;
Chapter 7 draws together practical recommendations and limits; Chapter 8 states
the contribution, answer and next steps. Condense the re-teaching in Section
7.1, preserving its advice on reporting estimates and uncertainty. In the
Conclusion, retain the firm recommendation but state the unchanged-estimates
point once. Conventional summary across chapters is appropriate; repeatedly
rebuilding the same explanation is not.

### 7. Remove Corrective Framing

**Medium priority.** Some sentences still defend against stronger claims or
reader mistakes that the surrounding passage has not invited. These are good
candidates for deletion or direct, positive wording:

- Section 2.4 says that computational cost alone does not establish statistical
  preference after noting bootstrap cost. The useful issue is its inability
  to sample unobserved cells. Keep that explanation; omit the aside about how
  a method must be judged. [Source](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:654>).
- Section 5.4 says copying creates dependence within an observation, "not
  between the two population samples." The construction and independent
  sampling have already been stated. State the independent sampling directly
  without another correction of this possible misunderstanding. [Source](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:263>).
- Section 6.3.2 ends the precision explanation with "This connects the margin
  comparison to the first-order MI variance..." The preceding sentences already
  explain how probabilities change precision. This final sentence comments
  on the explanation rather than adding to it. [Source](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:348>).
- The four-cell summary says that the main curves "retain their specific copying
  populations." Report the observed agreement at the matched settings instead
  of adding this reassurance about scope. [Source](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:366>).
- Appendix C.5 repeatedly contrasts supporting agreement with "identical
  performance under every association pattern" or "identical performance across
  constructions." Nobody has claimed universal identical performance. State
  positively that the qualitative failure persists while numerical power
  differs; retain the evidence and its actual scope. [First passage](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:314>),
  [second passage](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/C_additional_results.tex:360>).

The final application sentence about "not causal effects of visit timing"
is a lower-priority example. No causal argument is being developed. A concise
positive description of the findings as associations in the recorded sessions
would keep the interpretation bounded without introducing causality as a new
topic. [Source](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:512>).

### 8. Reduce Numerical Burden

**Medium priority.** The abstract introduces different-skew copying tables,
the four-cell construction, exact rates, validity, sample sizes and direction
reversal in one results paragraph. Several of those construction names are
unexplained at this point. The important finding is that unequal sparse-table
bias can create false positives and reverse the estimated ordering, and that
Expanded Welch does not fix this.

Location: [abstract results paragraph](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/frontmatter/abstract.tex:25>).

Keep the finding and its tested scope, but reduce unexplained construction
detail and numerical enumeration. One headline result is sufficient if a
number is retained. This is not a recommendation to hide the negative result
or claim that it holds for all sparse tables.

Section 6.1.1 also gives two rates, their two individual intervals, the paired
difference and its interval, then four more large-sample rates in one paragraph.
Keep the headline comparison and useful uncertainty for its interpretation;
put redundant numerical detail in the existing supporting results. A precise
argument does not require reading every table entry aloud.

Location: [large-table false positives](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:51>).

### 9. Relocate Timing Details

**Lower priority.** Section 6.4 opens with OS and library versions, warm-up
counts, timed passes and call ordering before discussing the result. These
are legitimate scientific details, but they interrupt the results narrative.

Location: [timing procedure](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:391>).

Keep the timing table, units, main sampling conditions and interpretation in
Chapter 6. Move the detailed environment and measurement procedure to Appendix
B with a brief pointer. Preserve absolute cost and the complexity explanation:
they are relevant to a computer-science thesis. Do not delete reproducibility
information merely because it resembles administrative detail.

### 10. Group Appendix Topics

**Lower priority.** Appendix A.5 concerns combined degrees of freedom with a
zero variance estimate, but its final mini-heading introduces numerical
derivative checks. That verification is useful, but it is not part of the
zero-component argument.

Location: [numerical derivative checks](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/appendices_rewrite/A_derivation_details.tex:267>).

Give the verification its own small section or place it beside the sensitivity
calculation it checks. Keep the zero-component limitation where it is: it
affects which results the method returns and is not disposable pedantry.

## Preservation And Scope

The recommended pass should preserve the following material:

- The Section 2.3 derivation, Chapter 4's essential intermediate algebra and
  the worked count-table example. These reduce mental reconstruction, even
  though they occupy space.
- Scientific assumptions, the distinction between exact derivatives and
  sampling approximations, and the near-independence limitations. Direct
  prose must not turn an approximate test into an exact one.
- Valid-result frequency and the unconditional rejection denominator. Failed
  calculations can lower reported rejection, so this distinction changes
  how readers interpret the figures.
- The fixed-nominal-threshold qualification for power, and the distinction
  between two-sided rejection and correct estimated direction.
- The jackknife's unchanged standard error and cutoff. Without this detail,
  the reader could mistake it for a validation of a complete jackknife test
  or jackknife Expanded Welch method.
- The application's sample definitions, category construction and six-comparison
  selection disclosure with Holm adjustment. These affect reproduction and
  interpretation; they are not file-management administration.
- The full parameter grids, numerical validity rules and supporting evidence
  in the appendices. Their greater detail is appropriate there.

The most valuable changes are to the Chapter 6 sequence and the repeated
motivation in Chapters 2 and 5. Follow those with a restrained sentence-level
pass and a shorter synthesis in Chapter 7. Do not add new experiments, symbols
or explanatory sidebars, and do not shorten paragraphs simply to make them
look concise. A slightly longer connected explanation is preferable to several
short corrective statements.

Only this review file has been added. The manuscript, PDFs, project goals and
historical working drafts have not been edited for this review. This report
evaluates narrative and reader workload, not a new mathematical or citation
audit.
