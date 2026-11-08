# Preserved focused and calibrated power passages

Removed from the submitted manuscript under the user-authorised fixed-gap
power redesign on 1 November 2026. Original code, results and figures remain
available internally. This is a preservation record, not active manuscript text.

## chapters_rewrite/05_experimental_design.tex

```latex
\section{RQ3: Nominal and calibrated power}

Power is the probability of rejecting equal MI when the population MI
values differ. We first compare power using the nominal 5\% cutoffs.
A test that rejects less often under equal MI can also reject less often
under alternatives, so we then compare power after adjusting the cutoffs
to match rejection at a specified equal-MI setting.

The focused comparison uses settings A--C in
Table~\ref{tab:redesign-focus-settings}. Earlier simulations identified
A and B as settings where Expanded Welch brought false-positive rates
closer to 5\%; their power is evaluated on new independent samples.
Setting C provides a larger-sample comparison.

To choose the MI differences for a power curve, we first measure the
sampling variation under equal MI. An independent null simulation estimates the standard deviation (SD) of
the corrected MI difference, giving the fitted value \(\sigma_0\). Measuring differences in units
of \(\sigma_0\) makes the three curves comparable relative to their null
sampling variation.

\begin{table}[!htbp]
\centering
\caption{Focus settings for the power comparison; common null MI is 0.02 nats.}
\label{tab:redesign-focus-settings}
\begin{tabular}{@{}llrlr@{}}
\toprule Setting & Margins & \(n_P=n_Q\) & Size & \shortstack{Fitted null SD\\\(\sigma_0\) (nats)}\\\midrule
A & Uniform & 20 & \(4\times4\) & 0.154967\\
B & Different skew & 100 & \(8\times8\) & 0.065138\\
C & Different skew & 10,000 & \(4\times4\) & 0.003175\\
\bottomrule
\end{tabular}
\end{table}

\begin{samepage}
For each curve, we hold \(I(P)=0.02\) nats and increase \(I(Q)\) so
that the population MI values are separated by \(h\) fitted null SDs.
The populations satisfy
\begin{equation}
\begin{aligned}
 I(P)&=0.02,\qquad I(Q)=0.02+h\sigma_0,\\
 h&\in\{0,0.5,1,1.5,2,2.5,3,3.5,4\},\\
 \Delta&=I(P)-I(Q)=-h\sigma_0.
\end{aligned}
\label{eq:design-focused-populations}
\end{equation}
\end{samepage}
Thus \(h=0\) gives equal MI, while positive \(h\) gives larger MI in
\(Q\) and a negative signed difference. For example, at C, two null SDs are approximately
\(2(0.003175)=0.00635\) nats, giving an alternative with
\(I(P)=0.02\), \(I(Q)\simeq0.02635\) and
\(\Delta\simeq-0.00635\) nats. The fitted SD and the resulting population
tables stay fixed during evaluation. Appendix~\ref{app:construction}
gives their construction and the fixed SD values.

\medskip
\thesisminiheading{Power after matching null rejection.}

Empirical calibration chooses a separate p-value threshold for each
test through the following procedure for each full power curve:
\begin{enumerate}
 \item Use the independent fitting samples with \(I(P)=I(Q)=0.02\) nats,
 retaining the curve's margins, table size and sample sizes.
 \item Choose each rule's threshold to give at most 5\% rejection in
 that fitting batch, and hold it fixed across the curve.
 \item Apply the thresholds to separate equal-MI evaluation samples and
 to the alternative samples, measuring the achieved false-positive rates
 and power.
\end{enumerate}
The thresholds are fitted for these known simulation settings, where
calibrated power compares the tests after matching false-positive rates.

Normal Wald ranks simulated datasets by \(|T|\): larger \(|T|\) always
gives a smaller p-value and stronger evidence against equal MI.
Expanded Welch's p-value also depends on degrees of freedom that change
with the sampled tables, so it can rank the datasets differently.
At a common p-value threshold, its rejections are a subset of Wald's.
Calibration fits a separate threshold for each test, so that earlier
nesting no longer determines which test has greater power.

\medskip
\thesisminiheading{Changing the calibration setting.}

Equal MI can occur at different common MI values. To examine how that
choice affects the power comparison, we repeat calibration at \(h=2\)
and \(h=4\) for A--C using the two equal-MI settings in
Table~\ref{tab:design-calibration-populations}.

Both calibration nulls retain the alternative's margins and sample
sizes, but the lower null sets both MI values to the alternative's smaller
value, whereas the upper null sets both to its larger value.

\begin{table}[!htbp]
\centering
\caption{The alternative and two calibration nulls; MI values are in nats.}
\label{tab:design-calibration-populations}
\begin{tabular}{@{}lll@{}}
\toprule
Scenario & \(I(P)\) & \(I(Q)\)\\
\midrule
Fixed alternative & \(0.02\) & \(0.02+h\sigma_0\)\\
Lower null & \(0.02\) & \(0.02\)\\
Upper null & \(0.02+h\sigma_0\) & \(0.02+h\sigma_0\)\\
\bottomrule
\end{tabular}
\end{table}

Independent upper-null batches fit and validate the new cutoffs. We apply
both calibrations to the same alternative simulation outputs, so any
change in measured power comes from the cutoffs rather than a change of alternative samples.
We also evaluate each calibration at both null settings because matching
rejection at one equal-MI setting does not ensure the same false-positive
rate elsewhere under equal MI. Appendix~\ref{sec:calibration-sensitivity-design} gives
the construction and uncertainty calculation.
```

## chapters_rewrite/06_results.tex

```latex
\section{RQ3: Nominal and calibrated power}

The power comparison uses A (uniform \(4\times4\), \(n_P=n_Q=20\)),
B (different-skew \(8\times8\), \(n_P=n_Q=100\)) and C
(different-skew \(4\times4\), \(n_P=n_Q=10{,}000\)). For each setting,
\(\sigma_0\) is the independently fitted SD of \(\Deltahat\) under
\(I(P)=I(Q)=0.02\) nats. We hold \(I(P)=0.02\) and increase \(I(Q)\),
so the true difference \(\Delta=I(P)-I(Q)\) becomes negative. Moving right along the horizontal axis, \(-\Delta/\sigma_0\), from the
equal-MI null at zero therefore gives \(Q\) a larger MI advantage in
fitted null SD units.

Nominal power uses each test's usual p-value threshold of 0.05, whereas
calibrated power uses separately fitted thresholds that target 5\%
rejection at a specified equal-MI population pair. The two comparisons use the same
alternative samples, allowing us to examine the effect of changing the
rejection thresholds.

\subsection{Nominal power}

Figure~\ref{fig:redesign-power} gives both tests' rejection fractions
from the same sampled pairs of tables at each alternative in the three
focus settings (Table~\ref{tab:redesign-focus-settings}). At zero on the horizontal axis, the curves give their different
false-positive rates relative to the black 5\% line, whereas at positive
values they give power against increasing MI differences. Expanded Welch has lower nominal power at the selected small-sample
settings A and B, accompanying its lower null rejection rates.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{focused_redesign_power.pdf}
\caption{Nominal power across differences measured in fitted null standard deviations.}
\label{fig:redesign-power}
\end{figure}

In panel A of Figure~\ref{fig:redesign-power}, both power curves rise
as the MI advantage of \(Q\) increases. Increasing \(I(Q)\) moves the
sampling centre of \(\Deltahat\) farther below zero, so more repetitions
have a negative statistic large enough in magnitude to cross the rejection
boundary. Expanded Welch requires a larger \(|T|\) and consequently
rejects fewer of those repetitions than Wald. The gap is greatest over
the middle of the curve, where more sampled statistics lie between the
two boundaries. At stronger alternatives, the power gap narrows as more statistics cross
both boundaries and larger estimated degrees of freedom lower the cutoff
from the Student \(t\) distribution.

In panel B, rejection initially falls even though the population MI
values move farther apart, then rises at stronger alternatives. This dip
occurs because \(\Deltahat\) has positive estimation bias at the first
alternatives. The increasingly negative true difference initially offsets
that bias and moves the sampling mean towards zero, reducing positive-tail
rejections. Once the negative difference becomes sufficiently large,
negative-tail rejections increase and power rises. Expanded Welch changes
the cutoff without removing this movement of the shared sampling centre,
so both methods retain the dip. Farther along the curve, B remains the least powerful setting because
positive bias still offsets part of the true negative difference, while the observed SD of \(\Deltahat\) grows
relative to its null value, reaching approximately \(1.70\sigma_0\)
at four null SDs. The sampled differences are therefore less
separated from zero relative to their spread.

In panel C, both power curves rise steeply and nearly overlap, eventually
exceeding A's as well as B's. This rise occurs with negligible bias and
a smaller relative change in sampling SD along the alternative path.
As \(I(Q)\) increases, the sampling centre therefore moves below zero
without the offsetting bias seen at B. The near-overlap occurs because
the large estimated degrees of freedom make the cutoff from the Student
\(t\) distribution close to the standard normal cutoff. Comparing
panels at the same \(-\Delta/\sigma_0\) matches the difference in null
SD units, but each alternative can still have a different bias and
sampling variance. Those differences help explain why the common
horizontal scale does not produce identical power curves.

\FloatBarrier
\subsection{Power after matching false-positive rates}

At A and B, Expanded Welch's lower nominal power accompanies a lower
false-positive rate than Wald's, so we use empirical calibration to
compare power after matching rejection to approximately 5\% at a
specified equal-MI setting. Independent equal-MI simulations fit a
separate p-value threshold for each test, replacing the usual threshold
of 0.05. We then hold those thresholds fixed,
evaluate their false-positive rates on independent null samples, and
apply them to the alternative samples used in the nominal comparison.
Changing the rejection thresholds leaves \(\Deltahat\), \(\SEhat\)
and the calculated p-values unchanged.

Separately fitted thresholds can reverse the nominal ordering because the
two methods can rank sampled datasets differently. Wald's p-value depends
only on \(|T|\), while Expanded Welch's also depends on the estimated
degrees of freedom, so two datasets with similar \(|T|\) can receive
different relative rankings when their degrees of freedom differ. Although the nominal nesting of rejections holds at a common p-value
threshold, separate calibration allows either method to reject samples
that the other retains, permitting a different power ordering.

With thresholds fitted at \(I(P)=I(Q)=0.02\) nats, both tests reject
between 4.93\% and 4.99\% on independent null evaluation samples across
A--C. Figure~\ref{fig:redesign-calibrated-power} applies these thresholds
to the same alternative samples as Figure~\ref{fig:redesign-power}, with
bands showing bootstrap uncertainty. The figure shows the closely matched false-positive rates at zero and
calibrated power as the MI advantage of \(Q\) increases.

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{focused_redesign_power_calibrated.pdf}
\caption{Power after calibration at common MI 0.02; bands show bootstrap uncertainty.}
\label{fig:redesign-calibrated-power}
\end{figure}

In panel A of Figure~\ref{fig:redesign-calibrated-power}, Expanded Welch
now has higher power over the alternatives shown, reversing the nominal
ordering. Calibration mainly lowers Wald's curve because its nominal
false-positive rate was above 5\%, whereas Expanded Welch's was already
close to the target. After this adjustment, the different rankings of
sampled datasets give Expanded Welch more rejections under the alternatives.
Its advantage grows over the middle of the curve and narrows slightly
at the largest difference.

In panel B, both calibrated curves lie below their nominal counterparts
because both nominal false-positive rates exceeded 5\%. Expanded Welch
now has greater power at positive horizontal-axis values, with a larger
advantage at stronger alternatives. Both curves nevertheless retain the initial dip because fitting a
threshold changes which p-values cause rejection but leaves the biased
\(\Deltahat\) and its movement towards zero unchanged. Reversing the method ordering therefore does not resolve this
distortion in the shared statistic.

In panel C, calibration changes little because both nominal false-positive
rates were already close to 5\%, and the curves continue to overlap as
they rise steeply towards high power. At stronger alternatives, C remains
the most powerful setting and B the least powerful, consistent with their different
bias and sampling-variation patterns. Matching null rejection at zero
does not make those alternative sampling distributions the same.

\medskip
\thesisminiheading{Does the calibration setting change the comparison?}

The preceding comparison matches false-positive rates at common MI 0.02,
but the null hypothesis requires only equality of the two MI values
without specifying their common value. Changing that value can change
the sampling distribution of the statistic and estimated degrees of
freedom, and hence the thresholds needed for 5\% rejection. We therefore
check whether Expanded Welch's calibrated power advantage persists when
we change the equal-MI populations used to fit the thresholds.

For each alternative with \(I(P)=0.02\) and \(I(Q)>0.02\),
\emph{lower-null calibration} fits both tests at
\(I(P)=I(Q)=0.02\), the alternative's smaller MI.
\emph{Upper-null calibration} instead uses the alternative's larger
\(I(Q)\) as the common MI, with both fitting settings retaining the
alternative's margins and sample sizes. After fitting a
separate threshold for each test at each null, we apply the two
calibrations to the same fixed alternative samples, so any change in
power arises from the thresholds rather than a change in the alternative data.

Here \(h=(I(Q)-I(P))/\sigma_0=-\Delta/\sigma_0\) measures the population
MI gap in fitted null SDs, where \(\sigma_0\) is the fitted SD of
\(\Deltahat\) under \(I(P)=I(Q)=0.02\).
Table~\ref{tab:redesign-calibration-sensitivity} reports Expanded Welch
power minus Normal Wald power at \(h=2\) and \(h=4\).
Differences are expressed in percentage points, with positive values
favouring Expanded Welch and negative values favouring Wald. The upper-MI column gives the
common MI used for upper-null fitting. Brackets give 95\% bootstrap
intervals accounting for the shared evaluation data and uncertainty in
the fitted thresholds.

\begin{table}[H]
\centering
\small
\setlength{\tabcolsep}{3pt}
\caption{Expanded Welch minus Wald power under two null calibrations.}
\label{tab:redesign-calibration-sensitivity}
\input{figures_rewrite/focused_redesign_calibration_sensitivity}
\end{table}

Under lower-null calibration, the gains at A and B increase from two to
four null SDs. Changing the fitting populations reverses the gain in two
comparisons: at A and two null SDs, the 3.58-point gain becomes a 0.76-point
loss; at B and four SDs, the 3.92-point gain becomes a 0.39-point loss.
The alternative data are identical within each comparison, so these
reversals arise from the changed thresholds. Under upper-null calibration,
A at four SDs retains a small positive estimate whose interval includes
zero, while B at two SDs retains a much smaller gain. At C, both
calibrations give differences well within the one-percentage-point
tolerance. The apparent power advantage is therefore sensitive to the
fitting null, particularly at the smaller-sample settings.

Table~\ref{tab:redesign-calibration-validation} checks whether the
thresholds that give about 5\% false positives at one null also do so
at the other, using the equal-MI populations at A and two null SDs. The lower evaluation null has common MI 0.02 nats, while the upper null
sets both MI values to 0.3299 nats, the larger MI in the fixed alternative. Each row applies the thresholds fitted at the named null to independent
samples from the evaluation null, with rates calculated over all 100,000
validation repetitions.

\begin{table}[H]
\centering
\small
\caption{Null rejection rates at A under both calibrations.}
\label{tab:redesign-calibration-validation}
\begin{tabular}{@{}llrr@{}}
\toprule
Fitting null & Evaluation null & Normal Wald & Expanded Welch\\
\midrule
Lower & Lower & 4.93\% & 4.99\%\\
Lower & Upper & 11.20\% & 13.71\%\\
Upper & Upper & 4.87\% & 4.84\%\\
Upper & Lower & 1.63\% & 0.79\%\\
\bottomrule
\end{tabular}
\end{table}

Both calibrations give rates close to 5\% at the null used for fitting,
but their thresholds transfer differently to the other null. Lower-null
calibration produces excessive rejection at the upper null, with a
higher rate for Expanded Welch than for Wald, whereas upper-null
calibration makes both tests conservative at the lower null.
The power gain and its reversal therefore accompany changes in the
relative false-positive rates at another common MI. Matching rejection
at one population pair does not establish that either test keeps
rejection at or below 5\% throughout the equal-MI null, so the calibrated
power comparison remains conditional on its fitting null.
```

## chapters_rewrite/07_conclusions.tex

```latex
\subsection{RQ3: Nominal and calibrated power}

At the selected small-sample settings A and B, Expanded Welch has lower
nominal power than Normal Wald alongside lower false-positive rates.
The calibrated comparison therefore adjusts their cutoffs to match
rejection at a specified equal-MI setting before comparing power.
After calibration at common MI 0.02 nats, Expanded Welch has higher power
at the reported two- and four-null-SD alternatives for A and B.
Moving calibration to the upper equal-MI setting while holding the
alternative fixed reverses the gain at A and two null SDs, and at B and
four null SDs (Table~\ref{tab:redesign-calibration-sensitivity}).
At the larger-sample setting C (different-skew \(4\times4\),
\(n_P=n_Q=10{,}000\)), nominal power differences are small and calibrated
differences remain practically small under both calibrations.

Expanded Welch's sample-dependent degrees of freedom can change the
ordering of sampled datasets by their p-values, allowing higher calibrated
power than Normal Wald. However, the null validation in
Table~\ref{tab:redesign-calibration-validation} shows that matching
false-positive rates at the lower common MI does not ensure matching at
the upper common MI.

Changing the cutoff leaves errors in the estimated MI difference
unchanged, so calibration does not remove the initial power dip at B.
At the first alternatives, the increasingly negative true difference
partly cancels the persistent positive estimation bias, moving the
sampling mean of \(\Deltahat\) towards zero. Rejection therefore
initially falls even though the population MI values move farther apart.

The observation-level sensitivity supplies an MI-specific basis for
choosing the cutoff from the Student \(t\) distribution, while the
simulations distinguish errors in the degrees-of-freedom approximations
from errors in the shared statistic. Expanded Welch improves
false-positive rates in selected tested settings, but its larger cutoff
also increases conservatism where rejection is already too infrequent,
and its calibrated power gains depend on the fitting null. The evidence
therefore supports these setting-specific improvements rather than a
general replacement of Normal Wald.
```

## appendices_rewrite/B_population_construction.tex

```latex
\section{Empirical calibration and power uncertainty}
\label{sec:calibration-sensitivity-design}

Calibration follows the fitting and independent evaluation steps in
Chapter~\ref{chap:design}. For Expanded Welch, assign invalid fitting
outputs p-value one and sort the fitting p-values. Set the threshold to
the \((\lfloor0.05M\rfloor+1)\)th smallest value, rejecting only
strictly smaller evaluation p-values. Ties at the boundary are excluded.
Normal Wald uses the equivalent upper-tail threshold for \(|T|\), with
invalid fitting values below all valid absolute statistics. This gives
at most 5\% rejection in the fitting batch; independent null evaluation
measures the achieved rate, including discreteness.

The calibration-sensitivity comparison uses the lower and upper nulls in
Table~\ref{tab:design-calibration-populations} at \(h=2,4\) for A--C.
For each upper null, solve for the copying probability with the original
margin vectors, dimensions and sample sizes. Generate 100,000 independent
fitting repetitions and 100,000 validation repetitions for each of these
six equal-MI settings. Apply both calibrations to the same original alternatives and
to both null validation settings. Invalid outputs remain non-rejections.

All calibrated-power intervals use 1,000 joint bootstrap repetitions.
For each full curve, share one lower fitting resample across its points.
For the sensitivity comparison, share one lower fitting resample across
the two alternatives within each focus setting. Independently resample
each upper fitting batch and refit the cutoffs. At each evaluation point,
resample the tests' joint decisions; in the sensitivity comparison, retain
both calibrations in that joint resample. This preserves dependence between
methods and between calibrations when estimating power differences and
changes in those differences. Population tables and effect sizes stay fixed.

Use the 2.5th and 97.5th percentiles for pointwise intervals of rates and
paired differences, comparing the latter with the practical tolerance of
minus one to plus one percentage point. Cross-null rates use Wilson
intervals conditional on the fitted cutoffs, quantifying validation
sampling uncertainty only. These checks concern the two specified null
settings.
```
