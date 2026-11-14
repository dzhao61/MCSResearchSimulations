# Comparing Mutual Information in Finite Samples: speaker notes

Daniel Zhao. Talk target 18:50 for Slides 1–13; Slide 13 stays up for questions. Slide 14 is the appendix title and the backups are Slides 15–33.
The notes for Slides 1–13 and the question guides under Slide 14 are the spoken script (Rehearsal/Daniel_Zhao_Welch_MI_Presentation_Script_Spoken.md, 14 November 2026), word for word. The backup notes (Slides 15–33) come from the presentation execution plan.

## Main talk

### Slide 1: Comparing Mutual Information in Finite Samples

Hi everyone, today I'll talk about comparing mutual information between two populations.

### Slide 2: Motivation: comparing MI across populations

Mutual information, or MI, measures how much knowing one variable reduces uncertainty about another, on average. If the variables are independent, MI is zero.

The hypotheses at the top compare MI for the same two categorical variables, X and Y, in populations P and Q. The null says their population MI values are equal. The alternative says they differ.

On the left, each observation gives us a pair: one category for X and one for Y. We count how often each pair occurs and estimate MI from that count table. We do that for each population. Even if the populations have equal MI, those estimates can differ. So the last step on the right asks whether sampling noise could explain the difference we see.

In the example at the bottom, imagine X is a student's mid-semester test grade and Y is their final exam grade, both recorded as categories. The two populations are students before and after generative AI. Does knowing the mid-semester grade tell us as much about the final grade in both groups?

### Slide 3: Literature review: foundations and the MI-specific step

The left column gives us an MI estimator, a leading bias correction, and a first-order approximation for its sampling variance. The step I need is to work out how much the variance estimate itself changes between samples.

In the middle is the Wald test. It uses the standard normal distribution to approximate how the test statistic behaves when population MI is equal. I check how well that cutoff works in finite samples.

The right column introduces Welch–Satterthwaite moment matching. It uses the mean and variance of the estimated variance contributions to choose degrees of freedom. For MI, that requires a new calculation of variance sensitivity.

At the bottom are my three steps: derive that sensitivity, use it to construct the Expanded Welch test, and compare the two tests in simulations.

### Slide 4: Method: one statistic, two reference distributions

In the box on the left, both tests start with the estimated MI in P minus the estimated MI in Q. They correct for the leading bias and divide by the estimated standard error. For example, plus two means the corrected difference is two standard errors above zero. The two-sided test uses the distance from zero in either direction.

In the second equation, V-hat estimates the variance of pointwise MI, the information contribution of each category pair. Dividing V-hat by sample size estimates the sampling variance of MI. The samples are independent, so we add those two estimates to get the squared standard error.

In the blue box, the Wald test uses the standard normal distribution. At the 5% significance level, its cutoff is about 1.96 in either direction.

In the green box, the Expanded Welch test uses a Student t distribution as its reference. I estimate the degrees of freedom from the tables to account for how much the variance estimates can vary.

On the right, the dashed green curve shows a Student t distribution with five degrees of freedom. Its heavier tails put the 5% rejection region further out, past about 2.57 in either direction. Five is just for illustration. With more degrees of freedom, the cutoff gets closer to the Wald cutoff.

Since both tests use the same statistic and the Expanded Welch cutoff is larger, every Expanded Welch rejection is also a Wald rejection. So how do I choose the degrees of freedom that set that cutoff?

### Slide 5: Approach and contributions

Start with the orange panel on the left. Each dot in this sketch is a V-hat from a different sample of the same size. V-hat measures variation in pointwise MI within one sample. The spread of the dots is a second kind of variation: how much V-hat itself changes between samples. The dashed line marks the population value V.

To explain that spread, look at the middle panel. I start with one cell: if I move a little probability towards it, how quickly does V change? That shift changes the cell weights, the row and column totals, and the pointwise MI values that depend on them. I call that sensitivity g. Its sign tells us whether V initially rises or falls.

A random observation lands in one cell and picks out that cell's g. Tau-squared is the variance of g across observations from the population.

The first-order expansion keeps the linear effect of changes in the table, so the error in V-hat is approximately the average of the sensitivities in the sample. The sensitivities average to zero in the population, so the approximation centres V-hat at V. The observations are independent, so the variance of their average is tau-squared divided by sample size. That's the approximation at the top of the panel.

In the green panel, I use the mean and sampling variance of V-hat to choose degrees of freedom. Matching those two quantities to a scaled chi-squared distribution gives the first formula: twice the squared mean divided by the variance. For a given mean, more variation gives fewer degrees of freedom and a larger cutoff. The second formula uses V as the approximate mean and tau-squared over sample size as the approximate variance, with both inputs estimated from the table for P. That gives the component degrees of freedom, meaning the value for one population.

At the bottom, I repeat the calculation for Q and use the Welch–Satterthwaite rule to combine the two into the degrees of freedom for the Student t distribution. RQ1 checks both approximations.

### Slide 6: Evaluation design

On the left are the three questions. RQ1 checks the approximations, including near zero MI. RQ2 checks false-positive rates when MI is equal, and RQ3 checks power. For the power study, I keep MI in P at 0.02 nats and give Q the higher value. MI is in nats because I use natural logarithms.

On the right, there are four table sizes, from two by two to sixteen by sixteen. The margin labels describe the category frequencies: uniform means equally frequent, same-skew means uneven in the same way in both populations, and different-skew means uneven in different ways. With ten sample sizes and three MI levels or gaps, that gives 360 settings per study for RQ2 and RQ3.

I draw 100,000 independent table pairs per setting. Both tests get the same pairs, so a difference in their decisions can't come from using different samples.

The model line shows how I set population MI. I draw X, then either copy its category into Y or draw Y independently from the same frequencies. I adjust the probability of copying to reach each target MI without changing the category frequencies.

At the bottom, both tests use a 5% significance level. If a calculation fails, I count it as a non-rejection and report calculation success separately.

### Slide 7: RQ1 results: approximation accuracy

Both graphs vary sample size. They show population P in a four-by-four, different-skew setting, with population MI of 0.02 nats.

The top graph divides average V-hat by population V. The ratio is well above one for small samples, so the first-order approximation gives too low a mean there. As sample size grows, the curve comes down towards one.

The box beside the top graph points to one reason. A rare category pair that appears in a sample can have a pointwise MI far from the table's MI. Squaring that gap can push V-hat up. Even at 1,000 observations, average V-hat is still 19% above V.

The lower graph divides the predicted sampling variance of V-hat by the variance observed across repeated samples. Below one means the prediction is too low, and above one means it's too high.

The solid navy curve uses the population tau-squared. Rare cells appearing in some samples but not others can produce changes larger than the linear approximation predicts. At the same sample size of 1,000, this prediction is about 3% low.

The dashed orange curve uses tau-squared estimated from each table, then averages the resulting predictions. Estimating sensitivities from sparse counts can instead overpredict the variation; at that sample size, the prediction is about 8% high.

Look at the summary at the bottom. The population inputs give us a fairly accurate prediction of the variance even though they give us too low a mean. Moment matching squares the mean, so using that lower value can push the degrees of freedom down.

### Slide 8: RQ1 results: near independence

Here the table size stays four by four and sample size stays at 1,000. We move left towards smaller population MI on the log scale and look at the component degrees of freedom on the vertical axis.

Start with the green line. It is the moment-matching target, calculated from V-hat's mean and variance across repeated samples. At the leftmost point, the target is about 9.1.

The dotted navy line uses known population inputs in the first-order formula, as explained in the navy box. Close to zero MI, this component value is approximately sample size times population MI, so it heads towards zero. At the same MI value it is about 0.1, far below the target.

The orange line averages the component degrees of freedom estimated from the sampled tables. As the orange box explains, at zero population MI the linear term in the uncorrected MI estimate vanishes, but squared probability errors can still make that estimate positive. The calculation from each table picks up that noise. The bracket shows the result: about 4.9, roughly half the target.

Hitting that target would still leave us with a question: how often do the tests reject when population MI is equal?

### Slide 9: RQ2 results: false positives across all null settings

Each dot is one of the 360 equal-MI settings. The horizontal axis shows the Wald test's false-positive rate, and the vertical axis shows Expanded Welch's. The dashed lines mark 5%.

The diagonal means equal rejection rates. All points lie on or below it because Expanded Welch can only reduce rejection.

Start with the top box on the right. The Wald test is above 5% in 178 settings, and Expanded Welch gets closer to 5% in 165 of them. The highlighted uniform example goes from 8.35% to 4.90%.

In the next box, the Wald test is below 5% in 180 settings. Expanded Welch pushes the rate even lower in 176 of those and leaves four unchanged.

At the bottom right, the two tests land in the 4% to 6% band in roughly the same number of settings. Now look at the circled different-skew example near the top right of the plot. Here the shared MI is 0.005 nats. The false-positive rate falls from about 36% to about 34%, still far above 5%.

To see why a larger cutoff helps in some settings and does little in others, let's look at the estimated difference and its standard error.

### Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

All three rows use equal MI of 0.02 nats, and every calculation succeeds. The bias column shows how far the average estimated difference is from zero, in sampling standard deviations. In the next column, one means the average squared standard error matches the observed variance of the estimated difference.

In the uniform row, the biases cancel in expectation, so the difference is centred near zero. The variance ratio is below one, so the squared standard error is too small on average. For a given difference, a smaller standard error puts the statistic further from zero. Here the larger cutoff offsets that, bringing the false-positive rate from 8.35% to 4.90%.

In the same-skew row, the biases again cancel in expectation, but the variance ratio is nearly two. That overstatement of uncertainty helps explain why the Wald test rejects only about 0.6% of the time. The larger cutoff pushes it further below 5%, to about 0.5%.

The third row keeps the table size and sample size but uses different-skew margins. The variance ratio is still nearly two, but now the estimated difference averages about two sampling standard deviations above zero. The false-positive rate only falls from about 26% to about 25%. As the final box shows, changing the cutoff leaves that bias in place.

The takeaway at the bottom is that a larger cutoff can offset a standard error that's too small, but it leaves the bias in the estimated difference unchanged.

### Slide 11: RQ3 results: the power cost of the larger cutoff

Power is the chance of detecting a real MI difference. This graph shows how many percentage points of power Expanded Welch loses compared with the Wald test. The line is the median loss across 36 settings at each sample size, and the shading shows the full range.

The upper-right box summarises the small-sample cost. With ten observations per population, the median loss is about six percentage points, partly because some calculations fail. From 50 to 1,000 observations, the median loss is about one point. By 10,000, even the largest loss is less than a third of a percentage point.

Both tests use a 5% significance level. Their actual false-positive rates can differ, so read the power results alongside those rates.

The lower-right box concerns absolute power. Even at 50,000 observations, the smallest MI gap of 0.005 nats gives Expanded Welch power of about 80% to 96%. Power is above 99.9% for the two larger gaps. So the two tests can have similar power and still miss some real differences when the MI gap is small.

At the bottom, notice that power counts rejections in either direction. Next, we'll see what happens to the estimated sign.

### Slide 12: RQ3 results: bias can reverse the estimated direction

This heat map uses different category frequencies and an MI gap of 0.01 nats, with Q always having greater population MI. Rows show table sizes and columns show sample sizes.

Each cell shows the share of Expanded Welch rejections that point to the wrong population. So 50% means about half the rejections point to P as having higher MI.

The dark cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range.

Look at the outlined sixteen-by-sixteen cell at 1,000 observations per population. Q truly has more MI, by 0.01 nats. On average, the estimate points the other way and puts P ahead by about 0.02 nats. Expanded Welch rejects in about 10% of repetitions. Almost every one of those rejections points to P as having higher MI.

The next box shows why. The table sizes and sample sizes match, so the two leading corrections cancel in the difference. But the remaining bias pulls Q's estimate down more than P's. That shifts the estimated difference up by about 0.03 nats, three times the true gap. The cutoff can't undo that shift. With 10,000 observations per population, fewer than 0.4% of rejections pointed the wrong way in every setting at that sample size.

At the bottom is the tally across all 360 power settings. In 28 settings, at least 90% of rejections point the wrong way. All 28 use different-skew margins with eight-by-eight or sixteen-by-sixteen tables. Those rejections still count towards two-sided power.

### Slide 13: Conclusions and next steps

Across the top are the three contributions. First, I derived how a change in the probability table affects pointwise-MI variance. Second, I used that result to choose degrees of freedom for the Student t distribution. Third, I evaluated the approximations and compared the tests in simulations.

In the next row, RQ1 shows that the approximations generally improve with sample size, but the first-order calculation misses sampling noise near zero MI.

For RQ2, the larger cutoff brings many excessive false-positive rates closer to 5%, but pushes them further below 5% when the Wald test already rejects too rarely.

For RQ3, Expanded Welch can't have higher power than the Wald test at the same 5% significance level. A large enough bias can also make rejections point to the wrong population.

These findings come from one way of constructing populations, equal sample sizes, and a comparison with the Wald test.

The first next step is to reduce bias in the estimated MI difference and improve its standard error and degrees of freedom, including when population MI is close to zero.

The second is to evaluate other population constructions and unequal sample sizes.

Overall, the cutoff adjustment helps in some settings, but reliable comparisons also require accurate estimates of the MI difference and its standard error.

Thank you.

## Appendix

### Slide 14: Appendix title

Questions and answer guides

1. What is your main contribution?

• I derived the MI-specific sensitivity of the pointwise-MI variance as the cell probabilities, margins, and log ratios change.
• That gives the sampling-variance approximation needed to estimate component degrees of freedom and combine them using the established Welch–Satterthwaite rule.
• I evaluated approximation accuracy, false positives, power, and calculation success. Keeping the same estimated difference and standard error as the Wald test lets me isolate the effect of changing the reference distribution.

2. What do V, g, and tau-squared actually mean?

• V measures variation in pointwise MI across outcomes. V-hat estimates it from one table, and V-hat divided by n estimates MI's sampling variance.
• g measures how sensitive V is to shifting probability towards a particular cell, including the resulting changes in the margins. Slide 20 gives the cell formulas, and Slide 21 works through an example.
• Tau-squared is the variance of those sensitivities across outcomes. The sampling variance of V-hat is approximately tau-squared divided by n; tau is the standard deviation of the sensitivities.

3. Where do the degrees of freedom come from, and is the Student t distribution exact?

• A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu. Matching moments gives nu as twice the squared mean divided by the variance.
• Approximating those moments by V and tau-squared/n gives component degrees of freedom of about 2nV²/tau-squared. The test estimates the inputs from each table. Slides 16–18 walk through the sampling variance, moment matching, and the combined degrees of freedom.
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

• With equal dimensions and sample sizes, the two leading bias corrections cancel exactly in the MI difference. Slide 15 shows the correction and why it cancels.
• Higher-order biases remain. Identical population tables have matching expected biases, but distinct tables can have unequal biases even when their MI values agree.
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
• In the highlighted example, the true difference is −0.01, but its estimated mean is about +0.0207 because the biases remaining after correction differ enough to outweigh the gap.
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

### Slide 15 (Method · for Slide 4): Bias correction

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Which bias correction do you use, and why does it not remove the bias seen on Slides 10 and 12?

**Answer to give**

“Each MI estimate subtracts the leading bias, (r − 1)(c − 1) over 2n, which is Miller's correction. In every simulation the two samples have the same size and table dimensions, so the two corrections are equal and cancel from the difference. What remains is higher-order bias, which depends on the whole probability table. Distinct tables with equal MI can have different remaining biases, and that shifts the estimated difference, as on Slides 10 and 12. Reducing that bias is my first next step.”

**Notes**

The leading term is 0.1125 nats per estimate for 16×16 at n = 1,000, and 0.225 nats for 4×4 at n = 20. With unequal sample sizes, the correction removes the leading unequal-sample bias; its performance there is untested (thesis Section 7.2). Corrected estimates can be negative and are retained. Empty sampled cells contribute nothing to the plug-in sum.

**Source**

Thesis Equations 2.7–2.9 and 3.7; Sections 2.2, 3.1.2, 5.5 and 7.2; Miller (1955); Panzeri and Treves (1996); Paninski (2003); Chao and Shen (2003); Nemenman et al. (2002).

### Slide 16 (Method · for Slide 5, step 2): Derivation 1 of 3: how much the variance estimate varies

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

Where does Var{V-hat(P)} ≈ tau-squared(P)/n_P come from?

**Answer to give**

“V-hat is V evaluated at the sample table, and the sample table is an average of one-observation tables. A first-order expansion is linear in the table change, so the error in V-hat becomes an average of one sensitivity per observation. The sensitivities average to zero, so V-hat is centred on V to first order. Because the observations are independent, the variance of that average is the variance of one sensitivity, tau-squared, divided by n.”

**Notes**

The expansion follows the straight line P + t(P-hat − P) from t = 0 to t = 1; the omitted terms are quadratic or higher in the cell-probability errors. The derivative of an average table change is the average of the one-observation derivatives because the linear term has fixed coefficients at P (thesis Section 4.3.1, citing van der Vaart, 1998, Chapter 20). Any bias in V-hat comes from terms beyond this linear approximation. Slide 7 shows both checks: the mean of V-hat over V, and the predicted over the observed variance.

**Source**

Thesis Sections 4.2.1, 4.3.1 and 4.3.2; Equations 4.10, 4.11, 4.30, 4.31 and 4.35–4.38.

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

Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final), and definition of tau-squared (eq:tau-definition). This derivative is exact for positive population tables. Its use for sampling errors is first order.

### Slide 20 (Method · detail for Slide 16): Variance sensitivity in cell probabilities

Not part of the timed talk. Return to Slide 13 afterwards.

**Question answered**

What are g and tau-squared in familiar terms, and what do they reduce to in the cell probabilities?

**Answer to give**

“Each quantity has a familiar definition and a cell form. MI is the expected pointwise MI, and V is its variance. The row and column means are conditional expectations of pointwise MI. The sensitivity g is the derivative of V when a small amount of probability moves towards one cell. In cell terms, it is the squared deviation from MI minus V, plus twice the cell's pointwise MI after subtracting its row and column means and adding back MI. Tau-squared is the variance of those sensitivities, which is the probability-weighted average of their squares. The next slide works through the thesis example.”

**Notes**

The sensitivities have probability-weighted mean zero, so the weighted average of their squares is their variance. The estimates replace each p_ij with n_ij / n_P and sum over occupied cells; the estimate of tau-squared centres the sensitivities explicitly (Equation 4.42). The derivative is exact for positive population tables; its use for sampling errors is first order.

**Source**

Thesis Equations 2.3 and 2.4 (pointwise MI and MI), 4.7 (moment matching), 4.9–4.11 (V, the perturbation, and g), 4.29 (final form of g), 4.36 (tau-squared) and 4.41–4.43 (estimates).

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

Thesis Chapter 5 and Appendix B.1–B.5; current grid results.

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

Thesis Appendix A.2 and Section 6.1.3; Figure 6.3. These are local approximations under fixed dimensions and positive limiting cell probabilities, not exact finite-sample distribution identities.

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
