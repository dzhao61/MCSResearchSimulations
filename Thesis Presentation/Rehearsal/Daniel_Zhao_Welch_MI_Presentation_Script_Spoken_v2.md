# Comparing Mutual Information in Finite Samples

## Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations using the Wald and Expanded Welch tests.

## Slide 2: Motivation: comparing MI across populations

Let's start with mutual information. It measures how much knowing one variable reduces uncertainty about another, on average. If the variables are independent, MI is zero.

At the top, the test compares MI across two populations, P and Q, for the same categorical variables, X and Y. Under the null, the population MI values are equal, while under the alternative they differ.

We don't know those population MI values, so we take a sample from each population to estimate them. Even if the populations have equal MI, their sample estimates can differ. So the last step on the right asks whether that difference is genuine or could be explained by sampling noise.

## Slide 3: Literature review: foundations and the MI-specific step

To answer that question, I draw on three areas of previous work. On the left is the work on estimating MI. We can estimate MI from a count table and correct for its leading bias. We can also estimate its sampling variance, which tells us how much the MI estimate varies across samples.

In the middle is the Wald test, which I use as my baseline. It asks whether the estimated MI difference is large compared with its standard error. To decide how large is large enough, it uses a cutoff from the standard normal distribution.

On the right, we have Welch's test. In its original form, it compares two means using a cutoff from a Student t distribution to allow for uncertainty in the estimated standard error. My main contribution in this thesis is to adapt Welch's test to compare MI. I use the Welch–Satterthwaite rule to choose the degrees of freedom, and for that I need an MI-specific approximation for how much the variance estimate itself varies from sample to sample.

The bottom row sums up my contributions. I work out how changes in the table affect the variance estimate, use that result to build the Expanded Welch test, and check how both the approximation and the test perform in simulations.

## Slide 4: Method: one statistic, two reference distributions

Let's put those ideas together and look at how the two tests work. In the box at the top, both tests start with the estimated MI of P minus the estimated MI of Q. They correct for the leading bias and divide by the estimated standard error.

In the second equation, V-hat estimates the variance of pointwise MI. So if we divide V-hat by the sample size, we get an estimate of the sampling variance of the MI estimator. Since the samples are independent, we add those two estimates to get the squared standard error.

The boxes below the equations show the approximate null distribution for each test. For the Wald test, we compare the statistic to the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the next box, Expanded Welch compares the same statistic with a Student t distribution, which gives a larger cutoff. That means every Expanded Welch rejection is also a Wald rejection. The degrees of freedom determine how much higher that cutoff is. On the next slide, I'll explain one of my main contributions: how I estimate those degrees of freedom from the count tables.

## Slide 5: Approach and contributions

In step one, each sample from the population gives me a new count table and a new estimate, V-hat. To choose the degrees of freedom, I need to know how much V-hat varies across samples of the same size. That's its sampling variance.

To work that out, I start with the middle equation in step two. Imagine shifting a little probability towards one cell. That also changes its row and column totals, which can affect the pointwise MI in other cells. The derivative g tells me how fast the variance of pointwise MI starts to change when I make that shift.

Now think about drawing one observation. The cell it lands in gives me its g value, so I can get different g values from different draws. The bottom equation gives the variance of g across those draws, which I call tau-squared.

For a whole sample, I average those g values, counting one for each observation. A first-order Taylor expansion lets me use that average to approximate how V-hat varies across samples. Since the observations are independent, I divide tau-squared by the sample size to get the variance of that average. That gives me the approximation at the top.

Finally, in step three, I use that sampling variance to choose the degrees of freedom. The top equation shows how the Satterthwaite moment matching rule uses the expectation of V-hat and its sampling variance. The second equation shows how I estimate the degrees of freedom from one table. If the expectation stays the same, more sampling variance means fewer degrees of freedom, which gives a larger cutoff from the Student t distribution.

As the callout shows, I can get the estimates I need from the sampled table counts. At the bottom, I repeat the calculation for Q and combine the results using the Welch–Satterthwaite rule. The full calculations are in the appendix.

## Slide 6: Evaluation design

To see how the test performs, I used simulations to answer the three questions on the left. RQ1 checks how well I can approximate the expectation and sampling variance of V-hat, and how accurately those approximations predict the degrees of freedom near and away from independence.

For RQ2, I give both populations the same MI by construction, then check how often the tests falsely say they differ. I repeat that at three shared MI values.

For RQ3, I give the populations different MI values by construction, then check how often the tests detect that difference. I keep the MI of P at 0.02 nats and increase the MI of Q to create three different gaps.

On the right is the shared grid for RQ2 and RQ3. I vary table size, sample size, and the margins, which are the category frequencies. Combining those choices with the three MI levels or gaps gives 360 settings per study. For each setting, I draw 100,000 independent pairs of tables and run both tests on each pair at the 5% significance level.

## Slide 7: RQ1 results: approximation accuracy

I'll start the results with one illustrative four-by-four setting. Sample size increases to the right, and a ratio of one means agreement with the simulations.

Look at the top graph first. I divide the average V-hat from the simulated tables by the population value V. In small samples, the ratio is well above one, so V is too low as a prediction of that average. The orange box gives one reason: when a rare pair turns up, its pointwise MI can be far from the table's MI, which can push V-hat up.

The lower graph asks how well we predict the sampling variance. I divide both predictions by the variance of V-hat across the actual simulation samples. The dark blue line uses the population probabilities and is often too low. As the blue box explains, the first-order approximation can miss variation from rare pairs turning up in some samples but not others. The orange line averages predictions from individual tables. A rare pair seen once can give a large estimated g, which can pull that average too high. For larger samples, both lines are close to one.

## Slide 8: RQ1 results: near independence

Now I'll keep the sample size fixed and look at what happens as MI approaches zero. The green line is the benchmark: I use the mean and variance of V-hat across the actual simulation samples to calculate the degrees of freedom.

For the orange line, I do the calculation in a different order. I estimate the degrees of freedom for each table, then average those estimates. As the orange box explains, chance alone can make nearly independent variables look related. That keeps the average near five at the smallest MI values, about half the green benchmark.

The dark blue line uses the known population probabilities. Its prediction is roughly sample size times population MI. With sample size fixed, the prediction heads towards zero.

## Slide 9: RQ2 results: false positives across all null settings

So what does a larger cutoff do to false positives? Each dot compares the two tests in one of the 360 settings with equal MI. The Wald rate is on the horizontal axis and the Expanded Welch rate is on the vertical. Below the diagonal, Expanded Welch rejects less often. The dashed lines mark the 5% target.

Whether rejecting less helps depends on where you start. In the orange box, the Wald test rejects too often, and Expanded Welch brings most of those rates closer to 5%. In the blue box, the Wald test already rejects too rarely, so the larger cutoff takes nearly all of those rates further away.

Even where the cutoff helps, the gains vary. In the uniform example, the rate falls from 8.35% to 4.90%. But at the top right, it only goes from about 36% to 34%.

## Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

These three illustrative examples show why the cutoff can help in one setting and hurt in another. The true difference is zero in all three, so the bias column shows how far the estimates sit from zero on average. The variance ratio tells us whether we overestimate or underestimate the sampling variance.

The first two examples have almost no bias, but the standard errors go wrong in opposite directions. In example one, the standard error is too small, which makes the same difference look more extreme. That's where the larger cutoff helps. In example two, the standard error is too large and the Wald test already rejects too rarely. The larger cutoff pushes the rate lower still.

In example three, the estimates are centred away from zero. Changing the cutoff can't shift them back, so both tests still reject in about 25% of runs.

## Slide 11: RQ3 results: the power cost of the larger cutoff

A larger cutoff also has a cost when there's a real MI difference. The orange line shows the median power loss for Expanded Welch compared with the Wald test at the same 5% significance level. The shaded band shows how much the loss varies across settings.

Most of the loss is in the smallest samples. At ten observations per population, the median loss is about six percentage points, partly because some Expanded Welch calculations fail. By ten thousand, it's under a third of a percentage point in every setting.

The two tests can have similar power and still miss a small gap. As the blue box shows, even at fifty thousand observations per population, power for the smallest gap ranges from about 80% to 96%. Both tests detect the larger gaps almost every time.

Now that we've seen how often the tests detect a difference, let's look more closely at the estimates behind those rejections.

## Slide 12: RQ3 results: bias can reverse the estimated direction

So by construction, the MI of Q is higher than the MI of P. There's a real difference, so we want Expanded Welch to reject. But sometimes it rejects because the estimated difference is large in the wrong direction. The darker the cell, the higher the percentage of rejections that put P ahead. In larger tables, it takes more observations before most rejections point to Q.

Take the outlined cell as an illustrative example. Q's MI is higher by 0.01 nats, but the estimate puts P ahead by about 0.02 nats on average. Expanded Welch rejects in about 10% of runs, and over 99.9% of those rejections get the direction wrong.

The blue box shows how that happens. The leading correction assumes the cells are sampled often enough, but Q's more skewed margins make its rare pairs less likely to appear. Here, that means Q's raw MI estimate has less upward bias than P's. I subtract the same correction from both, so Q's estimate ends up further below its true MI. That's enough to put P ahead on average.

The bottom callout shows this happens elsewhere too. In 28 of the 360 power settings, at least 90% of Expanded Welch rejections point the wrong way. A larger cutoff can change how often we reject, but it can't fix the bias.

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
