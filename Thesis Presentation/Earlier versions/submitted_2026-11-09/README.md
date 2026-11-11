# Thesis presentation (submitted thesis, 9 November 2026)

This version matches the submitted thesis, `FINAL SUBMISSION/Daniel_Zhao_Welch_MI_Thesis.pdf` (111 pages, last built on 8 November 2026). It starts from the review version, now in `Earlier versions/final_2026-11-08_v2/`, and keeps its design, content, and timing. The other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built.

The speaker notes are copied from the plan with no replacements. The plan in `Planning/` was updated at the same time, and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The current deck, preview PDF, speaker notes, and build assets. |
| `Planning/` | The presentation execution plan, its evidence manifest, and the style template notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/`, `final_2026-11-08/`, and `final_2026-11-08_v2/`. |

## What the submitted thesis changed

The submitted thesis adds subsections in Chapters 2–5 and the appendices, restructures the Chapter 4 derivation, renumbers some Chapter 4 equations, and applies Oxford commas. Its chapter, section, figure, and table numbers cited in the deck are unchanged, and every number on the slides still appears in it. The deck changes only where its wording or a reference differed from the thesis:

- **Complete distribution names**, as the thesis now uses:
  - Slide 3's Wald cell says “Assess the fixed cutoff from the standard normal distribution in finite samples”.
  - Slide 5 lists “Matching a scaled chi-squared distribution”.
  - The Slide 3 and Slide 4 scripts and the Slide 4 source name the standard normal and Student t distributions in full. Slide 4's script says “the Wald test” and “the Expanded Welch test”.
- **B2:** the caveat now names what an exact Student t distribution requires: a standard normal numerator independent of the variance estimates (thesis Section 4.1.1). The answer, the notes, and the matching question in the speaker-notes file use the full name of the scaled chi-squared distribution. The page range is now pp. 23–36.
- **B1 notes:** “Assumptions” replaces “Regularity assumptions” for the list of conditions.

The scripts and transitions total 1,944 words, 7 more than the review version.

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

- **Submitted thesis:** 111 pages, MD5 `bbd73bada062b1a7e4113c13211c438a`, identical to `Simulations/Thesis Writeup/Welch MI/deliverables/Daniel_Zhao_Welch_MI_Thesis_Signed.pdf`. Its contents and its figure and table lists were compared with the 8 November build the review version used, and every reference on B14–B15 appears in its bibliography.
- **Numbers:** every number on the slides and in the notes that appeared in the earlier thesis also appears in the submitted one.
- **Comparison with the review version:** text and notes were compared slide by slide. Only the changes above differ.
- **Validation:** the file passed OOXML validation. Every chart keeps its native aspect ratio.
- **Rendering:** Slides 3, 5, B1, and B2 were rendered and inspected; no other slide's layout changed.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
