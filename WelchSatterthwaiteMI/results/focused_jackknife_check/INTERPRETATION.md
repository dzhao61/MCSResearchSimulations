# Interpretation of the Focused Jackknife Diagnostic

## Question and Design

Does replacing the analytic leading bias correction with a delete-one
jackknife reduce unequal bias and wrong-direction rejections in the identified
sparse-table failure?

The four settings use the existing 16 by 16 copying populations. Both row and
column margins are (0.7, 0.3/15, ..., 0.3/15) for P and
(0.8, 0.2/15, ..., 0.2/15) for Q. I(P) is 0.02 nats; I(Q) is either 0.02 or
0.03 nats. The two samples have the same size, either 1,000 or 10,000.
Each setting uses exactly the original 20,000 independent simulated table
pairs. The jackknife replaces, rather than supplements, the analytic
correction. Neither estimate is clipped at zero.

The original per-sample delta-method standard error and two-sided normal
distribution cutoff are unchanged. This diagnostic tests the changed
estimate, not a jointly redesigned estimate and standard error. All rates
use all 20,000 repetitions; all calculations in these settings are valid.

## Main Findings

At n=1,000 under equal MI, the difference bias falls from 0.02960 to
-0.00116 nats. Under the -0.01-nat alternative, it falls from 0.03061 to
-0.00024 nats. The observed standard deviation rises modestly: from 0.01449
to 0.01521 under the null and from 0.01564 to 0.01638 under the alternative.
The root mean squared error of the difference falls substantially in both
settings, from 0.03295 to 0.01525 and from 0.03438 to 0.01638 nats,
respectively.

The improvement concerns the difference, not unbiased estimation of each MI.
Under the sparse null, the jackknife biases of the separate estimates are
0.03439 nats for P and 0.03555 nats for Q. Both estimates remain substantially
upward biased. Their similar biases largely cancel when the estimates are
subtracted. Under the alternative, the corresponding biases are 0.03452 and
0.03476 nats. This result therefore does not establish that the jackknife
removes sparse-table MI bias generally.

Under the sparse alternative, opposite-direction rejections fall from
2,009 to 5 out of 20,000 repetitions. Correct-direction rejections rise
from 1 to 544. The total rejection rate falls from 10.050% to 2.745%, because
the original rejections almost all indicated the wrong ordering of the two
population MI values. Comparing total rejection rates alone would hide
this improvement.

The changed numerator does not solve small-sample calibration. The sparse
null false-positive rate falls from 25.220% to 0.845%, below the nominal
5% rate. Its Wilson 95% Monte Carlo interval is 0.727%-0.982%. The mean
squared standard error remains 1.762 times the observed variance of the
jackknife difference under the null and 1.652 times that variance under the
alternative. The unchanged standard error still overstates the observed
variability on average.

At n=10,000, null rejection changes from 4.625% to 5.070%; the latter has a
Wilson 95% Monte Carlo interval of 4.774%-5.383%. The standard-error variance
ratios are 1.001 under the null and 0.991 under the alternative. However,
alternative detection falls from 69.920% to 66.190%, with all rejections
pointing in the correct direction for both estimators. Difference bias is
smaller after jackknife correction, but the observed standard deviation
and root mean squared error are slightly larger. It is not a uniform
improvement across sample sizes.

## Interpretation and Next Decision

This bounded check supports replacing unequal residual biases with more
similar residual biases as a way to improve these sparse MI differences.
It also separates two remaining issues: centering of the difference and
accuracy of its estimated uncertainty. Changing the numerator helps the
first, but does not automatically fix the second.

There is a useful, mixed finding here: dramatically fewer wrong-direction
rejections at n=1,000, conservative null rejection with the fixed standard
error, and a modest loss of detection at n=10,000. These four settings do
not establish performance across other table sizes, margins, constructions
or an entire detection curve. No further estimator or standard-error
experiment has been run, and the thesis has not been edited.

The subsequent manuscript addition reports this diagnostic in Appendix C.3,
with brief notes in Chapter 5 and Section 6.3.1. Chapters 3 and 4 and the
primary two-method comparison are unchanged. The preceding decision note
describes the experiment-only stage before that addition.

## Reproduction and Verification

From the repository root:

```sh
MPLCONFIGDIR=/private/tmp/welch-core-mpl .venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py preflight
MPLCONFIGDIR=/private/tmp/welch-core-mpl .venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py run
MPLCONFIGDIR=/private/tmp/welch-core-mpl .venv/bin/python WelchSatterthwaiteMI/experiments/run_focused_jackknife_check.py audit
```

The runner records the scope before computing outcomes. It regenerates the
original samples from their original chunk seeds and verifies every saved
baseline field for all 80,000 table pairs. It also compares 16 full-sized
jackknife estimates with an independent cell-weighted leave-one-out
calculation. Original inputs are hash-checked before and after the run.
The audit reproduces all diagnostic records and generated summaries.

`evidence.json` and the two summary CSV files include Monte Carlo intervals,
separate P and Q biases, observed variability, direction counts, validity and
paired contrasts. `verification.json` records the completed checks; the four
NPZ files retain per-repetition diagnostic outputs. The bootstrap used for
variance-ratio intervals resamples paired simulation outputs solely to
measure Monte Carlo uncertainty; it is not a bootstrap MI test.
