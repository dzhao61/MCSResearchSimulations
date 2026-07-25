# Thesis Claim Matrix

Date: 25 July 2026

## Purpose

This matrix prevents established results, direct applications, and new
project findings from being conflated.

| Candidate claim | Evidence status | Safe wording |
|---|---|---|
| MI values are compared across populations in real applications | Established | Cite Boughter et al. 2020 and 2023 |
| Raw label permutation is used to test MI differences | Established applied practice | Cite the AIMS methods directly |
| Raw permutation is exact when the complete distributions are equal | Established permutation theory | Cite Chung and Romano |
| Raw permutation need not test equality of a parameter when distributions differ | Established general theory | Cite Chung and Romano |
| Raw permutation can fail severely for equal discrete MI | Demonstrated by this project; MI-specific literature claim still under review | Present as our systematic MI-specific validation |
| The leading plug-in MI bias is `(r-1)(c-1)/(2n)` | Classical | Cite Miller and Moddemeijer |
| The first-order MI variance is the variance of the local log density ratio | Classical | Cite Moddemeijer |
| A two-sample Wald statistic can combine two independent MI variances | Standard consequence | Do not claim as a new statistical principle |
| Analytic correction outperforms jackknife in the tested regular grid | New empirical finding from this project | Restrict wording to the saved simulation regimes |
| Studentized MI permutation can degenerate when opposite associations cancel in the pooled mixture | New MI-specific observation from this project; follows established general assumptions | Claim the example, diagnostic, and practical consequence, not a new general theorem |
| The baseline is the first test of equal MI | False or unsupported | Do not use |
| No one uses MI differences in information theory | False | Do not use |
| The project provides the first dedicated fast weak-null validation framework for discrete MI differences | Plausible, not yet established | Use only after formal database and supervisor review |
| A simple Edgeworth refinement improves the two-sided test | Rejected at the theory gate | Do not claim; the leading skewness term cancels |

## Contribution Levels

### Established Ingredients

- Plug-in MI.
- Miller-Moddemeijer bias correction.
- First-order MI variance and influence function.
- Wald inference for smooth functionals.
- General weak-null studentized permutation theory.

### Existing Applied Practice

- Differences between MI matrices or MI values across biological sequence
  populations.
- Unstudentized label permutation with approximately 1,000 permutations.

### Current Project Contribution

- A precise weak-null formulation for the applied MI-difference question.
- Evidence that raw permutation can be invalid in both directions.
- A much faster analytic-bias-corrected deterministic implementation.
- Broad randomized calibration, coverage, power, runtime, and failure-boundary
  evidence.
- Identification of pooled-mixture degeneracy as a practical problem for
  studentized permutation.

### Contribution Still Being Developed

- A clear methodological contribution beyond combining established
  first-order ingredients, potentially simultaneous differential-MI
  inference.

### Refinement Result

- A one-term Edgeworth correction was rejected at the theory gate.
- A pre-specified empirical influence-saddlepoint refinement was stable and
  general but did not improve broad null calibration over analytic Wald.
- The saddlepoint result is a documented negative experiment, not a claimed
  methodological improvement.

## Prohibited Wording

Do not claim:

- invention of the MI bias or variance formula;
- invention of weak-null studentization;
- first comparison of MI values across populations;
- validity at or near independence;
- distribution-free or finite-sample exact inference;
- validity for growing alphabets, structural zeros, or dependent data;
- improved calibration from the tested influence-saddlepoint refinement.

## Provisional Thesis Statement

> Existing applications compare discrete mutual information across
> populations using raw label permutation. This thesis characterizes the
> weak-null failure of that practice and develops fast, bias-corrected
> deterministic inference with explicitly validated operating conditions.
