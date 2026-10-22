# Exploratory real-data comparison of Normal Wald and Expanded Welch

Specified 10 October 2026 before calculating any method p-values. This is a
separate feasibility exploration, not an amendment to the thesis or its
simulation design. No third method, smoothing or method-code change is used.

## Sources and six fixed comparisons

All three datasets are public UCI datasets under CC BY 4.0. Download the
original archives, retain them intact and record SHA-256 checksums.

| Dataset | Group P / group Q | Predictor X | Outcome Y |
| --- | --- | --- | --- |
| [Adult](https://archive.ics.uci.edu/dataset/2/adult), Becker and Kohavi (1996), DOI 10.24432/C5XW20 | Female / Male | education (16 original categories) | income above USD 50000 |
| Adult | Female / Male | occupation (14 original categories) | income above USD 50000 |
| [Online Shoppers](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset), Sakar and Kastro (2018), DOI 10.24432/C5F88Q | New_Visitor / Returning_Visitor | Month (the dataset's original observed categories) | Revenue |
| Online Shoppers | New_Visitor / Returning_Visitor | Weekend | Revenue |
| [Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance), Cortez (2008), DOI 10.24432/C5TG7T | school GP / school MS | studytime (original four levels) | final Portuguese grade G3 >= 10 |
| Student Performance | school GP / school MS | Medu (original five maternal-education levels) | final Portuguese grade G3 >= 10 |

The question is whether the predictor--outcome MI differs between the two
groups, not whether either predictor is independent of the outcome. All
comparisons are two-sided at 5%. Report all six, regardless of significance.
An MI difference is not a causal effect, a fairness metric or a change in
out-of-sample prediction accuracy.

## Preparation

- Combine Adult's original random training and testing partitions. Strip
  whitespace and the period appended to test-file income labels. Keep all
  records for education; drop only records with missing occupation for the
  occupation comparison. Do not discard records for unrelated missing values.
  Do not apply the survey weights: the implemented methods require integer
  counts, and this is an unweighted benchmark-data illustration, not a
  design-based estimate for the US population. Retain duplicate-looking rows;
  no person identifier is available to determine whether they are repeated
  people or genuinely identical profiles.
- Use all Online Shoppers records in the two chosen visitor types. Exclude
  the separate Other type. UCI states that each session belongs to a different
  user. Do not use transaction-related continuous variables or invent bins.
- Use only student-por.csv. Do not pool or compare it with student-mat.csv,
  because 382 students occur in both subject files. Keep grades of zero and
  define the outcome explicitly as G3 >= 10, without optimising the threshold.
- Use the same category order and declared alphabet in both group tables.
  Months use the pooled observed original labels, not group-specific levels.
  Record empty cells, empty margins, class proportions and group sizes.
  Do not smooth or silently remove empty group-specific categories.

## Full-data analysis

For each comparison, save both count tables, plug-in and leading-bias-corrected
MI for each group, their corrected difference, shared standard error and
statistic, Expanded Welch component/combined degrees of freedom, both
p-values, method validity and 95% approximate intervals. Report raw p-values
and Holm-adjusted p-values across the six comparisons separately for each
method. Count-table calculations use the current thesis implementations with
Simple Welch and the unbiased-variance sensitivity variant disabled.

## Repeated smaller-sample analysis

At equal group sample sizes in {50, 100, 200, 500, 1000, 2000, 5000}, retain
only sizes not exceeding either available group count. Draw 5000 subsets
without replacement per comparison and size, independently across groups,
using deterministic PCG64 streams derived from master seed 20261010,
comparison ID and sample size. Sampling table cells through a multivariate
hypergeometric distribution is equivalent to uniform row subsampling.

Keep the full-data category alphabet fixed. Apply both methods to each same
table pair. Save raw sampled counts and outputs, unconditional and
valid-only rejection frequencies, validity, paired decision disagreements,
degrees-of-freedom summaries and support loss. Wilson intervals quantify
Monte Carlo uncertainty conditional on the fixed datasets. The frequencies
are decision stability under subsampling, not estimates of power, Type I
error or independent replication in the source population. Subsets overlap
across repetitions; 5000 repetitions do not create 5000 new datasets.

## Checks and interpretation

Recompute the full-data formulas independently of the method's helper
functions. Audit sampled table totals, upper bounds, methods' nested rejection
decisions, raw records and reported summaries. Use no outcome-dependent
category changes or post-hoc tuning to obtain different decisions.

The true population MI is unknown. Neither disagreement nor a larger p-value
establishes which method is correct. Empty observed cells do not prove
population zeros, but extensive missing support limits first-order inference.
Sampling independence and representativeness are working assumptions, not
verified guarantees: Adult is survey-derived; students can share classrooms;
shop sessions may share seasonal effects. Results are exploratory aggregate
comparisons, not demographic, educational or commercial decision guidance.

Keep all outputs in PracticalMIExploration. Do not edit or rebuild the thesis,
delivery archives or any working draft.
