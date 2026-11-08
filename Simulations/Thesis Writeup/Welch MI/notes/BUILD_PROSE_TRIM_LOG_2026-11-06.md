# Log of prose trimmed during the PDF build — 6 November 2026

## Scope and provenance

This records the net prose changes made specifically to shorten Section 2.5,
“Previous work and this thesis’s contribution”, during the first PDF build
requested after the literature and Discussion revisions. These pagination
edits preceded the three later flow fixes that the user explicitly approved.

The **before** text below is reconstructed from the edit commands and source
excerpts recorded in this conversation. It was not saved as a separate Git
commit. The **after** text is verified against the shortened source in commit
`b0f7d96`. Source line wrapping is retained for readability; it has no effect
on the manuscript’s wording.

The comparison is against the revised Section 2.5 immediately before that
build, not against the earlier 100-page thesis. The build initially produced
103 pages. The final version had 102 pages after the text fitted without the
nearly empty overflow page. This page-count change was not produced by
changing typography or removing an experiment.

## Itemised build-time changes

1. **Combined the first two sentences.** “Existing work provides the leading
   bias and sampling variance of MI” and “These results support a standard
   error for the difference between two independent MI estimates” became one
   sentence using “supporting”. The four citations now follow the combined
   sentence rather than the first sentence alone.

2. **Removed an explicit distinction in the following sentence.** Deleted
   “They describe variation in the MI estimate, whereas choosing”. The
   remaining sentence now begins “Welch--Satterthwaite degrees of freedom
   additionally require …”. The mean and variance required for moment matching
   remain stated, but the contrast with variation of the MI estimate is less
   explicit here.

3. **Shortened the Hutcheson comparison.** Removed both “provides a precedent
   for comparing information quantities” and the explicit qualification that
   its sample-size-based degrees of freedom “do not account for how estimated
   pointwise MI changes with the observed table”. The replacement states only
   that Hutcheson’s entropy test uses a Student t distribution with degrees
   of freedom based on sample sizes. Section 2.4 still explains the MI-specific
   dependence, but this explicit comparison was removed from Section 2.5.

4. **Shortened and reorganised the end of the contribution paragraph.** Removed
   “The contribution is this calculation for MI, which supplies the inputs to
   the existing Welch--Satterthwaite combining rule.” The final wording instead
   states the sequence: obtain component degrees of freedom from the sampling
   variability approximation, then combine them using the Welch--Satterthwaite
   rule. The opening two sentences of this paragraph were retained.

5. **Compressed the sentence about holding the statistic fixed.** “Holding
   Normal Wald’s MI difference and standard error fixed allows the experiments
   to isolate the effect of this reference-distribution change” became
   “Retaining Normal Wald’s estimated MI difference and standard error isolates
   the effect of changing the reference distribution.”

6. **Deleted the explicit residual-error explanation and its local citation.**
   Removed: “The estimation problems identified by Paninski (2003) remain
   relevant: residual bias can shift the estimated difference, while an
   inaccurate standard error can distort its standardisation.” Those mechanisms
   remain discussed elsewhere, including Section 2.4 and the new Discussion,
   but this was a deletion of explanatory content from Section 2.5.

7. **Shortened the closing evaluation sentence.** “The evaluation therefore
   checks the variance-moment approximations separately from false-positive
   rates and power” became “The experiments evaluate the variance-moment
   approximations alongside false-positive rates and power.” This removes the
   explicit “separately from” wording; the distinct approximation and test
   evaluations themselves were not changed.

## Section 2.5 immediately before the build-time trimming

```latex
\section{Previous work and this thesis's contribution}

Existing work provides the leading bias and sampling variance of MI
\citep{miller1955,moddemeijer1989,brillinger2004,paninski2003}.
These results support a standard error for the difference between two
independent MI estimates. They describe variation in the MI estimate,
whereas choosing Welch--Satterthwaite degrees of freedom additionally
requires the sampling mean and variance of the variance estimate itself.
Hutcheson's entropy test provides a precedent for comparing information
quantities using a Student \(t\) distribution, but its sample-size-based
degrees of freedom do not account for how estimated pointwise MI changes
with the observed table \citep{hutcheson1970}.

This thesis follows the variance-moment approach used in regression by
\citet{panwall2002} and derives its MI-specific inputs. Changing a cell
count changes both its probability weight and the pointwise-MI values
calculated from the joint and marginal probabilities. Tracking these
changes gives a first-order approximation to the sampling variability of
the estimated pointwise-MI variance, which supplies the component degrees
of freedom for Expanded Welch. The contribution is this calculation for
MI, which supplies the inputs to the existing Welch--Satterthwaite
combining rule.

Holding Normal Wald's MI difference and standard error fixed allows the
experiments to isolate the effect of this reference-distribution change.
The estimation problems identified by \citet{paninski2003} remain relevant:
residual bias can shift the estimated difference, while an inaccurate
standard error can distort its standardisation. The evaluation therefore
checks the variance-moment approximations separately from false-positive
rates and power.
```

## Section 2.5 after the build-time trimming

```latex
\section{Previous work and this thesis's contribution}

Existing work provides the leading bias and sampling variance of MI,
supporting a standard error for the difference between two independent
MI estimates
\citep{miller1955,moddemeijer1989,brillinger2004,paninski2003}.
Welch--Satterthwaite degrees of freedom additionally require the sampling
mean and variance of the variance estimate itself. Hutcheson's entropy
test uses a Student \(t\) distribution with degrees of freedom based on
sample sizes \citep{hutcheson1970}.

This thesis follows the variance-moment approach used in regression by
\citet{panwall2002} and derives its MI-specific inputs. Changing a cell
count changes both its probability weight and the pointwise-MI values
calculated from the joint and marginal probabilities. Tracking these
changes gives a first-order approximation to the sampling variability of
the estimated pointwise-MI variance. Expanded Welch uses this approximation
to obtain component degrees of freedom, then combines them using the
Welch--Satterthwaite rule.

Retaining Normal Wald's estimated MI difference and standard error isolates
the effect of changing the reference distribution. The experiments evaluate
the variance-moment approximations alongside false-positive rates and power.
```

## Later deletions explicitly approved in the three-point flow plan

These were separate from the build-time trimming above:

- **Before the ordinary Welch subsection:** deleted “The power comparison
  measures the accompanying reduction in detection probability.” Section 6.3
  already introduces the power study.
- **At the end of the second Discussion paragraph:** deleted “Near independence,
  sampling-induced association also enters the estimated degrees of freedom,
  while the population first-order approximation misses quadratic variation.”
  The dedicated near-independence results and conclusion retain this finding.
- **The remaining flow fix moved and lightly rephrased text:** the common MI,
  equal sample sizes, 100,000 sampled pairs and all-valid statement moved from
  after the ordinary Welch table to before it. None of those conditions was
  removed.

The build-time changes were additional editorial changes during a build
request. Describing them only as “trimming repeated wording” did not adequately
identify the removed explanations. This log records the changes without making
any further manuscript edits or rebuilding or pushing any files.

## Subsequent selective restoration

The user subsequently authorised restoring the explanations affected by
items 2, 3, 6 and 7 while retaining the wording improvements in items 1, 4
and 5. Section 2.5 now again distinguishes MI-estimate variation from
variance-estimate variation, explains the limitation of assigning MI degrees
of freedom from sample sizes, states the residual-bias and standard-error
concerns, and explicitly distinguishes approximation checks from test
performance. The three approved Chapter 6 flow fixes remain unchanged.
This restoration initially updated the source only. Following the user's
explicit request to rebuild and push, the thesis was rebuilt to 103 pages.
The restored passages were checked in the rendered PDF, the final LaTeX log
had no warnings or unresolved references, and manuscript source hashes were
unchanged by the build. The named PDF, source archive and checksums were
refreshed and verified; the unchanged experiment supplement was retained.
