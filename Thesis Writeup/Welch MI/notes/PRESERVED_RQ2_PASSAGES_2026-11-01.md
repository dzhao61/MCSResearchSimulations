# Preserved RQ2 passages

Replaced by the user-authorised balanced null grid on 1 November 2026.
Original raw results, figures and table sources remain intact internally.

## Section 5.3

```latex
\section{RQ2: False-positive rates under equal MI}
\label{sec:null-design}

To measure false positives, we draw a count table from each of two
populations with equal MI in every repetition, so every rejection is
a false positive. Normal Wald and Expanded Welch use the
same bias-corrected MI difference and estimated standard error from
Chapter~\ref{chap:baselines}, but compare the resulting statistic with
different reference distributions. Normal Wald uses the standard normal
distribution, while Expanded Welch uses a Student \(t\) distribution
with MI-specific degrees of freedom estimated from the two sampled count
tables.

All reported simulation comparisons use equal sample sizes, so the two
leading MI bias corrections cancel from \(\Deltahat\), leaving the raw
plug-in MI difference. Residual biases can still differ between distinct
population tables, shifting the estimated difference away from its true
value even under equal population MI.

Both tests use a two-sided 5\% nominal test. The broad null comparison
uses the first grid in Table~\ref{tab:design-primary-grids}: common MI
0.02 nats, four table sizes, three margin regimes and ten sample sizes,
giving 120 settings. A false-positive rate above 5\% means excessive rejection, while a rate
below 5\% means conservative rejection. Because a rule that never rejects
has zero false positives and zero power, we assess nominal calibration
by closeness to 5\% and evaluate power separately.

We also report the fraction of valid results. Because invalid calculations
contribute no rejection to the all-repetition rate, failures can lower that
rate without improving the decisions made on usable samples.

```

## Section 6.2

```latex
\section{RQ2: False-positive rates under equal MI}

Under \(I(P)=I(Q)\), every rejection is a false positive. Both tests use
\(T=\Deltahat/\SEhat\), but Expanded Welch replaces Wald's standard normal
cutoff with a larger cutoff from the Student \(t\) distribution, reducing
rejection at the common nominal p-value threshold. We
therefore assess whether the reduction moves the rate towards the nominal
5\% level, and use the shared estimates to explain when it helps or
increases conservatism.

\subsection{Overall false-positive patterns}
\label{sec:null-rejection-patterns}

Table~\ref{tab:redesign-null-grid} summarises the comparison across
120 settings at common MI 0.02 nats. A setting is classified as improved
when Expanded Welch's false-positive rate is closer to 5\% than Wald's
by more than \RedesignGridTolerance{} percentage points, and worsened
when it is farther away by more than \RedesignGridTolerance{} percentage
points. Differences within this tolerance are grouped separately. The
rows distinguish settings where Wald starts above or below the target,
so a reduction in rejection can be assessed against its starting position.

\begin{table}[!htbp]
\centering
\caption{Change in distance from 5\% rejection across the broad null grid.}
\label{tab:redesign-null-grid}
\begin{tabular}{@{}lrrrr@{}}
\toprule
 & \multicolumn{3}{c}{Expanded Welch relative to Normal Wald} &\\
\cmidrule(lr){2-4}
\shortstack[l]{Normal Wald\\rejection rate} &
\shortstack{Closer\\to 5\%} &
\shortstack{Farther\\from 5\%} &
\shortstack{Within\\tolerance} & Total\\
\midrule
Above 5\% & \RedesignTowardAbove{} & \RedesignAwayAbove{} &
\RedesignWithinAbove{} & \RedesignTotalAbove{}\\
Below 5\% & \RedesignTowardBelow{} & \RedesignAwayBelow{} &
\RedesignWithinBelow{} & \RedesignTotalBelow{}\\
\midrule
Total & \RedesignToward{} & \RedesignAway{} & \RedesignWithin{} & 120\\
\bottomrule
\end{tabular}
\end{table}

Where Wald rejects too often, Expanded Welch moves closer to 5\% in
\RedesignTowardAbove{} of \RedesignTotalAbove{} settings, although
\RedesignAwayAbove{} reductions overshoot and leave the rate farther
from the target. Where Wald is already conservative, lowering rejection
cannot bring the rate closer to 5\%, so Expanded Welch either worsens
calibration or changes it by no more than the stated tolerance.

Each reported rate divides the number of valid rejections by all simulation
repetitions, counting invalid calculations as non-rejections, so the validity
fraction is reported separately to distinguish low rejection from a loss of
usable calculations. Brackets around rates and shading in rejection plots
give pointwise 95\% intervals for uncertainty from the finite simulation batch.

Figures~\ref{fig:redesign-null-uniform} and
\ref{fig:redesign-null-different} hold population MI at 0.02 nats and
increase the common sample size. Each panel compares Normal Wald with Expanded Welch at one table size,
with the black line marking 5\%.
The first figure uses uniform margins, whereas the second uses
\(m_k(0.7)\) for \(P\) and \(m_k(0.8)\) for \(Q\). Vertical scales differ between
panels, so comparisons between table sizes require the labelled rates.
The lower strips give the fraction of valid outputs for each method.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{focused_redesign_null_uniform.pdf}
\caption{False-positive rates under uniform margins.}
\label{fig:redesign-null-uniform}
\end{figure}

In the \(2\times2\) panel of Figure~\ref{fig:redesign-null-uniform}, both
rates fall into a deep trough and then recover towards 5\%, with Expanded
Welch more conservative over most of the range. These uniform-margin
settings use identical population tables, \(P=Q\), and equal sample
sizes, so the expected MI
estimation biases cancel in the difference. The trough therefore requires
an explanation through the standard error and the distribution of \(T\).
Because sampled tables with larger absolute MI differences also tend to
give larger standard errors, division by those denominators reduces the
extreme values of \(T\). This reduction in extreme statistics contributes to the low rejection
rate, which Expanded Welch's larger cutoff lowers further. The dependence weakens at larger sample sizes, allowing both rates to
recover, as shown by the diagnostics in
Section~\ref{sec:null-estimator-accuracy}.

In the \(4\times4\) panel, Wald initially rejects too often while Expanded
Welch is close to the target, before both rates fall below 5\% and then
recover. This reversal accompanies the average \(\SEhat^2\) moving from below
the observed variance of \(\Deltahat\) at small sample sizes to above
it over the conservative range. For a given difference estimate, a smaller
standard error increases \(|T|\), while a larger standard error decreases
it. The same increase in rejection cutoff therefore helps in the first
range and deepens conservatism in the second. With larger samples, the
squared standard error becomes more accurate and the methods approach 5\%.

In the \(8\times8\) panel, an early shoulder of excessive rejection is
followed by a later conservative trough and recovery. The shared squared
standard error initially underestimates the difference's sampling variance,
then overestimates it across the trough. The larger alphabet spreads
probability over more combinations, so the sampled tables require more
observations before these variance errors diminish. Expanded Welch reduces
the early excess but also lowers the conservative part of the curve. As in
\(4\times4\), its effect on calibration changes along the horizontal axis.

The \(16\times16\) panel has an additional rise between the early decline
and the later conservative trough. The average variance error also changes
direction more than once as the sampled tables fill: underestimation,
closer agreement, renewed underestimation and then overestimation accompany
the corresponding changes in rejection. Because the populations are identical, expected difference bias still
cancels, so the nonmonotonic curve reflects errors in the standard error
and the tails of \(T\), rather than a changing population difference. Expanded Welch lowers rejection throughout, but the methods become close
well before both rates settle near 5\%, so their agreement alone does not
establish accurate false-positive rates.

Under different-skew margins, \(I(P)=I(Q)\) in
Figure~\ref{fig:redesign-null-different}, but the population tables differ
and their expected MI estimation biases can therefore differ too.
The resulting bias in \(\Deltahat\) can shift the shared statistic away
from zero as well as changing its spread.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{focused_redesign_null_different_skew.pdf}
\caption{False-positive rates under different-skew margins.}
\label{fig:redesign-null-different}
\end{figure}

In the different-skew \(2\times2\) panel, Wald remains below 5\%
throughout the grid, so Expanded Welch's reduction mainly increases
conservatism. Both methods again have a trough and recovery, retaining
the small-table pattern seen under uniform margins despite the changed
margins. As the shared estimates improve, both rates recover towards 5\%, while
the increasing degrees of freedom bring Expanded Welch's cutoff closer
to Wald's.

In \(4\times4\), Wald starts above the target and then falls below it,
while Expanded Welch lowers both regions. The average squared standard error
moves from underestimating to overestimating the observed difference
variance, helping explain the fall into the trough. As that overestimation
diminishes, both rates rise towards 5\%. At \(n=10\), the first Expanded Welch rate is close to 5\% even though
only about three quarters of calculations are valid. Its
apparent closeness at that point therefore includes repetitions recorded
as non-rejections because the calculation failed.

The \(8\times8\) panel begins with much greater over-rejection than its
uniform counterpart. Expanded Welch initially rises as its validity and
cutoff change, then both methods fall below 5\% before recovering.
The diagnostics show that positive bias moves the centre of
\(\Deltahat\) away from zero, while overestimation of \(\SEhat^2\)
in the intermediate range tends to reduce \(|T|\). At \(n=100\), both effects are present even though Expanded
Welch brings the rate closer to 5\%. As the bias diminishes, the remaining
variance overestimation accompanies the conservative trough. The larger
cutoff deepens that trough before the shared estimates recover. A rate
close to the target at an intermediate point can therefore reflect the
combined effects of errors rather than accurate estimation of each input.

In the \(16\times16\) panel, both methods severely over-reject across
several intermediate sample sizes. Here the bias in \(\Deltahat\) grows relative to its sampling SD,
shifting the statistic away from zero (see
Section~\ref{sec:null-estimator-accuracy} for the comparison with the
unbiased same-skew case). The squared standard error is also too large
on average over part of this range, but that compensating effect does
not remove the large displacement. Expanded Welch changes the cutoff
without changing the displaced difference estimate, so its reduction in
rejection leaves substantial over-rejection. With larger samples, bias diminishes and both rates fall towards 5\%.

The validity strips separate early calculation failures from these later
patterns. Under uniform margins, appreciable losses are concentrated in the smallest
\(2\times2\) samples, whereas under different skew several table sizes
lose outputs at the smallest sample sizes. Across the full
120-setting grid, the minimum valid fractions are 0.958 for Normal Wald
and 0.631 for Expanded Welch. The conservative troughs in \(4\times4\)
and larger tables, and the different-skew \(16\times16\) plateau,
persist after validity is complete, so those patterns require explanations
through the estimates and statistic.

At the largest sample size in both figures, both tests' rates are close
to 5\% across the table sizes. More accurate cell frequencies reduce the
bias and variance errors entering the shared statistic, while larger
estimated degrees of freedom bring Expanded Welch's cutoff towards Wald's.
The curves consequently approach one another and the nominal target in
these settings.

\FloatBarrier

\subsection{Bias and standard-error accuracy}
\label{sec:null-estimator-accuracy}

RQ1 examined the moments of \(\Vhat(P)\) and \(\Vhat(Q)\) needed to
choose degrees of freedom. For the shared statistic, we now separately check whether \(\Deltahat\)
is centred on the population difference and whether \(\SEhat^2\)
describes its sampling variance.
At small sample sizes, \(V(P)/n_P\) can itself understate MI sampling
variance because it includes only linear sampling error. Consequently,
\(\Vhat(P)/n_P\) can exceed that population approximation while still
falling below the actual sampling variance of the MI estimate.

Table~\ref{tab:redesign-shared-estimates} calculates both diagnostics
across the evaluation repetitions. ``Bias / SD'' divides
\(\E(\Deltahat)-\Delta\) by the observed sampling SD of \(\Deltahat\),
so it measures displacement relative to the spread of the estimates.
The variance ratio divides the average \(\SEhat^2\) by the observed
\(\Var(\Deltahat)\): values below one indicate underestimation of
sampling variance, and values above one indicate overestimation. The
observed variance is measured about the sampling mean, so this ratio
can be close to one even when the difference is biased.
The table compares the selected null settings A, uniform \(4\times4\) with \(n=20\);
B, different-skew \(8\times8\) with \(n=100\); and C,
different-skew \(4\times4\) with \(n=10{,}000\), together with the sparse
\(16\times16\) cases at \(n=1{,}000\). All use equal sample sizes
and common MI 0.02 nats.

\begin{table}[!htbp]
\centering
\caption{Bias and standard-error accuracy at selected equal-MI settings.}
\label{tab:redesign-shared-estimates}
\input{figures_rewrite/focused_redesign_shared_estimates}
\end{table}

Table~\ref{tab:redesign-case-rates} gives rejection rates for the same
five settings, followed below the divider by the same \(16\times16\)
populations at \(n=10{,}000\). Each rate divides valid rejections by all 100,000 repetitions and is
reported with a pointwise 95\% interval. Both tests are valid in every
repetition at these seven settings.

\begin{table}[H]
\centering
\small
\setlength{\tabcolsep}{4pt}
\caption{Null rejection rates with pointwise 95\% intervals.}
\label{tab:redesign-case-rates}
\input{figures_rewrite/focused_redesign_cases_rates}
\end{table}

At A, difference bias is negligible, but the average \(\SEhat^2\) is
below the observed \(\Var(\Deltahat)\), tending to enlarge \(|T|\)
and accompanying Wald's excessive rejection.
Expanded Welch's larger cutoff brings the rate close to 5\%.
At B, \(\Deltahat\) is biased upwards while \(\SEhat^2\) overestimates
its sampling variance. The upward displacement tends to increase
rejection, whereas the larger denominator tends to reduce it. Expanded Welch lowers
rejection further but remains above 5\%, so its improvement occurs with
different input errors from those at A. At C,
bias is negligible and the variance ratio is close to one, accompanying
rates close to 5\% for both methods.

The same margins and sample sizes need not give the same calibration at
stronger association. Table~\ref{tab:redesign-stronger-null} retains
A's and B's margins, table sizes and sample sizes while increasing their
common population MI. Rates and their pointwise 95\% intervals are
percentages of all 100,000 repetitions.

\begin{table}[H]
\centering
\small
\caption{False-positive rates at stronger common MI.}
\label{tab:redesign-stronger-null}
\input{figures_rewrite/focused_redesign_stronger_null}
\end{table}

At A, increasing the common MI raises both rejection rates well above
their values at MI 0.02, and Expanded Welch no longer brings rejection
close to 5\%. At B, Wald's rate changes little, but Expanded Welch's
earlier reduction becomes much smaller. Both methods over-reject at both stronger-MI settings even though the
larger cutoff still lowers rejection. The improvement at MI 0.02 is
therefore specific to that tested population pair rather than a property
of its table dimensions and sample size alone.

The sparse different-skew case shows why changing the cutoff cannot
resolve a displaced difference estimate. At \(16\times16\) and
\(n=1{,}000\), the difference bias is about 0.030 nats, or 2.06 observed
SDs. Under the equal-MI null, its sampling centre
\(\E(\Deltahat)=\Delta+\Bias(\Deltahat)\) becomes
\begin{equation}
 \E(\Deltahat)\approx 0+0.02985=0.02985\text{ nats}.
 \label{eq:redesign-null-bias-shift}
\end{equation}
With an observed SD of approximately 0.01450 nats, this positive shift
places the sampling distribution largely above zero and moves most
rejections into the positive tail despite a zero population difference.
Expanded Welch leaves this centre unchanged, so both tests reject far too often.

The same-skew \(16\times16\) case has almost the same variance ratio
but rejection far below 5\%. Under equal MI, the expected estimation
biases cancel in the difference because the population tables and sample
sizes are identical. Its average
\(\SEhat^2\) exceeds the observed \(\Var(\Deltahat)\), shrinking
\(|T|\) without a large bias shifting the estimates away from zero.
Under different skew, that variance overestimation coexists with the
large positive bias, and rejection instead remains excessive. Thus the
similar variance ratios in Table~\ref{tab:redesign-shared-estimates}
can accompany rates on opposite sides of 5\% in
Table~\ref{tab:redesign-case-rates}. At \(n=10{,}000\), both skew
regimes have rejection rates closer to 5\%.

For the identical uniform-margin populations, expected difference bias
cancels, while changes in the average \(\SEhat^2\) below or above the
observed \(\Var(\Deltahat)\) tend to enlarge or reduce \(|T|\), respectively. These changes accompany the repeated
crossings in the \(16\times16\) panel of
Figure~\ref{fig:redesign-null-uniform}. The estimates recover at
different rates as sparse tables fill, so increasing sample size need
not improve rejection monotonically.

The \(2\times2\) trough also involves how the numerator and denominator
move together within repetitions. Larger absolute MI differences tend
to occur with larger standard errors, so division suppresses the
extreme values that would otherwise cause rejection. Consequently,
rejection can be far below 5\% even when the average \(\SEhat^2\)
is fairly close to the observed difference variance. Beyond the trough,
this dependence weakens and the tails of \(T\) move closer to the
normal approximation. The Spearman rank correlation between
\(|\Deltahat-\operatorname{mean}(\Deltahat)|\) and \(\SEhat\),
calculated over repetitions with both quantities finite, falls from
0.656 at \(n=50\) to 0.167 at \(n=1{,}000\).
Together these checks explain the broad patterns
without isolating every finite-sample contribution to rejection.

```

## RQ2 conclusion

```latex
\subsection{RQ2: False-positive rates under equal MI}

At common MI 0.02 nats, Expanded Welch brings false-positive rates
closer to 5\% at A (uniform \(4\times4\), \(n_P=n_Q=20\)) and
B (different-skew \(8\times8\), \(n_P=n_Q=100\)), as defined in
Table~\ref{tab:redesign-shared-estimates}. Both tests
return valid results
in every repetition at these settings, so the lower rejection rates
reflect the larger cutoff from the Student \(t\) distribution. Across the broad grid, Expanded Welch also lowers rates that are already
below 5\%, increasing conservatism. The larger cutoff therefore helps
when it corrects excessive rejection but worsens calibration when
rejection is already too infrequent.

A false-positive rate near 5\% does not establish that the estimated
component degrees of freedom match their sampling-moment targets.
At A, the average \(\SEhat^2\) is below the observed
\(\Var(\Deltahat)\), while the low estimated degrees of freedom
increase the rejection cutoff, so the two errors can compensate in the
false-positive rate. At B, the average squared standard error exceeds the observed
variance of the MI difference and the difference is biased, so the same
explanation does not apply unchanged.

In the sparse same-skew null, identical population tables at equal sample
sizes have the same expected MI estimation bias, so that bias cancels
in the difference. The average \(\SEhat^2\) is nevertheless almost
twice the observed \(\Var(\Deltahat)\) in the sparse copying case,
and both tests are conservative. Unequal sample sizes can also leave unequal residual biases
in otherwise identical populations.

Under different-skew margins, the large positive bias in the estimated
MI difference instead accompanies excessive rejection by both tests in
the sparse \(16\times16\) null comparison
(Section~\ref{sec:null-estimator-accuracy}).

```
