# Targeted edit brief review - 23 October 2026

Applied edits 1, 2, 3, 5, 6, 8 and 9, plus the presentation-only shortening in edit 4. The existing two-calibration comparison remains. No third calibration rule or gain column was added. The numerical RQ1 sentence proposed in edit 7 was omitted; the abstract keeps its qualitative explanation. No study samples, populations, nominal rules or bootstrap intervals were changed.

The preserved baseline is `archive/before_targeted_edit_brief_2026-10-23.zip`. The final PDF remains 108 pages. Chapters 5-8 retain their previous spans: 6, 13, 3 and 2 pages (24 combined). All figure PDF assets, Chapters 2-4, Appendix A and Appendix B are byte-identical to that snapshot.

## Numerical provenance

`redesign_report.py` generates `calibration_grid_summary.csv/json` from the 120 all-attempt null settings in the saved 100,000-pair run. The comparison uses the change in absolute distance from 5%, with a strict 0.3-percentage-point threshold. Integer rejection counts retain equality at the tolerance boundary. The results are 29 toward, 52 away and 39 within tolerance. All 29 improvements have Wald above 5%; 48 of the 52 deteriorations have Wald below 5%. These descriptive counts replace the older 20,000-pair pilot counts.

`report_calibration_sensitivity.py` generates `calibration_sensitivity/nominal_upper_rates.csv` directly from all six existing validation batches. It applies the unchanged nominal decision API, retains invalid outputs as non-rejections, and records counts, validity and Wilson intervals for Wald, the sample-size rule and Expanded Welch. No regeneration or new fitting was required. The main-text numbers and grid counts enter through the generated `focused_redesign_reporting_values.tex`.

| Setting | Common MI | Wald (%) | Size df (%) | Expanded Welch (%) |
| --- | ---: | ---: | ---: | ---: |
| A, 2 SD | 0.329933611140 | 16.164 | 14.904 | 13.564 |
| A, 4 SD | 0.639867222281 | 17.744 | 16.449 | 15.442 |
| B, 2 SD | 0.150275552998 | 6.953 | 6.777 | 6.222 |
| B, 4 SD | 0.280551105996 | 7.623 | 7.429 | 7.251 |
| C, 2 SD | 0.026349906291 | 4.858 | 4.854 | 4.782 |
| C, 4 SD | 0.032699812582 | 4.888 | 4.886 | 4.827 |

Comparable pilot checks (near 0.33 for A, 0.15 and 0.28 for B) all meet the one-percentage-point tolerance. The largest absolute discrepancy is 0.149 percentage points. The pilot rows at MI 0.50 or 0.80 have different populations from the saved upper nulls and were not treated as exact matches. No new power gains were introduced.

| Setting | Method | Saved rate (%) | Pilot (%) | Difference (pp) |
| --- | --- | ---: | ---: | ---: |
| A, 2 SD | wald | 16.164 | 16.3 | -0.136 |
| A, 2 SD | expanded | 13.564 | 13.6 | -0.036 |
| B, 2 SD | wald | 6.953 | 7.0 | -0.047 |
| B, 2 SD | expanded | 6.222 | 6.3 | -0.078 |
| B, 4 SD | wald | 7.623 | 7.7 | -0.077 |
| B, 4 SD | expanded | 7.251 | 7.4 | -0.149 |

## Prose and placement: old and new

The entries below give the exact edited source passages. Generated numeric macros are expanded in the new passages so their printed values can be reviewed.

### 1. Abstract

Source: `frontmatter/abstract.tex`

Old:

```tex
in selected small-sample populations, at a cost in nominal power.
```

New:

```tex
in selected small-sample populations at common MI 0.02 nats, at a cost
in nominal power.
```

### 2. 1.2: cross-reference label

Source: `chapters_rewrite/01_introduction.tex`

Old:

```tex
\section{Research questions}
```

New:

```tex
\section{Research questions}
\label{sec:research-questions}
```

### 3. 1.3: contribution 4

Source: `chapters_rewrite/01_introduction.tex`

Old:

```tex
  selected populations where Expanded Welch brings false-positive rates
  closer to 5\% than Normal Wald, the dependence of calibrated power on
```

New:

```tex
  selected populations at common MI 0.02 nats where Expanded Welch brings
  false-positive rates closer to 5\% than Normal Wald, the dependence of calibrated power on
```

### 4. Chapter 5 opening

Source: `chapters_rewrite/05_experimental_design.tex`

Old:

```tex
values are equal. The evaluation follows three questions: are the
variance approximations used by Expanded Welch accurate, does its
cutoff improve false-positive rates, and what happens to power when
false-positive rates are comparable?
```

New:

```tex
values are equal. The evaluation addresses the two research questions in
Section~\ref{sec:research-questions}: whether the variance approximations
used by Expanded Welch are accurate, and how its false-positive rates
and power compare with those of the other rules.
```

### 5. 7.2 opening

Source: `chapters_rewrite/07_discussion.tex`

Old:

```tex
selected small-sample populations. Every rule returns a valid result
```

New:

```tex
selected small-sample populations, both at common MI 0.02 nats.
Every rule returns a valid result
```

### 6. 8.1 RQ2

Source: `chapters_rewrite/08_conclusion.tex`

Old:

```tex
small-sample populations, with a nominal power cost. Its power advantage
after calibration at common MI 0.02 is sensitive to the fitting
```

New:

```tex
small-sample populations at common MI 0.02 nats, with a nominal power
cost. Its calibrated power advantage is sensitive to the fitting
```

### 7. 8.2 future work

Source: `chapters_rewrite/08_conclusion.tex`

Old:

```tex
complete population tables differ. Reversed power paths, additional
association constructions and broader allocation comparisons would
```

New:

```tex
complete population tables differ. Reversed power paths, stronger
dependence at small sample sizes, additional association constructions
and broader allocation comparisons would
```

### 8. Chapter 6 generated values

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
\label{chap:results}
```

New:

```tex
\label{chap:results}
\input{figures_rewrite/focused_redesign_reporting_values}
```

### 9. 6.2 grid summary

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
Expanded Welch's small-sample improvements do not extend to uniformly
better calibration across the grid.
```

New:

```tex
Across the 120 settings, Expanded Welch moves rejection closer to 5\%
in 29 settings and farther away in 52, using
changes in distance greater than 0.3 percentage points.
All 29 improvements occur with Wald above 5\%;
48 of the 52 deteriorations occur with Wald
below 5\%. The remaining 39 settings fall within this tolerance.
```

### 10. 6.2.1 upper-null nominal rates

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
closer than either main comparator.
```

New:

```tex
closer than either main comparator.

Both rules over-reject at stronger common MI: in A at
0.33 nats, Wald rejects 16.16\% and
Expanded Welch rejects 13.56\% of pairs.
In B at 0.28 nats, the rates are
7.62\% and 7.25\%, respectively.
```

### 11. 6.3.2 figure relocation

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
\begin{figure}[!htbp]
\centering
\includegraphics[width=\textwidth]{focused_redesign_power_calibrated.pdf}
\caption{Power after calibration at common MI 0.02; bands show bootstrap uncertainty.}
\label{fig:redesign-calibrated-power}
\end{figure}
```

New:

```tex
[Moved to Appendix C.4; see the placement entry below.]
```

### 12. 6.3.2 appendix figure reference

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
both order samples by \(|T|\). Figure~\ref{fig:redesign-calibrated-power}
uses these lower-null cutoffs throughout each alternative curve.
```

New:

```tex
both order samples by \(|T|\). Appendix Figure~\ref{fig:redesign-calibrated-power}
shows the full curves under this lower-null calibration.
```

### 13. C.4 figure placement

Source: `appendices_rewrite/C_additional_results.tex`

Old:

```tex
\label{sec:calibration-sensitivity-results}

```

New:

```tex
\label{sec:calibration-sensitivity-results}

\begin{figure}[!htbp]
\centering
\includegraphics[width=\textwidth]{focused_redesign_power_calibrated.pdf}
\caption{Power after calibration at common MI 0.02; bands show bootstrap uncertainty.}
\label{fig:redesign-calibrated-power}
\end{figure}

```

### 14. 6.3.2 sensitivity conclusion

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
Expanded Welch gains power under this calibration, but the gain depends
on the null population used to fit the cutoff.
```

New:

```tex
The power gain depends on which null population supplies the cutoff.
```

### 15. 6.3.2 table interpretation and cross-null detail

Source: `chapters_rewrite/06_results.tex`

Old:

```tex
The table gives gains in percentage points with paired 95\% bootstrap
intervals including cutoff-fitting uncertainty. The lower null has
common MI 0.02; the upper null has the MI in the second column.
At A and two SDs, applying the lower-null calibration to upper-null
samples gives 11.2\% rejection for Wald and 13.7\% for Expanded Welch.
Using the upper-null cutoffs instead gives about 4.8--4.9\% there,
but only 1.63\% for Wald and 0.79\% for Expanded Welch at the lower
null. Thus the original gain compares rules matched at the lower null,
with different rejection rates at another equal-MI population.
The two checks do not establish control over every population satisfying
equal MI. Appendix~\ref{sec:calibration-sensitivity-results} reports
all cross-null rates and the full calibrated-power tables.
```

New:

```tex
Brackets give paired 95\% bootstrap intervals including uncertainty from
fitting the cutoffs. The lower null has common MI 0.02; the upper null
has the MI in the second column. Appendix~\ref{sec:calibration-sensitivity-results}
reports the cross-null rates and full power tables. The two checks do
not establish control over every population satisfying equal MI.
```

## Generated tables: old and new

Rates use percentages with two decimal places and decimal half-up rounding. Table 6.2 retains every confidence interval; the bounds share the rate units. Table C.4 MI differences use three significant figures, retaining meaningful trailing zeros. Table C.5 remains unchanged in percentage points, including its existing intervals.

### Table 6.2

Old:

```tex
\begin{tabular}{@{}lrr@{}}
\toprule
Setting & Normal Wald & Sample-size df\\
\midrule
A & 0.0835 [0.0818, 0.0853] & 0.0739 [0.0723, 0.0756]\\
B & 0.0747 [0.0730, 0.0763] & 0.0725 [0.0709, 0.0741]\\
C & 0.0486 [0.0473, 0.0500] & 0.0486 [0.0473, 0.0500]\\
16, same, 1,000 & 0.0060 [0.0056, 0.0065] & 0.0060 [0.0055, 0.0065]\\
16, same, 10,000 & 0.0438 [0.0426, 0.0451] & 0.0438 [0.0425, 0.0451]\\
16, different, 1,000 & 0.2601 [0.2574, 0.2628] & 0.2595 [0.2568, 0.2622]\\
16, different, 10,000 & 0.0478 [0.0465, 0.0491] & 0.0478 [0.0464, 0.0491]\\
\addlinespace[5pt]
\midrule
Setting & Expanded Welch & Moment reference\\
\midrule
A & 0.0490 [0.0476, 0.0503] & 0.0720 [0.0704, 0.0736]\\
B & 0.0552 [0.0538, 0.0567] & 0.0633 [0.0618, 0.0648]\\
C & 0.0477 [0.0464, 0.0490] & 0.0477 [0.0464, 0.0490]\\
16, same, 1,000 & 0.0053 [0.0048, 0.0057] & 0.0056 [0.0052, 0.0061]\\
16, same, 10,000 & 0.0426 [0.0414, 0.0439] & 0.0427 [0.0415, 0.0440]\\
16, different, 1,000 & 0.2484 [0.2457, 0.2510] & 0.2535 [0.2508, 0.2562]\\
16, different, 10,000 & 0.0468 [0.0455, 0.0482] & 0.0469 [0.0457, 0.0483]\\
\bottomrule
\end{tabular}
```

New:

```tex
\begin{tabular}{@{}lrr@{}}
\toprule
Setting & Normal Wald & Sample-size df\\
\midrule
A & 8.35\% [8.18, 8.53] & 7.39\% [7.23, 7.56]\\
B & 7.47\% [7.30, 7.63] & 7.25\% [7.09, 7.41]\\
C & 4.87\% [4.73, 5.00] & 4.87\% [4.73, 5.00]\\
16, same, 1,000 & 0.60\% [0.56, 0.65] & 0.60\% [0.55, 0.65]\\
16, same, 10,000 & 4.38\% [4.26, 4.51] & 4.38\% [4.25, 4.51]\\
16, different, 1,000 & 26.01\% [25.74, 26.28] & 25.95\% [25.68, 26.22]\\
16, different, 10,000 & 4.78\% [4.65, 4.91] & 4.78\% [4.64, 4.91]\\
\addlinespace[5pt]
\midrule
Setting & Expanded Welch & Moment reference\\
\midrule
A & 4.90\% [4.76, 5.03] & 7.20\% [7.04, 7.36]\\
B & 5.52\% [5.38, 5.67] & 6.33\% [6.18, 6.48]\\
C & 4.77\% [4.64, 4.90] & 4.77\% [4.64, 4.90]\\
16, same, 1,000 & 0.53\% [0.48, 0.57] & 0.56\% [0.52, 0.61]\\
16, same, 10,000 & 4.26\% [4.14, 4.39] & 4.27\% [4.15, 4.40]\\
16, different, 1,000 & 24.84\% [24.57, 25.10] & 25.35\% [25.08, 25.62]\\
16, different, 10,000 & 4.68\% [4.55, 4.82] & 4.70\% [4.57, 4.83]\\
\bottomrule
\end{tabular}
```

### Table C.4

Old:

```tex
\begin{tabular}{@{}lrrrr@{}}
\toprule
Setting: SD & Nats & Wald/ref. & Size df & Expanded\\
\midrule
A: 0 & 0.00000 & 0.0493 & 0.0493 & 0.0499\\
A: 1 & 0.15497 & 0.1407 & 0.1403 & 0.1559\\
A: 2 & 0.30993 & 0.3256 & 0.3252 & 0.3614\\
A: 3 & 0.46490 & 0.5441 & 0.5433 & 0.5891\\
A: 4 & 0.61987 & 0.7384 & 0.7377 & 0.7784\\
B: 0 & 0.00000 & 0.0498 & 0.0498 & 0.0496\\
B: 1 & 0.06514 & 0.0154 & 0.0154 & 0.0177\\
B: 2 & 0.13028 & 0.0442 & 0.0441 & 0.0554\\
B: 3 & 0.19541 & 0.1307 & 0.1303 & 0.1564\\
B: 4 & 0.26055 & 0.2766 & 0.2761 & 0.3159\\
C: 0 & 0.00000 & 0.0498 & 0.0498 & 0.0498\\
C: 1 & 0.00317 & 0.1585 & 0.1585 & 0.1588\\
C: 2 & 0.00635 & 0.4561 & 0.4561 & 0.4566\\
C: 3 & 0.00952 & 0.7668 & 0.7668 & 0.7672\\
C: 4 & 0.01270 & 0.9356 & 0.9356 & 0.9358\\
\bottomrule
\end{tabular}
```

New:

```tex
\begin{tabular}{@{}lrrrr@{}}
\toprule
Setting: SD & Nats & Wald/ref. & Size df & Expanded\\
\midrule
A: 0 & 0 & 4.93\% & 4.93\% & 4.99\%\\
A: 1 & 0.155 & 14.07\% & 14.03\% & 15.59\%\\
A: 2 & 0.310 & 32.57\% & 32.52\% & 36.15\%\\
A: 3 & 0.465 & 54.41\% & 54.33\% & 58.91\%\\
A: 4 & 0.620 & 73.84\% & 73.77\% & 77.84\%\\
B: 0 & 0 & 4.98\% & 4.98\% & 4.96\%\\
B: 1 & 0.0651 & 1.54\% & 1.54\% & 1.77\%\\
B: 2 & 0.130 & 4.42\% & 4.41\% & 5.54\%\\
B: 3 & 0.195 & 13.07\% & 13.03\% & 15.64\%\\
B: 4 & 0.261 & 27.66\% & 27.61\% & 31.59\%\\
C: 0 & 0 & 4.98\% & 4.98\% & 4.98\%\\
C: 1 & 0.00317 & 15.85\% & 15.85\% & 15.88\%\\
C: 2 & 0.00635 & 45.61\% & 45.61\% & 45.66\%\\
C: 3 & 0.00952 & 76.68\% & 76.68\% & 76.72\%\\
C: 4 & 0.0127 & 93.56\% & 93.56\% & 93.58\%\\
\bottomrule
\end{tabular}
```

### Table C.6

Old:

```tex
\begin{tabular}{@{}lrrr@{}}
\toprule
Setting: SD, null & Wald/ref. & Size df & Expanded\\
\midrule
A: 2, lower & 0.3256 & 0.3252 & 0.3614\\
A: 2, upper & 0.1858 & 0.1835 & 0.1782\\
A: 4, lower & 0.7384 & 0.7377 & 0.7784\\
A: 4, upper & 0.5491 & 0.5468 & 0.5509\\
B: 2, lower & 0.0442 & 0.0441 & 0.0554\\
B: 2, upper & 0.0468 & 0.0463 & 0.0473\\
B: 4, lower & 0.2766 & 0.2761 & 0.3159\\
B: 4, upper & 0.2640 & 0.2625 & 0.2601\\
C: 2, lower & 0.4561 & 0.4561 & 0.4566\\
C: 2, upper & 0.4547 & 0.4547 & 0.4541\\
C: 4, lower & 0.9356 & 0.9356 & 0.9358\\
C: 4, upper & 0.9342 & 0.9342 & 0.9341\\
\bottomrule
\end{tabular}
```

New:

```tex
\begin{tabular}{@{}lrrr@{}}
\toprule
Setting: SD, null & Wald/ref. & Size df & Expanded\\
\midrule
A: 2, lower & 32.57\% & 32.52\% & 36.15\%\\
A: 2, upper & 18.58\% & 18.35\% & 17.83\%\\
A: 4, lower & 73.84\% & 73.77\% & 77.84\%\\
A: 4, upper & 54.91\% & 54.68\% & 55.09\%\\
B: 2, lower & 4.42\% & 4.41\% & 5.54\%\\
B: 2, upper & 4.68\% & 4.63\% & 4.73\%\\
B: 4, lower & 27.66\% & 27.61\% & 31.59\%\\
B: 4, upper & 26.40\% & 26.25\% & 26.01\%\\
C: 2, lower & 45.61\% & 45.61\% & 45.66\%\\
C: 2, upper & 45.47\% & 45.47\% & 45.42\%\\
C: 4, lower & 93.56\% & 93.56\% & 93.58\%\\
C: 4, upper & 93.42\% & 93.42\% & 93.41\%\\
\bottomrule
\end{tabular}
```

### Table C.7

Old:

```tex
\begin{tabular}{@{}lrrrrr@{}}
\toprule
Setting: SD & Fitting null & Evaluation null & Wald/ref. & Size df & Expanded\\
\midrule
A: 2 & lower & lower & 0.0493 & 0.0493 & 0.0499\\
A: 2 & lower & upper & 0.1120 & 0.1124 & 0.1371\\
A: 2 & upper & lower & 0.0163 & 0.0161 & 0.0079\\
A: 2 & upper & upper & 0.0487 & 0.0486 & 0.0484\\
A: 4 & lower & lower & 0.0493 & 0.0493 & 0.0499\\
A: 4 & lower & upper & 0.1256 & 0.1258 & 0.1558\\
A: 4 & upper & lower & 0.0134 & 0.0133 & 0.0053\\
A: 4 & upper & upper & 0.0504 & 0.0501 & 0.0500\\
B: 2 & lower & lower & 0.0498 & 0.0498 & 0.0496\\
B: 2 & lower & upper & 0.0482 & 0.0484 & 0.0576\\
B: 2 & upper & lower & 0.0526 & 0.0522 & 0.0415\\
B: 2 & upper & upper & 0.0503 & 0.0503 & 0.0504\\
B: 4 & lower & lower & 0.0498 & 0.0498 & 0.0496\\
B: 4 & lower & upper & 0.0537 & 0.0540 & 0.0676\\
B: 4 & upper & lower & 0.0456 & 0.0454 & 0.0327\\
B: 4 & upper & upper & 0.0498 & 0.0498 & 0.0499\\
C: 2 & lower & lower & 0.0498 & 0.0498 & 0.0498\\
C: 2 & lower & upper & 0.0497 & 0.0497 & 0.0499\\
C: 2 & upper & lower & 0.0493 & 0.0493 & 0.0490\\
C: 2 & upper & upper & 0.0494 & 0.0494 & 0.0494\\
C: 4 & lower & lower & 0.0498 & 0.0498 & 0.0498\\
C: 4 & lower & upper & 0.0503 & 0.0503 & 0.0506\\
C: 4 & upper & lower & 0.0484 & 0.0484 & 0.0481\\
C: 4 & upper & upper & 0.0486 & 0.0486 & 0.0486\\
\bottomrule
\end{tabular}
```

New:

```tex
\begin{tabular}{@{}lrrrrr@{}}
\toprule
Setting: SD & Fitting null & Evaluation null & Wald/ref. & Size df & Expanded\\
\midrule
A: 2 & lower & lower & 4.93\% & 4.93\% & 4.99\%\\
A: 2 & lower & upper & 11.20\% & 11.24\% & 13.71\%\\
A: 2 & upper & lower & 1.63\% & 1.61\% & 0.79\%\\
A: 2 & upper & upper & 4.87\% & 4.86\% & 4.84\%\\
A: 4 & lower & lower & 4.93\% & 4.93\% & 4.99\%\\
A: 4 & lower & upper & 12.56\% & 12.58\% & 15.58\%\\
A: 4 & upper & lower & 1.34\% & 1.33\% & 0.53\%\\
A: 4 & upper & upper & 5.04\% & 5.01\% & 5.00\%\\
B: 2 & lower & lower & 4.98\% & 4.98\% & 4.96\%\\
B: 2 & lower & upper & 4.82\% & 4.84\% & 5.76\%\\
B: 2 & upper & lower & 5.26\% & 5.22\% & 4.16\%\\
B: 2 & upper & upper & 5.04\% & 5.03\% & 5.04\%\\
B: 4 & lower & lower & 4.98\% & 4.98\% & 4.96\%\\
B: 4 & lower & upper & 5.37\% & 5.40\% & 6.76\%\\
B: 4 & upper & lower & 4.56\% & 4.54\% & 3.27\%\\
B: 4 & upper & upper & 4.99\% & 4.98\% & 4.99\%\\
C: 2 & lower & lower & 4.98\% & 4.98\% & 4.98\%\\
C: 2 & lower & upper & 4.97\% & 4.97\% & 4.99\%\\
C: 2 & upper & lower & 4.93\% & 4.93\% & 4.90\%\\
C: 2 & upper & upper & 4.94\% & 4.94\% & 4.94\%\\
C: 4 & lower & lower & 4.98\% & 4.98\% & 4.98\%\\
C: 4 & lower & upper & 5.03\% & 5.03\% & 5.06\%\\
C: 4 & upper & lower & 4.84\% & 4.84\% & 4.81\%\\
C: 4 & upper & upper & 4.87\% & 4.87\% & 4.86\%\\
\bottomrule
\end{tabular}
```

## Reporting and validation changes

The reporting code adds the nominal upper-null summary, grid classifications and generated manuscript values; it changes presentation units for the four named rate tables. Existing power samples, calibrated rates and bootstrap intervals are reused. Tests add independent normal/Student t checks of all 18 nominal rates and a boundary/overshoot check for the grid count. Existing table consistency assertions now check percentages.

The relocated lower-null figure changes from Figure 6.6 to Figure C.7. The following appendix figures change to C.8 and C.9. Labels and cross-references resolve automatically, and both lists of figures and tables were checked. The figure dimensions, font sizes and PDF bytes are unchanged.

No em dashes, genuinely, or rather-than constructions were introduced. The existing statistical limitation that two null populations do not establish general size control is retained. Captions remain short, validity details remain in the body, and all intervals remain available.

Final test, archive, preservation and isolated-build results are recorded in `REDESIGN_VERIFICATION.json` after packaging.

Final verification: 275 local tests and 185 extracted-package tests pass. The extracted source builds with no LaTeX warnings and produces PDF text identical to the delivery PDF. All 30,042 original files match their saved hashes. The current delivery consistency check passes. The final PDF is 108 pages; Chapters 5-8 remain 24 pages. Changed pages, percentage tables, figure placement, lists and cross-references were rendered and inspected. No Git commit was made in this pass.
