# Next Experiment Plan: Detection and Breakdown Sweep

**Status: designed, not implemented.** This document specifies the next
experiment to build. Nothing described under "Plan" below exists yet.

It responds to supervisor meeting notes asking for three things: test both
false-positive *and* true-positive rates as a function of a difference
parameter, remove every artificial lower bound and push until the method
breaks, and extend beyond `2x2` tables.

---

## 1. Current repository state

Repo root: `Simulations/`. This project: `WelchSatterthwaiteMI/`.
Run everything through the project virtual environment:

```bash
MPLBACKEND=Agg MPLCONFIGDIR=$PWD/.mplcache XDG_CACHE_HOME=$PWD/.cache \
  .venv/bin/python -m unittest discover -s WelchSatterthwaiteMI/tests
```

**Thesis scope.** Expanded Welch is the thesis and is supervisor-approved;
roughly 81 pages are drafted in `Thesis Writeup/Welch MI/`. The constrained
likelihood-ratio test is a *secondary* evaluation only — do not add an LR
chapter or restructure the thesis around it.

**Work completed but not yet committed** (staged in the working tree):

1. `experiments/run_supervisor_experiment.py` — modified:
   - Added a **strong-null regime** (`P = Q` exactly, 12 pairs) as a positive
     control. The grid grew from 60 to **72 population pairs**.
   - Added **three rejection-rate denominators** throughout: conditional on
     validity, unconditional (invalid counted as non-rejection), and
     common-valid (restricted to replicates where every method is defined).
   - Added **preregistered decision rules**: Bradley's liberal interval
     `[0.5*alpha, 1.5*alpha]` for adequate size control, and a 0.90 valid-rate
     floor, both reported as pass/fail counts in `regime_summary.csv`.
   - **Power extended to the full grid**, with effect sizes relative to each
     pair's own null MI (0.5x, 1.0x), plus size-adjusted power computed from an
     independent calibration RNG stream.
   - Infeasible power constructions are now logged to
     `power_infeasible_configurations.csv` rather than silently skipped.
2. `tests/test_supervisor_experiment.py` — five new tests. Full suite passes
   (57 tests).
3. `experiments/FINAL_PROTOCOL.json` — new frozen preregistration for the
   Expanded Welch validation.
4. `experiments/run_lr_permutation_comparison.py` — new secondary comparison of
   constrained LR and studentized permutation against Wald and Expanded Welch
   on the same 72 pairs. Results in `results/lr_permutation_comparison/`
   (untracked).
5. `results/supervisor_full/` regenerated at full profile (72 pairs, 10,000
   replicates, ~41 s).

**Known gap:** thesis Chapters 5 and 6 still quote the old 60-pair numbers and
have not been updated to the regenerated 72-pair results.

**Do not modify** the regime definitions in `run_supervisor_experiment.py` or
`experiments/FINAL_PROTOCOL.json`. That grid is the frozen primary evidence.
The work below is a separate, exploratory script.

---

## 2. Background: what the supervisor was looking at

The notes point at `experiments/run_2x2_power_curves.py`, whose docstring is
*"Trace fixed-threshold detection across MI effects and sample sizes."* It
already sweeps an MI-difference parameter from `0.0` (giving the false-positive
rate) through `0.5` (giving the detection rate) at a fixed `alpha = 0.05`. So
this task is a **generalisation of that script**, not a new idea.

What it already does well: no expected-count floor anywhere
(`"Build C1-C4 without filtering on expected counts"`), a realised minimum
expected count of 0.0139, a minimum `n` of 5, and a per-sub-case figure for each
of 13 named configurations.

What blocks the three asks:

- **`n` is not a first-class factor.** The low end is reached only incidentally,
  through `SAMPLE_SCALES = (0.5, 1.0, 2.0)` applied to 13 fixed anchors.
- **Hard `2x2` constraints.** `probability_table(u, v, delta)` in
  `run_2x2_experiment.py` is a literal `2x2` array; the `(u, v, delta)`
  parameterisation and its branch-boundary logic exist only for binary tables;
  `simulate_configuration` hard-reshapes to `(per_block, 2, 2)`.
- **API coupling.** Six modules import this script's constants
  (`run_constrained_lr_*.py`, `run_critical_value_audit.py`,
  `run_joint_cornish_fisher_audit.py`, `tests/test_2x2_power_curves.py`), and
  its figure code is hard-wired to three methods and at most 15 anchors.
  Modifying it in place would break five scripts and a test, so the new work
  must be a **separate script**.

---

## 3. Two findings that shape the design

### 3.1 The true floors, and three silent failure modes

Verified empirically against the library, not merely read from source:

- **Hard limit: `n >= 2` per table**, shape at least `2x2`, integer nonnegative
  counts (`src/welch_differential_mi/welch.py`, `_validate_pair`).
  `MINIMUM_SAMPLE_SIZE = 50` in the experiment scripts is purely a design
  choice; nothing in the library requires it.
- **`n = 2` is a genuine mathematical floor for Expanded Welch.** Every legal
  table at `n = 2` has influence variance exactly zero, because the log-ratio
  score is constant over the two occupied cells. So `base_valid` is always
  False there. **`n = 3` is the smallest sample size at which the expanded
  method can be valid at all**, and even then only about 40% of `2x2` tables
  qualify, with component degrees of freedom at most 1.083.
- Per-table degeneracy under multinomial sampling (`2x2`, MI approximately
  0.08 nats): **40.8% invalid at `n = 3`, 11.4% at `n = 5`, 6.1% at `n = 10`,
  1.1% at `n = 20`, 0.04% at `n = 50`.**

Three failure modes that **no validity flag catches**, concentrated roughly
between `n = 6` and `n = 20`. These are the substance of "where does it break":

1. **Degrees-of-freedom collapse (`df < 1`)** — for example `expanded_df_p =
   0.409` at `n = 6`. A Student reference on fewer than one degree of freedom
   pins p-values near 1, so the test *cannot reject at all*. This is the
   mechanism behind the supervisor's observation: at `n = 5` the existing `2x2`
   results show a median df of about 2.4 and a rejection rate identically zero
   at every effect size.
2. **Degrees-of-freedom explosion (`df > 1e4`)** — sparse but structured tables
   produce a near-zero variance-of-variance alongside a nonzero variance,
   giving df of 3.4e6 at `2x2` with `n = 12`, and 8.1e31 for a `3x3` at
   `n = 8`. Here `expanded_valid` is True, but the Student reference silently
   collapses to the normal, so the finite-df correction does nothing precisely
   where it is most needed.
3. **Catastrophic cancellation near independence** — `influence_variance`
   returns floating-point noise of order 1e-32 rather than exact zero, and the
   expanded df becomes a ratio of two pieces of noise, producing a spurious
   finite value. The `variance > 1e-14` guard inside `base_valid` is the only
   thing that catches these.

Consequently the sweep must record **the distribution of effective degrees of
freedom**, not only p-values: median, 5th and 95th percentiles, and the
fractions with `df < 1` and `df > 1e4`. Without this, the two opposite failure
modes are indistinguishable — both simply look like "the correction did
nothing".

**One floor must stay:** the `variance > 1e-14` guard. It is the only defence
against mode 3, so "remove the floors" does not extend to it. Relaxing it
produces garbage rather than more information, and this is worth stating
explicitly in the writeup.

### 3.2 A confound in the existing finding

In the existing results, **validity declines as the effect size grows**. For
`C1_N0_n10` at `n = 10`, the Expanded Welch valid rate falls from 0.972 to
0.925 to 0.783 as `mi_difference` goes from 0 to 0.2 to 0.5, because a larger
MI concentrates probability mass and trips the variance mask. Rejection rate is
currently computed **conditional on validity**, so part of the "rejects less
often when there is a difference at low samples" finding may be a conditioning
artefact rather than genuine conservatism.

The new sweep must therefore report conditional, unconditional, and
common-valid rates so the two explanations can be separated. That machinery
already exists in `run_supervisor_experiment.py` and can be reused directly.

The other mechanism is real and worth quantifying separately: at `n = 5`,
Expanded Welch has a rejection rate of exactly zero at every effect size, with
a median df of about 2.4 — such a reference simply cannot reach `p <= 0.05`.

---

## 4. Plan: new script `experiments/run_detection_breakdown_sweep.py`

A five-factor crossed sweep. At effect zero the rejection rate **is** the
false-positive rate; above zero it is the detection rate. One surface, both
quantities, one fixed threshold — exactly the framing in the notes.

| Factor | Levels |
| --- | --- |
| Shape | `2x2`, `3x3`, `4x4`, `5x5`, `8x8` |
| Margin skew (both margins, both populations) | balanced, mild (0.70), strong (0.90), ultra (0.95) |
| Sample size `n_P = n_Q` | 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50, 75, 100, 150, 250, 500, 1000 |
| Effect `delta` | 0, 0.01, 0.025, 0.05, 0.10, 0.20, 0.40 (relative; see below) |
| Null type | `strong` (Q margins equal P margins, so `P = Q` at `delta = 0`) and `weak` (Q margins rolled, so `P != Q` with equal MI at `delta = 0`) |

The sample grid deliberately begins at the hard limit. `n = 2` is *expected* to
be 100% invalid for Expanded Welch; that is a reportable result establishing the
floor empirically, not a reason to omit the row. The grid is dense from 3 to 20
because that is where the silent failure modes live.

Roughly 280 populations times 18 sample sizes gives about 5,040 cells. Measured
throughput is 266k to 1M table pairs per second, so 10,000 replicates per cell
is about 50M pairs, or **two to four minutes**. There is no reason to reduce
replicate counts or to allocate them unevenly across shapes.

### 4.1 Effect parameterisation: relative to the analytic MI ceiling

A fixed absolute MI difference is not comparable across this grid.
Ultra-skewed margins cap MI far below balanced ones — the existing `2x2` `N7`
anchor has a target MI of 0.0005 purely because margins of (0.005, 0.005)
cannot support more — and larger alphabets admit much larger MI.

The ceiling is analytic: `MI_ceiling = min(H(row margin), H(col margin))`,
confirmed to be exactly what the table constructor saturates to. So for each
(shape, skew):

- `I(P) = 0.25 * MI_ceiling`
- `I(Q) = I(P) + delta * MI_ceiling`

Using **P's** ceiling for the effect scale, rather than Q's, keeps
`delta = 0` implying `I(P) = I(Q)` exactly in both null arms. For the weak-null
arm, Q's margins are the *rolled* P margins (`np.roll(margin, 1)` for rows and
`-1` for columns, as `run_multialphabet_lr_experiment.py` already does), which
changes the distribution while preserving margin entropy. Both populations then
share one ceiling and the null remains exactly feasible.

The maximum fraction used is `0.25 + 0.40 = 0.65` of the ceiling, comfortably
below the region where iterative proportional fitting stops converging;
failures were observed to begin at roughly 96 to 99 percent of the ceiling.
Record absolute `I(P)`, `I(Q)`, `MI_ceiling`, and the realised L1 distance
`||P - Q||` so the absolute scale remains recoverable.

### 4.2 Reuse rather than rewrite

- `table_with_target_mi_from_interaction` and
  `association_table_from_interaction` in
  `DifferentialMI/src/differential_mi/distributions.py` — the R-by-C analogue
  of the `2x2` `(u, v, delta)` construction: fixed margins, iterative
  proportional fitting, Brent root-finding on association strength. Already
  used by `run_supervisor_experiment.py`.
- `marginal_probabilities` for balanced, mild, and strong; define `ultra`
  (0.95) locally, as the multi-alphabet LR script already does.
- `differential_mi_pvalues` in `src/welch_differential_mi/welch.py` — fully
  R-by-C and batched.
- `_wilson`, `_wilson_many`, the `METHODS` dictionary pattern, and the
  three-denominator reporting from `run_supervisor_experiment.py`.

### 4.3 Floors: what goes and what stays

Removed: `MINIMUM_SAMPLE_SIZE = 50`, all expected-count band constraints, and
the `||P - Q|| >= 0.05` population-separation floor.

Kept, because they are mathematical rather than design choices, and each is
*recorded* rather than silently applied: `n >= 2` (the library raises below
that), minimum cell probability above 1e-12, the `variance > 1e-14` guard
discussed in section 3.1, and the per-replicate validity masks — which become
the breakdown signal rather than a filter.

Infeasible constructions must catch **both** `ValueError` ("Target MI is
infeasible for the requested margins") **and** `RuntimeError` ("Iterative
proportional fitting did not converge"). Near the ceiling the `RuntimeError`
path is the more common one, and the existing test suite covers only the
`ValueError` case.

### 4.4 Outputs

- `cell_results.csv` — one row per (shape, skew, `n`, `delta`, null type,
  method): rejection rate at `alpha` in {0.10, 0.05, 0.01} under all three
  denominators, Wilson interval, Monte Carlo standard error, valid rate, and
  sparsity diagnostics (observations per cell, minimum expected count, fraction
  of expected counts below 1, zero-cell rate, empty-margin rate). Plus the
  **effective-df distribution** — median, 5th and 95th percentiles, and the
  fractions with `df < 1` and `df > 1e4` — which is what distinguishes
  "conservative because the reference collapsed" from "inert because the
  correction vanished".
- `breakdown_frontier.csv` — the "keep pushing until it breaks" deliverable.
  For each (shape, skew, null type, method), the smallest `n` at which each
  prespecified criterion is first met and continues to hold for all larger `n`:
  *calibration* (false-positive rate at `delta = 0` inside Bradley's
  [0.025, 0.075]), *validity* (valid rate at least 0.90), *detection*
  (rejection rate at least 0.5 at the largest `delta`), and *reference sanity*
  (fraction with `df < 1` below 0.01 and fraction with `df > 1e4` below 0.01).
  The last criterion is what catches the silent modes.
- `infeasible_configurations.csv` — every dropped construction, with a reason.
- Figures: detection heatmaps (`n` against `delta` per shape and skew, where
  the `delta = 0` column is the false-positive column); a breakdown-frontier
  plot (minimum usable `n` against alphabet size, one line per skew); and
  detection curves at selected sample sizes.
- `REPORT.md` and `run_metadata.json` recording seeds, software versions, and a
  SHA-256 hash of the script.

### 4.5 Relationship to the frozen protocol

This is **exploratory characterisation, not confirmatory evidence**. The
72-pair grid in `run_supervisor_experiment.py` and `FINAL_PROTOCOL.json` remain
exactly as they are and continue to serve as the thesis's primary validation.
This sweep answers the separate question of *where the method breaks*, and would
appear in the thesis as a boundary and operating-range section supported by
appendix figures.

---

## 5. Verification

- Run a smoke profile first (few replicates, two shapes) to exercise the
  pipeline end to end.
- Sanity checks that must hold: at `delta = 0` with `null_type = strong` and
  large `n`, all three methods sit within Monte Carlo error of nominal; the
  three denominators coincide wherever the valid rate is 1.0; detection
  increases monotonically in `delta` at fixed `n` for well-sampled cells; and
  every requested target MI is achieved to the constructor's 1e-10 tolerance.
- Reproduce the existing `2x2` finding as a cross-check: the `n` near 5,
  balanced, `2x2` cell should show Expanded Welch detection near zero at every
  `delta`, with a median df near 2.4, matching
  `results/2x2_power_curves/power_curves.csv`.
- Confirm the empirically established floors reproduce: `n = 2` gives a zero
  percent expanded-valid rate everywhere, and `n = 3` on a `2x2` gives roughly
  60 percent, with about 40 percent degenerate.
- Add unit tests for the `MI_ceiling` calculation (it must equal
  `min(H_row, H_col)`), the relative-effect construction (`delta = 0` must give
  exactly equal MI in both null arms), the breakdown-frontier logic, and the
  iterative-proportional-fitting `RuntimeError` path that the current suite
  misses. Then re-run the full suite.

---

## 6. Scope note

This plan addresses the first three asks in the meeting notes. Two other items
are deliberately excluded:

- **Adapting the chi-squared null test to autocorrelated data** via the
  "typical set" concept. The notes mark this "maybe direction afterwards", and
  it is a new research direction rather than an experiment.
- **"Start writing early."** The six-week schedule already front-loads writing
  from week three onward.
