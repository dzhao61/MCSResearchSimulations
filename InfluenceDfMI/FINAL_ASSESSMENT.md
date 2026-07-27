# Final Assessment: MI-Specific Influence Degrees of Freedom

## Bottom Line

The calculation is mathematically meaningful and empirically useful, but the
tested Student-t implementation should not replace the normal or naive-Welch
reference universally.

The prospective result is `NO-GO`: seven of nine adoption criteria passed.
The candidate delivered a large improvement in the pre-specified hard and
small-sample stress regimes, but it over-corrected balanced cases and narrowly
missed the broad-grid non-inferiority tolerance.

## What Was Derived

For

```text
V(P) = Var_P(log[p_XY/(p_X p_Y)]),
```

the variance-functional influence function is

```text
IF_V(a,b) =
    l_ab^2 - E[l^2]
    + 2(l_ab - E[l|X=a] - E[l|Y=b] + E[l])
    - 2 E[l](l_ab - E[l]).
```

Writing `tau^2 = Var_P(IF_V)`, the estimated variance component
`V(P_hat)/n` has leading variance `tau^2/n^3`. Matching that component to a
scaled chi-square gives the MI-specific component degrees of freedom

```text
nu_P = 2 n_P V(P_hat)^2 / tau_P_hat^2.
```

The two groups are then combined by the standard Satterthwaite moment match.
No tuning constant or validation-fitted parameter is used.

## Prospective Evidence

The experiment used 144 broad weak-null population pairs, 12 hard population
pairs with independently sampled tables, 144 strong-null controls, 26 stress
cases, and five power cases. It evaluated 1.94 million null table pairs and
50,000 power table pairs using untouched population and simulation seeds.

| Regime | Normal MAE | Naive Welch MAE | MI-specific MAE |
| --- | ---: | ---: | ---: |
| Broad | 0.00480 | 0.00462 | 0.00494 |
| Hard | 0.01231 | 0.01131 | 0.00736 |
| Strong null | 0.00530 | 0.00513 | 0.00537 |
| Stress diagnostic | 0.03729 | 0.03567 | 0.02658 |
| Balanced design 0 | 0.00546 | 0.00557 | 0.00735 |

On the hard grid, the candidate improved alpha-`0.05` MAE by `35.0%`; its
paired bootstrap interval for improvement was `[0.00248, 0.00591]`. On the
broad grid, its MAE was `0.000325` worse than naive Welch, with paired
bootstrap interval `[-0.000726, 0.000079]`. The broad miss was only
`0.000075` beyond the frozen tolerance, but the balanced degradation was
clearer: its paired interval relative to naive Welch was
`[-0.002792, -0.000967]`.

Mean power was `0.3456`, compared with `0.3547` for naive Welch, a loss of
`0.00912`. Median scalar runtime was `0.162 ms`, compared with `0.118 ms` for
normal Wald and `0.127 ms` for naive Welch.

## Why the Result Is Scientifically Useful

The candidate reduced median absolute log-error in denominator degrees of
freedom from `1.364` to `0.062`, a `95.4%` reduction. For example, one
balanced `2x2` case had empirical denominator df `28.18`; naive Welch
predicted `772.71`, while the MI-specific calculation predicted `27.15`.

This confirms the original `n-1` component-df assumption is not a good model
of the plug-in MI variance estimator. However, replacing it with an accurate
moment match made the balanced p-value too conservative. The missing step is
that a random denominator with chi-square-matched moments does not by itself
make the ratio Student-t. The numerator can be non-normal, the denominator
need not be scaled chi-square, and the two can be dependent. Hard cases had
observed numerator/denominator correlations as high as about `0.82`.

## Recommendation

Keep the influence-function derivation as a valid theoretical result and use
it to guide the next candidate. Do not publish the current Student-t p-value
as a universal finished method, and do not add a data-driven switch between
normal and Student-t using these same results.

The clean next derivation is a joint second-order approximation for

```text
(bias-corrected MI difference, estimated variance).
```

That calculation should include `Cov(Delta_hat, SE_hat^2)` and relevant third
cumulants, then approximate the studentized statistic directly. It attacks
the empirically identified failure rather than tuning the current df formula.
Any resulting method should be frozen and tested on new population seeds.

An external replication of this exact candidate is optional: it could
quantify the borderline broad-grid miss more precisely, but it will not
remove the demonstrated balanced-case over-correction.
