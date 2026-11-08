# Speaker notes: Comparing Mutual Information in Finite Samples

Synchronised with `Daniel_Zhao_Welch_MI_Presentation.pptx` (28 slides: 16 main, 12 backup). The scripts and transitions are the rehearsal draft from the presentation plan, unchanged. Learn the explanation, then speak naturally from the cues.

## Timing

| Slide | Title | Time | Finish by |
| --- | --- | --- | --- |
| 1 | Comparing Mutual Information in Finite Samples | 0:25 | 0:25 |
| 2 | Comparing association across populations | 1:05 | 1:30 |
| 3 | Sampling uncertainty in the MI comparison | 1:00 | 2:30 |
| 4 | Existing foundations and the MI-specific contribution | 0:55 | 3:25 |
| 5 | Normal Wald and Expanded Welch | 1:10 | 4:35 |
| 6 | Deriving the degrees of freedom | 2:00 | 6:35 |
| 7 | Evaluation from known populations | 1:15 | 7:50 |
| 8 | Sparse samples distort the variance inputs | 1:20 | 9:10 |
| 9 | Sampling noise matters near independence | 1:30 | 10:40 |
| 10 | The benefit depends on Wald's false-positive rate | 1:20 | 12:00 |
| 11 | False-positive rates across common MI values | 1:10 | 13:10 |
| 12 | Power across three MI differences | 1:05 | 14:15 |
| 13 | Bias can reverse the estimated direction | 1:30 | 15:45 |
| 14 | An application to online shopping | 1:15 | 17:00 |
| 15 | Limitations and future work | 1:00 | 18:00 |
| 16 | Contributions and conclusions | 0:50 | 18:50 |

Main talk target: 18:50, leaving 70 seconds before the 20-minute cut-off. Keep Slide 16 on screen when questions begin.

## Main slides

### Slide 1: Comparing Mutual Information in Finite Samples

**Time:** 0:25 (finish by 0:25)

**Script**

My project asks whether mutual information differs between two populations when we only have finite samples. I develop an MI-specific Welch–Satterthwaite test and examine when its larger rejection cutoff improves false-positive accuracy, and what that costs in detection.

**Transition**

“I will start with the comparison we might want to make.”

**Delivery Cue**

Look at the audience for the opening question. Do not read the full title and affiliation. Advance within 25 seconds.

**Source**

Thesis title, abstract and Chapter 1, pp. 1–3.

### Slide 2: Comparing association across populations

**Time:** 1:05 (finish by 1:30)

**Script**

Mutual information measures the average reduction in uncertainty about one variable when we observe another. In the application later in the talk, the variables are the month of a website visit and whether that session ends in a purchase. We can measure their association separately among new visitors and returning visitors. I call their joint population distributions P and Q. The question is whether the population MI differs between those groups. It is an association question, and it does not require a causal interpretation of month. Before using observed data, however, we need a way to account for sampling uncertainty in that comparison.

**Transition**

“Two different sample estimates can arise even when the population MI values are equal.”

**Delivery Cue**

Explain the definition facing the audience, then point once to each group. Do not announce the application result yet.

**Source**

Thesis Sections 1.1 and 2.1; Bossomaier et al. (2016). The shopping example is from Section 6.4, pp. 69–71.

### Slide 3: Sampling uncertainty in the MI comparison

**Time:** 1:00 (finish by 2:30)

**Script**

The parameter is the signed difference, MI in P minus MI in Q, and the null hypothesis sets that difference to zero. Different samples produce different count tables, so they also produce different MI estimates. Rare combinations of categories are especially difficult because a cell can be missed in one sample and observed only once in another. These errors can change both the estimated difference and its estimated standard error. When the population MI values are equal, I want a test using the usual five-percent significance level to reject in about five percent of repetitions. That false-positive target gives us a concrete way to assess the comparison.

**Transition**

“The literature supplies the MI variance approximation, but choosing a Welch-type reference requires an additional calculation.”

**Delivery Cue**

Pause after naming the null. Stress that equal MI allows different probability tables. Do not imply P = Q under every null setting.

**Source**

Thesis Chapters 1–3, particularly Equation (1.1) and Section 3.2.

### Slide 4: Existing foundations and the MI-specific contribution

**Time:** 0:55 (finish by 3:25)

**Script**

This project builds on established results rather than introducing the general Welch–Satterthwaite principle. Work on MI gives the leading bias and first-order sampling variance. Welch and Satterthwaite provide a way to choose degrees of freedom by matching variance moments, and related ideas have been used for entropy and regression comparisons. For this MI test, the additional task is to calculate how the estimated pointwise-MI variance changes when the table changes. I derive that sensitivity while allowing the cell probabilities, row totals and column totals to change together, then evaluate the resulting approximation.

**Transition**

“The resulting test keeps the same statistic as Wald and changes the reference distribution used to judge it.”

**Delivery Cue**

Spend most of the slide on the final row. Say what each strand provides; do not recite every citation or claim that no equivalent formula has ever appeared anywhere.
Mora and Ruiz-Castillo (2009) is the direct normal-approximation precedent for MI comparisons, if asked.

**Source**

Thesis Sections 2.2–2.5, pp. 6–17. Moddemeijer (1989); Paninski (2003); Satterthwaite (1946); Welch (1947); Hutcheson (1970); Pan and Wall (2002); Mora and Ruiz-Castillo (2009).

### Slide 5: Normal Wald and Expanded Welch

**Time:** 1:10 (finish by 4:35)

**Script**

Both methods divide the MI difference, after its leading bias correction, by the same estimated standard error. The denominator adds a variance contribution from each independent sample. Pointwise MI is the information contribution of one category pair. V-hat estimates its variance, and dividing by sample size estimates the sampling variance of an MI estimate. Wald compares the statistic with the standard normal distribution. Expanded Welch uses a Student t distribution, whose degrees of freedom are estimated from the data. The example with three degrees of freedom shows why heavier tails give a larger rejection cutoff. Consequently, Expanded Welch's rejections are a subset of Wald's under these testing rules. The next question is how to calculate the degrees of freedom for MI.

**Transition**

“The important input is how much the variance estimate itself changes from sample to sample.”

**Delivery Cue**

Trace the common numerator and denominator once. Point to the cutoff locations. Explain that the reference plot's three degrees of freedom are illustrative; actual values vary between sampled table pairs. Expanded Welch also needs valid degrees-of-freedom calculations; the additional validity requirements are introduced on Slide 7 and specified in B4.

**Source**

Thesis Sections 3.2–3.3 and 4.1–4.3; Figure 2.1.

### Slide 6: Deriving the degrees of freedom

**Time:** 2:00 (finish by 6:35)

**Script**

There are two levels of variability here. V-hat describes variation in pointwise MI across observation outcomes, but V-hat itself also changes when a new sample gives a different table. I first calculate its sensitivity to moving a small amount of probability towards one cell. That change affects the selected cell, its row and column totals, and the pointwise-MI values. The derivative g collects those effects.

Averaging the observation-level sensitivities gives a first-order approximation to the sampling error of V-hat. Its sampling variance is therefore approximately tau-squared divided by sample size. I then use Satterthwaite moment matching: twice the squared mean of a variance estimate, divided by that estimate's sampling variance. Substituting the sample-based inputs gives the component formula at the bottom. Greater fluctuation relative to the squared mean gives fewer degrees of freedom and a larger cutoff. I repeat the calculation for Q and combine the components. This is an approximate Student t reference, so the experiments must check how well these steps work.

**Transition**

“I checked the variance approximations first, then evaluated false positives and power using populations whose MI values are known.”

**Delivery Cue**

Use the full two minutes. Pause at each change of level of variance. The final formula gives component degrees of freedom, not the combined degrees of freedom. Do not suggest that moment matching proves the numerator and denominator are independent. If asked for the exact derivative, show Backup B1.

**Source**

Thesis Sections 4.1–4.3, pp. 23–35 (definition of g, final form of g, sampling variance of V-hat, component moment target, estimated component df, combined df).

### Slide 7: Evaluation from known populations

**Time:** 1:15 (finish by 7:50)

**Script**

I construct population tables with known MI, then draw repeated samples. MI is reported in nats, using natural logarithms. The first study checks the variance approximations. The false-positive study uses three equal-MI levels, while power fixes MI in P at 0.02 nats and gives Q three larger MI values. Both studies cross four table sizes and ten sample sizes with uniform or uneven margins. The uneven margins either agree between populations or differ, giving 360 settings each for false positives and power. Each test sees only its two sampled tables. The 100,000 repetitions measure performance rather than increasing that test's sample size. Both tests use the same sampled pairs, with invalid calculations counted as non-rejections and validity reported separately.

**Transition**

“The first result concerns the inputs to the degrees of freedom, before any test rejection is considered.”

**Delivery Cue**

Explain “same skew” as the same uneven margins in both populations and “different skew” as different category frequencies. Do not recite all ten sample sizes or every margin probability. Full margin vectors and the sample-size list are in B3.

**Source**

Thesis Chapter 5, pp. 39–46, Tables 5.1–5.3; Morris et al. (2019). Exact construction and validity rules: Appendix B.

### Slide 8: Sparse samples distort the variance inputs

**Time:** 1:20 (finish by 9:10)

**Script**

This slide isolates one population and table size so the two errors are visible. On the left, one would mean that the average V-hat equals the population quantity. Instead, the mean rises well above that benchmark before recovering. Rare cells that begin to appear can have large empirical pointwise-MI deviations and inflate the estimate.

On the right, one means that the predicted sampling variance of V-hat agrees with the variance observed across repetitions. The population first-order prediction falls below one over the sparse range. Estimating its inputs from each sample can reverse the error and overshoot. Since degrees of freedom square the mean input and divide by the sampling variance input, both errors matter. Larger samples improve the agreement in this fixed population.

**Transition**

“Near independence, sampling noise causes an additional separation between the population formula and the sample-based result.”

**Delivery Cue**

Explain the left graph completely before moving right. Say “sampling variance of V-hat” explicitly. Do not call the right graph the sampling variance of the MI estimator. Avoid narrating every marker.

**Source**

Thesis Section 6.1.1, pp. 47–50; Figure 6.1. At n = 50: mean ratio 12.71; population-input ratio 0.186; sample-based ratio 0.553.

### Slide 9: Sampling noise matters near independence

**Time:** 1:30 (finish by 10:40)

**Script**

Here sample size stays at one thousand and the population MI approaches zero. The black population first-order value becomes very small, but the mean degrees of freedom estimated from sampled tables remain around five at the weakest association. The green curve is the moment-matching target calculated from the actual sampling mean and variance. That target is about nine, so the mean estimate is still only about half the target.

A sampled table can show apparent association even when population association is almost absent. The sample-based variance and sensitivity retain that noise. Near independence, the linear sampling contribution becomes small, so quadratic sampling terms matter. The additional calculation in the thesis explains why the estimated degrees of freedom stay positive rather than following the shrinking population value. This is a check on the approximation, not a proof of an exact Student t distribution or a validated replacement test at independence.

**Transition**

“These approximation errors matter because the larger cutoff lowers rejection, and that reduction is not equally helpful everywhere.”

**Delivery Cue**

Point to the low-MI end before describing the curves. Pause after “around five”. Explain the target's role rather than reading three symbols. Keep this slide in the shorter route.

**Source**

Thesis Section 6.1.3, pp. 52–56, Figure 6.3 and Appendix A.2. At MI 0.0001, saved P values: mean df 4.859787, moment target 9.124808, population first-order df 0.096400. These are component quantities.

### Slide 10: The benefit depends on Wald's false-positive rate

**Time:** 1:20 (finish by 12:00)

**Script**

I assess false-positive accuracy by closeness to five percent. The first row shows the useful case: Expanded Welch brings Wald's excessive rejection from 8.35 percent to 4.90 percent. In the second row, Wald already rejects too rarely, and the larger cutoff lowers rejection further. The third row shows a more serious failure: rejection stays around a quarter of repetitions even after the cutoff increases.

These examples have no calculation failures. Their different behaviour comes from the shared estimates and the sampling distribution of the statistic. In particular, different remaining biases can shift the MI difference away from zero under equal MI. A larger cutoff can offset some errors at a particular setting without making inference accurate across populations.

**Transition**

“The full experiment also changes the common MI, while keeping the population difference at zero.”

**Delivery Cue**

Take one row at a time. Point back to the same 5% target for each row. Do not describe the table as three predetermined focus settings or as evidence of universal improvement.

**Source**

Thesis Section 6.2.4 and Table 6.1, p. 62. Combined balanced-null rates.

### Slide 11: False-positive rates across common MI values

**Time:** 1:10 (finish by 13:10)

**Script**

This panel keeps equal MI in the two populations but changes the common level of association. Colour identifies that common MI, and line style identifies the method. At the weakest MI and one thousand observations per population, Wald rejects in 36.38 percent of repetitions and Expanded Welch in 34.38 percent. The validity strip shows that both methods return usable results in every repetition there. The failure is inferential.

With more observations, rejection falls, and the weakest-MI curve is below the target at the largest tested sample size. The experiment can therefore pass through excessive and conservative ranges. The larger cutoff lowers rejection throughout, but it does not by itself solve either problem.

**Transition**

“The same larger cutoff also affects the probability of detecting a genuine MI difference.”

**Delivery Cue**

Introduce axes and encodings before pointing to the peak. Say which common MI the highlighted values use. Avoid presenting 36.38% as the MI-0.02 value from Slide 10. The shaded bands describe Monte Carlo uncertainty at each point, not simultaneous confidence over the full grid.

**Source**

Thesis Section 6.2.3, pp. 60–61; Figure 6.6. Balanced-null combined rates, 16×16, different skew, all repetitions as denominator. No threshold fitting is involved.

### Slide 12: Power across three MI differences

**Time:** 1:05 (finish by 14:15)

**Script**

Power is the probability of rejecting equal MI when the population MI values differ. Colour now identifies the magnitude of the MI gap. P stays at 0.02 nats, and Q's MI increases to create the three gaps. Once samples are sufficiently large, the larger differences become easier to detect. Expanded Welch remains at or below Wald because its cutoff is larger, with the method curves becoming close at larger sample sizes.

These are power rates under the usual testing rules. Because actual false-positive rates can differ, they do not compare power at a common achieved false-positive rate. The next example also shows why a two-sided rejection can conceal an important error in direction.

**Transition**

“In sparse tables with different margins, bias can even make the estimated difference point towards the wrong population.”

**Delivery Cue**

Explicitly announce the change in colour meaning from Slide 11: colour now means MI-gap magnitude. Do not interpret close curves as a plotting failure or claim Expanded Welch has higher nominal power anywhere.

**Source**

Thesis Section 6.3.1, pp. 63–65, Figure 6.7; MI-gap combined rates, 4×4, uniform, all repetitions as denominator.

### Slide 13: Bias can reverse the estimated direction

**Time:** 1:30 (finish by 15:45)

**Script**

This example fixes a true difference of minus 0.01 nats, so Q has greater population MI. At one thousand observations per population, however, the average estimated difference is about plus 0.0207 nats. Different residual biases in the two MI estimates have outweighed the true gap and shifted the sampling centre to the other side of zero.

Expanded Welch rejects in about 9.66 percent of repetitions at this point. Among those rejections, more than 99.9 percent have a positive estimated difference, opposite to the population direction. They count as power under the two-sided definition, but they fail to identify which population has greater MI. As sample size increases, the positive bias diminishes, the centre passes near zero, and rejection initially falls before recovering. Changing the cutoff leaves that biased movement unchanged.

**Transition**

“The shopping data illustrate the same calculation, although their unknown population values prevent this kind of accuracy check.”

**Delivery Cue**

Explain the two signed numbers before citing the percentage. Emphasise “among those rejections”. The bias is approximately 0.0306714 nats; the estimated mean is −0.01 plus that bias. Do not describe a positive estimate as higher true MI in P.

**Source**

Thesis Section 6.3.3, pp. 67–69; Figure 6.9. Saved counts: 9,659 positive and 3 negative Expanded Welch rejections, 9,662 in total, out of 100,000 repetitions.

### Slide 14: An application to online shopping

**Time:** 1:15 (finish by 17:00)

**Script**

Returning to the shopping question, I compare the association between month and purchase outcome among new and returning visitors. The corrected MI estimate is higher for returning visitors, giving a negative difference when I subtract returning-visitor MI from new-visitor MI. Both methods reject equal MI, including after Holm adjustment across the six exploratory comparisons. Expanded Welch's adjusted p-value is about 0.00149.

This is evidence from the approximate tests for a difference in month–purchase MI. It is not a causal claim about month. Unlike the simulations, the population tables are unknown, so this application illustrates how to use and interpret the outputs without measuring their false-positive accuracy. The weekend comparison does not reject equality, which also does not establish equality.

**Transition**

“The application makes the practical limits important, so I will finish by distinguishing the contribution from what remains to test.”

**Delivery Cue**

Keep the emphasis on association, signed difference and adjusted inference. Keep the group sizes out of the main spoken comparison. Explain the six-comparison family if asked (B10). Do not claim Holm adjustment repairs the test's approximation errors.

**Source**

Thesis Section 6.4, pp. 69–71, Tables 6.2–6.3 and Appendix B.7. Sakar and Kastro (2018); Holm (1979). Corrected MI 0.004316 (new) and 0.017880 (returning); difference −0.013563; Expanded Welch df 26.79; Holm-adjusted p 0.000189 (Wald) and 0.00149 (Expanded Welch).

### Slide 15: Limitations and future work

**Time:** 1:00 (finish by 18:00)

**Script**

The first limitation is the first-order approximation, particularly near independence, where additional quadratic sampling variation becomes important. The second is estimation: changing the reference cutoff leaves errors in the MI difference and standard error in place. A useful next step is to change one estimator at a time and check how that affects rejection and direction.

The experiments also use one copying construction and equal sample sizes. They vary several important parameters within that family, but they do not establish performance across every association pattern. Other constructions and unequal sample sizes would test how broadly the findings persist.

**Transition**

“The project therefore establishes a specific calculation and a clear boundary on what its cutoff adjustment can accomplish.”

**Delivery Cue**

Use the paired rows to show why each proposed extension makes sense. Keep to one minute and protect time for the conclusion. Explain unshown limits in the question period.

**Source**

Thesis Sections 7.2–7.3, pp. 74–75.

### Slide 16: Contributions and conclusions

**Time:** 0:50 (finish by 18:50)

**Script**

I derived how the estimated pointwise-MI variance responds to changes in a count table and used that sensitivity to calculate MI-specific degrees of freedom. The resulting larger cutoff brings some excessive false-positive rates closer to five percent, but also deepens conservatism and reduces power under the usual testing rules.

The sparse-table failures show why the estimates themselves remain important. A different cutoff leaves bias and standard-error errors unchanged. The contribution is therefore both the calculation and the evidence identifying its limits. Thank you, and I welcome your questions.

**Delivery Cue**

Face the audience for the final statements. Do not rush through “some” or imply a general recommendation. Stop at approximately 18:50 with this slide still displayed, and keep it on screen when questions begin.

**Source**

Final abstract; Sections 1.3 and 7.1–7.3.

## Backup slides

Jump from Slide 16 by typing the slide number and pressing Enter; return the same way.

### Slide 17: Variance sensitivity

Not part of the timed talk.

**Question answered**

What exactly did you differentiate, and where do the margin terms enter?

**Answer to give**

“I differentiate the pointwise-MI variance along a one-observation perturbation. The first part changes the probability weights. The bracket also changes the log ratios, including their row and column margins. Both contributions are necessary because the pointwise-MI values themselves depend on the table.”

**Notes**

Regularity assumptions: fixed categories, independent observations within each sample, independent samples, positive population cell probabilities, and positive V and tau-squared for the first-order degrees-of-freedom construction. Positive MI alone does not guarantee positive tau-squared. A zero component is not an ordinary finite degrees-of-freedom value.

**Source**

Thesis Chapter 4: perturbation path, final form of g and definition of tau-squared. The derivative is exact for positive population tables; its use for sampling errors is first order.

### Slide 18: Moment matching and the combined reference

Not part of the timed talk.

**Question answered**

Where do the component and combined degrees-of-freedom formulas come from, and why is the Student t reference approximate?

**Answer to give**

“A scaled chi-squared variable has variance twice its squared mean divided by its degrees of freedom. Matching those two moments gives the target. Dividing V-hat by fixed sample size rescales the squared mean and variance equally, so it leaves the component target unchanged. Independence between the two samples lets their variance contributions add. The resulting Student t reference still requires empirical assessment.”

**Notes**

Scaled chi-squared derivation: take E{V-hat} times chi-squared(nu) divided by nu. Its mean is E{V-hat}, because a chi-squared variable with nu degrees of freedom has mean nu. Its variance is [E{V-hat}]^2 times 2 nu divided by nu^2, which is 2[E{V-hat}]^2 / nu. Setting that equal to Var{V-hat} gives nu_mom = 2[E{V-hat}]^2 / Var{V-hat}. Substituting V-hat for the mean and tau-hat-squared / n for the sampling variance gives the estimated component formula.

**Source**

Thesis Sections 4.1 and 4.3, pp. 23–35; Satterthwaite (1946).

### Slide 19: Population construction and parameter grid

Not part of the timed talk.

**Question answered**

How are different tables constructed at a known MI, and what parameter combinations were evaluated?

**Answer to give**

“The construction mixes an independent draw with a copying draw. It preserves the specified margins, while the copying probability controls association. I solve separately for the copying probability in each population to reach the target MI. The full grid is evaluated at every null MI and power-gap value; it is not a selection of favourable cases.”

**Notes**

The construction is one controlled association family, not a representation of every possible categorical joint distribution.

**Source**

Thesis Section 5.1, Tables 5.1–5.2 and Appendix B.1–B.2.

### Slide 20: Validity and rejection denominators

Not part of the timed talk.

**Question answered**

How are degenerate calculations handled, and can calculation failures explain low rejection?

**Answer to give**

“The rate measures the complete implemented procedure, including failures, so invalid outputs count as non-rejections. The separate validity measure lets us see that contribution. Conditioning on validity would answer a different question and select a different subset of samples. Several important failures persist with 100% validity, including the large false-positive rate highlighted in the talk.”

**Notes**

Full rules: Normal Wald requires a finite corrected difference, a finite positive standard error, V-hat(P) + V-hat(Q) > 10^-14, and a finite p-value; the threshold treats variances extremely close to zero as numerically unusable. Expanded Welch additionally requires positive finite degrees of freedom for both components and their combination, and a finite Expanded Welch p-value. A failed component makes Expanded Welch invalid. If a sampled table has V-hat = tau-hat-squared = 0, the component formula requires 0/0, so Expanded Welch records the comparison as invalid even if the other table makes the shared standard error positive and finite. A zero V-hat with positive tau-hat-squared gives zero component degrees of freedom, which also fails the positive requirement. The primary rejection rate divides valid rejections by all repetitions. No minimum expected-count filter is applied.

**Source**

Thesis Appendix B.3–B.5 and the validity strips in Figures 6.4–6.9.

### Slide 21: The near-independence noise calculation

Not part of the timed talk.

**Question answered**

Why do the mean estimated degrees of freedom remain near five?

**Answer to give**

“Near independence, sampling noise creates apparent association. The quadratic likelihood-ratio approximation includes that noise. Substitution into the component formula gives roughly G divided by two, whose mean is about 4.6 in this setting. The population first-order formula instead approaches n times population MI. These are different approximations, which explains their separation.”

**Notes**

Formulas: mean estimated component df (d + kappa)/2 = 4.60; sampling-moment target (d + kappa)^2/(d + 2 kappa) = 9.00; variance-prediction ratio 2(d + kappa)/(d + 2 kappa) = 1.96. The observed column is population P. The model predicts 9.00 for the target; it does not predict the observed 9.12 exactly.

**Source**

Thesis Appendix A.2 and Section 6.1.3; Figure 6.3. These are local approximations under fixed dimensions and positive limiting cell probabilities, not exact finite-sample distribution identities.

### Slide 22: Null results with uniform margins

Not part of the timed talk.

**Question answered**

What happens outside the highlighted different-skew 16×16 example?

**Answer to give**

“Under the copying construction, equal MI and uniform margins give identical population tables. Their expected MI biases cancel in the difference, but errors in the uncertainty estimate and reference distribution can still cause excessive or conservative rejection. Increasing common MI changes those patterns.”

**Notes**

This page contains all 120 settings for the uniform profile.

**Source**

Final Figure 6.4; balanced-null combined rates, uniform profile.

### Slide 23: Null results with same-skew margins

Not part of the timed talk.

**Question answered**

What changes when both populations have the same uneven category frequencies?

**Answer to give**

“The population tables are still identical under equal MI, so expected bias in the difference cancels. Uneven margins leave more rare category combinations. The conservative ranges persist beyond the smallest samples and are not explained solely by calculation failures. Expanded Welch lowers those already-low rates further.”

**Notes**

This page contains all 120 settings for the same-skew profile.

**Source**

Final Figure 6.5; balanced-null combined rates, same-skew profile.

### Slide 24: Null results with different-skew margins

Not part of the timed talk.

**Question answered**

Are the severe failures restricted to the largest table, and what is visible over the complete margin-specific grid?

**Answer to give**

“Here equal MI permits different population tables. The remaining MI biases need not cancel, and in the sparse largest table they can shift the estimated difference substantially away from zero. The smaller-table patterns and the dependence on common MI remain visible in this complete slice of the null grid.”

**Notes**

This page contains all 120 settings for the different-skew profile. The main talk enlarged the 16×16 panel on Slide 11.

**Source**

Final Figure 6.6; balanced-null combined rates, different-skew profile.

### Slide 25: Power with same-skew margins

Not part of the timed talk.

**Question answered**

Do the power patterns also occur when both groups have the same uneven margins?

**Answer to give**

“These power curves use the same uneven margins in both populations. Larger tables need more observations, and the smaller MI gap remains harder to detect. For example, at n = 50,000, the 16×16 Expanded Welch power is 79.87% for the smallest gap, compared with more than 99.9% for each of the two larger gaps. The method difference is smaller than these gap and setting effects at larger sample sizes.”

**Notes**

This page contains all 120 settings for the same-skew power profile.

**Source**

Final Figure 6.8; Section 6.3.2; MI-gap combined rates, same-skew profile.

### Slide 26: Application details and the comparison family

Not part of the timed talk.

**Question answered**

Why were six comparisons adjusted, and what else was tested?

**Answer to give**

“The two shopping examples were selected from a fixed six-comparison exploratory family across three public datasets. I apply Holm's adjustment separately to each method's six p-values. Both adjusted month results remain below 0.05. This adjustment addresses multiplicity; it does not establish that the approximate underlying p-values are calibrated.”

**Notes**

Groups: 1,694 sessions labelled New_Visitor (P) and 10,551 labelled Returning_Visitor (Q); the 85 Other sessions are excluded. The dataset has 12,330 sessions, each from a different user according to its documentation. Outcome: the Boolean Revenue variable.
Month: January and April have no recorded sessions, so each month table is 10×2. All ten months occur in both groups, although the new-visitor February row contains one session and no purchase. Zero cells are retained without smoothing.
Month degrees of freedom: component 12.93 (new visitors) and 187.93 (returning visitors); combined 26.79.
Weekend: corrected MI 0.000664 (new) and 0.000727 (returning); T = −0.056; Expanded Welch df 2.18; p-values 0.9554 (Wald) and 0.9601 (Expanded Welch). Neither test rejects, and this non-rejection does not establish equality.
Holm: order each method's six p-values from smallest to largest, multiply by 6, 5, 4, 3, 2 and 1, take the cumulative maximum and cap at one. Month is the third smallest, so its multiplier is 4.
Other family members: Adult education and occupation versus income above $50,000, comparing female and male records; Student Performance study time and maternal education versus final grade at least 10 (Portuguese course), comparing schools GP and MS.

**Source**

Thesis Section 6.4 and Appendix B.7, Table B.1; the application protocol. Becker and Kohavi (1996); Sakar and Kastro (2018); Cortez (2008); Holm (1979).

### Slide 27: References: MI and testing foundations

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

### Slide 28: References: related methods and evaluation

Not part of the timed talk. Use this page if a source is requested. Entries follow the thesis bibliography.

## Question preparation

Aim for a direct first sentence, a short explanation and a stopping point.
Use a backup when it will help, rather than opening several slides in
succession. Answers below are starting scripts, not statements Daniel
should read aloud word for word.

| Likely question | Suggested answer and boundary | Backup |
| --- | --- | --- |
| What exactly is new here? | “The MI first-order variance and the general Satterthwaite principle are established. I derive the MI variance sensitivity including the changing margins, use it for component df, and evaluate where the resulting approximation succeeds or fails.” Avoid a claim of global priority beyond the literature review. | B1–B2 |
| Why not just use sample size minus one? | “That assignment follows from the ordinary sample-variance distribution under normal sampling. An estimated pointwise-MI variance depends on changing probabilities and log ratios, so I calculate its sampling variability instead.” | B1–B2 |
| Why does moment matching imply a Student t test? | “It motivates an approximate reference. Matching a scaled chi-squared variance component does not prove the standard normal numerator and independence conditions of an exact Student t construction.” | B2 |
| How is equal MI different from equal distributions? | “Distinct tables can have the same probability-weighted MI average. The different-skew null settings explicitly test that weaker hypothesis, allowing the tables and remaining estimation biases to differ.” | B3, B8 |
| Would a label-permutation test solve this? | “A simple pooled label permutation is exact under identical distributions. Equal MI alone does not give that exchangeability. A specialised parameter-valid permutation procedure would need its own justification.” Do not claim every permutation method is invalid. | B3; cite thesis Section 2.4 in notes |
| Why use only Wald as the comparator? | “It isolates the effect of changing the reference cutoff while sharing the same estimates and statistic. The study does not establish superiority over bootstrap methods or other MI estimators.” | Slide 15 |
| Why evaluate power when its ordering is already known? | “The ordering follows from the testing rules, but its magnitude and dependence on sample size, gap and margins require evaluation. The biased examples also show why rejection can fail to identify the true direction.” | Slides 12–13 |
| Is this a fair power comparison if actual false-positive rates differ? | “It compares the methods under their usual nominal testing rules. It is not a comparison at a common achieved false-positive rate, and I interpret it alongside the null results.” Do not describe an abandoned fitted-threshold experiment. | Slide 12 |
| Why does stronger population separation sometimes lower power? | “A persistent positive bias can oppose the negative true difference. Making that true difference more negative initially moves the sampling centre closer to zero, reducing positive-tail rejection before negative-tail rejection recovers.” | Slide 13; Section 6.3.3 |
| Are wrong-direction rejections excluded from power? | “No. The tests are two-sided, so both directions count. I report the sign separately to show that detecting some difference does not necessarily identify which population has greater MI.” | Slide 13 |
| Why do estimated df stay near five at almost zero MI? | “Sampling creates apparent association. The quadratic approximation retains it and gives approximately G/2 for the component df, rather than n times population MI alone.” | B5 |
| Is the moment target the correct t df? | “It is the target defined by matching the actual first two moments of the variance estimate. It is not a guarantee that the statistic follows a Student t distribution.” | B2, B5 |
| Could invalid calculations explain the low rejection? | “They contribute at some small sample sizes. I report their frequency separately. Important conservative ranges and the highlighted excessive-rejection cases persist when every calculation is valid.” | B4; Slide 11 |
| Why count invalid outputs as non-rejections? | “That reports the full implemented procedure's ability to reject. Restricting to valid outputs would condition on a selected subset. Reporting validity separately makes the distinction visible.” | B4 |
| Does the leading bias correction matter with equal sample sizes? | “For the shared fixed table dimensions, the corrections cancel exactly. Residual biases can still differ. The general method allows unequal sample sizes, but the simulations do not assess the correction's unequal-sample performance.” | B3; thesis Section 5.5 |
| Why one construction and equal row/column margins? | “They give a controlled family where I can vary MI and sparsity while preserving chosen margins. The balanced grid is broad within that family, but other association patterns and unequal margins remain a limitation.” | B3, B6–B9 |
| Can you recommend Expanded Welch for a new dataset? | “The evidence supports conditional improvements rather than a universal choice. In sparse settings, both methods can be inaccurate even with valid outputs. The application illustrates interpretation and cannot verify its population-level accuracy.” | Slides 10–15 |
| Why is the month table 10×2 rather than 12×2? | “January and April have no recorded sessions. Both groups use the same ten recorded month categories and the two purchase outcomes, retaining zero cells within those categories.” | B10 |
| Are the shopping observations independent? | “The dataset documentation says sessions belong to different users. I treat groups and observations as independent, but this remains a working sampling assumption and does not establish representativeness or rule out shared temporal influences.” | B10 |
| Does higher month MI mean a stronger causal month effect? | “It describes greater association in the population comparison. MI depends on the joint probabilities and margins, so it does not isolate a causal response or establish a change in predictive accuracy.” | Slide 14 |
| Why are six comparisons in the Holm family? | “They were the six specified public-data comparisons: two each from Adult, Shoppers and Student Performance. Both shopping results are interpreted within that original family, with a separate adjustment for each test.” | B10 |
| How much computation does one test require? | “The calculations use a fixed number of scans of an r-by-c table, so time and working memory are O(rc). I have not used this presentation to claim a measured runtime advantage over resampling.” | B1–B2; thesis Section 4.4 |

If asked a question the study did not evaluate, state the boundary directly:
“That comparison was not part of the reported experiment. The current
results establish [specific result]; testing [requested extension] would
be the next study.” Do not invent a result to make the answer more complete.

## Rehearsal, timing and an emergency shorter route

### Normal rehearsal

1. First practise the argument without slides. Daniel should be able to
   explain the question, the extra variance calculation and the conditional
   result in about two minutes.
2. Rehearse the full deck with a timer, including every pointer movement
   and graph-reading pause. Record split times at Slides 4, 7, 9, 13 and 15.
3. After learning the script, rehearse from the purpose and cue lines.
   Keep the full script in notes for preparation, not as projected prose.
4. Ask a listener unfamiliar with the derivation what V-hat, its sampling
   variance, and the method comparison mean. Repair the explanation if
   those quantities are confused. Do not solve the problem by adding all
   the algebra to the main slide.
5. Practise jumping from Slide 16 to the correct backup and back. Practise
   at least the questions about exact t validity, the power definition,
   near independence and the six-comparison family.
6. Rehearse from the exported PDF too. Every statement should be supported
   without depending on a live animation, link, notebook or internet access.

Leave brief pauses after introducing axes and after the main signed-number
comparison on Slide 13. Make eye contact after explaining each result.
Finishing earlier than 18:50 is acceptable if the explanation remains
complete. Do not fill spare time with unplanned backup material.

### Checkpoints

| Point reached | Target elapsed | Action if late |
| --- | --- | --- |
| End of Slide 4 | 3:25 | Shorten citation narration, not the statement of contribution. |
| End of Slide 7 | 7:50 | Use the short form for Slide 8; preserve the dedicated near-independence slide. |
| End of Slide 9 | 10:40 | If past 11:30, use short forms of Slides 10–12 and 14–15. |
| End of Slide 13 | 15:45 | If past 17:00, shorten the application and limitations. Protect the conclusion. |
| End of Slide 15 | 18:00 | Begin the conclusion immediately. Do not open backups. |

### Prepared reductions

| Slide | Planned | Short form | What to retain |
| --- | --- | --- | --- |
| 4 | 0:55 | 0:40 | Existing MI variance, moment matching, the MI-specific calculation. |
| 6 | 2:00 | 1:40 | The two levels of variance, component formula and approximate status. |
| 8 | 1:20 | 1:05 | Meaning of one and the opposite population/sample prediction errors. |
| 10 | 1:20 | 1:05 | One sentence per table row and the fixed 5% target. |
| 11 | 1:10 | 0:55 | Same MI null, 36.38%/34.38%, complete validity at the highlighted point. |
| 12 | 1:05 | 0:50 | Power definition, gap colours, fixed nominal rules and method ordering. |
| 14 | 1:15 | 1:00 | Higher returning-visitor estimate, adjusted rejection, unknown population truth. |
| 15 | 1:00 | 0:45 | Limits linked to specific next steps. |

Using all these reductions gives **16:45**. They are a controlled shorter
route, not permission to speak faster or remove the original contribution.
Slides 9 and 13 remain substantial because they carry the key explanation.

### If Slide 13 ends as late as 18:00

Use these brief scripts and still finish before the interruption:

- **Slide 14, about 30 seconds:** “In the shopping application, returning
  visitors have higher estimated month–purchase MI. Both tests reject
  equality after adjustment across six comparisons. The population values
  are unknown, so this illustrates interpretation without validating
  false-positive accuracy.”
- **Slide 15, about 25 seconds:** “The main limits are the first-order
  approximation, errors in the shared estimates, and one controlled
  population family. The next steps are to improve those estimates,
  retain the extra sampling variation near independence, and evaluate
  broader populations.”
- **Slide 16, about 40 seconds:** “I derived MI-specific variance
  sensitivity and used it to calculate degrees of freedom. The larger
  cutoff improves some excessive false-positive rates, while also reducing
  power. The remaining failures identify estimation accuracy as a priority
  in sparse settings. Thank you.”

Do not cut the conclusion or attempt to narrate the backup slides before
questions. Avoid a promise to cover an omitted result later in the talk.
