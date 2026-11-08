# Results

Each run directory contains:

- `replicates.csv`: one row per simulated table pair;
- `scenarios.csv`: exact generating distributions and diagnostics;
- `summary.csv`: rejection rates, Wilson intervals, coverage, bias, and timing;
- `calibration_05.png`: method comparison at nominal 5%;
- `run_metadata.json`: seed and software versions; and
- `REPORT.md`: automatically generated run summary.

Run purposes:

- `smoke`: pipeline check only.
- `screen`: broad low-replicate screen.
- `decisive`: pre-specified high-replicate experiment.
- `adversarial`: post-protocol interaction-pattern and rectangular-table tests.
- `power_curve`: post-protocol effect-size and sample-size power checks.

The overall interpretation is in `../GO_NO_GO_REPORT.md`.
