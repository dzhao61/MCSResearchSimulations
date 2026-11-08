# Presentation style template and plan review notes

> Historical inspection record from 4 November 2026. The presentation was
> substantively replanned on 5 November in
> `PRESENTATION_EXECUTION_PLAN_2026-11-04.md` and manifest version 2.
> Their 14-main/14-backup structure, primary 25-page reference, colour roles
> and resolved design choices supersede the earlier conflicts and open
> decisions below. Preserve this record for its source inspection details.

Prepared 4 November 2026. These notes accompany
`PRESENTATION_EXECUTION_PLAN_2026-11-04.md` and its evidence manifest. They
record the style template Daniel supplied, where it conflicts with the plan,
checks run on the plan, and decisions still open. No slides have been built.

## 1. Materials received

| File | Notes |
| --- | --- |
| `Zhao_Daniel_Presentation_vF2.pptx` and `.pdf` | Daniel's earlier 11-slide proposal talk, "Correcting the Analytical Null for Discrete Mutual Information". Supplied as the **stylistic template** for the new deck. Its content is outdated and must not be reused. |
| `18cp Research Path deliverables.pdf` | Identical to the copy in `Research/Example Thesis/` (SHA-256 `f9748fa0…`). |
| `18CP Research Pathway Project Marking Rubric V3.pdf` | Identical to the folder copy (`2f53a5f4…`). Thesis rubric. |
| `Presentation Marking Criteria.pdf` | Identical to the folder copy (`c45e7dee…`). Still only "Page 5 of 5". |

The vF2 template is not yet saved in the Research folder. Copy it into
`Thesis Writeup/Welch MI/presentation/style_reference/` when the build starts.

### University requirements (unchanged)

- Week 15 (Exam Week 1). The exact slot comes later by calendar invitation.
- Up to 20 minutes of talk, cut off at 20:00, then up to 10 minutes of questions.
- Worth 20% of the project. The audience is the markers, the supervisor, staff and students.
- Upload a PDF to Canvas. PowerPoint may be used live.
- Canvas has a declaration on whether future students may view the slides.
- A Canvas template is mentioned, but none has been supplied.

The presentation rubric awards 30 for content coverage, 20 for understanding and
answers, 20 for time use, 20 for engagement and 10 for fonts, colours and
readability. The thesis rubric (V3) adds context for how the talk can show
"critical evaluation", "substantive original contribution" and
"constructive future directions".

## 2. Style template specification (extracted from vF2 XML)

### Canvas

- 16:9, 13.333 × 7.5 in (matches the plan).
- White background on content slides.
- No slide numbers, footers or logo on any slide.

### Typography

| Element | Font | Size | Weight | Colour | Position |
| --- | --- | --- | --- | --- | --- |
| Content slide title | Lato | 36 pt | Bold | Black | x 0.85, y 0.41, w 11.5, h 0.81 in; left-aligned |
| Lead sentence under title | Lato | 16 pt | Bold | Black, with the key phrase in orange `E97132` | x 0.85, y 1.21, w 11.5 in; one or two lines |
| Section headings inside a slide | Lato | 18–20 pt | Bold | Orange `E97132`, or white on a header bar | |
| Panel body text | Lato | 12–14 pt | Regular | Grey `333333` | |
| Panel labels | Lato | 13–14 pt | Bold | Orange or navy | |
| Footnote / image source | Lato | 9 pt | Regular | Black | Bottom left |
| Equations | Cambria Math (native PowerPoint equations) | 16–20 pt | | Black | |
| Title slide title | Theme font (Aptos Display) | 26 pt | Regular | Orange | Left panel |
| Title slide subtitle | Theme font | 16 pt | Regular, with degree in italics | Black | Below a thin grey rule |

The template mixes Aptos on the title slide with Lato everywhere else. Use Lato throughout the new deck.

### Colour palette

| Role | Hex |
| --- | --- |
| Primary accent (highlights, icon circles, headings, arrows) | `E97132` (theme accent 2) |
| Secondary structure (header bars, numbered circles, panel labels) | Navy `1F3A5C` |
| Body text | `333333`; muted `555555`, `888888` |
| Orange tint panel | Fill `FFF1E8` / `FFF3E8`, border `F5C6A7` |
| Blue tint panel | Fill `E8EFF7` / `E8F0F7`, border `C8D8EA` |
| Positive / negative panels | Green `E8F5E9` with text `2E7D32`; red `FFEBEE` with text `C62828` |

The theme file is stock Office 2023, so `E97132` is accent 2 and the theme fonts are Aptos.

### Motifs

- Orange filled circles, 0.56–0.62 in, holding white Office SVG icons, letters (A/B/C) or numbers (1/2/3).
- Rounded-rectangle header bars, orange or navy, with white bold 18 pt text, over a tinted panel.
- Rounded tinted panels with a small corner radius.
- Orange block arrows between steps.
- A dashed black vertical divider (1.5 pt) between halves. Orange vertical rules (2.25 pt) appear in comparison tables.
- Light grey horizontal row rules in tables, with orange bold row labels on the left.
- Key equations sit centred in a rounded box with an orange border and orange tint.
- Title slide: a full-bleed photo of normal and t distributions on the right; a white curved panel on the left; a small orange bar top left; a thin grey rule above the name.
- Title slide photo is `ppt/media/image1.png`, only 760 × 484 px. It is soft when stretched to 9 in.

### Habits not to carry over

- Speaker notes: slides 3–11 repeat stale ASX-bank text pasted from another talk.
- Body text at 9–14 pt is too small for projection under the rubric's readability criterion.
- Numbered references `[n]`. The plan specifies author–year.
- "chi-square". The thesis uses "chi-squared".
- Title Case titles. The plan uses sentence case (open decision, see Section 5).

## 3. Conflicts between the plan (Section 4) and the template

The plan's visual specification was written before the template was supplied.
Daniel's instruction to use vF2 as the stylistic template takes precedence
where they conflict. The plan's content, evidence, chart encodings and
readability rules still apply.

| Topic | Plan | Template | Proposed resolution |
| --- | --- | --- | --- |
| Accent colour | Single restrained navy | Orange primary, navy secondary | Use the template: orange highlights, navy structure. |
| Font | Aptos or Arial | Lato | Lato for all text; Cambria Math for equations. |
| Decoration | Avoid cards, badges and repeated framing boxes | Tinted panels, header bars, icon circles | Use the template motifs where they organise content (Slides 4, 6, 7, 15, 16, B-series tables). Keep chart slides clean so the evidence dominates. |
| Text size | Titles 32–36, body 24–28, chart labels 20–24, sources 16–18 pt | Title 36, lead 16, body 12–14, footnotes 9 pt | Keep 36 pt titles. Lead sentence at 20 pt. Body and table text at 20–24 pt, never below 18. Chart labels at least 18 pt. Source line 12–14 pt. |
| Lead sentence | Only the exact copy listed per slide | A bold takeaway sentence on every content slide with an orange key phrase | Put the plan's setting line or takeaway in the lead-sentence slot. Do not add wording beyond the plan's copy. |
| Title slide | Minimal, small USyd logo, no decorative background | Photo with curved white panel | Open decision. |
| Slide numbers | Required (jumping to backups by number) | None | Add a quiet slide number at bottom right. |
| Chart colours | Okabe–Ito blue `0072B2`, orange `E69F00`, green `009E73` | None defined | Keep the plan's chart colours. `E69F00` sits close to the accent `E97132`, so avoid accent-orange text inside chart areas. Use navy or black for chart callouts. |

## 4. Plan review

### Numbers checked against the saved CSVs (4 November)

- **Slide 10:** all three rows match (8.352/4.897, 0.604/0.525, 26.011/24.836%). Validity is 100% for both methods in each row.
- **Slide 11:** 36.38% (Wald) and 34.38% (Expanded Welch) at MI 0.005 and n = 1,000, both 100% valid. At n = 50,000 the rates are 3.66% and 3.60%, below 5% as the script says.
- **Nesting:** Expanded Welch never exceeds Wald across all 360 null and 360 power settings.
- **Timing:** the table totals 18:50 and the short route 16:45. The late route after an 18:00 finish of Slide 13 ends at about 19:35. The scripts average about 109 words per minute.
- **Backup B5:** (d + κ)/2 = 4.60, (d + κ)²/(d + 2κ) = 9.00 and 2(d + κ)/(d + 2κ) = 1.96, all consistent.
- **Slide 14:** 4 × 0.000373 = 0.00149, consistent with the month comparison ranking third in the Holm sequence.

### Small issues

- **Slide 9:** the plan calls `#A53648` "purple", but that hex is dark crimson. Decide which colour is meant. Crimson also sits close to the orange accent.
- **Slide 5:** the t(3) illustration gives a cutoff of 3.18 against 1.96. In the application the combined degrees of freedom are about 26.8, giving a cutoff of 2.05. The plan already labels t(3) as an illustration. Consider saying in speech that estimated values are often much larger, so the audience does not take the illustrated gap as typical.
- The plan's font guidance (Aptos or Arial) is superseded by the template (Lato).

## 5. Open decisions for Daniel

1. **Title slide:** reuse the vF2 photo layout, or use the plan's minimal cover with the USyd logo? If the photo is reused, a higher-resolution copy would look sharper.
2. **Title case:** Title Case as in vF2, or sentence case as in the plan?
3. **Lead sentences:** on every content slide as in vF2, or only where the plan gives a setting line?
4. **Final PDF:** export from PowerPoint on the Mac (as with vF2), or from the build workspace? Both render the equations correctly.

## 6. Build-path notes

- **Output:** per the plan, an editable `.pptx`, a matching `.pdf`, a speaker-notes markdown file and `assets/` in `Thesis Writeup/Welch MI/presentation/`.
- **Equations:** native PowerPoint equations (OMML) render correctly through LibreOffice in the build workspace. This was tested on vF2 slide 3.
- **Fonts:** Lato was installed in the build workspace from `@fontsource/lato` (latin subset), so preview renders match the PowerPoint export in line breaks and fit.
- **Icons:** vF2 uses Office SVG icons. Equivalent icons can be reused by duplicating slide elements or recreated as SVG/PNG in white on orange circles.
