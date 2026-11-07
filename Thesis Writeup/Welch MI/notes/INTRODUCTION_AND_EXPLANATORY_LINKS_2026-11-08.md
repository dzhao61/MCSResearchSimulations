# Introduction and explanatory links: 8 November 2026

Implemented the agreed introduction expansion and six targeted prose revisions.

- Chapter 1 explains partial information, independence and MI magnitude before
  introducing the comparison between populations.
- Section 2.1.1 connects entropy to MI before defining information content.
  The previous post-equation interpretation and its Shannon citation were moved
  into this opening rather than repeated.
- Section 2.2 uses population independence to explain how nonnegative plug-in
  estimates can have upward bias, retaining the conditions on the subsequent
  leading-bias expansion.
- Section 6.1.1 states the purpose of the linear-remainder diagnostic before
  its findings. The covariance qualification and Appendix B.4 reference remain;
  the full decomposition is still given in the appendix.
- Section 6.1.3 introduces the near-independence model before Figure 6.3 and
  explains the mean and variance scalings explicitly at independence. The
  pointwise-MI variance approximation was moved before the figure, and its
  previous introductory repetition after the figure was absorbed there.
- Section 6.4 interprets the month result as greater information about purchase
  outcomes among returning visitors, without a causal or purchase-frequency claim.
- Section 6.5 distinguishes the degrees-of-freedom approximation from the
  standard error used in the observed statistic.

Reviewed the revised passages in context for sentence connections and Australian
English. Before building, verified unchanged displayed equations, tables,
figures, citation keys, labels and reference targets. Section 2.3 remained
byte-identical, as did the appendices and the experimental inputs.

Rebuilt with `package_deliverables.py --no-push`. The final LaTeX log has no
warnings, overfull boxes or underfull boxes. The PDF remains 109 pages.
Visually reviewed all 19 pages affected by text or reflow: physical PDF pages
5, 10, 11, 13–20, 60, 61, 63–66, 83 and 84. The source archive was refreshed
and checked; the unchanged experiment supplement was verified and reused.

The main and named delivery PDFs match. The signed PDF in `FINAL SUBMISSION`
was preserved and does not contain these latest revisions.
