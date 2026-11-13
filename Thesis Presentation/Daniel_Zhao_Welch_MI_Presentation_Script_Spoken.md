# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, measures how much knowing one variable reduces uncertainty about another, on average. If knowing X changes the probabilities we'd assign to Y's categories, X gives us information about Y. MI averages that information over possible outcomes, giving zero when the variables are independent and a positive value when they're associated.

The hypotheses below that definition compare two populations, whose joint probability tables I'll call P and Q. The null says their population MI values are equal, while the two-sided alternative says they differ in either direction.

The diagram on the left shows how we estimate those values. We take a sample from P, summarise its categorical observations in a count table, and calculate an MI estimate. We repeat that for Q, using the same definitions of X and Y.

On the right, the statistical task starts with those two estimates. New samples give us different counts and different MI estimates, even when the population MI values are equal. So the question at the bottom is whether the observed difference is too large to explain by sampling noise alone.

## Slide 3: Literature review: foundations and the MI-specific step

The left column gives us an MI estimator, a leading bias correction, and a first-order approximation for its sampling variance. The step I need is to work out how much the variance estimate itself changes between samples.

In the middle is the Wald test. It divides the estimated difference by its estimated standard error, then uses the standard normal distribution as its reference. A reference distribution here approximates how the statistic behaves when the population MI values are equal. I check how well the resulting cutoff works in finite samples.

The right column introduces Welch–Satterthwaite moment matching. It uses the mean and variability of estimated variance contributions to choose degrees of freedom, with related applications to entropy and regression. Applying that principle to MI requires an MI-specific calculation of variance sensitivity.

At the bottom are my three steps: derive that sensitivity, use it to construct the Expanded Welch test, and compare the two tests in simulations.

## Slide 4: Method: one statistic, two reference distributions

In the box on the left, both tests divide the bias-corrected estimate of the MI difference by its estimated standard error. A statistic of plus two means the estimated difference is two standard errors above zero. The sign tells us which population has the higher estimate. For the two-sided test, what matters is how far the statistic is from zero.

The second equation explains the standard error. Pointwise MI is a category pair's information contribution, and V-hat estimates the variance of those contributions. Dividing by sample size estimates the sampling variance of MI. Independence between the two samples lets us add their variance contributions to get the squared standard error.

In the blue box, the Wald test uses the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the orange box, the Expanded Welch test uses a Student t distribution as its reference. I estimate the degrees of freedom from the tables to account for how much the variance estimates can vary.

The graph on the right shows a Student t distribution with five degrees of freedom. Its heavier tails give a larger cutoff, about 2.57. The degrees of freedom will vary from sample to sample. The larger they are, the closer the cutoff gets to the one used by the Wald test.

Since both tests use the same statistic and the Expanded Welch cutoff is larger, every Expanded Welch rejection is also a Wald rejection. So how do I choose the degrees of freedom that set that cutoff?

## Slide 5: Approach and contributions

The chain on the left starts with V, the population variance of pointwise MI. I want to know how its estimate, V-hat, varies between samples.

In the first box, I move a small amount of probability towards one cell, reducing the other probabilities proportionally.

In the second box, I track what that shift changes: the cell weights, the row and column margins, and the log ratios that give pointwise MI. For example, when a row total changes, so do the log ratios elsewhere in that row. Holding pointwise MI fixed would miss that effect.

In the third box, I call the combined sensitivity g. A positive g means shifting probability towards that cell initially raises V, and a negative g means it lowers V. Each cell has its own value of g, so the value we get depends on which cell a random observation lands in.

In the fourth box, tau-squared is the variance of those sensitivities when observations are drawn from the population. The more they vary, the more a change in the mix of sampled outcomes can affect V-hat.

In the first equation below, tau-squared divided by sample size approximates the sampling variance of V-hat. In the second equation, I use V-hat and estimated tau-squared from the table for P to calculate its component degrees of freedom. That's the value for one population. I repeat the calculation for Q, then combine the two using the Welch–Satterthwaite rule.

There are two approximations behind those equations, shown on the right. First, the first-order expansion keeps the linear effect of changes in cell probabilities. That makes the error in V-hat approximately the average of the sensitivities in the sample. The sensitivities have mean zero, so the approximation puts the mean of V-hat at V. The observations are independent, so the variance of the average is tau-squared divided by sample size.

Second, I use moment matching to fit a scaled chi-squared distribution to that mean and variance. For a given mean, more variation gives fewer degrees of freedom. The sensitivity g comes from an exact derivative when the population cell probabilities are positive. The simulations check how well the approximations built on it work.

## Slide 6: Evaluation design

The research questions on the left separate that evaluation into three parts.

RQ1 checks the sampling moments and component degrees of freedom, including when population MI is close to zero.

RQ2 checks false-positive rates at the three equal MI values shown. MI is in nats because I use natural logarithms.

RQ3 checks power. I hold MI in P at 0.02 nats and give Q the higher value, using the three gaps shown.

On the right, there are four table sizes, from two by two to sixteen by sixteen. The margin labels describe the category frequencies: uniform means equally frequent, same-skew means uneven in the same way in both populations, and different-skew means uneven in different ways. With ten sample sizes, from 10 to 50,000 observations per population, there are 360 settings in each of the false-positive and power studies.

I draw 100,000 independent table pairs per setting and give both tests the same pairs. Each test still runs on one pair at a time.

The model line shows how I set population MI. I draw X, then either copy its category into Y or draw Y independently from the same frequencies. I adjust the probability of copying to reach each target MI without changing the category frequencies.

At the bottom, both tests use a 5% significance level. If a calculation fails, I count it as a non-rejection and report calculation success separately.

## Slide 7: RQ1 results: approximation accuracy

This is population P from a different-skew setting, with four-by-four tables and MI of 0.02 nats. Both graphs vary sample size and check the two moments that determine the degrees of freedom.

The top graph compares average V-hat with population V, so one means the first-order mean approximation agrees with the simulations. The curve rises above that benchmark before returning towards it.

The orange box on the right points to rare cells. When a rare category pair shows up in a sample, its pointwise MI can be far from the table's MI. V-hat uses the square of that gap, so a large gap can push it up. Larger counts stabilise the estimates, but at 1,000 observations the mean is still 19% above V.

The lower graph divides predicted sampling variance by observed sampling variance. Below one means the prediction is too low, and above one means it is too high.

The navy curve uses population inputs. Rare cells appearing in some samples but not others can produce changes larger than the linear approximation predicts. At the same sample size of 1,000, this prediction is about 3% low.

The orange curve estimates the inputs from each sampled table and averages the predictions. Estimating sensitivities from sparse counts can instead overpredict the variation; at that sample size, the prediction is about 8% high.

Look at the summary at the bottom. The population inputs give us a fairly accurate prediction of the variance even though they give us too low a mean. Moment matching squares the mean, so using that lower value can push the degrees of freedom down.

## Slide 8: RQ1 results: near independence

Here the table size stays four by four and sample size stays at 1,000, while population MI varies towards zero. The horizontal axis is population MI and the vertical axis is component degrees of freedom, both on logarithmic scales.

Start with the charcoal line. It is the moment-matching target, calculated from V-hat's mean and variance across repeated samples. At the smallest MI shown, one ten-thousandth of a nat, the target is about 9.1.

The dotted navy line uses known population inputs in the first-order formula, as explained in the upper-right box. Close to zero MI, this component value is approximately sample size times population MI, so it heads towards zero. At the same MI value it is about 0.1, far below the target.

The orange line averages the degrees of freedom from sampled tables. As the lower-right box explains, at zero population MI the linear term vanishes, but squared probability errors can still give a positive MI estimate. The calculation from each table picks up that noise, so at the smallest MI shown its average is about 4.9.

At the bottom, the sample-based estimate averages about half the target. Hitting that target would still leave us with a question: how often do the tests reject when population MI is equal?

## Slide 9: RQ2 results: false positives across all null settings

The plot contains all 360 null settings, where population MI is equal and every rejection is a false positive. Each point is one setting. The horizontal axis shows the false-positive rate of the Wald test, and the vertical axis shows the rate for Expanded Welch. The dashed lines mark the 5% target.

The diagonal means equal rejection rates. All points lie on or below it because Expanded Welch can only reduce rejection.

Start with the top box on the right. The Wald test is above 5% in 178 settings, and Expanded Welch gets closer to 5% in 165 of them. The highlighted uniform example goes from 8.35% to 4.90%.

In the next box, the Wald test is below 5% in 180 settings. Expanded Welch pushes the rate even lower in 176 of those and leaves four unchanged. The two remaining settings have a Wald false-positive rate of exactly 5%.

At the bottom right, the counts in the 4% to 6% band are close: 130 for the Wald test and 136 for Expanded Welch. Now look at the circled different-skew example: sixteen by sixteen, MI of 0.005 nats, and 1,000 observations per population. Its false-positive rate falls from about 36% to about 34%, still far above 5%.

To see why a larger cutoff helps in some settings and does little in others, let's look at the estimated difference and its standard error.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

All three rows use equal MI of 0.02 nats, and every calculation succeeds. The bias column shows how far the average estimated difference is from zero, in sampling standard deviations. In the next column, one means the average squared standard error matches the observed variance of the estimated difference.

Start with the uniform four-by-four tables in the first row, with 20 observations per population. The biases in the two MI estimates cancel in expectation, so the difference is centred near zero. But the variance ratio is below one. For a given difference, too small a standard error puts the statistic further from zero. As the first box shows, the larger cutoff offsets that here, bringing the false-positive rate from 8.35% to 4.90%.

The second row uses same-skew sixteen-by-sixteen tables with 1,000 observations per population. The biases again cancel in expectation, but the variance ratio is nearly two. That overstatement of uncertainty helps explain why the Wald test rejects only about 0.6% of the time. The larger cutoff makes it more conservative, pushing it further below 5% to about 0.5%.

The third row keeps the table size and sample size but uses different-skew margins. The variance ratio is still nearly two, but now the estimated difference averages about two sampling standard deviations above zero. The false-positive rate only falls from about 26% to about 25%. As the final box shows, changing the cutoff leaves that bias in place.

The takeaway at the bottom is that a larger cutoff can offset a standard error that's too small, but it leaves the bias in the estimated difference unchanged.

## Slide 11: RQ3 results: the power cost of the larger cutoff

The graph shows how much power Expanded Welch loses compared with the Wald test, in percentage points. Power is the chance of rejecting equal MI when the population values really differ. Every Expanded Welch rejection is also a Wald rejection, so Expanded Welch can't have higher power here.

The graph covers all 360 power settings. Its line is the median across 36 settings at each sample size, while the shading spans the full range across those settings.

The upper-right box summarises the small-sample cost. With ten observations per population, the median loss is about six percentage points, partly because some calculations fail. From 50 to 1,000 observations, the median loss is about one point. By 10,000, even the largest loss is less than a third of a percentage point.

Both tests use the same 5% significance level, but their actual false-positive rates can differ. So read the power comparison alongside the false-positive results we've just seen.

The lower-right box concerns absolute power. Even at 50,000 observations, the smallest MI gap of 0.005 nats gives Expanded Welch power of about 80% to 96%. Power is above 99.9% for the two larger gaps. So the two tests can have similar power and still miss the smallest MI gap.

The definition at the bottom also counts rejections in either direction. It does not check whether the estimated sign identifies the population with greater MI, which is the next result.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map uses different category frequencies and an MI gap of 0.01 nats, with Q always having greater population MI. Rows identify table size and columns identify sample size.

Each cell shows the share of Expanded Welch rejections that point to the wrong population. As the caption explains, 50% means about half the rejections for that setting point to P as having higher MI.

The dark cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range.

The upper-right box explains the outlined sixteen-by-sixteen cell at 1,000 observations per population. Q truly has more MI, by 0.01 nats. On average, the estimate points the other way and puts P ahead by about 0.02 nats. Expanded Welch rejects in about 10% of repetitions. Almost every one of those rejections points to P.

The next box explains why. The bias left after correction is different for P and Q, and the difference is enough to reverse the gap on average. The cutoff can't undo that shift. By 10,000 observations per population, fewer than 0.4% of rejections pointed the wrong way in every setting in the power study.

At the bottom is the tally across all 360 power settings. In 28 settings, all different-skew, at least 90% of rejections point the wrong way. Those rejections still count towards two-sided power.

## Slide 13: Conclusions and next steps

The top row separates three contributions.

First, I derived how changes in the probability table affect the pointwise-MI variance. That gives a way to approximate how its estimate varies from sample to sample.

Second, I used that approximation to estimate degrees of freedom for the Student t distribution. The test statistic is the same one used by the Wald test.

Third, I used simulations to check the approximations and compare the tests, including how often the calculations succeed.

The next row separates the findings by research question.

For RQ1, the approximations generally get better with larger samples. Near zero MI, the first-order calculation misses the noise from the squared probability errors we saw on Slide 8.

For RQ2, the larger cutoff brings many excessive false-positive rates closer to 5%, but pushes them further below 5% when the Wald test already rejects too rarely.

For RQ3, Expanded Welch can't have higher power than the Wald test at the same 5% significance level. A large enough bias can also make rejections point to the wrong population.

These findings come from one way of constructing populations, equal sample sizes, and a comparison with the Wald test.

The first next step is to reduce bias in the estimated MI difference and improve its standard error and degrees of freedom, including when population MI is close to zero.

The second is to evaluate other population constructions and unequal sample sizes.

Overall, the cutoff adjustment helps in some settings, but reliable comparisons also require accurate estimates of the MI difference and its standard error.

Thank you.

## Questions and answer guides

### 1. What is your main contribution?

- I derived the MI-specific sensitivity of the pointwise-MI variance as the cell probabilities, margins, and log ratios change.
- That gives the sampling-variance approximation needed to estimate component degrees of freedom and combine them using the established Welch–Satterthwaite rule.
- I evaluated approximation accuracy, false positives, power, and calculation success. Keeping the same estimated difference and standard error as the Wald test lets me isolate the effect of changing the reference distribution.

### 2. What do V, g, and tau-squared actually mean?

- V measures variation in pointwise MI across outcomes. V-hat estimates it from one table, and V-hat divided by n estimates MI's sampling variance.
- g measures how sensitive V is to shifting probability towards a particular cell, including the resulting changes in the margins. Slide 16 gives the cell formulas, and Slide 17 works through an example.
- Tau-squared is the variance of those sensitivities across outcomes. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of the sensitivities.

### 3. Where do the degrees of freedom come from, and is the Student t distribution exact?

- A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching moments gives nu as twice the squared mean divided by the variance.
- Approximating those moments by V and tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table.
- The Student t distribution is the reference distribution, an approximation under equal population MI. Matching moments does not establish independence between the estimated MI difference and the variance estimates.

### 4. Why does the approximation struggle when population MI is close to zero?

- When population MI is zero, all population pointwise-MI values are zero, and the first-order sampling terms for MI and V-hat vanish. Squared probability errors still produce positive estimated MI.
- On Slide 8, the population first-order value is about 0.1, while the mean sample-based estimate is about 4.9 because its calculation retains positive estimated MI from sampling noise.
- The repeated-sample moment target is about 9.1. Accounting for the squared probability errors helps explain the separation between the lines. That explanation does not establish an exact replacement test.

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
- Where uncertainty is overestimated and the Wald test already rejects too rarely, the larger cutoff lowers the false-positive rate further below 5%.
- Substantial difference bias can leave both tests unreliable. In the diagnostic different-skew example, both reject about a quarter of the time despite equal population MI.

### 8. If it loses power, is the comparison fair or the method useful?

- At the same 5% significance level, every Expanded Welch rejection is also a Wald rejection, so its power can only stay the same or fall.
- Reducing excessive false positives may justify some power loss, but reducing an already-low rate makes conservatism worse.
- The power comparison uses the tests' usual rules. Their actual false-positive rates can differ, so assess the power loss alongside the change in false positives.

### 9. What does the wrong-direction result mean?

- Population MI really differs, so these are rejections under an alternative. The error is that the estimated sign identifies the wrong population as having greater MI.
- In the highlighted example, the true difference is −0.01, but its estimated mean is about +0.0207 because the biases remaining after correction differ enough to outweigh the gap.
- Of 9,662 rejections, 9,659 point the wrong way. That is over 99.9% of the rejections. Two-sided power counts those rejections.

### 10. Why not use permutation or bootstrap instead?

- Simple group-label permutation requires exchangeability. Equal MI allows different joint distributions, so it does not supply that condition.
- Separate-sample bootstrapping is a candidate, but an ordinary empirical bootstrap cannot generate cells absent from the observed table, and estimation bias can remain.
- I did not conduct a full resampling comparison. The thesis cannot establish superiority over those alternatives.

### 11. What assumptions and calculation rules matter most?

- Observations are independent and identically distributed within each population, with independent samples, fixed, aligned categories, positive population cell probabilities, and positive V and tau-squared for the first-order construction.
- Positive population probabilities still allow empty sampled cells, which are retained. Successful calculations require a positive finite standard error and, for Expanded Welch, positive finite degrees of freedom.
- Failed calculations count as non-rejections, with success reported separately. They contribute to some small-sample power loss but do not explain the highlighted failures where every calculation succeeds.

### 12. What is your overall conclusion, and what would you improve next?

- Expanded Welch improves some excessive false-positive rates, but its larger cutoff also increases conservatism and can reduce power at the same 5% significance level.
- I would first improve the MI-difference and standard-error estimates, changing one at a time to identify what resolves the failures.
- Further work should retain additional sampling variation when population MI is close to zero and evaluate other population constructions and unequal sample sizes. There is no universal sample-size rule established here.
