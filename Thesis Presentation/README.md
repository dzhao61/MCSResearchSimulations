# Thesis presentation (whole-grid results, 9 November 2026)

This version answers RQ2 and RQ3 across the whole simulation grid instead of single settings, and Slide 10 explains the three RQ2 patterns with all three illustrative settings of thesis Table 6.1. It starts from the application-removed version, now in `Earlier versions/app_removed_2026-11-09/`, and keeps its design, timing, and the rest of its content. The other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built.

The plan in `Planning/` was updated at the same time (Sections 1, 3–6, 8–11), and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The current deck, preview PDF, speaker notes, and build assets. |
| `Planning/` | The presentation execution plan, its evidence manifest, and the style template notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/`, `final_2026-11-08/`, `final_2026-11-08_v2/`, `submitted_2026-11-09/`, `rq_labels_2026-11-09/`, and `app_removed_2026-11-09/`. |

## What changed

- **Slide 9, “RQ2 results: false positives across all null settings”:** a scatter of all 360 null settings, Wald rate against Expanded Welch rate. Where Wald is above 5% (178 settings), Expanded Welch is closer to 5% in 165; where Wald is below 5% (180), it is further away in 176 and unchanged in four. Within a descriptive 4–6% band, 130 versus 136 settings. The thesis examples (8.35% to 4.90%; 36.38% to 34.38%) are circled.
- **Slide 11, “RQ3 results: the power cost of the larger cutoff”:** power lost by Expanded Welch across all 360 power settings, by sample size (median and range). Expanded Welch never has more power; the loss is about 6 points at n = 10, about 1 point from n = 50 to 1,000, and under 0.32 points at n = 10,000.
- **Slide 12:** a heat map of the share of Expanded Welch rejections pointing the wrong way, across every table size and sample size under different-skew margins (0.01 gap), with the thesis example (16×16, n = 1,000) outlined. At least 90% of rejections point the wrong way in 28 of the 360 power settings, all different-skew.
- **Slide 10, “RQ2 results: why the cutoff helps, hurts, or cannot fix it”:** restores the uniform 4×4, n = 20 row of thesis Table 6.1, so its three rows (standard error too small, standard error too big, bias) explain the three patterns on Slide 9. Three mechanism panels replace the two, and the settings are labelled as illustrative.
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
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 13 main slides, an appendix title (Slide 14) and 16 backups (Slides 15–30: B1–B14, with two B1 continuation slides after B1), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 30-page preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, transitions, cues, and backup answers, then plan Sections 8 (question preparation) and 9 (rehearsal and timing control). |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. The application file is kept for reference; the deck no longer uses it. |
| `assets/code/` | `extract_data.py` (filters and manifest checks), `charts.py`, `build_deck.py`, `plan_notes.py` (reads the notes from the plan), `pptlib.py`, `eqrender.py`, `gen_notes.py`. |
| `assets/plan_snapshot/` | The plan and manifest as used for this build. |
| `assets/style_reference/` | Copies of `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf`. The originals are unchanged. |

## Before submitting

1. Open the .pptx in PowerPoint on the Mac. Check the following, including the inline hatted symbols on Slides 4, 6, 7, and 8, B4, and B5:
   - the equations on Slides 2, 4 and 5 and Backups B1, both B1 continuation slides, B2, B3, and B5;
   - the inline "n − 1" on B9;
   - the cover title, which uses Aptos Display.
2. Export the upload PDF from PowerPoint as `Daniel_Zhao_Welch_MI_Presentation.pdf`, the name the plan gives it.

The preview shows each equation through its fallback image, because the preview renderer cannot read Office equations. It also substitutes other fonts for Aptos on the cover and for Cambria Math in the short inline symbols. PowerPoint shows the native equations and fonts.

## Other build choices

- **Setting lines:** each results slide has an orange setting line under the lead, written as on the preferred reference (for example "Uniform 4×4 · n = 20 per population · equal MI in P and Q").
- **Slide 11:** the denominator footnote sits under the power definition, so the footer stays one line.
- **Slide 12:** the true and mean estimated differences sit on two aligned rows, with the 9.66% rejection rate and the direction statement directly beneath.
- **Appendix title:** the word "Appendix" in 48 pt bold navy Lato, centred, with the slide number. Its notes carry the plan's delivery line.
- **Backups:** each carries a small orange "Backup B1"–"Backup B14" label at top right; the two cell-probability slides are labelled "Backup B1, continued" and "Backup B1, worked example". The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.

## Checks run

- **Comparison with the application-removed version:** slide text, shape positions, images, and speaker notes were compared slide by slide. Only Slides 2, 6, 9–13, B3–B5, and B6’s notes differ.
- **Tallies:** every count was recomputed from the saved rates, and Slide 10’s three rows were checked against thesis Table 6.1 and the null diagnostics; the circled and outlined examples were checked against the thesis values (8.35%, 4.90%, 36.38%, 34.38%, 9.66%, and 9,659 of 9,662 positive rejections). The signed counts add up to the saved rejection counts for all 360 power settings.
- **Rendering:** all 30 slides were rendered and inspected.
- **Worked example:** g, tau-squared, and the component degrees of freedom for N^P were recomputed from the counts and match thesis Section 4.4.1 (0.4218, 0.93212, and 16.65). The thesis prints only cell (1, 1)’s sensitivity; the other eight on Slide 17 come from thesis Equation 4.41.
- **Validation:** the file passed OOXML validation.
- **Science source:** unchanged. The submitted thesis is 111 pages, MD5 `bbd73bada062b1a7e4113c13211c438a`.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
