# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations using the Wald and Expanded Welch tests.

## Slide 2: Motivation: comparing MI across populations

Let's start with mutual information, or MI. It measures how much knowing one variable reduces uncertainty about another, on average. If the variables are independent, MI is zero.

The hypotheses at the top compare MI for the same two categorical variables, X and Y, in populations P and Q. Under the null, the population MI values are equal, while under the alternative they differ.

We don't know those population MI values, so we take a sample from each population to estimate them. Even if the populations have equal MI, their sample estimates can differ. So the last step on the right asks whether that difference could be explained by sampling noise.

## Slide 3: Literature review: foundations and the MI-specific step

To answer that question, I draw on three areas of previous work. On the left is the work on estimating MI. We can estimate MI from a count table and correct for its leading bias. We can also estimate its sampling variance, which tells us how much the MI estimate varies across samples.

In the middle is my baseline, the Wald test. It uses a cutoff from the standard normal distribution, and I check how well that cutoff controls false positives in finite samples.

On the right, the Welch–Satterthwaite rule gives me a way to choose the degrees of freedom for a Student t distribution. To apply that rule to MI, I need one more quantity: how much the variance estimate itself varies from sample to sample.

My first contribution is to derive an approximation for that variation. I use it to build the Expanded Welch test, then use simulations to check the approximation and compare the two tests.

## Slide 4: Method: one statistic, two reference distributions

Let's put those ideas together and look at how the two tests work. In the box at the top, both tests start with the estimated MI of P minus the estimated MI of Q. They correct for the leading bias and divide by the estimated standard error. For example, plus two means the corrected difference is two standard errors above zero.

In the second equation, V-hat estimates the variance of pointwise MI. Dividing V-hat by the sample size estimates the sampling variance of the MI estimator. Since the samples are independent, we add those two estimates to get the squared standard error.

In the first box below the equations, the Wald test compares the statistic with the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the next box, Expanded Welch compares the same statistic with a Student t distribution, which gives a larger cutoff. That means every Expanded Welch rejection is also a Wald rejection. On the next slide, I'll explain one of my main contributions: how I estimate the degrees of freedom for that distribution.

## Slide 5: Approach and contributions

In step one, each sample gives a new count table and a new estimate, V-hat. To choose the degrees of freedom, I need the sampling variance of V-hat across samples of the same size.

In step two, I start with the middle equation. If I shift a little probability towards one cell, I change its row and column totals too. That can change the pointwise MI in other cells. The derivative g tells us how fast the variance of pointwise MI starts to change as I make that shift.

Now draw one observation from the population. The cell it lands in determines its g value, so g can differ from one draw to the next. The bottom equation gives the variance of g across those draws. That's tau-squared.

For a whole sample, each observation contributes the g value of its cell. A first-order Taylor expansion lets me use the average of those g values to approximate how V-hat varies across samples. Since the observations are independent, the variance of that average is tau-squared divided by the sample size. That's the approximation for the sampling variance of V-hat at the top.

Finally, in step three, I use the sampling variance of V-hat to choose the degrees of freedom. The top equation gives the Satterthwaite moment matching rule. It uses two quantities: the expectation of V-hat and its sampling variance. The second equation shows how I estimate the degrees of freedom from one table. For the same expectation, a larger sampling variance gives fewer degrees of freedom, which means a larger cutoff from the Student t distribution.

As the callout shows, I can calculate these estimates from the sampled table counts. I repeat the calculation for Q and use the Welch–Satterthwaite rule at the bottom to get the combined degrees of freedom. The full calculations are in the appendix.

## Slide 6: Evaluation design

To see how the test performs, I used simulations to answer the three questions on the left. RQ1 checks how well I can approximate the expectation and sampling variance of V-hat, and how accurately those approximations predict the degrees of freedom near and away from independence.

For RQ2, I give both populations the same MI and check how often the tests falsely say they differ. I repeat that at three shared MI values.

For RQ3, I give the populations different MI values and check how often the tests detect the difference. I keep the MI of P at 0.02 nats and increase the MI of Q to create three different gaps.

On the right is the shared grid for RQ2 and RQ3. I vary table size, sample size, and the margins, which are the category frequencies. Combining those choices with the three MI levels or gaps gives 360 settings per study. For each setting, I apply both tests to the same 100,000 independently drawn table pairs.

I set the population MI using a special case of the mixture model described by Bocci and colleagues in 2010. The details are on backup Slide 22.

Both tests use a 5% significance level.

## Slide 7: RQ1 results: approximation accuracy

Turning to the results, I'll start with the approximations. I use repeated samples to check how well they predict the expectation and sampling variance of V-hat. Both graphs use the same illustrative four-by-four example. Sample size increases as we move right, and a ratio of one means the prediction and the simulations agree.

The top graph checks the expectation of V-hat. I estimate it by averaging V-hat across the simulated samples, then divide by the population value V. The curve starts well above one and approaches one as the sample size grows. So V underestimates the expectation most in small samples. The orange box explains one reason: when a rare combination shows up, its pointwise MI can be far from the table's MI. Squaring that gap can push V-hat up.

The lower graph checks the sampling variance of V-hat. Here the ratio is the predicted variance divided by the variance measured across the simulated samples, so above one means the prediction is too high. As the blue box explains, rare cells appear in some samples and not others. That can cause changes in V-hat that the first-order approximation misses. That helps explain why the dark blue line, which uses population inputs, is often below one. The orange line uses inputs from the sampled tables and often overpredicts the sampling variance. At larger sample sizes, both lines are close to one.

So the sampling variance can be close while V still underestimates the expectation. Both quantities enter the degrees-of-freedom calculation.

## Slide 8: RQ1 results: near independence

Next, let's see how the approximations behave near independence. In this illustrative example, I keep the sample size fixed and focus on the smallest population MI values. The green line is our benchmark: the degrees of freedom we get when we estimate the expectation and sampling variance of V-hat using repeated samples.

For the orange line, I calculate degrees of freedom from each sampled table instead of the population probability table, then average these sampled estimates of degrees of freedom. As the orange box explains, chance fluctuations in the counts can make X and Y look related in a sample even when they're nearly independent in the population. Near independence, that apparent MI comes largely from squared errors in the sampled probabilities. The calculation from each table picks up some of that effect, so the average stays near five at the smallest MI values. That's still only about half the green benchmark.

For the dark blue line, I use the known population probabilities in the first-order degrees-of-freedom formula. As the dark blue box shows, the result near independence is roughly the sample size times population MI. With the sample size fixed, that prediction heads towards zero as population MI falls.

So the degrees of freedom can be hard to estimate near independence. What matters for the test is how often it actually rejects when MI is equal.

## Slide 9: RQ2 results: false positives across all null settings

Moving on to false positives, I've plotted all 360 settings where the two populations have equal MI. Each dot is one setting. The horizontal axis is the false-positive rate for the Wald test, and the vertical axis is the rate for Expanded Welch. Points below the diagonal tell us Expanded Welch rejects less often. The dashed lines mark the 5% target.

The orange box shows what happens when the Wald test starts above 5%: Expanded Welch brings most of those rates closer to the target. The dark blue box shows what happens when the Wald test starts below 5%: Expanded Welch pushes nearly all of those rates further below 5%.

The two marked points give illustrative examples of how much the improvement can vary. In the uniform example, the rate comes down from 8.35% to 4.90%. For the point near the top right, it drops from about 36% to 34%, still a long way from 5%. So what makes the Wald test miss the target in the first place?

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

To see why the larger cutoff helps in some settings and hurts in others, let's look at these three illustrative examples. The true MI difference is zero in all three, so the bias column tells us how far the expectation of the estimated difference is from zero, in sampling standard deviations.

The variance ratio compares the average squared standard error with the sampling variance measured across repetitions. If the ratio is below one, we're underestimating that variance on average. If it's above one, we're overestimating it.

In example one, the estimates are centred near zero, but we underestimate the sampling variance. Dividing by a standard error that's too small makes the same estimated difference look more extreme, so the larger cutoff helps bring the false-positive rate back towards 5%.

In example two, the estimates are still centred near zero, but this time we overestimate the sampling variance. The Wald test already rejects too rarely, so the larger cutoff pushes the false-positive rate even further below 5%.

In example three, the estimated difference has an expectation about two sampling standard deviations above zero. The larger cutoff makes rejection harder, but it can't move those estimates back towards zero. Both tests still reject in about 25% of runs.

## Slide 11: RQ3 results: the power cost of the larger cutoff

Now let's turn to power. When there's a real difference in MI, a larger cutoff makes it harder to detect. This graph shows the power Expanded Welch loses compared with the Wald test at the same 5% significance level. The orange line shows the median loss at each sample size, and the shaded band shows the range across settings. The tests can still have different actual false-positive rates, as we just saw.

The median loss is largest at the smallest sample size, partly because some Expanded Welch calculations fail. At larger sample sizes, the typical loss is smaller and the range across settings is narrower. By ten thousand observations per population, the loss is under a third of a percentage point in every setting studied.

The blue box shows how power depends on the size of the MI gap. At fifty thousand observations per population, both tests detect the two larger gaps almost every time. For the smallest gap, power still ranges from about 80% to 96% across settings.

One more thing: power counts every rejection when the population MI values differ. It doesn't tell us whether the estimate points to the right population.

## Slide 12: RQ3 results: bias can reverse the estimated direction

To check the direction, I look at which population the rejections point to. Q has the higher population MI in every setting shown here. Each cell shows the percentage of Expanded Welch rejections where the estimate puts P ahead. Darker cells mean that happens more often.

In the bigger tables, it takes more observations before most rejections point to Q. At the largest sample sizes shown, almost all rejections point to Q, no matter the table size.

The outlined cell is an illustrative example: a sixteen-by-sixteen table with a thousand observations per population. I subtract the MI of Q from the MI of P, so Q's true lead of 0.01 nats gives a negative difference. But the estimated difference has a positive expectation of about 0.02 nats, which puts P ahead on average. The test rejects in about 10% of runs, and over 99.9% of those rejections point to P.

The numbered box explains why. First, the leading correction assumes each cell is sampled often enough to contribute its share of the upward bias. Second, Q's margins are more skewed, so its rare pairs are much rarer and usually go unobserved. Third, those rare cells add less upward bias in Q, so its raw MI estimate is inflated less than P's. Finally, the same correction leaves Q's estimate further below its true MI, so P minus Q flips sign on average.

The bottom callout puts this example in context. In 28 of the 360 power settings, at least 90% of Expanded Welch rejections point the wrong way. All 28 use eight-by-eight or sixteen-by-sixteen tables with different-skew margins. A larger cutoff can change which estimates lead to a rejection, but it can't correct a sign reversal caused by bias.

## Slide 13: Conclusions and next steps

To wrap up, I'll return to the three contributions in the top row. I derived an approximation for the sampling variance of V-hat, used that to choose degrees of freedom for the Student t distribution, and compared the resulting test with the Wald test in simulations.

The middle row gives the findings for each research question. First, on approximation accuracy, the approximations generally improve as samples grow, but the first-order Taylor approximation misses some sampling variation near independence. Second, on false positives, the larger cutoff moves some rates closer to 5% and pushes others further below it. Third, on power and direction, the larger cutoff can cost power, and bias can still make rejections point to the wrong population.

So I wouldn't switch to Expanded Welch simply because the samples are small. Its larger cutoff can offset a standard error that's too small, but if bias makes the wrong population look like it has higher MI, the estimate itself needs to improve.

That brings me to the two next steps at the bottom. I'd start by reducing bias in the estimated MI difference and improving the standard error and the degrees-of-freedom approximation, especially near independence. Then I'd test those changes with other table constructions and unequal sample sizes.

Thank you.

## Questions and answer guides

### 1. What is your main contribution?

- I derived how the variance of pointwise MI starts to change when we shift probability towards a cell, accounting for changes to the joint and marginal probabilities.
- That gives the sampling-variance approximation needed to estimate component degrees of freedom and combine them using the established Welch–Satterthwaite rule.
- I evaluated approximation accuracy, false positives, power, and calculation success. Keeping the same estimated difference and standard error as the Wald test lets me isolate the effect of changing the reference distribution.

### 2. What do V, g, and tau-squared actually mean?

- V is the variance of pointwise MI across observations from the population. V-hat estimates it from one table, and V-hat divided by n estimates MI's sampling variance.
- g is the derivative of V as we shift probability towards a particular cell, evaluated at the original probability table. It includes the effect of changing the row and column totals. Slide 20 gives the cell formulas, and Slide 21 works through an example.
- Tau-squared is the variance of g across observations from the population. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of g.

### 3. Where do the degrees of freedom come from, and is the Student t distribution exact?

- A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching the expectation and sampling variance of V-hat gives nu as twice the squared expectation divided by the sampling variance.
- Approximating the expectation by V and the sampling variance by tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table. Slides 16–18 walk through the sampling variance, moment matching, and the combined degrees of freedom.
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

- With equal dimensions and sample sizes, the two leading bias corrections cancel exactly in the MI difference. Slide 15 shows why the correction cancels and explains why the leading approximation works better when the cells have large expected counts.
- Higher-order biases remain. Identical population tables have the same bias at equal sample sizes, but distinct tables can have unequal biases even when their MI values agree.
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
- In the highlighted example, the true difference is −0.01, but the expectation of the estimated difference is about +0.0207. Q's more skewed margins make the rare off-diagonal pairs much rarer. In this example, the bias in the marginal entropies is nearly the same for P and Q, but Q's joint entropy estimate has a smaller downward bias. Since MI subtracts joint entropy, Q's raw MI estimate has less upward bias. Subtracting the same correction leaves Q's estimate further below its true MI.
- Of 9,662 rejections, 9,659 point the wrong way. That is over 99.9% of the rejections. Two-sided power counts those rejections.

### 10. Why not use permutation or bootstrap instead?

- Simple group-label permutation requires exchangeability. Equal MI allows different joint distributions, so it does not supply that condition.
- Separate-sample bootstrapping is a candidate, but an ordinary empirical bootstrap cannot generate cells absent from the observed table, and estimation bias can remain.
- I did not conduct a full resampling comparison. The thesis cannot establish superiority over those alternatives.

### 11. What assumptions and calculation rules matter most?

- Observations are independent and identically distributed within each population, with independent samples, fixed, aligned categories, positive population cell probabilities, and positive V and tau-squared for the first-order construction.
- Positive population probabilities still allow empty sampled cells, which are retained. The Wald test needs a finite estimated difference and a positive finite standard error. Expanded Welch also needs positive finite degrees of freedom for each table and for the combined calculation.
- Failed calculations count as non-rejections, with success reported separately. They contribute to some small-sample power loss but do not explain the highlighted failures where every calculation succeeds.

### 12. What is your overall conclusion, and what would you improve next?

- Expanded Welch improves some excessive false-positive rates, but its larger cutoff also increases conservatism and can reduce power at the same 5% significance level.
- I would first improve the MI-difference and standard-error estimates, changing one at a time to identify what resolves the failures.
- Further work should retain additional sampling variation when population MI is close to zero and evaluate other population constructions and unequal sample sizes. There is no universal sample-size rule established here.
