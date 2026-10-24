# Findings from the practical-data exploration

## Recommendation

Online Shoppers is the strongest candidate for an illustrative application.
The practical question is whether month of visit carries the same amount of
information about purchasing for new and returning visitors. It uses existing
categorical variables, natural disjoint visitor groups and a relevant computing
application. The source states that every recorded session belongs to a
different user. The groups are naturally unequal: 1694 new visitors and 10551
returning visitors, making the application distinct from the main balanced
simulation comparisons.

Its corrected MI estimates are 0.004316 and 0.017880 nats, respectively.
Their difference is -0.013563 nats, with shared standard error 0.003333.
Normal Wald gives p=0.00004714; Expanded Welch gives p=0.00037263 using
26.79 degrees of freedom. Both reject equal MI at 5%, including after Holm
adjustment across the six comparisons (adjusted p=0.00018856 and 0.00149051).
The Student t distribution makes the p-value appreciably larger without
changing the observed ordering or the full-data decision.

At 1000 records per group, 2114 of 5000 subset pairs reject under Wald and
1859 reject under Expanded Welch. Both calculations are valid in every pair;
255 pairs, or 5.10%, therefore change the decision solely because of the
different cutoff. This is a practical example of the adjustment affecting
decisions, not evidence that those 255 Wald decisions were false positives.
The full-data month tables have one empty cell in the new-visitor group and
no empty margins. Smaller subsets can lose entire months: 42.12% of the
new-visitor subsets at n=1000 have an empty month margin. That support
diagnostic should accompany any eventual use of the subset comparison.

The weekend--purchase comparison supplies a useful contrasting result in
the same dataset. Both corrected MI estimates are approximately 0.0007 nats,
and the difference is about -0.000063. Wald gives p=0.9554 and Expanded Welch
p=0.9601, with only 2.18 degrees of freedom. A low degrees-of-freedom value
does not necessarily create a dramatic p-value or decision difference when
the shared statistic is already close to zero. Both tests do not reject;
neither establishes population equality.

## Other candidates

Adult provides a well-sampled contrast. Education--income and
occupation--income MI are lower in the Female-labelled records than in the
Male-labelled records. The corrected differences are -0.03714 and -0.04183
nats. Both full-data comparisons give extremely small p-values under either
method; their Expanded Welch degrees of freedom are approximately 1645 and
1850. This is useful for illustrating a practically unchanged decision when
the degrees of freedom are large. However, Adult is survey-derived, and the
current integer-count methods do not account for its survey design or weights.
The occupation table also has no Female-labelled Armed-Forces observations.
It is less suitable than Shoppers as the sole real-data illustration.

Student Performance provides a smaller-sample contrast: 423 GP-school and
226 MS-school Portuguese-course records. Studytime--grade-at-least-10 gives
p=0.1982 under Wald and 0.2339 under Expanded Welch, with 8.07 degrees of
freedom. Maternal-education--grade-at-least-10 gives p=0.8361 and 0.8468,
with 3.76 degrees of freedom. Neither comparison rejects, before or after
multiple-comparison adjustment. The data illustrate the calculations at
smaller sample sizes, but offer a weaker main application: the differences
are uncertain and within-class dependence is not modelled.

## What this adds and what it does not

All six full-data decisions agree between the methods: three rejections and
three non-rejections, unchanged by Holm adjustment. The exploration applies
the original methods to real count tables and shows when the numerical
adjustment does or does not affect an observed comparison. It does not
validate false-positive control, establish power or demonstrate superiority,
because the source populations' MI values are unknown. The repeated subsets
describe stability conditional on the recorded data, not independent
replications in a known population. MI contrasts also reflect different
category and outcome frequencies, not only a change in predictive usefulness.

Six full-data comparisons and 30 subset-size settings were retained. Each
size uses 5000 paired subsets, for 150000 subset table pairs. Both methods
receive identical tables within a pair. An independent formula audit checks
all full-data results and sampled checkpoints; every raw subset is regenerated
from its deterministic stream and its saved method outputs and summaries are
recomputed. Ten exploration tests pass. No thesis, working draft or method
implementation is changed.

Sources and attribution: [Online Shoppers, UCI](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset),
[Adult, UCI](https://archive.ics.uci.edu/dataset/2/adult), and
[Student Performance, UCI](https://archive.ics.uci.edu/dataset/320/student+performance).
All are CC BY 4.0; full attribution and preparation are in PROTOCOL.md.
The complete unrounded outputs and stability tables are in results/RESULTS.md
and its companion CSV files.
