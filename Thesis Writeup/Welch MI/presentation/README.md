# Thesis presentation

Built on 5 November 2026 from `notes/PRESENTATION_EXECUTION_PLAN_2026-11-04.md`, its evidence manifest and the vF2 style reference. Copies of the plan and manifest used are in `assets/plan_snapshot/`.

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 16 main slides and 12 backups, with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, cues, backup answers, question preparation and the rehearsal plan. |
| `assets/charts/` | Chart images (PNG at 300 dpi, plus SVG), each drawn at its size on the slide. |
| `assets/data/` | The filtered rows behind every chart and table. |
| `assets/code/` | `extract_data.py` (filters and manifest checks), `charts.py`, `build_deck.py`, `pptlib.py`, `eqrender.py`, `gen_notes.py`. |
| `assets/style_reference/` | Copies of `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf`. The originals in `INFO5993/A4/` are unchanged. |

## Before submitting

1. Open the .pptx in PowerPoint on the Mac. Check the equations on Slides 3, 5 and 6 and Backups B1–B5, and the cover title, which uses Aptos Display.
2. Export the submission PDF from PowerPoint as `Daniel_Zhao_Welch_MI_Presentation.pdf`.

The preview PDF shows each equation through its fallback image, drawn in a similar maths font, because the preview renderer cannot read Office equations. PowerPoint shows the native, editable equations instead. The preview also substitutes a different font for Aptos on the cover.

## Build choices beyond the plan

- **Slide 14:** the bars use orange for new visitors (P) and navy for returning visitors (Q), matching Slide 2.
- **Slide 12:** "usual 0.05 p-value threshold for both methods" sits in the setting line, which leaves the chart more height.
- **Slides 11–13:** the method key sits inside the plot, and the colour key sits in the row above it.
- **Backups:** each carries a small orange "Backup B1"–"Backup B12" label, top right.
- **Citations:** B10 cites the Adult (Becker and Kohavi, 1996) and Student Performance (Cortez, 2008) datasets from the thesis bibliography.

## Checks run

- All 17 source hashes matched the manifest.
- Every manifest filter, row count and numerical anchor passed.
- Expanded Welch is at or below Wald in all 720 settings.
- The 16 scripts and transitions match the plan word for word.
- The file passed OOXML validation.
- All 28 slides were rendered and inspected.

## Rebuild

Run from the folder that holds `assets/code`, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts
```

`charts.py` reads `assets/data/` and writes `assets/charts/`; `build_deck.py` needs `pandoc`.
