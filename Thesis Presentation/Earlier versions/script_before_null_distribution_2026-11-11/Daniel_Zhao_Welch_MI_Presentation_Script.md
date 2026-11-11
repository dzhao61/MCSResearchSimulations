# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, measures how much knowing one variable reduces uncertainty about another, on average. If knowing X changes the probabilities we'd assign to Y's categories, X gives us information about Y. MI averages that information over possible outcomes, giving zero when the variables are independent and a positive value when they're associated.

The hypotheses below that definition compare two populations, whose joint probability tables I'll call P and Q. The null says their population MI values are equal, while the two-sided alternative says they differ in either direction.

The diagram on the left shows how we estimate those values. We take a sample from P, summarise its categorical observations in a count table, and calculate an MI estimate. We repeat that for Q, using the same definitions of X and Y.

The task on the right brings those estimates together. After forming the count tables and estimating MI, we assess whether sampling noise can explain the difference. New samples produce different counts and estimates, so the question at the bottom requires a statistical test rather than just comparing two numbers.

## Slide 3: Literature review: foundations and the MI-specific step

The three columns separate the foundations of that test.

The left column concerns MI estimation and uncertainty. Existing work provides an MI estimator, a leading bias correction, and a first-order sampling-variance approximation. The remaining step listed below is to track how much the variance estimate itself changes between samples.

The middle column is the Wald comparison. It divides an estimated difference by its estimated standard error and uses the standard normal distribution as its reference. Here, we assess how well that fixed cutoff works with finite samples.

The right column introduces Welch–Satterthwaite moment matching. It uses the mean and variability of estimated variance contributions to choose degrees of freedom, with related applications to entropy and regression. Applying that principle to MI requires an MI-specific calculation of variance sensitivity.

That is the contribution stated at the bottom: I derive the sensitivity needed for the degrees of freedom, then evaluate the resulting comparison. The two methods share their estimated MI difference and standard error, which lets us study the effect of changing the reference distribution.

## Slide 4: Method: one statistic, two reference distributions

The shared-statistic box on the left shows that common calculation. The numerator is the estimated MI difference after a leading bias correction, and the denominator is its estimated standard error. A statistic of two means the difference is twice that standard error; its sign identifies the higher MI estimate, while the two-sided test uses its magnitude.

The second equation explains the standard error. Pointwise MI is a category pair's information contribution, and V-hat estimates the variance of those contributions. Dividing by sample size estimates the sampling variance of MI. Independence between the two samples lets us add their variance contributions to get the squared standard error.

The blue box below gives the Wald rule: compare the statistic with the standard normal distribution, using a two-sided 5% cutoff of about 1.96.

The orange box gives the Expanded Welch rule. It uses a Student t distribution with degrees of freedom estimated from the tables, intended to account for uncertainty in the variance estimates.

The graph on the right illustrates the resulting cutoff difference. The illustrated Student t distribution has five degrees of freedom and heavier tails, giving a larger cutoff of about 2.57. Five is illustrative: the actual estimated value changes between samples. Smaller degrees of freedom give a larger cutoff; as they increase, it approaches Wald's.

Under the implemented rules, Expanded Welch therefore only rejects where Wald also rejects. The next calculation determines how we choose those degrees of freedom.

## Slide 5: Approach and contribution

The derivation chain runs from left to right. Its purpose is to approximate how V-hat varies between samples. V describes variation in pointwise MI across outcomes, while V-hat estimates V from a sampled table.

In the first box, I move a small amount of probability towards one cell, reducing the other probabilities proportionally. This provides a controlled way to measure the effect of one possible outcome.

The second box tracks what changes with it. The cell weights, row and column margins, and pointwise-MI log ratios all change together. For example, a changed row total affects log ratios elsewhere in that row, so holding the pointwise-MI values fixed would miss part of the effect.

The third box defines the combined sensitivity, g. For a fixed population and cell, g is fixed: a positive value means the change initially raises V, and a negative value means it lowers V. Drawing a random outcome X and Y selects a cell's sensitivity, making g evaluated at X and Y a random quantity.

The fourth box uses the spread of those sensitivities. I call their variance tau-squared; greater spread means a different mix of sampled outcomes can make V-hat less stable.

The first equation below approximates the sampling variance of V-hat by tau-squared divided by sample size. The second substitutes the observed V-hat and estimated tau-squared into the component degrees-of-freedom formula. We repeat the calculation for Q and combine the components using Welch–Satterthwaite.

The panel on the right identifies two approximations behind those equations. First, the sampling expansion approximates V-hat's error by the average of the observation-level sensitivities. Their mean is zero, so V-hat's first-order sampling mean is V. Independence gives the variance of their average as tau-squared divided by sample size.

Second, moment matching fits a scaled chi-squared distribution to the approximated mean and variance. Greater variability relative to the mean gives fewer degrees of freedom. The derivative defining g is exact for positive population tables, but these sampling and distributional approximations require evaluation.

## Slide 6: Evaluation design

The research questions on the left separate that evaluation into three parts.

RQ1 checks the sampling moments and component degrees of freedom, including when population MI is close to zero.

RQ2 checks false-positive rates under equal MI, using shared population values of 0.005, 0.02, and 0.30 nats.

RQ3 checks power. MI in P stays at 0.02 nats, while Q has greater MI, with gaps of 0.005, 0.01, and 0.02 nats. Nats are the units obtained using natural logarithms.

The shared grid on the right uses four table sizes, from two-by-two to sixteen-by-sixteen. It includes uniform category frequencies, the same uneven frequencies in both populations, and different uneven frequencies. Ten sample sizes run from 10 to 50,000 observations per population. Combining these choices gives 360 settings in each of the false-positive and power studies.

At each setting, I draw 100,000 independent table pairs and give both tests the same pairs. These repetitions estimate performance precisely, while each individual test still uses only the stated sample size.

The model line explains how the populations have known MI. I draw X, then either copy its category into Y or draw Y independently from the same category frequencies. Changing the copying probability changes population MI while preserving those frequencies, and a numerical search finds the probability for each target MI.

Finally, the reporting rule at the bottom uses the usual 5% significance level. Unsuccessful calculations count as non-rejections, with calculation success reported separately so we can distinguish numerical failure from statistical performance.

## Slide 7: RQ1 results: approximation accuracy

This four-by-four example uses population P with different-skew frequencies and MI of 0.02 nats. Both graphs vary sample size along the horizontal axis and check the two moments needed for the degrees of freedom separately.

The top graph compares average V-hat with population V, so one means the first-order mean approximation agrees with the simulations. The curve rises above that benchmark before returning towards it.

The orange explanation on the right connects that rise to rare cells. Newly observed rare combinations can have pointwise-MI values far from the table's MI, whose squared deviations inflate V-hat. Larger counts stabilise the estimates, but at 1,000 observations the mean is still 19% above V.

The lower graph checks sampling variance. One means predicted and observed variance agree; values below one underestimate the variation, and values above one overestimate it.

The navy curve uses population inputs. Rare cells appearing in some samples but not others can produce changes larger than the linear approximation predicts. At the same sample size of 1,000, this prediction is about 3% low.

The orange curve estimates the inputs from each sampled table and averages the predictions. Estimating sensitivities from sparse counts can instead overpredict the variation; at that sample size, the prediction is about 8% high.

The bottom summary brings the checks together. A fairly accurate variance prediction can coexist with an inflated mean. Since moment matching uses the mean squared, substituting V for that larger sampling mean can push degrees of freedom down.

## Slide 8: RQ1 results: near independence

Here the table size stays four by four and sample size stays at 1,000, while population MI varies towards zero. The horizontal axis is population MI and the vertical axis is component degrees of freedom, both on logarithmic scales.

Start with the charcoal line. It is the moment-matching target, calculated from V-hat's mean and variance across repeated samples. At the smallest MI value, 0.0001, that target is about 9.1.

The dotted navy line uses known population inputs in the first-order formula, as explained in the upper-right box. Close to zero MI, this component value is approximately sample size times population MI, so it heads towards zero. At the same MI value it is about 0.1, far below the target.

The orange line averages the component degrees of freedom estimated from individual sampled tables. The lower-right box explains why it stays positive. At zero population MI, the linear sampling contribution vanishes, but squared probability errors still produce positive estimated MI. The sample-based calculation retains that noise, keeping its mean component value at about 4.9 at the weakest MI shown.

The callout therefore compares three distinct quantities: the moment target, the population first-order value, and the mean sample-based estimate. The last is about half the target here. Matching this moment target would not prove a Student t distribution for the statistic, so we also examine actual test decisions.

## Slide 9: RQ2 results: false positives across all null settings

The plot contains all 360 null settings, where population MI is equal and every rejection is a false positive. Each point is one setting, with Wald's rate on the horizontal axis and Expanded Welch's on the vertical. The dashed lines mark the 5% target.

The diagonal means equal rejection rates. All points lie on or below it because Expanded Welch can only reduce rejection.

The top callout on the right covers the 178 settings where Wald exceeds 5%. Expanded Welch moves closer to the target in 165 of them, including the highlighted uniform example, which moves from 8.35% to 4.90%.

The next callout covers the 180 settings where Wald is below 5%. Expanded Welch lowers the rate further in 176 and leaves four unchanged, so none moves closer to the target. Two remaining settings have Wald exactly at 5%.

The bottom callout first gives a descriptive count within the 4–6% band: 130 settings for Wald and 136 for Expanded Welch.

It also highlights the severe different-skew sixteen-by-sixteen example at MI 0.005 and 1,000 observations per population. Rejection only falls from 36.38% to 34.38%, still far above 5%.

The cutoff adjustment can therefore help without removing the errors responsible for excessive rejection. The next slide examines those errors in the estimated difference and standard error.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

The table gives three settings with equal MI of 0.02 nats, and every calculation succeeds. Bias divided by standard deviation measures how far the estimated difference is centred from zero, in sampling standard deviations. The variance ratio compares the average squared standard error with the observed sampling variance of that difference.

The first row is uniform four-by-four tables with 20 observations per population. Bias is near zero because the two estimators' expected biases cancel. The variance ratio is about 0.83, indicating underestimated uncertainty. For a given difference, a smaller denominator inflates the absolute statistic, and the larger cutoff brings rejection from 8.35% to 4.90%. That is the first explanation box: a cutoff can offset a standard error that is too small.

The second row is same-skew sixteen-by-sixteen tables with 1,000 observations. Bias again cancels, but the variance ratio is about 1.93. The oversized uncertainty estimate reduces the statistic's magnitude, so Wald already rejects only 0.60% of the time. Expanded Welch lowers that to 0.53%, making the test more conservative by pushing its false-positive rate further below 5%, as the middle box explains.

The third row uses different-skew sixteen-by-sixteen tables at the same sample size. The estimated difference is centred about 2.06 sampling standard deviations above zero, despite a variance ratio of about 1.94. Rejection remains high, moving from 26.01% to 24.84%. The final box explains that a larger cutoff cannot remove the shift in the estimated difference.

The conclusion at the bottom distinguishes these mechanisms: the cutoff can compensate for some underestimated uncertainty, but leaves the estimated difference and its bias unchanged.

## Slide 11: RQ3 results: the power cost of the larger cutoff

The quantity plotted here is power lost: Wald power minus Expanded Welch power, in percentage points. Power means rejecting equal MI when population MI really differs, using the usual 5% threshold. Expanded Welch cannot have higher power because its rejections are a subset of Wald's.

The graph covers all 360 power settings. Its line is the median across 36 settings at each sample size, while the shading spans their full range across populations.

The upper-right box summarises the small-sample cost. Median loss is about six points at ten observations, about one point from 50 to 1,000, and about 0.16 points at 10,000. Failed calculations also contribute at the smallest samples. At 10,000, even the largest loss is below 0.32 points.

These are comparisons at the same nominal level, rather than matched actual false-positive rates, so their interpretation also depends on the null results.

The lower-right box concerns absolute power. Even at 50,000 observations, the smallest MI gap of 0.005 nats gives Expanded Welch power of about 80% to 96%. The gaps of 0.01 and 0.02 exceed 99.9%, so similar power between methods does not mean every real difference is easy to detect.

The definition at the bottom also counts rejections in either direction. It does not check whether the estimated sign identifies the population with greater MI, which is the next result.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map uses different category frequencies and an MI gap of 0.01 nats, with Q always having greater population MI. Rows identify table size and columns identify sample size.

Each cell shows the percentage of Expanded Welch rejections whose estimated difference wrongly points to P as having greater MI. As the caption explains, a displayed 50% means roughly half the rejections have the wrong estimated sign. The percentages are rounded and are conditional on rejecting, rather than percentages of all sampled tables.

The dark cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range.

The upper-right box explains the outlined sixteen-by-sixteen cell at 1,000 observations per population. MI in P minus MI in Q is truly minus 0.01 nats, but its mean estimate is plus 0.0207. Expanded Welch rejects in about 9.66% of repetitions, and more than 99.9% of those rejections have the wrong estimated sign.

The next box gives the explanation: unequal residual biases outweigh the true gap and reverse the average estimate. A larger cutoff leaves that bias in place. Increasing sample size reduced the problem in these simulations; by 10,000 observations, fewer than 0.4% of rejections have the wrong sign in every setting across the full power grid.

The bottom callout summarises the extent of the problem across all 360 power settings. At least 90% of rejections point the wrong way in 28 settings, all with different category frequencies between populations. Those rejections count towards two-sided power but do not reliably identify which population has greater MI.

## Slide 13: Conclusions and next steps

The three numbered findings bring the results together.

First, I derived the variance sensitivity and used it to estimate MI-specific degrees of freedom for Expanded Welch.

Second, the larger cutoff helped in many settings where Wald rejected too often, but pushed already conservative settings further below 5%.

Third, at the same nominal significance level, power cannot exceed Wald's, and residual bias can make rejected differences point the wrong way.

The scope statement is important: the evaluation used one population construction and equal sample sizes, with Wald as the main benchmark.

The first next step is to reduce bias in the estimated MI difference and improve its standard error and degrees of freedom, including the sampling variation missed when population MI is close to zero.

The second is to evaluate other population constructions and unequal sample sizes.

Overall, adjusting the cutoff improves some comparisons, while the remaining failures show why accurate estimates of the MI difference and its uncertainty are also essential.

Thank you.

## Questions and answer guides

### 1. What is your main contribution?

- I derived the MI-specific sensitivity of the pointwise-MI variance as the cell probabilities, margins, and log ratios change.
- That gives the sampling-variance approximation needed to estimate component degrees of freedom and combine them using the established Welch–Satterthwaite rule.
- Comparing against Wald isolates the reference-distribution change because both tests use the same estimated difference and standard error.

### 2. What do V, g, and tau-squared actually mean?

- V measures variation in pointwise MI across outcomes. V-hat estimates it from one table, and V-hat divided by n estimates MI's sampling variance.
- g measures how sensitive V is to shifting probability towards a particular cell, including the resulting changes in the margins.
- Tau-squared is the variance of those sensitivities across outcomes. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of the sensitivities.

### 3. Where do the degrees of freedom come from, and is the Student t distribution exact?

- A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching moments gives nu as twice the squared mean divided by the variance.
- Approximating those moments by V and tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table.
- The Student t distribution is approximate: moment matching does not prove independence between the MI numerator and estimated variance, or determine their full distributions.

### 4. Why does the approximation struggle when population MI is close to zero?

- When population MI is zero, all population pointwise-MI values are zero, and the first-order sampling terms for MI and V-hat vanish. Squared probability errors still produce positive estimated MI.
- On Slide 8, the population first-order value is about 0.1, while the mean sample-based estimate is about 4.9 because its calculation retains positive estimated MI from sampling noise.
- The repeated-sample moment target is about 9.1. Including quadratic sampling noise helps explain the separation, but does not establish an exact replacement test.

### 5. Why this simulation design, and why 100,000 repetitions?

- The copying model controls MI while preserving chosen category frequencies, giving known population truth. It represents one family of joint probability tables.
- The 360 null and 360 power settings vary table size, frequencies, sample size, and MI values to expose different estimation problems.
- Repetitions estimate performance precisely; they do not increase an individual test's sample size. Both methods receive the same sampled pairs for comparison.

### 6. Why does bias remain after your correction?

- With equal dimensions and sample sizes, the two leading bias corrections cancel exactly in the MI difference.
- Higher-order biases remain. Identical population tables have matching expected biases, but distinct tables can have unequal biases even when their MI values agree.
- The difference can therefore be shifted away from its true value. Raising the rejection cutoff does not remove that shift.

### 7. Why does Expanded Welch help in some settings and hurt in others?

- Its larger cutoff can compensate for excessive rejection: the uniform example moves from 8.35% to 4.90% under equal MI.
- Where uncertainty is overestimated and Wald already rejects too rarely, the larger cutoff lowers the false-positive rate further below 5%.
- Substantial difference bias can leave both tests unreliable. In the diagnostic different-skew example, both reject about a quarter of the time despite equal population MI.

### 8. If it loses power, is the comparison fair or the method useful?

- At the same nominal 5% level, Expanded Welch rejections are a subset of Wald rejections, so its power can only stay the same or fall.
- Reducing excessive false positives may justify some power loss, but reducing an already-low rate makes conservatism worse.
- This compares the usual testing rules, rather than power at matched actual false-positive rates. The study establishes a conditional trade-off, not universal superiority.

### 9. What does the wrong-direction result mean?

- Population MI really differs, so these are rejections under an alternative. The error is that the estimated sign identifies the wrong population as having greater MI.
- In the highlighted example, the true difference is −0.01, but its estimated mean is about +0.0207 because unequal residual biases outweigh the gap.
- Of 9,662 rejections, 9,659 point the wrong way. The 99.9% figure is conditional on rejection, not a percentage of all samples; two-sided power counts those rejections.

### 10. Why not use permutation or bootstrap instead?

- Simple group-label permutation requires exchangeability. Equal MI allows different joint distributions, so it does not supply that condition.
- Separate-sample bootstrapping is a candidate, but an ordinary empirical bootstrap cannot generate cells absent from the observed table, and estimation bias can remain.
- I did not conduct a full resampling comparison. The thesis cannot establish superiority over those alternatives.

### 11. What assumptions and calculation rules matter most?

- Observations are independent and identically distributed within each population, with independent samples, fixed, aligned categories, positive population cell probabilities, and positive V and tau-squared for the first-order construction.
- Positive population probabilities still allow empty sampled cells, which are retained. Successful calculations require a positive finite standard error and, for Expanded Welch, positive finite degrees of freedom.
- Failed calculations count as non-rejections, with success reported separately. They contribute to some small-sample power loss but do not explain the highlighted failures where every calculation succeeds.

### 12. What is your overall conclusion, and what would you improve next?

- Expanded Welch improves some excessive false-positive rates, but its larger cutoff also increases conservatism and costs power at the same nominal level.
- I would first improve the MI-difference and standard-error estimates, changing one at a time to identify what resolves the failures.
- Further work should retain additional sampling variation when population MI is close to zero and evaluate other population constructions and unequal sample sizes. There is no universal sample-size rule established here.
