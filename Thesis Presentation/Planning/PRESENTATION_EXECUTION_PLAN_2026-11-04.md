# Presentation execution plan

Originally prepared on 4 November 2026. **Substantively replanned on
5 November 2026** following Daniel's preference for the supplied
*Comparing MI in Finite Samples* presentation. Keep this filename stable.
This revision replaces the 16-main-slide plan.
**Updated on 8 November 2026** to match the final thesis, and on
9 November 2026 to match the submitted version, to label the results
titles by research question, to remove the shopping application, and to
show the RQ2 and RQ3 results across the whole grid; Section 11 lists the
changes.

## 1. Execution brief and sources

Create **13 main slides, one appendix title slide and 16 backup slides**
(B1–B14, plus two B1 continuation slides), 30 slides in total. The
main talk targets **18:50**, leaving 70 seconds before the university's
20-minute limit. Keep Slide 13 visible during questions. Backups begin at
physical Slide 15, after the appendix title on Slide 14. The appendix title
and backups are outside the timed talk.

This is a substantive replan of the argument, figures and speech. Follow
the preferred deck's concrete opening, visible derivation chain and
results that place evidence beside its explanation. Use the current
thesis's balanced null and MI-gap power studies. Do not restore calibrated
power or discarded experiments.

**Editing boundary (confirmed 5 November 2026):** Daniel will edit the
presentation separately. Update this plan only; do not edit presentation
files, preview PDFs, speaker-note files, authoring code, evidence manifests
or presentation snapshots. The slide specifications below describe changes
for Daniel to make, not permission to implement them. Do not edit or rebuild
the thesis, run experiments or regenerate thesis figures.

All presentation files are in `/Users/danielzhao/MyMac/Masters Degree/Research/Thesis Presentation/`:
the current version at the top, this plan and its
manifest in `Planning/`, and the earlier versions in `Earlier versions/`:
`original_16_slide/`, `replanned_2026-11-05/` and its revisions
`replanned_2026-11-05_v2/` (appendix title), `replanned_2026-11-05_v3/`
(lighter formatting), `final_2026-11-08/` (matched to the final thesis),
`final_2026-11-08_v2/` (review revisions), `submitted_2026-11-09/`
(matched to the submitted thesis), `rq_labels_2026-11-09/`
(research-question labels), and `app_removed_2026-11-09/` (application
removed). Preserve the earlier versions. Until 8 November these lived in
`Thesis Writeup/Welch MI/presentation/` and `Thesis Writeup/Welch MI/notes/`.

Other project paths are relative to:
`/Users/danielzhao/MyMac/Masters Degree/Research/Simulations`.

| Authority | Source and role |
| --- | --- |
| Science | `/Users/danielzhao/MyMac/Masters Degree/Research/FINAL SUBMISSION/Daniel_Zhao_Welch_MI_Thesis.pdf`: submitted 111-page thesis, last built on 8 November 2026, SHA-256 `163f34b602bed9f868398a7175e0653a1882ea7658ca3b641a60c71141b54a59`. It is identical to `Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis_Signed.pdf`. |
| Primary presentation reference | `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/Comparing MI in Finite Samples.pdf`, 25 pages: 14 main slides, an index and 10 supporting pages. Follow its explanatory approach and visual hierarchy. |
| Editable design donor | `/Users/danielzhao/MyMac/Masters Degree/INFO5993/A4/Zhao_Daniel_Presentation_vF2.pptx` and matching PDF, 11 slides. Reuse original cover artwork and suitable editable styling. |
| Numerical evidence | `PRESENTATION_EVIDENCE_MANIFEST_2026-11-04.json`, version 2. Its filters, row counts and simulation values still apply. It predates the final thesis: its thesis hash is the 4 November build, its `backup_9_to_11` entries are now B10–B12, and its `backup_12` application entry, Holm values and six-comparison application rows are no longer used. B9 uses final Table 6.2. The deck no longer presents the application. |
| University requirements | `Presentation Marking Criteria.pdf`, `18cp Research Path deliverables.pdf` and `18CP Research Pathway Project Marking Rubric V3.pdf`, all under `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/`. |
| Scientific source | `Thesis Writeup/Welch MI/chapters_rewrite/`, `appendices_rewrite/`, `references.bib`. |
| Writing | `Thesis Writeup/Welch MI/notes/RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md` and `CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md` in the same folder. Use Australian English. |

The preferred 25-page PDF differs from the older PDF with the same name in
the thesis `deliverables/` directory. Neither supplies current experimental
authority. Exclude their fitted thresholds, calibrated-power gains, A/B/C
power-design narrative, four-cell check and obsolete summary counts.
Replace the old calibration sequence with current power and wrong-direction
results. Do not inherit old proposal notes, milestones or JIDT promises.
Do not run thesis plotting generators into their default destinations.

## 2. University requirements and coverage

The supplied documents specify up to **20 minutes of presentation**, with
interruption at 20 minutes, then up to **10 minutes of questions**. The
presentation contributes **20% of the project mark**. The audience includes
markers, the supervisor, academic staff and students. Upload PDF;
PowerPoint may be used live.

| Criterion | Weight | Coverage |
| --- | --- | --- |
| Motivation, objectives, literature, own method, results, evaluation, conclusion and future work | 30 | Slides 2–3 establish the question and foundations; 4–5 explain the method; 6 specifies evaluation; 7–12 develop the results; 13 applies the tests; 14 concludes and links future work to limitations. |
| Understanding, logic and answers | 20 | Defined quantities, visible mechanisms, matched comparisons and prepared backups/answers. |
| Pace and time | 20 | 18:50 including transitions and graph-reading pauses, with checkpoints and a shorter route. |
| Engagement and eye contact | 20 | Concrete example, purposeful pointing and rehearsal from cues rather than reading slides. |
| Fonts, colours and readability | 10 | Consistent hierarchy, simple method comparisons, readable charts and complete static PDF. |

The slide count and style are planning choices. No actual talk date,
current upload deadline or official slide master has been supplied. The
personal references are not verified university templates. Adapt to any
mandatory master supplied later; do not infer a talk date from the thesis
or revision date.

## 3. Lessons governing this revision

1. Open with two populations, their tables and estimates, and the
   population hypothesis on one page.
2. Make the literature explain what the method needs. Identify the
   MI-specific calculation without an unverified global priority claim.
3. Show relationships in the derivation before its final formula. Keep
   the expanded derivative in B1.
4. Give each result a complete explanatory point: setting, observation,
   mechanism and implication together. Necessary explanation stays visible.
5. Keep numbers beside their plotted point or table row. Avoid requiring
   recall of earlier values to understand a new comparison.
6. Keep main comparisons simple: stable method colours and one chart per
   result slide. Backups keep the full grids by margin regime.
7. Answer each research question across the whole grid. Show single
   settings only as highlighted examples within it, and report changes in
   both directions, never a favourable count alone.
8. Lower rejection follows from the cutoff. The experiments establish
   its magnitude, conditional accuracy, cost and remaining estimator errors.

The sequence is: the comparison question, literature, shared statistic, derivation,
evaluation, approximation limits, false positives, their mechanism, power,
wrong direction, conclusion and next steps. A separate agenda
or preparatory sampling-uncertainty slide would interrupt this sequence.

## 4. Design, evidence and language

Use the preferred 25-page deck's white backgrounds, black headings, orange
emphasis and pale explanation panels, with the lighter formatting adopted on
5 November. Each slide should look uncluttered: modest type sizes, generous
white space and few boxes. A short factual lead sentence establishes each
page's point. Matrices, diagrams and plots vary with their purpose.
Explanation panels contain complete causal or comparative relationships,
not lists of technical nouns. The deck in
`/Users/danielzhao/MyMac/Masters Degree/Research/Thesis Presentation/` implements this specification.

| Element | Specification |
| --- | --- |
| Canvas | 16:9, 13.3333 × 7.5 inches; donor size 12,192,000 × 6,858,000 EMU. |
| Title | Lato Bold 28 pt, black, left aligned at x=0.6, y≈0.3. Retain the titles below and sentence case. |
| Lead | Lato 17 pt regular in `#555555`, one or two lines at y≈1.0; set one meaningful phrase in bold orange. Backups use one 15 pt regular introduction line. |
| Setting line | Lato 13 pt bold orange, one line under the lead or at the top of the right-hand column. |
| Section labels | Lato 14 pt bold navy or orange, with a 1 pt hairline beneath in `#B8C5D6` or `#F5C7AA`. |
| Main text | Panel headings Lato 14.5–15 pt bold; panel and body text 13.5–15 pt; table cells 14.5–16 pt under 12.5–14 pt bold headers. |
| Maths | Editable Cambria Math, 20–22 pt for display equations, with definitions beside first use. |
| Charts | Labels and annotations 12–13 pt; lines about 2 pt (1.4 pt in backup grids); markers 5–6 pt; light grey axes and gridlines. Draw each chart at its placed size. |
| Sources | Footer 10.5 pt italic `#8C8C8C` at y≈7.05; slide numbers 10.5 pt `#A0A0A0`; reference entries 14.5 pt across two pages, with full citations in notes. |
| Cover | Curved white/chalkboard composition; orange Aptos Display title about 29 pt; italic question about 15.5 pt; Aptos details about 13.5 pt, kept inside the white area. |

Use white `#FFFFFF`, body text `#262626`, secondary text `#555555`, navy
`#1F3A5C` and orange `#E97132`. Use the darker orange `#B4501A` for
Expanded Welch labels on pale fills. The donor's `#ED7D31` may remain in
reused elements. Pale fills are peach `#FDF3EC` and blue `#EDF2F8`, with
modest rounding and no outline. A 1 pt `#F5C7AA` outline may mark a block
that needs emphasis, such as the project's own steps on Slide 5. Avoid
extra badges, symbols and logo/footer banners.

Use light components throughout. Section labels with hairlines take the
place of solid header bars. A callout is plain text beside a thin orange or
navy bar at its left edge, with no dashed box. Table headers are small bold
text above a 1 pt orange rule, with no filled header row. Number circles
are about 0.32–0.36 inches across, and arrows are small and light orange.

Use a 0.6-inch side margin. Reserve roughly the top 1.8 inches for title,
lead and setting line, the centre for evidence and explanation, and y≈7.05
for sources. Main charts sit at left, about 6.3–6.5 inches wide, with
explanation panels and callouts in a right-hand column about 5.3 inches
wide. Backup figures span about 12.1 inches. Leave white space between
elements. Do not enlarge text or panels to fill a slide, and do not force
every slide into identical cards.

Actual donor content runs use Lato although its generic Office theme says
Aptos. Check font availability in both authoring and rendering; embedded
PDF fonts do not establish installation. Do not silently substitute another
body font. Reuse donor `ppt/media/image1.png` and the original cover mask
on a copy. If the mask is lost, render decoration only after removing old
title/subtitle, then overlay editable new text. Do not bake old wording
into a background. No university logo is added by default.

### Chart meanings

- Main method comparisons: navy Wald, solid/filled circles; orange
  Expanded Welch, dashed/open squares. Keep overlaps real.
- RQ1: colours identify quantities. Slide 7 uses navy population-based
  inputs and orange sample-based inputs. Slide 8 keeps those meanings:
  charcoal target, orange sample-based estimate and dotted navy
  population-based value. Label directly.
- Full grid backups retain thesis parameter colours for shared MI/gap,
  with solid circles versus dashed squares identifying methods. Supply
  explicit legends and announce that encoding when opening a backup.
- Mark the ten observed sample sizes. Use logarithmic sample-size axes
  where specified. Lines guide the eye between tested points.
- Rates divide rejections by **all 100,000 repetitions**. Unsuccessful
  calculations count as non-rejections. B3 states the calculation
  requirements, and full grid figures retain calculation-success strips.
  Every calculation succeeds in the key main null examples and at the
  highlighted wrong-direction point.
- Main rate figures retain saved pointwise 95% Monte Carlo intervals.
  These are not simultaneous intervals over the grid. The whole-grid
  summaries on Slides 9, 11 and 12 show point estimates, one per setting. Snapshot tables
  show point estimates. RQ1 bands use approximately estimate ±1.96 MCSE.
- Preserve ratio directions. Distinguish Var(V-hat), V-hat/n and variance
  of the MI difference. The moment target is not a proven Student t df.
- MI and differences use nats; df are dimensionless; rates use percent.
  Multiply saved proportions by 100 once. Use manifest filter tolerances.
- Preserve scientific data and editability. Standard plotting tools may
  create presentation-specific charts. Do not use image generation for
  scientific evidence or place entire thesis pages on slides.

Use Australian English and full distribution names. Explain what changes,
why and its consequence; connect sentences through specific referents.
Preserve short definitions and distinct findings. Avoid unnecessary
abbreviations and repeated qualifications. Copy below goes on slides;
scripts, sources and cues go in notes. Keep build instructions out of
Daniel's rehearsal notes. A static PDF must contain the complete argument.

## 5. Sequence and timing

Allocations include scripts, transitions, pointing and pauses. Transitions
close the current slide's allocation. Actual timing requires rehearsal.

| Slide | Title | Time | Finish by |
| --- | --- | --- | --- |
| 1 | Comparing Mutual Information in Finite Samples | 0:25 | 0:25 |
| 2 | Motivation: comparing MI across populations | 1:15 | 1:40 |
| 3 | Literature review: foundations and the MI-specific step | 1:00 | 2:40 |
| 4 | Method: one statistic, two reference distributions | 1:20 | 4:00 |
| 5 | Approach and contribution | 2:05 | 6:05 |
| 6 | Evaluation design | 1:20 | 7:25 |
| 7 | RQ1 results: approximation accuracy | 1:40 | 9:05 |
| 8 | RQ1 results: near independence | 2:00 | 11:05 |
| 9 | RQ2 results: false positives across all null settings | 1:30 | 12:35 |
| 10 | RQ2 results: why the cutoff helps, hurts, or cannot fix it | 1:45 | 14:20 |
| 11 | RQ3 results: the power cost of the larger cutoff | 1:30 | 15:50 |
| 12 | RQ3 results: bias can reverse the estimated direction | 2:00 | 17:50 |
| 13 | Conclusions and next steps | 1:00 | 18:50 |

Slides 5, 8 and 12 carry the derivation, the near-independence explanation
and the direction reversal, so they receive the extra time. Use it for
pauses and slower delivery, not added material.

## 6. Detailed main-slide specifications

### Slide 1 — Comparing Mutual Information in Finite Samples

**Purpose:** Establish the project through the research question.

**On-slide content:**

Comparing Mutual Information in Finite Samples

*Can MI-specific degrees of freedom improve comparisons between populations?*

Daniel Zhao (Master of Computer Science)

Supervisor: Associate Professor Joseph T. Lizier

The University of Sydney

**Layout and evidence:** Follow preferred-reference page 1: original
chalkboard image at right, curved white area at left, orange title, short
italic question and author block below the divider. Keep replacement text
editable. Allow three title lines. Omit an agenda, abstract, student ID and
unconfirmed date.

**Speaker script:**

> This project asks whether mutual information differs between populations when we have finite samples. I derive MI-specific degrees of freedom for a Welch–Satterthwaite comparison, then examine when its larger rejection cutoff improves false-positive accuracy and what happens to power.

**Delivery cue:** Face the audience. Use the question rather than reading
the affiliation.

**Transition:** “The comparison starts with two populations and a sample from each.”

**Source:** Final title, abstract, and Chapter 1; preferred-reference page 1.

### Slide 2 — Motivation: comparing MI across populations

**Purpose:** Connect two populations, sampling uncertainty and the
hypothesis.

**On-slide content:**

**Lead:** Mutual information measures how much observing one variable
reduces uncertainty about another, on average. Different sample estimates
can arise from sampling noise.

\[
H_0:I(P)=I(Q)\quad\text{against}\quad H_1:I(P)\neq I(Q)
\]

**Two populations**

- Population P: a sample of size n_P, summarised in a count table, gives
  the MI estimate Î(P).
- Population Q: a sample of size n_Q gives Î(Q).
- Variables: the same two categorical variables, X and Y, in each
  population.

**Statistical task:** Summarise a sample from each population in a count
table. Estimate MI from each table. Assess whether sampling noise can explain the difference.

**Question:** Does MI differ between the two populations?

**Layout and evidence:** Adapt preferred-reference page 2. Put both
hypotheses, as in thesis Equation 1.1, on one line in a shallow peach
area labelled “Hypotheses”. At left align the two populations,
generic table icons and their MI estimates; at right use three connected
task steps. The icons are schematic and encode no counts. Show no dataset,
sample sizes or estimated values.

**Speaker script:**

> Mutual information measures the average reduction in uncertainty about one variable when we observe another. I compare that association between two populations, whose probability tables I call P and Q.

> We observe a sample from each population, summarise it in a count table, and estimate MI from each table. Different samples can produce different estimates even when population MI is equal. The null hypothesis therefore equates the two population MI values, against the two-sided alternative that they differ. It allows different probability tables. We need to account for sampling uncertainty before interpreting an observed difference.

**Delivery cue:** Trace each population into its estimate, then point to
the null.

**Transition:** “The literature supplies several parts of that comparison, with one additional MI-specific calculation needed.”

**Source:** Thesis Sections 1.1 and 2.1; Bossomaier et al. (2016).

### Slide 3 — Literature review: foundations and the MI-specific step

**Purpose:** Make the contribution follow from the established foundations.

**On-slide content:**

**Lead:** Existing results provide MI estimates, a Wald test using a
standard normal distribution, and moment matching. This project derives the
MI variance sensitivity needed for its degrees of freedom.

| | MI estimation and uncertainty | Wald comparison | Welch–Satterthwaite moment matching |
| --- | --- | --- | --- |
| Idea | Estimate MI and first-order sampling variance | Divide the estimated difference by its standard error | Match variance moments to choose degrees of freedom |
| Key work | Moddemeijer (1989); Paninski (2003) | Wald (1943); Mora and Ruiz-Castillo (2009) | Satterthwaite (1946); Welch (1947); Hutcheson (1970); Pan and Wall (2002) |
| Required step | Track variation in the variance estimate itself | Assess the fixed cutoff from the standard normal distribution in finite samples | Calculate the MI-specific variance sensitivity |

**Contribution:** Derive that sensitivity and evaluate the resulting
degrees of freedom.

**Layout and evidence:** Use preferred-reference page 3's three-column
matrix, orange labels and light rules. Keep citations secondary to the
ideas. Put the contribution in one pale peach strip, with "Contribution:"
in bold orange. Avoid an unverified
claim that no equivalent formula has appeared anywhere.

**Speaker script:**

> The project builds on three established strands. Work on MI supplies the estimator, its leading bias correction, and its first-order sampling variance. The Wald test uses those estimates with the standard normal distribution as its reference. Welch and Satterthwaite instead use variance moments to choose degrees of freedom, with related applications in entropy and other statistical comparisons.

> For this MI comparison, the additional calculation is how much the pointwise-MI variance estimate changes when the sampled table changes. Its probability weights, row and column margins, and pointwise-MI values all change together. I derive that sensitivity and evaluate the resulting approximation.

**Delivery cue:** Move across the columns once. Emphasise the required
calculation rather than reciting authors.

**Transition:** “The two tests then share a statistic but use different reference distributions.”

**Source:** Thesis Sections 2.2–2.5 and 3.2–3.3; bibliography keys
moddemeijer1989, paninski2003, mora2009, satterthwaite1946, welch1947,
hutcheson1970, and panwall2002.

### Slide 4 — Method: one statistic, two reference distributions

**Purpose:** Make the common estimates and larger cutoff visible.

**On-slide content:**

**Lead:** Both methods use the same estimated MI difference and standard
error. Expanded Welch uses estimated degrees of freedom for a Student t
distribution.

\[
T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}},\qquad
\widehat{\mathrm{SE}}^2=\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}.
\]

\(\widehat\Delta_{\mathrm{BC}}\): estimated \(I(P)-I(Q)\), after leading
bias correction.

\(V(P)\): population variance of pointwise MI; \(\widehat V(P)\) estimates
it from one sampled table.

- **Wald test:** standard normal distribution; two-sided 5% cutoff
  about ±1.96.
- **Expanded Welch test:** Student t distribution with estimated degrees
  of freedom; a larger cutoff.

**Plot label:** Student t distribution with 5 degrees of freedom, for
illustration; cutoff about ±2.57.

**Layout and evidence:** Follow preferred-reference page 4. Put shared
equations/definitions at left above pale-blue Wald and pale-peach Expanded
Welch panels with navy and orange headings. At right use a shared-axis
density plot with direct labels and
marked cutoffs. The illustrative df are 5, not an experimental estimate.
Calculation requirements are introduced on Slide 6 and specified in B3.

**Speaker script:**

> Both tests divide the estimated MI difference, after a leading bias correction, by the same estimated standard error. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Independence between the samples lets their two variance contributions add.

> The standard error itself fluctuates between samples. We use a Student t reference distribution so that the rejection cutoff can reflect uncertainty in that variance estimate. Its degrees of freedom are estimated from the tables.

> The Wald test uses the standard normal distribution, with a two-sided five-percent cutoff of about 1.96. The illustration uses a Student t distribution with five degrees of freedom, giving a larger cutoff of about 2.57. Actual estimated values vary. Under the same testing rules, Expanded Welch can only reject where Wald also rejects. The experiments assess whether this reduction improves false-positive rates and how much power it costs.

**Delivery cue:** Point to the shared standard error, explain why its sampling variation matters, then compare cutoffs. The illustrated five degrees of freedom is not typical of every dataset.

**Transition:** “Choosing the degrees of freedom requires the variability of the variance estimate itself.”

**Source:** Thesis Chapters 3–4 and Figure 2.1; quantiles of the standard
normal distribution and the Student t distribution with 5 degrees of freedom.

### Slide 5 — Approach and contribution

**Purpose:** Explain a connected calculation before its final formula.

**On-slide content:**

**Lead:** The estimated pointwise-MI variance changes between samples. We
approximate that variation and use it to choose the degrees of freedom.

**Derivation chain**

1. Cell probabilities change: move a small amount of probability towards
   one cell.
2. Margins and pointwise MI change: track their joint effect.
3. Variance sensitivity, derived here: \(g_P(x,y)\) describes the change
   in \(V(P)\).
4. Degrees of freedom: use the spread of those sensitivities.

\[
\operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P}
\quad\Longrightarrow\quad
\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
\]

\(\tau^2(P)\) is the variance of \(g_P(X,Y)\). Repeat for Q and combine
using Welch–Satterthwaite.

**Two approximations evaluated:** first-order sampling expansion; matching a
scaled chi-squared distribution.

**Layout and evidence:** Follow preferred-reference page 5. Use four short
connected blocks above, identifying the sensitivity and df as the project's
calculation. Below, put the result in a pale-blue area with the two
approximation labels beside it. Define tau-squared locally. Keep the
expanded derivative in B1. Each block explains a relationship rather than
merely naming a technical object.

**Speaker script:**

> There are two levels of variation. V-hat describes variation in pointwise MI, but V-hat itself changes when a new sample produces a different table. I calculate how V changes when a small amount of probability moves towards one cell. The cell weights, margins, and log ratios all change together, and the sensitivity g describes their combined effect.

> Different possible outcomes have different sensitivities. Tau-squared is the variance of those sensitivities. Averaging the observation-level contributions gives a first-order approximation to the error in V-hat. With independent observations, the sampling variance of that average is tau-squared divided by sample size.

> Satterthwaite moment matching uses the mean and sampling variance of V-hat to choose component degrees of freedom. Greater variability relative to the squared mean gives fewer degrees of freedom and a larger cutoff. I estimate the inputs from each table, repeat the calculation for Q, and combine the components using the Welch–Satterthwaite rule.

> The derivative is exact for positive population tables. Its use to approximate sampling errors, and the resulting Student t reference distribution, are approximations. The first research question checks the sampling approximations and the degrees of freedom they imply.

**Delivery cue:** Pause between the two levels of variation. Define g and tau-squared before the formula, then explain what greater relative uncertainty does to the cutoff. The displayed df are component df, not the combined test df.

**Transition:** “Known population tables let me check those approximations before assessing test decisions.”

**Source:** Thesis Sections 4.1–4.3; eq:g-final,
eq:vhat-sampling-variance, eq:nu-p-hat, and eq:expanded-df. B1–B2 retain the
full derivative and moment-matching argument. The source line also points
to Slides 16–17 for g and tau-squared in cell probabilities, with a worked example.

### Slide 6 — Evaluation design

**Purpose:** Explain the parallel studies and separate sample size from
repetition count.

**On-slide content:**

**Lead:** Known populations separate approximation accuracy, false
positives, and power. Both tests receive the same sampled table pairs.

| Research question | Evaluation |
| --- | --- |
| RQ1: Approximation accuracy | Sampling moments of V-hat and component df, including near independence |
| RQ2: False positives | Equal MI at 0.005, 0.02, and 0.30 nats |
| RQ3: Power | I(P) = 0.02; MI-gap magnitudes 0.005, 0.01, and 0.02 nats |

**Shared simulation grid**

- Four sizes: 2×2, 4×4, 8×8, 16×16.
- Uniform, same-skew, and different-skew margins.
- Ten sample sizes: 10 to 50,000 observations per population.
- 360 settings per study (4 sizes × 3 margins × 10 sample sizes × 3 MI
  levels or gaps).
- 100,000 independent table pairs per setting.

**Model:** A copying construction that fixes the margins and solves for
the target MI.

**Reporting:** Usual 0.05 p-value thresholds. Unsuccessful calculations
count as non-rejections; calculation success is reported separately.

**Layout and evidence:** Follow preferred-reference page 6. Put questions
in a navy-headed area at left and settings in an orange-headed area at
right. Keep sample size and repetition count distinct. Put reporting below.
State 360 settings each for null and power in speech/notes, without another
counter. Exact vectors, sample sizes, and requirements are in B3.

**Speaker script:**

> I construct population tables with known MI by drawing X, then either copying its category into Y or drawing Y independently from the same category frequencies. Changing how often I copy controls association while preserving those frequencies. A numerical search chooses the copying probability for the target MI.

> RQ1 checks the variance approximations and degrees of freedom. The false-positive study uses equal MI, while the power study fixes MI in P at 0.02 nats and gives Q greater MI. Nats are units based on natural logarithms.

> Each test study has 360 settings, varying table size, category frequencies, sample size, and the shared MI or MI gap. Each setting uses 100,000 independent sampled table pairs. Both methods receive the same pairs, but each test sees only the observations in its two tables. Repetition measures performance without increasing that sample size. Both methods use the usual five-percent threshold. Unsuccessful calculations count as non-rejections, with calculation success reported separately.

**Delivery cue:** Explain copying in words. Name the factors without reciting the grid multiplication. Keep sample size distinct from repetition count, and retain the unsuccessful-calculation rule.

**Transition:** “The first result shows why accurate variance prediction can coexist with an inflated mean.”

**Source:** Thesis Chapter 5, Tables 5.1–5.3, and Appendix B; Morris et al.
(2019). Current balanced-null and MI-gap grids.

### Slide 7 — RQ1 results: approximation accuracy

**Purpose:** Teach the two moment errors using the clear 4×4 example.

**On-slide content:**

**Lead:** The mean of V-hat can remain inflated even when its population
first-order sampling-variance prediction is accurate.

**Setting:** Different-skew P; 4×4; population MI 0.02 nats.

- Top plot: mean of \(\widehat V\) / population \(V\).
- Bottom plot: predicted / observed sampling variance of \(\widehat V\).
- Bottom curves: population-based inputs; sample-based inputs.

**Mean: rare cells can inflate it.** Newly observed rare cells can have
large pointwise-MI deviations, whose squares raise V-hat.

**Sampling variance: linearisation can miss large changes.** Rare cells
appear in some samples and not others; sample-based sensitivities can also
overpredict the resulting variation.

**At n=1,000:** mean 19% high; variance prediction 3% low with
population-based inputs and 8% high with sample-based inputs. Both moments enter the degrees
of freedom.

**Layout and evidence:** Follow preferred-reference page 7. Stack two
white plots at left, with the two mechanism panels at right and numerical
conclusion beneath. Use P/4×4 null-display rows from current moments.csv.
Top: mean_ratio in neutral charcoal, linear y=0–5.5. Bottom:
variance_ratio and plugin_variance_ratio, linear y about 0.4–1.7. Both use log sample size and
a reference at one. The bottom plot uses navy population-based inputs and
orange sample-based inputs, directly labelled as quantities with parallel
names. At n=1,000 label the top +19% and the population-based curve −3%. Retain narrow approximate 95%
Monte Carlo bands. Do not call the sample-based prediction 3% low.
B4 supplies wider table-size/P/Q context.

**Speaker script:**

> This is one population and a four-by-four table, so the two moment errors can be read together. On top, one would mean the average V-hat equals the population variance. The mean rises above that benchmark and then recovers. When rare cells first appear, their estimated pointwise MI can lie far from the table's MI. The squared deviations can inflate V-hat until repeated counts stabilise the estimates.

> The lower graph concerns the sampling variance of V-hat itself. The navy curve uses known population inputs; the orange curve estimates those inputs from each sample. The population prediction misses variation when rare cells appear in some samples and remain absent in others. Estimating the sensitivities from sparse counts can instead overshoot. Larger samples improve both predictions.

> At one thousand observations, the population prediction is about three percent low, while the sample-based prediction is about eight percent high. The mean is still nineteen percent high. Since the degrees-of-freedom calculation squares the mean input and divides by the variance input, a good variance prediction alone does not make that calculation accurate.

**Delivery cue:** Pause when the graphs appear. Explain the top graph
before the bottom. Say “sampling variance of V-hat”. Tie both annotations to n=1,000.

**Transition:** “Near independence, an additional separation appears because sampling noise creates apparent association.”

**Source:** Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2; null-display IDs,
side=p, k=4, profile=different_skew, MI=.02. B2 retains the numerical df
consequence of this same example.

### Slide 8 — RQ1 results: near independence

**Purpose:** Keep the important near-independence check in the main story
and explain the three distinct quantities.

**On-slide content:**

**Lead:** Near independence, first-order theory gives almost no degrees
of freedom, while sampling noise keeps the mean sample-based estimate at
about half the target.

**Setting:** Different-skew P; 4×4; n=1,000 fixed.

**Population-based: falls to about n × MI:** Inserts known population
inputs into the first-order formula. Near independence it is about
n × population MI, which heads to zero.

**Sample-based: noise keeps it near 5:** Quadratic sampling errors create
apparent association, which remains in each sample's calculation.

**At MI 0.0001:** target ≈9.1; mean sample-based estimate ≈4.9;
population-based value ≈0.1.

**Chart caption:** Target: component degrees of freedom from the actual
mean and variance of V-hat across 100,000 samples.

**Layout and evidence:** Follow preferred-reference page 8. Place a large
chart at left, two short explanations at right and one numerical callout
beneath them. Plot df_mean, nu_mom and nu_fo for the P/4×4/n=1,000
association-display rows against MI, both axes logarithmic and labelled
as such. Use charcoal for the target, orange for the sample-based estimate
and dotted navy for the population-based value, matching Slide 7's
colours, with direct labels: “target (measured from 100,000 samples)”,
“mean sample-based estimate” and “population-based value”. Mark the gap at
MI 0.0001 with a small bracket labelled “about half the target”. The footer
names the thesis symbols ν_P,mom, mean ν̂_P and ν_P,FO. These are
quantities, not methods.
Preserve all seven MI values. The target is not “true t df”. B5 explains
the local prediction and compares it with observations.

**Speaker script:**

> Here sample size stays at one thousand while population MI approaches zero. Start with the charcoal line: this is the moment-matching target, calculated from the mean and variance of V-hat across 100,000 sampled tables. It is our benchmark for the component degrees of freedom.

> The dotted navy line instead uses population inputs in the first-order formula. The orange line averages the component degrees of freedom estimated from each sampled table. At the weakest association, the target is about nine, the population-based value is about 0.1, and the mean sample-based estimate is about five, or half the target.

> Random count fluctuations can make sampled tables look associated even when the variables are independent in the population. At independence, the linear sampling contribution vanishes, but variation from squared probability errors remains. These are the quadratic terms omitted by the first-order calculation. The sample-based calculation retains apparent association, keeping its mean positive. A calculation that includes this sampling noise predicts about 4.6, close to the observed 4.9.

**Delivery cue:** Pause when the graph appears. Introduce the charcoal target first, then dotted navy population-based values and orange mean sample-based estimates. Point to the weakest-association end. Preserve this slide in every shorter route. Matching the target does not prove an exact Student t distribution.

**Transition:** “The decision-level question is whether the larger cutoff brings false positives towards five percent.”

**Source:** Thesis Section 6.1.3, Figure 6.3, and Appendix A.2; observed
mean 4.859787, target 9.124808, and first-order value .096400.

### Slide 9 — RQ2 results: false positives across all null settings

**Purpose:** Answer RQ2 across the whole null grid, not one slice, and show
where the larger cutoff helps and where it hurts.

**On-slide content:**

**Lead:** A larger cutoff helps only where Wald rejects too often; where
Wald already rejects too rarely, it never brings the rate closer to 5%.

**Setting:** All 360 null settings; equal MI in P and Q; each point is one
setting.

**Wald too high: 178 settings:** Expanded Welch moves closer to 5% in 165,
for example 8.35% to 4.90% (uniform 4×4, n = 20, MI 0.02).

**Wald too low: 180 settings:** Further below 5% in 176 settings;
unchanged in four.

**Descriptive 4–6% band:** 130 versus 136 settings. Bias-driven excess
persists: 36.38% to 34.38% (different-skew 16×16, n = 1,000,
MI 0.005).

**Chart note:** Below the diagonal: Expanded Welch rejects less often.
Dashed lines: the 5% target.

**Layout and evidence:** One scatter of all 360 null settings at left:
Wald false-positive rate on the horizontal axis, Expanded Welch on the
vertical, both logarithmic, with the diagonal, dashed 5% lines and lightly
shaded halves (“Wald too low”, “Wald too high”). Circle and label the two
thesis examples. Panels and callout at right. Counts are tallies of the
balanced null rates using all 100,000 repetitions per setting, with
unsuccessful calculations counted as non-rejections; two settings have a
Wald rate of exactly 5%. Report both directions of change, never a
favourable count alone. Compare exact rejection counts: four conservative
settings have identical counts under both tests. The 4–6% band is a
descriptive choice (4.5–5.5% gives 105 versus 98), so the verdict rests on
the pattern and Slide 10's mechanisms, not on the band.

**Speaker script:**

> This chart shows all 360 null settings, so every rejection is a false positive. Each point is one setting: Wald's false-positive rate is on the horizontal axis and Expanded Welch's is on the vertical. The diagonal means no change, and the dashed lines mark five percent.

> Every point lies on or below the diagonal because the larger cutoff can only reduce rejection. On the right, Wald's observed rate exceeds five percent. Expanded Welch moves closer to the target in 165 of those 178 settings. On the left, Wald already rejects too rarely. None of those 180 settings improves: the rate falls further or remains unchanged.

> The circled examples show both improvement and remaining failure. In the upper-right example, even the reduced rate is above 34 percent. Lowering rejection therefore does not by itself make the test accurate.

**Delivery cue:** Pause when the graph appears. Explain axes, diagonal, and target before the counts. Take the right half, then the left. Leave the descriptive 4–6% tally for the audience to read; retain the overall pattern and the severe remaining failure.

**Transition:** “These diagnostic examples help explain the different rejection patterns.”

**Source:** Thesis Sections 6.2.1–6.2.3 and Figures 6.4–6.6; tallies of
the balanced null rates (360 settings, both methods, all repetitions).
Examples: uniform 4×4, n = 20, MI 0.02 (Wald 8.35%, Expanded Welch 4.90%);
different-skew 16×16, n = 1,000, MI 0.005 (36.38% and 34.38%).

### Slide 10 — RQ2 results: why the cutoff helps, hurts, or cannot fix it

**Purpose:** Explain the three patterns on Slide 9 with the three
illustrative settings of thesis Table 6.1.

**On-slide content:**

**Lead:** Three kinds of estimation error explain the three patterns on
Slide 9.

**Setting:** Three illustrative settings (thesis Table 6.1); equal MI 0.02
nats; every calculation succeeds.

| Setting | Bias / SD | Variance ratio | Wald | Expanded Welch |
| --- | --- | --- | --- | --- |
| Uniform 4×4, n = 20 | ≈0 | 0.83 | 8.35% | 4.90% |
| Same skew 16×16, n = 1,000 | ≈0 | 1.93 | 0.60% | 0.53% |
| Different skew 16×16, n = 1,000 | 2.06 | 1.94 | 26.01% | 24.84% |

Bias / SD: shift of the estimated MI difference from zero, in sampling
standard deviations. Variance ratio: average squared estimated standard
error / observed variance.

**Standard error too small:** Wald rejects too often. The larger cutoff
offsets it: 8.35% to 4.90%.

**Standard error too big:** Wald already rejects too rarely. The larger
cutoff pushes it further below 5%.

**Bias in the MI difference:** The estimate sits about two SDs from zero.
The larger cutoff barely helps: 26.01% to 24.84%.

**Conclusion:** A larger cutoff can offset a standard error that is too
small, but it cannot fix bias in the estimated MI difference.

**Layout and evidence:** Native three-row table with the driver in each
row in bold (0.83, 1.93, 2.06), the definitions immediately below, three
aligned mechanism panels beneath, and the conclusion at the bottom. Label
the settings as illustrative; Slide 9 carries the whole grid. Explain
average uncertainty misestimation rather than claiming every standard error
is too small or too big. The comparison supports a diagnostic explanation
without proving these are the only distributional differences. The footer
points to B6–B8 for the full grids and B9 for the ordinary Welch
comparison.

**Speaker script:**

> These three examples help explain the different rejection patterns. All have equal population MI, so every rejection is a false positive, and every calculation succeeds. Bias over SD measures the shift of the estimated difference from zero. The variance ratio compares the average squared standard error with the observed sampling variance of that difference.

> In the uniform four-by-four example, the two MI estimates have the same expected bias, so it cancels in their difference. The variance ratio is about 0.83, indicating underestimated sampling variation. A small denominator inflates the statistic, and the larger cutoff brings rejection closer to five percent.

> In the same-skew example, the biases again cancel. But the variance ratio is about 1.93, indicating overestimated sampling variation. Wald already rejects less than one percent of the time, and the larger cutoff lowers that further.

> The different-skew example has a similarly inflated variance estimate, but the residual biases in the two MI estimates do not cancel. Their difference is centred about two sampling standard deviations above zero, and both tests reject about a quarter of the time. The larger cutoff changes the boundary without removing this bias.

**Delivery cue:** Follow the rows from cancellation of difference bias to the variance ratio and rejection pattern. Do not imply the individual MI estimates are unbiased or that all three settings are otherwise matched.

**Transition:** “The same larger cutoff also changes the probability of detecting a real MI difference.”

**Source:** Thesis Section 6.2.4 and Table 6.1; current null rates and
diagnostics. Bias/SD .002744/−.002719/2.057921; variance ratios
.826509/1.928694/1.938104.

### Slide 11 — RQ3 results: the power cost of the larger cutoff

**Purpose:** Answer RQ3 across the whole power grid: how much detection the
larger cutoff costs, and when.

**On-slide content:**

**Lead:** Expanded Welch never has more power than Wald; the loss is
largest in small samples and under 0.32 points by n = 10,000.

**Setting:** All 360 power settings; MI in P = 0.02 nats; gaps of 0.005,
0.01, and 0.02 nats.

**The loss is concentrated in small samples:** Median loss: about 6 points
at n = 10, about 1 point from n = 50 to 1,000, and 0.16 at n = 10,000.
Failed calculations add to it at the smallest samples.

**Small MI gaps can stay hard to detect:** Even at n = 50,000, the 0.005
gap reaches only 79.87%–96.47% power; gaps of 0.01 and 0.02 exceed 99.9%.

**Power:** rejecting equal MI when population MI differs, in either
direction, at the usual 0.05 threshold.

**Chart note:** Power lost: Wald power minus Expanded Welch power, in
percentage points.

**Layout and evidence:** One chart at left: power lost against sample size
(log scale), with the median across the 36 settings at each n as a line and
the full range shaded. Annotate the n = 10,000 maximum (under 0.32 points).
Panels and callout at right. Values are tallies of the MI-gap power rates
using all 100,000 repetitions, with unsuccessful calculations counted as
non-rejections. This is not matched-size power.

**Speaker script:**

> Power is the probability of rejecting equal MI when the population MI values differ. This chart summarises all 360 power settings under the same nominal five-percent threshold. It shows Wald power minus Expanded Welch power, in percentage points. The line is the median across 36 settings at each sample size. The shading is their full range, not Monte Carlo uncertainty like the earlier bands.

> Expanded Welch cannot have more power because its rejections are a subset of Wald's. The loss is largest at ten observations, with a median of about six percentage points; unsuccessful calculations also contribute there. By ten thousand observations, the loss is below 0.32 percentage points in every setting.

> A small difference between methods does not necessarily mean high power. Even with fifty thousand observations, power for the smallest MI gap ranges from about 80 to 96 percent, while the two larger gaps exceed 99.9 percent. These rates count rejections in either direction, which matters for the next slide.

**Delivery cue:** Pause when the graph appears. Define power lost, median, and range. Emphasise the small-sample loss and the under-0.32-point bound at n = 10,000, retaining the distinction between method differences and absolute power. This is not matched-size power.

**Transition:** “Different residual biases can make that directional error dominate the apparent detections.”

**Source:** Thesis Sections 6.3.1–6.3.3, Figures 6.7–6.9, and Section
7.1.3; tallies of the MI-gap power rates (360 settings, both methods, all
repetitions). Median loss 5.78 points at n = 10 (maximum 13.42); maximum
0.313 points at n = 10,000.

### Slide 12 — RQ3 results: bias can reverse the estimated direction

**Purpose:** Show how widely bias makes rejections point to the wrong
population, using the whole different-skew grid, with the thesis example
outlined.

**On-slide content:**

**Lead:** Under different-skew margins, sparse tables give rejections that
point to the wrong population.

**Setting:** Different-skew margins; MI gap 0.01 nats; % of Expanded Welch
rejections with the wrong sign.

**Outlined cell: 16×16, n = 1,000:** True difference −0.0100 nats; mean
estimate +0.0207. Expanded Welch rejects in 9.66% of repetitions, and over
99.9% of those point the wrong way.

**Bias outweighs the gap:** A larger cutoff cannot remove bias; more data
can. By n = 10,000, under 0.4% of rejections point the wrong way.

**All 360 power settings:** at least 90% wrong in 28, all with
different-skew margins.

**Chart note:** Percentages are rounded. A value of 50% means half the
rejections have the wrong estimated sign.

**Layout and evidence:** One heat map at left: table size (rows) by sample
size (columns) for different-skew margins and the 0.01-nat gap, each cell
the percentage of Expanded Welch rejections with a positive estimated
difference (the true difference is negative). Print the value in each
cell and outline the 16×16, n = 1,000 cell. Panels and callout at right.
Shares come from the signed rejection counts in the MI-gap power
diagnostics. The 0.005 and 0.02 gaps show the same pattern. Do not turn
“over 99.9%” into a percentage of all repetitions.

**Speaker script:**

> This heat map covers all table sizes and sample sizes under different-skew margins, for the 0.01-nat gap. Q always has greater population MI. Each cell shows, among Expanded Welch rejections, the percentage whose estimated difference incorrectly points to P as having greater MI. The displayed percentages are rounded.

> The darker cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range. Focus on the outlined sixteen-by-sixteen cell at one thousand observations per population. The true difference is minus 0.01 nats, but the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9 percent of those rejections have the wrong estimated sign.

> Unequal residual biases have outweighed the true gap. A larger cutoff cannot remove that bias; it changes how often we reject. In these simulations, increasing sample size reduced the bias. Across the full power grid at ten thousand observations, fewer than 0.4 percent of rejections point the wrong way.

> Across all 360 power settings, at least 90 percent of rejections point the wrong way in 28 settings, all with different-skew margins. These count as detections under the two-sided definition of power, but do not reliably identify which population has greater MI.

**Delivery cue:** Pause when the heat map appears. Define the percentage as conditional on rejection. Explain the outlined cell through its signed differences before the wrong-direction percentage. Preserve this slide in every shorter route; every calculation succeeds at the outlined cell.

**Transition:** “The contribution and the remaining estimation problems lead to specific next steps.”

**Source:** Thesis Section 6.3.3 and Figure 6.9; signed rejection counts in
the MI-gap power diagnostics (360 settings). Outlined cell: 9,659 of 9,662
Expanded Welch rejections positive; bias about 0.0307 nats.

### Slide 13 — Conclusions and next steps

**Purpose:** Answer the research question and link future work to
observed limitations.

**On-slide content:**

**Lead:** MI-specific degrees of freedom improve some false-positive rates,
while remaining failures identify estimation accuracy as a priority.

**Contributions** (thesis Section 1.3)

1. Derivation: how the estimated pointwise-MI variance varies between
   samples.
2. Test construction: the Wald statistic with estimated Student t degrees
   of freedom.
3. Empirical evaluation: accuracy, false positives, power, and calculation
   success.

**Findings by research question** (thesis Sections 7.1.1–7.1.3)

- RQ1, approximation accuracy: approximations improve as samples grow;
  near independence, first-order theory misses sampling noise.
- RQ2, false positives: helped only where Wald rejected too often; pushed
  conservative settings further below 5%.
- RQ3, power and direction: at the same nominal 5% threshold, power is no
  higher; bias can make rejections point the wrong way.

**Scope:** The evaluation covers one population construction and equal
sample sizes, with the Wald test as the main benchmark.

**Next steps**

- Reduce bias in the estimated MI difference and improve its standard error
  and degrees of freedom, including near independence.
- Test other association constructions and unequal sample sizes.

Thank you.

**Layout and evidence:** Follow preferred-reference page 14. Keep
contributions and findings as two separate elements. Contributions are the
highlight: three cards in a stronger peach, each with a large orange
numeral, a dark-orange name and a one-line description, beneath an orange
“Contributions” heading. Findings follow as three pale-blue cards beneath a
navy “Findings by research question” heading, each with a navy RQ tag, a
short navy title and the finding. Then a navy-bar scope line, and the two
next steps as orange-arrow items without boxes beneath orange. Keep phrases readable and add no new
equations. This combines the former limitations and conclusion pages.
Leave it displayed during questions. Its speaker notes contain the
backup-number index.

**Speaker script:**

> This work makes three contributions. It derives how the pointwise-MI variance estimate varies between samples, builds the Expanded Welch test from that result, and evaluates both in controlled simulations.

> For RQ1, the approximations improve as samples grow, but miss sampling noise near independence. For RQ2, the larger cutoff helps only where Wald rejects too often. For RQ3, power is no higher at the same nominal threshold, and bias can make rejections point the wrong way.

> The evaluation covers one population construction and equal sample sizes. Next, I would improve the MI-difference and standard-error estimates and test broader populations.

> The main finding is that adjusting the cutoff helps in some settings, while the remaining failures show why accurate MI differences and standard errors are also essential. Thank you.

**Delivery cue:** Name the three contributions, then give one finding per research question. Keep the scope brief. Finish with the overall scientific finding, then face the audience and leave this slide visible for questions.

**Source:** Final abstract; thesis Sections 1.3 (three contributions) and 7.1–7.3 (findings by research question). No claim of
universal superiority or validated independence-specific replacement test.

## 7. Backup specifications and navigation

The appendix begins with a title page on physical Slide 14, followed by
16 backups on physical Slides 15–30: B1–B14, with “B1 continued” and “B1 worked example” straight after B1. They are question material,
not another section to narrate. Keep the index below in Slide 13's notes;
do not add a projected index page. Jump by physical slide number
and return to Slide 13. Preserve the same fonts, equation/panel styles and
readability. Full grid backups retain their explicit parameter legends and
compact calculation-success strips; their colours differ in meaning from main method
comparisons, which must be stated when opening one.

| Backup | Physical slide | Question addressed |
| --- | --- | --- |
| B1 | 15 | Variance sensitivity |
| B1 continued | 16 | Variance sensitivity in cell probabilities |
| B1 worked example | 17 | Variance sensitivity: a worked example |
| B2 | 18 | Moment matching and combined degrees of freedom |
| B3 | 19 | Population construction, grid, and calculation requirements |
| B4 | 20 | Approximation ratios across table sizes |
| B5 | 21 | Near-independence noise calculation |
| B6 | 22 | Full null results: uniform margins |
| B7 | 23 | Full null results: same-skew margins |
| B8 | 24 | Full null results: different-skew margins |
| B9 | 25 | Ordinary Welch degrees of freedom |
| B10 | 26 | Full power results: uniform margins |
| B11 | 27 | Full power results: same-skew margins |
| B12 | 28 | Full power results: different-skew margins |
| B13 | 29 | References: MI and testing foundations |
| B14 | 30 | References: related methods and evaluation |

### Appendix divider — physical Slide 14

**Purpose:** Mark the beginning of the supporting material clearly in the
slide deck and PDF.

**On screen:** Only the word **Appendix**, in bold Lato (48 pt),
centred on a white background in the deck's navy colour. Retain the small
slide number. Do not add an index, explanatory paragraph, figures or data.

**Delivery:** No timed speech. Keep the conclusion on Slide 13 visible when
questions begin, then open the relevant backup when needed and return to
Slide 13 afterwards. The divider adds no time to the 18:50 main talk.

### B1 / Slide 15 — Variance sensitivity

**Question answered:** What exactly did you differentiate, and where do
the margin terms enter?

**Show:** Define
\(P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(x,y)}\),
then the exact derivative in three readable aligned lines:

\[
\begin{aligned}
g_P(x,y)={}&\{\ell_P(x,y)-I(P)\}^2-V(P)\\
 &+2\bigl[\ell_P(x,y)-\mathbb E_P\{\ell_P(X,Y)\mid X=x\}\\
 &\hspace{16mm}-\mathbb E_P\{\ell_P(X,Y)\mid Y=y\}+I(P)\bigr].
\end{aligned}
\]

Below it, define \(\ell_P(i,j)=\log\{p_{ij}/(p_{i+}p_{+j})\}\)
and \(\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}\).
Use two aligned verbal labels: “Changing probability weights” for the
first line and “Changing pointwise-MI values and margins” for the bracket.
Use about 22 pt for the main equation and 15 pt orange labels. Do not
replace conditional
means by undefined short symbols.

**Answer to give:** “I differentiate the pointwise-MI variance along a
one-observation perturbation. The first part changes the probability
weights. The bracket also changes the log ratios, including their row and
column margins. Both contributions are necessary because the pointwise-MI
values themselves depend on the table.”

**Source:** Chapter 4, source labels `eq:contamination-path`, `eq:g-final`,
`eq:tau-definition`. This derivative is exact for positive population
tables. Its use for sampling errors is first order.
The notes must state the assumptions: fixed categories,
independent observations within each sample, independent samples,
positive population cell probabilities, and positive V and tau-squared
for the first-order df construction. With every cell positive, positive
MI is equivalent to positive V (Appendix A.3), but positive V does not
guarantee positive tau-squared. Do not treat a zero component as ordinary
finite df.

### B1 continued / Slide 16 — Variance sensitivity in cell probabilities

**Question answered:** What are g and tau-squared in familiar terms, and
what do they reduce to in the cell probabilities?

**Show:** A full-width grid with three columns: the quantity in words, its
definition as an expectation, variance, or derivative, and the same
quantity as a sum over cells. Rows: pointwise MI; MI,
\(I(P)=\mathbb E_P\{\ell_P(X,Y)\}\); pointwise-MI variance,
\(V(P)=\operatorname{Var}_P\{\ell_P(X,Y)\}\); the row and column means
\(\mathbb E_P\{\ell_P(X,Y)\mid X=i\}\) and
\(\mathbb E_P\{\ell_P(X,Y)\mid Y=j\}\), written as
\(\bar\ell_{i+}=\sum_j p_{ij}\ell_{ij}/p_{i+}\) and
\(\bar\ell_{+j}=\sum_i p_{ij}\ell_{ij}/p_{+j}\); the sensitivity
\(g_P(i,j)=\mathrm dV(P_\varepsilon)/\mathrm d\varepsilon\) at zero, with
\(P_\varepsilon=(1-\varepsilon)P+\varepsilon\delta_{(i,j)}\), equal to
\(g_{ij}=(\ell_{ij}-I)^2-V+2(\ell_{ij}-\bar\ell_{i+}-\bar\ell_{+j}+I)\)
in a peach row; \(\tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}\), equal to
\(\sum_{i,j}p_{ij}g_{ij}^2\); and the moment-matched component df with
its estimate. Slide 5's source line points here.

**Answer to give:** “Each quantity has a familiar definition and a cell
form. MI is the expected pointwise MI, and V is its variance. The row and
column means are conditional expectations of pointwise MI. The sensitivity
g is the derivative of V when a small amount of probability moves towards
one cell. In cell terms, it is the squared deviation from MI minus V, plus
twice the cell's pointwise MI after subtracting its row and column means
and adding back MI. Tau-squared is the variance of those sensitivities,
which is the probability-weighted average of their squares. The next slide
works through the thesis example.”

**Notes:** The sensitivities have probability-weighted mean zero, so the
weighted average of their squares is their variance. The estimates replace
each p_ij with n_ij / n_P and sum over occupied cells; the estimate of
tau-squared centres the sensitivities explicitly (Equation 4.42). The
derivative is exact for positive population tables; its use for sampling
errors is first order.

**Source:** Thesis Equations 2.3 and 2.4 (pointwise MI and MI), 4.7 (moment
matching), 4.9–4.11 (V, the perturbation, and g), 4.29 (final form of g),
4.36 (tau-squared) and 4.41–4.43 (estimates).

### B1 worked example / Slide 17 — Variance sensitivity: a worked example

**Question answered:** Can you show the calculation with numbers?

**Show:** The thesis table \(N^P\) (Section 4.4.1, \(n_P=105\)) with row
and column totals, and cell (1, 1) highlighted. Step through cell (1, 1):
pointwise MI 0.385; MI 0.137 and V 0.272; the row 1 mean 0.103 (column 1
is the same, by symmetry); sensitivity 0.422. Show the sensitivities of all
nine cells, then tau-squared 0.932 and 16.65 component df.

**Answer to give:** “For cell (1, 1), the count is 35 and its row and
column each total 50, so its pointwise MI is 0.385. Across the table, MI is
0.137 and V is 0.272. Row 1's mean pointwise MI is 0.103, and column 1's is
the same. The sensitivity is the squared deviation 0.062 minus 0.272, plus
twice 0.316, which gives 0.422. Repeating this for all nine cells gives
tau-squared 0.932, and the component degrees of freedom are 16.65.”

**Notes:** Rounded thesis values: 0.38526, 0.13693, 0.27189, 0.10308,
0.4218, 0.93212 and 16.65. Row 1's pointwise-MI values are 0.38526,
−0.51083 and −0.64436. The thesis prints only cell (1, 1)'s sensitivity;
the other eight come from thesis Equation 4.41 and were recomputed from
the counts, as were tau-squared and the df. Cell (1, 1) contributes 0.0593
to tau-squared. The results use unrounded values, so recomputing from the
rounded inputs gives 16.67.

**Source:** Thesis Section 4.4.1, Equations 4.41–4.43 and 4.47.

### B2 / Slide 18 — Moment matching and combined degrees of freedom

**Question answered:** Where do the component and combined df formulas
come from, and why is the Student t distribution approximate?

**Show:** Use the top half for the component target and its substitution:

\[
\nu_{P,\mathrm{mom}}=
\frac{2[\mathbb E\{\widehat V(P)\}]^2}
     {\operatorname{Var}\{\widehat V(P)\}},
\quad
\widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}.
\]

Use the bottom half for the combined df, with a clear line break if needed:

\[
\widehat\nu=
\frac{\{\widehat V(P)/n_P+\widehat V(Q)/n_Q\}^2}
{\{\widehat V(P)/n_P\}^2/\widehat\nu_P+
 \{\widehat V(Q)/n_Q\}^2/\widehat\nu_Q}.
\]

Keep one sentence below: “Moment matching does not establish the standard
normal numerator, or its independence from the variance estimates, that an
exact Student t distribution requires.” Put the
scaled-chi-squared mean/variance derivation in notes rather than forcing
another four equations onto the slide.

**Answer to give:** “A variable with a scaled chi-squared distribution has
variance twice its squared mean divided by its degrees of freedom. Matching those two moments
gives the target. Dividing V-hat by fixed sample size rescales the squared
mean and variance equally, so it leaves the component target unchanged.
Independence between the two samples lets their variance contributions add.
The resulting Student t distribution still requires empirical assessment.”

**Source:** Thesis Sections 4.1 and 4.3, pp. 23–36; Satterthwaite (1946).

**Notes to include:** For a generic variance estimate U modelled as
c times a variable with a chi-squared distribution on ν degrees of freedom,
E(U)=cν and Var(U)=2c²ν, giving
ν=2[E(U)]²/Var(U). Scaling by fixed n leaves this ratio unchanged.
For the Slide 7 example at n=1,000, first-order component df are 15.30
against the moment target 21.03: approximately (1/1.19)²/0.97=0.73.
This explains the squared-mean effect without another main-slide formula.

### B3 / Slide 19 — Population construction, grid, and calculation requirements

**Question:** How are known-MI populations generated and degenerate
calculations handled?

**Show:** One construction equation above two aligned areas, with exact
sample sizes in a single line below:

\[
p_{ij}(\lambda)=(1-\lambda)a_i a_j+
\lambda a_i\mathbf1\{i=j\},\qquad 0\leq\lambda<1.
\]

- k=2, 4, 8, 16; uniform, same-skew, or different-skew margins.
- Same skew: both use m_k(0.8). Different skew: P uses m_k(0.7),
  Q uses m_k(0.8), where m_k(ρ)=(ρ,(1−ρ)/(k−1),…).
- Null: shared MI .005, .02, .30. Power: I(P) = .02; I(Q) = .025, .03, .04.
- n=10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000 per group.
- Each null or power study has 360 settings, 100,000 independent pairs
  per setting.
- A Wald calculation needs a finite difference and a positive finite
  standard error. Expanded Welch also needs positive finite degrees of
  freedom.
- Rate = rejections from successful calculations / all repetitions.
  Calculation success is reported separately.

**Layout:** Construction equation in a shallow peach area; parameter grid
and calculation requirements in two readable columns. Keep the long n list full width.

**Answer:** “The copying probability changes association while preserving
chosen margins. I solve it separately for each target MI. Unsuccessful
calculations count as non-rejections, so the rate measures the complete
procedure; calculation success is reported separately. Conditioning on
success would describe a selected subset of sampled tables.”

**Notes:** Preserve Appendix B.3's full requirements: a Wald calculation
succeeds when it has a finite corrected difference, a finite positive
standard error, Vhat(P)+Vhat(Q)>10^-14, and a finite p-value. The Expanded
Welch calculation additionally requires positive finite component and
combined df and a finite p-value; if either component fails, the Expanded
Welch calculation is unsuccessful. If a sampled table has
Vhat = tauhat² = 0, the component formula requires 0/0, so the Expanded
Welch calculation is unsuccessful even when the other table makes the
shared standard error positive and finite. Zero and undefined component
df are distinct cases; both fail the positive-finite requirement. A failed
calculation is not evidence of equality. Sampling is independent within and between
populations; methods receive identical sampled pairs. This construction
uses the same vector for row and column margins within each population
and is one association family, not all categorical distributions.

**Source:** Chapter 5 and Appendix B.1–B.5; current grid CSVs. No
calibration or four-cell study.

### B4 / Slide 20 — Approximation ratios across table sizes

**Question:** Is the 4×4 example representative of other sizes and both
populations?

**Show:** Replot current Figure 6.1's six panels with the four table-size
curves, P and Q columns, and three rows: mean_ratio, variance_ratio,
plugin_variance_ratio. Filter to different-skew null-display IDs at shared
MI .02. Use log sample size, the original logarithmic y-axes and a line
at one. Keep each quantity's ratio direction. Supply shared legends and
outer labels, with chart text at about 13 pt.

**Answer:** “The larger tables generally have higher mean peaks, deeper
population-variance troughs, and slower recovery in this family. Sample
substitution can overpredict even while population inputs underpredict.
The main slide isolates one slice so these quantities can first be
understood separately.”

**Notes:** Figure 6.2 separately checks how those moment errors affect
df. In the worked 4×4/n=1,000 case, FO/target is about 0.73 and the exact
values are 15.30/21.03; B2 explains why. Do not infer the mean of estimated
df by inserting mean inputs into a nonlinear ratio. Full current Figure
6.2 remains in the thesis; it is not needed as another timed slide.

**Source:** Sections 6.1.1–6.1.2, Figures 6.1–6.2, and current moments.csv;
expected 80 rows: 4 sizes × 10 sample sizes × 2 populations.

### B5 / Slide 21 — Near-independence noise calculation

**Question answered:** Why do the mean estimated df remain near five?

**Show:** Setting: 4×4, n=1,000, MI 0.0001; d=9 and approximately
\(\kappa=2nI(P)=0.2\). Present

\[
G=2n\widehat I(P)\ \dot\sim\ \chi^2_d(\kappa),
\qquad \widehat\nu_P\approx G/2.
\]

Then a three-row editable table:

| Quantity | Local prediction | Observed |
| --- | --- | --- |
| Sample-based estimate (mean component df) | 4.60 | 4.86 |
| Target (from sampling moments) | 9.00 | 9.12 |
| Mean sample-based variance prediction / observed sampling variance | 1.96 | 1.97 |

In G, \(\widehat I(P)\) is the uncorrected plug-in MI, not a bias-corrected
estimate. Use the notes for the formulas
\((d+\kappa)/2\), \((d+\kappa)^2/(d+2\kappa)\), and
\(2(d+\kappa)/(d+2\kappa)\). State that the observed column is P.
The model predicts 9.00 for the target; do not claim the model predicts
the observed 9.12 exactly.

**Answer to give:** “Near independence, sampling noise creates apparent
association. The quadratic likelihood-ratio approximation includes that
noise. Substitution into the component formula gives roughly G divided by
two, whose mean is about 4.6 in this setting. The population first-order
formula instead approaches n times population MI. These are different
approximations, which explains their separation.”

**Source:** Thesis Appendix A.2 and Section 6.1.3; Figure 6.3. These are
local approximations under fixed dimensions and positive limiting cell
probabilities, not exact finite-sample distribution identities.

### B6 / Slide 22 — Full null results: uniform margins

**Question answered:** What happens outside the highlighted different-skew
16×16 example?

**Show/layout:** Replot all four table-size panels of Figure 6.4 in a
readable 2×2 grid, with all three MI levels and both methods. Share the
method and MI legends. Use about 13 pt labels and fewer ticks where
necessary. Preserve the original y-axis range for each table size and keep
those ranges identical in B6–B8. Retain the compact calculation-success strips.
Use shared labels and a few ticks to keep the four-panel view readable. State the all-repetitions denominator
in the footer and point to B3 for the calculation requirements.

**Answer to give:** “Under the copying construction, equal MI and uniform
margins give identical population tables. Their expected MI biases cancel
in the difference, but errors in the uncertainty estimate and reference
distribution can still cause excessive or conservative rejection. Increasing
shared MI changes those patterns.”

**Source:** Final Figure 6.4 and balanced-null combined rates, uniform
profile. This page contains all 120 settings for that profile.

### B7 / Slide 23 — Full null results: same-skew margins

**Question answered:** What changes when both populations have the same
uneven category frequencies?

**Show/layout:** The same layout and scale policy as B6, using all four
panels of Figure 6.5. Label P and Q margins as \(m_k(0.8)\). Retain
all MI levels, both methods and all ten sample sizes.

**Answer to give:** “The population tables are still identical under equal
MI, so expected bias in the difference cancels. Uneven margins leave more
rare category combinations. The conservative ranges persist beyond the
smallest samples and are not explained solely by calculation failures.
Expanded Welch lowers those already-low rates further.”

**Source:** Final Figure 6.5 and balanced-null combined rates, same-skew
profile. This page contains all 120 settings for that profile.

### B8 / Slide 24 — Full null results: different-skew margins

**Question answered:** Are the severe failures restricted to the largest
table, and what is visible over the complete margin-specific grid?

**Show/layout:** The same layout and scale policy as B6, using all four
panels of Figure 6.6. Label margins \(m_k(0.7)\) in P and \(m_k(0.8)\)
in Q. The main diagnostic table uses the .02/n=1,000 slice of these
populations.

**Answer to give:** “Here equal MI permits different population tables.
The remaining MI biases need not cancel, and in the sparse largest table
they can shift the estimated difference substantially away from zero.
The smaller-table patterns and the dependence on shared MI remain visible
in this complete slice of the null grid.”

**Source:** Final Figure 6.6 and balanced-null combined rates,
different-skew profile. This page contains all 120 settings for that profile.

**Additional anchor:** At MI .005, n=1,000, and 16×16, Wald is 36.38%
and Expanded Welch 34.38%, with every calculation successful in both
tests. This is a different shared-MI level from the diagnostic table's
.02; do not interchange the numbers.

### B9 / Slide 25 — Ordinary Welch degrees of freedom

**Question answered:** Would ordinary Welch degrees of freedom work as well
as the MI-specific calculation?

**Show:** One introduction line: “Same statistic and sampled pairs;
ordinary Welch gives each component \(n-1\) degrees of freedom; shared MI
0.02 nats”. Below it, an editable four-column table from final Table 6.2:

| Setting | Wald | Ordinary Welch | Expanded Welch |
| --- | --- | --- | --- |
| Uniform 4×4, n = 20 | 8.35% | 7.35% | 4.90% |
| Uniform 4×4, n = 50 | 4.87% | 4.57% | 3.24% |
| Different skew 16×16, n = 1,000 | 26.01% | 25.95% | 24.84% |

Add a quiet note beneath it: “False-positive rates; nominal target 5%.”
Then three short peach panels:

- **n = 20:** Ordinary Welch reduces the excess less than Expanded Welch.
- **n = 50:** Wald is already close to 5%; Expanded Welch is the most
  conservative.
- **Different skew 16×16:** Neither choice removes the excess caused by
  bias.

**Conclusion:** MI-specific degrees of freedom change the results, but a
larger reduction in rejection does not consistently improve calibration.

**Answer to give:** “Ordinary Welch keeps the same estimated MI difference,
standard error, and statistic, but gives each component n minus one degrees
of freedom, the rule for comparing sample means. For MI that is only a
benchmark, because it ignores how the pointwise-MI variance estimate
changes with the table. At n = 20 it removes less of the excess than
Expanded Welch. At n = 50, where Wald is already close to 5%, Expanded
Welch becomes the most conservative. In the biased 16×16 case neither
choice removes the excess. So the MI-specific calculation changes the
results, but a larger reduction in rejection does not consistently improve
calibration.”

**Notes:** The three settings reuse the main null study's 100,000 sampled
pairs per setting at shared MI 0.02 nats with n_P = n_Q = n; all three
methods' calculations succeed in every repetition. The thesis examines
ordinary Welch only at these illustrative settings and lists this as a
limitation (Section 7.2); the main comparison is with the Wald test.

**Source:** Thesis Section 6.2.5, Table 6.2; Section 7.2.

### B10 / Slide 26 — Full power results: uniform margins

**Question:** How does absolute power change with MI gap, sample size, and table size under uniform margins?

**Show:** Replot all four size panels of current Figure 6.7 with all
three gaps, both methods and ten sample sizes, common 0–100% power axes
and compact calculation-success strips. Retain thesis gap colours and method
line/marker encodings, explicitly labelled. There are 120 settings,
240 method rows for this margin profile.

**Answer:** “The complete uniform-margin grid shows the increase in
detection with sufficient observations and the stronger-gap advantage.
Larger tables need more data. Expanded Welch never exceeds Wald under
the usual thresholds, with method differences becoming small at larger
sample sizes.”

**Source:** Section 6.3.1, Figure 6.7; power rates, profile=uniform,
denominator=all. At n=10,000 and gap=.01, EW is 89.44% for 2×2 and 71.12%
for 16×16. These values describe the stated population family.

### B11 / Slide 27 — Full power results: same-skew margins

**Question answered:** Do the power patterns also occur when both groups
have the same uneven margins?

**Show/layout:** Replot all four panels of Figure 6.8 in a 2×2 grid, with
all gaps, both methods and a common 0–100% power scale. Retain compact
calculation-success strips, the all-repetitions denominator statement and the thesis
parameter/method encodings. This complements the uniform and different-skew examples in the main talk.

**Answer to give:** “These power curves use the same uneven margins in
both populations. Larger tables need more observations, and the smaller
MI gap remains harder to detect. For example, at n=50,000, the 16×16
Expanded Welch power is 79.87% for the smallest gap, compared with more
than 99.9% for each of the two larger gaps. The method difference is
smaller than these gap and setting effects at larger sample sizes.”

**Source:** Final Figure 6.8; Section 6.3.2; MI-gap combined rates,
same-skew profile. This page contains all 120 settings for that profile.

### B12 / Slide 28 — Full power results: different-skew margins

**Question:** How does the bias-related failure vary with gap and table
size?

**Show:** All four panels of current Figure 6.9, all three gap magnitudes,
both methods and ten n values, 0–100% power axes and compact
calculation-success strips. Use the explicit thesis gap/method legends. There are 120 settings,
240 method rows. Mark the 16×16/.01/n=1,000 point if it aids orientation.

**Answer:** “Unequal residual biases can shift the estimated difference
opposite to its true sign. The two-sided rate includes those rejections.
As the bias shrinks, rejection can first fall and later recover. Gap size
and margins therefore affect power through the estimator's behaviour as
well as the true separation.”

**Notes:** At the main point the mean estimate is +.0206714 for true
−.01. Of 9,662 EW rejections, 9,659 are positive and 3 negative.
Do not apply that conditional percentage to the entire grid or all
100,000 estimates.

**Source:** Section 6.3.3, Figure 6.9, and current power CSVs,
profile=different_skew, denominator=all.

### B13 / Slide 29 — References: MI and testing foundations

**Show/layout:** Follow preferred-reference page 25 and donor Slide 11's two-column bibliography,
using three entries per column, in Lato 14.5 pt with comfortable
paragraph spacing. Keep the common 28 pt black title and
white background. Use author, year, title, venue and DOI/URL where supplied.
Do not use a screenshot of a bibliography page. Retain published spelling
and names. Exact bibliographic text comes from the thesis `references.bib`.

Include these keys: `bossomaier2016`, `moddemeijer1989`, `paninski2003`,
`mora2009`, `satterthwaite1946`, `welch1947`.

**Speech:** No prepared narration. Use this page if a source is requested.
It is not part of the 20-minute talk.

### B14 / Slide 30 — References: related methods and evaluation

**Show/layout:** Four entries, two per column, in the same style and at the
same readable size as B13. Include `hutcheson1970`, `panwall2002`,
`morris2019`, `wald1943`.

**Speech:** No prepared narration. Do not add another thank-you or
conclusion page after the references.

## 8. Question preparation

Give a direct answer, a short reason, and a stopping point. Open a backup
when it clarifies the explanation. These are starting answers, not text
to read verbatim. Keep the cited boundary when the study did not evaluate
a proposed extension.

| Likely question | Suggested answer and boundary | Destination |
| --- | --- | --- |
| What exactly is new here? | “The MI first-order variance and the general Satterthwaite principle are established. I derive the MI variance sensitivity including the changing margins, use it for component df, and evaluate where the resulting approximation succeeds or fails.” Avoid a claim of global priority beyond the literature review. | B1–B2 |
| Why not just use sample size minus one? | “That assignment follows from the ordinary sample-variance distribution under normal sampling. An estimated pointwise-MI variance depends on changing probabilities and log ratios, so I calculate its sampling variability instead.” | B1–B2, B9 |
| Why does moment matching imply a Student t test? | “It motivates an approximate reference distribution. Matching a variance component to a scaled chi-squared distribution does not establish the standard normal numerator, or its independence from the variance estimates, that an exact Student t distribution requires.” | B2 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | B3, B8 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | B3; thesis Section 2.4 |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 13 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap, and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 11–12 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 11 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | B12; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 12 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | B5 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | B2, B5 |
| Could unsuccessful calculations explain the low rejection? | “They contribute at some small sample sizes. I report calculation success separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation succeeds.” | B3; Slides 9–10 and B6–B8 |
| Why count unsuccessful calculations as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to successful calculations would condition on a selected subset. Reporting calculation success separately makes the distinction visible.” | B3 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | B3; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | B3, B6–B12 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even when every calculation succeeds.” | Slides 9–13 |
| Why judge accuracy with a 4–6% band? | “The band is only descriptive: 4–6% gives 130 settings for Wald and 136 for Expanded Welch, but 4.5–5.5% gives 105 and 98. The answer rests on the pattern on Slide 9 and the mechanisms on Slide 10, not on a band.” | Slides 9–10 |
| Did you apply the tests to real data? | “Yes. Thesis Section 6.4 compares month–purchase and weekend–purchase MI between new and returning visitors in the Online Shoppers data. I left it out of this talk because unknown population tables cannot show which test is accurate; the known-population simulations carry that evidence.” | Thesis Section 6.4 |
| How much computation does one test require? | “The calculations use a fixed number of scans of an r-by-c table, so time and working memory are O(rc). I have not used this presentation to claim a measured runtime advantage over resampling.” | B1–B2; thesis Section 4.4 |

If a requested comparison was not performed, name that limitation and the
specific result established here. Do not invent a broader conclusion.

## 9. Rehearsal and timing control

Learn the argument before memorising wording. Rehearse from the purpose
and delivery cues after learning the scripts. Keep full scripts in notes.
A listener new to this derivation should be able to identify the research
question, the two levels of variance, the change in cutoff, and the main
reason that cutoff adjustment leaves some failures unresolved.

Allow pauses after introducing axes, between the two variance levels, and
after the signed-number comparison on Slide 12. Explain a chart before
moving to its mechanism panel. Do not read all numerical labels. Explain
which comparison they support. Rehearse the exported PDF as well as the
PowerPoint, including jumping from Slide 13 to backups and back.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 3 | 2:40 | Keep literature roles concise; do not recite citations. |
| End of Slide 6 | 7:25 | Use the short form of Slide 7; protect near independence. |
| End of Slide 8 | 11:05 | Shorten Slide 9's rate narration and read only its key comparison. |
| End of Slide 10 | 14:20 | Use the compact Slide 11 explanation; protect the directional result. |
| End of Slide 12 | 17:50 | Begin the conclusion immediately; do not open backups. If past 18:30, use the emergency close below. |

### Prepared shorter route

| Slide | Planned | Short form | Preserve |
| --- | --- | --- | --- |
| 2 | 1:15 | 1:00 | Two populations, their estimates, and the population hypothesis |
| 3 | 1:00 | 0:50 | Existing foundations and required MI-specific calculation |
| 4 | 1:20 | 1:10 | Shared statistic and visible cutoff difference |
| 5 | 2:05 | 1:40 | Two levels of variation, definitions of g and tau-squared, df consequence, and approximation status |
| 6 | 1:20 | 1:10 | Copying construction, parallel studies, sample size versus repetitions, and unsuccessful-calculation rule |
| 7 | 1:40 | 1:25 | Mean/variance distinction and the 19%, 3%, and 8% anchors |
| 9 | 1:30 | 1:20 | Axes and diagonal, improvement above 5%, no improvement below 5%, and remaining severe rejection |
| 10 | 1:45 | 1:35 | One line per row: difference-bias cancellation, underestimated or overestimated variation, and residual bias |
| 11 | 1:30 | 1:20 | Power definition, median/range, small-sample loss, and under 0.32 points at n = 10,000 |
| 13 | 1:00 | 0:50 | Three contributions, one finding per research question, scope, and the overall scientific finding |

These reductions total 125 seconds, giving **16:45**. Slides 8 and 12
remain at full length because they carry important explanations. Use this
route to simplify narration, not to speak faster.

### If Slide 12 ends at 18:30

- **Slide 13, about 50 seconds:** “I derived MI-specific variance
  sensitivity and degrees of freedom. The larger cutoff improves some
  excessive false-positive rates, while deepening conservatism and reducing
  power elsewhere. The remaining bias can even reverse the estimated
  direction. Improving estimation, retaining sampling variation near
  independence, and testing broader populations are the next steps.
  Thank you.”

This route finishes at about 19:20. Do not cut the conclusion, start
narrating backup slides, or fill spare time with an unplanned experiment.
Timing remains provisional until a complete timed rehearsal.

## 10. Implementation and acceptance

### Read and validate before authoring

- Read this revision and the version-2 manifest. Confirm the final-thesis
  hash in Section 1 (the manifest's hash predates the final submission)
  and the primary-reference path. The existing 16-main-slide deck
  and old metadata do not override this plan.
- Apply the manifest filters before styling; assert expected row counts,
  units, repetitions and method identities. Numeric comparisons use
  absolute tolerance 1e-12 and relative tolerance zero.
- Read `displays.csv` with `keep_default_na=False` in pandas. Its literal
  study label `null` otherwise becomes a missing value. Read numeric
  result files normally. Keep only the specified display IDs for RQ1.
- Slide 7 is now **P/4×4**, not the previous plan's P/16×16 slice. Its
  variance annotation concerns population inputs; the sample-input
  prediction is about 8% high at n=1,000, not 3% low.
- Slide 9 plots **all 360 null settings** (Wald against Expanded Welch).
  Its tallies report both directions of change. Do not retain old A/B/C
  case labels or favourable-only counters.
- Slide 10 is a **three-row diagnostic comparison** (thesis Table 6.1). Slide 11 shows the
  **power lost across all 360 power settings** by sample size, and Slide 12
  the **share of wrong-direction rejections across the different-skew
  grid**. These are summaries of the existing results, not new experiments.
- Keep component and combined df distinct; distinguish the moment target
  from an exact Student t distribution. B1's derivative is exact under its
  population assumptions; its sampling expansion is first order.
- Slide 12's conditional denominator is 9,662 EW rejections: 9,659 positive,
  3 negative. Do not turn over 99.9% into a percentage of all repetitions.
- Match citations to `references.bib`. Preserve published spelling and
  dataset identifiers; check Australian spelling in authored prose.

### Authoring sequence when execution is requested

1. Inspect the preferred 25-page PDF and use the 11-slide donor only for
   editable style/cover assets. Work on a separate copy in the versioned
   output directory. Preserve existing presentations.
2. Build the intended ending, Slide 13, then the shared-statistic and
   derivation Slides 4–5. Establish readable equations and definitions.
3. Filter and verify data for Slides 7–12 before designing their charts.
   Save selected rows and chart code with the new presentation assets.
4. Build the opening and literature around the knowledge those results
   need. The opening must present the actual statistical problem.
5. Add the mechanism panels, local numerical anchors and full speaker
   notes. Keep visual instructions out of rehearsal notes.
6. Build the 14 backups and update Slide 13's notes index with physical
   slide numbers. Rehearse likely questions.
7. Inspect every rendered page, compare it with the relevant preferred
   reference page and rehearse to the timing table. Correct genuine
   problems without adding new scientific material.

### Proposed outputs

Under `/Users/danielzhao/MyMac/Masters Degree/Research/Thesis Presentation/`, the current
version:

- `Daniel_Zhao_Welch_MI_Presentation.pptx`: 13 main slides, one appendix title slide and 14 backup slides,
  editable text/equations/tables, complete notes.
- `Daniel_Zhao_Welch_MI_Presentation.pdf`: matching 28-page PDF, including
  backups and references, suitable for upload.
- `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md`: final speech,
  timings, cues and short route, synchronised after rehearsal.
- `assets/`: selected data, scientific plots and authoring sources.

These are outputs for Daniel to update separately. This task updates this plan only,
without building slides, changing the thesis or committing/pushing git.

### Final review criteria

Check the scientific argument as well as the appearance:

- Can a new reader identify each slide's point from its lead and evidence?
- Does the necessary mechanism appear beside the evidence, rather than
  relying on several spoken definitions that disappear on advancing?
- Does each numerical comparison state what is held fixed and changed?
- Do key values attach to a point or row, with correct denominators?
- Can the two method curves be followed without repeated legend searches?
- Do the results establish conditional benefit, power cost and remaining
  estimation error without implying a universal recommendation?
- Are all six rubric content areas covered, including limits/future work?

Inspect every slide for clipped text, overlapping labels, unreadable
axes, misleading crops, altered units, incorrect colours and leftover
proposal content. Compare the cover with preferred page 1, the method with
pages 4–5 and explanatory result layouts with pages 7–10. The new deck
should share their explanatory clarity, while using current evidence.
Check native text/equation editability, font substitution, complete PDF
export and agreement between PDF and PowerPoint. Check that the smallest
text (12–13 pt chart labels and 10.5 pt footers) stays legible in the room
and on the uploaded PDF; raise panel text to 15–16 pt if it does not. Add
actual scheduling or
mandatory Canvas details only when known.

Full product-rule algebra, all grid panels, calculation requirements
and the local chi-squared calculation stay in the thesis/backups. The
removed calibration and four-cell studies stay excluded. No new analysis
is needed for this replan: its figures select existing results.

## 11. Revision and verification record

**Conclusion slide split (11 November):** Slide 13's “Contribution and
findings” row is now two separate elements. “Contributions” shows the
thesis's three contributions (Section 1.3: derivation, test construction,
and empirical evaluation) as the highlight: stronger peach cards with large
orange numerals. “Findings by research question” gives one pale-blue card
each for RQ1–RQ3, with navy RQ tags, following thesis
Sections 7.1.1–7.1.3; the RQ1 finding is new to this slide and matches
Slides 7–8. The scope line stays, and the next steps become two arrow items. The
Slide 13 script names
the three contributions, then gives one finding per research question; it
is 14 words longer (about six seconds), within Slide 13's minute. Other
slides are unchanged. The deck in
`Thesis Presentation/` was updated in place.

**Cell-probability backups (11 November):** Two new backups follow B1.
“B1 continued” (physical Slide 16) is a grid that gives each quantity as
an expectation, variance, or derivative beside its sum over cell
probabilities: pointwise MI, MI, V, the row and column means of pointwise
MI, g, tau-squared, and the component df. “B1 worked example” (Slide 17)
works through thesis Section 4.4.1: table N^P, cell (1, 1) step by step
(sensitivity 0.422), the sensitivities of all nine cells, tau-squared 0.932
and 16.65 component df. All values were recomputed from the counts and
match the thesis. Slide 5's source line now points to Slides 16–17. B2–B14
move to physical Slides 18–30; their B numbers are unchanged. The deck in
`Thesis Presentation/` was updated in place.

**Hats (11 November):** Inline hatted symbols (V-hat on Slides 4, 6, 7
and 8 and B4; Δ-hat BC on Slide 4; I-hat on B5; ν-hat and the other
component-df symbols in Slide 8's footer) were typed as a letter plus a
combining circumflex, which PowerPoint positions poorly. They are now inline
native equations, like the display equations, so PowerPoint places the hat
correctly. The preview PDF still shows the plain-text fallback. The deck in
`Thesis Presentation/` was updated in place.

**Review corrections (10 November):** Checked against the exact rejection
counts. Slide 9: of the 180 settings where Wald is below 5%, Expanded Welch
is further below in 176 and unchanged in four (previously “all 180”); the
lead now says it never brings these rates closer to 5%; the 4–6% count is
labelled a descriptive band (4.5–5.5% gives 105 versus 98), with a new
Section 8 question. Slide 12's chart note now says percentages are rounded
and that 50% means half the rejections have the wrong sign (the outlined
cell is 99.97%, with three correct rejections). Slide 13's third finding
restores the testing rule: “At the same nominal 5% threshold, power is no
higher.” Slide 8's orange line is labelled “mean sample-based estimate”.
Slide 11's second panel now reads “Small MI gaps can stay hard to detect”,
and its script says the shading is a range across settings, not Monte Carlo
uncertainty. Cues on Slides 7, 8, 9, 11 and 12 now start with a pause when
the graph appears. The deck in `Thesis Presentation/` was updated in place.

**Alternative hypothesis (10 November):** Slide 2 now states both
hypotheses from thesis Equation 1.1, H₀: I(P) = I(Q) against
H₁: I(P) ≠ I(Q), in a box labelled “Hypotheses”. This sets up the
two-sided framing that Slides 11 and 12 rely on. The Slide 2 script adds
“against the two-sided alternative that they differ”; the timing is
unchanged. The deck in `Thesis Presentation/` was updated in place.

**Whole-grid results (9 November, late night):** Slides 9, 11 and 12 now answer RQ2 and RQ3 across the whole grid instead
of single settings. Slide 9 plots all 360 null settings (Wald against
Expanded Welch): where Wald is above 5% (178 settings), Expanded Welch is
closer in 165; where Wald is below 5% (180), it is further away in all
180; settings within 4–6% rise only from 130 to 136. Slide 11 shows power
lost across all 360 power settings by sample size. Slide 12 shows the
share of wrong-direction rejections across the different-skew grid
(0.01 gap), with the thesis example outlined; at least 90% of rejections
point the wrong way in 28 settings, all different-skew. These tallies come
from the thesis simulation results but are not printed in the thesis.
A formatting pass then added “360 settings per study” to Slide 6's grid
panel, evened its research-question spacing and reworded its model line;
matched Slide 13's findings to Slides 9–12; added “(log scale)” to
Slide 9's y-axis; and aligned the B3, B4 and B5 labels with Slides 6–8
(I(P) and I(Q); “population-based inputs”; “target” and “sample-based
estimate”). Titles: Slide 9 “RQ2 results: false positives across all null
settings”, Slide 11 “RQ3 results: the power cost of the larger cutoff”.
Slide 10 restores the uniform 4×4, n = 20 row of thesis Table 6.1, so its
three rows (standard error too small, standard error too big, bias)
explain the three patterns on Slide 9; its title is now “RQ2 results: why
the cutoff helps, hurts, or cannot fix it”. Scripts, cues, sources,
lessons 6–7 and the shorter route change to match; the timings are
unchanged. The deck in `Thesis Presentation/` implements this revision; the
application-removed version moved to `Earlier versions/app_removed_2026-11-09/`.

**Application removed (9 November, night):** Daniel removed the Online
Shoppers application so the talk does less in its 20 minutes.

- Slide 2 shows two generic populations, P and Q, with count-table icons
  and their MI estimates. It names no dataset and shows no sample sizes or
  estimates. Its script, cue and source change to match, and Slide 1's
  transition no longer mentions the shopping example.
- The application slide and B13 (Application details) are removed, with
  the Sakar and Kastro (2018) reference and the three application questions
  in Section 8. Section 8 adds a short answer for “Did you apply the tests
  to real data?”, pointing to thesis Section 6.4.
- Conclusions is now Slide 13, the appendix title is Slide 14, and B1–B14
  are Slides 15–28; the references become B13–B14. Slide 12's transition
  now leads to the conclusion.
- The freed 1:05 goes to Slides 5 (+0:25), 8 (+0:20) and 12 (+0:20), so the
  talk still ends at 18:50. The checkpoints, shorter route and emergency
  close are updated to match.
- Slide 7's navy curve is labelled “population-based inputs”, parallel to
  “sample-based inputs”, on the chart and in the callout.
- Slide 8's lines are relabelled “target (measured from 100,000 samples)”,
  “sample-based estimate” and “population-based value”, and recoloured
  charcoal, orange and dotted navy so the colours mean the same as on
  Slide 7. A bracket marks “about half the target”, the y-axis says
  “(log scale)”, and the lead, panels, callout and script use the same
  names. The footer keeps the thesis symbols.
- This revision's deck is now in `Earlier versions/app_removed_2026-11-09/`;
  the research-question-label version moved to
  `Earlier versions/rq_labels_2026-11-09/`.

**Research-question labels (9 November, evening):** The six results titles
now name the research question each slide answers, matching the RQ labels
on Slide 6 and thesis Sections 6.1–6.3: Slides 7–8 begin “RQ1 results:”,
Slides 9–10 begin “RQ2 results:”, and Slides 11–12 begin “RQ3 results:”.
Slide 13 keeps “Illustration:” because the application (thesis Section 6.4)
answers none of the three questions. Slide 6's RQ3 box writes the fixed MI
as “I(P) = 0.02”, replacing “P MI 0.02”. Other slide content, notes, and
timings are unchanged. This revision's deck is now in
`Earlier versions/rq_labels_2026-11-09/`; the submitted-thesis version
moved to `Earlier versions/submitted_2026-11-09/`.

**Submitted-thesis revision (9 November):** The submitted thesis adds
subsections in Chapters 2–5 and the appendices, restructures the Chapter 4
derivation, renumbers some Chapter 4 equations, and applies Oxford commas.
Its chapter, section, figure, and table numbers used in the deck are
unchanged, and every number on the slides still appears in it. The deck
changes only where its wording or references differ from the thesis:

- Distribution names are complete, as in the thesis: Slide 3's Wald cell
  says “the fixed cutoff from the standard normal distribution”, Slide 5
  lists “Matching a scaled chi-squared distribution”, and the Slide 3 and
  Slide 4 scripts and source name the standard normal and Student t
  distributions in full. Slide 4's script says “the Wald test” and “the
  Expanded Welch test”.
- B2's caveat names the conditions an exact Student t distribution
  requires: a standard normal numerator independent of the variance
  estimates (thesis Section 4.1.1). The B2 answer, B2 notes, and the
  matching Section 8 answer use the complete name of the scaled chi-squared
  distribution.
- B2's page range is now pp. 23–36, and B1's notes say “Assumptions” for
  the list of conditions.
- This revision's deck is now in `Earlier versions/submitted_2026-11-09/`;
  the review version moved to `Earlier versions/final_2026-11-08_v2/`.

**Review revision (8 November, afternoon):** These changes follow a content
review of the final deck. The argument, evidence, and timing table are
unchanged.

- Slide 6's script now gives the count correctly: four table sizes, ten
  sample sizes, and three margin regimes make 120 combinations for each MI
  level or gap, and three levels or gaps make 360 settings. B3 says “Each
  null or power study”.
- Slide 4 defines \(V(P)\) and \(\widehat V(P)\). Slide 5 has a simpler
  lead.
- Slide 7's callout and script separate the two variance predictions at
  n = 1,000: 3% low with population inputs and 8% high with sample-based
  inputs (the implemented calculation).
- Slide 8 defines the sampling-moment target in a caption under the chart
  and in the script before interpreting it.
- Slide 14 says “Lower power under the same 5% testing rules”, adds a scope
  line (one population construction, equal sample sizes, and the Wald test
  as the main benchmark), and words the first next step as reducing bias in
  the estimated MI difference and improving its standard error and degrees
  of freedom.
- Slide 2 adds “on average” and “Summarise a sample from each population in
  a count table”. Slide 3 names the Wald test. Slide 4 and B2 say “Student t
  distribution” instead of “Student t reference”.
- Slide text, speaker notes, and Sections 8–9 use Oxford commas in lists of
  three or more, following the prose guidelines. Reference entries keep
  their citation format.
- The deck in `/Users/danielzhao/MyMac/Masters Degree/Research/Thesis Presentation/` implements this revision.
  It was first saved as `Thesis Writeup/Welch MI/presentation/final_2026-11-08_v2/`
  and moved there for easier access, followed by the earlier versions and
  this plan.
  Its speaker notes are copied from this plan without replacements. The
  scripts and transitions total 1,937 words, 62 more than before, which
  leaves less of the 70-second margin; confirm timing in rehearsal.

**Final-thesis revision (8 November):** The plan now follows the final
submitted thesis. Wording, numbers and notes changed as follows; timings
and the main argument are unchanged.

- “Normal Wald” is now “Wald” or “the Wald test” (thesis Section 3.3), and
  Slide 3 cites Wald (1943).
- “Common MI” is now “shared MI”, matching the captions of thesis
  Figures 6.4–6.6.
- “Valid” and “validity” are now “successful calculation” and “calculation
  success”, matching thesis Appendix B.3. B3 and its notes state the full
  requirements, including the 0/0 case.
- Slide 13 reports unadjusted two-sided p-values (month: Wald
  4.71 × 10⁻⁵, Expanded Welch 3.73 × 10⁻⁴). Its weekend panel now shows
  its p-values (0.9554 and 0.9601). The Holm adjustment and six-comparison
  family are removed from the slide, script, cue, source and Section 8.
- New B9 presents the ordinary Welch comparison (thesis Section 6.2.5,
  Table 6.2). The power backups move to B10–B12 and the references to
  B14–B15. B13 replaces the six-comparison table with the two Online
  Shoppers comparisons from Tables 6.3–6.4.
- B1's notes add the Appendix A.3 equivalence between positive MI and
  positive V when every cell is positive.
- References add Wald (1943) and remove Holm (1979).
- The deck now in `Earlier versions/final_2026-11-08/` implements this revision.
  Its scripts and transitions total 1,875 words.

**Formatting revision (5 November, evening):** Section 4 now specifies
smaller type, lighter components and more white space, replacing the
earlier 34–36 pt titles, 20–22 pt leads, 22–24 pt body text, solid header
bars and dashed callouts. The slide-level sizes for the appendix title, B1,
B4, B6–B8 and B13–B14 (now B14–B15) follow it. This revision changes no wording, numbers,
speaker notes, timings or evidence.

The 5 November replan combines the opening material, replaces the main
expanded derivative display with a derivation chain, uses the 4×4 moment
example, covers all three common MI levels in grouped bars, and pairs a
simple power curve with a three-gap table. It restores the explanatory
bias contrast and merges limitations/future work into the conclusion.
Near independence and wrong-direction rejection each retain a full main
slide. Wider grid coverage moves to labelled backups.

The matching version-2 manifest records source hashes, exact selections,
row counts, values, 14-slide timing and 14-backup numbering. Verify those
checks before using the plan. Current thesis, source package and existing
presentations are preserved. Rendering and actual speech timing remain
execution/rehearsal checks, not results of this planning task.

Planning checks completed on 5 November: all main selections and displayed
rates match the saved outputs; 22 source hashes were verified. The 14 main
slides, 14 backups, 22 question responses, 18:50 allocation and 16:45
shorter route agree with the manifest. The scripts and transitions contain
about 1,900 words, with time reserved for explanation and graph reading.
Australian spelling, equation delimiters and cross-references were checked.
The 88 protected source, thesis, delivery and existing-presentation files
were unchanged. These checks establish a consistent handoff; they do not
substitute for rendering the future slides or timing a live rehearsal.
