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

## Questions and answer guides

### Main question and contribution

#### 1. What is the main contribution of your thesis?

- The MI-specific step is deriving how the pointwise-MI variance changes when the underlying table changes, including changes in the margins and log ratios.
- That sensitivity gives a first-order approximation to the sampling variance of V-hat, which supplies the component degrees of freedom.
- Welch–Satterthwaite moment matching is established. My contribution is its MI-specific calculation and the evaluation of the resulting test.
- The results identify both useful cutoff adjustments and failures caused by estimation errors that the adjustment leaves unchanged.

#### 2. What does MI measure, and why use it rather than correlation?

- MI measures the average reduction in uncertainty about one variable from observing another. For these discrete variables, it is zero exactly at independence.
- It can describe association beyond a linear relationship and works directly with categorical joint probabilities. It does not establish causation.
- Population MI is non-negative, but an individual pointwise-MI value can be negative when a category pair occurs less often than its marginal probabilities would suggest.
- MI measures the amount of association, without giving a positive or negative direction like correlation. The sign in this talk belongs to the difference between two MI values.

#### 3. Does equal MI mean the two populations have the same distribution?

- No. Different joint probability tables can have the same MI, just as different distributions can have the same mean.
- The hypothesis equates one numerical feature, I(P) and I(Q), while allowing category frequencies and association patterns to differ.
- This distinction matters because the two estimators can have different residual biases under the null, and a test of complete distributional equality answers a different question.

#### 4. How is Expanded Welch different from ordinary Welch, and why call it expanded?

- Ordinary Welch compares means and uses component degrees of freedom of n minus one, justified by the sample-variance calculation for populations with normal distributions.
- Here, pointwise-MI values depend on the estimated table. Expanded Welch derives the variability of their variance estimate as the cell probabilities, margins, and log ratios change.
- The name refers to that expansion. The way the two component degrees of freedom are combined follows the established Welch–Satterthwaite rule.

#### 5. If Expanded Welch cannot have higher power, why is it worth studying?

- A method can reject more often under alternatives partly because it also rejects too often under the null. Higher rejection alone does not establish better inference.
- Expanded Welch can bring an excessive false-positive rate closer to 5%, with a corresponding cost in detection probability at the same nominal level.
- The benefit depends on the setting. Where Wald already rejects too rarely, lowering rejection further makes the false-positive rate worse.

### Derivation and assumptions

#### 6. What is the difference between V, V-hat, and the variance of V-hat?

- V is the population variance of pointwise MI across possible observation outcomes.
- V-hat estimates V from one sampled table. V-hat divided by sample size estimates the sampling variance of the MI estimate.
- The variance of V-hat describes how much the variance estimate itself changes across new samples. This is the additional quantity needed for moment matching.
- Keep the two levels separate: variability of the information contributions, and variability of the estimate calculated from a whole table.

#### 7. What exactly is g_P(x,y)?

- It is the derivative of V along the path that mixes a small amount of probability onto cell (x,y), while reducing the original probabilities proportionally.
- At a fixed cell and population table, g is a fixed sensitivity. A positive value means V initially increases along that path; a negative value means it decreases.
- When the sampled outcome is random, g_P(X,Y) is random because different outcomes select different cell sensitivities.
- Its formula includes changing probability weights and changing pointwise-MI values. It describes the sensitivity of V, rather than the information contribution itself.

#### 8. What is tau-squared, and how is it different from tau or V?

- Tau-squared is the population variance of g_P(X,Y): it measures how much the observation-level sensitivities differ across outcomes.
- Tau is its non-negative square root, so tau is a standard deviation and tau-squared is a variance. The formulas in this talk use tau-squared.
- V measures variation in pointwise MI. Tau-squared measures variation in the sensitivity of that variance, so they describe different objects.
- Greater tau-squared means a larger first-order sampling variance of V-hat at a fixed sample size. Its effect on degrees of freedom also depends on V's magnitude.

#### 9. Why do the row and column terms appear in g?

- Pointwise MI is a log ratio of a joint probability to the product of its two marginal probabilities.
- Increasing one cell's probability also changes its row and column probabilities. Differentiating only the joint probability would miss part of the change in the log ratio.
- The conditional-mean terms collect those marginal effects when the derivative is averaged over the table. Omitting them would describe a different sensitivity.

#### 10. Could you just write MI as three entropies and apply an existing entropy test?

- MI equals H(X) plus H(Y) minus H(X,Y), but all three estimates use the same observations and have dependent errors.
- Treating their variances as three independent contributions would miss covariance terms. Hutcheson's entropy comparison does not automatically provide the required MI calculation.
- An entropy-based derivation could retain those dependencies, but choosing MI-specific Satterthwaite degrees of freedom still requires the sampling variability of the MI variance estimate.

#### 11. How do you get from one-cell sensitivity to tau-squared divided by n?

- The first-order expansion writes V-hat minus V approximately as the average of g evaluated at the sampled observations.
- Those sensitivities have mean zero and variance tau-squared. Independent observations make the variance of their average tau-squared divided by n.
- The variance calculation for that average is exact under independence. Approximating the sampling error by that average is the first-order step.

#### 12. Why does g have mean zero?

- In the centred squared-pointwise-MI part, the expected squared deviation is V, so subtracting V gives mean zero.
- In the remaining bracket, pointwise MI and each of its two conditional means all average to I. The bracket therefore averages to I minus I minus I plus I, which is zero.
- This centring is why the linear expansion has no first-order bias. It does not imply that the full finite-sample estimator is unbiased.

#### 13. Where does the degrees-of-freedom formula come from?

- A scaled chi-squared distribution with mean m and degrees of freedom nu has variance 2m²/nu.
- Matching that variance to the sampling variance of V-hat gives the target: twice the squared sampling mean divided by the sampling variance.
- Using mean approximately V and sampling variance approximately tau-squared/n gives the population first-order value, 2nV²/tau-squared. Replacing its inputs by estimates gives the actual sample-based component value.
- This is an effective measure of relative variance uncertainty. It can be fractional and is not simply a count of observations or cells.

#### 14. Why does dividing V-hat by n leave its component degrees of freedom unchanged, and how do you combine the components?

- Dividing by fixed n divides the squared mean and the variance by n². Those factors cancel in the moment-matching ratio.
- The two samples are independent, so the sampling variances of their estimated variance contributions add.
- The combined degrees of freedom are the squared total variance contribution, divided by the sum of each squared contribution over its component degrees of freedom.
- If one contribution dominates, its uncertainty largely controls the combined value. Equal sample sizes alone do not make the two contributions equal.

#### 15. Does your derivation prove that the statistic follows a Student t distribution?

- No. An exact Student t construction requires a numerator with a standard normal distribution and an independent denominator based on a suitably scaled chi-squared distribution.
- Here, the MI estimate and its estimated variance come from the same counts. Moment matching does not prove their independence or determine the full denominator distribution.
- The derivative defining g is exact for positive population tables, but the sampling expansion and the Student t reference distribution are approximations.
- Even matching the component moment target perfectly would not, by itself, prove correct test rejection rates. That is why the decision-level simulations are necessary.

#### 16. What assumptions does the method require?

- Observations are independent and identically distributed within each population, and the two samples are independent.
- Both tables use the same fixed category definitions, and every population cell has positive probability.
- The first-order construction requires positive pointwise-MI variances and positive variances of the sensitivities. Exact independence is a boundary where the first-order calculation degenerates.
- The asymptotic argument holds dimensions and population probabilities fixed as sample sizes grow. Sparse samples can still give poor approximations under those population assumptions.

#### 17. Does positive MI guarantee that the degrees-of-freedom formula is well defined?

- Positive MI and positive V do not by themselves guarantee positive tau-squared. The sensitivity can vanish at an associated population where V is locally stationary.
- A zero first-order sensitivity variance does not prove that V-hat is constant across samples. Higher-order sampling variation can remain.
- If the estimated sensitivity variance is zero, the implemented finite-degrees-of-freedom calculation fails its numerical requirements. Population degeneracy would require a separate higher-order argument.

#### 18. Why is independence a problem if it is such a simple population?

- At independence, every population pointwise-MI value is zero. Both MI and V are therefore zero, and the first-order sampling contributions vanish.
- Sample counts can still show apparent association. Its leading contribution comes from squared probability errors, so it needs a second-order description.
- Close to independence, those omitted terms can remain important relative to the small linear contribution. Large-sample accuracy at a fixed positive MI does not guarantee uniform accuracy as MI approaches zero.
- The thesis explains this boundary behaviour; it does not establish a replacement test valid across the boundary.

#### 19. Shouldn't the degrees of freedom always be large when the sample is large?

- For a fixed positive-MI population with positive tau-squared, the population first-order component value grows in proportion to n. The Student t distribution then approaches the standard normal distribution.
- Sample size alone does not determine the value: the formula also depends on V squared relative to tau-squared. Close to independence, the population approximation is roughly n times MI.
- A large n can therefore coexist with modest degrees of freedom when association is weak. The fixed-population large-sample result does not establish uniform accuracy as MI approaches zero.

#### 20. Why use a bias correction if it cancels in your simulations?

- The general estimator subtracts the leading MI bias, (r−1)(c−1)/(2n), from each population's plug-in estimate.
- In the balanced simulations, the dimensions and sample sizes match, so the two fixed corrections cancel exactly in the difference.
- That cancellation does not remove higher-order bias. Different population tables can still give different remaining biases, shifting the estimated difference.
- Unequal sample sizes give unequal leading corrections. The formula allows them, but the simulation study does not evaluate that case.

#### 21. How do you handle empty cells or a negative corrected MI estimate?

- Positive population probabilities do not guarantee positive sample counts. Empty sampled cells are retained, and their zero-weight contributions are omitted without evaluating a logarithm at zero.
- This avoids adding artificial counts, but it does not solve the statistical difficulty of estimating rare or unobserved cells.
- Population MI is non-negative, but subtracting a bias correction can produce a negative estimate. The procedure retains it rather than clipping it to zero.
- Clipping would change the estimator and its sampling behaviour, so it would need a separate derivation and evaluation.

#### 22. What happens when a test calculation fails? Could that explain your results?

- The procedure requires a finite estimated difference, a positive finite standard error, and finite p-values. Expanded Welch also requires positive finite component and combined degrees of freedom.
- A degenerate component can make the degrees-of-freedom formula undefined even when the other table gives a positive total standard error.
- Failed calculations count as non-rejections, and success rates are reported separately. A failure is not evidence that population MI is equal.
- Failures contribute to some small-sample power loss. They cannot explain the highlighted severe false positives or wrong-direction example, where every calculation succeeds.

#### 23. Would changing logarithm base or relabelling categories change the answer?

- Changing log base rescales MI and its standard error by the same factor, so their ratio is unchanged when the whole calculation uses that base consistently.
- V scales by the square of that factor, and tau-squared by its fourth power. Their scaling cancels in the component degrees of freedom.
- Consistently relabelling categories only reorders the probabilities. Merging categories or choosing a different discretisation changes the variables and can change MI and the test result.

### Experimental design

#### 24. Why use the copying construction?

- It gives explicit positive population tables with chosen category frequencies and a controllable amount of association, so the true MI is known.
- Adjusting the copying probability changes association without changing those margins. That helps separate MI effects from the selected frequency regimes.
- It is one association family, with matching row and column frequency vectors within each table. The results do not establish performance for every joint distribution.

#### 25. Why these table sizes, frequency regimes, and MI values?

- The grid varies dimensions from 2×2 to 16×16 and includes uniform frequencies, the same skew in both populations, and different skews. These expose different patterns of rare cells and bias cancellation.
- The null study uses shared MI values of 0.005, 0.02, and 0.30 nats. The power study starts P at 0.02 and gives Q gaps of 0.005, 0.01, and 0.02 nats.
- Together they test selected weak and stronger associations over a wide sample-size range. They are controlled comparisons rather than a representative sample of all possible applications.

#### 26. Why 100,000 repetitions? Does that mean each test has a huge sample?

- One repetition gives each test only the stated sample size from each population. Repeating the experiment estimates its rejection probability more precisely.
- With 100,000 repetitions and a true rejection probability near 5%, the Monte Carlo standard error is about 0.07 percentage points.
- The two methods receive the same sampled table pair in each repetition, which supports direct comparison on identical data. The population samples themselves remain independent.
- More repetitions reduce simulation uncertainty. They do not repair bias or a poor reference distribution within an individual test.

#### 27. Why use equal sample sizes when Welch's test is often associated with unequal samples?

- Equal sizes provide a controlled first evaluation of the MI-specific calculation while varying table size, frequencies, association, and available data.
- They also make the leading bias corrections cancel, which separates the reported failures from differences in those fixed corrections.
- The formula permits unequal sizes, but the simulations do not establish its performance there. Unequal-size evaluation is a substantive next step.

#### 28. Does the actual test use known populations or information from all 100,000 repetitions?

- No. Each actual test estimates the MI difference, standard error, sensitivities, and degrees of freedom from its two observed tables.
- Known population inputs are used to check the first-order formulas, and repeated samples provide empirical moment targets for assessment.
- Those benchmarks diagnose approximation errors. They are not inputs available to the test on a single dataset.

#### 29. Why not just use a permutation test or bootstrap?

- A simple group-label permutation is exact under exchangeability, as when the complete population distributions are equal. Equal MI alone does not give that condition.
- Separate-sample bootstrapping is a plausible alternative for uncertainty in the difference, but an ordinary empirical bootstrap cannot generate cells absent from the observed table.
- Residual estimation bias and sparse counts therefore remain relevant to resampling too. A suitable procedure would need to respect the equal-MI hypothesis and be evaluated.
- I did not conduct a full resampling comparison, so I cannot claim Expanded Welch outperforms those alternatives.

#### 30. Why use Wald as the main benchmark, and did you compare ordinary Welch?

- Wald uses the same MI-difference estimate and standard error. Comparing the methods isolates the change in reference distribution and its additional calculation requirements.
- Ordinary Welch component degrees of freedom were examined at three illustrative null settings. They changed rejection rates but did not remove residual-bias failures.
- Those examples provide context rather than a comprehensive ranking. The study does not establish superiority over all tests or MI estimators.

#### 31. How did you check that the derivation and its implementation agree?

- The numerical checks perturb positive tables and compare finite-difference derivatives of V with the analytic sensitivity g.
- Independent calculations of the sensitivity variance and component degrees of freedom are compared with the implementation. The checks also cover centring and near-independence limits.
- These checks support the algebra and code agreement. They do not prove that a first-order expansion or Student t reference distribution is accurate in finite samples; the simulation studies assess those claims.

#### 32. What do the shaded regions and uncertainty intervals in the figures mean?

- Rejection-rate intervals are pointwise Wilson 95% intervals for simulation uncertainty at a fixed population and sample size.
- The approximation plots use Monte Carlo uncertainty intervals where shown. These describe uncertainty in estimated moments or ratios across repetitions.
- The shading in the whole-grid power-loss plot instead spans the full range across 36 different settings at each sample size. It describes variation between settings, not a confidence interval.
- Narrow simulation intervals mean the estimated performance is precise. They do not mean the test itself has accurate false-positive rates or that all settings are covered simultaneously.

### Interpreting the results

#### 33. Does improving 165 settings prove Expanded Welch is better overall?

- The count is 165 out of the 178 settings where Wald's observed false-positive rate exceeds 5%. It is not 165 improvements out of an otherwise uniformly improved grid.
- Among 180 settings where Wald is already below 5%, Expanded Welch lowers rejection further or leaves it unchanged. Two settings have Wald exactly at 5%.
- Counting settings gives each grid point equal weight. It does not identify how frequently those populations arise in practice or define a universal trade-off with power.
- The displayed 4–6% band is descriptive. Changing that band changes the tally, so proximity counts should support the full pattern rather than establish a global winner.

#### 34. How can the variance prediction be good while the degrees of freedom are wrong?

- The moment target depends on both the squared mean of V-hat and its sampling variance. Predicting the spread well does not imply that the mean is close to V.
- In the Slide 7 example at n = 1,000, mean V-hat is about 1.19 times V, while the population variance prediction is about 0.97 times the observed variance.
- Using V in place of that larger mean gives a degrees-of-freedom ratio of about (1/1.19)²/0.97, or 0.73.
- The population first-order component value is therefore about 15.30 against the moment target 21.03. These are not the degrees of freedom from a single observed table.

#### 35. Can you explain the near-independence values 0.1, 4.9, and 9.1?

- About 0.1 is the population first-order component value. Near independence, V is approximately 2I and tau-squared approximately 4V, giving degrees of freedom approximately nI.
- About 4.9 is the mean component value estimated from sampled tables. Sampling noise creates apparent association, so this average does not approach zero in the fixed-n experiment.
- About 9.1 is the empirical moment-matching target, calculated from the repeated-sample mean and variance of V-hat. It is the benchmark, not another sample-based estimate.
- The local noncentral chi-squared distribution calculation predicts about 4.6 for the mean estimate and about 9.0 for the target in this setting. It explains their separation approximately, rather than producing an exact finite-sample test.

#### 36. Why not insert average estimated inputs into the degrees-of-freedom formula?

- Degrees of freedom involve squares and a ratio. Averaging the resulting values generally differs from applying that nonlinear formula to averaged inputs.
- The numerator and denominator estimates also come from the same table and can vary together.
- Keep the population first-order value, the mean sample-based estimate, and the moment target separate. They answer different questions and need not agree in finite samples.

#### 37. Do the diagnostic variance ratios fully explain the false-positive rates?

- They identify whether the average squared standard error understates or overstates the observed sampling variance. They do not describe the full statistic distribution.
- The uniform example has near-zero difference bias and a variance ratio about 0.83; the same-skew example has near-zero difference bias and a ratio about 1.93.
- The different-skew example combines an inflated variance estimate with a difference centred about two sampling standard deviations above zero. That shift helps explain why high rejection remains despite the large denominator.
- The severe 36.38% versus 34.38% example uses shared MI 0.005. The two-standard-deviation diagnostic uses MI 0.02. They illustrate related failures in different settings.

#### 38. Are wrong-direction rejections false positives? What does the 99.9% figure mean?

- In that power experiment, population MI really differs. Rejecting equality is therefore a rejection under an alternative, rather than a false positive under equal MI.
- The problem is the estimated sign. In the highlighted example, true MI in P minus MI in Q is −0.01, but its estimated difference has mean about +0.0207.
- Expanded Welch rejects in 9,662 of 100,000 repetitions. Of those rejections, 9,659 point the wrong way: more than 99.9% conditional on rejection.
- That percentage does not describe all estimates or all grid settings. The conventional two-sided power definition counts these rejections without checking their estimated direction.

#### 39. Why can power fall when the true MI gap increases?

- With different residual biases, the average estimated difference can initially have the opposite sign to the population difference.
- Increasing the true gap can move that average towards zero by opposing the bias. The statistic then crosses a two-sided cutoff less often even though the true gap grows.
- Once the true difference dominates the bias, rejection can rise again. The estimate and standard error both matter, so power is not determined by the MI gap alone.
- This is an observed finite-sample pattern in the tested family, not a claim that more separation generally makes a well-calibrated test less powerful.

#### 40. Is the power comparison fair if the actual false-positive rates differ?

- It compares both procedures as used at the same nominal 5% significance level, which directly answers how their usual rejection rules differ.
- It does not compare power after forcing their actual false-positive rates to match. Higher Wald power can accompany excessive null rejection.
- For the implemented rules, Expanded Welch rejections are nested within Wald rejections, so its power cannot exceed Wald's. That ordering need not apply after separately recalibrating thresholds.
- Matching one selected null setting would still not establish equal false-positive control over every pair of populations with equal MI.

### Practical implications and further work

#### 41. How much data is enough? Can I just use Expanded Welch above a certain n?

- The study does not establish a universal sample-size threshold. Performance depends on the table dimensions, rare-cell probabilities, MI, and the size of the MI difference.
- At n = 10,000, the methods' power differs by less than 0.32 percentage points across the tested grid. That only establishes their closeness there, rather than high power or calibration in every application.
- Even at n = 50,000, power for the smallest gap ranges from about 80% to 96%. Sample-size planning should use plausible populations and the effect size of interest.

#### 42. What did the real-data example show, and does it validate the test?

- In the thesis's online-shopping example, both tests reject equal month–purchase MI, with higher corrected MI among returning visitors.
- Neither rejects equal weekend–purchase MI. That non-rejection does not establish that the population MI values are identical.
- The example illustrates calculation and interpretation with observed data. Because the population truth is unknown, it cannot establish false-positive accuracy; the controlled simulations address that question.

#### 43. Could the method handle unequal samples, paired observations, or continuous variables?

- Unequal sample sizes enter the existing formulas directly, but need empirical evaluation, including the unequal leading bias corrections.
- Paired or dependent samples require covariance terms. The independent-sample variance sum and its moment matching cannot simply be reused unchanged.
- Continuous variables require an estimator and uncertainty argument appropriate to that setting. Discretising them changes the variables and makes the category choices relevant.
- Allowing the number of categories to grow with sample size also requires extending the fixed-dimension argument.

#### 44. What would you improve first, and what is your overall recommendation?

- I would first investigate the MI-difference and standard-error estimates, because changing the cutoff cannot remove their bias or rescale an inaccurate uncertainty estimate.
- I would change one estimator at a time and assess false positives, power, calculation success, and the estimated direction, so improvements can be attributed to a specific change.
- Near independence, I would investigate a treatment retaining quadratic sampling variation, then evaluate it over broader association patterns and unequal sample sizes.
- The current evidence supports a conditional conclusion: Expanded Welch improves some excessive false-positive rates, but it is not a universally reliable replacement for Wald.
