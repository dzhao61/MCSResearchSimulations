# Generated Results

Experiment outputs are placed in timestamped subdirectories here. Each run
contains:

- `configuration_results.csv`
- `summary.md`
- `run_metadata.json`

Large generated result directories are intentionally not committed by default.

Current evidence runs:

- `saddlepoint_full_k100000_b1000/`: authoritative optimized deterministic
  router run over 103 configurations, with a separate 74-configuration
  post-pilot confirmation subset.
- `jidt_blockwise_anchors_b1000_k200000/`: six direct JIDT comparisons using
  1,000 correct within-stratum orderings and 200,000-draw references where
  convolution was unavailable.
- `jidt_tie_anchor_b100000/`: high-shuffle reproduction of JIDT's
  floating-point tie behavior.
- `saddlepoint_router_pilot_k20000_b1000/`: routing pilot; useful for audit
  history but not the strict confirmation result.
- `full_initial_k100000_b1000/`: 103 fixed-margin configurations, 100,000
  null draws per configuration, and 1,000 literal block permutations using
  the earlier moment-approximation implementation.
- `unconditional_smoke_r5000_a100_k1000/`: 32 data-generating regimes,
  5,000 fresh-margin null datasets per regime, and 100 conditional Monte Carlo
  anchors with 1,000 draws each.
