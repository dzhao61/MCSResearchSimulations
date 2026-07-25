# Empirical Fixed-Margin Method: Adversarial Audit

Date: 2026-07-06

This audit tried to invalidate the empirical fixed-margin table-sampling result by checking implementation assumptions, null-distribution equivalence, p-value conventions, saved-output integrity, and edge cases.

## Audit Verdict

The main result is sane after one edge-case patch.

The empirical fixed-margin sampler appears to target the same fixed-margin null as JIDT shuffling. Manual `G`, batched `G`, and JIDT `G` agree numerically. SciPy `random_table` samples agree with exact enumeration on small supports and with manual raw-observation permutation on larger checks. Saved stress-test CSVs contain finite p-values, valid margins, no JIDT errors, and no method errors.

The one bug found was limited to degenerate fixed-margin nulls. The empirical p-value was valid in principle, but the wrapper returned `NaN` because the optional gamma fit had zero variance. This is now patched.

## Checks Performed

### 1. Statistic Agreement

Compared three versions of the `G = 2N * MI` statistic:

- `g_statistic()`
- vectorized `g_statistics_batch()`
- JIDT MI converted from bits to nats

Tables tested included balanced, perfectly dependent, skewed, and empty-margin cases.

Result:

```text
max observed manual-vs-JIDT G difference in audit examples: ~3.6e-15
max saved stress CSV jidt_g_abs_diff: 5.46e-10
```

This supports that the statistic and unit conversion are not driving the result.

### 2. Exact Enumeration vs SciPy `random_table`

For small fixed-margin supports, enumerated all possible contingency tables exactly, computed exact fixed-margin tail probabilities, and compared them against Monte Carlo samples from `scipy.stats.random_table`.

Observed checks:

| rows | cols | support | exact tail | SciPy MC tail | abs diff |
| --- | --- | ---: | ---: | ---: | ---: |
| `[3, 2]` | `[2, 3]` | 3 | 0.4000 | 0.4032 | 0.0032 |
| `[2, 2]` | `[1, 1, 2]` | 4 | 1.0000 | 1.0000 | 0.0000 |
| `[2, 2, 1]` | `[1, 2, 2]` | 11 | 1.0000 | 1.0000 | 0.0000 |

These differences are consistent with Monte Carlo noise.

### 3. SciPy Fixed-Margin Sampling vs Manual Permutation

For several nontrivial tables, compared:

- direct fixed-margin table sampling via SciPy,
- manual raw-observation permutation of `Y` labels.

Observed p-value differences with 20,000 samples:

```text
0.00015
0.00000
0.00000
```

This supports the key assumption that direct table sampling is equivalent to permutation testing under fixed margins.

### 4. Sparse Tie Convention

Earlier testing found a major sparse-table trap:

```text
100x50, N=1000, extreme skew
observed nonempty shape: 18x15
observed G: 0.651768...
```

Many null tables have exactly the same `G` as the observed table. Without numerical tie handling, empirical table sampling gave a p-value near `0.25`, while JIDT gave `1.0`.

After adding:

```text
G_null >= G_obs - tie_tol
```

the empirical sampler returned `1.0`, matching JIDT.

This fix is essential.

### 5. Degenerate Null Edge Case

Found during this audit:

```text
[[5, 0],
 [0, 0]]
```

The fixed-margin null is degenerate. All valid tables have `G = 0`, so the correct empirical p-value is `1.0`.

Previous behavior:

```text
empirical_p = NaN
error = invalid null moments: mu=0, variance=0
```

Patched behavior:

```text
observed_g = 0
empirical_p = 1
gamma_p = 1
mu = 0
variance = 0
gamma_shape = NaN
gamma_scale = NaN
error = ""
```

This patch prevents the optional gamma fit from invalidating a valid empirical result.

### 6. Saved Output Integrity

Checked corrected stress and mega-anchor output CSVs:

```text
rows checked: 155
bad empirical_fixed_margin_p: 0
bad gamma_fixed_margin_p: 0
bad chi2_dynamic_p: 0
bad chi2_nominal_p: 0
bad jidt_p: 0
gamma_error nonempty: 0
jidt_error nonempty: 0
bad saved table/margin checks: 0
```

The saved tables, row totals, column totals, configured dimensions, and `N` values are internally consistent.

## Assumptions That Still Matter

### 1. JIDT Is Treated As The Baseline, Not Ground Truth

JIDT `computeSignificance` is itself Monte Carlo. With `K=1000`, its p-values have nontrivial noise and resolution about:

```text
1 / 1000 ~= 0.001
```

The empirical fixed-margin implementation uses the standard conservative `+1` correction:

```text
(exceedances + 1) / (K + 1)
```

JIDT may report zero when no shuffle exceeds the observed statistic. Therefore empirical-vs-JIDT differences of order `1 / K` are just finite-Monte-Carlo convention differences, not statistical disagreement.

At `p = 0.5`, the standard error of one Monte Carlo estimate is about `0.016`. So median empirical-vs-JIDT differences around `0.01` are plausible even if both methods target the same null.

### 2. The Method Tests The Conditional Fixed-Margin Null

This is the same null targeted by permutation/shuffling:

```text
condition on observed row and column totals
```

It is not the same as repeatedly drawing new independent datasets from estimated marginal probabilities. That distinction is intentional, but it should be stated clearly in any paper or handoff.

### 3. Stress Runs Are Screens, Not Publication-Grade FPR Calibration

The large stress run used one table per configuration. It is excellent for finding bugs and broad runtime/accuracy patterns. It is not enough to claim precise false-positive-rate calibration per regime.

For publishable FPR claims, rerun selected regimes with many independent null tables per configuration.

### 4. Timing Comparison Is Conservative But Not Perfect

The JIDT timer excludes the Python step that reconstructs raw observation arrays from contingency tables, but includes Java calculator setup, list conversion, statistic computation, and shuffling. This is conservative in favor of JIDT if the user starts from contingency tables.

If a real workflow already has raw observations, excluding reconstruction is fair. If it starts from contingency tables, empirical fixed-margin sampling is even more favorable than the reported timing suggests.

### 5. Gamma Remains Secondary

Gamma can agree well in many cases, but sparse discrete nulls can have large point masses. The continuous gamma approximation cannot represent those. The empirical fixed-margin p-value is the valid candidate method.

## Code Changes From Audit

Patched `SaddlepointValidation/general_fixed_margin.py`:

- `g_statistics_batch()` now avoids invalid divide warnings for zero-total inputs.
- `fixed_margin_gamma_approx()` computes the empirical p-value before gamma fitting.
- zero-variance fixed-margin nulls now return a valid empirical p-value instead of `NaN`.
- the exception path preserves `observed_g` if it was already computed.

Updated `SaddlepointValidation/EMPIRICAL_FIXED_MARGIN_METHOD.md`:

- documented degenerate fixed-margin behavior,
- added a degenerate-null verification check.

## Bottom Line

The core empirical fixed-margin result survives this adversarial pass.

The biggest invalidating bug found was real but fixable, and it affected edge cases where the optional gamma fit had zero variance. It does not undermine the main stress-test conclusion that direct fixed-margin table sampling closely matches JIDT while becoming much faster at large `N`.

The remaining risks are mostly evidence-strength risks, not implementation-invalidating bugs:

- need more replicates for formal calibration,
- need high-`K` anchors for tail accuracy,
- need asymmetric marginal regimes,
- need tests beyond `100x100` if the intended use case requires larger alphabets.
