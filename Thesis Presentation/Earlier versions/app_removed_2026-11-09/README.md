# Thesis presentation (application removed, 9 November 2026)

This version removes the Online Shoppers application so the talk does less in its 20 minutes. It starts from the research-question-label version, now in `Earlier versions/rq_labels_2026-11-09/`, and keeps its design and the rest of its content. The other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built.

The plan in `Planning/` was updated at the same time (Sections 1, 3, 5–10, and 11), and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The current deck, preview PDF, speaker notes, and build assets. |
| `Planning/` | The presentation execution plan, its evidence manifest, and the style template notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/`, `final_2026-11-08/`, `final_2026-11-08_v2/`, `submitted_2026-11-09/`, and `rq_labels_2026-11-09/`. |

## What changed

- **Slide 2:** the left panel now shows two generic populations, P and Q, each with a sample size, a schematic count table, and an MI estimate (𝐼̂(𝑃) and 𝐼̂(𝑄)). It names no dataset and shows no sample sizes or estimates. The question reads “Does MI differ between the two populations?” The script drops the month, visitor, and estimate details; the cue and source change to match.
- **Slide 1:** the transition now reads “The comparison starts with two populations and a sample from each.”
- **Application slide removed.** “Illustration: online shopping data” is gone, so Conclusions is now Slide 13. Slide 12’s transition now leads to the conclusion: “The contribution and the remaining estimation problems lead to specific next steps.”
- **B13 (Application details) removed.** The appendix title is now Slide 14 and B1–B12 are Slides 15–26. The references become B13–B14 (Slides 27–28), and Sakar and Kastro (2018) is dropped from them. Slide 3’s footer now points to B13–B14.
- **Timing:** the freed 1:05 goes to Slides 5 (2:05), 8 (2:00), and 12 (2:00), so the talk still ends at 18:50. The checkpoints, shorter route, and emergency close in the speaker notes are updated.
- **Questions:** the three application questions are removed. A new one, “Did you apply the tests to real data?”, points to thesis Section 6.4.
- **Notes:** backups now say to return to Slide 13, and Slide 13’s notes carry the renumbered backup index.
- **Slide 7:** the navy curve is now labelled “population-based inputs”, parallel to “sample-based inputs”, on the chart and in the n = 1,000 callout.
- **Slide 8:** the lines are now “target (measured from 100,000 samples)” in charcoal, “sample-based estimate” in orange, and “population-based value” in dotted navy, so the colours mean the same as on Slide 7. A bracket marks “about half the target”, the y-axis says “(log scale)”, and the lead, panels, callout, and script use the same names. The footer keeps the thesis symbols.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 13 main slides, an appendix title (Slide 14) and 14 backups (Slides 15–28), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 28-page preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, transitions, cues, and backup answers, then plan Sections 8 (question preparation) and 9 (rehearsal and timing control). |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. The application file is kept for reference; the deck no longer uses it. |
| `assets/code/` | `extract_data.py` (filters and manifest checks), `charts.py`, `build_deck.py`, `plan_notes.py` (reads the notes from the plan), `pptlib.py`, `eqrender.py`, `gen_notes.py`. |
| `assets/plan_snapshot/` | The plan and manifest as used for this build. |
| `assets/style_reference/` | Copies of `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf`. The originals are unchanged. |

## Before submitting

1. Open the .pptx in PowerPoint on the Mac. Check the following:
   - the equations on Slides 2, 4 and 5 and Backups B1–B3 and B5;
   - the inline "n − 1" on B9;
   - the cover title, which uses Aptos Display.
2. Export the upload PDF from PowerPoint as `Daniel_Zhao_Welch_MI_Presentation.pdf`, the name the plan gives it.

The preview shows each equation through its fallback image, because the preview renderer cannot read Office equations. It also substitutes other fonts for Aptos on the cover and for Cambria Math in the short inline symbols. PowerPoint shows the native equations and fonts.

## Other build choices

- **Setting lines:** each results slide has an orange setting line under the lead, written as on the preferred reference (for example "Uniform 4×4 · n = 20 per population · equal MI in P and Q").
- **Slide 11:** the denominator footnote sits under the power definition, so the footer stays one line.
- **Slide 12:** the true and mean estimated differences sit on two aligned rows, with the 9.66% rejection rate and the direction statement directly beneath.
- **Appendix title:** the word "Appendix" in 48 pt bold navy Lato, centred, with the slide number. Its notes carry the plan's delivery line.
- **Backups:** each carries a small orange "Backup B1"–"Backup B14" label at top right. The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.

## Checks run

- **Comparison with the research-question-label version:** slide text, shape positions, and speaker notes were compared slide by slide, matching each slide to its new number. Only the changes listed above differ.
- **Sweep:** no slide or note mentions the shopping data, visitors, months, weekends, Sakar and Kastro, or the old slide numbers.
- **Rendering:** all 28 slides were rendered and inspected, including the new Slide 2 panel and the two-column B14.
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
