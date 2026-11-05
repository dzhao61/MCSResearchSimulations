# Thesis presentation (replanned 5 November 2026, version 3)

Built on 5 November 2026 from the replanned `notes/PRESENTATION_EXECUTION_PLAN_2026-11-04.md` (revised that evening to add an appendix title slide), version 2 of its evidence manifest, the preferred reference `Example Thesis/Comparing MI in Finite Samples.pdf` and the vF2 design donor. Copies of the plan and manifest used are in `assets/plan_snapshot/`.

This folder supersedes `presentation/replanned_2026-11-05_v2/`. That folder, `presentation/replanned_2026-11-05/` and the earlier 16-slide deck in `presentation/` are unchanged.

Version 3 is a formatting pass on version 2, requested on 5 November to make the slides less crowded. It sets aside the plan's type sizes. The wording on every slide, the numbers, the charts' data and the speaker notes are identical to version 2.

## What the formatting pass changed

- **Type scale:** titles 28 pt (were 34–36), lead sentences 17 pt regular with one bold orange phrase (were 20 pt bold), panel and table text 13.5–15 pt (were 17–21), footers 10.5 pt (were 14).
- **Section headings:** the solid navy and orange header bars are now small coloured labels with a thin rule beneath.
- **Panels:** soft fills without outlines. The dashed callout boxes are now text marked by a thin coloured bar at the left.
- **Tables:** no filled header rows; headers are small bold text above a thin orange rule.
- **Charts:** labels 12–13 pt (were 17–20), thinner lines, smaller markers and lighter axes and gridlines. Each chart is redrawn at its new size on the slide.
- **Cover:** slightly smaller title, question and author details.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 14 main slides, an appendix title (Slide 15) and 14 backups (Slides 16–29), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 29-page preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, transitions, cues, backup answers, then plan sections 8 (question preparation) and 9 (rehearsal and timing control). |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. |
| `assets/code/` | `extract_data.py` (filters and manifest checks), `charts.py`, `build_deck.py`, `plan_notes.py` (reads the notes from the plan), `pptlib.py`, `eqrender.py`, `gen_notes.py`. |
| `assets/plan_snapshot/` | The plan and manifest as used for this build. |
| `assets/style_reference/` | Copies of `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf`. The originals are unchanged. |

## Before submitting

1. Open the .pptx in PowerPoint on the Mac. Check the equations on Slides 2, 4 and 5 and Backups B1–B3 and B5, and the cover title, which uses Aptos Display.
2. Export the upload PDF from PowerPoint as `Daniel_Zhao_Welch_MI_Presentation.pdf`, the name the plan gives it.

The preview shows each equation through its fallback image, because the preview renderer cannot read Office equations. It also substitutes other fonts for Aptos on the cover and for Cambria Math in the short inline symbols. PowerPoint shows the native equations and fonts.

## Other build choices

- **Setting lines:** each results slide has an orange setting line under the lead, written as on the preferred reference (for example "Uniform 4×4 · n = 20 per population · equal MI in P and Q").
- **Slide 11:** the denominator footnote sits under the power definition, so the footer stays one line.
- **Slide 12:** the true and mean estimated differences sit on two aligned rows, with the 9.66% rejection rate and the direction statement directly beneath.
- **Appendix title:** the word "Appendix" in 48 pt bold navy Lato, centred, with the slide number. Its notes carry the plan's delivery line.
- **Backups:** each carries a small orange "Backup B1"–"Backup B14" label at top right. The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.
- **Citations:** B12 cites the Adult (Becker and Kohavi, 1996) and Student Performance (Cortez, 2008) datasets from the thesis bibliography.

## Checks run

- The plan file used matched the copy in `notes/` (MD5 `d286b3a7289d8e4802a0c747154decd1`).
- Every version-2 manifest filter, row count and numerical anchor passed, and every number on the slides matched the filtered data.
- The scripts, transitions, delivery cues and sources for Slides 1–14, the appendix delivery line, and the questions and answers for B1–B12, match the plan word for word. The scripts and transitions total 1,893 words.
- The file passed OOXML validation.
- All 29 slides were rendered and inspected. Every slide's text and speaker notes match `replanned_2026-11-05_v2/` exactly.
- The authored text uses Australian spelling. "Generalization" and "generalized" appear only in published reference titles.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
