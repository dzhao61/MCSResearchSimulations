# First-reader revision plan and implementation record — 27 October 2026

Status: source revision and the explicitly requested PDF build completed on 28 October 2026. The user authorised planning and implementation of the first-reader review. This includes the narrow N02 explanation in Section 2.3; preserve all of that section's derivation equations and steps. The PDF and delivery refresh remain deferred until explicitly requested.

## Scope and scientific invariants

Address N01–N11 in FIRST_READER_REVIEW_2026-10-27.md and the smaller prerequisite issues recorded there. Reconcile overlapping recommendations with the earlier language review; do not mechanically apply its unrelated optional copyedits. Preserve the current abstract, Chapter 1's research scope, Section 5.1's construction, the worked example, all observed numerical results, citations, figure sizes, plot values and shared benchmark denominators. Preserve all historical sources and archives. No experiment, fitting or bootstrap rerun is required.

The source snapshot is `archive/before_first_reader_edits_2026-10-27.zip`. The baseline manifest records source hashes, result-summary hashes, protected PDF hashes and delivery-file sizes/mtimes. Internal notes are outside the manuscript.

## 1. Establish the needed vocabulary (N01, N02 and small prerequisites)

- Section 2.2: define bias as the sampling mean minus population MI; express its link to an estimator's centre. Replace “positive support” with positive cell probabilities. Explain the O(n^-2) remainder beside its first use without claiming a finite-sample bound uniform over tables.
- Section 2.3: add only a short connection after the centred first-order error: its zero mean applies to the linear part; higher-order terms give the bias already discussed. Leave all algebra, equations, assumptions and citations unchanged.
- Section 2.4: identify degrees of freedom as the positive Student t shape parameter, including noninteger effective values. Name mean and variance before calling them moments; identify Shannon diversity as entropy.
- Sections 2.4 and 3.2–3.3: make clear that a standard error estimates a sampling standard deviation, and explain both symmetric tails in the normal p-value. Keep the reference distribution under H0 explicit.

Acceptance: a reader can explain bias, sampling variance, standard error and the two-sided p-value without supplying prior inference terminology. No glossary is added to the abstract.

## 2. Establish the uncertainty hierarchy and reason for the derivation (N03–N05)

- Section 3.2: explain how V(P), V-hat(P), V-hat(P)/n and Var(V-hat(P)) relate. Move the useful quantity table from Chapter 6 to this point, after the shared standard error is defined. Include the estimated difference's sampling variance, so the objects are defined before the reader studies their variability.
- Section 2.4: replace the “assessment of spread itself” wording with named objects. Do not repeat the entire relocated table.
- Section 4.1: explain the normal/independent scaled chi-squared construction behind a Student t distribution before using moment matching. Distinguish this standard distributional identity from the approximation used for MI. Preserve the mean/variance matching algebra.
- Section 4.2: state why the one-cell direction represents an observation's contribution to sample-table error. Keep the full averaging identity and proof in 4.3.
- Keep g(P) as the observation-level variance sensitivity and tau-squared(P) as its variance. Remove the late naming drift in 4.5.

Acceptance: the reader can state why uncertainty in a variance estimate affects the cutoff and why the perturbation calculation answers a sampling question.

## 3. Give the three component degrees-of-freedom quantities stable identities (N06)

Use these three scientifically distinct names throughout the active manuscript:

| Quantity | Meaning | Inputs |
| --- | --- | --- |
| nu(P,mom) | Component sampling-moment target | Actual mean and variance of V-hat(P) at fixed P and n |
| nu(P,FO) | Population first-order approximation to that target | Population V(P), tau-squared(P), n |
| nu-hat(P) | Component estimate used by the test | One observed count table |

- In 4.1 use nu(P,mom) throughout the scaled chi-squared matching calculation.
- In 4.3 define nu(P,FO) explicitly by 2nV-squared/tau-squared. Explain the approximation to nu(P,mom), then define the empirical estimate as before. A compact table distinguishes the inputs and which quantity varies between repetitions.
- Keep nu(P), nu(Q) only as generic inputs to the general combination equation, explicitly identified as such. They must no longer also denote the population first-order value elsewhere.
- Explain that rescaling V-hat by fixed n preserves its moment-matched degrees of freedom. Explain once that averaging the nonlinear empirical estimate need not yield the target defined from sampling moments.
- Propagate the distinct labels through 5.2, 6.1, 7.1, Appendix A and Appendix B. Use a subscript “mom” consistently rather than alternating superscript and subscript.
- Update the component-ratio plot's population numerator to nu(FO), and the affected generated table headers and reporter templates. Regenerate only the affected figure from existing saved summaries, without rebuilding the thesis or changing plot values, dimensions, ratios or limits.

Acceptance: each degrees-of-freedom symbol has one role across the derivation, experiment and results. The component plot and table use those same roles. The test's calculations are unchanged.

## 4. Explain the limits of the approximation at the point of interpretation (N07, N10)

- In 4.5 connect vanishing pointwise-MI weights in the linear error to the surviving quadratic cell errors. Keep the full local-alternative theorem in Appendix A.
- In 6.1.3 give the plain mechanism before the plot: even nearly independent populations produce noisy empirical association. Explain the three plotted degrees-of-freedom roles using their stable names, rather than adding another glossary.
- Connect 6.1 to 6.2: RQ1 checks the moments used to choose degrees of freedom; RQ2 additionally compares the shared squared standard error against the actual finite-sample variance of the estimated difference. Explicitly note that V(P)/n is itself an approximation, so error relative to V(P) does not settle standard-error accuracy.
- In the conclusion preserve the squared-mean mechanism and use the same quantity names. Avoid implying that substituting sample proportions always makes approximation error worse.

Acceptance: the reader can reconcile an inflated V-hat relative to V with an underestimated standard error relative to the actual difference variance, and can understand the near-independence graph's mechanism without deriving the appendix theorem.

## 5. Clarify calibration, simulation precision and performance interpretation (N08, N09, N11)

- In 4.3 state the nested rejection relationship at a common p-value threshold.
- In 5.4 explain that the methods rank complete simulated datasets by evidence against equal MI. Separate thresholds after calibration remove the earlier nesting implication; changing estimated degrees of freedom can change their ranking. In 6.3.2 connect that fact explicitly to the observed power reversal.
- State once that calibration uses known equal-MI simulation settings for the power comparison. The application uses the nominal test. Keep the independent fitting/validation/alternative sequence and lower/upper-null example intact.
- Use “calibration setting” for a specification of both P and Q, reserving individual-population wording for P and Q separately. Propagate through the design, results, conclusion and appendices.
- In 5.5 explain that more repetitions improve precision of reported rates without increasing the sample size within any test.
- In 5.3 motivate the nominal 5% target alongside power: a never-reject rule has zero false positives and zero power. In 6.2 describe closeness to 5% as calibration under the stated criterion. A conservative test is not invalid solely because its rate is below 5%.
- Beside the validity panels explain that failed calculations also reduce the all-repetition rejection rate. Preserve all inclusion rules, validity thresholds and rates.

Acceptance: the reader can explain why calibrated power can reverse the nominal comparison, why a lower false-positive rate does not alone establish better testing, and why 100,000 repetitions do not cure a small-n test.

## 6. Resolve the appendix and label dependencies

- Appendix A: keep technical derivations; align nu labels and identify G moments as properties of its chi-squared approximation.
- Appendix B: identify the function differentiated by the joint delta method and its two derivative coefficients, connecting to the existing Taylor method without restoring a long removed derivation. Describe zero-component exclusion as the operational componentwise validity rule; retain the explicit fact that a simplified combined expression may remain defined. Do not invent a mathematical necessity or alter eligibility.
- Appendix C: identify a proposed 9/n correction as applying to V-hat, not the MI point estimate. Name the centred-magnitude and signed-correlation statistics precisely where discussed.
- Replace “Setting: SD” with “Setting, h” in the three included calibration tables and their generator. Name upper-null MI and its units. Preserve all numeric cells.
- Make only directly connected wording repairs from the earlier review; leave unrelated stylistic preferences for a separate pass.

## 7. Verification and final reading pass

1. Review the diff in connected passages and trace each N01–N11 issue to its repair.
2. Audit every active nu(P)/nu(Q), FO and mom occurrence, the meaning of tau-squared, calibration terminology and first-use definitions. Check table/plot labels against prose.
3. Check source references, labels, citations, LaTeX braces/environments and the flush-left paragraph policy without compiling.
4. Compare retained mathematics with the snapshot: equation changes are limited to explicit role labels, exact definitions of the named first-order approximation, and short explanatory identities. Confirm all experimental numbers and table numeric cells remain unchanged.
5. Run the existing manuscript-consistency and ratio-display tests appropriate to the changed labels/plot; confirm the plotted numerical series and inclusion rules remain unchanged. No tests that merely mirror prose are needed.
6. Re-read Chapters 2–6 in their revised sequence, then the conclusion/appendix dependencies. Remove duplicate explanations and check that a bridge does not introduce new undefined notation.
7. Verify result-summary hashes and protected PDF/delivery state against the baseline. Record checks, word-count effect and any remaining layout checks. Mark pending_source_rebuild true without publishing or refreshing delivery packages.

Completion requires source edits and the source-level checks above. PDF layout and page count can be checked only at the next explicitly requested build; do not present the current delivered PDF as containing these source revisions.

## Completion record

Completed on 28 October 2026. All eleven first-reader issues have source-level repairs and their dependencies have been checked. The original research questions, experiment, estimators, eligibility rules and numerical findings are preserved. The current abstract was retained.

| Issue | Revised locations | Implemented repair |
| --- | --- | --- |
| N01 | [2.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:123>), [3.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:143>) and [3.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:207>) | Defined bias and the standard error; explained the two symmetric p-value tails and the implemented nominal p ≤ 0.05 rule. |
| N02 | [2.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:418>) | Connected the zero-mean linear approximation to bias generated by omitted higher-order terms. All displayed algebra is byte-identical. |
| N03 | [3.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/03_problem_baselines.tex:151>), [2.4](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/02_background_literature.tex:584>) | Moved and extended the existing variance table to the point where the standard error is defined. Distinguished V, V-hat, V-hat/n, Var(V-hat), SE-squared and Var(Delta-hat); corrected tau-squared naming in 4.5. |
| N04 | [4.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:39>) | Added the normal/independent chi-squared construction of a Student t variable, with its exact conditions distinguished from the MI approximation. Defined the moment target before its first use. |
| N05 | [4.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:126>) | Explained why the one-cell direction represents an observation’s contribution before differentiating. Kept the full empirical-table averaging argument in 4.3. |
| N06 | [4.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:522>), [5.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:200>) | Used stable mom, FO and sampled-estimate labels; explained fixed-scale invariance and why averaging a nonlinear sample-based estimate need not recover the moment target. Updated the plot label, table header and generators. |
| N07 | [4.5](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/04_expanded_welch.tex:698>) and [6.1.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:161>) | Explained vanishing linear weights and surviving quadratic cell errors before interpreting the curves. Kept the technical local-alternative derivation in Appendix A. |
| N08 | [5.4](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:351>) and [6.3.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:453>) | Connected nominal nesting to a common threshold, explained separate calibrated thresholds and dataset ranking, and clarified that the fitted thresholds concern known simulation settings. Used calibration-setting terminology throughout. |
| N09 | [5.5](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:404>) | Distinguished Monte Carlo repetition count from observations within each test. |
| N10 | [6.2.2](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:287>) | Explained the change from the RQ1 moment benchmarks to actual finite-sample variance of the MI difference, where the standard-error diagnostic is introduced. Stated why an inflated V-hat relative to V can coexist with an underestimated standard error. |
| N11 | [5.3](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/05_experimental_design.tex:264>) and [6.2.1](</Users/danielzhao/MyMac/Masters Degree/Research/Simulations/Thesis Writeup/Welch MI/chapters_rewrite/06_results.tex:261>) | Motivated closeness to the nominal 5% target alongside power and explained how failed calculations can reduce the all-repetition rejection rate. Preserved every inclusion/validity rule. |

The smaller prerequisite issues were also addressed: positive support, the first O(n^-2) remainder, Shannon diversity/entropy, moment terminology, the three calibration tables’ h labels, the function and derivatives used in the appendix delta method, the operational reason for rejecting undefined component degrees of freedom, the target of a proposed 9/n correction, and the distinction between signed Pearson correlation and centred-magnitude rank correlation. Appendix A’s G moments are explicitly properties of the approximating chi-squared distribution.

The final reading pass kept the results sequence as overall false-positive patterns followed by their diagnostics; the full benchmark explanation sits where the diagnostic is first used. Calibration motivation precedes fitting, validation and results, followed by sensitivity to the lower/upper equal-MI setting. Repeated explanations were shortened where the new connections made them unnecessary. Numerical evidence supports the clarified description of B’s power curve; no claim is made that the diagnostics isolate each error’s causal contribution.

### Completed checks

- 5 existing manuscript-consistency tests and 7 existing ratio/display tests passed.
- All 31 active TeX inputs passed brace, environment, math-delimiter, label and reference checks: 157 unique labels and 173 references.
- Every original displayed mathematical block is retained, allowing only the explicit component-role names and the equality defining the named first-order value. The one added display is the standard Student t construction. Section 2.3’s displayed derivation, the complete worked example and Section 5.1 are byte-identical to the snapshot. Citations are preserved.
- Numerical rows in all 13 included generated tables are byte-identical. All three calibration tables reproduce exactly from saved summaries using their updated generator.
- The updated component-degrees-of-freedom figure was rendered and inspected. Its size, x/y series, uncertainty-band coordinates, axis limits and common scales are identical; only the population numerator’s label changes to nu(FO). Both rows remain readable.
- The paragraph-style guard and git diff whitespace check passed. All body paragraphs retain the global flush-left policy.
- All 7,381 saved result-summary hashes match the baseline. No simulation, fitting or bootstrap was run.
- All ten protected current PDF/delivery files retain their sizes and mtimes; all smaller files, including the main and named delivery PDFs, also retain their SHA-256 hashes. No LaTeX or delivery-publication command was run.

Whitespace-delimited source words across the ten chapters/appendices changed from 19,511 to 20,392, an increase of 881 (4.5%). This count includes mathematics and table text. Most new explanation is in Chapter 4; the variance table was moved rather than duplicated. It is not a prediction of the eventual page count.

At the source-only handoff, typeset layout, page breaks, equation/table fit and delivery consistency were deferred. The subsequent requested build completed these checks and refreshed the delivered PDF; see the build record below.

Detailed machine-readable results: [FIRST_READER_REVISION_CHECKS_2026-10-28.json](FIRST_READER_REVISION_CHECKS_2026-10-28.json).

## Subsequent requested PDF build

The user requested the build after source completion. The 99-page main PDF and all delivery packages are now current. Formatting, references, paragraph consistency and the independently rebuilt source archive passed review. The only final source adjustment was ragged-right text columns in Table 4.1.

[Build and formatting record](FIRST_READER_PDF_BUILD_2026-10-28.md).
