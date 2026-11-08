# Chapter 6 reading-order edits — 28 October 2026

The user approved three small edits following the first-pass reading assessment. The scope was to reduce the table-label burden in Section 6.1.2, separate the comparisons in Section 6.1.3, and finish explaining calibrated power before introducing calibration sensitivity in Section 6.3.2.

## Implementation and reading review

1. **Section 6.1.2:** shortened the Table 6.1 guide and divided it into moment-ratio and component-degrees-of-freedom paragraphs. The common observed-variance denominator, population versus averaged sample-based predictions, column-label mappings and complete inclusion of positive finite estimates remain explicit. The worked comparison and following explanation of sample substitution are unchanged.
2. **Section 6.1.3:** explained Figure 6.3 together before returning to Table 6.1. The figure guide identifies the mean and sampling variance separately. The subsequent comparison explicitly names the population first-order and averaged sample-based predictions of the sampling variance. The discussion retains the quadratic sampling contribution, the loss of local accuracy as MI grows, the numerical scale of the prediction errors and their implications for degrees of freedom.
3. **Section 6.3.2:** moved B's persistent dip beside the A/C interpretation of Figure 6.7, before the calibration-sensitivity question. At this position, the text says calibration at common MI 0.02; the lower-null terminology is introduced later with the two calibration settings.

The revised passages were reread with their surrounding explanations. Each comparison identifies its target, the figure interpretation precedes the next question, and the table guide retains necessary definitions without repeating each population's formulas. The chapter is two whitespace-delimited source words shorter overall; this is a reading-order revision rather than an expansion.

## Source verification

- All changes are confined to the three approved subsections. All displayed equations, figure/table blocks, labels and citations in Chapter 6 are unchanged.
- The other 103 tracked baseline source and figure assets are byte-identical. Numerical table values and figure files were not edited.
- Five existing manuscript consistency tests pass. The paragraph-style guard and whitespace check pass; Chapter 6's braces, environments and math delimiters are balanced.
- The ten current PDF/delivery files retain their baseline sizes and modification times, and the main PDF retains its SHA-256 hash. No LaTeX build, delivery refresh or experiment was run.

The pre-edit chapter and verification record are preserved in `archive/before_chapter6_final_readability_2026-10-28.zip`. Machine-readable checks are in `notes/CHAPTER_6_READING_ORDER_CHECKS_2026-10-28.json`. The source is ready; rendered page flow will be checked at the next explicitly requested rebuild.
