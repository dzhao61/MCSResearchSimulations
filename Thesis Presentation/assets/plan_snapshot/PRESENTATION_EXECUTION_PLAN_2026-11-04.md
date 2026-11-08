# Presentation execution plan

Originally prepared on 4 November 2026. **Substantively replanned on
5 November 2026** following Daniel's preference for the supplied
*Comparing MI in Finite Samples* presentation. Keep this filename stable.
This revision replaces the 16-main-slide plan.
**Updated on 8 November 2026** to match the final submitted thesis; Section
11 lists the changes.

## 1. Execution brief and sources

Create **14 main slides, one appendix title slide and 15 backup slides**,
30 slides in total. The
main talk targets **18:50**, leaving 70 seconds before the university's
20-minute limit. Keep Slide 14 visible during questions. Backups begin at
physical Slide 16, after the appendix title on Slide 15. The appendix title
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
the current version (review revisions) at the top, this plan and its
manifest in `Planning/`, and the earlier versions in `Earlier versions/`:
`original_16_slide/`, `replanned_2026-11-05/` and its revisions
`replanned_2026-11-05_v2/` (appendix title), `replanned_2026-11-05_v3/`
(lighter formatting), and `final_2026-11-08/` (matched to the final thesis).
Preserve the earlier versions. Until 8 November these lived in
`Thesis Writeup/Welch MI/presentation/` and `Thesis Writeup/Welch MI/notes/`.

Other project paths are relative to:
`/Users/danielzhao/MyMac/Masters Degree/Research/Simulations`.

| Authority | Source and role |
| --- | --- |
| Science | `/Users/danielzhao/MyMac/Masters Degree/Research/FINAL SUBMISSION/Daniel_Zhao_Welch_MI_Thesis.pdf`: final submitted 109-page thesis, 8 November 2026, SHA-256 `61257162c884db9d4e822dd1b99c13130f3a7b4fc930ee42edb9bcf9a0470697`. It is identical to `Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis_Signed.pdf`. |
| Primary presentation reference | `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/Comparing MI in Finite Samples.pdf`, 25 pages: 14 main slides, an index and 10 supporting pages. Follow its explanatory approach and visual hierarchy. |
| Editable design donor | `/Users/danielzhao/MyMac/Masters Degree/INFO5993/A4/Zhao_Daniel_Presentation_vF2.pptx` and matching PDF, 11 slides. Reuse original cover artwork and suitable editable styling. |
| Numerical evidence | `PRESENTATION_EVIDENCE_MANIFEST_2026-11-04.json`, version 2. Its filters, row counts and simulation values still apply. It predates the final thesis: its thesis hash is the 4 November build, its `backup_9_to_11` and `backup_12` entries are now B10–B12 and B13, and its Holm values and six-comparison application rows are no longer used. B9 uses final Table 6.2; Slide 13 and B13 use final Tables 6.3–6.4 and the application CSV. |
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

1. Open with groups, tables, estimates and the population hypothesis on
   one page. Return to the shopping question near the end.
2. Make the literature explain what the method needs. Identify the
   MI-specific calculation without an unverified global priority claim.
3. Show relationships in the derivation before its final formula. Keep
   the expanded derivative in B1.
4. Give each result a complete explanatory point: setting, observation,
   mechanism and implication together. Necessary explanation stays visible.
5. Keep numbers beside their plotted point or table row. Avoid requiring
   recall of earlier values to understand a new comparison.
6. Keep main comparisons simple: stable method colours, two curves or
   grouped bars. Use a local table for the three power gaps and backups
   for full grids.
7. Label selected examples as slices of balanced studies. They do not
   become favourable cases used to define the power experiment.
8. Lower rejection follows from the cutoff. The experiments establish
   its magnitude, conditional accuracy, cost and remaining estimator errors.

The sequence is: concrete question, literature, shared statistic, derivation,
evaluation, approximation limits, false positives, their mechanism, power,
wrong direction, application, conclusion and next steps. A separate agenda
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
- RQ1: colours identify quantities. Slide 7 uses navy population inputs
  and orange sample inputs. Slide 8 uses navy moment target, orange mean
  estimate and dotted grey population first-order value. Label directly.
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
  These are not simultaneous intervals over the grid. Snapshot tables
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
| 5 | Approach and contribution | 1:40 | 5:40 |
| 6 | Evaluation design | 1:20 | 7:00 |
| 7 | Results: approximation accuracy | 1:40 | 8:40 |
| 8 | Results: near independence | 1:40 | 10:20 |
| 9 | Results: false positives across shared MI values | 1:30 | 11:50 |
| 10 | Results: why bias changes rejection | 1:45 | 13:35 |
| 11 | Results: power across MI differences | 1:30 | 15:05 |
| 12 | Results: bias can reverse the estimated direction | 1:40 | 16:45 |
| 13 | Illustration: online shopping data | 1:05 | 17:50 |
| 14 | Conclusions and next steps | 1:00 | 18:50 |

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

**Transition:** “The shopping example gives a concrete reason to make this comparison.”

**Source:** Final title, abstract, and Chapter 1; preferred-reference page 1.

### Slide 2 — Motivation: comparing MI across populations

**Purpose:** Connect the application, sampling uncertainty and hypothesis.

**On-slide content:**

**Lead:** Mutual information measures how much observing one variable
reduces uncertainty about another, on average. Different sample estimates
can arise from sampling noise.

\[
H_0:I(P)=I(Q)
\]

**Online shoppers**

- P: new visitors; 1,694 sessions; corrected MI estimate 0.0043 nats.
- Q: returning visitors; 10,551 sessions; corrected MI estimate 0.0179 nats.
- Variables: month of visit and purchase outcome.

**Statistical task:** Summarise a sample from each population in a count
table. Estimate MI from each table. Assess whether sampling noise can explain the difference.

**Question:** Does month–purchase MI differ between the populations?

**Layout and evidence:** Adapt preferred-reference page 2. Put the
hypothesis in a shallow peach area. At left align groups, generic table
icons and estimates; at right use three connected task steps. The icons
are schematic and encode no invented counts or heatmap values; the actual
month tables are 10×2. These are sample estimates, not population MI.
The counts provide context and need not be read aloud.

**Speaker script:**

> Mutual information measures the average reduction in uncertainty about one variable when we observe another. Here the variables are the month of a website visit and whether the session ends in a purchase. I compare that association between new and returning visitors, whose population tables I call P and Q.

> The corrected sample estimates are about 0.0043 and 0.0179 nats. Their difference motivates the question, but different samples can produce different estimates even when population MI is equal. The null hypothesis therefore equates the two population MI values. It allows different probability tables. We need to account for sampling uncertainty before interpreting the observed difference. I will return to the application after checking the comparison in known populations.

**Delivery cue:** Trace groups into estimates, then point to the null.
Do not announce the application p-values yet.

**Transition:** “The literature supplies several parts of that comparison, with one additional MI-specific calculation needed.”

**Source:** Thesis Sections 1.1, 2.1, and 6.4; application row shoppers_month;
Bossomaier et al. (2016).

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
| Required step | Track variation in the variance estimate itself | Assess the fixed normal cutoff in finite samples | Calculate the MI-specific variance sensitivity |

**Contribution:** Derive that sensitivity and evaluate the resulting
degrees of freedom.

**Layout and evidence:** Use preferred-reference page 3's three-column
matrix, orange labels and light rules. Keep citations secondary to the
ideas. Put the contribution in one pale peach strip, with "Contribution:"
in bold orange. Avoid an unverified
claim that no equivalent formula has appeared anywhere.

**Speaker script:**

> The project builds on three established strands. Work on MI supplies the estimator, its leading bias correction, and its first-order sampling variance. The Wald test uses those estimates with a standard normal reference. Welch and Satterthwaite instead use variance moments to choose degrees of freedom, with related applications in entropy and other statistical comparisons.

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

> Both tests divide the corrected MI difference by the same estimated standard error. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Independence between the samples lets their two variance contributions add.

> Wald compares the statistic with the standard normal distribution. Expanded Welch uses a Student t distribution with degrees of freedom estimated from the tables. The illustration uses five degrees of freedom: its heavier tails move the two-sided cutoff from about 1.96 to 2.57. Actual estimated values vary. The larger cutoff means Expanded Welch's rejections are a subset of Wald's under the implemented rules. The experiments assess whether that reduction helps accuracy and how much detection it costs.

**Delivery cue:** Point to the common denominator, then cutoffs. Do not
imply the illustrated difference is typical of every dataset.

**Transition:** “Choosing the degrees of freedom requires the variability of the variance estimate itself.”

**Source:** Thesis Chapters 3–4 and Figure 2.1; standard normal and
Student t(df=5) quantiles.

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

**Two approximations evaluated:** first-order sampling expansion; scaled
chi-squared moment matching.

**Layout and evidence:** Follow preferred-reference page 5. Use four short
connected blocks above, identifying the sensitivity and df as the project's
calculation. Below, put the result in a pale-blue area with the two
approximation labels beside it. Define tau-squared locally. Keep the
expanded derivative in B1. Each block explains a relationship rather than
merely naming a technical object.

**Speaker script:**

> There are two levels of variation. V-hat describes variation in pointwise MI, but V-hat itself changes when a new sample produces a different table. I calculate how V changes when a small amount of probability moves towards one cell. That perturbation changes the cell weights, margins, and log ratios together. The sensitivity g collects those effects.

> Averaging observation-level sensitivities gives a first-order approximation to the sampling error of V-hat. Its sampling variance is therefore approximately tau-squared divided by sample size. Satterthwaite moment matching uses twice the squared mean of a variance estimate divided by its sampling variance. Substituting the sample-based inputs gives the component formula shown here. Greater variation relative to the squared mean gives fewer degrees of freedom. I repeat the calculation for Q and combine the components.

> The derivative is an exact calculation for positive population tables. Its sampling expansion and the moment-matched Student t distribution are approximations, which motivates the first evaluation question.

**Delivery cue:** Pause between V-hat and its sampling variance. Explain
the chain before the formula. The displayed df are component df, not the
combined test df.

**Transition:** “Known population tables let me check those approximations before assessing test decisions.”

**Source:** Thesis Sections 4.1–4.3; eq:g-final,
eq:vhat-sampling-variance, eq:nu-p-hat, and eq:expanded-df. B1–B2 retain the
full derivative and moment-matching argument.

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
| RQ3: Power | P MI 0.02; MI-gap magnitudes 0.005, 0.01, and 0.02 nats |

**Shared simulation grid**

- Four sizes: 2×2, 4×4, 8×8, 16×16.
- Uniform, same-skew, and different-skew margins.
- Ten sample sizes: 10 to 50,000 observations per population.
- 100,000 independent table pairs per setting.

**Model:** Copying construction: choose margins and solve for target MI.

**Reporting:** Usual 0.05 p-value thresholds. Unsuccessful calculations
count as non-rejections; calculation success is reported separately.

**Layout and evidence:** Follow preferred-reference page 6. Put questions
in a navy-headed area at left and settings in an orange-headed area at
right. Keep sample size and repetition count distinct. Put reporting below.
State 360 settings each for null and power in speech/notes, without another
counter. Exact vectors, sample sizes, and requirements are in B3.

**Speaker script:**

> I construct population tables with known MI using a copying model that preserves chosen margins. RQ1 checks the variance approximations and the resulting degrees of freedom. The null study uses three shared MI values, while power fixes MI in P at 0.02 nats and makes Q larger by three gaps. Nats are MI units based on natural logarithms.

> Both test studies cross four table sizes, ten sample sizes, and three margin regimes, giving 120 combinations for each MI level or gap. With three levels or gaps, each study has 360 settings. The uneven margins either agree between populations or differ. Every test sees only its two sampled tables. Repeating the comparison 100,000 times measures performance without increasing the observations available to one test. Both methods use the same pairs and usual p-value thresholds. Unsuccessful calculations count as non-rejections, with calculation success tracked separately.

**Delivery cue:** Name what varies and stays fixed. Do not recite ten
sample sizes or restore fitted-threshold experiments.

**Transition:** “The first result shows why accurate variance prediction can coexist with an inflated mean.”

**Source:** Thesis Chapter 5, Tables 5.1–5.3, and Appendix B; Morris et al.
(2019). Current balanced-null and MI-gap grids.

### Slide 7 — Results: approximation accuracy

**Purpose:** Teach the two moment errors using the clear 4×4 example.

**On-slide content:**

**Lead:** The mean of V-hat can remain inflated even when its population
first-order sampling-variance prediction is accurate.

**Setting:** Different-skew P; 4×4; population MI 0.02 nats.

- Top plot: mean of \(\widehat V\) / population \(V\).
- Bottom plot: predicted / observed sampling variance of \(\widehat V\).
- Bottom curves: population inputs; sample-based inputs.

**Mean: rare cells can inflate it.** Newly observed rare cells can have
large pointwise-MI deviations, whose squares raise V-hat.

**Sampling variance: linearisation can miss large changes.** Rare cells
appear in some samples and not others; sample-based sensitivities can also
overpredict the resulting variation.

**At n=1,000:** mean 19% high; variance prediction 3% low with population
inputs and 8% high with sample-based inputs. Both moments enter the degrees
of freedom.

**Layout and evidence:** Follow preferred-reference page 7. Stack two
white plots at left, with the two mechanism panels at right and numerical
conclusion beneath. Use P/4×4 null-display rows from current moments.csv.
Top: mean_ratio in neutral charcoal, linear y=0–5.5. Bottom:
variance_ratio and plugin_variance_ratio, linear y about 0.4–1.7. Both use log sample size and
a reference at one. The bottom plot uses navy population inputs and orange
sample-based inputs, directly labelled as quantities. At n=1,000 label the
top +19% and the population-input curve −3%. Retain narrow approximate 95%
Monte Carlo bands. Do not call the sample-based prediction 3% low.
B4 supplies wider table-size/P/Q context.

**Speaker script:**

> This is one population and a four-by-four table, so the two moment errors can be read together. On top, one would mean the average V-hat equals the population variance. The mean rises above that benchmark and then recovers. When rare cells first appear, their estimated pointwise MI can lie far from the table's MI. The squared deviations can inflate V-hat until repeated counts stabilise the estimates.

> The lower graph concerns the sampling variance of V-hat itself. The navy curve uses known population inputs; the orange curve estimates those inputs from each sample. The population prediction misses variation when rare cells appear in some samples and remain absent in others. Estimating the sensitivities from sparse counts can instead overshoot. Larger samples improve both predictions.

> At one thousand observations, the population prediction is about three percent low, while the sample-based prediction is about eight percent high. The mean is still nineteen percent high. Since the degrees-of-freedom calculation squares the mean input and divides by the variance input, a good variance prediction alone does not make that calculation accurate.

**Delivery cue:** Explain the top graph before the bottom. Say “sampling
variance of V-hat”. Tie both annotations to n=1,000.

**Transition:** “Near independence, an additional separation appears because sampling noise creates apparent association.”

**Source:** Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2; null-display IDs,
side=p, k=4, profile=different_skew, MI=.02. B2 retains the numerical df
consequence of this same example.

### Slide 8 — Results: near independence

**Purpose:** Keep the important near-independence check in the main story
and explain the three distinct quantities.

**On-slide content:**

**Lead:** Near independence, sampling noise keeps the mean estimated
component degrees of freedom positive while the population first-order
value becomes very small.

**Setting:** Different-skew P; 4×4; n=1,000 fixed.

**Population first-order value:** Insert known population inputs into the
component formula. Near independence, its local value is approximately
n × population MI.

**Sample estimate:** Quadratic sampling errors create apparent association,
which remains in the sample-based calculation.

**At MI 0.0001:** mean estimated component df ≈4.9; sampling-moment target
≈9.1; population first-order value ≈0.1.

**Chart caption:** Sampling-moment target: component degrees of freedom
calculated from the repeated-sample mean and variance of V-hat.

**Layout and evidence:** Follow preferred-reference page 8. Place a large
chart at left, two short explanations at right and one numerical callout
beneath them. Plot df_mean, nu_mom and nu_fo for the P/4×4/n=1,000
association-display rows against MI, both axes logarithmic. Use orange for
the mean estimate, navy for the target and dotted grey for the population
first-order value, with direct labels. These are quantities, not methods.
Preserve all seven MI values. The target is not “true t df”. B5 explains
the local prediction and compares it with observations.

**Speaker script:**

> Here sample size stays at one thousand while population MI approaches zero. The grey line inserts known population inputs into the first-order component formula and becomes very small. The orange curve, the mean component degrees of freedom estimated from sampled tables, stays near five at the weakest association. The navy moment target is the component degrees of freedom calculated from the repeated-sample mean and variance of V-hat. It is near nine, so the mean estimate is still only about half that target.

> At independence, population pointwise MI is zero and the linear sampling contribution vanishes. Sampled tables nevertheless contain apparent association from quadratic sampling errors. The sample-based calculation retains that noise, which explains why its mean stays positive instead of following the population value towards zero. The local calculation in the thesis predicts a mean near 4.6 here, against the observed 4.9. This explains the separation while also showing the limits of the first-order approximation.

**Delivery cue:** Point to the low-MI end and explain each curve once.
Preserve this slide in every shorter route. The calculation does not prove
an exact Student t distribution.

**Transition:** “The decision-level question is whether the larger cutoff brings false positives towards five percent.”

**Source:** Thesis Section 6.1.3, Figure 6.3, and Appendix A.2; observed
mean 4.859787, target 9.124808, and first-order value .096400.

### Slide 9 — Results: false positives across shared MI values

**Purpose:** Show all three shared-MI levels with a controlled comparison
and stable method colours.

**On-slide content:**

**Lead:** A larger cutoff brings some excessive false-positive rates closer
to 5%, but accuracy at one association level does not persist across
shared MI values.

**Setting:** Uniform 4×4; n=20 per population; equal MI in P and Q.

| Shared MI (nats) | Wald | Expanded Welch |
| --- | --- | --- |
| 0.005 | 7.61% | 4.16% |
| 0.02 | 8.35% | 4.90% |
| 0.30 | 15.86% | 13.11% |

**Nominal target: 5%.** Both tests’ calculations succeed in every
repetition in these examples.

**Interpretation:** The larger cutoff reduces rejection, while the shared
statistic can still have the wrong sampling distribution.

**Layout and evidence:** Use preferred-reference page 9's annotated grouped
bars. The table above specifies chart data; do not also project a duplicate
table. At left draw three shared-MI groups, navy Wald and orange Expanded
Welch, saved 95% whiskers, direct rate labels and a 5% reference. Use linear
y=0–20%, starting at zero. At right explain the .02 improvement from 8.35%
to 4.90%, then the .30 failure remaining at 13.11%. Keep the
calculation-success sentence below. These are slices of the balanced grid, not
selected power-design cases. Full null grids in B6–B8 retain sample-size,
table-size and margin comparisons, including the weak-MI large-table
failure.

**Speaker script:**

> Each group here uses equal MI in P and Q, so every rejection is a false positive. Table size, margins, and sample size stay fixed; only the shared MI changes. The dashed line is the five-percent target, navy is Wald, and orange is Expanded Welch.

> At shared MI 0.02, the larger cutoff brings rejection from 8.35 percent to 4.90 percent. At shared MI 0.30, rejection still exceeds thirteen percent. Both tests' calculations succeed in every repetition in all three groups, so those departures reflect inference rather than calculation failures.

> The cutoff adjustment can offset some errors at a particular population pair, but it does not make the reference accurate across association strengths. Other margin settings also have rates below five percent, where lowering rejection increases conservatism.

**Delivery cue:** Shared MI changes both populations together; their
difference remains zero. Read the highlighted comparisons, not all six
labels. No old aggregate counts or A/B/C labels.

**Transition:** “A matched diagnostic comparison shows why similar uncertainty errors can give opposite rejection behaviour.”

**Source:** Thesis Section 6.2.1, Figure 6.4, and current null rates,
k=4, uniform, n_p=n_q=20, denominator=all; six method rows.

### Slide 10 — Results: why bias changes rejection

**Purpose:** Use the preferred presentation's strongest explanatory
contrast with current, verified diagnostics.

**On-slide content:**

**Lead:** Similar errors in estimated uncertainty accompany opposite
false-positive behaviour when bias in the MI difference changes.

**Setting:** 16×16; n=1,000 per population; equal MI 0.02 nats.

| Margins | Variance ratio | Bias / SD | Wald | Expanded Welch |
| --- | --- | --- | --- | --- |
| Same skew | 1.93 | ≈0 | 0.60% | 0.53% |
| Different skew | 1.94 | 2.06 | 26.01% | 24.84% |

Variance ratio: average squared estimated standard error / observed
variance of the estimated MI difference.

**Same skew:** The oversized denominator suppresses the statistic;
expected MI biases cancel.

**Different skew:** The estimated difference is shifted away from zero
by unequal residual biases.

**Conclusion:** Changing the cutoff leaves the biased estimated difference
unchanged. Both tests’ calculations succeed in every repetition here.

**Layout and evidence:** Follow preferred-reference page 10. Use the
native two-row table above, its ratio definition immediately below, and
aligned mechanism panels beneath. The bottom conclusion links bias to the
cutoff's limitation. Keep dimensions, n and shared MI fixed. Explain
average uncertainty inflation rather than claiming every standard error
is oversized. The comparison supports a diagnostic explanation without
proving bias is the only distributional difference. The footer points to
B8 for the full different-skew grid and B9 for the ordinary Welch
comparison.

**Speaker script:**

> These two examples have the same dimensions, sample size, and population MI. Their average squared standard errors are almost equally inflated: the variance ratios are about 1.93 and 1.94. Yet their false-positive rates are very different.

> With the same margins, the population tables are identical and expected biases cancel in the MI difference. The oversized denominator suppresses the statistic, accompanying rejection below one percent. Expanded Welch lowers that already-conservative rate further.

> With different margins, residual biases no longer cancel. The sampling mean of the estimated difference is more than two sampling standard deviations above zero. Both tests then reject around a quarter of repetitions despite the inflated uncertainty estimate. Every calculation succeeds in these examples. The larger cutoff changes the decision boundary while leaving the shifted estimate in place, which helps explain why both methods can remain inaccurate.

**Delivery cue:** Compare variance ratios, then bias, then rejection.
Name the MI difference as the biased object.

**Transition:** “The same larger cutoff also changes the probability of detecting a real MI difference.”

**Source:** Thesis Section 6.2.4 and Table 6.1; current null rates and
diagnostics. Variance ratios 1.928694/1.938104; bias/SD −.002719/2.057921.

### Slide 11 — Results: power across MI differences

**Purpose:** Cover sample size and all three gaps using a simple plot and
local numerical comparison.

**On-slide content:**

**Lead:** With sufficient observations, larger MI differences become easier
to detect. Expanded Welch's larger cutoff lowers or preserves rejection.

**Setting:** Uniform 4×4; population MI in P =0.02 nats.

**Plot:** MI-gap magnitude 0.01 nats; power against sample size.

**Snapshot at n=2,500**

| MI-gap magnitude (nats) | Wald | Expanded Welch |
| --- | --- | --- |
| 0.005 | 11.60% | 11.14% |
| 0.01 | 31.85% | 31.14% |
| 0.02 | 79.24% | 78.74% |

**Power:** probability of rejecting equal MI when population MI differs.
Rates use the usual 0.05 p-value threshold.

**Layout and evidence:** Adapt preferred-reference page 11's readable
power curves. Use one large chart at left and the three-gap table at right.
The chart uses only gap=.01, both methods and all ten sample sizes, log x,
y=0–100% and saved pointwise 95% intervals. Keep navy Wald and orange
Expanded Welch and directly label curves without separating overlaps.
The table fixes n=2,500 in the same population family; tint its .01 row to
connect it with the plotted point. It is a snapshot, not a whole-grid
summary. Read the small-to-large gap contrast. B10–B12 retain full
three-gap curves. A quiet footnote states the all-repetitions denominator
and that unsuccessful calculations count as non-rejections.

**Speaker script:**

> Power is the probability of rejecting equal MI when the population MI values differ. Here P stays at 0.02 nats and Q has greater MI. The graph fixes the gap at 0.01 and increases sample size. As estimates become more accurate and less variable, detection rises. Expanded Welch stays at or below Wald, with the curves becoming close at larger samples.

> The table holds sample size at two thousand five hundred and compares all three gaps. Expanded Welch power increases from about eleven percent for the smallest gap to about seventy-nine percent for the largest. That is a local comparison; the full grid also varies dimensions and margins.

> These rates use the usual testing thresholds and are interpreted alongside the false-positive results. A two-sided rejection also needs care because it can point towards the wrong population.

**Delivery cue:** Connect the .01 table row to the plotted point. Do not
call nominal power matched-size power or restore threshold fitting.

**Transition:** “Different residual biases can make that directional error dominate the apparent detections.”

**Source:** Thesis Section 6.3.1, Figure 6.7; current power rates, all
repetitions, k=4, uniform; plot gap=.01 (20 rows), snapshot n_p=2500
(6 rows).

### Slide 12 — Results: bias can reverse the estimated direction

**Purpose:** Preserve the current wrong-direction result in place of the
preferred reference's obsolete calibrated-power sequence.

**On-slide content:**

**Lead:** In sparse tables, unequal residual biases can outweigh the true
MI difference and reverse the estimated direction.

**Setting:** Different-skew 16×16; MI 0.02 versus 0.03 nats.

**At n=1,000**

- True difference, P minus Q: −0.0100 nats.
- Mean estimated difference: +0.0207 nats.
- Expanded Welch rejects in 9.66% of repetitions.
- Among those rejections, over 99.9% have the opposite estimated direction.

**Mechanism:** As positive bias diminishes, the sampling centre passes near
zero, so rejection initially falls before recovering.

**Layout and evidence:** Use evidence beside an explanation, as on
preferred-reference pages 10–12. At left plot the two .01-gap method curves,
log sample size, y=0–100% and saved intervals. At right align true and mean
estimated differences under a navy "At n = 1,000" label. Place the
conditional direction
statement immediately beneath the 9.66% rejection rate. Add the short
mechanism explaining the curve and mark n=1,000 unambiguously. Navy/orange
identify methods. No calibration procedure or fitted thresholds appear.

**Speaker script:**

> The true difference here is minus 0.01 nats, so Q has greater population MI. At one thousand observations per population, however, the mean estimated difference is about plus 0.0207. Unequal residual biases have outweighed the true gap and shifted the sampling centre to the other side of zero.

> Expanded Welch rejects in about 9.66 percent of repetitions at that point. Among those rejections, more than 99.9 percent have a positive estimated difference, opposite to the population direction. They count as power under a two-sided definition, but they fail to identify which population has greater MI.

> As sample size increases, the positive bias diminishes and the centre moves towards zero. Rejection can initially fall before recovering in the correct direction. Changing the cutoff leaves that biased movement unchanged. The shape therefore requires an explanation of the estimator as well as the rejection threshold.

**Delivery cue:** Explain the signed numbers first, then “among the
rejections”. Preserve this slide in the shorter route. Both methods'
calculations succeed in every repetition at the highlighted point.

**Transition:** “The observed-data application illustrates how to interpret outputs when the population values are unknown.”

**Source:** Thesis Section 6.3.3, Figure 6.9; current power rates/diagnostics,
k=16, different_skew, gap=.01. EW positive rejections 9,659, negative 3,
total 9,662.

### Slide 13 — Illustration: online shopping data

**Purpose:** Resolve the opening question and distinguish application
from validation.

**On-slide content:**

**Lead:** Returning visitors have higher estimated month–purchase MI, and
both approximate tests reject equal MI.

**Month × purchase: corrected MI estimates (nats)**

- New visitors: 0.0043.
- Returning visitors: 0.0179.

**Two-sided p-values**

- Wald: 4.71 × 10⁻⁵.
- Expanded Welch: 3.73 × 10⁻⁴.

Both tests reject equal MI at the 0.05 threshold.

**Weekend × purchase**

- Corrected MI estimates: new visitors 0.0007; returning visitors 0.0007.
- Two-sided p-values: Wald 0.9554; Expanded Welch 0.9601.

Estimates are close; neither test rejects equality.

**Interpretation:** Population MI is unknown. The simulations provide the
evidence about reliability.

**Layout and evidence:** Follow preferred-reference page 13. Use a broad
peach month panel at left with the two large estimates, two-sided
p-values and concise rejection statement. Put weekend in a narrower
pale-blue panel with the same layout and matching conclusion type. Reuse
opening group labels. These are corrected estimates, not population
values. The final thesis reports unadjusted p-values for these two
comparisons only. Add no invented group error bars or confidence
intervals. Keep group sizes in the footer; B13 retains details.

**Speaker script:**

> Returning to the opening question, the corrected month–purchase MI estimate is higher for returning visitors. Both methods reject equal MI at the usual 0.05 threshold. Expanded Welch's p-value is about 0.0004. The weekend comparison has very close estimates and neither test rejects equality.

> These are associations, without a causal interpretation of month. The unknown population tables also mean the application cannot tell us which test has accurate false-positive rates. It illustrates how to read the estimates and test outputs, while the known-population simulations establish the strengths and limitations of the comparison.

**Delivery cue:** Close the loop with Slide 2. Non-rejection does not
establish equality. Do not read every number.

**Transition:** “The contribution and the remaining estimation problems lead to specific next steps.”

**Source:** Thesis Section 6.4, Tables 6.3–6.4, and application CSV; Sakar
and Kastro (2018). Month: Wald p = 4.71 × 10^-5; Expanded Welch
p = 3.73 × 10^-4 with 26.79 degrees of freedom (unadjusted, two-sided).

### Slide 14 — Conclusions and next steps

**Purpose:** Answer the research question and link future work to
observed limitations.

**On-slide content:**

**Lead:** MI-specific degrees of freedom improve some false-positive rates,
while remaining failures identify estimation accuracy as a priority.

**Contribution and findings**

1. Derived variance sensitivity and MI-specific degrees of freedom.
2. Brought some excessive false-positive rates closer to 5%; deepened
   conservatism elsewhere.
3. Lower power under the same 5% testing rules; residual bias can reverse
   the estimated direction.

**Scope:** The evaluation covers one population construction and equal
sample sizes, with the Wald test as the main benchmark.

**Next steps**

- Reduce bias in the estimated MI difference and improve its standard error
  and degrees of freedom, including near independence.
- Test other association constructions and unequal sample sizes.

Thank you.

**Layout and evidence:** Follow preferred-reference page 14. Use three
pale-blue finding blocks beneath a navy heading, a navy-bar scope line, then two shallow peach
next-step blocks beneath orange. Keep phrases readable and add no new
equations. This combines the former limitations and conclusion pages.
Leave it displayed during questions. Its speaker notes contain the
backup-number index.

**Speaker script:**

> I derived the MI-specific variance sensitivity and used it to calculate degrees of freedom for a Welch–Satterthwaite comparison. Its larger cutoff brings some excessive false-positive rates closer to five percent, but also increases conservatism and reduces power under the usual rules.

> The sparse-table examples show why the estimates remain central: a cutoff adjustment leaves bias and errors in the standard error unchanged, and bias can reverse the estimated direction. The evaluation covers one population construction and equal sample sizes, with the Wald test as the main benchmark. The next steps are to improve those estimates, retain additional sampling variation near independence, and evaluate broader population constructions and unequal sample sizes. The project contributes both the calculation and evidence identifying where it needs further development. Thank you.

**Delivery cue:** Give contribution and boundary equal emphasis. Face the
audience and keep this page visible for questions.

**Source:** Final abstract; thesis Sections 1.3 and 7.1–7.3. No claim of
universal superiority or validated independence-specific replacement test.

## 7. Backup specifications and navigation

The appendix begins with a title page on physical Slide 15, followed by
15 backups on physical Slides 16–30. They are question material,
not another section to narrate. Keep the index below in Slide 14's notes;
do not add a projected index page. Jump by physical slide number
and return to Slide 14. Preserve the same fonts, equation/panel styles and
readability. Full grid backups retain their explicit parameter legends and
compact calculation-success strips; their colours differ in meaning from main method
comparisons, which must be stated when opening one.

| Backup | Physical slide | Question addressed |
| --- | --- | --- |
| B1 | 16 | Variance sensitivity |
| B2 | 17 | Moment matching and combined degrees of freedom |
| B3 | 18 | Population construction, grid, and calculation requirements |
| B4 | 19 | Approximation ratios across table sizes |
| B5 | 20 | Near-independence noise calculation |
| B6 | 21 | Full null results: uniform margins |
| B7 | 22 | Full null results: same-skew margins |
| B8 | 23 | Full null results: different-skew margins |
| B9 | 24 | Ordinary Welch degrees of freedom |
| B10 | 25 | Full power results: uniform margins |
| B11 | 26 | Full power results: same-skew margins |
| B12 | 27 | Full power results: different-skew margins |
| B13 | 28 | Application details |
| B14 | 29 | References: MI and testing foundations |
| B15 | 30 | References: related methods and evaluation |

### Appendix divider — physical Slide 15

**Purpose:** Mark the beginning of the supporting material clearly in the
slide deck and PDF.

**On screen:** Only the word **Appendix**, in bold Lato (48 pt),
centred on a white background in the deck's navy colour. Retain the small
slide number. Do not add an index, explanatory paragraph, figures or data.

**Delivery:** No timed speech. Keep the conclusion on Slide 14 visible when
questions begin, then open the relevant backup when needed and return to
Slide 14 afterwards. The divider adds no time to the 18:50 main talk.

### B1 / Slide 16 — Variance sensitivity

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
The notes must state the regularity assumptions: fixed categories,
independent observations within each sample, independent samples,
positive population cell probabilities, and positive V and tau-squared
for the first-order df construction. With every cell positive, positive
MI is equivalent to positive V (Appendix A.3), but positive V does not
guarantee positive tau-squared. Do not treat a zero component as ordinary
finite df.

### B2 / Slide 17 — Moment matching and combined degrees of freedom

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

Keep one sentence below: “Moment matching does not establish the normality
or independence needed for an exact Student t distribution.” Put the
scaled-chi-squared mean/variance derivation in notes rather than forcing
another four equations onto the slide.

**Answer to give:** “A scaled chi-squared variable has variance twice its
squared mean divided by its degrees of freedom. Matching those two moments
gives the target. Dividing V-hat by fixed sample size rescales the squared
mean and variance equally, so it leaves the component target unchanged.
Independence between the two samples lets their variance contributions add.
The resulting Student t distribution still requires empirical assessment.”

**Source:** Thesis Sections 4.1 and 4.3, pp. 23–35; Satterthwaite (1946).

**Notes to include:** For a generic variance estimate U modelled as
c times a chi-squared variable, E(U)=cν and Var(U)=2c²ν, giving
ν=2[E(U)]²/Var(U). Scaling by fixed n leaves this ratio unchanged.
For the Slide 7 example at n=1,000, first-order component df are 15.30
against the moment target 21.03: approximately (1/1.19)²/0.97=0.73.
This explains the squared-mean effect without another main-slide formula.

### B3 / Slide 18 — Population construction, grid, and calculation requirements

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
- Null: shared MI .005, .02, .30. Power: P MI .02, Q MI .025, .03, .04.
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

### B4 / Slide 19 — Approximation ratios across table sizes

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

### B5 / Slide 20 — Near-independence noise calculation

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
| Mean estimated component df | 4.60 | 4.86 |
| Sampling-moment target | 9.00 | 9.12 |
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

### B6 / Slide 21 — Full null results: uniform margins

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

### B7 / Slide 22 — Full null results: same-skew margins

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

### B8 / Slide 23 — Full null results: different-skew margins

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

### B9 / Slide 24 — Ordinary Welch degrees of freedom

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

### B10 / Slide 25 — Full power results: uniform margins

**Question:** Do the gap and sample-size patterns hold outside the
single curve and snapshot?

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

### B11 / Slide 26 — Full power results: same-skew margins

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

### B12 / Slide 27 — Full power results: different-skew margins

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

### B13 / Slide 28 — Application details

**Question answered:** How were the shopping comparisons set up, and why
are the weekend degrees of freedom so small?

**Show:** One introduction line: “Online Shoppers Purchasing Intention
data; new (P) versus returning (Q) visitors; two-sided p-values”. Then two
editable tables from final Tables 6.3–6.4, without filled header rows.

**Corrected MI estimates (nats)**

| Predictor | New visitors | Returning visitors | Difference | Standard error | Statistic T |
| --- | --- | --- | --- | --- | --- |
| Month | 0.004316 | 0.017880 | −0.013563 | 0.003333 | −4.069 |
| Weekend | 0.000664 | 0.000727 | −0.000063 | 0.001124 | −0.056 |

**Test results**

| Predictor | Expanded Welch degrees of freedom | Wald p-value | Expanded Welch p-value |
| --- | --- | --- | --- |
| Month | 26.79 | 4.71 × 10⁻⁵ | 3.73 × 10⁻⁴ |
| Weekend | 2.18 | 0.9554 | 0.9601 |

Below the tables: “Month tables are 10×2 (no January or April sessions)
and weekend tables are 2×2. The leading correction subtracts 9/(2n) from
each month estimate and 1/(2n) from each weekend estimate.” The footer
gives the group sizes and the 85 excluded Other sessions.

**Answer to give:** “I compare month–purchase and weekend–purchase MI
between new and returning visitors, treating the two visitor groups as
independent samples. For month, the corrected difference is about 4.07
standard errors from zero, so both tests reject equal MI. For weekend,
both estimates are about 0.0007 nats and the statistic is close to zero,
so neither test rejects; that does not establish equality. The weekend
degrees of freedom are only 2.18 despite the large samples because both
variance estimates fluctuate a lot relative to their size.”

**Notes:** Dataset: 12,330 sessions, each from a different user according
to its documentation. P: 1,694 sessions labelled New_Visitor; Q: 10,551
labelled Returning_Visitor; the 85 Other sessions are excluded. Outcome:
the Boolean Revenue variable. Month: January and April have no recorded
sessions, so each table is 10×2. All ten months occur in both groups,
although the new-visitor February row contains one session and no
purchase. Zero cells are retained without adding artificial counts.
Component degrees of freedom: month 12.93 (new) and 187.93 (returning),
combined 26.79; weekend 1.69 (new) and 7.71 (returning), combined 2.18.
The final thesis reports unadjusted two-sided p-values for these two
comparisons only; it no longer includes a multiple-comparison family or
Holm adjustment.

**Source:** Thesis Section 6.4, Tables 6.3–6.4; application CSV; Sakar and
Kastro (2018).

### B14 / Slide 29 — References: MI and testing foundations

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

### B15 / Slide 30 — References: related methods and evaluation

**Show/layout:** Five entries in the same style and at the same readable
size as B14. Include `hutcheson1970`, `panwall2002`, `morris2019`,
`sakar2018`, `wald1943`.

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
| Why does moment matching imply a Student t test? | “It motivates an approximate reference. Matching a scaled chi-squared variance component does not prove the standard normal numerator and independence conditions of an exact Student t construction.” | B2 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | B3, B8 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | B3; thesis Section 2.4 |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 14 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap, and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 11–12 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 11 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | Slide 12; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 12 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | B5 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | B2, B5 |
| Could unsuccessful calculations explain the low rejection? | “They contribute at some small sample sizes. I report calculation success separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation succeeds.” | B3; Slides 9–10 and B6–B8 |
| Why count unsuccessful calculations as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to successful calculations would condition on a selected subset. Reporting calculation success separately makes the distinction visible.” | B3 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | B3; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | B3, B6–B12 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even when every calculation succeeds. The application illustrates interpretation and cannot verify its population-level accuracy.” | Slides 9–14 |
| Why is the month table 10×2 rather than 12×2? | “January and April have no recorded sessions. Both groups use the same ten recorded month categories and the two purchase outcomes, retaining zero cells within those categories.” | B13 |
| Are the shopping observations independent? | “The dataset documentation says sessions belong to different users. I treat groups and observations as independent, but this remains a working sampling assumption and does not establish representativeness or rule out shared temporal influences.” | B13 |
| Does higher month MI mean a stronger causal month effect? | “It describes greater association in the population comparison. MI depends on the joint probabilities and margins, so it does not isolate a causal response or establish a change in predictive accuracy.” | Slide 13 |
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
PowerPoint, including jumping from Slide 14 to backups and back.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 3 | 2:40 | Keep literature roles concise; do not recite citations. |
| End of Slide 6 | 7:00 | Use the short form of Slide 7; protect near independence. |
| End of Slide 8 | 10:20 | Shorten Slide 9's rate narration and read only its key comparison. |
| End of Slide 10 | 13:35 | Use the compact Slide 11 explanation; protect the directional result. |
| End of Slide 12 | 16:45 | If past 18:00 use the emergency closing route below. |
| End of Slide 13 | 17:50 | Begin the conclusion immediately; do not open backups. |

### Prepared shorter route

| Slide | Planned | Short form | Preserve |
| --- | --- | --- | --- |
| 2 | 1:15 | 1:00 | Concrete comparison, sample estimates, and population hypothesis |
| 3 | 1:00 | 0:50 | Existing foundations and required MI-specific calculation |
| 4 | 1:20 | 1:10 | Shared statistic and visible cutoff difference |
| 5 | 1:40 | 1:25 | Derivation chain, final formula, and two approximations |
| 6 | 1:20 | 1:10 | Parallel studies, sample size versus repetitions, unsuccessful-calculation rule |
| 7 | 1:40 | 1:25 | Mean/variance distinction and the 19%, 3%, and 8% anchors |
| 9 | 1:30 | 1:20 | The .02 improvement and .30 failure, equal MI, and every calculation succeeding |
| 10 | 1:45 | 1:35 | Similar variance errors, different bias, and opposite rejection |
| 11 | 1:30 | 1:20 | Power definition, one curve, and three-gap snapshot |
| 13 | 1:05 | 0:55 | Return to example, rejection at 0.05, and unknown population MI |
| 14 | 1:00 | 0:50 | Contribution, conditional benefit, remaining errors, and next steps |

These reductions total 125 seconds, giving **16:45**. Slides 8 and 12
remain at full length because they carry important explanations. Use this
route to simplify narration, not to speak faster.

### If Slide 12 ends at 18:00

- **Slide 13, about 30 seconds:** “Returning visitors have higher estimated
  month–purchase MI, and both tests reject equality at the usual 0.05
  threshold. The unknown population values mean this illustrates
  interpretation without validating false-positive accuracy.”
- **Slide 14, about 50 seconds:** “I derived MI-specific variance
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
- Slide 9 is now **uniform 4×4/n=20 at all three shared MI values**.
  Use current rates and intervals. Do not retain old A/B/C case labels or
  aggregate favourable-setting counters.
- Slide 10 is a **two-row diagnostic comparison**. Slide 11 is a **.01-gap
  curve plus a three-gap snapshot at n=2,500**. These choices are deliberate
  reductions in simultaneous comparisons, not changes to the experiments.
- Keep component and combined df distinct; distinguish the moment target
  from an exact Student t distribution. B1's derivative is exact under its
  population assumptions; its sampling expansion is first order.
- Slide 12's conditional denominator is 9,662 EW rejections: 9,659 positive,
  3 negative. Do not turn over 99.9% into a percentage of all repetitions.
- Application numbers are corrected estimates and unadjusted two-sided
  p-values from final Tables 6.3–6.4. Do not add invented individual-group
  confidence intervals.
- Match citations to `references.bib`. Preserve published spelling and
  dataset identifiers; check Australian spelling in authored prose.

### Authoring sequence when execution is requested

1. Inspect the preferred 25-page PDF and use the 11-slide donor only for
   editable style/cover assets. Work on a separate copy in the versioned
   output directory. Preserve existing presentations.
2. Build the intended ending, Slide 14, then the shared-statistic and
   derivation Slides 4–5. Establish readable equations and definitions.
3. Filter and verify data for Slides 7–13 before designing their charts.
   Save selected rows and chart code with the new presentation assets.
4. Build the opening and literature around the knowledge those results
   need. The opening must present the actual statistical problem.
5. Add the mechanism panels, local numerical anchors and full speaker
   notes. Keep visual instructions out of rehearsal notes.
6. Build the 15 backups and update Slide 14's notes index with physical
   slide numbers. Rehearse likely questions.
7. Inspect every rendered page, compare it with the relevant preferred
   reference page and rehearse to the timing table. Correct genuine
   problems without adding new scientific material.

### Proposed outputs

Under `/Users/danielzhao/MyMac/Masters Degree/Research/Thesis Presentation/`, the current
version:

- `Daniel_Zhao_Welch_MI_Presentation.pptx`: 14 main slides, one appendix title slide and 15 backup slides,
  editable text/equations/tables, complete notes.
- `Daniel_Zhao_Welch_MI_Presentation.pdf`: matching 30-page PDF, including
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
