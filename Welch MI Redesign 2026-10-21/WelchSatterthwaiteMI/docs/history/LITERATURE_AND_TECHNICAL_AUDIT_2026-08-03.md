# Literature and Technical Audit: 3 August 2026

## Bottom Line

The external critique materially improves the project, but not every claim in
it is correct.

The original `n - 1` Welch-Satterthwaite construction should not be presented
as a new statistical template. Hutcheson's 1970 test already applies the same
broad architecture to differences in Shannon entropy. The defensible project
is an MI-specific transport and audit: add the discrete-MI bias correction,
derive the appropriate MI influence quantities, test the unrestricted weak
null `I(P) = I(Q)`, and determine how the finite-sample reference must change.

The post-hoc experiment supports a more interesting candidate: degrees of
freedom derived from the full influence function of the MI variance
functional. It improves deliberately liberal hard regimes substantially but
is not uniformly superior across regular tables. A new frozen validation is
required.

## Claims Confirmed

### Hutcheson is direct prior art

Hutcheson (1970), *A Test for Comparing Diversities Based on the Shannon
Formula*, compares two Shannon entropies using their estimated delta-method
variances and a Satterthwaite reference. The current `ecolTest`
implementation computes

```text
t  = (H1 - H2) / sqrt(S1 + S2)
df = (S1 + S2)^2 / (S1^2 / n1 + S2^2 / n2)
```

This is the same general template as BCW-DMI. The MI extension remains
nontrivial because MI depends on joint and marginal probabilities, has leading
bias `(r - 1)(c - 1)/(2n)`, and has a degenerate first-order influence
function at independence.

Primary record: <https://doi.org/10.1016/0022-5193(70)90124-4>.

### The segregation literature is important

Mora and Ruiz-Castillo directly study statistical comparison of the mutual
information segregation index. Allen et al. (2015) provide a close programme
for another segregation index: bias adjustment, asymptotic tests, bootstrap
comparison, and between-population applications.

- Mora and Ruiz-Castillo working paper: *The Statistical Properties of the
  Mutual Information Index of Multigroup Segregation*, WP 09-84.
- Mora and Ruiz-Castillo (2011): <https://doi.org/10.1111/j.1467-9531.2011.01237.x>.
- Allen et al. (2015): <https://doi.org/10.1111/ectj.12039>.

### Bootstrap-t is a required comparator

The Shannon-diversity literature reports strong bootstrap-t coverage in its
simulated regimes. This does not prove it will win for weak-null differential
MI, but it makes omission hard to defend. It is now included in the required
next experiment.

### The stress result needed stronger wording

The original stress-grid in-band fraction fell from 19.23% to 15.38%.
BCW-DMI is monotone conservative and can worsen already-conservative cases.
The revised article states this directly and notes that no validated
pre-test diagnostic currently identifies those cases.

### The asymptotic proposition was too weak

The removed proposition only established that a Student reference converges
to normal as its degrees of freedom diverge. The revised article presents
this as asymptotic compatibility, not a substantive theorem.

## Claims Corrected

### The 2011 Mora paper is not simply the published 2009 paper

The 2011 *Entropy-Based Segregation Indices* article is related and should be
cited, but its abstract and lineage concern the properties and normalization
of the M, H, and H* indices. The 2009 statistical-properties working paper was
substantially revised into a separate 2010 working paper on conditional
segregation. The manuscript therefore cites both sources for their distinct
roles rather than replacing one with the other.

### Local kurtosis is not the full degrees-of-freedom derivation

For a fixed score, the sample-variance moment approximation gives

```text
df approximately 2n / (excess kurtosis + 2).
```

For MI, however, the local score is itself estimated from the same table.
The correct first-order calculation differentiates the full variance
functional. The repository had already derived this influence function, and
the new audit independently reproduced the old calculation to
`3.6e-15`.

### Estimated variance is not uniformly biased downward

The requested diagnostic was run on 960,000 new table pairs.

| Population set | Mean estimated SE2 / population SE2 | Empirical Var(delta) / population SE2 | Mean Corr(delta, estimated SE2) |
| --- | ---: | ---: | ---: |
| Decisive hard (12) | 1.0014 | 1.0710 | 0.5865 |
| Fresh regular (72) | 1.0662 | 1.0632 | 0.3963 |

The plug-in standard error is approximately unbiased on the hard grid and
upward-biased on average in the fresh broad grid. Moreover, using the known
population variance did not uniformly fix calibration. The failure is in the
joint finite-sample distribution, not one universal downward variance bias.

### Dependence does not prove that Student correction is useless

Strong correlation between the numerator and denominator invalidates an
exact classical-t interpretation. It does not logically imply that every
Student reference must fail to improve calibration. The simulation results
show small gains for naive Welch and larger hard-regime gains for the full
variance-functional reference. The correct conclusion is that these are
approximations requiring empirical validation, not exact pivots.

## New Experimental Result

Mean absolute FPR error was:

| Population set | Alpha | Normal | Naive Welch | Local kurtosis | Variance IF |
| --- | ---: | ---: | ---: | ---: | ---: |
| Decisive hard (12) | 0.05 | 0.01270 | 0.01169 | 0.01040 | **0.00823** |
| Decisive hard (12) | 0.01 | 0.00568 | 0.00506 | 0.00428 | **0.00266** |
| Fresh hard (6) | 0.05 | 0.00993 | 0.00912 | 0.00775 | **0.00662** |
| Fresh hard (6) | 0.01 | 0.00407 | 0.00360 | 0.00317 | **0.00232** |
| Fresh all (72) | 0.05 | 0.00463 | 0.00445 | **0.00423** | 0.00446 |

The full variance-functional candidate reduced alpha-0.05 MAE by 35.2% on
the decisive hard populations and 33.4% on the fresh hard subset relative to
normal Wald. Across all 72 fresh scenarios, it improved 28, worsened 39, and
tied 5, despite a slightly lower average MAE. This is promising but not a
universal win.

## Changes Made

- Added `experiments/audit_variance_bias.py`.
- Added `results/variance_bias_audit/` with scenario results, summaries,
  metadata, and a report.
- Renamed the formal method to the descriptive BCW-DMI acronym.
- Added Hutcheson, Mora and Ruiz-Castillo (2011), Allen et al. (2015), and
  bootstrap-t literature to the article.
- Corrected the Martin/Holmes citation attribution.
- Demoted the asymptotic proposition to a qualification.
- Strengthened reporting of the negative stress-grid result and paired Monte
  Carlo design.
- Added the variance-functional derivation and post-hoc results to the article.

## Next Decision

Do not promote either refinement yet. Freeze a new protocol comparing normal
Wald, naive Hutcheson-type Welch, local-kurtosis df, full variance-functional
df, studentized permutation, and multinomial bootstrap-t. Use new population
families and seeds, include alpha 0.10, 0.05, and 0.01, and test power and
support-dimension sensitivity. That experiment will decide whether the thesis
centres on the full variance-functional refinement or on a broader negative
audit of Welch-type information-functional inference.
