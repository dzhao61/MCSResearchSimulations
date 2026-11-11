# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone. Today I'll talk about comparing mutual information between two populations.

When we only have a sample from each population, an estimated difference could reflect a real difference, or it could come from sampling variation. My thesis develops the Expanded Welch test for this comparison and investigates when it improves on the Wald test.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, tells us how much knowing one variable reduces uncertainty about another, on average. It's zero when the variables are independent, and positive when they're associated.

If knowing X changes the probabilities we'd assign to Y's categories, X tells us something about Y. MI summarises the average information we gain across the outcomes we could observe.

I'm interested in whether that association differs between two populations. I'll call their joint probability tables P and Q.

We take a sample from each population, put the observations into count tables, and estimate MI from those counts. But if we collected new samples, we'd generally get different estimates. So even when population MI is equal, the two estimates can differ.

That's the reason for testing. The null hypothesis says the population MI values are equal. The two-sided alternative says they're different. We need to decide whether the observed difference is large relative to its sampling uncertainty.

## Slide 3: Literature review: foundations and the MI-specific step

Existing research gives us an MI estimator, a correction for its leading bias, and an approximation to its sampling variance. The Wald test uses those results with the standard normal distribution as its reference.

The Welch–Satterthwaite approach uses the variability of estimated variances to choose degrees of freedom. Related work applies moment matching to entropy and other statistical comparisons.

Applying that approach here requires an extra calculation: how much does the pointwise-MI variance estimate change between samples? Pointwise MI is a category pair's contribution to the overall MI.

Changing a table affects its cell weights, row and column totals, and pointwise-MI values together. For example, changing a row total changes the log ratios for cells in that row, including cells whose own counts haven't changed. Treating the estimated pointwise-MI values as fixed would miss those effects.

I derive the combined effect of these changes, then use that result to estimate degrees of freedom for the test.

## Slide 4: Method: one statistic, two reference distributions

The two tests start with exactly the same statistic. We estimate the MI difference, apply the same leading bias correction, and divide by the same estimated standard error. A statistic of two means the estimated difference is twice its estimated standard error. Its sign identifies which population has the higher estimate, while the two-sided test uses its magnitude.

Here, V-hat estimates how much those pointwise-MI contributions vary. Dividing by sample size estimates the sampling variance of MI. The samples are independent, so we add their two variance contributions to get the squared standard error.

The standard error itself also changes between samples. Expanded Welch uses estimated degrees of freedom and a Student t distribution so that the cutoff reflects uncertainty in the variance estimate.

In the graph, the Wald test uses the standard normal distribution, giving a two-sided 5% cutoff of about 1.96. The Student t distribution shown has five degrees of freedom, giving a cutoff of about 2.57. In the actual test, we estimate the degrees of freedom from the tables. Fewer degrees of freedom give a larger cutoff. As they increase, that cutoff approaches the Wald cutoff.

Under these calculation rules, Expanded Welch only rejects when Wald also rejects. The experiments check whether that reduction improves false-positive rates and how much power it costs.

## Slide 5: Approach and contribution

Choosing the degrees of freedom means accounting for two kinds of variation. V describes how pointwise MI varies across outcomes. V-hat estimates V, and that estimate varies from sample to sample.

I start by slightly increasing the probability assigned to one cell, while reducing the other probabilities proportionally. I call the sensitivity of V to that change g. It includes the effects of changing the cell weights, margins, and pointwise-MI values. A positive g means this small shift initially raises V. A negative g means it lowers V.

Different cells can have different effects. For a fixed population and cell, g is fixed. It becomes random when a sampled outcome selects which cell's sensitivity we observe. That's what g evaluated at X and Y means.

Tau-squared measures how much those sensitivities vary across outcomes drawn from the population. If the sensitivities vary more, changing the mix of observed outcomes can make V-hat less stable.

We can approximate the error in V-hat by averaging the sensitivities of the sampled observations. Those contributions have population mean zero. Because the observations are independent, the variance of that average is tau-squared divided by sample size.

That gives us the sampling-variance approximation needed for moment matching. Here, we model V-hat using a scaled chi-squared distribution with matching mean and variance. Matching those two quantities determines the component degrees of freedom. The more variable V-hat is relative to its mean, the fewer component degrees of freedom we get.

We estimate the inputs for P and Q, then combine the components using the Welch–Satterthwaite rule.

The derivative defining g is exact for positive population tables. Using it to approximate sampling errors, and then using a Student t reference distribution, involves approximations. The first research question checks how well those approximations work.

## Slide 6: Evaluation design

I check the method using populations with known MI.

I construct them using a copying model. First, I draw X. Then I either copy its category into Y or draw Y independently from the same category frequencies. Changing how often I copy changes the association while keeping those frequencies fixed. A numerical search finds the copying probability for the target MI.

The first research question checks the approximations and degrees of freedom. The second checks false positives using equal population MI. The third checks power, with MI in P fixed at 0.02 nats and greater MI in Q. Nats are the units we get from natural logarithms.

The false-positive and power studies each have 360 settings, varying table size, category frequencies, sample size, and MI. The frequency regimes include uniform category frequencies, the same uneven frequencies in both populations, and different uneven frequencies. These let us examine how rare combinations and unequal estimation biases affect the comparison.

For each setting, I draw 100,000 independent table pairs and give both tests the same pairs. One repetition is one application of each test at the stated sample size. Repeating the experiment lets us measure how often a test rejects, while each application still uses only the stated sample size.

Both tests use a nominal 5% significance level. Unsuccessful calculations count as non-rejections, and I report calculation success separately.

## Slide 7: RQ1 results: approximation accuracy

This example uses a four-by-four population table. The top graph compares the average V-hat with the population value of V. A ratio of one means agreement.

The average estimate rises above the population value before coming back down. When rare cells first appear, their estimated pointwise-MI values can be far from the table's MI. Those large squared deviations can inflate V-hat until larger counts stabilise the estimates.

The lower graph asks how much V-hat itself varies between samples. The navy curve uses population inputs. The orange curve uses inputs estimated from each sample, then averages the predictions. A ratio of one means agreement with the variance observed across repetitions. Below one, we predict too little variation; above one, we predict too much.

At 1,000 observations, the population prediction is about 3% low, and the sample-based prediction is about 8% high. But the average V-hat is still 19% above V.

That matters because moment matching uses both the mean and the variance. Getting the variance approximately right doesn't, by itself, give us accurate degrees of freedom. The mean enters that calculation squared, so replacing the larger sampling mean with V can push the predicted degrees of freedom down.

## Slide 8: RQ1 results: near independence

For this graph, sample size stays at 1,000 while population MI approaches zero. Moving towards weaker association reduces the population signal without giving us more data to distinguish it from fluctuations in the counts.

The charcoal line is the moment-matching target, calculated from the mean and variance of V-hat across repeated samples. It's our benchmark for the component degrees of freedom.

The dotted navy line uses population inputs in the first-order formula. The orange line is the average of the degrees of freedom estimated from each sampled table.

At the weakest association, the target is about 9.1. The population-based formula gives about 0.1, while the mean sample-based estimate is about 4.9.

To understand that gap, remember that random count fluctuations can make a sampled table look associated even when the population variables are independent. At independence, the linear contribution to the error in V-hat vanishes. But squared probability errors still contribute variation, and the first-order calculation leaves those quadratic terms out.

The sample-based formula picks up this apparent association, keeping its average positive. Including this sampling noise predicts a mean estimate of about 4.6, close to the observed 4.9. That helps explain the orange line's position below the target.

The charcoal target comes from the mean and variance of V-hat. Even matching those two moments wouldn't prove that the full statistic follows a Student t distribution. We still need to check the test decisions.

## Slide 9: RQ2 results: false positives across all null settings

Now we can look at the test decisions. All 360 settings here have equal population MI, so every rejection is a false positive. An accurately calibrated 5% test would reject in about one experiment out of twenty across repeated samples at each setting.

Each point is one setting. The horizontal axis shows Wald's false-positive rate, and the vertical axis shows Expanded Welch's. The diagonal means equal rates, and the dashed lines mark 5%.

Every point is on or below the diagonal because Expanded Welch can only reduce rejection.

On the right, where Wald exceeds 5%, Expanded Welch moves closer to the target in 165 of 178 settings. On the left, Wald is already below 5%. None of those 180 settings improves: rejection either falls further or stays the same.

The example in the upper right also shows how much can remain unresolved. Expanded Welch still rejects more than 34% of the time, even though population MI is equal.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These three examples help explain those patterns. All have equal population MI, and every calculation succeeds. Bias shifts the centre of the estimated difference, while the variance estimate determines how much uncertainty we attach to it. Those two errors can have different effects on rejection.

Bias divided by standard deviation measures how far the estimated difference is centred from zero, in sampling standard deviations. The variance ratio compares the average squared standard error with the variance of the estimated difference across repetitions.

In the uniform four-by-four example, the two MI estimates have the same expected bias, so their biases cancel in the difference. The variance ratio is about 0.83, which means we're underestimating uncertainty. The larger cutoff brings rejection from about 8.35% to 4.90%.

In the same-skew example, the biases again cancel, but the variance ratio is about 1.93. We're overestimating uncertainty, and Wald already rejects less than 1% of the time. Expanded Welch lowers that further. The test becomes more conservative: its false-positive rate falls further below 5%.

In the different-skew example, the variance estimate is similarly inflated, but the residual biases don't cancel. The estimated difference is centred about two sampling standard deviations above zero. Both tests reject about a quarter of the time.

Raising the cutoff doesn't move that estimated difference back towards zero. The two tests can therefore agree on a rejection while sharing the estimation error that helped produce it.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the probability of rejecting equal MI when the population MI values really differ.

This graph covers all 360 power settings at the same nominal 5% significance level. It shows the power lost with Expanded Welch compared with Wald, in percentage points. The line is the median across 36 settings at each sample size, and the shading covers their full range. That shaded range shows variation between population settings, rather than uncertainty in a single estimated rate.

Because Expanded Welch's rejections are a subset of Wald's, its power can only stay the same or fall. At ten observations, the median loss is about six percentage points. Unsuccessful calculations also contribute there. By 10,000 observations, the loss is below 0.32 percentage points in every setting.

These rates use the usual thresholds, so the methods can have different actual false-positive rates. We need to read the power loss alongside the null results before judging the trade-off.

The two methods being close doesn't necessarily mean that either has high power. Even at 50,000 observations, Expanded Welch power for the smallest MI gap ranges from about 80% to 96%. The two larger gaps exceed 99.9%.

There's another issue here: these power rates count rejections in either direction, including those where the estimated difference points the wrong way.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map shows populations with different category frequencies and an MI gap of 0.01 nats. Q always has greater population MI.

Each percentage tells us how often the estimated difference wrongly suggests that P has greater MI, among samples where Expanded Welch rejects. The denominator is the number of rejections. For example, 90% would mean nine out of ten rejections have the wrong estimated direction, rather than nine out of ten samples. The displayed values are rounded.

In parts of the range with sparse, larger tables, almost every rejection points the wrong way.

Take the outlined sixteen-by-sixteen example, with 1,000 observations per population. The difference is MI in P minus MI in Q, so the true difference is minus 0.01 nats. But the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9% of those rejections have the wrong estimated sign.

Here, unequal residual biases have outweighed the true gap. The positive bias has carried the average estimate past zero, reversing its sign. A larger cutoff changes how often we reject, but it leaves that bias in place.

Increasing sample size reduced the problem in these simulations. At 10,000 observations, fewer than 0.4% of rejections have the wrong sign in every setting across the full power grid.

Across all 360 settings, 28 have at least 90% of rejections pointing the wrong way. All have different category frequencies between populations. Those rejections count towards two-sided power, even though they don't reliably identify which population has greater MI.

## Slide 13: Conclusions and next steps

I derived the MI-specific variance sensitivity and used it to estimate degrees of freedom for Expanded Welch.

The larger cutoff brings many excessive false-positive rates closer to 5%. But it also lowers rejection when the rate is already too low, and it costs power at the same nominal significance level.

The approximation checks and the wrong-direction results help explain what's left unresolved. Near independence, the first-order calculation misses quadratic sampling variation. In sparse tables, unequal residual biases can outweigh the real MI difference.

I evaluated one population construction with equal sample sizes, using Wald as the main benchmark. The next steps are to improve the MI-difference and standard-error estimates, account for the additional variation near independence, and test broader populations and unequal sample sizes.

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

### 4. Why does the approximation struggle near independence?

- At independence, population pointwise MI and its first-order sampling contributions vanish. Squared probability errors still produce apparent association in sampled tables.
- On Slide 8, the population first-order value is about 0.1, while the mean sample-based estimate is about 4.9 because it retains that apparent association.
- The repeated-sample moment target is about 9.1. Including quadratic sampling noise helps explain the separation, but does not establish an exact replacement test.

### 5. Why this simulation design, and why 100,000 repetitions?

- The copying model controls MI while preserving chosen category frequencies, giving known population truth. It represents one association family.
- The 360 null and 360 power settings vary table size, frequencies, sample size, and association to expose different estimation problems.
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
- Further work should retain additional sampling variation near independence and evaluate other association patterns and unequal sample sizes. There is no universal sample-size rule established here.
