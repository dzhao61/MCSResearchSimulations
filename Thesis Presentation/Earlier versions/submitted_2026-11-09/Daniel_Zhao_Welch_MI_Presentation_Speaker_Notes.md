# Comparing Mutual Information in Finite Samples: speaker notes

Daniel Zhao. Talk target 18:50 for Slides 1–14; Slide 14 stays up for questions. Slide 15 is the appendix title and the backups are Slides 16–30.
Scripts, transitions, delivery cues, sources, and backup answers are copied from the presentation execution plan, as updated on 8 November 2026.

## Main talk

### Slide 1: Comparing Mutual Information in Finite Samples

Time: 0:25 (finish by 0:25)

**Script**

> This project asks whether mutual information differs between populations when we have finite samples. I derive MI-specific degrees of freedom for a Welch–Satterthwaite comparison, then examine when its larger rejection cutoff improves false-positive accuracy and what happens to power.

**Transition**

“The shopping example gives a concrete reason to make this comparison.”

**Delivery cue**

Face the audience. Use the question rather than reading the affiliation.

**Source**

Final title, abstract, and Chapter 1; preferred-reference page 1.

### Slide 2: Motivation: comparing MI across populations

Time: 1:15 (finish by 1:40)

**Script**

> Mutual information measures the average reduction in uncertainty about one variable when we observe another. Here the variables are the month of a website visit and whether the session ends in a purchase. I compare that association between new and returning visitors, whose population tables I call P and Q.

> The corrected sample estimates are about 0.0043 and 0.0179 nats. Their difference motivates the question, but different samples can produce different estimates even when population MI is equal. The null hypothesis therefore equates the two population MI values. It allows different probability tables. We need to account for sampling uncertainty before interpreting the observed difference. I will return to the application after checking the comparison in known populations.

**Transition**

“The literature supplies several parts of that comparison, with one additional MI-specific calculation needed.”

**Delivery cue**

Trace groups into estimates, then point to the null. Do not announce the application p-values yet.

**Source**

Thesis Sections 1.1, 2.1, and 6.4; application row shoppers_month; Bossomaier et al. (2016).

### Slide 3: Literature review: foundations and the MI-specific step

Time: 1:00 (finish by 2:40)

**Script**

> The project builds on three established strands. Work on MI supplies the estimator, its leading bias correction, and its first-order sampling variance. The Wald test uses those estimates with the standard normal distribution as its reference. Welch and Satterthwaite instead use variance moments to choose degrees of freedom, with related applications in entropy and other statistical comparisons.

> For this MI comparison, the additional calculation is how much the pointwise-MI variance estimate changes when the sampled table changes. Its probability weights, row and column margins, and pointwise-MI values all change together. I derive that sensitivity and evaluate the resulting approximation.

**Transition**

“The two tests then share a statistic but use different reference distributions.”

**Delivery cue**

Move across the columns once. Emphasise the required calculation rather than reciting authors.

**Source**

Thesis Sections 2.2–2.5 and 3.2–3.3; bibliography keys moddemeijer1989, paninski2003, mora2009, satterthwaite1946, welch1947, hutcheson1970, and panwall2002.

### Slide 4: Method: one statistic, two reference distributions

Time: 1:20 (finish by 4:00)

**Script**

> Both tests divide the corrected MI difference by the same estimated standard error. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Independence between the samples lets their two variance contributions add.

> The Wald test compares the statistic with the standard normal distribution. The Expanded Welch test uses a Student t distribution with degrees of freedom estimated from the tables. The illustration uses five degrees of freedom: its heavier tails move the two-sided cutoff from about 1.96 to 2.57. Actual estimated values vary. The larger cutoff means Expanded Welch's rejections are a subset of Wald's under the implemented rules. The experiments assess whether that reduction helps accuracy and how much detection it costs.

**Transition**

“Choosing the degrees of freedom requires the variability of the variance estimate itself.”

**Delivery cue**

Point to the common denominator, then cutoffs. Do not imply the illustrated difference is typical of every dataset.

**Source**

Thesis Chapters 3–4 and Figure 2.1; quantiles of the standard normal distribution and the Student t distribution with 5 degrees of freedom.

### Slide 5: Approach and contribution

Time: 1:40 (finish by 5:40)

**Script**

> There are two levels of variation. V-hat describes variation in pointwise MI, but V-hat itself changes when a new sample produces a different table. I calculate how V changes when a small amount of probability moves towards one cell. That perturbation changes the cell weights, margins, and log ratios together. The sensitivity g collects those effects.

> Averaging observation-level sensitivities gives a first-order approximation to the sampling error of V-hat. Its sampling variance is therefore approximately tau-squared divided by sample size. Satterthwaite moment matching uses twice the squared mean of a variance estimate divided by its sampling variance. Substituting the sample-based inputs gives the component formula shown here. Greater variation relative to the squared mean gives fewer degrees of freedom. I repeat the calculation for Q and combine the components.

> The derivative is an exact calculation for positive population tables. Its sampling expansion and the moment-matched Student t distribution are approximations, which motivates the first evaluation question.

**Transition**

“Known population tables let me check those approximations before assessing test decisions.”

**Delivery cue**

Pause between V-hat and its sampling variance. Explain the chain before the formula. The displayed df are component df, not the combined test df.

**Source**

Thesis Sections 4.1–4.3; eq:g-final, eq:vhat-sampling-variance, eq:nu-p-hat, and eq:expanded-df. B1–B2 retain the full derivative and moment-matching argument.

### Slide 6: Evaluation design

Time: 1:20 (finish by 7:00)

**Script**

> I construct population tables with known MI using a copying model that preserves chosen margins. RQ1 checks the variance approximations and the resulting degrees of freedom. The null study uses three shared MI values, while power fixes MI in P at 0.02 nats and makes Q larger by three gaps. Nats are MI units based on natural logarithms.

> Both test studies cross four table sizes, ten sample sizes, and three margin regimes, giving 120 combinations for each MI level or gap. With three levels or gaps, each study has 360 settings. The uneven margins either agree between populations or differ. Every test sees only its two sampled tables. Repeating the comparison 100,000 times measures performance without increasing the observations available to one test. Both methods use the same pairs and usual p-value thresholds. Unsuccessful calculations count as non-rejections, with calculation success tracked separately.

**Transition**

“The first result shows why accurate variance prediction can coexist with an inflated mean.”

**Delivery cue**

Name what varies and stays fixed. Do not recite ten sample sizes or restore fitted-threshold experiments.

**Source**

Thesis Chapter 5, Tables 5.1–5.3, and Appendix B; Morris et al. (2019). Current balanced-null and MI-gap grids.

### Slide 7: Results: approximation accuracy

Time: 1:40 (finish by 8:40)

**Script**

> This is one population and a four-by-four table, so the two moment errors can be read together. On top, one would mean the average V-hat equals the population variance. The mean rises above that benchmark and then recovers. When rare cells first appear, their estimated pointwise MI can lie far from the table's MI. The squared deviations can inflate V-hat until repeated counts stabilise the estimates.

> The lower graph concerns the sampling variance of V-hat itself. The navy curve uses known population inputs; the orange curve estimates those inputs from each sample. The population prediction misses variation when rare cells appear in some samples and remain absent in others. Estimating the sensitivities from sparse counts can instead overshoot. Larger samples improve both predictions.

> At one thousand observations, the population prediction is about three percent low, while the sample-based prediction is about eight percent high. The mean is still nineteen percent high. Since the degrees-of-freedom calculation squares the mean input and divides by the variance input, a good variance prediction alone does not make that calculation accurate.

**Transition**

“Near independence, an additional separation appears because sampling noise creates apparent association.”

**Delivery cue**

Explain the top graph before the bottom. Say “sampling variance of V-hat”. Tie both annotations to n=1,000.

**Source**

Thesis Sections 6.1.1–6.1.2, Figures 6.1–6.2; null-display IDs, side=p, k=4, profile=different_skew, MI=.02. B2 retains the numerical df consequence of this same example.

### Slide 8: Results: near independence

Time: 1:40 (finish by 10:20)

**Script**

> Here sample size stays at one thousand while population MI approaches zero. The grey line inserts known population inputs into the first-order component formula and becomes very small. The orange curve, the mean component degrees of freedom estimated from sampled tables, stays near five at the weakest association. The navy moment target is the component degrees of freedom calculated from the repeated-sample mean and variance of V-hat. It is near nine, so the mean estimate is still only about half that target.

> At independence, population pointwise MI is zero and the linear sampling contribution vanishes. Sampled tables nevertheless contain apparent association from quadratic sampling errors. The sample-based calculation retains that noise, which explains why its mean stays positive instead of following the population value towards zero. The local calculation in the thesis predicts a mean near 4.6 here, against the observed 4.9. This explains the separation while also showing the limits of the first-order approximation.

**Transition**

“The decision-level question is whether the larger cutoff brings false positives towards five percent.”

**Delivery cue**

Point to the low-MI end and explain each curve once. Preserve this slide in every shorter route. The calculation does not prove an exact Student t distribution.

**Source**

Thesis Section 6.1.3, Figure 6.3, and Appendix A.2; observed mean 4.859787, target 9.124808, and first-order value .096400.

### Slide 9: Results: false positives across shared MI values

Time: 1:30 (finish by 11:50)

**Script**

> Each group here uses equal MI in P and Q, so every rejection is a false positive. Table size, margins, and sample size stay fixed; only the shared MI changes. The dashed line is the five-percent target, navy is Wald, and orange is Expanded Welch.

> At shared MI 0.02, the larger cutoff brings rejection from 8.35 percent to 4.90 percent. At shared MI 0.30, rejection still exceeds thirteen percent. Both tests' calculations succeed in every repetition in all three groups, so those departures reflect inference rather than calculation failures.

> The cutoff adjustment can offset some errors at a particular population pair, but it does not make the reference accurate across association strengths. Other margin settings also have rates below five percent, where lowering rejection increases conservatism.

**Transition**

“A matched diagnostic comparison shows why similar uncertainty errors can give opposite rejection behaviour.”

**Delivery cue**

Shared MI changes both populations together; their difference remains zero. Read the highlighted comparisons, not all six labels. No old aggregate counts or A/B/C labels.

**Source**

Thesis Section 6.2.1, Figure 6.4, and current null rates, k=4, uniform, n_p=n_q=20, denominator=all; six method rows.

### Slide 10: Results: why bias changes rejection

Time: 1:45 (finish by 13:35)

**Script**

> These two examples have the same dimensions, sample size, and population MI. Their average squared standard errors are almost equally inflated: the variance ratios are about 1.93 and 1.94. Yet their false-positive rates are very different.

> With the same margins, the population tables are identical and expected biases cancel in the MI difference. The oversized denominator suppresses the statistic, accompanying rejection below one percent. Expanded Welch lowers that already-conservative rate further.

> With different margins, residual biases no longer cancel. The sampling mean of the estimated difference is more than two sampling standard deviations above zero. Both tests then reject around a quarter of repetitions despite the inflated uncertainty estimate. Every calculation succeeds in these examples. The larger cutoff changes the decision boundary while leaving the shifted estimate in place, which helps explain why both methods can remain inaccurate.

**Transition**

“The same larger cutoff also changes the probability of detecting a real MI difference.”

**Delivery cue**

Compare variance ratios, then bias, then rejection. Name the MI difference as the biased object.

**Source**

Thesis Section 6.2.4 and Table 6.1; current null rates and diagnostics. Variance ratios 1.928694/1.938104; bias/SD −.002719/2.057921.

### Slide 11: Results: power across MI differences

Time: 1:30 (finish by 15:05)

**Script**

> Power is the probability of rejecting equal MI when the population MI values differ. Here P stays at 0.02 nats and Q has greater MI. The graph fixes the gap at 0.01 and increases sample size. As estimates become more accurate and less variable, detection rises. Expanded Welch stays at or below Wald, with the curves becoming close at larger samples.

> The table holds sample size at two thousand five hundred and compares all three gaps. Expanded Welch power increases from about eleven percent for the smallest gap to about seventy-nine percent for the largest. That is a local comparison; the full grid also varies dimensions and margins.

> These rates use the usual testing thresholds and are interpreted alongside the false-positive results. A two-sided rejection also needs care because it can point towards the wrong population.

**Transition**

“Different residual biases can make that directional error dominate the apparent detections.”

**Delivery cue**

Connect the .01 table row to the plotted point. Do not call nominal power matched-size power or restore threshold fitting.

**Source**

Thesis Section 6.3.1, Figure 6.7; current power rates, all repetitions, k=4, uniform; plot gap=.01 (20 rows), snapshot n_p=2500 (6 rows).

### Slide 12: Results: bias can reverse the estimated direction

Time: 1:40 (finish by 16:45)

**Script**

> The true difference here is minus 0.01 nats, so Q has greater population MI. At one thousand observations per population, however, the mean estimated difference is about plus 0.0207. Unequal residual biases have outweighed the true gap and shifted the sampling centre to the other side of zero.

> Expanded Welch rejects in about 9.66 percent of repetitions at that point. Among those rejections, more than 99.9 percent have a positive estimated difference, opposite to the population direction. They count as power under a two-sided definition, but they fail to identify which population has greater MI.

> As sample size increases, the positive bias diminishes and the centre moves towards zero. Rejection can initially fall before recovering in the correct direction. Changing the cutoff leaves that biased movement unchanged. The shape therefore requires an explanation of the estimator as well as the rejection threshold.

**Transition**

“The observed-data application illustrates how to interpret outputs when the population values are unknown.”

**Delivery cue**

Explain the signed numbers first, then “among the rejections”. Preserve this slide in the shorter route. Both methods' calculations succeed in every repetition at the highlighted point.

**Source**

Thesis Section 6.3.3, Figure 6.9; current power rates/diagnostics, k=16, different_skew, gap=.01. EW positive rejections 9,659, negative 3, total 9,662.

### Slide 13: Illustration: online shopping data

Time: 1:05 (finish by 17:50)

**Script**

> Returning to the opening question, the corrected month–purchase MI estimate is higher for returning visitors. Both methods reject equal MI at the usual 0.05 threshold. Expanded Welch's p-value is about 0.0004. The weekend comparison has very close estimates and neither test rejects equality.

> These are associations, without a causal interpretation of month. The unknown population tables also mean the application cannot tell us which test has accurate false-positive rates. It illustrates how to read the estimates and test outputs, while the known-population simulations establish the strengths and limitations of the comparison.

**Transition**

“The contribution and the remaining estimation problems lead to specific next steps.”

**Delivery cue**

Close the loop with Slide 2. Non-rejection does not establish equality. Do not read every number.

**Source**

Thesis Section 6.4, Tables 6.3–6.4, and application CSV; Sakar and Kastro (2018). Month: Wald p = 4.71 × 10^-5; Expanded Welch p = 3.73 × 10^-4 with 26.79 degrees of freedom (unadjusted, two-sided).

### Slide 14: Conclusions and next steps

Time: 1:00 (finish by 18:50)

**Script**

> I derived the MI-specific variance sensitivity and used it to calculate degrees of freedom for a Welch–Satterthwaite comparison. Its larger cutoff brings some excessive false-positive rates closer to five percent, but also increases conservatism and reduces power under the usual rules.

> The sparse-table examples show why the estimates remain central: a cutoff adjustment leaves bias and errors in the standard error unchanged, and bias can reverse the estimated direction. The evaluation covers one population construction and equal sample sizes, with the Wald test as the main benchmark. The next steps are to improve those estimates, retain additional sampling variation near independence, and evaluate broader population constructions and unequal sample sizes. The project contributes both the calculation and evidence identifying where it needs further development. Thank you.

**Delivery cue**

Give contribution and boundary equal emphasis. Face the audience and keep this page visible for questions.

**Source**

Final abstract; thesis Sections 1.3 and 7.1–7.3. No claim of universal superiority or validated independence-specific replacement test.

**Backup index (type the slide number, press Enter, then return to 14)**

- 15  Appendix title
- 16  B1  Variance sensitivity
- 17  B2  Moment matching and combined degrees of freedom
- 18  B3  Population construction, grid, and calculation requirements
- 19  B4  Approximation ratios across table sizes
- 20  B5  Near-independence noise calculation
- 21  B6  Full null results: uniform margins
- 22  B7  Full null results: same-skew margins
- 23  B8  Full null results: different-skew margins
- 24  B9  Ordinary Welch degrees of freedom
- 25  B10 Full power results: uniform margins
- 26  B11 Full power results: same-skew margins
- 27  B12 Full power results: different-skew margins
- 28  B13 Application details
- 29  B14 References: MI and testing foundations
- 30  B15 References: related methods and evaluation

## Appendix

### Slide 15: Appendix title

Appendix title. Not part of the timed talk.

**Delivery**

No timed speech. Keep the conclusion on Slide 14 visible when questions begin, then open the relevant backup when needed and return to Slide 14 afterwards. The divider adds no time to the 18:50 main talk.

### Slide 16 (B1): Variance sensitivity

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

What exactly did you differentiate, and where do the margin terms enter?

**Answer to give**

“I differentiate the pointwise-MI variance along a one-observation perturbation. The first part changes the probability weights. The bracket also changes the log ratios, including their row and column margins. Both contributions are necessary because the pointwise-MI values themselves depend on the table.”

**Notes**

Assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. With every cell positive, positive MI is equivalent to positive V (Appendix A.3), but positive V does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.

**Source**

Thesis Chapter 4: perturbation path (eq:contamination-path), final form of g (eq:g-final), and definition of tau-squared (eq:tau-definition). This derivative is exact for positive population tables. Its use for sampling errors is first order.

### Slide 17 (B2): Moment matching and combined degrees of freedom

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

Where do the component and combined df formulas come from, and why is the Student t distribution approximate?

**Answer to give**

“A variable with a scaled chi-squared distribution has variance twice its squared mean divided by its degrees of freedom. Matching those two moments gives the target. Dividing V-hat by fixed sample size rescales the squared mean and variance equally, so it leaves the component target unchanged. Independence between the two samples lets their variance contributions add. The resulting Student t distribution still requires empirical assessment.”

**Notes**

For a generic variance estimate U modelled as c times a variable with a chi-squared distribution on ν degrees of freedom, E(U)=cν and Var(U)=2c²ν, giving ν=2[E(U)]²/Var(U). Scaling by fixed n leaves this ratio unchanged. For the Slide 7 example at n=1,000, first-order component df are 15.30 against the moment target 21.03: approximately (1/1.19)²/0.97=0.73. This explains the squared-mean effect without another main-slide formula.

**Source**

Thesis Sections 4.1 and 4.3, pp. 23–36; Satterthwaite (1946).

### Slide 18 (B3): Population construction, grid, and calculation requirements

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

How are known-MI populations generated and degenerate calculations handled?

**Answer to give**

“The copying probability changes association while preserving chosen margins. I solve it separately for each target MI. Unsuccessful calculations count as non-rejections, so the rate measures the complete procedure; calculation success is reported separately. Conditioning on success would describe a selected subset of sampled tables.”

**Notes**

Full requirements (Appendix B.3): a Wald calculation succeeds when it has a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14, and a finite p-value. The Expanded Welch calculation additionally requires positive finite component and combined degrees of freedom and a finite p-value; if either component fails, the Expanded Welch calculation is unsuccessful. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so the Expanded Welch calculation is unsuccessful even if the other table makes the shared standard error positive and finite. Zero and undefined component degrees of freedom are distinct cases; both fail the positive-finite requirement. A failed calculation is not evidence of equality.

Sampling is independent within and between populations, and both methods receive identical sampled pairs. The construction uses the same vector for row and column margins within each population and is one association family, not all categorical distributions.

**Source**

Thesis Chapter 5 and Appendix B.1–B.5; current grid results.

### Slide 19 (B4): Approximation ratios across table sizes

Not part of the timed talk. Return to Slide 14 afterwards.

**When opening**

Colour now identifies table size; the rows are three different ratios.

**Question answered**

Is the 4×4 example representative of other sizes and both populations?

**Answer to give**

“The larger tables generally have higher mean peaks, deeper population-variance troughs, and slower recovery in this family. Sample substitution can overpredict even while population inputs underpredict. The main slide isolates one slice so these quantities can first be understood separately.”

**Notes**

Figure 6.2 separately checks how those moment errors affect df. In the worked 4×4/n=1,000 case, FO/target is about 0.73 and the exact values are 15.30/21.03; B2 explains why. Do not infer the mean of estimated df by inserting mean inputs into a nonlinear ratio. Full current Figure 6.2 remains in the thesis; it is not needed as another timed slide.

**Source**

Sections 6.1.1–6.1.2, Figures 6.1–6.2, and current moments.csv; expected 80 rows: 4 sizes × 10 sample sizes × 2 populations.

### Slide 20 (B5): Near-independence noise calculation

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

Why do the mean estimated df remain near five?

**Answer to give**

“Near independence, sampling noise creates apparent association. The quadratic likelihood-ratio approximation includes that noise. Substitution into the component formula gives roughly G divided by two, whose mean is about 4.6 in this setting. The population first-order formula instead approaches n times population MI. These are different approximations, which explains their separation.”

**Notes**

Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.

**Source**

Thesis Appendix A.2 and Section 6.1.3; Figure 6.3. These are local approximations under fixed dimensions and positive limiting cell probabilities, not exact finite-sample distribution identities.

### Slide 21 (B6): Full null results: uniform margins

Not part of the timed talk. Return to Slide 14 afterwards.

**When opening**

Colours here identify the shared MI, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

What happens outside the highlighted different-skew 16×16 example?

**Answer to give**

“Under the copying construction, equal MI and uniform margins give identical population tables. Their expected MI biases cancel in the difference, but errors in the uncertainty estimate and reference distribution can still cause excessive or conservative rejection. Increasing shared MI changes those patterns.”

**Notes**

All 120 settings for the uniform profile. Slide 9 used the 4×4, n = 20 slice of this page.

**Source**

Final Figure 6.4 and balanced-null combined rates, uniform profile. This page contains all 120 settings for that profile.

### Slide 22 (B7): Full null results: same-skew margins

Not part of the timed talk. Return to Slide 14 afterwards.

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

### Slide 23 (B8): Full null results: different-skew margins

Not part of the timed talk. Return to Slide 14 afterwards.

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

### Slide 24 (B9): Ordinary Welch degrees of freedom

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

Would ordinary Welch degrees of freedom work as well as the MI-specific calculation?

**Answer to give**

“Ordinary Welch keeps the same estimated MI difference, standard error, and statistic, but gives each component n minus one degrees of freedom, the rule for comparing sample means. For MI that is only a benchmark, because it ignores how the pointwise-MI variance estimate changes with the table. At n = 20 it removes less of the excess than Expanded Welch. At n = 50, where Wald is already close to 5%, Expanded Welch becomes the most conservative. In the biased 16×16 case neither choice removes the excess. So the MI-specific calculation changes the results, but a larger reduction in rejection does not consistently improve calibration.”

**Notes**

The three settings reuse the main null study's 100,000 sampled pairs per setting at shared MI 0.02 nats with n_P = n_Q = n; all three methods' calculations succeed in every repetition. The thesis examines ordinary Welch only at these illustrative settings and lists this as a limitation (Section 7.2); the main comparison is with the Wald test.

**Source**

Thesis Section 6.2.5, Table 6.2; Section 7.2.

### Slide 25 (B10): Full power results: uniform margins

Not part of the timed talk. Return to Slide 14 afterwards.

**When opening**

Colours here identify the MI gap, not the method: solid lines with filled circles are the Wald test, dashed lines with open squares are the Expanded Welch test. Lower strips show calculation success.

**Question answered**

Do the gap and sample-size patterns hold outside the single curve and snapshot?

**Answer to give**

“The complete uniform-margin grid shows the increase in detection with sufficient observations and the stronger-gap advantage. Larger tables need more data. Expanded Welch never exceeds Wald under the usual thresholds, with method differences becoming small at larger sample sizes.”

**Notes**

120 settings, 240 method rows for this margin profile.

**Source**

Section 6.3.1, Figure 6.7; power rates, profile=uniform, denominator=all. At n=10,000 and gap=.01, EW is 89.44% for 2×2 and 71.12% for 16×16. These values describe the stated population family.

### Slide 26 (B11): Full power results: same-skew margins

Not part of the timed talk. Return to Slide 14 afterwards.

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

### Slide 27 (B12): Full power results: different-skew margins

Not part of the timed talk. Return to Slide 14 afterwards.

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

### Slide 28 (B13): Application details

Not part of the timed talk. Return to Slide 14 afterwards.

**Question answered**

How were the shopping comparisons set up, and why are the weekend degrees of freedom so small?

**Answer to give**

“I compare month–purchase and weekend–purchase MI between new and returning visitors, treating the two visitor groups as independent samples. For month, the corrected difference is about 4.07 standard errors from zero, so both tests reject equal MI. For weekend, both estimates are about 0.0007 nats and the statistic is close to zero, so neither test rejects; that does not establish equality. The weekend degrees of freedom are only 2.18 despite the large samples because both variance estimates fluctuate a lot relative to their size.”

**Notes**

Dataset: 12,330 sessions, each from a different user according to its documentation. P: 1,694 sessions labelled New_Visitor; Q: 10,551 labelled Returning_Visitor; the 85 Other sessions are excluded. Outcome: the Boolean Revenue variable.

Month: January and April have no recorded sessions, so each table is 10×2. All ten months occur in both groups, although the new-visitor February row contains one session and no purchase. Zero cells are retained without adding artificial counts.

Component degrees of freedom: month 12.93 (new) and 187.93 (returning), combined 26.79; weekend 1.69 (new) and 7.71 (returning), combined 2.18.

The final thesis reports unadjusted two-sided p-values for these two comparisons only; it no longer includes a multiple-comparison family or Holm adjustment.

**Source**

Thesis Section 6.4, Tables 6.3–6.4; application CSV; Sakar and Kastro (2018).

### Slide 29 (B14): References: MI and testing foundations

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

### Slide 30 (B15): References: related methods and evaluation

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

## 8. Question preparation

Give a direct answer, a short reason, and a stopping point. Open a backup
when it clarifies the explanation. These are starting answers, not text
to read verbatim. Keep the cited boundary when the study did not evaluate
a proposed extension.

| Likely question | Suggested answer and boundary | Destination |
| --- | --- | --- |
| What exactly is new here? | “The MI first-order variance and the general Satterthwaite principle are established. I derive the MI variance sensitivity including the changing margins, use it for component df, and evaluate where the resulting approximation succeeds or fails.” Avoid a claim of global priority beyond the literature review. | B1–B2 |
| Why not just use sample size minus one? | “That assignment follows from the ordinary sample-variance distribution under normal sampling. An estimated pointwise-MI variance depends on changing probabilities and log ratios, so I calculate its sampling variability instead.” | B1–B2, B9 |
| Why does moment matching imply a Student t test? | “It motivates an approximate reference distribution. Matching a variance component to a scaled chi-squared distribution does not establish the standard normal numerator, or its independence from the variance estimates, that an exact Student t distribution requires.” | B2 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | B3, B8 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | B3; thesis Section 2.4 |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 14 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap, and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 11–12 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 11 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | Slide 12; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 12 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | B5 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | B2, B5 |
| Could unsuccessful calculations explain the low rejection? | “They contribute at some small sample sizes. I report calculation success separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation succeeds.” | B3; Slides 9–10 and B6–B8 |
| Why count unsuccessful calculations as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to successful calculations would condition on a selected subset. Reporting calculation success separately makes the distinction visible.” | B3 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | B3; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | B3, B6–B12 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even when every calculation succeeds. The application illustrates interpretation and cannot verify its population-level accuracy.” | Slides 9–14 |
| Why is the month table 10×2 rather than 12×2? | “January and April have no recorded sessions. Both groups use the same ten recorded month categories and the two purchase outcomes, retaining zero cells within those categories.” | B13 |
| Are the shopping observations independent? | “The dataset documentation says sessions belong to different users. I treat groups and observations as independent, but this remains a working sampling assumption and does not establish representativeness or rule out shared temporal influences.” | B13 |
| Does higher month MI mean a stronger causal month effect? | “It describes greater association in the population comparison. MI depends on the joint probabilities and margins, so it does not isolate a causal response or establish a change in predictive accuracy.” | Slide 13 |
| How much computation does one test require? | “The calculations use a fixed number of scans of an r-by-c table, so time and working memory are O(rc). I have not used this presentation to claim a measured runtime advantage over resampling.” | B1–B2; thesis Section 4.4 |

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
PowerPoint, including jumping from Slide 14 to backups and back.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 3 | 2:40 | Keep literature roles concise; do not recite citations. |
| End of Slide 6 | 7:00 | Use the short form of Slide 7; protect near independence. |
| End of Slide 8 | 10:20 | Shorten Slide 9's rate narration and read only its key comparison. |
| End of Slide 10 | 13:35 | Use the compact Slide 11 explanation; protect the directional result. |
| End of Slide 12 | 16:45 | If past 18:00 use the emergency closing route below. |
| End of Slide 13 | 17:50 | Begin the conclusion immediately; do not open backups. |

### Prepared shorter route

| Slide | Planned | Short form | Preserve |
| --- | --- | --- | --- |
| 2 | 1:15 | 1:00 | Concrete comparison, sample estimates, and population hypothesis |
| 3 | 1:00 | 0:50 | Existing foundations and required MI-specific calculation |
| 4 | 1:20 | 1:10 | Shared statistic and visible cutoff difference |
| 5 | 1:40 | 1:25 | Derivation chain, final formula, and two approximations |
| 6 | 1:20 | 1:10 | Parallel studies, sample size versus repetitions, unsuccessful-calculation rule |
| 7 | 1:40 | 1:25 | Mean/variance distinction and the 19%, 3%, and 8% anchors |
| 9 | 1:30 | 1:20 | The .02 improvement and .30 failure, equal MI, and every calculation succeeding |
| 10 | 1:45 | 1:35 | Similar variance errors, different bias, and opposite rejection |
| 11 | 1:30 | 1:20 | Power definition, one curve, and three-gap snapshot |
| 13 | 1:05 | 0:55 | Return to example, rejection at 0.05, and unknown population MI |
| 14 | 1:00 | 0:50 | Contribution, conditional benefit, remaining errors, and next steps |

These reductions total 125 seconds, giving **16:45**. Slides 8 and 12
remain at full length because they carry important explanations. Use this
route to simplify narration, not to speak faster.

### If Slide 12 ends at 18:00

- **Slide 13, about 30 seconds:** “Returning visitors have higher estimated
  month–purchase MI, and both tests reject equality at the usual 0.05
  threshold. The unknown population values mean this illustrates
  interpretation without validating false-positive accuracy.”
- **Slide 14, about 50 seconds:** “I derived MI-specific variance
  sensitivity and degrees of freedom. The larger cutoff improves some
  excessive false-positive rates, while deepening conservatism and reducing
  power elsewhere. The remaining bias can even reverse the estimated
  direction. Improving estimation, retaining sampling variation near
  independence, and testing broader populations are the next steps.
  Thank you.”

This route finishes at about 19:20. Do not cut the conclusion, start
narrating backup slides, or fill spare time with an unplanned experiment.
Timing remains provisional until a complete timed rehearsal.
