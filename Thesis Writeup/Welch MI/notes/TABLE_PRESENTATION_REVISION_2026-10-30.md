# Chapter 6 table presentation — 30 October 2026

Implemented the requested changes to Table 6.4 and the former Table 6.8, then completed the requested PDF rebuild and delivery refresh. Table 6.2 was subsequently converted to the two-dimensional version below and rebuilt; the later implementation and current delivery hashes are recorded in [TWO_DIMENSIONAL_NULL_GRID_2026-10-30.md](TWO_DIMENSIONAL_NULL_GRID_2026-10-30.md).

## Implemented

- **Table 6.4:** the first five rows now follow the setting order in Table 6.3: A, B, C, same-skew 16 × 16 at n = 1,000, and different-skew 16 × 16 at n = 1,000. A divider separates the two n = 10,000 checks. The preceding paragraph explains that grouping and retains the all-valid statement for all seven settings. Every rate and confidence interval is preserved.
- **Former Table 6.8:** replaced the variable/population mapping with three sentences defining X, Y, P, Q and the equal-MI null. The following paragraph still explains the count-table construction. Sample sizes, independence assumptions, bias corrections, numerical results and interpretation are unchanged. The application estimates and test results are now Tables 6.8 and 6.9, respectively.
- Updated both reporting entry points and the table writer so regeneration preserves Table 6.4's ordering and divider. No experiment, fitting or bootstrap computation was run.

The preceding sources are preserved in `../archive/before_table_streamlining_2026-10-30.zip`.

## Table 6.2 proposal, subsequently implemented

Rows should classify **Normal Wald's observed false-positive rate** relative to 5%. Columns should classify how Expanded Welch changes the absolute distance from 5%, using the existing 0.3-percentage-point tolerance.

| Normal Wald rate | Closer to 5% | Farther from 5% | Within tolerance | Total |
| --- | ---: | ---: | ---: | ---: |
| Above 5% | 29 | 4 | 5 | 38 |
| Below 5% | 0 | 48 | 34 | 82 |
| Total | 29 | 52 | 39 | 120 |

No Wald rate is exactly 5% in this grid. The four deteriorations in the first row cross below 5% and end farther from the target. This layout preserves the existing column totals and exposes the connection between the baseline rate and the effect of the larger cutoff. It also avoids suggesting that every reduction from a Wald rate above 5% improves calibration.

These counts were independently reproduced with `calibration_grid` from the saved rejection counts in `rates.csv` and the 120 null settings identified by `displays.csv`. The resulting classifications match `calibration_grid_summary.csv`. No estimates were recomputed from simulation records.

## Source verification

All five existing manuscript-consistency tests pass. The paragraph-style check and whitespace check pass. The revised Table 6.4 reproduces the saved rates and intervals exactly through the updated table writer. Its row contents are identical to the previous table; only order and the divider changed.

The application-definition table is the only removed numbered display. All other Chapter 6 equation, figure and table blocks and its citations are preserved. Active labels and references resolve statically.

## Requested PDF rebuild

The rebuilt PDF remains 107 A4 pages. The final LaTeX log has no warnings, overfull or underfull boxes, or unresolved references. Inspected PDF pages 66–67 and 74–75 (printed pages 57–58 and 65–66). Table 6.4's divider and grouping are clear, its guide remains directly before it, and the application definitions and results flow without the former mapping table. Tables fit within the margins and retain readable typography. No further layout or manuscript changes were needed during the build.

The main, build and named delivery PDFs are identical. The refreshed source archive was verified against all packaged source files. The experiment supplement's report-generator member was updated, with its bytes checked against the current source. The inventory remains 24,996 files; metadata for all other 24,995 members is unchanged. Input sizes and modification times were verified, using the updated member's extended UTC timestamp because its DOS timestamp rounds to an even second. A new supplement checksum was calculated. No experiments or independent exported-source build were run, and unchanged members were copied without recompression.

The previous PDF, source archive, checksums and packaged report generator are preserved in `../archive/before_table_presentation_pdf_build_2026-10-30.zip`.

PDF SHA-256: `f6401f58f22702041120287211e32c6a0850a7c1c9f4b578bf49db4714f9287c`.

Source archive SHA-256: `e11522bc6ec474359f9fe31bb0e9f51413df7cfd4caea0c7a645a10718b7e276`.

Supplement SHA-256: `bc41f54d29d85b0590f5d99ef7407062edea9d42a196c540b47b30afbb08d314`.
