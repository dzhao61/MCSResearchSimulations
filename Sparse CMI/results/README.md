# Generated Results

Experiment outputs are placed in timestamped subdirectories here. Each run
contains:

- `configuration_results.csv`
- `summary.md`
- `run_metadata.json`

Large generated result directories are intentionally not committed by default.

Current evidence runs:

- `full_initial_k100000_b1000/`: 103 fixed-margin configurations, 100,000
  null draws per configuration, and 1,000 literal block permutations.
- `unconditional_smoke_r5000_a100_k1000/`: 32 data-generating regimes,
  5,000 fresh-margin null datasets per regime, and 100 conditional Monte Carlo
  anchors with 1,000 draws each.
