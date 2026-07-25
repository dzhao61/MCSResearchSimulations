# JIDT Discrete MI Significance Implementation Audit

Date: 2026-07-06

This note verifies that the project is using JIDT's discrete mutual-information significance methods correctly and documents how JIDT implements them internally.

## Short Verdict

The project is using JIDT shuffling correctly:

```python
calc = MutualInformationCalculatorDiscrete(r_nominal, c_nominal, 0)
calc.initialise()
calc.addObservations(x, y)
mi_bits = calc.computeAverageLocalOfObservations()
dist = calc.computeSignificance(shuffles)
```

The JIDT shuffle baseline is a fixed-margin permutation test. It reconstructs marginal arrays from the observed counts, randomly permutes one variable, recomputes MI, and returns:

```text
p = count(surrogate_MI >= observed_MI) / numPermutations
```

There is no `+1` correction in JIDT's empirical p-value.

## Source Evidence

### Observations Are Counted Into A Contingency Table

File:

```text
/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/java/source/infodynamics/measures/discrete/MutualInformationCalculatorDiscrete.java
```

Relevant lines:

```text
202-217
```

JIDT loops through paired observations and increments:

```java
jointCount[iVal][jVal]++;
iCount[iVal]++;
jCount[jVal]++;
```

This means our row-major reconstruction from a contingency table is valid. JIDT only needs the counts for MI and significance.

### MI Is Returned In Bits

Relevant lines:

```text
245-291
```

JIDT computes:

```java
double localValue = Math.log(jointProb / (probi * probj)) / log_2;
miCont = jointProb * localValue;
mi += miCont;
```

So:

```text
computeAverageLocalOfObservations() returns MI in bits.
```

For likelihood-ratio `G`, the project correctly converts:

```text
G = 2 * N * MI_bits * ln(2)
```

### JIDT Shuffle Significance

Relevant lines:

```text
294-358
```

`computeSignificance(int numPermutationsToCheck)` calls:

```java
RandomGenerator rg = new RandomGenerator();
int[][] newOrderings = rg.generateRandomPerturbations(observations, numPermutationsToCheck);
return computeSignificance(newOrderings);
```

Then `computeSignificance(int[][] newOrderings)`:

1. Computes the actual MI.
2. Reconstructs `iValues` from `iCount`.
3. Reconstructs `jValues` from `jCount`.
4. Applies each permutation to `iValues`.
5. Recomputes the joint table against fixed `jValues`.
6. Counts how many surrogate MI values are at least the observed MI.

The p-value is:

```java
measDistribution.pValue =
    (double) countWhereMIIsMoreSignificantThanOriginal /
    (double) numPermutationsToCheck;
```

So JIDT's empirical p-value convention is:

```text
count / K
```

not:

```text
(count + 1) / (K + 1)
```

### Random Permutations

File:

```text
/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/java/source/infodynamics/utils/RandomGenerator.java
```

Relevant lines:

```text
38-47
671-702
```

JIDT uses:

```java
random = new Random();
Collections.shuffle(list, random);
```

The permutations are not necessarily distinct. The default `computeSignificance(int)` method does not expose a seed. For reproducible JIDT shuffles, use `computeSignificance(int[][] newOrderings)` with explicit permutation arrays.

## Controlled Test

I tested JIDT with explicit permutation orderings and manually reconstructed exactly the surrogate tables JIDT should produce.

Test table:

```text
[[3, 1, 0],
 [1, 2, 1],
 [0, 1, 1]]
```

Observed MI:

```text
JIDT bits:   0.3974168451037089
manual bits: 0.3974168451037092
```

For five supplied permutation arrays, JIDT returned surrogate MI values:

```text
[1.5219280948873621,
 0.7219280948873621,
 1.5219280948873621,
 0.7219280948873621,
 0.32192809488736207]
```

Manual reconstruction returned:

```text
[1.5219280948873624,
 0.7219280948873623,
 1.5219280948873624,
 0.7219280948873623,
 0.3219280948873624]
```

Maximum surrogate difference:

```text
3.33e-16
```

JIDT p-value:

```text
0.8
```

Manual p-value using JIDT's `count / K` convention:

```text
0.8
```

This confirms our understanding of JIDT's permutation implementation.

## Relationship To Empirical Fixed-Margin Table Sampling

JIDT shuffling samples the fixed-margin null by permuting one marginal label array against the other. The empirical table sampler samples the same fixed-margin null directly at the contingency-table level.

The two methods differ in Monte Carlo convention:

- JIDT: `count / K`
- Our empirical table p-value: `(count + 1) / (K + 1)`

This difference is intentional and conservative. It creates differences of order `1 / K`, not substantive disagreement.

## Relationship To JIDT Analytic Significance

JIDT's no-argument analytic significance method is separate:

```java
computeSignificance()
```

It uses JIDT's bit-valued MI estimate directly inside a chi-square calculation:

```text
p = P(ChiSquare_df >= 2N * MI_bits)
```

The standard likelihood-ratio chi-square uses:

```text
p = P(ChiSquare_df >= 2N * MI_nats)
```

Therefore the JIDT analytic result is not the same as the standard nats-based likelihood-ratio chi-square result.

## Conclusion

The project is using JIDT shuffling correctly as the baseline permutation significance test.

The important caveats are:

- JIDT MI is in bits.
- Convert to nats when computing standard `G = 2N * MI_nats`.
- JIDT shuffle p-values use `count / K`, no `+1` correction.
- JIDT default shuffle calls are not seeded.
- JIDT analytic significance is a separate bits-scaled chi-square convention and should not be confused with the standard likelihood-ratio chi-square.

