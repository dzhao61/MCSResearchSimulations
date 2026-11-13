# Comparing Mutual Information in Finite Samples: speaker notes

Daniel Zhao. Talk target 18:50 for Slides 1–13; Slide 13 stays up for questions. Slide 14 is the appendix title and the backups are Slides 15–33.
Scripts, transitions, delivery cues, sources, and backup answers are copied from the presentation execution plan, as updated on 13 November 2026.

## Main talk

### Slide 1: Comparing Mutual Information in Finite Samples

Time: 0:25 (finish by 0:25)

**Script**

> This project asks whether mutual information differs between populations when we have finite samples. I derive MI-specific degrees of freedom for a Welch–Satterthwaite comparison, then examine when its larger rejection cutoff improves false-positive accuracy and what happens to power.

**Transition**

“The comparison starts with two populations and a sample from each.”

**Delivery cue**

Face the audience. Use the question rather than reading the affiliation.

**Source**

Final title, abstract, and Chapter 1; preferred-reference page 1.

### Slide 2: Motivation: comparing MI across populations

Time: 1:15 (finish by 1:40)

**Script**

> Mutual information measures the average reduction in uncertainty about one variable when we observe another. I study two discrete variables, X and Y, recorded for each individual in two populations. P and Q are the joint probability tables of X and Y in those populations.

> For example, X could be a student's mid-semester test grade and Y their final exam grade. P is the students before generative AI and Q is the students after. The question is whether the mid-semester grade tells us as much about the final grade in both groups.

> We observe a sample from each population, summarise it in a count table, and estimate MI from each table. Different samples can produce different estimates even when population MI is equal. The null hypothesis therefore equates the two population MI values, against the two-sided alternative that they differ. It allows different probability tables. We need to account for sampling uncertainty before interpreting an observed difference.

**Transition**

“The literature supplies several parts of that comparison, with one additional MI-specific calculation needed.”

**Delivery cue**

Say “discrete” clearly. Give the example in one breath, then trace each population into its estimate and point to the null.

**Source**

Thesis Sections 1.1 and 2.1; Bossomaier et al. (2016).

### Slide 3: Literature review: foundations and the MI-specific step

Time: 1:00 (finish by 2:40)

**Script**

> The project builds on three established strands. Work on MI supplies the estimator, its leading bias correction, and its first-order sampling variance. The Wald test uses those estimates with the standard normal distribution as its reference. Welch and Satterthwaite instead use variance moments to choose degrees of freedom, with related applications in entropy and other statistical comparisons.

> For this MI comparison, the additional calculation is how much the pointwise-MI variance estimate changes when the sampled table changes. Its probability weights, row and column margins, and pointwise-MI values all change together. I derive that sensitivity, construct the Expanded Welch test from it, and evaluate both.

**Transition**

“The two tests then share a statistic but use different reference distributions.”

**Delivery cue**

Move across the columns once. Emphasise the required calculation rather than reciting authors.

**Source**

Thesis Sections 2.2–2.5 and 3.2–3.3; bibliography keys moddemeijer1989, paninski2003, mora2009, satterthwaite1946, welch1947, hutcheson1970, and panwall2002.

### Slide 4: Method: one statistic, two reference distributions

Time: 1:20 (finish by 4:00)

**Script**

> Both tests divide the estimated MI difference, after a leading bias correction, by the same estimated standard error. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Independence between the samples lets their two variance contributions add.

> The standard error itself fluctuates between samples. We use a Student t reference distribution so that the rejection cutoff can reflect uncertainty in that variance estimate. Its degrees of freedom are estimated from the tables.

> The Wald test uses the standard normal distribution, with a two-sided five-percent cutoff of about 1.96. The illustration uses a Student t distribution with five degrees of freedom, giving a larger cutoff of about 2.57. Actual estimated values vary. Under the same testing rules, Expanded Welch can only reject where Wald also rejects. The experiments assess whether this reduction improves false-positive rates and how much power it costs.

**Transition**

“Choosing the degrees of freedom requires the variability of the variance estimate itself.”

**Delivery cue**

Point to the shared standard error, explain why its sampling variation matters, then compare cutoffs. The illustrated five degrees of freedom is not typical of every dataset.

**Source**

Thesis Chapters 3–4 and Figure 2.1; quantiles of the standard normal distribution and the Student t distribution with 5 degrees of freedom.

### Slide 5: Approach and contributions

Time: 2:05 (finish by 6:05)

**Script**

> There are two levels of variation. V-hat describes variation in pointwise MI, but V-hat itself changes when a new sample produces a different table. I calculate how V changes when a small amount of probability moves towards one cell. The cell weights, margins, and log ratios all change together, and the sensitivity g describes their combined effect.

> Different possible outcomes have different sensitivities. Tau-squared is the variance of those sensitivities. Averaging the observation-level contributions gives a first-order approximation to the error in V-hat. With independent observations, the sampling variance of that average is tau-squared divided by sample size.

> Satterthwaite moment matching uses the mean and sampling variance of V-hat to choose component degrees of freedom. Greater variability relative to the squared mean gives fewer degrees of freedom and a larger cutoff. I estimate the inputs from each table, repeat the calculation for Q, and combine the components using the Welch–Satterthwaite rule.

> The derivative is exact for positive population tables. Its use to approximate sampling errors, and the resulting Student t reference distribution, are approximations. The first research question checks the sampling approximations and the degrees of freedom they imply.

**Transition**

“Known population tables let me check those approximations before assessing test decisions.”

**Delivery cue**

Pause between the two levels of variation. Define g and tau-squared before the formula, then explain what greater relative uncertainty does to the cutoff. The displayed df are component df, not the combined test df.

**Source**

Thesis Sections 4.1–4.3; eq:g-final, eq:vhat-sampling-variance, eq:nu-p-hat, and eq:expanded-df. The source line points to Slides 16–18 for the derivations of these equations, and to Slides 19–21 for g and tau-squared in full, with a worked example.

### Slide 6: Evaluation design

Time: 1:20 (finish by 7:25)

**Script**

> I construct population tables with known MI by drawing X, then either copying its category into Y or drawing Y independently from the same category frequencies. Changing how often I copy controls association while preserving those frequencies. A numerical search chooses the copying probability for the target MI.

> RQ1 checks the variance approximations and degrees of freedom. The false-positive study uses equal MI, while the power study fixes MI in P at 0.02 nats and gives Q greater MI. Nats are units based on natural logarithms.

> Each test study has 360 settings, varying table size, category frequencies, sample size, and the shared MI or MI gap. Each setting uses 100,000 independent sampled table pairs. Both methods receive the same pairs, but each test sees only the observations in its two tables. Repetition measures performance without increasing that sample size. Both methods use the usual five-percent threshold. Unsuccessful calculations count as non-rejections, with calculation success reported separately.

**Transition**

“The first result shows why accurate variance prediction can coexist with an inflated mean.”

**Delivery cue**

Explain copying in words. Name the factors without reciting the grid multiplication. Keep sample size distinct from repetition count, and retain the unsuccessful-calculation rule.

**Source**

Thesis Chapter 5, Tables 5.1–5.3, and Appendix B; Morris et al. (2019). Current balanced-null and MI-gap grids.

### Slide 7: RQ1 results: approximation accuracy

Time: 1:40 (finish by 9:05)

**Script**

> This is one population and a four-by-four table, so the two moment errors can be read together. On top, one would mean the average V-hat equals the population variance. The mean rises above that benchmark and then recovers. When rare cells first appear, their estimated pointwise MI can lie far from the table's MI. The squared deviations can inflate V-hat until repeated counts stabilise the estimates.

> The lower graph concerns the sampling variance of V-hat itself. The navy curve uses known population inputs; the orange curve estimates those inputs from each sample. The population prediction misses variation when rare cells appear in some samples and remain absent in others. Estimating the sensitivities from sparse counts can instead overshoot. Larger samples improve both predictions.

> At one thousand observations, the population prediction is about three percent low, while the sample-based prediction is about eight percent high. The mean is still nineteen percent high. Since the degrees-of-freedom calculation squares the mean input and divides by the variance input, a good variance prediction alone does not make that calculation accurate.

**Transition**

“Near independence, an additional separation appears because sampling noise creates apparent association.”

**Delivery cue**

Pause when the graphs appear. Explain the top graph before the bottom. Say “sampling variance of V-hat”. Tie both annotations to n=1,000.

**Source**

Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2; null-display IDs, side=p, k=4, profile=different_skew, MI=.02. Slide 18's notes retain the numerical df consequence of this same example.

### Slide 8: RQ1 results: near independence

Time: 2:00 (finish by 11:05)

**Script**

> Here sample size stays at one thousand while population MI approaches zero. Start with the charcoal line: this is the moment-matching target, calculated from the mean and variance of V-hat across 100,000 sampled tables. It is our benchmark for the component degrees of freedom.

> The dotted navy line instead uses population inputs in the first-order formula. The orange line averages the component degrees of freedom estimated from each sampled table. At the weakest association, the target is about nine, the population-based value is about 0.1, and the mean sample-based estimate is about five, or half the target.

> Random count fluctuations can make sampled tables look associated even when the variables are independent in the population. At independence, the linear sampling contribution vanishes, but variation from squared probability errors remains. These are the quadratic terms omitted by the first-order calculation. The sample-based calculation retains apparent association, keeping its mean positive. A calculation that includes this sampling noise predicts about 4.6, close to the observed 4.9.

**Transition**

“The decision-level question is whether the larger cutoff brings false positives towards five percent.”

**Delivery cue**

Pause when the graph appears. Introduce the charcoal target first, then dotted navy population-based values and orange mean sample-based estimates. Point to the weakest-association end. Preserve this slide in every shorter route. Matching the target does not prove an exact Student t distribution.

**Source**

Thesis Section 6.1.3, Figure 6.3, and Appendix A.2; observed mean 4.859787, target 9.124808, and first-order value .096400.

### Slide 9: RQ2 results: false positives across all null settings

Time: 1:30 (finish by 12:35)

**Script**

> This chart shows all 360 null settings, so every rejection is a false positive. Each point is one setting: Wald's false-positive rate is on the horizontal axis and Expanded Welch's is on the vertical. The diagonal means no change, and the dashed lines mark five percent.

> Every point lies on or below the diagonal because the larger cutoff can only reduce rejection. On the right, Wald's observed rate exceeds five percent. Expanded Welch moves closer to the target in 165 of those 178 settings. On the left, Wald already rejects too rarely. None of those 180 settings improves: the rate falls further or remains unchanged.

> The circled examples show both improvement and remaining failure. In the upper-right example, even the reduced rate is above 34 percent. Lowering rejection therefore does not by itself make the test accurate.

**Transition**

“These diagnostic examples help explain the different rejection patterns.”

**Delivery cue**

Pause when the graph appears. Explain axes, diagonal, and target before the counts. Take the right half, then the left. Leave the descriptive 4–6% tally for the audience to read; retain the overall pattern and the severe remaining failure.

**Source**

Thesis Sections 6.2.1–6.2.3 and Figures 6.4–6.6; tallies of the balanced null rates (360 settings, both methods, all repetitions). Examples: uniform 4×4, n = 20, MI 0.02 (Wald 8.35%, Expanded Welch 4.90%); different-skew 16×16, n = 1,000, MI 0.005 (36.38% and 34.38%).

### Slide 10: RQ2 results: why the cutoff helps, hurts, or cannot fix it

Time: 1:45 (finish by 14:20)

**Script**

> These three examples help explain the different rejection patterns. All have equal population MI, so every rejection is a false positive, and every calculation succeeds. Bias over SD measures the shift of the estimated difference from zero. The variance ratio compares the average squared standard error with the observed sampling variance of that difference.

> In the uniform four-by-four example, the two MI estimates have the same expected bias, so it cancels in their difference. The variance ratio is about 0.83, indicating underestimated sampling variation. A small denominator inflates the statistic, and the larger cutoff brings rejection closer to five percent.

> In the same-skew example, the biases again cancel. But the variance ratio is about 1.93, indicating overestimated sampling variation. Wald already rejects less than one percent of the time, and the larger cutoff lowers that further.

> The different-skew example has a similarly inflated variance estimate, but the residual biases in the two MI estimates do not cancel. Their difference is centred about two sampling standard deviations above zero, and both tests reject about a quarter of the time. The larger cutoff changes the boundary without removing this bias.

**Transition**

“The same larger cutoff also changes the probability of detecting a real MI difference.”

**Delivery cue**

Follow the rows from cancellation of difference bias to the variance ratio and rejection pattern. Do not imply the individual MI estimates are unbiased or that all three settings are otherwise matched.

**Source**

Thesis Section 6.2.4 and Table 6.1; current null rates and diagnostics. Bias/SD .002744/−.002719/2.057921; variance ratios .826509/1.928694/1.938104.

### Slide 11: RQ3 results: the power cost of the larger cutoff

Time: 1:30 (finish by 15:50)

**Script**

> Power is the probability of rejecting equal MI when the population MI values differ. This chart summarises all 360 power settings under the same nominal five-percent threshold. It shows Wald power minus Expanded Welch power, in percentage points. The line is the median across 36 settings at each sample size. The shading is their full range, not Monte Carlo uncertainty like the earlier bands.

> Expanded Welch cannot have more power because its rejections are a subset of Wald's. The loss is largest at ten observations, with a median of about six percentage points; unsuccessful calculations also contribute there. By ten thousand observations, the loss is below 0.32 percentage points in every setting.

> A small difference between methods does not necessarily mean high power. Even with fifty thousand observations, power for the smallest MI gap ranges from about 80 to 96 percent, while the two larger gaps exceed 99.9 percent. These rates count rejections in either direction, which matters for the next slide.

**Transition**

“Different residual biases can make that directional error dominate the apparent detections.”

**Delivery cue**

Pause when the graph appears. Define power lost, median, and range. Emphasise the small-sample loss and the under-0.32-point bound at n = 10,000, retaining the distinction between method differences and absolute power. This is not matched-size power.

**Source**

Thesis Sections 6.3.1–6.3.3, Figures 6.7–6.9, and Section 7.1.3; tallies of the MI-gap power rates (360 settings, both methods, all repetitions). Median loss 5.78 points at n = 10 (maximum 13.42); maximum 0.313 points at n = 10,000.

### Slide 12: RQ3 results: bias can reverse the estimated direction

Time: 2:00 (finish by 17:50)

**Script**

> This heat map covers all table sizes and sample sizes under different-skew margins, for the 0.01-nat gap. Q always has greater population MI. Each cell shows, among Expanded Welch rejections, the percentage whose estimated difference incorrectly points to P as having greater MI. The displayed percentages are rounded.

> The darker cells show that almost every rejection points the wrong way over parts of the sparse, larger-table range. Focus on the outlined sixteen-by-sixteen cell at one thousand observations per population. The true difference is minus 0.01 nats, but the mean estimated difference is about plus 0.0207. Expanded Welch rejects about one time in ten, and more than 99.9 percent of those rejections have the wrong estimated sign.

> Unequal residual biases have outweighed the true gap. A larger cutoff cannot remove that bias; it changes how often we reject. In these simulations, increasing sample size reduced the bias. Across the full power grid at ten thousand observations, fewer than 0.4 percent of rejections point the wrong way.

> Across all 360 power settings, at least 90 percent of rejections point the wrong way in 28 settings, all with different-skew margins. These count as detections under the two-sided definition of power, but do not reliably identify which population has greater MI.

**Transition**

“The contribution and the remaining estimation problems lead to specific next steps.”

**Delivery cue**

Pause when the heat map appears. Define the percentage as conditional on rejection. Explain the outlined cell through its signed differences before the wrong-direction percentage. Preserve this slide in every shorter route; every calculation succeeds at the outlined cell.

**Source**

Thesis Section 6.3.3 and Figure 6.9; signed rejection counts in the MI-gap power diagnostics (360 settings). Outlined cell: 9,659 of 9,662 Expanded Welch rejections positive; bias about 0.0307 nats.

### Slide 13: Conclusions and next steps

Time: 1:00 (finish by 18:50)

**Script**

> This work makes three contributions. It derives how the pointwise-MI variance estimate varies between samples, builds the Expanded Welch test from that result, and evaluates both in controlled simulations.

> For RQ1, the approximations improve as samples grow, but miss sampling noise near independence. For RQ2, the larger cutoff helps only where Wald rejects too often. For RQ3, power is no higher at the same nominal threshold, and bias can make rejections point the wrong way.

> The evaluation covers one population construction and equal sample sizes. Next, I would improve the MI-difference and standard-error estimates and test broader populations.

> The main finding is that adjusting the cutoff helps in some settings, while the remaining failures show why accurate MI differences and standard errors are also essential. Thank you.

**Delivery cue**

Name the three contributions, then give one finding per research question. Keep the scope brief. Finish with the overall scientific finding, then face the audience and leave this slide visible for questions.

**Source**

Final abstract; thesis Sections 1.3 (three contributions) and 7.1–7.3 (findings by research question). No claim of universal superiority or validated independence-specific replacement test.

**Backup index (type the slide number, press Enter, then return to 13)**

- 14  Appendix title and index
- **Method (supports Slides 4–5)**
- 15  Bias correction
- 16  Derivation 1 of 3: how much the variance estimate varies
- 17  Derivation 2 of 3: moment matching gives the df rule
- 18  Derivation 3 of 3: estimated and combined degrees of freedom
- 19  Variance sensitivity in full
- 20  Variance sensitivity in cell probabilities
- 21  Worked example: sensitivities and degrees of freedom
- **Evaluation design (supports Slide 6)**
- 22  Population construction, grid, and calculation requirements
- **RQ1: approximation accuracy (supports Slides 7–8)**
- 23  Approximation ratios across table sizes
- 24  Near-independence noise calculation
- **RQ2: full null results (supports Slides 9–10)**
- 25  Full null results: uniform margins
- 26  Full null results: same-skew margins
- 27  Full null results: different-skew margins
- 28  Ordinary Welch degrees of freedom
- **RQ3: full power results (supports Slides 11–12)**
- 29  Full power results: uniform margins
- 30  Full power results: same-skew margins
- 31  Full power results: different-skew margins
- **References**
- 32  References: MI and testing foundations
- 33  References: related methods and evaluation

## Appendix

### Slide 14: Appendix title

Appendix title. Not part of the timed talk.

**Delivery**

No timed speech. Keep the conclusion on Slide 13 visible when questions begin, then open the relevant backup when needed and return to Slide 13 afterwards. The divider adds no time to the 18:50 main talk.

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
