# Adversarial Audit

## Verdict

The implementation, frozen experiment, and saved artifacts passed the audit.
No unit inconsistency, data leakage, look-ahead use of simulated outcomes,
seed collision, invalid null population, or aggregate-calculation error was
found.

This supports the reported `NO-GO`; it does not convert the internal
simulation into external replication or prove the Student-t approximation.

## Mathematical Checks

- The analytic `IF_V` matched cellwise contamination finite differences.
- Its probability-weighted mean was zero to numerical tolerance.
- The direct combined-df calculation matched the component Satterthwaite
  formula.
- Scaling probabilities did not alter the functional diagnostics.
- The candidate converged to the normal reference as sample size increased.
- Exact independence was marked first-order invalid.

## Software Checks

- Eleven permanent tests passed.
- The estimate, influence variance, standard error, statistic, normal
  p-value, naive-Welch df, and naive-Welch p-value exactly matched the prior
  implementation.
- Scalar and vectorized results agreed.
- Swapping groups or relabelling categories preserved two-sided inference.
- Malformed, fractional, negative, non-finite, and undersized tables were
  rejected.
- All valid p-values were finite and in `[0,1]`.

## Experimental Checks

- The 326 null scenario keys and simulation seeds were unique.
- Power seeds were disjoint from null simulation seeds.
- Saved weak-null population pairs had equal MI within `2e-12`.
- Saved strong-null population arrays were exactly equal.
- Broad, hard, and strong stages had `100%` valid calculations.
- Stress validity was `99.991%`; its 23 invalid pairs were retained through
  the reported validity denominator.
- Rejection rates mapped to integer rejection counts.
- Wilson intervals contained their reported rates.
- Every aggregate metric recomputed from scenario-level output.
- The stored decision agreed with the frozen criteria.
- Recorded hashes matched the exact method and runner used for the result.

The machine-readable audit is `results/frozen_decisive/AUDIT.json`.

## Leakage and Look-Ahead Assessment

The formula was motivated by an earlier exploratory variance audit, but the
derivation and acceptance criteria were frozen before applying the candidate
to the new population and simulation seeds. No simulation outcome is used to
estimate a tuning constant, choose a threshold, or select a candidate.

The hard stage reuses its population distributions from the broad grid by
design, but uses independent table-sampling seeds. This is not leakage into
the method because the method has no fitted parameters; it does mean broad
and hard are not independent population-level experiments. The reported hard
evidence is therefore a targeted resampling assessment, not an external
replication.

## Residual Risks

- The population generator and validation framework are internal code, not
  an independently implemented external benchmark.
- The protocol was prospectively frozen inside this research workflow rather
  than publicly preregistered.
- Near-zero MI, changing support, and severe empirical zero-cell boundaries
  remain outside the regular influence-function theory.
- The first-order MI bias correction remains unchanged and may dominate in
  the smallest sparse tables.
- The variance-functional moment match is not a proof that the studentized
  statistic follows a Student distribution.
