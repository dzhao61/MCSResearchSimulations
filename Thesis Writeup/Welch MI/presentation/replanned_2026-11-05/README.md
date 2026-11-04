# Thesis presentation (replanned 5 November 2026)

Built on 5 November 2026 from the replanned `notes/PRESENTATION_EXECUTION_PLAN_2026-11-04.md`, version 2 of its evidence manifest, the preferred reference `Example Thesis/Comparing MI in Finite Samples.pdf` and the vF2 design donor. Copies of the plan and manifest used are in `assets/plan_snapshot/`. The earlier 16-slide deck in `presentation/` is unchanged.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 14 main slides and 14 backups (Slides 15–28), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 28-page preview rendered outside PowerPoint. Use it for checking only. |
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

## Build choices beyond the plan

- **Setting lines:** each results slide has an orange setting line under the lead, written as on the preferred reference (for example "Uniform 4×4 · n = 20 per population · equal MI in P and Q").
- **Slide 11:** the denominator footnote sits under the power definition, so the footer stays one line.
- **Slide 12:** the true and mean estimated differences sit on two aligned rows, with the 9.66% rejection rate and the direction statement directly beneath.
- **Backups:** each carries a small orange "Backup B1"–"Backup B14" label at top right. The colour key for the grid backups is in each figure's legend and in the notes for opening that slide.
- **Citations:** B12 cites the Adult (Becker and Kohavi, 1996) and Student Performance (Cortez, 2008) datasets from the thesis bibliography.

## Checks run

- The plan file used matched the copy in `notes/` (MD5 `a20b42aae0c27f22d3a5e075473d2ee7`).
- Every version-2 manifest filter, row count and numerical anchor passed, and every number on the slides matched the filtered data.
- The scripts, transitions, delivery cues and sources for Slides 1–14, and the questions and answers for B1–B12, match the plan word for word. The scripts and transitions total 1,893 words.
- The file passed OOXML validation.
- All 28 slides were rendered and inspected against the preferred reference pages.
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
