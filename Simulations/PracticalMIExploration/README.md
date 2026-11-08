# Practical MI exploration

This folder contains the practical-data comparisons used by the thesis.
PROTOCOL.md fixes the six comparisons and their interpretation. The raw/
archives are public CC BY 4.0 UCI datasets, cited there and in the generated
report. The initial exploration did not edit the thesis, any working draft or
either statistical method. On 11 October 2026, the two full-data Online
Shoppers comparisons were incorporated into the main thesis as a
self-contained Section 6.5. Subset analyses remain outside the manuscript.

From the workspace root:

```bash
env MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py full --output application-reproduction
env MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py verify-full
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python -m unittest discover -s PracticalMIExploration -p 'test_*.py'
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py run
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py verify
```

The supplement includes all three attributed raw archives, the runner,
protocol, count tables, six full-data results and Holm-adjusted p-values
under `thesis_application/`. The `full` and `verify-full` modes reproduce
and verify these results without running the 150,000 exploratory subsets.
Tests that inspect manuscript text require the separately supplied thesis
source and are skipped when it is absent. Other application tests run in
the standalone supplement.

The runner refuses to overwrite existing results. Use --output with a new
directory to rerun. Default repetitions are 5000 for each permitted subset
size. Method validity and support-loss diagnostics are saved alongside
unconditional and valid-only rejection frequencies.

Outputs in results/ include RESULTS.md, full_data_results.csv,
subsample_results.csv, original count tables, raw subset count/output records,
checksums, source/environment identity, two figures and independent formula
verification. The CSV files preserve unrounded values. Both tests use the
same samples, corrected difference and standard error; the calculation of
the Expanded Welch degrees of freedom and Student t distribution p-value is
the only methodological addition.

The main limitations are unknown population MI, sampling-design assumptions,
rare-category support loss and overlapping subsets. These results illustrate
practical outputs and decision stability, not which method is correctly
calibrated in the real source populations.
