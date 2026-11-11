# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone. Today I'll talk about comparing mutual information between two populations.

When we only have a sample from each population, an estimated difference could reflect a real difference, or it could come from sampling variation. My thesis develops the Expanded Welch test for this comparison and investigates when it improves on the Wald test.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, tells us how much knowing one variable reduces uncertainty about another, on average. It's zero when the variables are independent, and positive when they're associated.

I'm interested in whether that association differs between two populations. I'll call their joint probability tables P and Q.

We take a sample from each population, put the observations into count tables, and estimate MI from those counts. But if we collected new samples, we'd generally get different estimates. So even when population MI is equal, the two estimates can differ.

That's the reason for testing. The null hypothesis says the population MI values are equal. The two-sided alternative says they're different. We need to decide whether the observed difference is large relative to its sampling uncertainty.

## Slide 3: Literature review: foundations and the MI-specific step

Existing research gives us an MI estimator, a correction for its leading bias, and an approximation to its sampling variance. The Wald test uses those results with the standard normal distribution as its reference.

The Welch–Satterthwaite approach uses the variability of estimated variances to choose degrees of freedom. Related work applies moment matching to entropy and other statistical comparisons.

Applying that approach here requires an extra calculation: how much does the pointwise-MI variance estimate change between samples?

Changing a table affects its cell weights, row and column totals, and pointwise-MI values together. I derive their combined effect, then use that result to estimate degrees of freedom for the test.

## Slide 4: Method: one statistic, two reference distributions

The two tests start with exactly the same statistic. We estimate the MI difference, apply the same leading bias correction, and divide by the same estimated standard error.

Pointwise MI is the information contribution of one category pair. V-hat estimates the variance of those contributions. Dividing by sample size estimates the sampling variance of MI. The samples are independent, so we add their two variance contributions to get the squared standard error.

The standard error itself also changes between samples. Expanded Welch uses estimated degrees of freedom and a Student t distribution so that the cutoff reflects uncertainty in the variance estimate.

In the graph, the Wald test uses the standard normal distribution, giving a two-sided 5% cutoff of about 1.96. The Student t distribution shown has five degrees of freedom, giving a cutoff of about 2.57. In the actual test, we estimate the degrees of freedom from the tables.

Under these calculation rules, Expanded Welch only rejects when Wald also rejects. The experiments check whether that reduction improves false-positive rates and how much power it costs.

## Slide 5: Approach and contribution

Choosing the degrees of freedom means accounting for two kinds of variation. V describes how pointwise MI varies across outcomes. V-hat estimates V, and that estimate varies from sample to sample.

I start by slightly increasing the probability assigned to one cell, while reducing the other probabilities proportionally. I call the sensitivity of V to that change g. It includes the effects of changing the cell weights, margins, and pointwise-MI values.

Different cells can have different effects. For a sampled outcome X and Y, g tells us the sensitivity associated with that outcome. Tau-squared measures how much those sensitivities vary across outcomes drawn from the population.

We can approximate the error in V-hat by averaging the sensitivities of the sampled observations. Because the observations are independent, the variance of that average is tau-squared divided by sample size.

That gives us the sampling-variance approximation needed for moment matching. The more variable V-hat is relative to its mean, the fewer component degrees of freedom we get. We estimate the inputs for P and Q, then combine the components using the Welch–Satterthwaite rule.

The derivative defining g is exact for positive population tables. Using it to approximate sampling errors, and then using a Student t reference distribution, involves approximations. The first research question checks how well those approximations work.

## Slide 6: Evaluation design

I check the method using populations with known MI.

I construct them using a copying model. First, I draw X. Then I either copy its category into Y or draw Y independently from the same category frequencies. Changing how often I copy changes the association while keeping those frequencies fixed. A numerical search finds the copying probability for the target MI.

The first research question checks the approximations and degrees of freedom. The second checks false positives using equal population MI. The third checks power, with MI in P fixed at 0.02 nats and greater MI in Q. Nats are the units we get from natural logarithms.

The false-positive and power studies each have 360 settings, varying table size, category frequencies, sample size, and MI. For each setting, I draw 100,000 independent table pairs and give both tests the same pairs.

Both tests use a nominal 5% significance level. Unsuccessful calculations count as non-rejections, and I report calculation success separately.

## Slide 7: RQ1 results: approximation accuracy

This example uses a four-by-four population table. The top graph compares the average V-hat with the population value of V. A ratio of one means agreement.

The average estimate rises above the population value before coming back down. When rare cells first appear, their estimated pointwise-MI values can be far from the table's MI. Those large squared deviations can inflate V-hat until larger counts stabilise the estimates.

The lower graph asks how much V-hat itself varies between samples. The navy curve uses population inputs. The orange curve uses inputs estimated from each sample, then averages the predictions. A ratio of one means agreement with the variance observed across repetitions.

At 1,000 observations, the population prediction is about 3% low, and the sample-based prediction is about 8% high. But the average V-hat is still 19% above V.

That matters because moment matching uses both the mean and the variance. Getting the variance approximately right doesn't, by itself, give us accurate degrees of freedom.

## Slide 8: RQ1 results: near independence

For this graph, sample size stays at 1,000 while population MI approaches zero.

The charcoal line is the moment-matching target, calculated from the mean and variance of V-hat across repeated samples. It's our benchmark for the component degrees of freedom.

The dotted navy line uses population inputs in the first-order formula. The orange line is the average of the degrees of freedom estimated from each sampled table.

At the weakest association, the target is about 9.1. The population-based formula gives about 0.1, while the mean sample-based estimate is about 4.9.

To understand that gap, remember that random count fluctuations can make a sampled table look associated even when the population variables are independent. At independence, the linear contribution to the error in V-hat vanishes. But squared probability errors still contribute variation, and the first-order calculation leaves those quadratic terms out.

The sample-based formula picks up this apparent association, keeping its average positive. Including this sampling noise predicts a mean estimate of about 4.6, close to the observed 4.9. That helps explain the orange line's position below the target.

## Slide 9: RQ2 results: false positives across all null settings

Now we can look at the test decisions. All 360 settings here have equal population MI, so every rejection is a false positive.

Each point is one setting. The horizontal axis shows Wald's false-positive rate, and the vertical axis shows Expanded Welch's. The diagonal means equal rates, and the dashed lines mark 5%.

Every point is on or below the diagonal because Expanded Welch can only reduce rejection.

On the right, where Wald exceeds 5%, Expanded Welch moves closer to the target in 165 of 178 settings. On the left, Wald is already below 5%. None of those 180 settings improves: rejection either falls further or stays the same.

The example in the upper right also shows how much can remain unresolved. Expanded Welch still rejects more than 34% of the time, even though population MI is equal.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These three examples help explain those patterns. All have equal population MI, and every calculation succeeds.

Bias divided by standard deviation measures how far the estimated difference is centred from zero, in sampling standard deviations. The variance ratio compares the average squared standard error with the variance of the estimated difference across repetitions.

In the uniform four-by-four example, the two MI estimates have the same expected bias, so their biases cancel in the difference. The variance ratio is about 0.83, which means we're underestimating uncertainty. The larger cutoff brings rejection from about 8.35% to 4.90%.

In the same-skew example, the biases again cancel, but the variance ratio is about 1.93. We're overestimating uncertainty, and Wald already rejects less than 1% of the time. Expanded Welch lowers that further. The test becomes more conservative: its false-positive rate falls further below 5%.

In the different-skew example, the variance estimate is similarly inflated, but the residual biases don't cancel. The estimated difference is centred about two sampling standard deviations above zero. Both tests reject about a quarter of the time.

Raising the cutoff doesn't move that estimated difference back towards zero.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the probability of rejecting equal MI when the population MI values really differ.

This graph covers all 360 power settings at the same nominal 5% significance level. It shows the power lost with Expanded Welch compared with Wald, in percentage points. The line is the median across 36 settings at each sample size, and the shading covers their full range.

Because Expanded Welch's rejections are a subset of Wald's, its power can only stay the same or fall. At ten observations, the median loss is about six percentage points. Unsuccessful calculations also contribute there. By 10,000 observations, the loss is below 0.32 percentage points in every setting.

The two methods being close doesn't necessarily mean that either has high power. Even at 50,000 observations, Expanded Welch power for the smallest MI gap ranges from about 80% to 96%. The two larger gaps exceed 99.9%.

There's another issue here: these power rates count rejections in either direction, including those where the estimated difference points the wrong way.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map shows populations with different category frequencies and an MI gap of 0.01 nats. Q always has greater population MI.

Each percentage tells us how often the estimated difference wrongly suggests that P has greater MI, among samples where Expanded Welch rejects. The displayed values are rounded.

In parts of the range with sparse, larger tables, almost every rejection points the wrong way.

Take the outlined sixteen-by-sixteen example, with 1,000 observations per population. The difference is MI in P minus MI in Q, so the true difference is minus 0.01 nats. But the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9% of those rejections have the wrong estimated sign.

Here, unequal residual biases have outweighed the true gap. A larger cutoff changes how often we reject, but it leaves that bias in place.

Increasing sample size reduced the problem in these simulations. At 10,000 observations, fewer than 0.4% of rejections have the wrong sign in every setting across the full power grid.

Across all 360 settings, 28 have at least 90% of rejections pointing the wrong way. All have different category frequencies between populations. Those rejections count towards two-sided power, even though they don't reliably identify which population has greater MI.

## Slide 13: Conclusions and next steps

I derived the MI-specific variance sensitivity and used it to estimate degrees of freedom for Expanded Welch.

The larger cutoff brings many excessive false-positive rates closer to 5%. But it also lowers rejection when the rate is already too low, and it costs power at the same nominal significance level.

The approximation checks and the wrong-direction results help explain what's left unresolved. Near independence, the first-order calculation misses quadratic sampling variation. In sparse tables, unequal residual biases can outweigh the real MI difference.

I evaluated one population construction with equal sample sizes, using Wald as the main benchmark. The next steps are to improve the MI-difference and standard-error estimates, account for the additional variation near independence, and test broader populations and unequal sample sizes.

My overall finding is that changing the cutoff can help, but reliable comparison also depends on estimating the MI difference and its uncertainty accurately.

Thank you.
