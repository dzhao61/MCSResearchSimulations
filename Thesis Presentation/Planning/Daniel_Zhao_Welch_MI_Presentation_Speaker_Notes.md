# Comparing Mutual Information in Finite Samples: speaker notes

Daniel Zhao. Talk target 18:50 for Slides 1–13; Slide 13 stays up for questions. Slide 14 is the appendix title and the backups are Slides 15–33.
The notes for Slides 1–13 and the question guides under Slide 14 are the spoken script (Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md, 14 November 2026), word for word. The backup notes (Slides 15–33) come from the presentation execution plan.

## Main talk

### Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

### Slide 2: Motivation: comparing MI across populations

Let's start with mutual information, or MI. It measures how much knowing one variable reduces uncertainty about another, on average. If the variables are independent, MI is zero.

The hypotheses at the top compare MI for the same two categorical variables, X and Y, in populations P and Q. The null says their population MI values are equal. The alternative says they differ.

On the left, each observation gives us a pair: one category for X and one for Y. We count how often each pair occurs and estimate MI from that count table. We do that for each population. Even if the populations have equal MI, those estimates can differ. So the last step on the right asks whether sampling noise could explain the difference we see.

In the example at the bottom, imagine X is a student's mid-semester test grade and Y is their final exam grade, both recorded as categories. The two populations are students before and after generative AI, and we want to know if there is a change in relationship between the two as measured by mutual information.

### Slide 3: Literature review: foundations and the MI-specific step

With that question in mind, let's look at what the literature gives us. On the left, the literature on MI gives us a way to estimate MI, correct its leading bias, and approximate the sampling variance of the MI estimator. However, to choose degrees of freedom, we also need to know the sampling variance of the variance estimate itself: how much it varies across repeated samples.

In the middle, the literature on Wald tests gives us a baseline for comparing MI. We divide the estimated MI difference by its standard error and use a cutoff from the standard normal distribution. However, we still need to check how often that cutoff leads to false positives in finite samples.

On the right, Welch–Satterthwaite moment matching gives us a way to choose the degrees of freedom for a Student t distribution. The calculation uses the expectation and sampling variance of the estimated variance contributions. However, to apply it to MI, we need to work out how shifting a little probability towards a cell changes the variance of pointwise MI.

My first contribution is to derive that rate of change and use it to approximate the sampling variance of the pointwise-MI variance estimate. My second is to use that approximation to build the Expanded Welch test, and my third is to check the approximation and compare Expanded Welch with the Wald test in simulations.

### Slide 4: Method: one statistic, two reference distributions

Let's put those ideas together and look at how the two tests work. In the box at the top, both tests start with the estimated MI of P minus the estimated MI of Q. They correct for the leading bias and divide by the estimated standard error. For example, plus two means the corrected difference is two standard errors above zero.

In the second equation, V-hat estimates the variance of pointwise MI. Dividing V-hat by the sample size estimates the sampling variance of the MI estimator. Since the samples are independent, we add those two estimates to get the squared standard error.

In the first box below the equations, the Wald test compares the statistic with the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the next box, the Expanded Welch test uses a Student t distribution as its reference. One of my main contributions is how I estimate the degrees of freedom for that distribution. I'll explain how I do that on the next slide.

The graph compares the dark blue curve for the standard normal distribution with the green curve for a Student t distribution. The green curve uses five degrees of freedom as an example. Its heavier tails put the 5% cutoffs further out, at about 2.57 in either direction. With more degrees of freedom, the Student t distribution approaches the standard normal distribution.

Since both tests use the same statistic and the Expanded Welch cutoff is larger, every Expanded Welch rejection is also a Wald rejection.

### Slide 5: Approach and contributions

Next, I'll show how I choose the degrees of freedom for Expanded Welch. In step one, each sample from the population gives a new count table and an estimate, V-hat. To choose the degrees of freedom, I need its sampling variance: how much V-hat varies across samples of the same size.

In step two, I start with the middle equation. If I shift a little probability towards one cell, I change its row and column totals too. That can change the pointwise MI in other cells. The derivative g tells us how fast the variance of pointwise MI starts to change as I make that shift.

Now draw one observation from the population. The cell it lands in determines its g value, so g can differ from one draw to the next. The bottom equation gives the variance of g across those draws. That's tau-squared.

For a whole sample, I have one g value per observation. A first-order Taylor expansion lets me use the average of those g values to approximate how V-hat varies across samples. Since the observations are independent, the variance of that average is tau-squared divided by the sample size. That's the approximation for the sampling variance of V-hat at the top.

Finally, in step three, I use the sampling variance of V-hat to choose the degrees of freedom. The top equation gives the Satterthwaite moment matching rule. It uses two quantities: the expectation of V-hat, meaning its average across repeated samples, and its sampling variance. The second equation shows how I estimate the degrees of freedom from one table. For the same expectation, a larger sampling variance gives fewer degrees of freedom, which means a larger cutoff from the Student t distribution.

As the callout shows, we can calculate all these estimates from the sampled table counts. I've left the full calculations to the appendix because they're lengthy.

### Slide 6: Evaluation design

To see how the test performs, I used simulations to answer the three questions on the left. RQ1 checks how well I can approximate the expectation and sampling variance of V-hat, and how accurately those approximations predict the degrees of freedom near and away from independence.

For RQ2, I give both populations the same MI and check how often the tests falsely say they differ. I repeat that at three shared MI values.

For RQ3, I give the populations different MI values and check how often the tests detect the difference. I keep the MI of P at 0.02 nats and increase the MI of Q to create three different gaps.

On the right is the grid for the false-positive and power studies. I use four table sizes, from two by two to sixteen by sixteen.

Next are the margins, which describe how often the categories occur. With uniform margins, the categories are equally frequent. With same-skew margins, the frequencies are uneven but match across the two populations. With different-skew margins, the two populations have different uneven frequencies.

I also vary the number of observations per population across ten sample sizes. Combining the table sizes, margins, and sample sizes with the three shared MI values for RQ2 or the three MI gaps for RQ3 gives 360 settings in each study.

I draw 100,000 independent table pairs per setting. Both tests get the same pairs, so when both calculations succeed, any difference in their decisions comes from the cutoff.

To set the population MI, I use a special case of the mixture model described by Bocci and colleagues in 2010. The details are on backup Slide 22.

At the bottom, both tests use a 5% significance level. If a calculation fails, I count it as a non-rejection and report calculation success separately.

### Slide 7: RQ1 results: approximation accuracy

Turning to the results, I'll start with the approximations. I use repeated samples to check how well they predict the expectation and sampling variance of V-hat. Both graphs use the same illustrative four-by-four example. Sample size increases as we move right, and a ratio of one means the prediction and the simulations agree.

The top graph checks the expectation of V-hat. I estimate it by averaging V-hat across the simulated samples, then divide by the population value V. The curve starts well above one and approaches one as the sample size grows. So V underestimates the expectation most in small samples. The orange box explains one reason: when a rare combination shows up, its pointwise MI can be far from the table's MI. Squaring that gap can push V-hat up.

The lower graph checks the sampling variance of V-hat. Here the ratio is the predicted variance divided by the variance measured across the simulated samples, so above one means the prediction is too high. As the blue box explains, rare cells appear in some samples and not others. That can cause changes in V-hat that the first-order approximation misses. That helps explain why the dark blue line, which uses population inputs, is often below one. The orange line uses inputs from the sampled tables and often overpredicts the sampling variance. At larger sample sizes, both lines are close to one.

So the sampling variance can be close while V still underestimates the expectation. Both quantities enter the degrees-of-freedom calculation.

### Slide 8: RQ1 results: near independence

Next, let's see how the approximations behave near independence. In this illustrative example, I keep the sample size fixed and focus on the smallest population MI values. The green line is our benchmark: the degrees of freedom we get when we estimate the expectation and sampling variance of V-hat using repeated samples.

For the orange line, I calculate degrees of freedom from each sampled table instead of the population probability table, then average these sampled estimates of degrees of freedom. As the orange box explains, chance fluctuations in the counts can make X and Y look related in a sample even when they're nearly independent in the population. Near independence, that apparent MI comes largely from squared errors in the sampled probabilities. The calculation from each table picks up some of that effect, so the average stays near five at the smallest MI values. That's still only about half the green benchmark.

For the dark blue line, I use the known population probabilities in the first-order degrees-of-freedom formula. As the dark blue box shows, the result near independence is roughly the sample size times population MI. With the sample size fixed, that prediction heads towards zero as population MI falls.

So the degrees of freedom can be hard to estimate near independence. What matters for the test is how often it actually rejects when MI is equal.

### Slide 9: RQ2 results: false positives across all null settings

Moving on to false positives, I've plotted all 360 settings where the two populations have equal MI. Each dot is one setting. The horizontal axis is the false-positive rate for the Wald test, and the vertical axis is the rate for Expanded Welch. Points below the diagonal tell us Expanded Welch rejects less often. The dashed lines mark the 5% target.

The orange box shows what happens when the Wald test starts above 5%: Expanded Welch brings most of those rates closer to the target. The dark blue box shows what happens when the Wald test starts below 5%: Expanded Welch pushes nearly all of those rates further below 5%.

The two marked points give illustrative examples of how much the improvement can vary. In the uniform example, the rate comes down from 8.35% to 4.90%. For the point near the top right, it drops from about 36% to 34%, still a long way from 5%. So what makes the Wald test miss the target in the first place?

### Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

To see why the larger cutoff helps in some settings and hurts in others, let's look at these three illustrative examples. The true MI difference is zero in all three, so the bias column tells us how far the expectation of the estimated difference is from zero, in sampling standard deviations.

The variance ratio compares the average squared standard error with the sampling variance measured across repetitions. If the ratio is below one, we're underestimating that variance on average. If it's above one, we're overestimating it.

In example one, the estimates are centred near zero, but we underestimate the sampling variance. Dividing by a standard error that's too small makes the same estimated difference look more extreme, so the larger cutoff helps bring the false-positive rate back towards 5%.

In example two, the estimates are still centred near zero, but this time we overestimate the sampling variance. The Wald test already rejects too rarely, so the larger cutoff pushes the false-positive rate even further below 5%.

In example three, the estimated difference has an expectation about two sampling standard deviations above zero. The larger cutoff makes rejection harder, but it can't move those estimates back towards zero. Both tests still reject in about 25% of runs.

### Slide 11: RQ3 results: the power cost of the larger cutoff

Now let's turn to power. When there's a real difference in MI, a larger cutoff makes it harder to detect. This graph shows the power Expanded Welch loses compared with the Wald test at the same 5% significance level. The orange line shows the median loss at each sample size, and the shaded band shows the range across settings. The tests can still have different actual false-positive rates, as we just saw.

The median loss is largest at the smallest sample size, partly because some Expanded Welch calculations fail. At larger sample sizes, the typical loss is smaller and the range across settings is narrower. By ten thousand observations per population, the loss is under a third of a percentage point in every setting studied.

The blue box shows how power depends on the size of the MI gap. At fifty thousand observations per population, both tests detect the two larger gaps almost every time. For the smallest gap, power still ranges from about 80% to 96% across settings.

One more thing: power counts every rejection when the population MI values differ. It doesn't tell us whether the estimate points to the right population.

### Slide 12: RQ3 results: bias can reverse the estimated direction

To check the direction, I look at which population the rejections point to. Q has the higher population MI in every setting shown here. Each cell shows the percentage of Expanded Welch rejections where the estimate puts P ahead. Darker cells mean that happens more often.

In the bigger tables, it takes more observations before most rejections point to Q. At the largest sample sizes shown, almost all rejections point to Q, no matter the table size.

The outlined cell is an illustrative example: a sixteen-by-sixteen table with a thousand observations per population. I subtract the MI of Q from the MI of P, so Q's true lead of 0.01 nats gives a negative difference. But the estimated difference has a positive expectation of about 0.02 nats, which puts P ahead on average. The test rejects in about 10% of runs, and over 99.9% of those rejections point to P.

The numbered box explains why. First, the leading correction assumes each cell is sampled often enough to contribute its share of the upward bias. Second, Q's margins are more skewed, so its rare pairs are much rarer and usually go unobserved. Third, those rare cells add less upward bias in Q, so its raw MI estimate is inflated less than P's. Finally, the same correction leaves Q's estimate further below its true MI, so P minus Q flips sign on average.

The bottom callout puts this example in context. In 28 of the 360 power settings, at least 90% of Expanded Welch rejections point the wrong way. All 28 use eight-by-eight or sixteen-by-sixteen tables with different-skew margins. A larger cutoff can change which estimates lead to a rejection, but it can't correct a sign reversal caused by bias.

### Slide 13: Conclusions and next steps

To wrap up, I'll return to the three contributions in the top row. I derived an approximation for the sampling variance of V-hat, used that to choose degrees of freedom for the Student t distribution, and compared the resulting test with the Wald test in simulations.

The middle row gives the findings for each research question. First, on approximation accuracy, the approximations generally improve as samples grow, but the first-order Taylor approximation misses some sampling variation near independence. Second, on false positives, the larger cutoff moves some rates closer to 5% and pushes others further below it. Third, on power and direction, the larger cutoff can cost power, and bias can still make rejections point to the wrong population.

So I wouldn't switch to Expanded Welch simply because the samples are small. Its larger cutoff can offset a standard error that's too small, but if bias makes the wrong population look like it has higher MI, the estimate itself needs to improve.

That brings me to the two next steps at the bottom. I'd start by reducing bias in the estimated MI difference and improving the standard error and the degrees-of-freedom approximation, especially near independence. Then I'd check how those changes perform with other population constructions and unequal sample sizes.

Thank you.

## Appendix

### Slide 14: Appendix title

Questions and answer guides

1. What is your main contribution?

• I derived how the variance of pointwise MI starts to change when we shift probability towards a cell, accounting for changes to the joint and marginal probabilities.
• That gives the sampling-variance approximation needed to estimate component degrees of freedom and combine them using the established Welch–Satterthwaite rule.
• I evaluated approximation accuracy, false positives, power, and calculation success. Keeping the same estimated difference and standard error as the Wald test lets me isolate the effect of changing the reference distribution.

2. What do V, g, and tau-squared actually mean?

• V is the variance of pointwise MI across observations from the population. V-hat estimates it from one table, and V-hat divided by n estimates MI's sampling variance.
• g is the derivative of V as we shift probability towards a particular cell, evaluated at the original probability table. It includes the effect of changing the row and column totals. Slide 20 gives the cell formulas, and Slide 21 works through an example.
• Tau-squared is the variance of g across observations from the population. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of g.

3. Where do the degrees of freedom come from, and is the Student t distribution exact?

• A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching the expectation and sampling variance of V-hat gives nu as twice the squared expectation divided by the sampling variance.
• Approximating the expectation by V and the sampling variance by tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table. Slides 16–18 walk through the sampling variance, moment matching, and the combined degrees of freedom.
• The Student t distribution is the reference distribution, an approximation under equal population MI. Matching moments does not establish independence between the estimated MI difference and the variance estimates.

4. Why does the approximation struggle when population MI is close to zero?

• When population MI is zero, all population pointwise-MI values are zero, and the first-order sampling terms for MI and V-hat vanish. Squared probability errors can still give a positive plug-in MI estimate.
• On Slide 8, the population first-order value is about 0.1, while the mean sample-based estimate is about 4.9 because its calculation retains positive estimated MI from sampling noise.
• The repeated-sample moment target is about 9.1. The calculation on Slide 24 includes the squared probability errors and helps explain the separation between the lines. That explanation does not establish an exact replacement test.

5. Why this simulation design, and why 100,000 repetitions?

• The copying model controls MI while preserving chosen category frequencies, giving known population truth. It represents one family of joint probability tables.
• The 360 null and 360 power settings vary table size, frequencies, sample size, and MI values to expose different estimation problems.
• Repetitions estimate performance precisely; they do not increase an individual test's sample size. Both methods receive the same sampled pairs for comparison.

6. Why does bias remain after your correction?

• With equal dimensions and sample sizes, the two leading bias corrections cancel exactly in the MI difference. Slide 15 shows why the correction cancels and explains why the leading approximation works better when the cells have large expected counts.
• Higher-order biases remain. Identical population tables have the same bias at equal sample sizes, but distinct tables can have unequal biases even when their MI values agree.
• The difference can therefore be shifted away from its true value. Raising the rejection cutoff does not remove that shift.

7. Why does Expanded Welch help in some settings and hurt in others?

• Its larger cutoff can compensate for excessive rejection: the uniform example moves from 8.35% to 4.90% under equal MI.
• Where uncertainty is overestimated and the Wald test already rejects too rarely, the larger cutoff lowers the false-positive rate further below 5%.
• Substantial difference bias can leave both tests unreliable. In the diagnostic different-skew example, both reject about a quarter of the time despite equal population MI.

8. If it loses power, is the comparison fair or the method useful?

• At the same 5% significance level, every Expanded Welch rejection is also a Wald rejection, so its power can only stay the same or fall.
• Reducing excessive false positives may justify some power loss, but reducing an already-low rate makes conservatism worse.
• The power comparison uses the tests' usual rules. Their actual false-positive rates can differ, so assess the power loss alongside the change in false positives.

9. What does the wrong-direction result mean?

• Population MI really differs, so these are rejections under an alternative. The error is that the estimated sign identifies the wrong population as having greater MI.
• In the highlighted example, the true difference is −0.01, but the expectation of the estimated difference is about +0.0207. Q's more skewed margins make the rare off-diagonal pairs much rarer. In this example, the bias in the marginal entropies is nearly the same for P and Q, but Q's joint entropy estimate has a smaller downward bias. Since MI subtracts joint entropy, Q's raw MI estimate has less upward bias. Subtracting the same correction leaves Q's estimate further below its true MI.
• Of 9,662 rejections, 9,659 point the wrong way. That is over 99.9% of the rejections. Two-sided power counts those rejections.

10. Why not use permutation or bootstrap instead?

• Simple group-label permutation requires exchangeability. Equal MI allows different joint distributions, so it does not supply that condition.
• Separate-sample bootstrapping is a candidate, but an ordinary empirical bootstrap cannot generate cells absent from the observed table, and estimation bias can remain.
• I did not conduct a full resampling comparison. The thesis cannot establish superiority over those alternatives.

11. What assumptions and calculation rules matter most?

• Observations are independent and identically distributed within each population, with independent samples, fixed, aligned categories, positive population cell probabilities, and positive V and tau-squared for the first-order construction.
• Positive population probabilities still allow empty sampled cells, which are retained. Successful calculations require a positive finite standard error and, for Expanded Welch, positive finite degrees of freedom.
• Failed calculations count as non-rejections, with success reported separately. They contribute to some small-sample power loss but do not explain the highlighted failures where every calculation succeeds.

12. What is your overall conclusion, and what would you improve next?

• Expanded Welch improves some excessive false-positive rates, but its larger cutoff also increases conservatism and can reduce power at the same 5% significance level.
• I would first improve the MI-difference and standard-error estimates, changing one at a time to identify what resolves the failures.
• Further work should retain additional sampling variation when population MI is close to zero and evaluate other population constructions and unequal sample sizes. There is no universal sample-size rule established here.

### Slide 15 (Method · for Slides 4 and 12): Bias correction

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Which bias correction do you use, why does it not remove the bias seen on Slides 10 and 12, and is what remains a higher-order effect?

**Answer to give**

“Each MI estimate subtracts the leading bias, (r − 1)(c − 1) over 2n, following Miller and Moddemeijer. In every simulation the two samples have the same size and table dimensions, so the two corrections are equal and cancel from the difference. The correction assumes every cell is well sampled. Then what remains is a small higher-order term: under 0.002 nats for the 16×16 tables at n = 10,000. In the sparse tables on Slide 12, many cells are expected less than once, and that expansion breaks down. The correction overshoots instead, and by more for Q, whose rare pairs are rarer. That's what flips the sign. So it isn't a small higher-order effect; it's sparse sampling. Reducing this bias is my first next step.”

**Notes**

The leading term is 0.1125 nats per estimate for 16×16 at n = 1,000, and 0.225 nats for 4×4 at n = 20. With unequal sample sizes, the correction removes the leading unequal-sample bias; its performance there is untested (thesis Section 7.2). Corrected estimates can be negative and are retained. Empty sampled cells contribute nothing to the plug-in sum. The figures below are exact expectations, not simulations: plug-in MI is a sum of per-cell terms and each cell count is binomial. Bias beyond the leading term, exact against the 1/n² term of the large-sample expansion: P at n = 1,000, −0.008 against +0.048; Q at n = 1,000, −0.039 against +0.110; P at n = 10,000, +0.0008 against +0.0005; Q at n = 10,000, +0.0017 against +0.0011; at n = 50,000 they agree. Slide 12's mechanism: raw plug-in inflation is 0.105 nats for P and 0.074 for Q; each of the 210 rare pairings is expected 0.37 times in P (margin 0.7) but 0.16 times in Q (0.8); these cells account for 0.0308 of the 0.0307 gap. Copying probabilities: 0.069 in P and 0.100 in Q. Equal MI 0.02 with the same margins (Slide 10's different-skew row) gives +0.030; same-skew margins with MI 0.02 and 0.03 give +0.0009; swapped margins give −0.029, which keeps the true sign. The gap shrinks with n: 0.083 at n = 250, 0.031 at 1,000, 0.008 at 2,500 (mean −0.0016, the power trough), and about zero at 10,000. The figures reproduce the thesis values in Section 6.3.3 (bias +0.0307, mean +0.0207). This breakdown is not in the thesis; the thesis attributes the shift to different residual biases from unequal margins (Sections 6.2.3 and 6.3.3; Paninski, 2003).

**Source**

Thesis Equations 2.7–2.9 and 3.7; Sections 2.2, 3.1.2, 5.1.2, 5.5, 6.2.3, 6.3.3 and 7.2; Miller (1955); Moddemeijer (1989); Panzeri and Treves (1996); Paninski (2003); Chao and Shen (2003); Nemenman et al. (2002). Exact bias figures: calculated for this presentation (assets/code/bias_breakdown.py).

### Slide 16 (Method · for Slide 5, step 2): Derivation 1 of 3: how much the variance estimate varies

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Where does Var{V-hat(P)} ≈ tau-squared(P)/n_P come from?

**Answer to give**

“V-hat is V evaluated at the sample table, and the sample table is an average of one-observation tables. A first-order expansion is linear in the table change, so the error in V-hat becomes an average of one sensitivity per observation. The sensitivities average to zero, so V-hat is centred on V to first order. Because the observations are independent, the variance of that average is the variance of one sensitivity, tau-squared, divided by n.”

**Notes**

The expansion follows the straight line P + t(P-hat − P) from t = 0 to t = 1; the omitted terms are quadratic or higher in the cell-probability errors. The derivative of an average table change is the average of the one-observation derivatives because the linear term has fixed coefficients at P (thesis Section 4.3.1, citing van der Vaart, 1998, Chapter 20). Any bias in V-hat comes from terms beyond this linear approximation. Slide 7 shows both checks: the mean of V-hat over V, and the predicted over the observed variance.

**Source**

Thesis Sections 4.2.1, 4.3.1 and 4.3.2; Equations 4.10, 4.11, 4.30, 4.31 and 4.35–4.38. The perturbation towards one cell and the first-order expansion follow Hampel (1974) and van der Vaart (1998), as the thesis cites them in Sections 2.3.2, 4.2.1 and 4.3.1.

### Slide 17 (Method · for Slide 5, step 3): Derivation 2 of 3: moment matching gives the df rule

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Why are the component df twice the squared mean over the variance, and why does dividing by n_P not change them?

**Answer to give**

“A variable with a scaled chi-squared distribution has variance twice its squared mean divided by its degrees of freedom. Matching those two moments to V-hat gives the target. Dividing V-hat by the fixed sample size rescales the squared mean and the variance equally, so the target is unchanged. For a normal sample variance the same rule gives n minus one, which is ordinary Welch. The resulting Student t distribution is still an approximation that needs empirical checking.”

**Notes**

For a generic variance estimate U modelled as c times a variable with a chi-squared distribution on ν degrees of freedom, E(U) = cν and Var(U) = 2c²ν, giving ν = 2[E(U)]²/Var(U). Scaling by fixed n leaves this ratio unchanged.

**Source**

Thesis Section 4.1.2, Equations 4.2–4.7; Satterthwaite (1946).

### Slide 18 (Method · for Slide 5, step 3): Derivation 3 of 3: estimated and combined degrees of freedom

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

How do the moments become the formula used in the test, and how are P and Q combined?

**Answer to give**

“Putting the first-order mean and variance into the moment-matching rule gives two n V-squared over tau-squared. That is two divided by the relative variance of V-hat, so more relative variation gives fewer degrees of freedom. The test replaces V and tau-squared by their table estimates, which gives nu-hat for P, and the same for Q. To combine them, I apply moment matching once more to the squared standard error. The samples are independent, so the variances add, which gives the Welch–Satterthwaite formula.”

**Notes**

For the Slide 7 example at n = 1,000, the first-order component df are 15.30 against the moment target 21.03: approximately (1/1.19)²/0.97 = 0.73. The squared mean enters the target, so the mean ratio matters twice. Positive V does not guarantee positive tau-squared; a zero component is not an ordinary finite df.

**Source**

Thesis Sections 4.3.3–4.3.4, Equations 4.39–4.44 and Table 4.1; Satterthwaite (1946); Welch (1947).

### Slide 19 (Method · detail for Slide 16): Variance sensitivity in full

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

What exactly did you differentiate, and where do the margin terms enter?

**Answer to give**

“I differentiate the pointwise-MI variance along a one-observation perturbation. The first part changes the probability weights. The bracket also changes the log ratios, including their row and column margins. Both contributions are necessary because the pointwise-MI values themselves depend on the table.”

**Notes**

Assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. With every cell positive, positive MI is equivalent to positive V (Appendix A.3), but positive V does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.

**Source**

Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final), and definition of tau-squared (eq:tau-definition). The perturbation follows Hampel (1974) and van der Vaart (1998). This derivative is exact for positive population tables. Its use for sampling errors is first order.

### Slide 20 (Method · detail for Slide 16): Variance sensitivity in cell probabilities

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

What are g and tau-squared in familiar terms, and what do they reduce to in the cell probabilities?

**Answer to give**

“Each quantity has a familiar definition and a cell form. MI is the expected pointwise MI, and V is its variance. The row and column means are conditional expectations of pointwise MI. The sensitivity g is the derivative of V when a small amount of probability moves towards one cell. In cell terms, it is the squared deviation from MI minus V, plus twice the cell's pointwise MI after subtracting its row and column means and adding back MI. Tau-squared is the variance of those sensitivities, which is the probability-weighted average of their squares. The next slide works through the thesis example.”

**Notes**

The sensitivities have probability-weighted mean zero, so the weighted average of their squares is their variance. The estimates replace each p_ij with n_ij / n_P and sum over occupied cells; the estimate of tau-squared centres the sensitivities explicitly (Equation 4.42). The derivative is exact for positive population tables; its use for sampling errors is first order.

**Source**

Thesis Equations 2.3 and 2.4 (pointwise MI and MI), 4.7 (moment matching), 4.9–4.11 (V, the perturbation, and g), 4.29 (final form of g), 4.36 (tau-squared) and 4.41–4.43 (estimates); perturbation: Hampel (1974); van der Vaart (1998).

### Slide 21 (Method · example for Slides 16–20): Worked example: sensitivities and degrees of freedom

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Can you show the calculation with numbers?

**Answer to give**

“For cell (1, 1), the count is 35 and its row and column each total 50, so its pointwise MI is 0.385. Across the table, MI is 0.137 and V is 0.272. Row 1's mean pointwise MI is 0.103, and column 1's is the same. The sensitivity is the squared deviation 0.062 minus 0.272, plus twice 0.316, which gives 0.422. Repeating this for all nine cells gives tau-squared 0.932, and the component degrees of freedom are 16.65.”

**Notes**

Rounded thesis values: 0.38526, 0.13693, 0.27189, 0.10308, 0.4218, 0.93212 and 16.65. Row 1's pointwise-MI values are 0.38526, −0.51083 and −0.64436. The thesis prints only cell (1, 1)'s sensitivity; the other eight come from thesis Equation 4.41 and were recomputed from the counts, as were tau-squared and the df. Cell (1, 1) contributes 0.0593 to tau-squared. The results use unrounded values, so recomputing from the rounded inputs gives 16.67.

**Source**

Thesis Section 4.4.1, Equations 4.41–4.43 and 4.47.

### Slide 22 (Evaluation design · for Slide 6): Population construction, grid, and calculation requirements

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

How are known-MI populations generated and degenerate calculations handled?

**Answer to give**

“The copying probability changes association while preserving chosen margins. I solve it separately for each target MI. Unsuccessful calculations count as non-rejections, so the rate measures the complete procedure; calculation success is reported separately. Conditioning on success would describe a selected subset of sampled tables.”

**Notes**

Full requirements (Appendix B.3): a Wald calculation succeeds when it has a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14, and a finite p-value. The Expanded Welch calculation additionally requires positive finite component and combined degrees of freedom and a finite p-value; if either component fails, the Expanded Welch calculation is unsuccessful. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so the Expanded Welch calculation is unsuccessful even if the other table makes the shared standard error positive and finite. Zero and undefined component degrees of freedom are distinct cases; both fail the positive-finite requirement. A failed calculation is not evidence of equality.

Sampling is independent within and between populations, and both methods receive identical sampled pairs. The construction uses the same vector for row and column margins within each population and is one association family, not all categorical distributions.

**Source**

Thesis Chapter 5 and Appendix B.1–B.5; current grid results. The copying construction is a special case of the mixture model of Bocci et al. (2010) (thesis Section 5.1.1).

### Slide 23 (RQ1 · for Slide 7): Approximation ratios across table sizes

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colour now identifies table size; the rows are three different ratios.

**Question answered**

Is the 4×4 example representative of other sizes and both populations?

**Answer to give**

“The larger tables generally have higher mean peaks, deeper population-variance troughs, and slower recovery in this family. Sample substitution can overpredict even while population inputs underpredict. The main slide isolates one slice so these quantities can first be understood separately.”

**Notes**

Figure 6.2 separately checks how those moment errors affect df. In the worked 4×4/n=1,000 case, FO/target is about 0.73 and the exact values are 15.30/21.03; Slide 18's notes explain why. Do not infer the mean of estimated df by inserting mean inputs into a nonlinear ratio. Full current Figure 6.2 remains in the thesis; it is not needed as another timed slide.

**Source**

Sections 6.1.1–6.1.2, Figures 6.1–6.2, and current moments.csv; expected 80 rows: 4 sizes × 10 sample sizes × 2 populations.

### Slide 24 (RQ1 · for Slide 8): Near-independence noise calculation

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Why do the mean estimated df remain near five?

**Answer to give**

“Near independence, sampling noise creates apparent association. The quadratic likelihood-ratio approximation includes that noise. Substitution into the component formula gives roughly G divided by two, whose mean is about 4.6 in this setting. The population first-order formula instead approaches n times population MI. These are different approximations, which explains their separation.”

**Notes**

Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.

**Source**

Thesis Appendix A.2 and Section 6.1.3; Figure 6.3; Wilks (1938) for the chi-squared limit of 2nI-hat at independence and Banerjee (2005) for its noncentral form under local alternatives. These are local approximations under fixed dimensions and positive limiting cell probabilities, not exact finite-sample distribution identities.

### Slide 25 (RQ2 · for Slide 9): Full null results: uniform margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the shared MI, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

What happens outside the highlighted different-skew 16×16 example?

**Answer to give**

“Under the copying construction, equal MI and uniform margins give identical population tables. Their expected MI biases cancel in the difference, but errors in the uncertainty estimate and reference distribution can still cause excessive or conservative rejection. Increasing shared MI changes those patterns.”

**Notes**

All 120 settings for the uniform profile. Slide 9 plots each setting here as one point; its 8.35% to 4.90% example is the 4×4, n = 20, MI 0.02 setting.

**Source**

Final Figure 6.4 and balanced-null combined rates, uniform profile. This page contains all 120 settings for that profile.

### Slide 26 (RQ2 · for Slide 9): Full null results: same-skew margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the shared MI, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

What changes when both populations have the same uneven category frequencies?

**Answer to give**

“The population tables are still identical under equal MI, so expected bias in the difference cancels. Uneven margins leave more rare category combinations. The conservative ranges persist beyond the smallest samples and are not explained solely by calculation failures. Expanded Welch lowers those already-low rates further.”

**Notes**

All 120 settings for the same-skew profile.

**Source**

Final Figure 6.5 and balanced-null combined rates, same-skew profile. This page contains all 120 settings for that profile.

### Slide 27 (RQ2 · for Slide 9): Full null results: different-skew margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the shared MI, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

Are the severe failures restricted to the largest table, and what is visible over the complete margin-specific grid?

**Answer to give**

“Here equal MI permits different population tables. The remaining MI biases need not cancel, and in the sparse largest table they can shift the estimated difference substantially away from zero. The smaller-table patterns and the dependence on shared MI remain visible in this complete slice of the null grid.”

**Notes**

All 120 settings for the different-skew profile. The Slide 10 diagnostic table uses the MI 0.02, n = 1,000 slice of these populations.

Additional anchor: At MI .005, n=1,000, and 16×16, Wald is 36.38% and Expanded Welch 34.38%, with every calculation successful in both tests. This is a different shared-MI level from the diagnostic table's .02; do not interchange the numbers.

**Source**

Final Figure 6.6 and balanced-null combined rates, different-skew profile. This page contains all 120 settings for that profile.

### Slide 28 (RQ2 · for Slide 10): Ordinary Welch degrees of freedom

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Would ordinary Welch degrees of freedom work as well as the MI-specific calculation?

**Answer to give**

“Ordinary Welch keeps the same estimated MI difference, standard error, and statistic, but gives each component n minus one degrees of freedom, the rule for comparing sample means. For MI that is only a benchmark, because it ignores how the pointwise-MI variance estimate changes with the table. At n = 20 it removes less of the excess than Expanded Welch. At n = 50, where Wald is already close to 5%, Expanded Welch becomes the most conservative. In the biased 16×16 case neither choice removes the excess. So the MI-specific calculation changes the results, but a larger reduction in rejection does not consistently improve calibration.”

**Notes**

The three settings reuse the main null study's 100,000 sampled pairs per setting at shared MI 0.02 nats with n_P = n_Q = n; all three methods' calculations succeed in every repetition. The thesis examines ordinary Welch only at these illustrative settings and lists this as a limitation (Section 7.2); the main comparison is with the Wald test.

**Source**

Thesis Section 6.2.5, Table 6.2; Section 7.2.

### Slide 29 (RQ3 · for Slides 11–12): Full power results: uniform margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the MI gap, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

How does absolute power change with MI gap, sample size, and table size under uniform margins?

**Answer to give**

“The complete uniform-margin grid shows the increase in detection with sufficient observations and the stronger-gap advantage. Larger tables need more data. Expanded Welch never exceeds Wald under the usual thresholds, with method differences becoming small at larger sample sizes.”

**Notes**

120 settings, 240 method rows for this margin profile.

**Source**

Section 6.3.1, Figure 6.7; power rates, profile=uniform, denominator=all. At n=10,000 and gap=.01, EW is 89.44% for 2×2 and 71.12% for 16×16. These values describe the stated population family.

### Slide 30 (RQ3 · for Slides 11–12): Full power results: same-skew margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the MI gap, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

Do the power patterns also occur when both groups have the same uneven margins?

**Answer to give**

“These power curves use the same uneven margins in both populations. Larger tables need more observations, and the smaller MI gap remains harder to detect. For example, at n=50,000, the 16×16 Expanded Welch power is 79.87% for the smallest gap, compared with more than 99.9% for each of the two larger gaps. The method difference is smaller than these gap and setting effects at larger sample sizes.”

**Notes**

All 120 settings for the same-skew power profile.

**Source**

Final Figure 6.8; Section 6.3.2; MI-gap combined rates, same-skew profile. This page contains all 120 settings for that profile.

### Slide 31 (RQ3 · for Slides 11–12): Full power results: different-skew margins

Not part of the timed talk. Return to Slide 13 afterwards.

**When opening**

Colours here identify the MI gap, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

How does the bias-related failure vary with gap and table size?

**Answer to give**

“Unequal residual biases can shift the estimated difference opposite to its true sign. The two-sided rate includes those rejections. As the bias shrinks, rejection can first fall and later recover. Gap size and margins therefore affect power through the estimator's behaviour as well as the true separation.”

**Notes**

120 settings, 240 method rows. The main point is 16×16, gap 0.01, n = 1,000.

At the main point the mean estimate is +.0206714 for true −.01. Of 9,662 EW rejections, 9,659 are positive and 3 negative. Do not apply that conditional percentage to the entire grid or all 100,000 estimates.

**Source**

Section 6.3.3, Figure 6.9, and current power CSVs, profile=different_skew, denominator=all.

### Slide 32 (References): References: MI and testing foundations

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

### Slide 33 (References): References: related methods and evaluation

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

## 8. Question preparation

Give a direct answer, a short reason, and a stopping point. Open a backup
when it clarifies the explanation. These are starting answers, not text
to read verbatim. Keep the cited boundary when the study did not evaluate
a proposed extension.

| Likely question | Suggested answer and boundary | Destination |
| --- | --- | --- |
| What exactly is new here? | “The MI first-order variance and the general Satterthwaite principle are established. I derive the MI variance sensitivity including the changing margins, use it for component df, and evaluate where the resulting approximation succeeds or fails.” Avoid a claim of global priority beyond the literature review. | Slides 16–20 |
| Why not just use sample size minus one? | “That assignment follows from the ordinary sample-variance distribution under normal sampling. An estimated pointwise-MI variance depends on changing probabilities and log ratios, so I calculate its sampling variability instead.” | Slides 17 and 28 |
| Why does moment matching imply a Student t test? | “It motivates an approximate reference distribution. Matching a variance component to a scaled chi-squared distribution does not establish the standard normal numerator, or its independence from the variance estimates, that an exact Student t distribution requires.” | Slide 17 |
| Where does the variance of V-hat come from? | “V-hat is V at the sample table, which is an average of one-observation tables. A first-order expansion turns its error into an average of one sensitivity per observation, so its variance is tau-squared over n.” | Slide 16 |
| How are the two component df combined? | “By moment matching once more, now on the squared standard error. The samples are independent, so the variances add, which gives the Welch–Satterthwaite formula.” | Slide 18 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | Slides 22 and 27 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | Slide 22; thesis Section 2.4 |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 13 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap, and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 11–12 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 11 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | Slide 31; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 12 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | Slide 24 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | Slides 17 and 24 |
| Could unsuccessful calculations explain the low rejection? | “They contribute at some small sample sizes. I report calculation success separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation succeeds.” | Slides 9–10, 22 and 25–27 |
| Why count unsuccessful calculations as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to successful calculations would condition on a selected subset. Reporting calculation success separately makes the distinction visible.” | Slide 22 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | Slide 15; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | Slides 22 and 25–31 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even when every calculation succeeds.” | Slides 9–13 |
| Why judge accuracy with a 4–6% band? | “The band is only descriptive: 4–6% gives 130 settings for Wald and 136 for Expanded Welch, but 4.5–5.5% gives 105 and 98. The answer rests on the pattern on Slide 9 and the mechanisms on Slide 10, not on a band.” | Slides 9–10 |
| Did you apply the tests to real data? | “Yes. Thesis Section 6.4 compares month–purchase and weekend–purchase MI between new and returning visitors in the Online Shoppers data. I left it out of this talk because unknown population tables cannot show which test is accurate; the known-population simulations carry that evidence.” | Thesis Section 6.4 |
| How much computation does one test require? | “The calculations use a fixed number of scans of an r-by-c table, so time and working memory are O(rc). I have not used this presentation to claim a measured runtime advantage over resampling.” | Slides 16–20; thesis Section 4.4 |

If a requested comparison was not performed, name that limitation and the
specific result established here. Do not invent a broader conclusion.

## 9. Rehearsal and timing control

Learn the argument before memorising wording. Rehearse from the purpose
and delivery cues after learning the scripts. Keep full scripts in notes.
A listener new to this derivation should be able to identify the research
question, the two levels of variance, the change in cutoff, and the main
reason that cutoff adjustment leaves some failures unresolved.

Allow pauses after introducing axes, between the two variance levels, and
after the signed-number comparison on Slide 12. Explain a chart before
moving to its mechanism panel. Do not read all numerical labels. Explain
which comparison they support. Rehearse the exported PDF as well as the
PowerPoint, including jumping from Slide 13 to backups and back.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 3 | 2:40 | Keep literature roles concise; do not recite citations. |
| End of Slide 6 | 7:25 | Use the short form of Slide 7; protect near independence. |
| End of Slide 8 | 11:05 | Shorten Slide 9's rate narration and read only its key comparison. |
| End of Slide 10 | 14:20 | Use the compact Slide 11 explanation; protect the directional result. |
| End of Slide 12 | 17:50 | Begin the conclusion immediately; do not open backups. If past 18:30, use the emergency close below. |

### Prepared shorter route

| Slide | Planned | Short form | Preserve |
| --- | --- | --- | --- |
| 2 | 1:15 | 1:00 | Two populations, their estimates, and the population hypothesis |
| 3 | 1:00 | 0:50 | Existing foundations and required MI-specific calculation |
| 4 | 1:20 | 1:10 | Shared statistic and visible cutoff difference |
| 5 | 2:05 | 1:40 | Two levels of variation, definitions of g and tau-squared, df consequence, and approximation status |
| 6 | 1:20 | 1:10 | Copying construction, parallel studies, sample size versus repetitions, and unsuccessful-calculation rule |
| 7 | 1:40 | 1:25 | Mean/variance distinction and the 19%, 3%, and 8% anchors |
| 9 | 1:30 | 1:20 | Axes and diagonal, improvement above 5%, no improvement below 5%, and remaining severe rejection |
| 10 | 1:45 | 1:35 | One line per row: difference-bias cancellation, underestimated or overestimated variation, and residual bias |
| 11 | 1:30 | 1:20 | Power definition, median/range, small-sample loss, and under 0.32 points at n = 10,000 |
| 13 | 1:00 | 0:50 | Three contributions, one finding per research question, scope, and the overall scientific finding |

These reductions total 125 seconds, giving **16:45**. Slides 8 and 12
remain at full length because they carry important explanations. Use this
route to simplify narration, not to speak faster.

### If Slide 12 ends at 18:30

- **Slide 13, about 50 seconds:** “I derived MI-specific variance
  sensitivity and degrees of freedom. The larger cutoff improves some
  excessive false-positive rates, while deepening conservatism and reducing
  power elsewhere. The remaining bias can even reverse the estimated
  direction. Improving estimation, retaining sampling variation near
  independence, and testing broader populations are the next steps.
  Thank you.”

This route finishes at about 19:20. Do not cut the conclusion, start
narrating backup slides, or fill spare time with an unplanned experiment.
Timing remains provisional until a complete timed rehearsal.
