# Thesis presentation (final, 8 November 2026)

Built on 8 November 2026 to match the final thesis, `FINAL SUBMISSION/Daniel_Zhao_Welch_MI_Thesis.pdf` (identical to `deliverables/Daniel_Zhao_Welch_MI_Thesis_Signed.pdf`). It starts from version 3 and keeps its design. Copies of the plan and manifest used are in `assets/plan_snapshot/`; the plan copy is the 5 November plan with the formatting guidelines added.

This folder supersedes `presentation/replanned_2026-11-05_v3/`. That folder, `replanned_2026-11-05_v2/`, `replanned_2026-11-05/` and the earlier 16-slide deck in `presentation/` are unchanged.

## Changes to match the final thesis

- **Wald test:** "Normal Wald" is now "Wald" or "the Wald test" on the slides, charts and notes, as in thesis Section 3.3. Slide 3 cites Wald (1943) for the Wald comparison.
- **Shared MI:** "common MI" is now "shared MI" (Slide 9 title, lead and panels; B3; B4; the B6–B8 legends and notes; chart axis labels), as in the captions of thesis Figures 6.4–6.6.
- **Calculation success:** "valid" and "validity" are now "successful calculation" and "calculation success" (Slides 4, 6, 9, 10, 11 and 12, B3, the grid footers and the chart strip labels), as in thesis Appendix B.3.
- **Slide 13:** the final thesis drops the Holm adjustment and the six-comparison family. The slide now gives unadjusted two-sided p-values (month: Wald 4.71 × 10⁻⁵, Expanded Welch 3.73 × 10⁻⁴). The weekend panel now shows its p-values (0.9554 and 0.9601) to match the month panel. The lead, script and delivery cue no longer mention adjustment. Source: thesis Tables 6.3–6.4.
- **New B9, "Ordinary Welch degrees of freedom" (Slide 24):** thesis Section 6.2.5 and Table 6.2, with its own question and answer in the notes. Slide 10's footer points to it. The later backups move up by one: power grids B10–B12, application details B13, references B14–B15.
- **B13, "Application details":** this was B12, "Application details and comparison family". The six-comparison table is replaced by the two Online Shoppers comparisons from thesis Tables 6.3–6.4: corrected estimates, difference, standard error, statistic, Expanded Welch degrees of freedom and p-values.
- **B1 notes:** add the Appendix A.3 result that, with every cell positive, positive MI is equivalent to positive V.
- **References:** Wald (1943) added. Holm (1979), Becker and Kohavi (1996) and Cortez (2008) removed, matching the thesis bibliography.

## Formatting pass

- **Slide 2:** the three statistical-task boxes are slightly wider.
- **Slide 4:** the method panels read "Wald test" and "Expanded Welch test". The chart caption is slightly smaller and wider, so it stays on one line.
- **Slides 7, 8 and 12:** the bottom-right callouts fit inside their marker bars. On Slide 8 the three degrees-of-freedom values sit on separate lines, and "n × population MI" no longer splits across lines.
- **Slides 10 and 11:** the leads break at a natural point instead of leaving a word or two on the second line.
- **Slide 13:** the month and weekend panels share one layout, and their conclusion lines use matching type.
- **Slide 14:** the finding and next-step blocks break at natural points.
- **Slide 3 and B3:** Slide 3's key-work cells are set as two lines each. B3's first rate bullet breaks after "360 settings,".
- **References:** the Welch title uses a typographic apostrophe, as in the thesis.

## Speaker notes

The notes still come from the plan word for word, except where the final thesis changed the wording. `build_deck.py` lists each replacement in `NOTE_FIXES` and stops if any no longer matches the plan. The main ones:

- **Slide 3:** "The Wald test uses…" replaces "Normal Wald uses…".
- **Slides 6, 9, 10 and 12, B3 and B6–B8:** "shared MI" and "calculation success" wording.
- **Slide 13:**
  - The script reads "Both methods reject equal MI at the usual 0.05 threshold. Expanded Welch's p-value is about 0.0004."
  - The Holm clause is removed from the cue.
  - The source is updated.
- **B9 and B13:** the notes are new, written from thesis Sections 6.2.5 and 6.4, because the plan has no entry for B9 and its B12 entry describes the Holm family.

`Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` also copies plan Sections 8 and 9. `gen_notes.py` updates them in the same way (`SECTION_FIXES`):

- validity wording replaced;
- backup numbers updated (B6–B12, B13);
- the Holm question removed;
- the n − 1 question now also points to B9;
- the emergency Slide 13 line now says "at the usual 0.05 threshold".

The plan in `notes/` is unchanged. Its Sections 7–9 still use the earlier wording (Normal Wald, common MI, validity, Holm).

## Files

| File | Purpose |
| --- | --- |
| `Daniel_Zhao_Welch_MI_Presentation.pptx` | The deck: 14 main slides, an appendix title (Slide 15) and 15 backups (Slides 16–30), with editable text, tables and native equations, and full speaker notes. |
| `Daniel_Zhao_Welch_MI_Presentation_preview.pdf` | A 30-page preview rendered outside PowerPoint. Use it for checking only. |
| `Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md` | Scripts, timings, transitions, cues and backup answers, then plan Sections 8 (question preparation) and 9 (rehearsal and timing control). |
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

- **Final thesis:** 109 pages, MD5 `a27f13dfb6b3da4c5a1ad610dbfa8514`.
- **Numbers:** every number on the slides was checked against the final thesis text and the filtered data. This includes Table 6.2 on B9, Tables 6.3–6.4 on Slide 13 and B13, and the component degrees of freedom in the B13 notes.
- **Comparison with version 3:** text and notes were compared slide by slide. Only the changes listed above differ.
  - The scripts and transitions total 1,875 words in the speaker notes, five fewer than version 3 by the same count.
- **Validation:** the file passed OOXML validation, and every image keeps its native aspect ratio.
- **Rendering:** all 30 slides were rendered and inspected.
- **Spelling:** the authored text uses Australian spelling. "Generalization" and "generalized" appear only in published reference titles.
- **Plan snapshot:** the plan snapshot (MD5 `328dbbca5b4a1c105784a1221a608a9c`) gives the same slides and notes as the 5 November plan.

## Rebuild

Run from this folder, with Lato installed:

```
python3 assets/code/extract_data.py <Simulations root> assets/data
python3 assets/code/charts.py
python3 assets/code/build_deck.py <copy of vF2 .pptx> Daniel_Zhao_Welch_MI_Presentation.pptx assets/charts assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md
python3 assets/code/gen_notes.py Daniel_Zhao_Welch_MI_Presentation.pptx assets/plan_snapshot/PRESENTATION_EXECUTION_PLAN_2026-11-04.md Daniel_Zhao_Welch_MI_Presentation_Speaker_Notes.md
```

`charts.py` reads `assets/data/` and writes `assets/charts/`. `build_deck.py` needs `pandoc`.
