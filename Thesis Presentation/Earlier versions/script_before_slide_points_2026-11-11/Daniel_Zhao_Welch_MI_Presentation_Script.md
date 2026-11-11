# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, tells us how much knowing one variable reduces uncertainty about another, on average. If knowing X changes the probabilities we'd assign to Y's categories, then X gives us information about Y, and MI averages that gain over the possible outcomes. That average is zero when the variables are independent and positive when they're associated.

I'm interested in whether that MI value differs between two populations, whose joint probability tables I'll call P and Q. We can't observe those population tables directly, so we take a sample from each, summarise the observations in count tables, and estimate MI from the counts.

Those counts fluctuate between samples, which means the two estimates can differ even when population MI is equal. An estimated difference on its own therefore doesn't tell us whether the populations have different MI values.

We test the null hypothesis that population MI is equal, against a two-sided alternative that it differs. To make that decision, we need an estimate of how much the MI difference would vary under repeated sampling.

## Slide 3: Literature review: foundations and the MI-specific step

Existing research provides that starting point: an MI estimator, a correction for its leading bias, and a first-order approximation to its sampling variance. The Wald test uses those results to compare an estimated MI difference with its standard error, taking the standard normal distribution as its reference.

That standard error is itself estimated from the sampled tables. The Welch–Satterthwaite approach accounts for its variability when choosing degrees of freedom, with related applications of moment matching to entropy and other statistical comparisons.

To use that principle for MI, we need the sampling variability of the variance estimates making up the standard error. Each category pair has a pointwise-MI contribution, but those contributions are also calculated from the table.

A new sample therefore changes both their probability weights and their values. For example, changing a row total alters the log ratios for cells in that row, including cells whose own counts haven't changed.

Tracking those changes together gives the MI-specific variance sensitivity. I use it to approximate how much the variance estimate changes between samples, then obtain the degrees of freedom needed for the comparison.

## Slide 4: Method: one statistic, two reference distributions

Both tests begin by expressing the estimated MI difference relative to the same estimated uncertainty. After applying the leading bias correction, we divide the difference by its estimated standard error to get the shared statistic.

A statistic of two means the estimated difference is twice its estimated standard error. Its sign identifies which population has the higher estimate, while the two-sided test uses its magnitude.

The standard error comes from the pointwise-MI variance estimates. Here, V-hat estimates how much those contributions vary, and dividing it by sample size estimates the sampling variance of MI. Independence between the two samples lets us add their variance contributions to get the squared standard error.

The tests then differ in the cutoff used to judge this ratio. Wald uses the standard normal distribution, giving a two-sided 5% cutoff of about 1.96. Expanded Welch uses a Student t distribution, with estimated degrees of freedom intended to reflect uncertainty in the variance estimate.

The Student t distribution illustrated here has five degrees of freedom and a cutoff of about 2.57. In the actual test, we estimate the degrees of freedom from the tables: smaller values give a larger cutoff, while increasing them brings it closer to Wald's.

Under these calculation rules, Expanded Welch only rejects when Wald also rejects. Its potential benefit is therefore a reduction in excessive false positives, accompanied by a possible loss of power. To choose that cutoff from the data, we need to quantify uncertainty in the variance estimates.

## Slide 5: Approach and contribution

That requires keeping two kinds of variation separate. V describes how pointwise MI varies across outcomes, while V-hat estimates V from a sampled table. Choosing degrees of freedom requires knowing how much V-hat itself changes between samples.

We can approximate that whole-table change by working out the effect of each possible observation. I start by slightly increasing the probability assigned to one cell, while reducing the other probabilities proportionally, and call the sensitivity of V to that change g.

The sensitivity includes changes in the cell weights, margins, and pointwise-MI values. A positive g means the shift initially raises V, whereas a negative g means it lowers V.

For a fixed population and cell, g is fixed. But drawing an outcome X and Y randomly selects which cell's sensitivity we observe, so g evaluated at X and Y is a random quantity.

The first-order expansion connects those individual sensitivities to the whole table: it approximates the error in V-hat by their average across the sampled observations. The sampling variance of V-hat therefore depends on how much those sensitivities vary.

I call that sensitivity variance tau-squared. Because the observations are independent, the variance of their average is tau-squared divided by sample size, giving our first-order sampling-variance approximation for V-hat.

The sensitivities have mean zero, so at first order we also approximate V-hat's sampling mean by V. We now have both inputs for moment matching: a mean and a sampling variance. Matching them to a scaled chi-squared distribution determines the component degrees of freedom, with greater variability relative to the mean giving fewer degrees of freedom.

We estimate the inputs for P and Q and combine the components using the Welch–Satterthwaite rule. The derivative defining g is exact for positive population tables, but the sampling expansion and Student t reference distribution are approximations. I therefore check the moment approximations before assessing the test's false positives and power.

## Slide 6: Evaluation design

To check those approximations and the resulting test decisions, I use populations with known MI and the three research questions on the left.

The first checks the sampling moments and degrees of freedom. The second asks how often the tests reject when population MI is equal, while the third checks power when it differs. For power, MI in P is fixed at 0.02 nats and Q has greater MI. Nats are the units we get from natural logarithms.

These questions require both null and alternative populations. On the right, the shared design gives each of the false-positive and power studies 360 settings, varying table size, category frequencies, sample size, and MI.

The frequency regimes include uniform category frequencies, the same uneven frequencies in both populations, and different uneven frequencies. Varying these frequencies changes which combinations are rare and allows the two populations to have different estimation biases.

For each setting, I draw 100,000 independent table pairs and give both tests the same pairs. Repetition estimates performance more precisely, while each individual test still uses only the stated sample size.

To generate those populations, I use the copying model at the bottom of the design panel. I first draw X, then either copy its category into Y or draw Y independently from the same category frequencies. Changing how often I copy changes population MI while keeping those frequencies fixed, and a numerical search finds the copying probability for the target MI.

Finally, the reporting line at the bottom applies to both tests: we use a nominal 5% significance level. Unsuccessful calculations count as non-rejections, with calculation success reported separately.

## Slide 7: RQ1 results: approximation accuracy

The degrees-of-freedom calculation needs both the mean and sampling variance of V-hat, so this figure checks those inputs separately.

The top graph of this four-by-four example checks the first-order mean approximation by comparing average V-hat with population V. A ratio of one means agreement.

The average estimate rises above the population value before coming back down. As rare cells first appear, their estimated pointwise-MI values can be far from the table's MI, producing large squared deviations that inflate V-hat until larger counts stabilise the estimates. Even at 1,000 observations, average V-hat is still 19% above V.

The other input, sampling variance, is checked in the lower graph. The navy curve uses population inputs, testing the first-order formula itself. The orange curve estimates the inputs from each sampled table and averages the predictions, showing how estimating the inputs changes the prediction.

Here, one means agreement with the variance observed across repetitions. Below one we predict too little variation; above one we predict too much.

Rare cells appearing in some samples but not others can produce changes larger than linearisation predicts, while estimating sensitivities from sparse counts can also overpredict that variation. At the same sample size of 1,000, the population-based prediction is about 3% low and the sample-based prediction about 8% high.

That fairly accurate variance prediction still coexists with the inflated mean above. Because moment matching uses the mean squared, replacing the larger sampling mean with V can push degrees of freedom down even when the sampling variance is predicted well.

## Slide 8: RQ1 results: near independence

The previous figure varied sample size for a fixed population. Here, we hold sample size at 1,000 and reduce population MI towards zero to examine what happens when the MI value itself is small.

The charcoal line is the component moment-matching target, calculated from the mean and variance of V-hat across repeated samples. We compare that benchmark with the dotted navy population-based first-order value and the orange mean of the estimates calculated from individual sampled tables.

At the smallest population MI value shown, the target is about 9.1. The population-based formula gives about 0.1, while the mean sample-based estimate is about 4.9.

Near zero population MI, the component degrees of freedom from population inputs are approximately sample size times MI, so they head towards zero. But sampled counts still fluctuate and can produce positive estimated MI even when population MI is zero.

At zero population MI, the linear contribution to the error in V-hat vanishes, while squared probability errors still produce variation. The first-order calculation misses those quadratic terms, whereas the sample-based calculation retains positive MI produced by sampling noise.

Keeping that noise in a quadratic approximation predicts a mean estimate of about 4.6, close to the observed 4.9, and helps explain the orange line's position below the target.

Even matching the moment target wouldn't establish the Student t distribution for the full statistic. Expanded Welch has to choose a cutoff from each sampled pair, so I next check how often those cutoffs reject equal population MI.

## Slide 9: RQ2 results: false positives across all null settings

This chart answers that question across all 360 null settings. Population MI is equal, so every rejection is a false positive, and an accurately calibrated 5% test would reject in about one experiment out of twenty at each setting.

Each point represents one setting, with Wald's false-positive rate on the horizontal axis and Expanded Welch's on the vertical. The diagonal means equal rates, and the dashed lines mark 5%.

Every point is on or below the diagonal because Expanded Welch can only reduce rejection. Whether that helps depends on where Wald starts: on the right, where Wald exceeds 5%, the reduction moves closer to the target in 165 of 178 settings.

On the left, where Wald is already below 5%, none of the 180 settings improves, because rejection either falls further or stays the same.

The upper-right example shows the limit of the improvement: Expanded Welch still rejects more than 34% of the time under equal MI. The cutoff changes, but the estimated MI difference and standard error do not, so errors in those shared inputs can remain in both tests.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These three examples examine those inputs under equal population MI, with every calculation successful. Bias shifts the centre of the estimated difference, while error in its estimated variance changes how much uncertainty we attach to it.

Bias divided by standard deviation measures the shift from zero in sampling standard deviations. The variance ratio compares the average squared standard error with the variance of the estimated difference across repetitions.

In the uniform four-by-four example, the two MI estimates have the same expected bias, so their biases cancel in the difference. The variance ratio is about 0.83, indicating underestimated uncertainty. For a given difference, a smaller standard error gives a larger absolute statistic, and the larger cutoff partly offsets that, bringing rejection from about 8.35% to 4.90%.

In the same-skew example, the biases again cancel, but the variance ratio is about 1.93. The oversized uncertainty estimate reduces the magnitude of the statistic, so Wald already rejects less than 1% of the time. Raising the cutoff lowers that rate further below 5%, making the test more conservative.

In the different-skew example, the variance estimate is similarly inflated, but unequal residual biases move the estimated difference about two sampling standard deviations above zero. That shift helps explain why both tests reject about a quarter of the time despite the large uncertainty estimate.

The cutoff changes the rejection boundary, without moving the estimated difference back towards zero. The same reduction in rejection also applies when population MI really differs, which leads to the power cost.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the probability of rejecting equal MI when the population MI values really differ. Expanded Welch's rejections are a subset of Wald's, so it cannot have higher power at the same nominal level. The reduction in rejection can therefore also mean missing real differences.

This graph covers all 360 power settings at the same nominal 5% significance level and shows the loss with Expanded Welch compared with Wald, in percentage points. The line gives the median across 36 settings at each sample size, while the shading spans their full range across populations.

At ten observations, the median loss is about six percentage points, with unsuccessful calculations also contributing. By 10,000 observations, the loss is below 0.32 percentage points in every setting.

That describes the methods under their usual thresholds, rather than at matched actual false-positive rates. We therefore interpret the loss alongside the null results: reducing power accompanies an improvement in some settings and greater conservatism in others.

Closeness between methods also doesn't imply high power. Even at 50,000 observations, Expanded Welch power for the smallest MI gap ranges from about 80% to 96%, while the two larger gaps exceed 99.9%.

These are two-sided rejection rates, so they count a rejection even when the estimated difference has the wrong sign. The residual bias seen in the null examples makes it important to check that direction as well.

## Slide 12: RQ3 results: bias can reverse the estimated direction

Here, Q always has greater population MI, so we can check whether the estimated direction agrees with that known ordering. The heat map uses different category frequencies and an MI gap of 0.01 nats.

Each percentage tells us, among samples where Expanded Welch rejects, how often the estimated difference wrongly suggests that P has greater MI. The displayed values are rounded, so 90% means roughly nine out of ten rejections point the wrong way, rather than nine out of ten samples.

In parts of the range with sparse, larger tables, almost every rejection points the wrong way. Take the outlined sixteen-by-sixteen example, with 1,000 observations per population. Our difference is MI in P minus MI in Q, so its true value is minus 0.01 nats, but its estimated mean is about plus 0.0207.

Expanded Welch rejects about one time in ten, and more than 99.9% of those rejections have the wrong estimated sign. Unequal residual biases have carried the average estimate past zero and reversed it, outweighing the true MI gap. Changing the cutoff leaves that bias in the shared estimate.

Increasing sample size reduced this problem in these simulations: by 10,000 observations, fewer than 0.4% of rejections have the wrong sign in every setting across the full power grid.

Across all 360 settings, 28 have at least 90% of rejections pointing the wrong way, and all have different category frequencies between populations. Those rejections count towards two-sided power, but don't reliably identify which population has greater MI.

## Slide 13: Conclusions and next steps

The thesis derives the MI-specific variance sensitivity and uses it to estimate degrees of freedom for Expanded Welch. That calculation changes the rejection cutoff while retaining Wald's estimated difference and standard error.

Its larger cutoff brings many excessive false-positive rates closer to 5%, but lowers rejection further where the rate is already too low. The same change costs power at the nominal significance level, and it cannot remove the residual bias that can reverse the estimated direction.

The evaluation used one population construction, equal sample sizes, and Wald as the main benchmark.

The remaining errors make estimation accuracy the priority: I would improve the MI-difference and standard-error estimates and account for the quadratic sampling variation missed when population MI is close to zero. A broader evaluation should also cover other population constructions and unequal sample sizes.

My overall finding is that adjusting the cutoff can improve some comparisons, but reliable inference also depends on estimating the MI difference and its uncertainty accurately.

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
