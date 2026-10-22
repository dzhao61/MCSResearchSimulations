# Adversarial Audit

Date: 25 July 2026

## Overall Finding

No error was found in the retained analytic-bias-corrected Wald formula,
influence variance, weak-null simulation target, or table-level permutation
construction.

Two software issues and one rejected-method stability issue were found and
fixed:

1. fractional table entries were silently truncated to integers;
2. a result field overstated numerical computability as first-order validity;
3. the experimental Lugannani-Rice calculation was unstable extremely close
   to its mean.

None changes the saved calibration conclusions for valid integer tables.

## Formula and Unit Checks

### Manual MI

`plugin_mi` uses natural logarithms and matches hand calculations for:

- an independent `2x2` table, MI `0`;
- a diagonal balanced `2x2` table, MI `ln(2)`; and
- randomized rectangular tables through the JIDT cross-check below.

The influence function agrees with a direct contamination derivative, and
its variance agrees with the full multinomial delta-method quadratic form.
The MI Hessian trace reproduces the leading bias

```text
(r-1)(c-1)/(2n).
```

### JIDT

The local JAR requires:

```python
MutualInformationCalculatorDiscrete(r, c, 0)
```

The two-argument constructor in the original exploratory sketch does not
exist in this JIDT version.

Across 34 fixed and randomized tables:

- maximum manual-versus-JIDT MI error after bits-to-nats conversion:
  `6.11e-16` nats;
- JIDT MI therefore passes the `1e-10` unit gate.

JIDT's no-argument analytic significance method is not the standard
nats-based likelihood-ratio chi-square calculation. Local source inspection
shows that it passes bit-valued MI into `2N*MI` without multiplying by
`ln(2)`. It exactly matches a SciPy reconstruction of that bits convention,
to `5.03e-17`, but differs from standard chi-square p-values by as much as
`0.0780` in this audit.

Consequences:

- use `MI_bits * ln(2)` before forming standard `G=2N*MI_nats`;
- do not use JIDT's built-in analytic p-value as the standard chi-square
  baseline;
- JIDT's shuffled significance remains a separate empirical procedure.

## Permutation Check

For pooled cell counts `C` and a fixed group-one size `n`, the table-level
draw

```text
T_P ~ multivariate hypergeometric(C, n)
```

has exactly the same probability as choosing `n` individual labels uniformly
and recounting cells. A small exhaustive example verifies the multiplicities
exactly.

The implementation:

- conditions on pooled counts;
- preserves both sample sizes;
- recomputes MI in every permuted table;
- recomputes each permuted standard error for studentized tests; and
- uses the conservative Monte Carlo correction `(extreme+1)/(B+1)`.

## Invariance and Input Checks

Automated tests now cover:

- row and column category relabeling;
- swapping the two sample groups;
- signed-difference reversal under group swap;
- equal two-sided p-values under group swap;
- exact CGF/Wald first-two-cumulant agreement;
- fractional, nonfinite, complex, negative, mismatched, and one-category
  inputs;
- invalid confidence levels and permutation counts; and
- explicit behavior when the empirical standard error is zero.

The full suite passes `21/21`, and every source and experiment script compiles.

## Simulation Integrity

The retained evidence comprises:

- 144 randomized weak-null scenarios over two independent scenario seeds;
- 432,000 table-pair comparisons;
- exact equal population MI with otherwise different probability tables;
- square and rectangular shapes from `2x2` through `20x20`;
- sample-size ratios through `1:4`;
- balanced-like through strongly heterogeneous margins;
- separate strong-null controls;
- pre-selected permutation anchors; and
- post-hoc hard cases labeled separately.

Analytic Wald remains stable across the independent scenario seeds and strong
null. The catastrophic uncorrected-Wald behavior is explained by unequal
leading bias, not by a units error.

## Experimental Saddlepoint Audit

The influence-saddlepoint candidate was stable in rejection tails but had
Lugannani-Rice cancellation near its mean. The default normal-fallback region
was changed post hoc from standardized distance `1e-4` to `0.01`, and the
observed failure was added as a regression test.

This patch changes no 5% decision in the 288,000-row refinement run. The
candidate still fails its pre-specified improvement criterion and remains
rejected.

## Real-Data Scope Check

The AIMS manuscript repository directly motivates MI-difference inference,
but its native position-pair tables have 21 amino-acid/gap states and are
often sparse at the available sample sizes. They are not a clean demonstration
of the frozen regular method without additional category modeling.

The pre-specified UCI Adult case instead produces aligned `16x2` tables with:

- no expected count below 1;
- 3.125% of female expected counts and 0% of male expected counts below 5;
- positive influence variances; and
- MI values away from zero.

It is therefore a more honest first case study. One female table has two
observed zero cells, so positive population support remains an assumption,
not an observed fact.

## Residual Risks

The following are limitations, not fixed bugs:

- no observable diagnostic currently proves that a table is in the
  first-order regular regime;
- the method excludes exact and near independence;
- positive population support cannot be verified from finite samples;
- rows are assumed independent and identically distributed;
- the analytic correction uses declared full dimensions;
- fixed-alphabet simulations do not establish growing-alphabet validity;
- the UCI case study is unweighted and descriptive; and
- the current ingredients are largely established prior art.

These boundaries must remain visible in any thesis proposal.

## Reproduction

```bash
.venv/bin/python -m unittest discover -s DifferentialMI/tests -v

.venv/bin/python DifferentialMI/experiments/audit_jidt_units.py \
  --output-dir DifferentialMI/results/jidt_unit_audit

.venv/bin/python DifferentialMI/experiments/run_adult_case_study.py \
  --output-dir DifferentialMI/results/adult_case_study
```

