# Documentation

## Current Reading Path

1. [`SUMMARY.md`](SUMMARY.md) presents the full research story from first
   principles.
2. [`EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md)
   is the main derivation, mapping the generic Welch-Satterthwaite weights,
   variances, and component degrees of freedom to their MI counterparts.
3. [`INDEPENDENCE_REFERENCE_DISTRIBUTION.md`](INDEPENDENCE_REFERENCE_DISTRIBUTION.md)
   derives what happens when a distribution is compared with an independent
   reference having the same marginals, including the first-order degeneracy
   and resulting chi-squared limit.
4. [`MI_TAYLOR_EXPANSION.md`](MI_TAYLOR_EXPANSION.md) derives the second-order
   Taylor expansion of MI at independence term by term and records the
   preferred presentation style for future Taylor derivations.
5. [`../derivation/main.pdf`](../derivation/main.pdf) is the formatted
   textbook-style PDF; [`../derivation/main.tex`](../derivation/main.tex) is
   its generated LaTeX source.

## Historical Record

The [`history/`](history/) directory preserves earlier decision documents:

- [`../archive/ORIGINAL_EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md`](../archive/ORIGINAL_EXPANDED_WELCH_SATTERTHWAITE_DERIVATION.md)
  preserves the original expanded-method derivation.
- [`../archive/QUICK_SUMMARY.md`](../archive/QUICK_SUMMARY.md) preserves the
  earlier abbreviated summary.
- [`VALIDATION_PROTOCOL.md`](history/VALIDATION_PROTOCOL.md) records the
  original frozen validation rules.
- [`FINAL_ASSESSMENT.md`](history/FINAL_ASSESSMENT.md) records the conclusion
  from the earlier decisive experiment.
- [`LITERATURE_AND_TECHNICAL_AUDIT_2026-08-03.md`](history/LITERATURE_AND_TECHNICAL_AUDIT_2026-08-03.md)
  records the literature and technical audit that motivated the expanded
  variance-influence method.
- [`../archive/custom_welch/`](../archive/custom_welch/) preserves the
  discontinued routing-method study and its complete evidence.

The historical documents are retained for provenance. The current summary
and primary evidence are the three documents above and
[`results/supervisor_full/REPORT.md`](../results/supervisor_full/REPORT.md).
