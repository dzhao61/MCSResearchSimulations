# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

My thesis asks whether mutual information differs between two populations when we only have finite samples from each.

I develop an MI-specific version of the Welch–Satterthwaite approach, called the Expanded Welch test. I then investigate whether its larger rejection cutoff improves false-positive rates, what it costs in power, and which estimation problems remain.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, measures how much knowing one variable reduces uncertainty about another, on average. It is zero when the variables are independent, and positive when they are associated.

I compare MI between two populations, whose joint probability tables I call P and Q. We observe a sample from each population, summarise the observations in count tables, and estimate MI from those counts.

The difficulty is that these estimates change from sample to sample. An observed difference can therefore arise even when the population MI values are equal.

The null hypothesis is that population MI is equal, against the two-sided alternative that it differs. The test must account for sampling uncertainty before we interpret an estimated difference as evidence against that null.

## Slide 3: Literature review: foundations and the MI-specific step

The comparison builds on established results for estimating MI, correcting its leading bias, and approximating its sampling variance. The Wald test combines these estimates with the standard normal distribution as its reference.

Welch and Satterthwaite provide a way to account for variability in estimated variances when choosing degrees of freedom. Related work applies moment matching to entropy and other statistical comparisons.

For MI, the additional calculation concerns the variability of the pointwise-MI variance estimate itself. When the sampled table changes, its cell weights, row and column totals, and pointwise-MI values change together.

I derive the combined effect of those changes, then use it to estimate degrees of freedom for the test.

## Slide 4: Method: one statistic, two reference distributions

Both tests use the same statistic. They take the estimated MI difference, apply the same leading bias correction, and divide by the same estimated standard error.

Pointwise MI describes the information contribution of one category pair. V-hat estimates the variance of those contributions. Dividing V-hat by sample size estimates the sampling variance of the MI estimate. Because the two samples are independent, their variance contributions add.

The standard error also varies between samples. The Expanded Welch test uses estimated degrees of freedom and a Student t distribution to adjust the rejection cutoff for uncertainty in the variance estimate.

The Wald test uses the standard normal distribution, giving a two-sided 5% cutoff of about 1.96. The illustration uses a Student t distribution with five degrees of freedom, giving a cutoff of about 2.57. The actual degrees of freedom depend on the sampled tables.

Under the calculation rules used here, every Expanded Welch rejection is also a Wald rejection. The question is whether reducing rejection improves false-positive rates enough to justify the accompanying loss of power.

## Slide 5: Approach and contribution

The key calculation involves two levels of variation. V describes variation in pointwise MI, while V-hat itself changes between samples. Choosing degrees of freedom requires an approximation to that second level.

I begin by moving a small amount of probability towards one cell, reducing the other probabilities proportionally. The function g measures how sensitive V is to that change, including the effects on the margins and pointwise-MI values.

Each possible outcome has its own sensitivity. If the observed outcome is X and Y, its sensitivity is g evaluated at X and Y. Tau-squared is the variance of these sensitivities across outcomes drawn from the population.

The sampling error in V-hat is approximately the average of these observation-level sensitivities. Independent observations therefore give an approximate sampling variance of tau-squared divided by sample size.

Satterthwaite moment matching uses the mean and sampling variance of V-hat to choose component degrees of freedom. Greater variability relative to the squared mean gives fewer degrees of freedom. I estimate the inputs from each table and combine the two components using the Welch–Satterthwaite rule.

The derivative defining g is exact for positive population tables. The sampling expansion and the Student t reference distribution are approximations, which motivates the first part of the evaluation.

## Slide 6: Evaluation design

I construct population tables with known MI using a copying model. I draw X, then either copy its category into Y or draw Y independently from the same category frequencies. Changing the copying probability controls association while preserving those frequencies. A numerical search finds the probability that produces the target MI.

The first research question checks the approximations and degrees of freedom. The false-positive study uses equal population MI. The power study fixes MI in P at 0.02 nats and gives Q greater MI. Nats are the units obtained using natural logarithms.

Each test study contains 360 settings, varying table size, category frequencies, sample size, and MI. Each setting uses 100,000 independently sampled table pairs, and both tests receive the same pairs.

Both tests use a nominal 5% significance level. Unsuccessful calculations count as non-rejections, and I report calculation success separately from statistical performance.

## Slide 7: RQ1 results: approximation accuracy

This example uses a four-by-four population table. The top graph compares the average V-hat with the population value of V. A ratio of one means agreement.

The average estimate rises above the population value before recovering. When rare cells first appear, their estimated pointwise-MI values can lie far from the table's MI. The resulting squared deviations can inflate V-hat until larger counts stabilise the estimates.

The lower graph concerns the sampling variance of V-hat itself. The navy curve predicts it using population inputs. The orange curve estimates the inputs from each sampled table, then averages those predictions. Again, one means agreement with the observed sampling variance.

At 1,000 observations, the population prediction is about 3% low, and the sample-based prediction is about 8% high. But the mean V-hat is still 19% above V.

Moment matching depends on both the mean and the sampling variance. An accurate variance prediction alone therefore does not ensure accurate degrees of freedom.

## Slide 8: RQ1 results: near independence

Here sample size stays at 1,000 while population MI approaches zero.

The charcoal line is the moment-matching target, calculated from the observed mean and variance of V-hat across repeated samples. It provides the benchmark for component degrees of freedom.

The dotted navy line uses population inputs in the first-order formula. The orange line averages the component degrees of freedom estimated from each sampled table.

At the weakest association, the target is about 9.1. The population-based formula gives about 0.1, while the mean sample-based estimate is about 4.9. These are three different quantities, and they separate sharply near independence.

Random count fluctuations can make a sample look associated even when the population variables are independent. At independence, the linear contribution to sampling error vanishes, but variation from squared probability errors remains. The first-order calculation omits those quadratic terms.

The sample-based formula responds to the apparent association in sampled tables, so its mean stays positive. A calculation that includes this sampling noise predicts about 4.6, close to the observed 4.9. It explains why the sample-based estimate stays positive while remaining below the moment target.

## Slide 9: RQ2 results: false positives across all null settings

This chart shows all 360 settings with equal population MI, so every rejection is a false positive.

Each point represents one setting. Wald's false-positive rate is on the horizontal axis, and Expanded Welch's is on the vertical. The diagonal means equal rejection rates, and the dashed lines mark the 5% target.

Every point lies on or below the diagonal because Expanded Welch can only reduce rejection.

Where Wald exceeds 5%, Expanded Welch moves closer to the target in 165 of 178 settings. Where Wald is already below 5%, none of the 180 settings improves. Rejection either falls further or stays unchanged.

The upper-right example also shows the limit of the improvement: Expanded Welch still rejects more than 34% of the time under equal MI.

The larger cutoff therefore helps in many settings with excessive rejection, but the remaining errors need an explanation beyond the cutoff.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These examples separate bias in the estimated difference from error in its estimated uncertainty. All three have equal population MI, and every calculation succeeds.

Bias divided by the sampling standard deviation measures how far the estimated difference is centred from zero. The variance ratio compares the average squared standard error with the observed sampling variance of that difference.

In the uniform four-by-four example, the two MI estimates have the same expected bias, so it cancels in their difference. The variance ratio is about 0.83, indicating underestimated uncertainty. The larger cutoff brings rejection from about 8.35% to 4.90%.

In the same-skew example, bias again cancels, but the variance ratio is about 1.93. Uncertainty is overestimated, so Wald already rejects less than 1% of the time. Expanded Welch lowers rejection further. This is greater conservatism: the false-positive rate falls further below 5%.

In the different-skew example, the variance estimate is similarly inflated, but the two residual biases do not cancel. The estimated difference is centred about two sampling standard deviations above zero, and both tests reject about a quarter of the time.

Changing the cutoff leaves that shift in the estimated difference unchanged.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the probability of rejecting equal MI when the population MI values differ.

This chart summarises all 360 power settings at the same nominal 5% significance level. It shows Wald power minus Expanded Welch power, in percentage points. The line is the median across 36 settings at each sample size, and the shading shows their full range.

Expanded Welch loses power because its rejections are a subset of Wald's. At ten observations, the median loss is about six percentage points, with unsuccessful calculations also contributing. By 10,000 observations, the loss is below 0.32 percentage points in every setting.

However, similar power between methods does not necessarily mean high power. Even at 50,000 observations, Expanded Welch power for the smallest MI gap ranges from about 80% to 96%. The two larger gaps exceed 99.9%.

These power rates count rejections in either direction, which leads to a further problem.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map uses populations with different category frequencies and an MI gap of 0.01 nats. Q always has greater population MI.

Each cell shows the percentage of Expanded Welch rejections whose estimated difference incorrectly points to P as having greater MI. The percentage is conditional on rejecting, and the displayed values are rounded.

The darker cells show that almost every rejection points the wrong way in parts of the range with sparse, larger tables.

In the outlined sixteen-by-sixteen example, each population has 1,000 observations. The true difference is minus 0.01 nats, but the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9% of those rejections have the wrong estimated sign.

The unequal residual biases have outweighed the true MI gap. Raising the cutoff changes rejection frequency while leaving that bias unchanged.

Increasing sample size reduced this problem in these simulations. At 10,000 observations, the wrong-sign share is below 0.4% in every setting across the full power grid.

Across all 360 power settings, 28 have at least 90% of rejections pointing the wrong way. All use different category frequencies between populations. Those rejections count towards two-sided power, even though their estimated direction is unreliable.

## Slide 13: Conclusions and next steps

The thesis derives the MI-specific variance sensitivity and uses it to calculate degrees of freedom for the Expanded Welch test.

The larger cutoff improves many excessive false-positive rates, but it also increases conservatism and reduces power at the same nominal significance level. Near independence, omitted quadratic sampling variation helps explain why the degrees-of-freedom approximations separate. In sparse tables, unequal residual biases can even reverse the estimated direction.

The evaluation uses one population construction, equal sample sizes, and Wald as the main benchmark. The next steps are to improve the MI-difference and standard-error estimates, account for additional sampling variation near independence, and evaluate broader populations and unequal sample sizes.

Overall, adjusting the cutoff can improve the test, but reliable comparison also requires accurate estimates of the MI difference and its uncertainty.

Thank you.
