# Two-dimensional Table 6.2 — 30 October 2026

Implemented the approved above/below-5% breakdown and rebuilt the PDF. Rows identify Normal Wald's observed rejection rate; the grouped column heading identifies Expanded Welch's change relative to Normal Wald. The original 0.3-percentage-point tolerance applies to the change in absolute distance from 5%.

| Normal Wald rate | Closer to 5% | Farther from 5% | Within tolerance | Total |
| --- | ---: | ---: | ---: | ---: |
| Above 5% | 29 | 4 | 5 | 38 |
| Below 5% | 0 | 48 | 34 | 82 |
| Total | 29 | 52 | 39 | 120 |

The six cells and all totals were reproduced from the saved integer rejection-count classifications using `calibration_grid`. These classifications match the saved grid summary. No Wald rate is exactly 5% in this grid. All four deteriorations in the above-5% row cross below 5% under Expanded Welch and end farther from the target. The body now explains this finding without repeating every count.

The reporting helper generates the new macros from the grid and checks that an equality row is not required. All existing reporting values are preserved. Relative to the pre-edit snapshot, only Section 6.2.1 changes in the manuscript; all other numbered displays and the earlier stronger-MI reordering are preserved.

All five existing manuscript-consistency tests, the paragraph-style check and the whitespace check pass. No experiments, fitting batches or bootstrap draws were rerun.

## Rebuild verification

The final PDF has 107 A4 pages and no LaTeX warnings, overfull/underfull boxes or unresolved references. Inspected PDF pages 62–63 and 67. Table 6.2 is on printed page 53 (PDF page 62), with readable method headings, counts and interpretation. The following plot remains readable, and Tables 6.4 and 6.5 remain together on printed page 58.

The main, build and named delivery PDFs are identical. The refreshed source archive was checked against every packaged source file. The experiment supplement's report-generator member was updated and checked byte-for-byte against its source; metadata for all other 24,995 members is preserved. The complete inventory, input sizes and timestamps were checked, and a new supplement checksum was calculated. Unchanged archive members were copied without recompression; no independent exported-source build was run for this interim update.

The pre-edit source and previous delivery files are preserved in `../archive/before_two_dimensional_null_grid_2026-10-30.zip`.

PDF SHA-256: `366ab9ed357b1782a1b8926f86c6d0af75f8dbb5bebf79885f7a192a0198c22f`.

Source archive SHA-256: `a6cfa41b1a9faf542fad10f8f20fd6846968c6f3a2608e83e9ff8516a6c62270`.

Supplement SHA-256: `2986f079aaed3cdf313912cea75ef4c3525bd1a2386f9c61d96712a117b5a1f5`.
