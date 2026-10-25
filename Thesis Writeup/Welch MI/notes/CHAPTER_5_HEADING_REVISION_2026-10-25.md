# Chapter 5 heading revision — 25 October 2026

The reader requested headings that identify the role of each part of Chapter 5 in the thesis as a whole. The five section headings are now:

1. **5.1 Setup: Constructing joint distributions with known MI**
2. **5.2 RQ1: Checking the variance approximations**
3. **5.3 RQ2: False-positive rates under equal MI**
4. **5.4 RQ2: Nominal and calibrated power**
5. **5.5 Shared evaluation: Sampling and uncertainty**

RQ1 and RQ2 correspond to the two research questions in Section 1.2. Both false-positive rates and power belong to RQ2. Sampling and interval calculations support the evaluation rather than introducing a third research question.

The pre-edit 98-page manuscript and all active source/figure inputs are preserved in `archive/before_chapter5_heading_revision_2026-10-25.zip`.

## Verification

- Normalising only the five section-heading strings makes the old and new Chapter 5 source byte-identical. All body text, mathematics, citations, figures and tables are unchanged.
- Chapter/section numbering, chapter page spans and the total of 98 pages are unchanged. The main text remains 60 pages.
- No other chapter, appendix, scientific source or result is edited. Appendix C is unchanged; the preceding discussion about possible cuts has not been implemented.
- The existing eight packaging tests pass. The main build has no LaTeX warnings, undefined references or overfull/underfull boxes.
- Physical pages 4–8 and 42–51 were rendered and inspected. Contents entries, section headings, running headers, page flow and the transition to Chapter 6 fit cleanly.

Final checksum/inventory delivery verification passes. The extracted source archive builds independently without warnings and produces identical PDF text. These completed checks are recorded in the root verification file. No Git commit or experiment rerun was requested.
