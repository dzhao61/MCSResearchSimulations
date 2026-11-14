# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

## Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, measures how much knowing one variable reduces uncertainty about another, on average. If the variables are independent, MI is zero.

The hypotheses at the top compare MI for the same two categorical variables, X and Y, in populations P and Q. The null says their population MI values are equal. The alternative says they differ.

On the left, each observation gives us a pair: one category for X and one for Y. We count how often each pair occurs and estimate MI from that count table. We do that for each population. Even if the populations have equal MI, those estimates can differ. So the last step on the right asks whether sampling noise could explain the difference we see.

In the example at the bottom, imagine X is a student's mid-semester test grade and Y is their final exam grade, both recorded as categories. The two populations are students before and after generative AI. Does knowing the mid-semester grade tell us as much about the final grade in both groups?

## Slide 3: Literature review: foundations and the MI-specific step

The left column gives us an MI estimator, a leading bias correction, and a first-order approximation for its sampling variance. The step I need is to work out how much the variance estimate itself changes between samples.

In the middle is the Wald test. It uses the standard normal distribution to approximate how the test statistic behaves when population MI is equal. I check how well that cutoff works in finite samples.

The right column introduces Welch–Satterthwaite moment matching. It uses the mean and variance of the estimated variance contributions to choose degrees of freedom. For MI, that requires a new calculation of variance sensitivity.

At the bottom are my three steps: derive that sensitivity, use it to construct the Expanded Welch test, and compare the two tests in simulations.

## Slide 4: Method: one statistic, two reference distributions

In the box on the left, both tests start with the estimated MI in P minus the estimated MI in Q. They correct for the leading bias and divide by the estimated standard error. For example, plus two means the corrected difference is two standard errors above zero. The two-sided test uses the distance from zero in either direction.

In the second equation, V-hat estimates the variance of pointwise MI, the information contribution of each category pair. Dividing V-hat by sample size estimates the sampling variance of MI. The samples are independent, so we add those two estimates to get the squared standard error.

In the blue box, the Wald test uses the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the green box, the Expanded Welch test uses a Student t distribution as its reference. I estimate the degrees of freedom from the tables to account for how much the variance estimates can vary.

On the right, the dashed green curve shows a Student t distribution with five degrees of freedom. Its heavier tails put the 5% rejection region further out, past about 2.57 in either direction. Five is just for illustration. With more degrees of freedom, the cutoff gets closer to the Wald cutoff.

Since both tests use the same statistic and the Expanded Welch cutoff is larger, every Expanded Welch rejection is also a Wald rejection. So how do I choose the degrees of freedom that set that cutoff?

## Slide 5: Approach and contributions

Start with the orange panel on the left. Each dot in this sketch is a V-hat from a different sample of the same size. V-hat measures variation in pointwise MI within one sample. The spread of the dots is a second kind of variation: how much V-hat itself changes between samples. The dashed line marks the population value V.

To explain that spread, look at the middle panel. I start with one cell: if I move a little probability towards it, how quickly does V change? That shift changes the cell weights, the row and column totals, and the pointwise MI values that depend on them. I call that sensitivity g. Its sign tells us whether V initially rises or falls.

A random observation lands in one cell and picks out that cell's g. Tau-squared is the variance of g across observations from the population.

The first-order expansion keeps the linear effect of changes in the table, so the error in V-hat is approximately the average of the sensitivities in the sample. The sensitivities average to zero in the population, so the approximation centres V-hat at V. The observations are independent, so the variance of their average is tau-squared divided by sample size. That's the approximation at the top of the panel.

In the green panel, I use the mean and sampling variance of V-hat to choose degrees of freedom. Matching those two quantities to a scaled chi-squared distribution gives the first formula: twice the squared mean divided by the variance. For a given mean, more variation gives fewer degrees of freedom and a larger cutoff. The second formula uses V as the approximate mean and tau-squared over sample size as the approximate variance, with both inputs estimated from the table for P. That gives the component degrees of freedom, meaning the value for one population.

At the bottom, I repeat the calculation for Q and use the Welch–Satterthwaite rule to combine the two into the degrees of freedom for the Student t distribution. RQ1 checks both approximations.

## Slide 6: Evaluation design

On the left are the three questions. RQ1 checks the approximations, including near zero MI. RQ2 checks false-positive rates when MI is equal, and RQ3 checks power. For the power study, I keep MI in P at 0.02 nats and give Q the higher value. MI is in nats because I use natural logarithms.

On the right, there are four table sizes, from two by two to sixteen by sixteen. The margin labels describe the category frequencies: uniform means equally frequent, same-skew means uneven in the same way in both populations, and different-skew means uneven in different ways. With ten sample sizes and three MI levels or gaps, that gives 360 settings per study for RQ2 and RQ3.

I draw 100,000 independent table pairs per setting. Both tests get the same pairs, so a difference in their decisions can't come from using different samples.

The model line shows how I set population MI. I draw X, then either copy its category into Y or draw Y independently from the same frequencies. I adjust the probability of copying to reach each target MI without changing the category frequencies.

At the bottom, both tests use a 5% significance level. If a calculation fails, I count it as a non-rejection and report calculation success separately.

## Slide 7: RQ1 results: approximation accuracy

Both graphs vary sample size. They show population P in a four-by-four, different-skew setting, with population MI of 0.02 nats.

The top graph divides average V-hat by population V. The ratio is well above one for small samples, so the first-order approximation gives too low a mean there. As sample size grows, the curve comes down towards one.

The box beside the top graph points to one reason. A rare category pair that appears in a sample can have a pointwise MI far from the table's MI. Squaring that gap can push V-hat up. Even at 1,000 observations, average V-hat is still 19% above V.

The lower graph divides the predicted sampling variance of V-hat by the variance observed across repeated samples. Below one means the prediction is too low, and above one means it's too high.

The solid navy curve uses the population tau-squared. Rare cells appearing in some samples but not others can produce changes larger than the linear approximation predicts. At the same sample size of 1,000, this prediction is about 3% low.

The dashed orange curve uses tau-squared estimated from each table, then averages the resulting predictions. Estimating sensitivities from sparse counts can instead overpredict the variation; at that sample size, the prediction is about 8% high.

Look at the summary at the bottom. The population inputs give us a fairly accurate prediction of the variance even though they give us too low a mean. Moment matching squares the mean, so using that lower value can push the degrees of freedom down.

## Slide 8: RQ1 results: near independence

Here the table size stays four by four and sample size stays at 1,000. We move left towards smaller population MI on the log scale and look at the component degrees of freedom on the vertical axis.

Start with the green line. It is the moment-matching target, calculated from V-hat's mean and variance across repeated samples. At the leftmost point, the target is about 9.1.

The dotted navy line uses known population inputs in the first-order formula, as explained in the navy box. Close to zero MI, this component value is approximately sample size times population MI, so it heads towards zero. At the same MI value it is about 0.1, far below the target.

The orange line averages the component degrees of freedom estimated from the sampled tables. As the orange box explains, at zero population MI the linear term in the uncorrected MI estimate vanishes, but squared probability errors can still make that estimate positive. The calculation from each table picks up that noise. The bracket shows the result: about 4.9, roughly half the target.

Hitting that target would still leave us with a question: how often do the tests reject when population MI is equal?

## Slide 9: RQ2 results: false positives across all null settings

Each dot is one of the 360 equal-MI settings. The horizontal axis shows the Wald test's false-positive rate, and the vertical axis shows Expanded Welch's. The dashed lines mark 5%.

The diagonal means equal rejection rates. All points lie on or below it because Expanded Welch can only reduce rejection.

Start with the top box on the right. The Wald test is above 5% in 178 settings, and Expanded Welch gets closer to 5% in 165 of them. The highlighted uniform example goes from 8.35% to 4.90%.

In the next box, the Wald test is below 5% in 180 settings. Expanded Welch pushes the rate even lower in 176 of those and leaves four unchanged.

At the bottom right, the two tests land in the 4% to 6% band in roughly the same number of settings. Now look at the circled different-skew example near the top right of the plot. Here the shared MI is 0.005 nats. The false-positive rate falls from about 36% to about 34%, still far above 5%.

To see why a larger cutoff helps in some settings and does little in others, let's look at the estimated difference and its standard error.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

All three rows use equal MI of 0.02 nats, and every calculation succeeds. The bias column shows how far the average estimated difference is from zero, in sampling standard deviations. In the next column, one means the average squared standard error matches the observed variance of the estimated difference.

In the uniform row, the biases cancel in expectation, so the difference is centred near zero. The variance ratio is below one, so the squared standard error is too small on average. For a given difference, a smaller standard error puts the statistic further from zero. Here the larger cutoff offsets that, bringing the false-positive rate from 8.35% to 4.90%.

In the same-skew row, the biases again cancel in expectation, but the variance ratio is nearly two. That overstatement of uncertainty helps explain why the Wald test rejects only about 0.6% of the time. The larger cutoff pushes it further below 5%, to about 0.5%.

The third row keeps the table size and sample size but uses different-skew margins. The variance ratio is still nearly two, but now the estimated difference averages about two sampling standard deviations above zero. The false-positive rate only falls from about 26% to about 25%. As the final box shows, changing the cutoff leaves that bias in place.

The takeaway at the bottom is that a larger cutoff can offset a standard error that's too small, but it leaves the bias in the estimated difference unchanged.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the chance of detecting a real MI difference. This graph shows how many percentage points of power Expanded Welch loses compared with the Wald test. The line is the median loss across 36 settings at each sample size, and the shading shows the full range.

The upper-right box summarises the small-sample cost. With ten observations per population, the median loss is about six percentage points, partly because some calculations fail. From 50 to 1,000 observations, the median loss is about one point. By 10,000, even the largest loss is less than a third of a percentage point.

Both tests use a 5% significance level. Their actual false-positive rates can differ, so read the power results alongside those rates.

The lower-right box concerns absolute power. Even at 50,000 observations, the smallest MI gap of 0.005 nats gives Expanded Welch power of about 80% to 96%. Power is above 99.9% for the two larger gaps. So the two tests can have similar power and still miss some real differences when the MI gap is small.

At the bottom, notice that power counts rejections in either direction. Next, we'll see what happens to the estimated sign.

## Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map uses different category frequencies and an MI gap of 0.01 nats, with Q always having greater population MI. Rows show table sizes and columns show sample sizes.

Each cell shows the share of Expanded Welch rejections that point to the wrong population. So 50% means about half the rejections point to P as having higher MI.

The dark cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range.

Look at the outlined sixteen-by-sixteen cell at 1,000 observations per population. Q truly has more MI, by 0.01 nats. On average, the estimate points the other way and puts P ahead by about 0.02 nats. Expanded Welch rejects in about 10% of repetitions. Almost every one of those rejections points to P as having higher MI.

The next box shows why. The table sizes and sample sizes match, so the two leading corrections cancel in the difference. But the remaining bias pulls Q's estimate down more than P's. That shifts the estimated difference up by about 0.03 nats, three times the true gap. The cutoff can't undo that shift. With 10,000 observations per population, fewer than 0.4% of rejections pointed the wrong way in every setting at that sample size.

At the bottom is the tally across all 360 power settings. In 28 settings, at least 90% of rejections point the wrong way. All 28 use different-skew margins with eight-by-eight or sixteen-by-sixteen tables. Those rejections still count towards two-sided power.

## Slide 13: Conclusions and next steps

Across the top are the three contributions. First, I derived how a change in the probability table affects pointwise-MI variance. Second, I used that result to choose degrees of freedom for the Student t distribution. Third, I evaluated the approximations and compared the tests in simulations.

In the next row, RQ1 shows that the approximations generally improve with sample size, but the first-order calculation misses sampling noise near zero MI.

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
- g measures how sensitive V is to shifting probability towards a particular cell, including the resulting changes in the margins. Slide 20 gives the cell formulas, and Slide 21 works through an example.
- Tau-squared is the variance of those sensitivities across outcomes. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of the sensitivities.

### 3. Where do the degrees of freedom come from, and is the Student t distribution exact?

- A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching moments gives nu as twice the squared mean divided by the variance.
- Approximating those moments by V and tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table. Slides 16–18 walk through the sampling variance, moment matching, and the combined degrees of freedom.
- The Student t distribution is the reference distribution, an approximation under equal population MI. Matching moments does not establish independence between the estimated MI difference and the variance estimates.

### 4. Why does the approximation struggle when population MI is close to zero?

- When population MI is zero, all population pointwise-MI values are zero, and the first-order sampling terms for MI and V-hat vanish. Squared probability errors can still give a positive plug-in MI estimate.
- On Slide 8, the population first-order value is about 0.1, while the mean sample-based estimate is about 4.9 because its calculation retains positive estimated MI from sampling noise.
- The repeated-sample moment target is about 9.1. The calculation on Slide 24 includes the squared probability errors and helps explain the separation between the lines. That explanation does not establish an exact replacement test.

### 5. Why this simulation design, and why 100,000 repetitions?

- The copying model controls MI while preserving chosen category frequencies, giving known population truth. It represents one family of joint probability tables.
- The 360 null and 360 power settings vary table size, frequencies, sample size, and MI values to expose different estimation problems.
- Repetitions estimate performance precisely; they do not increase an individual test's sample size. Both methods receive the same sampled pairs for comparison.

### 6. Why does bias remain after your correction?

- With equal dimensions and sample sizes, the two leading bias corrections cancel exactly in the MI difference. Slide 15 shows the correction and why it cancels.
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
