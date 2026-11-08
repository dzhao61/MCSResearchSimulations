# External Data and Code

## AIMS Manuscripts

`AIMS_manuscripts/` is a shallow clone of:

```text
https://github.com/ctboughter/AIMS_manuscripts
```

It is retained to verify the direct applied precedent and assess a possible
immune-sequence case study. The repository contains its own MIT license.

The native amino-acid position tables were not used for the primary case
study because their sparse `21x21` support is outside the frozen regular
scope without additional modeling.

## UCI Adult

`adult.zip` and `adult/` are the official UCI Adult dataset:

- DOI: https://doi.org/10.24432/C5XW20
- Source: https://archive.ics.uci.edu/static/public/2/adult.zip
- License: CC BY 4.0

The files are used by `experiments/run_adult_case_study.py`.
