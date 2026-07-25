# Safety-Net Thesis: Deterministic Saddlepoint Testing for Binary CMI

Status: preserved fallback project

Date frozen: 25 July 2026

## Working Title

*A Deterministic Saddlepoint Significance Test for Sparse Binary Conditional
Mutual Information*

## Research Problem

The standard chi-square approximation for plug-in conditional mutual
information can be poorly calibrated when binary variables are conditioned on
many sparse or skewed states. Permutation testing is more reliable, but it is
computationally expensive when repeated across many hypotheses and has finite
Monte Carlo tail resolution.

The proposed thesis asks:

> Can the exact fixed-margin CGF structure of binary conditional mutual
> information provide permutation-level calibration without resampling when
> many sparse conditioning strata are present?

## Proposed Method

For each conditioning state `z`, summarize the binary 2x2 table using
`(n_z, r_z, s_z, a_z)`. Conditional on the observed margins, the free count
has the exact null:

```text
A_z | n_z, r_z, s_z ~ Hypergeometric(n_z, s_z, r_z).
```

The observed likelihood-ratio statistic is:

```text
G^2 = 2 N CMI_nats = sum_z g_z(A_z).
```

The deterministic test:

1. computes the exact finite-support CGF of each stratum contribution;
2. adds the CGFs using conditional independence;
3. solves the one-dimensional equation `K'(s_hat) = G^2_observed`;
4. applies the Lugannani-Rice upper-tail approximation; and
5. groups identical margin configurations by multiplicity for speed.

This safety-net thesis proposes the factorized saddlepoint test as one method.
Exact convolution, permutation, chi-square, normal, and Edgeworth calculations
are validation baselines, not production routes. The broader exact/saddlepoint
router remains useful experimental infrastructure but is not required in the
clean thesis architecture.

## Intended Regime

- Binary `X` and `Y`
- Discrete `Z` with many informative states
- Sparse or skewed margins within states
- No single stratum dominating total variance
- Aggregate support sufficiently rich that summation smooths severe
  discreteness
- High-throughput testing where repeated permutation is materially expensive

The method does not target ordinary one-table binary MI, very few informative
strata, or highly coarse aggregate support.

## Evidence Already Available

On 13 post-pilot configurations that required the saddlepoint approximation:

| Metric | Result |
|---|---:|
| Mean FPR error at `alpha=0.05` | 0.00063 |
| Maximum FPR error at `alpha=0.05` | 0.00236 |
| Median speedup over 1,000 literal permutations | 63x |
| Approximate median speedup on direct JIDT saddlepoint anchors | 20x |
| Approximate median p-value error on those JIDT anchors | 0.0005 |

The complete implementation passed 33 tests, and the full validation grid had
no invalid p-values, root failures, or monotonicity violations.

## Defensible Contribution

The contribution is not the invention of saddlepoint approximation,
Lugannani-Rice, exact conditional testing, or product-hypergeometric
inference. The defensible contribution is:

- the CMI-specific fixed-margin factorization;
- exact finite-support per-stratum CGFs;
- repeated-component grouping and efficient deterministic evaluation;
- a carefully bounded sparse many-stratum application regime;
- comparison against chi-square and correct blockwise JIDT permutation;
- the JIDT default-null and floating-point tie audits; and
- an open, reproducible validation implementation.

This is best framed as a methods-transfer and algorithm-validation thesis.
Existing conditional saddlepoint theory, especially the current spaCRT work,
must be cited and specialized rather than claimed as new.

## Important Limitations

- `X` and `Y` are binary.
- General `r x c` fixed-margin CGFs are not implemented.
- The test conditions on observed margins.
- Independent observations are assumed.
- Power under alternatives has not been evaluated.
- Temporal dependence and transfer entropy are not yet covered.
- Real-world usefulness has not been demonstrated on an application dataset.
- A dedicated saddlepoint-only confirmation grid has not yet been completed.
- The final novelty claim requires supervisor and citation-chain review.

## Work Needed to Submit This Thesis

1. Define a predeclared applicability regime using informative-stratum count,
   variance concentration, and support diagnostics.
2. Run a larger saddlepoint-only grid with multiple independent seeds.
3. Add conditional alternatives and compare statistical power.
4. Validate one real high-throughput binary-CMI application.
5. Map the construction formally to existing conditional saddlepoint theory.
6. Remove router-centric framing from the main thesis narrative.
7. Complete the focused novelty review and obtain supervisor approval.

## Preserved Artifacts

- Main validation report:
  `SADDLEPOINT_ROUTER_VALIDATION_REPORT.md`
- Novelty boundary:
  `NOVELTY_AUDIT_AND_CLAIM_BOUNDARY.md`
- JIDT source and tie audit:
  `JIDT_CMI_BASELINE_AUDIT.md`
- Full validation:
  `../results/saddlepoint_full_k100000_b1000/`
- Direct JIDT anchors:
  `../results/jidt_blockwise_anchors_b1000_k200000/`
- High-shuffle tie reproduction:
  `../results/jidt_tie_anchor_b100000/`
- Core implementation:
  `../src/sparse_cmi/saddlepoint.py`
- Experimental router:
  `../src/sparse_cmi/routing.py`

## Restart Decision

Return to this project if broader thesis exploration does not identify a
candidate with a better combination of:

- methodological novelty;
- generality;
- practical relevance;
- feasibility within the degree timeline; and
- a clean validation story.

