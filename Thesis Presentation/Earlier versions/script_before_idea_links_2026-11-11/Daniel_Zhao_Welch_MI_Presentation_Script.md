# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, tells us how much knowing one variable reduces uncertainty about another, on average. If knowing X changes the probabilities we'd assign to Y's categories, then X gives us information about Y, and MI averages that gain over the possible outcomes. That average is zero when the variables are independent and positive when they're associated.

I'm interested in whether the MI value differs between two populations, whose joint probability tables I'll call P and Q.

We take a sample from each population, put the observations into count tables, and estimate MI from those counts. If we collected new samples, we'd generally get different estimates, so a difference between the estimates can arise even when population MI is equal.

We therefore test the null hypothesis that the population MI values are equal, against a two-sided alternative that they differ. The test assesses whether the observed difference is large relative to its sampling uncertainty.

## Slide 3: Literature review: foundations and the MI-specific step

Existing research gives us an MI estimator, a correction for its leading bias, and an approximation to its sampling variance. The Wald test uses those results with the standard normal distribution as its reference.

The Welch–Satterthwaite approach chooses degrees of freedom using the variability of estimated variances, and related work applies this moment-matching principle to entropy and other statistical comparisons.

For MI, each category pair contributes a pointwise-MI value to the overall average. To adapt Welch–Satterthwaite, we need to know how much the estimated variance of those contributions changes between samples.

Changing a table affects its cell weights, row and column totals, and pointwise-MI values together. For example, changing a row total alters the log ratios for cells in that row, including cells whose own counts haven't changed, so treating the estimated pointwise-MI values as fixed would miss those effects.

I track those changes together and derive their combined effect on the variance, which gives us the inputs needed to estimate the degrees of freedom.

## Slide 4: Method: one statistic, two reference distributions

Both tests use the same statistic, calculated by applying the leading bias correction to the estimated MI difference and dividing by the estimated standard error. A statistic of two means the estimated difference is twice its estimated standard error, with the sign identifying which population has the higher estimate. The two-sided test uses the statistic's magnitude.

Here, V-hat estimates how much the pointwise-MI contributions vary, and dividing it by sample size estimates the sampling variance of MI. Because the two samples are independent, we add their variance contributions to get the squared standard error.

Since that standard error also changes between samples, Expanded Welch uses estimated degrees of freedom and a Student t distribution to adjust the cutoff for uncertainty in the variance estimate.

In the graph, the Wald test uses the standard normal distribution, giving a two-sided 5% cutoff of about 1.96. For comparison, the Student t distribution shown has five degrees of freedom and a cutoff of about 2.57.

In the actual test, those degrees of freedom are estimated from the tables, with smaller values giving a larger cutoff. As the degrees of freedom increase, the cutoff approaches the Wald cutoff.

Under these calculation rules, Expanded Welch only rejects when Wald also rejects, so the experiments check whether that reduction improves false-positive rates and how much power it costs.

## Slide 5: Approach and contribution

To choose the degrees of freedom, we need to keep two kinds of variation separate. V describes how pointwise MI varies across outcomes, while V-hat estimates V from a sampled table and therefore changes from sample to sample.

I start by slightly increasing the probability assigned to one cell, while reducing the other probabilities proportionally, and call the sensitivity of V to that change g. This sensitivity includes the effects of changing the cell weights, margins, and pointwise-MI values. A positive g means the shift initially raises V, whereas a negative g means it lowers V.

Although g is fixed for a particular population and cell, different cells can have different effects. When we draw an outcome X and Y, we're randomly selecting which cell's sensitivity we observe, so g evaluated at X and Y is a random quantity.

Tau-squared measures how much those sensitivities vary across outcomes drawn from the population. Greater variation in those sensitivities means that changes in the mix of sampled outcomes can make V-hat less stable.

The first-order expansion approximates the error in V-hat by the average sensitivity across the sampled observations. Those contributions have population mean zero, and because the observations are independent, the variance of their average is tau-squared divided by sample size.

We use V as an approximation to V-hat's sampling mean, and combine it with tau-squared divided by sample size to fit a scaled chi-squared distribution. Matching those two quantities determines the component degrees of freedom: a variance estimate that fluctuates more relative to its mean gets fewer degrees of freedom.

We estimate the inputs for P and Q and combine the two components using the Welch–Satterthwaite rule. The derivative defining g is exact for positive population tables, but the sampling expansion and the Student t reference distribution are approximations. The first research question checks the moment approximations and degrees of freedom before we assess the actual test decisions.

## Slide 6: Evaluation design

This evaluation uses populations with known MI to answer the three research questions on the left.

The first checks the approximations and degrees of freedom, while the second asks how often the tests reject when population MI is equal. The third checks power, with MI in P fixed at 0.02 nats and greater MI in Q. Nats are the units we get from natural logarithms.

On the right, the shared simulation design gives each of the false-positive and power studies 360 settings, varying table size, category frequencies, sample size, and MI. The frequency regimes include uniform category frequencies, the same uneven frequencies in both populations, and different uneven frequencies, allowing us to examine how rare combinations and unequal estimation biases affect the comparison.

For each setting, I draw 100,000 independent table pairs and give both tests the same pairs. Each repetition is one application of each test at the stated sample size, so repetition lets us measure performance more precisely while each individual test still uses only that sample size.

To generate those populations, I use the copying model at the bottom of the design panel. I first draw X, then either copy its category into Y or draw Y independently from the same category frequencies. By changing how often I copy, I change the population MI value while keeping those frequencies fixed, and a numerical search finds the copying probability for the target MI.

Finally, the reporting line at the bottom applies to both tests: we use a nominal 5% significance level. Unsuccessful calculations count as non-rejections, with calculation success reported separately.

## Slide 7: RQ1 results: approximation accuracy

In the top graph of this four-by-four example, we're comparing the average V-hat with the population value of V. A ratio of one means agreement.

The average estimate rises above the population value before coming back down. As rare cells first appear, their estimated pointwise-MI values can be far from the table's MI, producing large squared deviations that can inflate V-hat until larger counts stabilise the estimates. Even at 1,000 observations, the average V-hat is still 19% above V.

Moving to the lower graph, we're now asking how much V-hat itself varies between samples. The navy curve uses population inputs, while the orange curve uses inputs estimated from each sampled table and then averages the predictions.

Here, a ratio of one means agreement with the variance observed across repetitions. Ratios below one predict too little variation, while those above one predict too much.

As rare cells appear in some samples but not others, their contributions can change more than the linear approximation predicts. At the same time, estimating the sensitivities from sparse counts can overpredict that variation.

At the same sample size of 1,000, the population-based prediction is about 3% low, while the sample-based prediction is about 8% high.

Taken together, the graphs show why getting the variance approximately right doesn't, by itself, give us accurate degrees of freedom. Moment matching also uses the mean squared, so replacing the larger sampling mean with V can push the predicted degrees of freedom down.

## Slide 8: RQ1 results: near independence

For this graph, sample size stays at 1,000 while population MI approaches zero. As that population value gets smaller, fluctuations in the counts become more important relative to the MI we're trying to estimate.

The charcoal line is our moment-matching benchmark for the component degrees of freedom, calculated from the mean and variance of V-hat across repeated samples. The dotted navy line uses population inputs in the first-order formula, while the orange line averages the degrees of freedom estimated from each sampled table.

At the smallest population MI value shown, the target is about 9.1. By comparison, the population-based formula gives about 0.1, while the mean sample-based estimate is about 4.9.

To understand that gap, remember that random count fluctuations can produce positive estimated MI even when population MI is zero. In that case, the linear contribution to the error in V-hat vanishes, but squared probability errors still produce variation that the first-order calculation leaves out.

The sample-based formula retains this positive estimated MI, keeping the average estimated degrees of freedom positive. Including this sampling noise predicts a mean estimate of about 4.6, close to the observed 4.9, and helps explain why the orange line stays below the target.

Even if our estimated degrees of freedom matched that target, we'd still be using a moment-based approximation. That wouldn't prove that the full statistic follows a Student t distribution, so we still need to check the test decisions.

## Slide 9: RQ2 results: false positives across all null settings

We're now looking at test decisions across all 360 null settings, where population MI is equal and every rejection is a false positive. An accurately calibrated 5% test would reject in about one experiment out of twenty across repeated samples at each setting.

Each point represents one setting, with Wald's false-positive rate on the horizontal axis and Expanded Welch's on the vertical. The diagonal means equal rates, and the dashed lines mark 5%.

Every point is on or below the diagonal because Expanded Welch can only reduce rejection. On the right, where Wald exceeds 5%, that reduction moves closer to the target in 165 of 178 settings.

On the left, where Wald is already below 5%, none of the 180 settings improves, because rejection either falls further or stays the same.

The example in the upper right shows how much can remain unresolved: Expanded Welch still rejects more than 34% of the time, even though population MI is equal.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These three examples help explain the different rejection patterns, and all have equal population MI with every calculation successful. Bias shifts the centre of the estimated difference, while the variance estimate determines how much uncertainty we attach to it.

Bias divided by standard deviation measures how far the estimated difference is centred from zero, in sampling standard deviations. The variance ratio compares the average squared standard error with the variance of the estimated difference across repetitions.

In the uniform four-by-four example, the two MI estimates have the same expected bias, so their biases cancel in the difference. The variance ratio is about 0.83, meaning we're underestimating uncertainty, and the larger cutoff brings rejection from about 8.35% to 4.90%.

In the same-skew example, the biases again cancel, but the variance ratio is about 1.93. We're overestimating uncertainty, so Wald already rejects less than 1% of the time. Expanded Welch lowers that rate further below 5%, making the test more conservative.

In the different-skew example, the variance estimate is similarly inflated, but the residual biases don't cancel. The estimated difference is centred about two sampling standard deviations above zero, which helps explain why both tests reject about a quarter of the time.

Because raising the cutoff doesn't move that estimated difference back towards zero, the two tests can agree on a rejection while sharing the estimation error that helped produce it.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the probability of rejecting equal MI when the population MI values really differ.

This graph covers all 360 power settings at the same nominal 5% significance level and shows the power lost with Expanded Welch compared with Wald, in percentage points. The line gives the median across 36 settings at each sample size, while the shading spans their full range, showing variation between population settings rather than uncertainty in a single rate.

Because Expanded Welch's rejections are a subset of Wald's, its power can only stay the same or fall. At ten observations, the median loss is about six percentage points, with unsuccessful calculations also contributing. By 10,000 observations, the loss is below 0.32 percentage points in every setting.

Because the usual thresholds can give the methods different actual false-positive rates, we need to read this power loss alongside the null results before judging the trade-off.

The methods being close doesn't necessarily mean either has high power. Even at 50,000 observations, Expanded Welch power for the smallest MI gap ranges from about 80% to 96%, while the two larger gaps exceed 99.9%.

Those two-sided power rates also include rejections where the estimated difference points the wrong way, which leads to the next result.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map shows populations with different category frequencies and an MI gap of 0.01 nats, with Q always having greater population MI.

Each percentage tells us, among the samples where Expanded Welch rejects, how often the estimated difference wrongly suggests that P has greater MI. The displayed percentages are rounded, so 90% means roughly nine out of ten rejections have the wrong estimated direction, rather than nine out of ten samples.

In parts of the range with sparse, larger tables, almost every rejection points the wrong way.

Take the outlined sixteen-by-sixteen example, with 1,000 observations per population. Because the difference is MI in P minus MI in Q, the true difference is minus 0.01 nats, but the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9% of those rejections have the wrong estimated sign.

Here, unequal residual biases outweigh the true gap and carry the average estimate past zero, reversing its sign. A larger cutoff changes how often we reject, but leaves that bias in place.

Increasing sample size reduced this problem in these simulations: by 10,000 observations, fewer than 0.4% of rejections have the wrong sign in every setting across the full power grid.

Across all 360 settings, 28 have at least 90% of rejections pointing the wrong way, and all have different category frequencies between populations. Those rejections count towards two-sided power even though they don't reliably identify which population has greater MI.

## Slide 13: Conclusions and next steps

I derived the MI-specific variance sensitivity and used it to estimate degrees of freedom for Expanded Welch.

Its larger cutoff brings many excessive false-positive rates closer to 5%, but also lowers rejection when the rate is already too low and costs power at the same nominal significance level.

The approximation checks show that the first-order calculation misses important quadratic sampling variation when population MI is close to zero. The wrong-direction results also show how unequal residual biases can outweigh the real MI difference in sparse tables.

I evaluated one population construction with equal sample sizes, using Wald as the main benchmark. I would next focus on improving the MI-difference and standard-error estimates, while accounting for the extra sampling variation when population MI is close to zero. A broader evaluation would then cover other population constructions and unequal sample sizes.

My overall finding is that changing the cutoff can help, but reliable comparison also depends on estimating the MI difference and its uncertainty accurately.

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
