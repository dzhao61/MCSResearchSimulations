# Practical MI exploration

This folder is separate from the thesis and its packaged experiments.
PROTOCOL.md fixes the six comparisons and their interpretation. The raw/
archives are public CC BY 4.0 UCI datasets, cited there and in the generated
report. No thesis, working draft or statistical method is edited.

From the workspace root:

```bash
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python -m unittest discover -s PracticalMIExploration -p 'test_*.py'
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py run
env MPLBACKEND=Agg MPLCONFIGDIR=/private/tmp/practical-mi-mpl .venv/bin/python PracticalMIExploration/run_exploration.py verify
```

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
