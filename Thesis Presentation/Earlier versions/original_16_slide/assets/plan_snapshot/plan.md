# Presentation execution plan

Prepared for Daniel Zhao on 4 November 2026. This is a handoff specification
for the agent that will create the presentation. It includes the argument,
slide copy, layouts, evidence selection, spoken script, timings and question
preparation. The visual specification was updated on 4 November 2026 to
follow Daniel's supplied INFO5993 presentation. It does not itself author
a slide deck.

## 1. Instructions to the executing agent

Create **16 main slides**, followed by **12 backup slides**. The main talk
targets **18 minutes 50 seconds**, leaving 70 seconds before the university's
20-minute limit. Backup slides are for the question period and are not part
of the timed talk. Keep Slide 16 on screen when questions begin.

Use the final, 100-page thesis rebuilt on 4 November 2026 as the scientific
authority. The source and PDF already include the four approved changes
from the final review. Do not revise the thesis, regenerate its figures,
change its delivery files, run new experiments or alter historical files
when creating this presentation. Create presentation outputs in a separate
`Thesis Writeup/Welch MI/presentation/` directory if instructed to execute.
That directory is a proposed destination, not an existing deliverable.

Read this complete plan and the accompanying
`PRESENTATION_EVIDENCE_MANIFEST_2026-11-04.json` before making slides. The
manifest provides exact data filters and verified numerical anchors.
Populate speaker notes with the scripts below, source references and cues.
The scripts are a rehearsal draft. Daniel should learn the explanation
and then speak naturally rather than read the notes verbatim.

Use Daniel's supplied `Zhao_Daniel_Presentation_vF2.pptx` as the visual
reference and its PDF as the reference for rendered appearance. Section 4
and the per-slide layouts now follow that design. This replaces the earlier
plain navy design proposal. The scientific content, main-slide order,
scripts, evidence selections and timing allocations remain unchanged.

### Source hierarchy

The workspace root is:

`/Users/danielzhao/MyMac/Masters Degree/Research/Simulations`

All project paths below are relative to that root unless marked otherwise.

| Authority | Location and role |
| --- | --- |
| Final manuscript | `Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis.pdf`. SHA-256: `6a3442e9732f29daace007433b7ee3c575d984ab1a3196a7a8555c0863b91a94`. Printed page numbers below refer to this PDF. |
| Scientific source | `Thesis Writeup/Welch MI/chapters_rewrite/`, `appendices_rewrite/`, `references.bib`. |
| Visual reference | `/Users/danielzhao/MyMac/Masters Degree/INFO5993/A4/Zhao_Daniel_Presentation_vF2.pptx` and the matching `.pdf`. Both contain 11 slides. Use their design, not the earlier project claims or proposed experiments. |
| Presentation rubric | `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/Presentation Marking Criteria.pdf`. The locally saved file has one PDF page, labelled “Page 5 of 5”. |
| University deliverables | `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/18cp Research Path deliverables.pdf`, especially page 1 and the PDF submission instruction on page 2. |
| Research rubric | `/Users/danielzhao/MyMac/Masters Degree/Research/Example Thesis/18CP Research Pathway Project Marking Rubric V3.pdf`. Context for contribution and critical evaluation, not a substitute for the presentation rubric. |
| Writing principles | `Thesis Writeup/Welch MI/notes/RESEARCH_PROSE_WRITING_GUIDELINES_2026-10-31.md` and `CHAPTER_6_RESULTS_WRITING_GUIDELINES_2026-10-30.md`. Use Australian English. |

### The previous presentation is outdated

`Thesis Writeup/Welch MI/deliverables/Comparing MI in Finite Samples.pdf`
is an existing 25-page presentation. Preserve it. It is not the current
thesis PDF and is not the scientific authority for this new talk.

Its nominal/calibrated-power discussion, A/B/C focus-setting narrative,
cross-null calibration, four-cell comparison and robustness slides belong
to earlier versions. Do not copy those results or restore those experiments.
The final thesis uses the balanced three-common-MI null grid and the
three-gap power grid, evaluated at the usual p-value threshold of 0.05.
Files with old result names still exist in the repository. Their existence
does not make them current presentation evidence.

Do not run `focused_results_displays.py` or other thesis generators with
their default output destinations. Some generators also write historical
analyses. Read the saved CSVs and create presentation-specific graphics in
the separate presentation directory.

## 2. University requirements and how the talk addresses them

The supplied deliverables document specifies a talk of **up to 20 minutes**,
followed by **up to 10 minutes of questions**. It says the talk will be
interrupted at 20 minutes. The presentation is **20% of the project mark**.
The audience includes the thesis markers, supervisor, other academic staff
and students. Submit the presentation as PDF; PowerPoint may be used live.

These are requirements in the supplied documents. The 16-slide structure,
18:50 target, aspect ratio and design choices below are planning decisions,
not additional university rules. The saved documents do not establish the
actual presentation date or the current Canvas upload deadline.

| Presentation criterion | Weight | Implementation |
| --- | --- | --- |
| Relevant content: motivation/objective, literature, own method, results, discussion/contribution, conclusion/future work | 30 | Slides 2–4 establish the problem and prior work; 5–6 explain the method; 7 specifies evaluation; 8–14 present and interpret evidence; 15–16 establish limits, future work and contributions. |
| Understanding, logical and persuasive explanation, answers to questions | 20 | Explain the variance quantities before plotting them, distinguish exact derivatives from approximations, explain failures, and prepare Backups B1–B10 and the answer bank. |
| Pace, appropriate detail and finishing on time | 20 | Allocate 18:50 including graph-reading pauses. Use the checkpoints and the explicit shorter route. Do not add an agenda slide or narrate backup material. |
| Engagement, eye contact and speaking rather than reading slides | 20 | Open with a concrete comparison, introduce each graph before pointing to its curves, use short on-slide labels, and practise from cue summaries after learning the full script. |
| Fonts, colours, readability and restraint in animation | 10 | Use a consistent academic layout, readable charts, limited colour, editable text and equations, and a static PDF that contains the complete argument. |

The deliverables document mentions a Canvas template. No official
presentation master has been supplied. Daniel has now supplied a previous
presentation and asked that this plan follow its style, so that deck is
the current visual authority. It is a personal reference, not a verified
university slide template. The thesis's `usydthesis.cls` remains a thesis
class. If a mandatory official presentation master is supplied later,
adapt the approved content to it without changing the scientific argument.

## 3. Narrative and audience assumptions

Assume familiarity with basic probability, sampling and hypothesis tests,
but no familiarity with this MI derivation. Explain mutual information,
false positives, power and the distinct variance quantities when first used.
Use “degrees of freedom” in speech. The abbreviation “df” may appear in a
crowded graph legend after it has been introduced.

The central question is:

> Can degrees of freedom derived specifically for MI improve comparisons
> between two populations when samples are finite?

The answer develops through the evidence:

> The derivation gives an MI-specific way to choose the Student t reference.
> Its larger cutoff can bring excessive false-positive rates closer to 5%,
> but it also reduces power and cannot remove errors in the shared estimates.

The scientific contribution is the MI variance-sensitivity calculation,
its use in the degrees of freedom, and the evaluation explaining its
limits. Lower rejection follows from the larger cutoff. Do not sell that
ordering alone as an empirical discovery or imply that Expanded Welch is
uniformly better.

Use the shopping question near the beginning and return to it near the end.
The middle of the talk answers what must be established before interpreting
that application. Do not present a compressed chapter-by-chapter summary.

### Explanation order

1. Association can differ between populations, but sampled MI estimates
   also differ because counts fluctuate.
2. Prior work gives MI estimates and their first-order sampling variance.
   A Welch–Satterthwaite reference additionally needs the variability of
   the variance estimate itself.
3. Derive that MI-specific sensitivity, then evaluate its approximations.
4. Show conditional improvement, substantial failures and the power cost.
5. Illustrate the calculation on observed data and close with bounded
   contributions and specific future work.

## 4. Visual and language specification

### Supplied reference and design priority

Inspect both of these files before authoring:

- `/Users/danielzhao/MyMac/Masters Degree/INFO5993/A4/Zhao_Daniel_Presentation_vF2.pptx`
- `/Users/danielzhao/MyMac/Masters Degree/INFO5993/A4/Zhao_Daniel_Presentation_vF2.pdf`

All 11 reference slides were visually inspected for this revision. The
PowerPoint XML was also inspected for canvas dimensions, fonts, colour
values and text positions. The PDF establishes the intended appearance;
the PowerPoint supplies editable layouts and original assets.

Follow the reference's white backgrounds, black Lato headings, orange
emphasis, navy comparison headings, pale panels and restrained rounded
corners. Use its layout variety: paired comparisons, numbered explanatory
steps, comparison matrices and charts with short explanations. The cover
uses a curved white area at left and a statistical chalkboard image at
right. Preserve that distinctive composition.

The reference describes an earlier research proposal about a corrected
independence null. Its chi-squared baseline, proposed resampling comparison,
45-configuration grid, future milestones and JIDT integration are not
content for this final-thesis talk. The final thesis remains the scientific
authority. Do not copy old slide text, chart data or speaker notes.

### Measured design features and implementation choices

| Element | Observed in Daniel's reference | Specification for this talk |
| --- | --- | --- |
| Canvas | 13.3333 × 7.5 inches, 16:9; OOXML size 12,192,000 × 6,858,000 EMU | Use the same canvas. |
| Content titles | Lato Bold, 36 pt, black, left aligned | Retain Lato Bold at 36 pt, with the current wording and sentence case. Keep the title on one line where it fits naturally. |
| Title position | x=0.8486, y=0.4063, width=11.5, height=0.8074 inches | Use these coordinates for the common title placeholder. |
| Introductory line | Usually a short black paragraph under the title, with a meaningful phrase highlighted orange; many runs are 16 pt | Use an existing question, definition or setting line here at 20–22 pt. Highlight one short phrase when useful. Avoid adding a duplicate summary. |
| Main text | Predominantly Lato; dense areas contain 11–16 pt text | Use Lato at 22–24 pt for main prose and 20–22 pt for table cells. Keep the visual style while giving scientific content room to read. |
| Maths | Cambria Math | Use editable Cambria Math equations, normally 24–28 pt. |
| Cover | Aptos Display title, 26 pt and orange; Aptos author details, 16 pt | Keep those font families and orange title treatment. Allow a 28–32 pt title and 18–20 pt details to fit the current title and affiliation. |
| Panels | Shallow orange/navy headers, pale fills, thin outlines, modest rounded corners | Reuse these for actual comparisons and steps. Main result graphs retain large white plotting areas. |
| Emphasis | Orange words, numbered circles, occasional simple arrows | Apply to existing labels and genuine calculation steps. Use plain text when an icon adds no information. |
| Footers | Small citations where needed; no repeated large logo or full-width footer banner | Use a quiet 14–16 pt source line and slide number, without a coloured footer banner. |

The reference has two Office themes. Its main content slides use
`#ED7D31` for the orange accent, while the cover and some early elements
use `#E97132`. The generic theme font is Aptos, but the actual content
headings and body runs are predominantly Lato. Do not infer the intended
content font from the theme name alone. Set the intended fonts and
colours explicitly when rebuilding a layout.

| Role | Colour |
| --- | --- |
| Background | White `#FFFFFF` |
| Titles and primary text | Black `#000000`; secondary body text `#333333` |
| Main orange accent | `#ED7D31` |
| Cover orange / retained early-slide accent | `#E97132` |
| Navy comparison header | `#1F3A5C`; the source also uses the very similar `#1E3A5C` |
| Pale orange panel | `#FFF1E8`; stronger source tint `#FBE5D6` where useful |
| Pale blue panel | `#E8EFF7`; retained source variant `#E8F0F7` |
| Orange / blue panel outline | `#F5C6A7` / `#C8D8EA` |
| Light divider | `#DDDDDD` |

Use white text on navy headers. For orange headers, use a clearly readable
weight and at least 22 pt, following the reference's white-on-orange
heading treatment. Use black text for longer explanations on pale fills.
Avoid thin orange text for small sources or axis labels. The green/red
strength-and-weakness boxes in reference Slide 3 are optional source
features, not a requirement to assign good/bad colours to scientific
outcomes. The method comparison does not have a uniformly better method.

### Common layout, cover and reuse

- Keep the content title at the measured reference position. Introductory
  copy normally begins at x=0.85, y=1.25, across about 11.5 inches. Allow
  one or two lines, then start the main evidence around y=2.0. Where a
  setting line already introduces a graph, use it as the introduction.
- Most panel-based layouts can extend from x=0.5 to x=12.83, as in the
  source, while text within panels stays comfortably inset. Use a gap of
  approximately 0.3–0.4 inches between columns. Leave the bottom source
  line clear around y=7.1. Do not extend dense content to the slide edge.
- For chart slides, minimise the framing so plots can use approximately
  y=1.9 to y=6.8. A short orange panel heading or a single tinted
  explanatory panel is enough. Do not put every curve in a separate card.
- Use the supplied reference's functional header bars, rounded panels,
  numbered circles and simple connectors where the per-slide plan calls
  for them. These are intentional features of Daniel's chosen style.
  Avoid extra decorative symbols, dashboards, status badges or new motifs.
- Use the original chalkboard image from the supplied PowerPoint cover:
  `ppt/media/image1.png`, referenced by Slide 1's `Picture 4`. Preserve
  the curved white mask, small orange mark and light divider from that
  cover. They are cover features, not recurring body-slide decoration.
- Work on a copy of the reference when reusing objects or layouts. Keep
  the original two files unchanged. Reuse original cover artwork rather
  than recreating the image or drawing a different curve. If the authoring
  tool loses the mask, a decoration-only render from the copied cover is
  acceptable after removing its old title and subtitle. Overlay the new
  text as editable text. Do not flatten old research wording into a new
  background.
- Use Lato in both authoring and rendering. The PDF embeds Lato, which
  does not by itself ensure it is installed for the executing tool.
  Check font availability and inspect substitutions before approving fit.
  Do not silently change the content font to Aptos or Arial. Preserve
  editable text even if cover decoration uses the fallback above.
- Match the reference's unbranded content pages. Do not add a university
  logo to every slide or to the cover by default. The existing thesis
  logo remains available if a subsequently supplied university master
  requires it. Keep the planned author, supervisor and affiliation text.
- Use 20–24 pt chart labels on main slides. Backup grids may use 18–20 pt
  if inspected at presentation scale. References may use 16–18 pt, with
  full entries split across the two planned reference slides. Prefer
  reducing redundant labels to shrinking important evidence.

### Layout references for the executing agent

| New slide(s) | Relevant source slide(s) | Design to carry across |
| --- | --- | --- |
| 1 | 1 | Curved white cover, statistical image, orange title and author block |
| 2–3 | 2, 5 | Clear definition or question, pale equation area, paired group explanation |
| 4 | 7 | Comparison matrix, orange labels and restrained rules |
| 5 | 3 | Orange/navy method headings and pale comparison panels |
| 6 | 8, 10 | Numbered steps with a clear calculation sequence |
| 7 | 9 | Navy evaluation area paired with an orange parameter-grid area |
| 8 | 4 | Two large plots, short settings and orange panel headings |
| 9 | 9 | Large evidence area with a compact tinted explanation |
| 10 | 7, 9 | Readable comparison table with colour confined mainly to headings |
| 11–12 | 4 | Large white plotting area and compact setting introduction |
| 13–14 | 3, 9 | Chart beside a pale explanation/result panel |
| 15 | 7 | Two-column comparison organised by matching rows |
| 16 | 8 | Navy contribution heading and three pale-blue numbered blocks |
| B1–B10 | 2, 4, 7, 9 | The same equation, chart, matrix and explanation styles |
| B11–B12 | 11 | Two-column bibliography with larger, readable entries |

### Evidence and graph rules

- Replot selected data for projection. Do not place a screenshot of a
  whole thesis page on a slide. Preserve the numerical data, scale meaning,
  denominator and relevant uncertainty.
- Keep text, tables and equations editable. Prefer native charts when
  reliable; scientific plotting tools may export clean presentation-scale
  charts, with the underlying data supplied alongside them. Do not generate
  scientific evidence with an image-generation tool.
- Use visible markers at the ten tested sample sizes. Connecting lines
  guide the eye between tested points. Do not imply that every intermediate
  sample size was evaluated.
- Method encoding for multi-curve result charts: **Normal Wald is solid
  with filled circles; Expanded Welch is dashed with open squares**.
  Keep this encoding across null and power slides.
- Common-MI colours: 0.005 blue `#0072B2`, 0.02 orange `#E69F00`,
  0.30 green `#009E73`. Power-gap colours: 0.005 blue, 0.01 orange,
  0.02 green. The legends must name the different quantities. The presenter
  explicitly introduces the change from common MI to MI gap on Slide 12.
- On Slides 8–9, colours refer to approximation quantities, not test
  methods. Directly label those curves and use their separate definitions.
- Use logarithmic sample-size axes. Preserve logarithmic ratio and MI
  axes on Slides 8–9. Do not invert prediction/observation ratios.
- Plot false-positive and power rates as percentages, converting saved
  proportions once. Show the nominal 5% line on null charts. Retain the
  validity strip where specified. Main power charts span 0–100%.
- Retain the saved pointwise 95% intervals on main null/power charts as
  restrained bands. Explain once that they describe Monte Carlo uncertainty,
  not simultaneous confidence over the full grid.
- Keep plotted method overlaps. The final data genuinely make the methods
  close in many settings. Do not offset, jitter or invent separation.
- Where a main slide uses one setting or population, label it explicitly
  as an illustrative slice. Do not turn a selected example into a claim
  about all populations. The thesis and backup results provide context.

### Writing and delivery

- Use Australian English and ordinary statistical names, including
  “Student t distribution”. Preserve published titles and dataset fields.
- Put the scientific subject in the title. Use a factual finding title
  when the slide establishes a result. Do not add promotional subtitles.
- Keep setting labels beside the evidence. Limit prose to the exact copy
  specified below, with room for minor line wrapping. Put the explanation
  in speaker notes rather than adding another paragraph on the slide.
- Avoid vague “this” where several estimates are visible. Name the mean,
  variance prediction, estimated difference or cutoff that changes.
- Equations appear only after their quantities have been introduced.
  Read their meaning aloud rather than pronouncing every symbol.
- Default to static slides. Optional simple reveals may help Slides 5–6,
  but the exported PDF must show the full argument without animation,
  hidden objects, motion paths or presenter actions.
- Cite prior work visibly in short author–year form and put the full
  reference in notes and Backups B11–B12. Cite thesis figures/sections on
  result slides. Local filenames and computational provenance belong in
  authoring files and notes, not on the projected slide.

## 5. Main-slide sequence and timing

The timings include the speaker script, transition, pointing and short
pauses. They are rehearsal targets, not durations achieved merely by
reading the scripts quickly. The transition is the closing sentence of
that slide's allocation, not an additional untimed passage.
The scripts and transitions contain approximately 2,050 words. Allow
time for the audience to inspect the equations and graphs rather than
treating that word count as a guarantee of delivery time.

| Slide | Title | Time | Finish by |
| --- | --- | --- | --- |
| 1 | Comparing Mutual Information in Finite Samples | 0:25 | 0:25 |
| 2 | Comparing association across populations | 1:05 | 1:30 |
| 3 | Sampling uncertainty in the MI comparison | 1:00 | 2:30 |
| 4 | Existing foundations and the MI-specific contribution | 0:55 | 3:25 |
| 5 | Normal Wald and Expanded Welch | 1:10 | 4:35 |
| 6 | Deriving the degrees of freedom | 2:00 | 6:35 |
| 7 | Evaluation from known populations | 1:15 | 7:50 |
| 8 | Sparse samples distort the variance inputs | 1:20 | 9:10 |
| 9 | Sampling noise matters near independence | 1:30 | 10:40 |
| 10 | The benefit depends on Wald's false-positive rate | 1:20 | 12:00 |
| 11 | False-positive rates across common MI values | 1:10 | 13:10 |
| 12 | Power across three MI differences | 1:05 | 14:15 |
| 13 | Bias can reverse the estimated direction | 1:30 | 15:45 |
| 14 | An application to online shopping | 1:15 | 17:00 |
| 15 | Limitations and future work | 1:00 | 18:00 |
| 16 | Contributions and conclusions | 0:50 | 18:50 |

The opening and literature take 3:25; method and evaluation setup take
4:25; experimental results take 7:55; application, limits and conclusion
take 3:05. Do not insert a separate agenda or “Questions?” slide.

## 6. Detailed main-slide specifications

### Slide 1 — Comparing Mutual Information in Finite Samples

**Purpose and takeaway:** Establish the project and the comparison being
studied. The audience should hear a concrete research question immediately.

**Exact on-slide copy:**

- Comparing Mutual Information in Finite Samples
- Normal Wald and Expanded Welch–Satterthwaite Tests
- Daniel Zhao
- Supervisor: Associate Professor Joseph T. Lizier
- School of Computer Science, The University of Sydney

**Layout:** Follow reference Slide 1. Keep its curved white panel at left,
chalkboard image at right, small orange mark near the upper left and thin
light-grey divider above the author block. Keep the current title wording,
with deliberate breaks such as “Comparing Mutual / Information in / Finite
Samples”, in orange Aptos Display at about 30–32 pt. Position the title
in the lower half of the white area, approximately x=0.6, y=3.2, width=4.7
inches. Put the method subtitle beneath it at 18–20 pt. Place Daniel's
name, supervisor and affiliation below the divider, allowing the supervisor
and affiliation to wrap naturally. Keep all text inside the white region
and clear of the curve. Adjust the vertical spacing of these text groups
to fit rather than copying the old title box's bottom alignment blindly.
Use the original image and mask. Add no logo or extra cover decorations.

**Speaker script:**

> My project asks whether mutual information differs between two
> populations when we only have finite samples. I develop an MI-specific
> Welch–Satterthwaite test and examine when its larger rejection cutoff
> improves false-positive accuracy, and what that costs in detection.

**Delivery cue:** Look at the audience for the opening question. Do not read
the full title and affiliation. Advance within 25 seconds.

**Transition:** “I will start with the comparison we might want to make.”

**Source:** Thesis title, abstract and Chapter 1, pp. 1–3.

### Slide 2 — Comparing association across populations

**Purpose and takeaway:** Define MI through a concrete question before
introducing the test. Establish the P/Q group meaning used again on Slide 14.

**Exact on-slide copy:**

- Mutual information: average reduction in uncertainty about one variable
  obtained by observing another
- Month of visit and purchase outcome
- P: new visitors
- Q: returning visitors
- Does the month–purchase MI differ between these populations?

**Layout:** Use the reference's black Lato title and short definition
under it, highlighting only the key phrase about reduced uncertainty in
orange. Below, show two aligned group panels: an orange “P: new visitors”
header above a pale-orange area and a navy “Q: returning visitors” header
above a pale-blue area, following reference Slides 2–3. Both contain the
same “Month” and “Purchase” variable labels and a simple count-table motif
without invented numerical cells. Put the existing question beneath the
panels in black. Keep the objects editable. This is a conceptual
introduction, not a real-data results slide.

**Speaker script:**

> Mutual information measures the average reduction in uncertainty about
> one variable when we observe another. In the application later in the
> talk, the variables are the month of a website visit and whether that
> session ends in a purchase. We can measure their association separately
> among new visitors and returning visitors. I call their joint population
> distributions P and Q. The question is whether the population MI differs
> between those groups. It is an association question, and it does not
> require a causal interpretation of month. Before using observed data,
> however, we need a way to account for sampling uncertainty in that
> comparison.

**Delivery cue:** Explain the definition facing the audience, then point
once to each group. Do not announce the application result yet.

**Transition:** “Two different sample estimates can arise even when the
population MI values are equal.”

**Source/citation:** Thesis Sections 1.1 and 2.1; Bossomaier et al. (2016).
The shopping example is from Section 6.4, pp. 69–71.

### Slide 3 — Sampling uncertainty in the MI comparison

**Purpose and takeaway:** State the hypothesis, explain the finite-sample
problem, and define the false-positive target.

**Exact on-slide copy:**

\[
\Delta=I(P)-I(Q),\qquad H_0:\Delta=0
\]

- Rare category combinations may be missed or observed only once
- Errors can affect both the estimated MI difference and its standard error
- Under equal population MI, the intended rejection rate is 5%

**Layout:** Combine the spacious research-question treatment of reference
Slide 5 with the pale equation area of reference Slide 2. Centre the large
editable hypothesis in a shallow pale-orange rounded panel in the upper
content area. Below, keep the two explanatory lines left aligned, and
highlight the existing 5% target once in orange or bold black. A small
schematic count table may sit beside the explanation to identify a rare
cell, with no invented empirical numbers. Keep generous white space and
use the current copy without adding a separate roadmap or new summary.

**Speaker script:**

> The parameter is the signed difference, MI in P minus MI in Q, and the
> null hypothesis sets that difference to zero. Different samples produce
> different count tables, so they also produce different MI estimates.
> Rare combinations of categories are especially difficult because a cell
> can be missed in one sample and observed only once in another. These
> errors can change both the estimated difference and its estimated
> standard error. When the population MI values are equal, I want a test
> using the usual five-percent significance level to reject in about
> five percent of repetitions. That false-positive target gives us a
> concrete way to assess the comparison.

**Delivery cue:** Pause after naming the null. Stress that equal MI allows
different probability tables. Do not imply P=Q under every null setting.

**Transition:** “The literature supplies the MI variance approximation, but
choosing a Welch-type reference requires an additional calculation.”

**Source:** Thesis Chapters 1–3, particularly Equations (1.1), (3.3)–(3.10).
Use source labels rather than assuming equation numbering when authoring.

### Slide 4 — Existing foundations and the MI-specific contribution

**Purpose and takeaway:** Demonstrate relevant literature engagement and
locate the student's contribution without a global priority claim.

**Exact on-slide copy:**

| Part of the method | Role in this project |
| --- | --- |
| MI bias and sampling variance | Estimate the difference and its uncertainty |
| Welch–Satterthwaite moment matching | Choose a reference from variance-estimator variability |
| MI-specific variance sensitivity, derived here | Track changes in cell probabilities, margins and pointwise MI |

Place a short source line naming Moddemeijer (1989), Paninski (2003),
Satterthwaite (1946), Welch (1947), Hutcheson (1970), and Pan and Wall (2002).
The notes may also identify Mora and Ruiz-Castillo (2009) as the direct
normal-approximation precedent for MI comparisons.

**Layout:** Adapt the comparison-matrix treatment of reference Slide 7.
Use a native two-column table with three generous rows, orange column
labels, thin light-grey row rules and black body text. Give the final,
MI-specific row a pale-orange fill and bold its key phrase so the original
contribution is easy to locate. Keep literature names in the existing
source line, not miniature paper covers or extra callout boxes. Retain
Lato and the reference title position.

**Speaker script:**

> This project builds on established results rather than introducing the
> general Welch–Satterthwaite principle. Work on MI gives the leading bias
> and first-order sampling variance. Welch and Satterthwaite provide a way
> to choose degrees of freedom by matching variance moments, and related
> ideas have been used for entropy and regression comparisons. For this
> MI test, the additional task is to calculate how the estimated
> pointwise-MI variance changes when the table changes. I derive that
> sensitivity while allowing the cell probabilities, row totals and column
> totals to change together, then evaluate the resulting approximation.

**Delivery cue:** Spend most of the slide on the final row. Say what each
strand provides; do not recite every citation or claim that no equivalent
formula has ever appeared anywhere.

**Transition:** “The resulting test keeps the same statistic as Wald and
changes the reference distribution used to judge it.”

**Source:** Thesis Sections 2.2–2.5, pp. 6–17; references.bib keys
`moddemeijer1989`, `paninski2003`, `satterthwaite1946`, `welch1947`,
`hutcheson1970`, `panwall2002`, `mora2009`.

### Slide 5 — Normal Wald and Expanded Welch

**Purpose and takeaway:** Explain the shared statistic and the different
reference distributions before showing any comparative results.

**Exact on-slide copy:**

\[
T=\frac{\widehat\Delta_{\mathrm{BC}}}{\widehat{\mathrm{SE}}},
\qquad
\widehat{\mathrm{SE}}^2=
\frac{\widehat V(P)}{n_P}+\frac{\widehat V(Q)}{n_Q}
\]

- Normal Wald: standard normal reference
- Expanded Welch: Student t reference with estimated degrees of freedom
- Same estimates and statistic, larger rejection cutoff

Put a concise definition directly beneath the numerator:
“BC: leading bias correction”. Do not leave the subscript unexplained.

**Layout:** Use reference Slide 3's orange/navy comparison treatment.
Place the shared equations in a shallow pale-orange rounded area across
the upper content region, with the BC definition directly beneath the
numerator. In the lower region, put two compact method panels at left:
an orange Normal Wald header with a pale-orange body, and a navy Expanded
Welch header with a pale-blue body. Use the existing reference-distribution
labels as their contents. At right, give most of the space to a single
shared-axis density plot comparing the standard normal distribution with
a Student t distribution with 3 degrees of freedom. Label the plot as an
illustration and indicate the two-sided 5% cutoffs, about ±1.96 and ±3.18.
Use matching orange/navy curves and direct distribution labels for this
illustrative plot only. The empirical charts retain their separate
encodings below. Put “Same estimates and statistic, larger rejection
cutoff” in the short introduction under the title. Keep the illustrative
df separate from the df actually estimated in the experiment.

**Speaker script:**

> Both methods divide the MI difference, after its leading bias correction,
> by the same estimated standard error. The denominator adds a variance
> contribution from each independent sample. Pointwise MI is the information
> contribution of one category pair. V-hat estimates its variance, and
> dividing by sample size estimates the sampling variance of an MI estimate.
> Wald compares the statistic with the standard normal
> distribution. Expanded Welch uses a Student t distribution, whose
> degrees of freedom are estimated from the data. The example with three
> degrees of freedom shows why heavier tails give a larger rejection
> cutoff. Consequently, Expanded Welch's rejections are a subset of
> Wald's under these testing rules. The next question is how to calculate
> the degrees of freedom for MI.

**Delivery cue:** Trace the common numerator and denominator once. Point
to the cutoff locations. Explain that the reference plot's three degrees
of freedom are illustrative; actual values vary between sampled table pairs.
Expanded Welch also needs valid df calculations; the additional validity
requirements are introduced on Slide 7 and specified in B4.

**Transition:** “The important input is how much the variance estimate
itself changes from sample to sample.”

**Source:** Thesis Sections 3.2–3.3 and 4.1–4.3; Figure 2.1. Read the
shared-SE, shared-statistic and Expanded-Welch df equations from source.
The existing reference-distribution PDF/code may inform the new plot.

### Slide 6 — Deriving the degrees of freedom

**Purpose and takeaway:** Explain the original mathematical calculation
and how it becomes an executable test, without reproducing every algebraic
step in the talk.

**Exact on-slide copy:** Use three numbered rows with these labels and
editable equations. Label P-epsilon in words as moving a small amount of
probability towards cell (x,y).

1. **Sensitivity of the pointwise-MI variance**

   \[
   g_P(x,y)=\left.\frac{\mathrm d V(P_\varepsilon)}
      {\mathrm d\varepsilon}\right|_{\varepsilon=0}
   \]

2. **Sampling variation of its estimate**

   \[
   \operatorname{Var}\{\widehat V(P)\}\approx\frac{\tau^2(P)}{n_P},
   \qquad \tau^2(P)=\operatorname{Var}_P\{g_P(X,Y)\}
   \]

3. **Component degrees of freedom**

   \[
   \widehat\nu_P=\frac{2n_P\widehat V(P)^2}{\widehat\tau^2(P)}
   \]

Bottom line: “Repeat for Q and combine the components using
Welch–Satterthwaite moment matching.”

**Layout:** Use three wide, shallow pale-orange rows, following the
numbered-step styling of reference Slides 8 and 10. Each row begins with
an orange numbered circle, followed by its existing verbal role at left
and editable equation at right. Keep the first row's reminder, “Track
joint, row and column changes together”, beside that row without crowding
the derivative. Thin outlines and modest rounded corners should match the
reference. Use simple vertical alignment to show the sequence; a short
connector is optional only where it clarifies the calculation. Keep the
existing final Welch–Satterthwaite sentence below the three rows. The exact
expanded formula for g remains in Backup B1, with no fourth main block.

**Speaker script:**

> There are two levels of variability here. V-hat describes variation in
> pointwise MI across observation outcomes, but V-hat itself also changes
> when a new sample gives a different table. I first calculate its
> sensitivity to moving a small amount of probability towards one cell.
> That change affects the selected cell, its row and column totals, and
> the pointwise-MI values. The derivative g collects those effects.
>
> Averaging the observation-level sensitivities gives a first-order
> approximation to the sampling error of V-hat. Its sampling variance is
> therefore approximately tau-squared divided by sample size. I then use
> Satterthwaite moment matching: twice the squared mean of a variance
> estimate, divided by that estimate's sampling variance. Substituting
> the sample-based inputs gives the component formula at the bottom.
> Greater fluctuation relative to the squared mean gives fewer degrees
> of freedom and a larger cutoff. I repeat the calculation for Q and
> combine the components. This is an approximate Student t reference,
> so the experiments must check how well these steps work.

**Delivery cue:** Use the full two minutes. Pause at each change of level
of variance. The final formula gives component df, not the combined df.
Do not suggest that moment matching proves the numerator and denominator
are independent. If asked for the exact derivative, show Backup B1.

**Transition:** “I checked the variance approximations first, then evaluated
false positives and power using populations whose MI values are known.”

**Source:** Thesis Sections 4.1–4.3, pp. 23–35, specifically source labels
`eq:g-definition`, `eq:g-final`, `eq:vhat-sampling-variance`,
`eq:component-df-moments`, `eq:nu-p-hat`, `eq:expanded-df`.

### Slide 7 — Evaluation from known populations

**Purpose and takeaway:** Establish the design before results. Distinguish
the number of observations in each sample from simulation repetitions.

**Exact on-slide copy:**

| Question | Known-population comparison |
| --- | --- |
| RQ1: Approximation accuracy | Mean and sampling variance of V-hat, including near independence |
| RQ2: False positives | Equal MI: 0.005, 0.02 and 0.30 nats |
| RQ3: Power | MI in P = 0.02; gaps of 0.005, 0.01 and 0.02 nats |

- Four table sizes: 2×2, 4×4, 8×8, 16×16
- Uniform, same-skew and different-skew margins
- Ten sample sizes, 10 to 50,000 observations per population
- 100,000 independent table pairs per setting

Use a small source line: “Both methods use each same pair of sampled
tables. Invalid outputs count as non-rejections; validity is reported.”

**Layout:** Adapt reference Slide 9's paired evaluation and parameter
areas. At left, use a navy heading and pale-blue area for the three
research questions and their known-population comparisons. Keep each
question with its comparison as an aligned row. At right, use an orange
heading and pale-orange area for the four shared setting bullets. Keep
sample size and repetitions on separate lines so 100,000 cannot be read
as the observations available to a test. Use the existing source-line
sentence below both areas. Avoid splitting each number into a separate
small box. Full margin vectors and the sample-size list remain in B3.

**Speaker script:**

> I construct population tables with known MI, then draw repeated samples.
> MI is reported in nats, using natural logarithms. The first study checks
> the variance approximations. The false-positive
> study uses three equal-MI levels, while power fixes MI in P at 0.02 nats
> and gives Q three larger MI values. Both studies cross four table sizes
> and ten sample sizes with uniform or uneven margins. The uneven margins either
> agree between populations or differ, giving 360 settings each for false
> positives and power. Each test sees only its two sampled tables. The
> 100,000 repetitions measure performance rather than increasing that
> test's sample size. Both tests use the same sampled pairs, with invalid
> calculations counted as non-rejections and validity reported separately.

**Delivery cue:** Explain “same skew” as the same uneven margins in both
populations and “different skew” as different category frequencies.
Do not recite all ten sample sizes or every margin probability.

**Transition:** “The first result concerns the inputs to the degrees of
freedom, before any test rejection is considered.”

**Source/citation:** Thesis Chapter 5, pp. 39–46, Tables 5.1–5.3;
Morris et al. (2019). Exact construction and validity rules: Appendix B.

### Slide 8 — Sparse samples distort the variance inputs

**Purpose and takeaway:** Demonstrate that both the mean approximation and
sampling-variance approximation can fail. Distinguish population inputs
from sample-based inputs.

**Exact on-slide copy:**

- Setting line: “Different-skew P, 16×16, population MI 0.02 nats”
- Left chart heading: “Mean estimate / population variance”
- Right chart heading: “Variance prediction / observed sampling variance”
- Below charts: “One indicates agreement. Errors affect both parts of
  the degrees-of-freedom calculation.”

**Layout and evidence:** Follow reference Slide 4's two-plot comparison.
Use the existing setting line under the black title, then two equally
sized white charts with orange Lato panel headings. A thin light-grey
vertical divider is optional if it improves separation. Replot the P/16×16
slice of Figure 6.1. The left chart uses `mean_ratio`. The right overlays
`variance_ratio` and `plugin_variance_ratio`, labelled “Population inputs”
and “Sample-based inputs”. Both horizontal axes use the ten sample sizes
on a log scale. The left y-axis is logarithmic, approximately 0.9–20;
the right is logarithmic, approximately 0.1–3. Both have a clear reference
at one. Retain restrained saved Monte Carlo intervals. Keep the existing
interpretation in one line below the charts rather than adding separate
panels for each curve. Treat this as one illustrative slice, not the full
RQ1 study. Use the manifest's null-display ID filter to avoid mixing
near-independence rows into this plot.

**Speaker script:**

> This slide isolates one population and table size so the two errors are
> visible. On the left, one would mean that the average V-hat equals the
> population quantity. Instead, the mean rises well above that benchmark
> before recovering. Rare cells that begin to appear can have large
> empirical pointwise-MI deviations and inflate the estimate.
>
> On the right, one means that the predicted sampling variance of V-hat
> agrees with the variance observed across repetitions. The population
> first-order prediction falls below one over the sparse range. Estimating
> its inputs from each sample can reverse the error and overshoot. Since
> degrees of freedom square the mean input and divide by the sampling
> variance input, both errors matter. Larger samples improve the agreement
> in this fixed population.

**Delivery cue:** Explain the left graph completely before moving right.
Say “sampling variance of V-hat” explicitly. Do not call the right graph
the sampling variance of the MI estimator. Avoid narrating every marker.

**Transition:** “Near independence, sampling noise causes an additional
separation between the population formula and the sample-based result.”

**Source:** Thesis Section 6.1.1, pp. 47–50; Figure 6.1. CSV source:
`WelchSatterthwaiteMI/results/approximation_redesign/moments.csv`, joined
to the `null` IDs in `displays.csv`. See the manifest for exact columns.

### Slide 9 — Sampling noise matters near independence

**Purpose and takeaway:** Give the important near-independence check its
own main slide. Explain why the sample-based df do not follow the shrinking
population first-order value.

**Exact on-slide copy:**

- Setting line: “Different-skew P, 4×4, n = 1,000 per population”
- Curve labels: “Mean estimated component df”, “Sampling-moment target”,
  “Population first-order value”
- Callout: “At MI 0.0001: mean estimate about 5; first-order value about 0.1”
- Bottom line: “Quadratic sampling variation creates apparent association”

**Layout and evidence:** Use a large white chart at left, approximately
70% of the content width, and a single pale-orange explanation panel at
right, following the evidence/explanation balance in reference Slide 9.
The panel contains the existing low-MI callout and bottom-line explanation,
with an orange heading and black text. Use the P/4×4/n=1,000 association
grid underlying Figure 6.3. Plot `df_mean`, `nu_mom` and `nu_fo` against
population MI, with both axes logarithmic. Keep the established curve
colours: mean estimate muted crimson `#A53648`, moment target green `#34866F`,
population formula black and dotted. The orange panel does not change
those data encodings. Preserve the seven MI values. Directly label curves
or use an unambiguous legend. Do not label the moment target “true t df”.
The local noise prediction and its algebra remain in Backup B5.

**Speaker script:**

> Here sample size stays at one thousand and the population MI approaches
> zero. The black population first-order value becomes very small, but
> the mean degrees of freedom estimated from sampled tables remain around
> five at the weakest association. The green curve is the moment-matching
> target calculated from the actual sampling mean and variance. That
> target is about nine, so the mean estimate is still only about half
> the target.
>
> A sampled table can show apparent association even when population
> association is almost absent. The sample-based variance and sensitivity
> retain that noise. Near independence, the linear sampling contribution
> becomes small, so quadratic sampling terms matter. The additional
> calculation in the thesis explains why the estimated degrees of freedom
> stay positive rather than following the shrinking population value.
> This is a check on the approximation, not a proof of an exact Student t
> distribution or a validated replacement test at independence.

**Delivery cue:** Point to the low-MI end before describing the curves.
Pause after “around five”. Explain the target's role rather than reading
three symbols. Preserve this slide in the shorter route.

**Transition:** “These approximation errors matter because the larger
cutoff lowers rejection, and that reduction is not equally helpful everywhere.”

**Source:** Thesis Section 6.1.3, pp. 52–56, Figure 6.3 and Appendix A.2.
At MI 0.0001, saved P values are mean df 4.859787, moment target 9.124808,
and population first-order df 0.096400. These are component quantities.

### Slide 10 — The benefit depends on Wald's false-positive rate

**Purpose and takeaway:** Demonstrate conditional benefit using three
clearly labelled examples at one common MI. Define accuracy through
closeness to 5%, not through lower rejection alone.

**Exact on-slide copy:**

Setting line: “Equal population MI = 0.02 nats; target false-positive rate = 5%”

| Illustrative setting | Normal Wald | Expanded Welch | Interpretation |
| --- | --- | --- | --- |
| Uniform 4×4, n=20 | 8.35% | 4.90% | Closer to 5% |
| Same skew 16×16, n=1,000 | 0.60% | 0.53% | Further below 5% |
| Different skew 16×16, n=1,000 | 26.01% | 24.84% | Still far above 5% |

Below the table: “Both methods are valid in all 100,000 repetitions in
each example.”

**Layout:** Use a large native comparison table styled after reference
Slides 7 and 9. Give the setting column an orange heading, the two method
columns the orange/navy labels already introduced on Slide 5, and the
interpretation column a neutral black heading. Use white body cells,
light-grey row rules and generous spacing; a very light peach tint may
identify the first example without labelling the method generally better.
Allow two lines per setting. Align all percentages and keep the existing
interpretations. Bold the 5% target and first row's 4.90%. Keep the complete
validity sentence below the table. Do not replace it with a 0–30% bar chart
that conceals the 0.60%/0.53% comparison. This remains an illustrative
diagnostic table, not an average over the grid.

**Speaker script:**

> I assess false-positive accuracy by closeness to five percent. The first
> row shows the useful case: Expanded Welch brings Wald's excessive
> rejection from 8.35 percent to 4.90 percent. In the second row, Wald
> already rejects too rarely, and the larger cutoff lowers rejection
> further. The third row shows a more serious failure: rejection stays
> around a quarter of repetitions even after the cutoff increases.
>
> These examples have no calculation failures. Their different behaviour
> comes from the shared estimates and the sampling distribution of the
> statistic. In particular, different remaining biases can shift the MI
> difference away from zero under equal MI. A larger cutoff can offset
> some errors at a particular setting without making inference accurate
> across populations.

**Delivery cue:** Take one row at a time. Point back to the same 5% target
for each row. Do not describe the table as three predetermined focus
settings A, B and C or as evidence of universal improvement.

**Transition:** “The full experiment also changes the common MI, while
keeping the population difference at zero.”

**Source:** Thesis Section 6.2.4 and Table 6.1, p. 62. Use the combined
balanced-null rates, not old focus-case or calibrated-power tables.

### Slide 11 — False-positive rates across common MI values

**Purpose and takeaway:** Show a broad sample-size comparison and make
clear that valid calculations and larger samples do not automatically
produce accurate rejection at the tested sizes.

**Exact on-slide copy:**

- Setting line: “16×16, different-skew margins; equal MI in P and Q”
- Plot annotation at common MI 0.005 and n=1,000:
  “Wald 36.38%; Expanded Welch 34.38%”
- Below chart: “Both methods are valid in every repetition at this point”

**Layout and evidence:** Use the reference Slide 4 chart treatment at
full presentation width, with the existing setting as the introduction
under the black title. Replot the 16×16 panel of Figure 6.6, retaining all
three common MI levels, both methods, ten sample sizes, pointwise intervals
and the lower validity strip. Use a 0–40% main y-axis and a clearly labelled
5% line. The numerical annotation may use a small pale-orange callout in
unused chart space beside the blue peak. It must point unambiguously to
the common-MI 0.005, n=1,000 values and cover no evidence. Keep the validity
strip at 0–100% and the legend “Common population MI (nats)”. Keep plot
colours and method markers unchanged by the surrounding orange/navy theme.
Backups B6–B8 provide the full null figures.

**Speaker script:**

> This panel keeps equal MI in the two populations but changes the common
> level of association. Colour identifies that common MI, and line style
> identifies the method. At the weakest MI and one thousand observations
> per population, Wald rejects in 36.38 percent of repetitions and Expanded
> Welch in 34.38 percent. The validity strip shows that both methods return
> usable results in every repetition there. The failure is inferential.
>
> With more observations, rejection falls, and the weakest-MI curve is
> below the target at the largest tested sample size. The experiment can
> therefore pass through excessive and conservative ranges. The larger
> cutoff lowers rejection throughout, but it does not by itself solve
> either problem.

**Delivery cue:** Introduce axes and encodings before pointing to the
peak. Say which common MI the highlighted values use. Avoid presenting
36.38% as the MI-0.02 value from Slide 10.

**Transition:** “The same larger cutoff also affects the probability of
detecting a genuine MI difference.”

**Source:** Thesis Section 6.2.3, pp. 60–61; Figure 6.6. Exact source:
balanced-null `combined_rates.csv`, `k=16`, `profile=different_skew`,
`denominator=all`. No threshold fitting is involved.

### Slide 12 — Power across three MI differences

**Purpose and takeaway:** Define nominal power and show its relation to gap
size and sample size. Keep the interpretation consistent with the known
nesting of the tests' decisions.

**Exact on-slide copy:**

- Setting line: “Uniform 4×4; MI in P = 0.02 nats”
- Gap legend: “MI-gap magnitude: 0.005, 0.01, 0.02 nats”
- Below chart: “Usual 0.05 p-value threshold for both methods”
- Interpretation: “With sufficient observations, larger MI gaps are easier
  to detect. Expanded Welch has a lower or equal rejection rate.”

**Layout and evidence:** Reuse Slide 11's large white plotting area,
Lato typography and compact setting introduction, following reference
Slide 4. Replot the 4×4 uniform panel of Figure 6.7 using all three gaps
and both methods. Retain the 0–100% power axis, pointwise intervals and
validity strip. Colour now means gap magnitude. Preserve the method
line/marker conventions and gap colours. Keep “Power: rejection when
population MI differs” near the y-axis and the existing interpretation
below the chart in black, with at most one short orange emphasis. Do not
add decorative panels over the plot or an inset of calibrated power.

**Speaker script:**

> Power is the probability of rejecting equal MI when the population MI
> values differ. Colour now identifies the magnitude of the MI gap.
> P stays at 0.02 nats, and Q's MI increases to create the three gaps.
> Once samples are sufficiently large, the larger differences become
> easier to detect. Expanded Welch remains at or below Wald because its
> cutoff is larger, with the method curves becoming close at larger
> sample sizes.
>
> These are power rates under the usual testing rules. Because actual
> false-positive rates can differ, they do not compare power at a common
> achieved false-positive rate. The next example also shows why a
> two-sided rejection can conceal an important error in direction.

**Delivery cue:** Explicitly announce the change in colour meaning from
Slide 11. Do not interpret close curves as a plotting failure or claim
Expanded Welch has higher nominal power anywhere.

**Transition:** “In sparse tables with different margins, bias can even
make the estimated difference point towards the wrong population.”

**Source:** Thesis Section 6.3.1, pp. 63–65, Figure 6.7; MI-gap
`combined_rates.csv`, `k=4`, `profile=uniform`, `denominator=all`.

### Slide 13 — Bias can reverse the estimated direction

**Purpose and takeaway:** Show the most informative sparse-table power
failure and explain its mechanism. Separate two-sided rejection from
correctly identifying the direction of association.

**Exact on-slide copy:**

- Setting line: “Different-skew 16×16; MI 0.02 versus 0.03 nats”
- Right-side comparison at n=1,000:
  - True difference: −0.0100 nats
  - Mean estimated difference: +0.0207 nats
  - Among Expanded Welch rejections, over 99.9% have the opposite
    estimated direction
- Beneath comparison: “Unequal residual biases can outweigh the true gap”

**Layout and evidence:** Follow reference Slide 9's split layout. Give
the left two thirds to the white chart and the right third to one pale-blue
result panel with a navy heading identifying n=1,000. Replot the 0.01-gap
curve from the 16×16 different-skew power panel, retaining both methods,
all sample sizes and intervals. Keep this gap orange `#E69F00`, with
methods distinguished by line and marker. Use a 0–100% power axis and
compact validity strip. In the result panel, align the true and mean
estimated differences as large signed black numbers, then give the
existing conditional wrong-direction statement. Orange emphasis can
highlight “among Expanded Welch rejections”. Preserve that denominator
in readable text, followed by the residual-bias explanation. Do not label
99.9% as a fraction of all repetitions or all estimates.

**Speaker script:**

> This example fixes a true difference of minus 0.01 nats, so Q has greater
> population MI. At one thousand observations per population, however,
> the average estimated difference is about plus 0.0207 nats. Different
> residual biases in the two MI estimates have outweighed the true gap
> and shifted the sampling centre to the other side of zero.
>
> Expanded Welch rejects in about 9.66 percent of repetitions at this
> point. Among those rejections, more than 99.9 percent have a positive
> estimated difference, opposite to the population direction. They count
> as power under the two-sided definition, but they fail to identify which
> population has greater MI. As sample size increases, the positive bias
> diminishes, the centre passes near zero, and rejection initially falls
> before recovering. Changing the cutoff leaves that biased movement
> unchanged.

**Delivery cue:** Explain the two signed numbers before citing the
percentage. Emphasise “among those rejections”. The bias is approximately
0.0306714 nats; the estimated mean is −0.01 plus that bias. Do not
describe a positive estimate as higher true MI in P.

**Transition:** “The shopping data illustrate the same calculation, although
their unknown population values prevent this kind of accuracy check.”

**Source:** Thesis Section 6.3.3, pp. 67–69; Figure 6.9 and its
interpretation. Saved counts: 9,659 positive and 3 negative Expanded
Welch rejections, for 9,662 total. Rates and diagnostics are in the
MI-gap combined CSVs.

### Slide 14 — An application to online shopping

**Purpose and takeaway:** Return to the opening example and demonstrate
how to interpret estimates and test outputs without claiming real-data
calibration has been established.

**Exact on-slide copy:**

- Question: “Does month–purchase MI differ between new and returning visitors?”
- Left chart: “Corrected MI estimate (nats)”
  - New visitors: 0.0043
  - Returning visitors: 0.0179
- Right-side result:
  - Estimated difference, new minus returning: −0.0136 nats
  - Both tests reject after Holm adjustment across six comparisons
  - Expanded Welch adjusted p = 0.00149
- Bottom line: “Observed-data illustration; population MI is unknown”

**Layout and evidence:** Follow reference Slides 3 and 9: a white chart
at left and one pale-blue result panel with a navy heading at right. Put
the existing shopping question under the title. Use two simple navy bars
for the corrected MI point estimates, starting at zero with a shared
axis. Label the groups and values directly and state that they are point
estimates; do not add invented group-level error bars. The right panel
contains the signed difference, adjusted inference and p-value, with a
short orange emphasis where useful. Group labels may include n=1,694
and n=10,551; keep those counts out of the main spoken comparison. Put
the existing unknown-population statement below the evidence and the UCI
and Holm citations in the source line. The full six-comparison family
remains in B10.

**Speaker script:**

> Returning to the shopping question, I compare the association between
> month and purchase outcome among new and returning visitors. The
> corrected MI estimate is higher for returning visitors, giving a
> negative difference when I subtract returning-visitor MI from
> new-visitor MI. Both methods reject equal MI, including after Holm
> adjustment across the six exploratory comparisons. Expanded Welch's
> adjusted p-value is about 0.00149.
>
> This is evidence from the approximate tests for a difference in
> month–purchase MI. It is not a causal claim about month. Unlike the
> simulations, the population tables are unknown, so this application
> illustrates how to use and interpret the outputs without measuring
> their false-positive accuracy. The weekend comparison does not reject
> equality, which also does not establish equality.

**Delivery cue:** Keep the emphasis on association, signed difference and
adjusted inference. Explain the six-comparison family if asked. Do not
claim Holm adjustment repairs the test's approximation errors.

**Transition:** “The application makes the practical limits important, so
I will finish by distinguishing the contribution from what remains to test.”

**Source/citation:** Thesis Section 6.4, pp. 69–71, Tables 6.2–6.3 and
Appendix B.7. Sakar and Kastro (2018); Holm (1979). Source values are in
`PracticalMIExploration/thesis_application/full_data_results.csv`.

### Slide 15 — Limitations and future work

**Purpose and takeaway:** Demonstrate critical evaluation and connect each
future direction to a demonstrated limit.

**Exact on-slide copy:**

| Present limit | Next investigation |
| --- | --- |
| First-order approximation near independence | Retain the additional quadratic sampling variation |
| Bias and errors in the shared standard error | Evaluate improved estimates one at a time |
| One population construction; equal simulation sample sizes | Test other association patterns and unequal sample sizes |

**Layout:** Adapt reference Slide 7's comparison matrix to the existing
three-row table. Use an orange “Present limit” header and a navy “Next
investigation” header, with white or very pale matching cells beneath.
Align each limitation with its corresponding next investigation. Use
Lato at a readable size, thin light-grey row rules and modest corner
rounding only on the header containers. Retain complete phrases and
sufficient white space. Do not add a new list of possible extensions.

**Speaker script:**

> The first limitation is the first-order approximation, particularly
> near independence, where additional quadratic sampling variation
> becomes important. The second is estimation: changing the reference
> cutoff leaves errors in the MI difference and standard error in place.
> A useful next step is to change one estimator at a time and check how
> that affects rejection and direction.
>
> The experiments also use one copying construction and equal sample
> sizes. They vary several important parameters within that family,
> but they do not establish performance across every association pattern.
> Other constructions and unequal sample sizes would test how broadly
> the findings persist.

**Delivery cue:** Use the paired rows to show why each proposed extension
makes sense. Keep to one minute and protect time for the conclusion.

**Transition:** “The project therefore establishes a specific calculation
and a clear boundary on what its cutoff adjustment can accomplish.”

**Source:** Thesis Sections 7.2–7.3, pp. 74–75.

### Slide 16 — Contributions and conclusions

**Purpose and takeaway:** State the contribution and answer the original
question in language understandable without the detailed derivation.

**Exact on-slide copy:**

- Derived MI-specific variance sensitivity and degrees of freedom
- Improved some excessive false-positive rates, with a reduction in power
- Sparse-table failures identify estimation accuracy as a priority

Use “Thank you” in small type if desired. Do not replace the conclusion
with a large “Questions?” label. Keep this slide visible during discussion.

**Layout:** Adapt the contribution blocks in reference Slide 8. Beneath
the common black title, use a shallow navy “Contributions” header and three
pale-blue blocks with navy numbered circles. Each block contains one of
the existing three statements in Lato at 22–24 pt. Keep the blocks wide
and tall enough for natural line wrapping, with generous internal space,
thin blue outlines and modest rounded corners. Bold only the existing key
phrases “variance sensitivity”, “some” and “estimation accuracy”. Keep
“Thank you” small below the group if used. No new plots, numerical claims
or equations. This is the concluding slide displayed during questions.

**Speaker script:**

> I derived how the estimated pointwise-MI variance responds to changes
> in a count table and used that sensitivity to calculate MI-specific
> degrees of freedom. The resulting larger cutoff brings some excessive
> false-positive rates closer to five percent, but also deepens
> conservatism and reduces power under the usual testing rules.
>
> The sparse-table failures show why the estimates themselves remain
> important. A different cutoff leaves bias and standard-error errors
> unchanged. The contribution is therefore both the calculation and
> the evidence identifying its limits. Thank you, and I welcome your
> questions.

**Delivery cue:** Face the audience for the final statements. Do not rush
through “some” or imply a general recommendation. Stop at approximately
18:50, with the conclusion still displayed.

**Source:** Final abstract, Sections 1.3 and 7.1–7.3.

## 7. Backup slide specifications

Backups begin immediately after Slide 16. Do not add an appendix divider.
Use the same visual system, but identify the slides as backup material.
The physical slide numbers are 17–28. In PowerPoint, Daniel can jump by
typing the slide number and Enter, then return to Slide 16. Do not add
navigation buttons or a projected file inventory.

Carry the reference's Lato titles, orange/navy headings and pale panels
through all backups. Use a shallow pale-orange equation area on B1, and
orange/navy component/combined sections on B2. B3–B5 and B10 use the same
readable comparison-table styling as the main talk. Keep B6–B9 as white
four-panel figures with short orange panel headings, not four heavy
framed cards. These treatments change the presentation of the material;
the formulas, numerical values, denominators and question answers below
remain the same.

### B1 / Slide 17 — Variance sensitivity

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
Use at least 24–26 pt for the main equation. Do not replace conditional
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
for the first-order df construction. Positive MI alone does not guarantee
positive tau-squared. Do not treat a zero component as ordinary finite df.

### B2 / Slide 18 — Moment matching and the combined reference

**Question answered:** Where do the component and combined df formulas
come from, and why is the Student t reference approximate?

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
The resulting Student t reference still requires empirical assessment.”

**Source:** Thesis Sections 4.1 and 4.3, pp. 23–35; Satterthwaite (1946).

### B3 / Slide 19 — Population construction and parameter grid

**Question answered:** How are different tables constructed at a known
MI, and what parameter combinations were evaluated?

**Show:** At top,

\[
p_{ij}(\lambda)=(1-\lambda)a_i a_j+
\lambda a_i\mathbf 1\{i=j\},\quad 0\leq\lambda<1.
\]

Use a compact two-column table below with these exact settings:

- k: 2, 4, 8, 16.
- n: 10, 20, 50, 100, 250, 500, 1,000, 2,500, 10,000, 50,000.
- Uniform: both margins uniform in both populations.
- Same skew: P and Q each use \(m_k(0.8)\).
- Different skew: P uses \(m_k(0.7)\); Q uses \(m_k(0.8)\).
- Null: common MI 0.005, 0.02, 0.30 nats.
- Power: P MI 0.02; Q MI 0.025, 0.03, 0.04 nats.

Define \(m_k(\rho)=(\rho,(1-\rho)/(k-1),\ldots)\) in a readable
setting line. If the complete list is crowded, move the n list to a single
full-width line, not smaller type.

**Answer to give:** “The construction mixes an independent draw with a
copying draw. It preserves the specified margins, while the copying
probability controls association. I solve separately for the copying
probability in each population to reach the target MI. The full grid is
evaluated at every null MI and power-gap value; it is not a selection of
favourable cases.”

**Source:** Thesis Section 5.1, Tables 5.1–5.2 and Appendix B.1–B.2.
The construction is one controlled association family, not a representation
of every possible categorical joint distribution.

### B4 / Slide 20 — Validity and rejection denominators

**Question answered:** How are degenerate calculations handled, and can
calculation failures explain low rejection?

**Show:** Two short definitions at left:

- Wald: finite difference, finite positive standard error,
  \(\widehat V(P)+\widehat V(Q)>10^{-14}\), finite p-value.
- Expanded Welch: Wald requirements plus positive finite component and
  combined df, and a finite p-value.

At right, show the main reported denominator:

\[
\text{rejection rate}=
\frac{\text{valid rejections}}{\text{all repetitions}}.
\]

Then: “Validity is reported separately. An invalid calculation is not
evidence that the null is true.” Retain the distinction between zero and
undefined df. Put the full componentwise numerical rules in notes.

**Answer to give:** “The rate measures the complete implemented procedure,
including failures, so invalid outputs count as non-rejections. The separate
validity measure lets us see that contribution. Conditioning on validity
would answer a different question and select a different subset of samples.
Several important failures persist with 100% validity, including the large
false-positive rate highlighted in the talk.”

**Source:** Thesis Appendix B.3–B.5 and the validity strips in Figures
6.4–6.9. Do not change the implemented validity rules for this presentation.

### B5 / Slide 21 — The near-independence noise calculation

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

Use the notes for the formulas
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

### B6 / Slide 22 — Null results with uniform margins

**Question answered:** What happens outside the highlighted different-skew
16×16 example?

**Show/layout:** Replot all four table-size panels of Figure 6.4 in a
readable 2×2 grid, with all three MI levels and both methods. Share the
method and MI legends. Use at least 18–20 pt labels and fewer ticks where
necessary. Preserve the original y-axis range for each table size and keep
those ranges identical in B6–B8. Omit the validity strips on these backup
pages to preserve readable plotting space; state the all-repetitions
denominator in a single footnote and point to B4 and the thesis for validity.

**Answer to give:** “Under the copying construction, equal MI and uniform
margins give identical population tables. Their expected MI biases cancel
in the difference, but errors in the uncertainty estimate and reference
distribution can still cause excessive or conservative rejection. Increasing
common MI changes those patterns.”

**Source:** Final Figure 6.4 and balanced-null combined rates, uniform
profile. This page contains all 120 settings for that profile.

### B7 / Slide 23 — Null results with same-skew margins

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

### B8 / Slide 24 — Null results with different-skew margins

**Question answered:** Are the severe failures restricted to the largest
table, and what is visible over the complete margin-specific grid?

**Show/layout:** The same layout and scale policy as B6, using all four
panels of Figure 6.6. Label margins \(m_k(0.7)\) in P and \(m_k(0.8)\)
in Q. The main talk already enlarged the 16×16 panel.

**Answer to give:** “Here equal MI permits different population tables.
The remaining MI biases need not cancel, and in the sparse largest table
they can shift the estimated difference substantially away from zero.
The smaller-table patterns and the dependence on common MI remain visible
in this complete slice of the null grid.”

**Source:** Final Figure 6.6 and balanced-null combined rates,
different-skew profile. This page contains all 120 settings for that profile.

### B9 / Slide 25 — Power with same-skew margins

**Question answered:** Do the power patterns also occur when both groups
have the same uneven margins?

**Show/layout:** Replot all four panels of Figure 6.8 in a 2×2 grid, with
all gaps, both methods and a common 0–100% power scale. As on the null
backup pages, omit validity strips for readable panel space, but retain
the all-repetitions denominator statement and method encodings. This
complements the uniform and different-skew examples in the main talk.

**Answer to give:** “These power curves use the same uneven margins in
both populations. Larger tables need more observations, and the smaller
MI gap remains harder to detect. For example, at n=50,000, the 16×16
Expanded Welch power is 79.87% for the smallest gap, compared with more
than 99.9% for each of the two larger gaps. The method difference is
smaller than these gap and setting effects at larger sample sizes.”

**Source:** Final Figure 6.8; Section 6.3.2; MI-gap combined rates,
same-skew profile. This page contains all 120 settings for that profile.

### B10 / Slide 26 — Application details and the comparison family

**Question answered:** Why were six comparisons adjusted, and what else
was tested?

**Show:** An editable table of the six unadjusted p-values from final
Table B.1, in its existing order: Adult occupation, Adult education,
shopping month, student study time, student maternal education, shopping
weekend. Columns identify dataset/predictor, Normal Wald and Expanded
Welch. Below, give the adjusted month values: Wald 0.000189, Expanded
Welch 0.00149. Use the exact source values and appropriate scientific
notation for the very small Adult p-values.

Notes must retain the group sizes, group definitions, the ten recorded
months, missing January/April, and the February new-visitor row with one
session. Include month component/combined df and the weekend non-rejection
for possible follow-up questions. Do not squeeze all these facts onto the
projected table.

**Answer to give:** “The two shopping examples were selected from a fixed
six-comparison exploratory family across three public datasets. I apply
Holm's adjustment separately to each method's six p-values. Both adjusted
month results remain below 0.05. This adjustment addresses multiplicity;
it does not establish that the approximate underlying p-values are calibrated.”

**Source:** Thesis Section 6.4 and Appendix B.7; source application CSV
and its six-comparison protocol. Cite the relevant datasets and Holm (1979).

### B11 / Slide 27 — References: MI and testing foundations

**Show/layout:** Follow reference Slide 11's two-column bibliography,
using three entries per column, but give them larger Lato text at 16–18 pt
and comfortable paragraph spacing. Keep the common 36 pt black title and
white background. Use author, year, title, venue and DOI/URL where supplied.
Do not use a screenshot of a bibliography page. Retain published spelling
and names. Exact bibliographic text comes from the thesis `references.bib`.

Include these keys: `bossomaier2016`, `moddemeijer1989`, `paninski2003`,
`mora2009`, `satterthwaite1946`, `welch1947`.

**Speech:** No prepared narration. Use this page if a source is requested.
It is not part of the 20-minute talk.

### B12 / Slide 28 — References: related methods and evaluation

**Show/layout:** Five entries in the same style and at the same readable
size as B11. Include `hutcheson1970`, `panwall2002`, `morris2019`,
`sakar2018`, `holm1979`.

**Speech:** No prepared narration. Do not add another thank-you or
conclusion page after the references.

## 8. Question preparation

Aim for a direct first sentence, a short explanation and a stopping point.
Use a backup when it will help, rather than opening several slides in
succession. Answers below are starting scripts, not statements Daniel
should read aloud word for word.

| Likely question | Suggested answer and boundary | Backup |
| --- | --- | --- |
| What exactly is new here? | “The MI first-order variance and the general Satterthwaite principle are established. I derive the MI variance sensitivity including the changing margins, use it for component df, and evaluate where the resulting approximation succeeds or fails.” Avoid a claim of global priority beyond the literature review. | B1–B2 |
| Why not just use sample size minus one? | “That assignment follows from the ordinary sample-variance distribution under normal sampling. An estimated pointwise-MI variance depends on changing probabilities and log ratios, so I calculate its sampling variability instead.” | B1–B2 |
| Why does moment matching imply a Student t test? | “It motivates an approximate reference. Matching a scaled chi-squared variance component does not prove the standard normal numerator and independence conditions of an exact Student t construction.” | B2 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | B3, B8 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | B3; cite thesis Section 2.4 in notes |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 15 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 12–13 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 12 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | Slide 13; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 13 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | B5 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | B2, B5 |
| Could invalid calculations explain the low rejection? | “They contribute at some small sample sizes. I report their frequency separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation is valid.” | B4; Slide 11 |
| Why count invalid outputs as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to valid outputs would condition on a selected subset. Reporting validity separately makes the distinction visible.” | B4 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | B3; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | B3, B6–B9 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even with valid outputs. The application illustrates interpretation and cannot verify its population-level accuracy.” | Slides 10–15 |
| Why is the month table 10×2 rather than 12×2? | “January and April have no recorded sessions. Both groups use the same ten recorded month categories and the two purchase outcomes, retaining zero cells within those categories.” | B10 |
| Are the shopping observations independent? | “The dataset documentation says sessions belong to different users. I treat groups and observations as independent, but this remains a working sampling assumption and does not establish representativeness or rule out shared temporal influences.” | B10 |
| Does higher month MI mean a stronger causal month effect? | “It describes greater association in the population comparison. MI depends on the joint probabilities and margins, so it does not isolate a causal response or establish a change in predictive accuracy.” | Slide 14 |
| Why are six comparisons in the Holm family? | “They were the six specified public-data comparisons: two each from Adult, Shoppers and Student Performance. Both shopping results are interpreted within that original family, with a separate adjustment for each test.” | B10 |
| How much computation does one test require? | “The calculations use a fixed number of scans of an r-by-c table, so time and working memory are O(rc). I have not used this presentation to claim a measured runtime advantage over resampling.” | B1–B2; thesis Section 4.4 |

If asked a question the study did not evaluate, state the boundary directly:
“That comparison was not part of the reported experiment. The current
results establish [specific result]; testing [requested extension] would
be the next study.” Do not invent a result to make the answer more complete.

## 9. Rehearsal, timing and an emergency shorter route

### Normal rehearsal

1. First practise the argument without slides. Daniel should be able to
   explain the question, the extra variance calculation and the conditional
   result in about two minutes.
2. Rehearse the full deck with a timer, including every pointer movement
   and graph-reading pause. Record split times at Slides 4, 7, 9, 13 and 15.
3. After learning the script, rehearse from the purpose and cue lines.
   Keep the full script in notes for preparation, not as projected prose.
4. Ask a listener unfamiliar with the derivation what V-hat, its sampling
   variance, and the method comparison mean. Repair the explanation if
   those quantities are confused. Do not solve the problem by adding all
   the algebra to the main slide.
5. Practise jumping from Slide 16 to the correct backup and back. Practise
   at least the questions about exact t validity, the power definition,
   near independence and the six-comparison family.
6. Rehearse from the exported PDF too. Every statement should be supported
   without depending on a live animation, link, notebook or internet access.

Leave brief pauses after introducing axes and after the main signed-number
comparison on Slide 13. Make eye contact after explaining each result.
Finishing earlier than 18:50 is acceptable if the explanation remains
complete. Do not fill spare time with unplanned backup material.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 4 | 3:25 | Shorten citation narration, not the statement of contribution. |
| End of Slide 7 | 7:50 | Use the short form for Slide 8; preserve the dedicated near-independence slide. |
| End of Slide 9 | 10:40 | If past 11:30, use short forms of Slides 10–12 and 14–15. |
| End of Slide 13 | 15:45 | If past 17:00, shorten the application and limitations. Protect the conclusion. |
| End of Slide 15 | 18:00 | Begin the conclusion immediately. Do not open backups. |

### Prepared reductions

| Slide | Planned | Short form | What to retain |
| --- | --- | --- | --- |
| 4 | 0:55 | 0:40 | Existing MI variance, moment matching, the MI-specific calculation. |
| 6 | 2:00 | 1:40 | The two levels of variance, component formula and approximate status. |
| 8 | 1:20 | 1:05 | Meaning of one and the opposite population/sample prediction errors. |
| 10 | 1:20 | 1:05 | One sentence per table row and the fixed 5% target. |
| 11 | 1:10 | 0:55 | Same MI null, 36.38%/34.38%, complete validity at the highlighted point. |
| 12 | 1:05 | 0:50 | Power definition, gap colours, fixed nominal rules and method ordering. |
| 14 | 1:15 | 1:00 | Higher returning-visitor estimate, adjusted rejection, unknown population truth. |
| 15 | 1:00 | 0:45 | Limits linked to specific next steps. |

Using all these reductions gives **16:45**. They are a controlled shorter
route, not permission to speak faster or remove the original contribution.
Slides 9 and 13 remain substantial because they carry the key explanation.

### If Slide 13 ends as late as 18:00

Use these brief scripts and still finish before the interruption:

- **Slide 14, about 30 seconds:** “In the shopping application, returning
  visitors have higher estimated month–purchase MI. Both tests reject
  equality after adjustment across six comparisons. The population values
  are unknown, so this illustrates interpretation without validating
  false-positive accuracy.”
- **Slide 15, about 25 seconds:** “The main limits are the first-order
  approximation, errors in the shared estimates, and one controlled
  population family. The next steps are to improve those estimates,
  retain the extra sampling variation near independence, and evaluate
  broader populations.”
- **Slide 16, about 40 seconds:** “I derived MI-specific variance
  sensitivity and used it to calculate degrees of freedom. The larger
  cutoff improves some excessive false-positive rates, while also reducing
  power. The remaining failures identify estimation accuracy as a priority
  in sparse settings. Thank you.”

Do not cut the conclusion or attempt to narrate the backup slides before
questions. Avoid a promise to cover an omitted result later in the talk.

## 10. Execution and acceptance requirements

### Scientific checks before authoring

- Confirm the final thesis hash and read the currently included results.
  Use the final PDF rather than the old presentation or the last git
  commit alone, because the final rebuild contains subsequently approved
  source changes.
- Apply the filters in the evidence manifest before plotting. Assert row
  counts, sample-size order, denominator and repetition count.
- Preserve the literal study label `null` when loading `displays.csv`.
  For pandas, use `pd.read_csv(path, keep_default_na=False)` for that file;
  the default parser treats `null` as a missing value and would silently
  remove the rows needed for Slide 8. Read numeric result files normally.
- Keep component df separate from combined test df and the moment target
  separate from a proven sampling distribution.
- Distinguish V, V-hat, V-hat/n, and Var(V-hat). The right graph on Slide 8
  concerns Var(V-hat), not the sampling variance of the MI estimator.
- Label MI, MI differences and standard errors in nats. Label rejection
  and power in percent. Do not rescale the df or count sample repetitions
  as observations available to one test.
- Do not mix MI=0.005 values with MI=0.02 table examples. Keep the
  9,659/9,662 directional denominator exact.
- For the application, label corrected estimates and adjusted p-values
  correctly. Do not create or imply multiplicity-adjusted confidence
  intervals from the unadjusted intervals in the CSV.
- Match all literature references to the thesis bibliography. Preserve
  the original spelling in titles, authors and dataset identifiers.

### Authoring order

1. Inspect the supplied PDF and PowerPoint together. Work on a separate
   copy, reuse the cover artwork and relevant layout objects, and set the
   Lato content styles and explicit orange/navy colours. Build the common
   master and Slide 16 first, fixing the intended ending. Do not inherit
   the earlier proposal's wording, data or animation timings.
2. Build Slides 5–6 to establish readable equations and the variance
   distinction. If they cannot be explained at the specified size, simplify
   the main slide and retain the exact formula in B1–B2.
3. Prepare the filtered data and charts for Slides 8–14. Validate their
   data before styling them. Store copies of the selected rows and chart
   code in the separate presentation assets directory.
4. Build Slides 1–4 and 7 around the knowledge those results require.
5. Build Slide 15 and the backup slides. Add source references and the
   scripts to speaker notes, keeping execution instructions out of notes
   intended for Daniel to rehearse.
6. Review the complete sequence and rehearse to the timing table. Inspect
   the PowerPoint rendering and the exported PDF at readable size.

### Proposed final outputs for the executing agent

- `presentation/Daniel_Zhao_Welch_MI_Presentation.pptx`: editable text,
  equations and tables, 16 main slides plus 12 backups, complete notes.
- `presentation/Daniel_Zhao_Welch_MI_Presentation.pdf`: the same 28 slides,
  including the backup references, suitable for the university PDF upload.
- `presentation/Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md`: the
  final spoken script, timings and short-route cues, synchronised with the
  authored deck after rehearsal changes.
- `presentation/assets/`: source extracts, plots and authoring materials.
  Internal filenames and hashes do not appear on projected slides.

These are future execution deliverables. This planning task creates only
this handoff plan and its evidence manifest. Do not overwrite the existing
presentation PDF or any thesis delivery file. No git commit or push is
requested by the planning task.

### Final review before delivery

Confirm that the main talk covers all six content areas in the rubric,
that no obsolete calibrated-power or four-cell material has returned,
and that every main slide has one identifiable purpose. Inspect every
slide for clipped text, oversized equations, unreadable axes, overlapping
labels, misleading crops and altered colour meanings. Keep source notes
legible and the main point visually dominant.

Compare the new cover with source Slide 1 and the body pages with source
Slides 3, 4, 7, 8 and 9 side by side. Check the curved cover composition,
Lato headings, orange emphasis, navy headers, pale fills and spacing. The
body should read as the same visual family, while the charts remain large
and scientifically faithful. Confirm that no old project title, 45-setting
grid, milestone plan or proposal notes remain. A theme import alone is
insufficient because much of the source styling lives on individual
objects. Check that native text and equations remain editable.

Check that the final PDF is complete without animations and that the
PowerPoint and PDF agree. Put the actual supplied presentation date and
any required Canvas identification/disclosure into the final master only
when those details are known. Preserve accurate source acknowledgements.
Do not invent a university requirement, talk date or declaration of AI use.

### Content deliberately left out of the timed talk

The full product-rule algebra, scaled-chi-squared derivation, every
parameter value, numerical tolerance and every grid panel are available
in the thesis or relevant backup. Ordinary sample-size Welch, empirical
bootstrap comparisons and an independence-specific replacement test were
not evaluated in the final thesis and must not be presented as results.
The discarded fitted-threshold power study and four-cell construction
comparison are excluded entirely from this new deck.

The choice to emphasise selected figures is a communication decision for
20 minutes. State their settings and retain the balanced design description
so the audience can distinguish an illustration from a universal claim.

### Planning checks completed on 4 November 2026

The 19 source-file hashes were verified, including the final thesis and
the three university documents. The selected chart row counts, highlighted
rates, application outputs and directional rejection counts were checked
against the saved CSVs. Both primary simulation grids contain 360 settings
with 100,000 repetitions each, and the Expanded Welch rejection rate never
exceeds Wald's in those saved results.

The plan contains all 16 main slides, 12 backups and 22 question responses.
The timing allocations total 18:50, and the specified shorter route totals
16:45. Reference keys and Australian spelling were checked. The evidence
manifest records the numerical checks and approximate speech word counts.
The subsequent style revision inspected all 11 supplied PDF pages and
checked the matching PowerPoint's canvas, actual font runs, two themes,
palette, title position and cover asset. Section 4, all 16 main layouts,
backup styling and the authoring checks now follow that reference. The
scientific copy, equations, scripts, transitions, data selections and
timings were preserved. The manifest also records both style-reference
hashes.

Slide rendering and actual delivery timing remain checks for the executing
agent and Daniel once the deck has been built. No thesis, existing
presentation or delivery file was changed by this planning task.
