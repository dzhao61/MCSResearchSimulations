# Thesis presentation (final, 14 November 2026)

**Status: final.** `Daniel_Zhao_Welch_MI_Presentation_Final.pptx` is the version to present: 13 main slides and 20 appendix slides (33 in all), with speaker notes. `Daniel_Zhao_Welch_MI_Presentation_Final.pdf` matches it page for page. The change log below records every edit since the whole-grid version of 9 November.

**For Canvas:** the [Submission folder](Submission/) contains the three upload PDFs. For the live talk, open the PowerPoint deck and use the [spoken script](Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md).

**Before presenting:** install Lato on the presenting computer, or PowerPoint will substitute another font. Keep the final PDF as a backup; it shows every slide, with equations as images.

## Whole-grid results (9 November 2026)

This version answers RQ2 and RQ3 across the whole simulation grid instead of single settings, and Slide 10 explains the three RQ2 patterns with all three illustrative settings of thesis Table 6.1. It starts from the application-removed version, now in `Earlier versions/app_removed_2026-11-09/`, and keeps its design, timing, and the rest of its content. The other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built.

The plan in `Planning/` was updated at the same time (Sections 1, 3–6, 8–11), and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The final PowerPoint deck for the live presentation and this README. |
| `Submission/` | The three PDFs for Canvas: slides, signed consent declaration, and AI acknowledgement. |
| `Rehearsal/` | The current spoken script for the live talk. |
| `assets/` | Charts, data, build scripts, and reference material. |
| `Planning/` | The presentation execution plan, evidence manifest, style notes, and expanded speaker notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/`, `final_2026-11-08/`, `final_2026-11-08_v2/`, `submitted_2026-11-09/`, `rq_labels_2026-11-09/`, and `app_removed_2026-11-09/`. |

## What changed

- **Speaker notes from the spoken script (14 November):** the PowerPoint notes for Slides 1–13 are now the spoken script from `Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md`, word for word, and nothing else: no timings, delivery cues, sources, or backup index. Slide 14's notes are the script's question-and-answer guides. The backup notes (Slides 15–33) are unchanged. The slides themselves are unchanged, and `Submission/Daniel_Zhao_Welch_MI_Presentation_Final.pdf` still matches them page for page. `Planning/Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` is regenerated from the updated deck.
- **Slide 9, “RQ2 results: false positives across all null settings”:** a scatter of all 360 null settings, Wald rate against Expanded Welch rate. Where Wald is above 5% (178 settings), Expanded Welch is closer to 5% in 165; where Wald is below 5% (180), it is further away in 176 and unchanged in four. Within a descriptive 4–6% band, 130 versus 136 settings. The thesis examples (8.35% to 4.90%; 36.38% to 34.38%) are circled.
- **Slide 11, “RQ3 results: the power cost of the larger cutoff”:** power lost by Expanded Welch across all 360 power settings, by sample size (median and range). Expanded Welch never has more power; the loss is about 6 points at n = 10, about 1 point from n = 50 to 1,000, and under 0.32 points at n = 10,000.
- **Slide 12:** a heat map of the share of Expanded Welch rejections pointing the wrong way, across every table size and sample size under different-skew margins (0.01 gap), with the thesis example (16×16, n = 1,000) outlined. At least 90% of rejections point the wrong way in 28 of the 360 power settings, all different-skew.
- **Slide 10, “RQ2 results: why the cutoff helps, hurts, or cannot fix it”:** restores the uniform 4×4, n = 20 row of thesis Table 6.1, so its three rows (standard error too small, standard error too big, bias) explain the three patterns on Slide 9. Three mechanism panels replace the two, and the settings are labelled as illustrative.
- **Slides 2 and 6 restored (14 November):** Slide 2's task steps are orange again (two outlines, filled final step); Slide 6's RQ markers are one colour, orange to match their panel.
- **Boxes by position; Slide 9 quadrants (14 November):** every set of boxes runs orange, navy, green (Slides 2, 4, 6, 7, 8, 12, 13 and 18; Slide 8's panels and Slide 18's cards are reordered to keep chart colours consistent). Slide 4's Expanded Welch curve is green to match its box. Slide 9's chart labels all four quadrants, with an enlarged inset for the crowded 0–6% corner.
- **Three-colour consistency (14 November):** orange primary, navy secondary, green third, with no colour marking two things on one slide. Slides 7 and 8 colour the mean and the target green; Slide 10 and 28 headers are neutral; Slide 18's df cards match Slide 8; Slides 23 and 25–31 use the deck colours instead of off-palette ones. Speaker notes: Slide 8's “charcoal” target is now “green”.
- **Slide 9 linear chart (14 November):** the null scatter now uses linear axes from 0% to 40%, so it shows every setting, including the 36.38% to 34.38% bias example, without log scales.
- **Backup spacing (14 November):** Slides 19, 22 and 24 now use the full slide. Slide 22 labels its equation “Copying construction” and uses larger text; Slide 24 has a larger equation and table.
- **Design pass (14 November):** layout only, no wording changes. Even gaps and padding in the right-hand columns of Slides 7–9, 11 and 12, and on Slide 15's cards; no single words left on a line (Slides 6, 7, 17 and 22); no ranges or DOIs split across lines (Slides 11, 32 and 33); Slide 20's note clears the footer.
- **Slide 5 contribution tags centred (14 November):** the two contribution tags now span the text column, so they sit centred in their panels and line up with the text.
- **Slide 12 higher-order bias (14 November):** the peach panel is now “Higher-order bias outweighs the gap”, as three bullets: the leading term (0.11 nats each) cancels with equal n; the higher-order bias differs between P’s and Q’s margins, shifting the difference by +0.031 nats (3× the 0.01 gap); the fix is more data, not a larger cutoff. The callout below it now says that 28 of the 360 power settings have at least 90% of rejections pointing the wrong way, all 8×8 or 16×16 with different-skew margins.
- **Slide 8 chart (14 November):** degrees of freedom are now on a linear axis (MI stays logarithmic), so the estimate visibly sits at about half the target and the population-based value near zero. A key gives each line's formula: target ν_P,mom = 2[E(V̂)]²/Var(V̂), population-based first order ν_P,FO = 2nV²/τ², and mean sample-based estimate ν̂_P = 2nV̂²/τ̂². The bracket reads “estimate 4.9 vs target 9.1”.
- **Formatting pass and chart keys (14 November):** every line in every chart now has a label or key. Slide 7’s plots are headed “Mean check: E(V-hat) ÷ V” and “Variance check: tau-squared/n ÷ Var(V-hat)”, as in thesis Figure 6.1; the bottom lines read “true tau-squared (population-based)” and “mean estimated tau-hat-squared (sample-based)”, and both plots mark “1 = exact”. Slide 23’s rows use the same labels. Slide 8’s lines carry their symbols, and Slide 4’s plot has a line key and a label for the shaded rejection region. The null grids (Slides 25–27) key the dotted 5% line. Alignment fixes on Slides 2, 4, 5, 16–18, 20 and 22; Slide 32’s references are now alphabetical. Speaker notes are unchanged.
- **Appendix reorganised, with three derivation slides (13 November):** the backups now follow the order of the talk: Method (Slides 15–21, supporting Slides 4–5), Evaluation design (Slide 22, for Slide 6), RQ1 (Slides 23–24), RQ2 (Slides 25–28), RQ3 (Slides 29–31), and References (Slides 32–33). B numbers are gone: every pointer uses the slide number you type to jump, and each backup has a top-right breadcrumb such as “Appendix · Method · for Slide 5, step 2”. Slides 16–18 are new and derive Slide 5’s three equations step by step, with thesis equation numbers: Derivation 1, Var{V-hat(P)} ≈ tau-squared(P)/n_P (navy, matching step 2); Derivation 2, moment matching and the df rule; and Derivation 3, the estimated and combined degrees of freedom (both green, matching step 3). The old “Moment matching and combined degrees of freedom” backup is absorbed into Derivations 2 and 3. The exact derivative, the cell-probability grid, and the worked example now follow the derivations (Slides 19–21). Slide 14’s index, Slide 13’s notes index, the source lines on Slides 3–11, the speaker notes, and the plan all use the new numbers. Earlier entries below keep the B numbers of their time.
- **Slide 5 redesign (13 November):** Slide 5 now shows three steps in the order of its script: V-hat(P) varies between samples (a schematic, not data), measuring that variation, and turning it into degrees of freedom. Each step has its own colour, as on Slide 10: orange, navy, and green. Steps 2 and 3 carry Contribution 1 and 2 tags and name the approximation each step makes; a strip below covers combining P and Q. The script and timing are unchanged. It was reviewed as a draft on Slide 32, which is now removed.
- **Bias-correction backup (13 November):** a new B4, “Bias correction” (Slide 20, in the Method group), shows the plug-in estimate, its leading bias (Miller, 1955), and the bias-corrected difference (thesis Equations 2.7–2.9 and 3.7). Three cards give the size of the leading term, why it cancels in these equal-sample simulations, and the higher-order bias that remains. Slides 4 and 10 point to it. The former B4–B14 are now B5–B15 on Slides 21–31; the slide labels, footers, Slide 14’s index, Slide 13’s notes index, and the speaker notes match. The references add Miller (1955), Panzeri and Treves (1996), Chao and Shen (2003), and Nemenman et al. (2002). Earlier entries below keep the B numbers of their time.
- **Slide 10 colours (13 November):** the three mechanisms now have three colours (orange, navy, green), on both the table markers and the panels below.
- **Hats in the preview (13 November):** inline hatted symbols (V̂, V̂(P), Î(P), p̂, Δ̂) now sit centred in the preview PDF and other viewers that cannot show PowerPoint's own equations. PowerPoint itself is unchanged.
- **Supervisor feedback on Slide 2 (13 November):** Slide 2 now shows each population as n observed pairs (X, Y), says in the heading and in one line below the diagram that the two variables are discrete (categorical), and gives a one-sentence illustrative example (mid-semester and final exam grades, before and after generative AI). The example is not thesis data.
- **Review fixes (12 November):** Slide 10's rows and explanation panels have matching numbered markers. Slide 14 shows the backup index with slide numbers. The captions on Slides 9 and 12 no longer leave a word alone, and Slide 12's caption sits clear of the axis label. Slide 3's strip names all three contributions, matching Slide 13, and Slide 5 is titled “Approach and contributions”.
- **Conclusion slide (11 November):** Slide 13 now separates contributions from findings. “Contributions” shows the thesis's three contributions (derivation, test construction, and empirical evaluation) as the highlight, in stronger peach cards with large orange numerals. “Findings by research question” gives one pale-blue card each for RQ1–RQ3, with navy RQ tags. The next steps are now two arrow items. The script names the three contributions, then gives one finding per research question.
- **Cell-probability backups (11 November):** two new backups follow B1. “Backup B1, continued” (Slide 16) is a grid that gives each quantity as an expectation, variance, or derivative beside its sum over cell probabilities: pointwise MI, MI, V, the row and column means of pointwise MI, g, tau-squared, and the component degrees of freedom. “Backup B1, worked example” (Slide 17) works through thesis Section 4.4.1 (table N^P): cell (1, 1) step by step, the sensitivities of all nine cells, tau-squared 0.932, and 16.65 component degrees of freedom. Slide 5’s source line points to Slides 16–17. B2–B14 move to Slides 18–30; their B numbers are unchanged, and Slide 13’s backup index is updated.
- **Hats (11 November):** inline hatted symbols (𝑉̂, 𝐼̂, 𝜈̂, and Δ̂BC) are now native PowerPoint equations instead of a letter plus a combining hat, so PowerPoint places each hat correctly. The preview PDF still shows them as plain text.
- **Review corrections (10 November):** Slide 9 now says Expanded Welch is further below 5% in 176 of the 180 conservative settings and unchanged in four, and labels the 130 versus 136 count as a descriptive 4–6% band. Slide 12’s chart note says percentages are rounded and that 50% means half the rejections have the wrong sign. Slide 13 says “At the same nominal 5% threshold, power is no higher”. Slide 8 labels the orange line “mean sample-based estimate”. Slide 11’s second panel reads “Small MI gaps can stay hard to detect”. Scripts and cues match.
- **Slide 2 (10 November):** the hypothesis box now shows both hypotheses from thesis Equation 1.1, H₀: I(P) = I(Q) against H₁: I(P) ≠ I(Q), and the script mentions the two-sided alternative.
- **Formatting pass:** Slide 6’s grid panel now states “360 settings per study”, its research questions are evenly spaced, and its model line is reworded. Slide 13’s findings now match Slides 9–12. Slide 9’s y-axis says “(log scale)”. B3, B4, and B5 use the same labels as Slides 6–8 (I(P) and I(Q); “population-based inputs”; “target” and “sample-based estimate”).
- **Notes:** the scripts, cues, and sources for Slides 9–12 are rewritten to match, as are the shorter-route rows. B6’s notes now say how Slide 9 uses its settings. All timings are unchanged.
- **Data:** `assets/data/slide12_wrong_direction_all.csv` adds the signed rejection counts for all 360 power settings, from the MI-gap power diagnostics; `extract_data.py` writes it.

The counts on Slides 9, 11, and 12 are tallies of the thesis simulation results behind Figures 6.4–6.9. The thesis states the same conclusions in words but does not print these counts.

- **Speaker-script revision (10 November):** clarified why the Student t distribution is used, defined g and tau-squared before the df calculation, explained copying in words, introduced Slide 8’s target first, reduced spoken numerical detail, made difference-bias cancellation explicit, and ended with the scientific takeaway. The plan, plan snapshot, embedded notes, and rehearsal Markdown are synchronised; the visible slides are unchanged. B10’s question now refers to absolute power behind the whole-grid loss summary.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation_Final.pptx` | The deck: 13 main slides, an appendix title and index (Slide 14) and 19 backups (Slides 15–33, in the order of the talk), with editable text, tables and native equations, and full speaker notes. |
| `Submission/Daniel_Zhao_Welch_MI_Presentation_Final.pdf` | The 33-page slide PDF for Canvas and a backup for the live talk. |
| `Submission/Declaration-presentation signed.pdf` | Signed and dated consent declaration for sharing the presentation slides. |
| `Submission/AI_Acknowledgement.pdf` | Completed AI acknowledgement for this presentation. The editable Word source is outside the upload folder. |
| `Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md` | The current trimmed script and Q&A prompts. |
| `Planning/Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | The deck's speaker notes as one file: the spoken script for Slides 1–13, the question guides, and the backup answers. |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. The application file is kept for reference; the deck no longer uses it. |
| `assets/code/` | `extract_data.py` (filters and manifest checks), `charts.py`, `build_deck.py`, `plan_notes.py` (reads the notes from the plan), `pptlib.py`, `eqrender.py`, `gen_notes.py`. |
| `assets/plan_snapshot/` | The plan and manifest as used for this build. |
| `assets/style_reference/` | Copies of `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf`. The originals are unchanged. |

## Before submitting

1. Open the .pptx in PowerPoint on the Mac. Check the following, including the inline hatted symbols on Slides 4–8, 15–18, 21, 23, and 24:
   - the equations on Slides 2, 4 and 5 (including the df rule in words), the derivations on Slides 16–18, and Slides 15 and 19–24;
   - the inline "n − 1" on Slides 17 and 28;
   - the cover title, which uses Aptos Display.
2. Upload the three PDFs in [Submission/](Submission/) using the presentation assignment in Canvas. If you edit the deck or acknowledgement after organising the files, refresh the corresponding upload PDF.

The preview shows each equation through its fallback image, because the preview renderer cannot read Office equations. It also substitutes other fonts for Aptos on the cover and for Cambria Math in the short inline symbols. PowerPoint shows the native equations and fonts.

## Other build choices

- **Setting lines:** each results slide has an orange setting line under the lead, written as on the preferred reference (for example "Uniform 4×4 · n = 20 per population · equal MI in P and Q").
- **Slide 11:** the denominator footnote sits under the power definition, so the footer stays one line.
- **Slide 12:** the true and mean estimated differences sit on two aligned rows, with the 9.66% rejection rate and the direction statement directly beneath.
- **Appendix title:** the word "Appendix" in 48 pt bold navy Lato, centred, with the slide number. Its notes carry the plan's delivery line.
- **Backups:** each carries a small orange breadcrumb at top right naming its appendix group and the main slide it supports, for example "Appendix · RQ2 · for Slide 9". The derivation slides (16–18) are deliberately denser: numbered steps, each with the step in words, the equation, and the thesis equation number. The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.

## Checks run

- **Comparison with the application-removed version:** slide text, shape positions, images, and speaker notes were compared slide by slide. Only Slides 2, 6, 9–13, B3–B5, and B6’s notes differ.
- **Tallies:** every count was recomputed from the saved rates, and Slide 10’s three rows were checked against thesis Table 6.1 and the null diagnostics; the circled and outlined examples were checked against the thesis values (8.35%, 4.90%, 36.38%, 34.38%, 9.66%, and 9,659 of 9,662 positive rejections). The signed counts add up to the saved rejection counts for all 360 power settings.
- **Comparison for the bias-correction backup (13 November):** apart from the new Slide 20, only the source lines on Slides 3, 4 and 7–11, Slide 14’s index, Slide 13’s notes index, the backup labels and slide numbers, and the two references slides differ from the previous build.
- **Comparison for the formatting pass (14 November):** speaker notes are identical to the previous build. Slide text changed only on Slides 7, 8, 17, 22 and 23; positions changed on Slides 2, 4, 5, 8, 16–18, 20, 22 and 23; charts were redrawn on Slides 4, 7, 8, 23 and 25–27, and fallback equation images on Slides 15–18, 20 and 21. Every fallback equation image now holds its equation.
- **Comparison for the appendix reorganisation (13 November):** every moved backup matches its previous version apart from its slide number, breadcrumb, and pointers; the exact-derivative and worked-example slides also have new titles. Main slides differ only in the source lines on Slides 3–11, Slide 14’s index, and the notes on Slides 5, 7 and 13.
- **Derivations:** each step on Slides 16–18 was checked against thesis Sections 4.1.2 and 4.3 (Equations 4.2–4.7, 4.10–4.11, 4.30–4.31, and 4.35–4.44).
- **Rendering:** all 33 slides were rendered and inspected.
- **Worked example:** g, tau-squared, and the component degrees of freedom for N^P were recomputed from the counts and match thesis Section 4.4.1 (0.4218, 0.93212, and 16.65). The thesis prints only cell (1, 1)’s sensitivity; the other eight on Slide 21 come from thesis Equation 4.41.
- **Validation:** the file passed OOXML validation.
- **Science source:** unchanged. The submitted thesis is 111 pages, MD5 `bbd73bada062b1a7e4113c13211c438a`.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation_Final.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation_Final.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Planning/Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
