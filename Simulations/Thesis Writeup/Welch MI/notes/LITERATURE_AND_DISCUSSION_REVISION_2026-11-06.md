# Literature and discussion revision, 6 November 2026

The user requested that the initial literature and discussion additions be
undone and reconsidered carefully. The separately authorised ordinary Welch
subsection was retained. The literature additions and Chapter 6 discussion
were removed before replacement drafting; no archived files were changed.

## Reading and editorial decisions

Reread the existing estimation review and comparison literature in Chapter 2,
the moment-matching construction and its qualifications in Chapter 4, the
evaluation design in Chapter 5, the approximation, null and power findings
in Chapter 6, and the conclusions and limitations in Chapter 7.

Revisited the supplied samples: Jones's literature summary and discussions
of observation length, model comparison and alignment with literature;
Fang's Section 5.4; and Yan's method comparison and conclusions. The useful
pattern was a specific finding connected to a published result or mechanism,
followed by its implication. The new section follows that progression,
without adopting the samples' broader claims or stylistic flourishes.

On the user's subsequent clarification, the Discussion opening was refocused
on Normal Wald as the main benchmark. Ordinary Welch remains confined to
its short supporting subsection and the benchmark-scope statement in the
conclusion; it does not lead the synthesis of the thesis findings.

The previous draft repeated the existing summaries of Bayesian inference,
bootstrap and permutation testing. Those paragraphs were not restored.
Instead, the existing regression paragraph and contribution synthesis in
Chapter 2 were revised. Chapter 6 gains three discussion paragraphs that
connect the evidence and literature without another catalogue of results.

## Sources checked against the claims

- [Pan and Wall (2002), abstract](https://pubmed.ncbi.nlm.nih.gov/12185894/):
  approximate Student t and F references account for variability of a sandwich
  variance estimate and reduce Wald rejection. This motivates investigating
  the same principle for MI, without asserting accurate calibration for MI.
- [Bell and McCaffrey (2002), Sections 4 and 6](https://www150.statcan.gc.ca/n1/pub/12-001-x/2002002/article/9058-eng.pdf):
  variance bias reduction and Satterthwaite degrees of freedom each affect
  inference. Their jackknife comparisons show that positive variance bias
  combined with Satterthwaite degrees of freedom can produce conservative
  tests. This is the specific precedent used to interpret MI conservatism.
- [Paninski (2003), abstract and introduction](https://www.cns.nyu.edu/pub/lcv/paninski-infoEst-2003.pdf):
  bias can persist after common corrections and invalidate standard error
  assessments. The discussion connects that concern to the thesis's measured
  difference bias and incorrect estimated direction; it does not attribute
  the thesis's two-population experiment to Paninski.

Existing bibliography entries suffice. No new method, estimator or claim of
superiority to resampling procedures was introduced.

## Checks and scope

- Recomputed the ordinary Welch comparison from the saved 100,000 pairs at
  each of three null settings. Record loading verifies chunk checksums.
  Verified rejection decisions using both p-values and critical values.
- All three benchmark methods are valid in every repetition at those settings.
  Rates remain 8.35/7.35/4.90, 4.87/4.57/3.24, and
  26.01/25.95/24.84 percent for Wald/ordinary Welch/Expanded Welch.
- The discussion's 1.93 variance ratio refers to the same-skew 16-by-16
  diagnostic at common MI 0.02 and n = 1,000. It compares average squared
  standard error with the observed variance of the difference. An enlarged
  mean of V-hat relative to V alone is not treated as proof of this ratio.
- Chapter 7's benchmark limitation now acknowledges the three ordinary
  Welch cases. Other conclusion prose remains unchanged.
- Checked citations, labels, references, nested LaTeX environments, Australian
  spelling and paragraph style. All pre-existing displayed equations and
  Section 2.3 remain unchanged.

The source revision was initially completed without rebuilding. On the
user's subsequent request, the thesis was rebuilt on 6 November 2026
(102 pages). The final log has no warnings, unresolved references or
overfull/underfull boxes. The revised literature, comparison and discussion
pages were rendered and inspected. Repeated wording in Section 2.5 was
shortened so the chapter no longer ends with a nearly empty page.
The named PDF and source archive were refreshed and verified against the
final inputs. The existing experiment supplement was reused after checking
its inventory, file sizes, modification times and archive checksum.

## Follow-up flow edits

Applied the three subsequently agreed Chapter 6 edits: removed the power
transition that preceded the ordinary Welch subsection, placed its common MI,
sample sizes, repetition count and validity statement before the table, and
removed the closing near-independence sentence from the second Discussion
paragraph. The near-independence findings remain in the dedicated results
section and conclusion. Table values and statistical qualifications are
unchanged. The rebuilt comparison and Discussion pages were inspected,
and the final LaTeX log remains free of warnings and unresolved references.
