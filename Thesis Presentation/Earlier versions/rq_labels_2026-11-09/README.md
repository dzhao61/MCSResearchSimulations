# Thesis presentation (research-question labels, 9 November 2026)

This version labels each results slide with the research question it answers. It starts from the submitted-thesis version, now in `Earlier versions/submitted_2026-11-09/`, and keeps its content, design, speaker notes, and timing. The other earlier versions are unchanged apart from their location; their READMEs still give the paths they had when built.

The plan in `Planning/` was updated at the same time (Sections 1, 5, 6, and 11), and a copy is in `assets/plan_snapshot/`.

## Folder layout

| Folder | Contents |
| --- | --- |
| This folder | The current deck, preview PDF, speaker notes, and build assets. |
| `Planning/` | The presentation execution plan, its evidence manifest, and the style template notes. |
| `Earlier versions/` | `original_16_slide/`, `replanned_2026-11-05/`, `replanned_2026-11-05_v2/`, `replanned_2026-11-05_v3/`, `final_2026-11-08/`, `final_2026-11-08_v2/`, and `submitted_2026-11-09/`. |

## What changed

The six results titles now begin with the research question they answer. The labels match the RQ boxes on Slide 6 and thesis Sections 6.1–6.3, which the slide footers already cite.

| Slide | Previous title | New title | Thesis section |
| --- | --- | --- | --- |
| 7 | Results: approximation accuracy | RQ1 results: approximation accuracy | 6.1.1–6.1.2 |
| 8 | Results: near independence | RQ1 results: near independence | 6.1.3 |
| 9 | Results: false positives across shared MI values | RQ2 results: false positives across shared MI values | 6.2.1 |
| 10 | Results: why bias changes rejection | RQ2 results: why bias changes rejection | 6.2.4 |
| 11 | Results: power across MI differences | RQ3 results: power across MI differences | 6.3.1 |
| 12 | Results: bias can reverse the estimated direction | RQ3 results: bias can reverse the estimated direction | 6.3.3 |

Slide 13 keeps “Illustration: online shopping data”, because the application (thesis Section 6.4) answers none of the three questions. The backups keep their titles. In the speaker notes, only the six slide headings changed.

Slide 6’s RQ3 box now writes the fixed MI as “𝐼(𝑃) = 0.02”, replacing “P MI 0.02”.

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

- **Comparison with the submitted-thesis version:** slide text, shape positions, and speaker notes were compared slide by slide. Only the six titles and Slide 6’s RQ3 line differ.
- **Fit:** Slides 6–12 were rendered. Each title fits on one line; the longest (Slide 12) uses about two-thirds of the title width.
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
