# Thesis presentation (final, version 2, 8 November 2026)

This version applies a content review of `Earlier versions/final_2026-11-08/`. That folder and the other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built. The argument, evidence, charts' data, and timing table are the same; the changes are wording, two definitions, a scope line, and Oxford commas.

The speaker notes are now copied from the plan with no replacements. The plan in `Planning/` was updated at the same time, and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The current deck, preview PDF, speaker notes and build assets. |
| `Planning/` | The presentation execution plan, its evidence manifest and the style template notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/` and `final_2026-11-08/`. |

These were moved here on 8 November from `Simulations/Thesis Writeup/Welch MI/presentation/` and `notes/`.

## What changed

- **Slide 6 script:** the setting count is now correct. Four table sizes, ten sample sizes, and three margin regimes make 120 combinations for each MI level or gap; three levels or gaps make 360 settings. B3 now says “Each null or power study”.
- **Slide 4:** a definition under the shared statistic: “V(P): population variance of pointwise MI; V̂(P) estimates it from one sampled table.” The lead now says “Student t distribution”, as does B2.
- **Slide 5:** a simpler lead: “The estimated pointwise-MI variance changes between samples. We approximate that variation and use it to choose the degrees of freedom.”
- **Slide 7:** the callout and script now separate the two variance predictions at n = 1,000: 3% low with population inputs and 8% high with sample-based inputs, which the test uses (data: 0.970 and 1.080).
- **Slide 8:** a caption under the chart defines the sampling-moment target, and the script defines it before interpreting it. The chart is redrawn 0.4 inches shorter to make room.
- **Slide 14:**
  - Finding 3 says “Lower power under the same 5% testing rules”.
  - A scope line: “The evaluation covers one population construction and equal sample sizes, with the Wald test as the main benchmark.” The script says the same before the next steps.
  - Next step 1: “Reduce bias in the estimated MI difference and improve its standard error and degrees of freedom, including near independence.”
- **Slides 2 and 3:** Slide 2's definition ends “on average”, and its first task reads “Summarise a sample from each population in a count table”. Slide 3's lead names “a Wald test using a standard normal distribution”.
- **Oxford commas:** added to lists of three or more in slide text, speaker notes, and plan Sections 8–9, following the prose guidelines. Reference entries keep their citation format. The submitted thesis mostly omits them, so the deck and thesis now differ on this point.
- **Layout:** leads on Slides 3–6 break at sentence boundaries; Slides 4, 7, and 14 have adjusted spacing for the added text.

The scripts and transitions now total 1,937 words, 62 more than the previous version (Slides 6, 7, 8, and 14). That uses part of the 70-second margin in the 18:50 plan, so time the talk in rehearsal.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 14 main slides, an appendix title (Slide 15) and 15 backups (Slides 16–30), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 30-page preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, transitions, cues, and backup answers, then plan Sections 8 (question preparation) and 9 (rehearsal and timing control). |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. The application file keeps its version-3 name and still holds all six comparisons and the Holm columns. The deck uses only the two Online Shoppers rows. |
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
- **Backups:** each carries a small orange "Backup B1"–"Backup B15" label at top right. The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.

## Checks run

- **Plan and notes:** the deck's notes come from the updated plan with no replacements. Built from the plan as it stood before this revision, the deck's text and notes matched `final_2026-11-08/` exactly.
- **Comparison with the previous version:** text and notes were compared slide by slide. Only the changes above differ.
- **Numbers:** the 8% figure on Slide 7 matches the saved ratio at n = 1,000 (1.080 for sample-based inputs; 0.970 for population inputs). No other numbers changed.
- **Validation:** the file passed OOXML validation. Every chart keeps its native aspect ratio.
- **Rendering:** all changed slides were rendered and inspected.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
