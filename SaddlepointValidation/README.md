# Saddlepoint MI Validation

This folder tests the exact conditional-CGF saddlepoint method described in
`mi_saddlepoint_paper.pdf` and `MI_TE_significance_testing_handoff.docx`.

It also contains the newer empirical fixed-margin table-sampling method, which is
currently the most promising general replacement candidate for JIDT shuffling in
large-`N`, skewed, large-alphabet MI significance tests. Start here for that method:

```text
SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_CURRENT_HANDOFF.md
```

Detailed method notes are here:

```text
SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_METHOD.md
```

The routed-test roadmap is here:

```text
SaddlepointValidation/ROUTED_MI_SIGNIFICANCE_ROADMAP.md
```

Core verification checks for the fixed-margin tier and JIDT conventions are here:

```text
SaddlepointValidation/fixed_margin_tier_checks.py
```

The adversarial audit for that method is here:

```text
SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_ADVERSARIAL_AUDIT.md
```

The distinction between standard likelihood-ratio chi-square and JIDT's built-in
analytic significance method is documented here:

```text
SaddlepointValidation/CHI_SQUARE_ANALYTIC_AUDIT.md
```

The source-level audit of JIDT's discrete MI shuffle implementation is here:

```text
SaddlepointValidation/JIDT_IMPLEMENTATION_AUDIT.md
```

The implemented method targets the same fixed-margin null distribution sampled by
JIDT's permutation/shuffling significance test:

1. Build the exact conditional cumulant-generating function for `G = 2N * MI`.
2. Use exact conditional tails when the fixed-margin support is small.
3. Otherwise use Lugannani-Rice saddlepoint inversion for upper-tail p-values.

The validation runner compares:

- `saddle_p`: the tiered exact/saddlepoint p-value.
- `chi2_nominal_p`: the standard asymptotic chi-squared p-value using configured alphabet sizes.
- `chi2_dynamic_p`: chi-squared using observed nonempty rows and columns.
- `jidt_p`: JIDT's default shuffle/permutation p-value from `computeSignificance`.

## Run

Run correctness checks first:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/validation_checks.py
```

From the simulations workspace:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/run_validation.py --profile quick --output-dir SaddlepointValidation/outputs/quick
```

The default standard run is:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/run_validation.py --profile standard --output-dir SaddlepointValidation/outputs/standard
```

The interactive focused calibration run is:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/run_validation.py --profile focused --replicates 1000 --jidt-replicates 100 --shuffles 5000 --output-dir SaddlepointValidation/outputs/focused_hardened
```

For a heavier sweep:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/run_validation.py --profile robust --replicates 50 --jidt-replicates 20 --shuffles 2000 --output-dir SaddlepointValidation/outputs/robust
```

For no-JIDT calibration screens, use multiple worker processes:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/run_validation.py --profile robust --replicates 50 --jidt-replicates 0 --workers 4 --output-dir SaddlepointValidation/outputs/robust_no_jidt
```

Each completed configuration writes `checkpoints/<config>.csv` plus a combined
`saddlepoint_validation_results.partial.csv`. Restart interrupted runs with `--resume`.
If JIDT replicates are enabled, the runner stays serial by default to avoid unmanaged
multi-JVM runs; pass `--parallel-jidt` only when you explicitly want one JVM per worker process.

Run high-shuffle anchors from a completed validation CSV:

```bash
XDG_CACHE_HOME=$PWD/.cache .venv/bin/python SaddlepointValidation/high_shuffle_anchors.py --input-results SaddlepointValidation/outputs/focused_hardened/saddlepoint_validation_results.csv --output-dir SaddlepointValidation/outputs/high_shuffle_anchors --anchors 5 --shuffles 100000
```

## Outputs

- `saddlepoint_validation_results.csv`: one row per null dataset.
- `saddlepoint_validation_summary.csv`: per-configuration calibration and JIDT agreement.
- `overall_summary.csv`: aggregate calibration metrics.
- `pvalue_scatter_vs_jidt.png`: p-value agreement against JIDT shuffling.
- `fpr_alpha05_by_config.png`: null rejection rates at alpha 0.05.
- `runtime_comparison.png`: per-table runtime comparison.
- `summary.md`: short written summary.

## Notes

JIDT permutation p-values are Monte Carlo estimates. With `S` shuffles their resolution is
around `1/S`, and JIDT may report zero if no shuffle is as extreme as the observed statistic.
Use a larger `--shuffles` value for tail-focused comparisons.

Every replicate stores the full contingency table, nonempty table, margins, dynamic degrees of
freedom, support status, saddlepoint root diagnostics, JIDT shuffle count, and the manual-vs-JIDT
`G` statistic difference.
