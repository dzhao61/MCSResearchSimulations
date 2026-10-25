# Earlier experiment archive — 25 October 2026

The 23 older experiment folders formerly at the workspace root are stored in `Past experiments 2026-10-25.zip`. All 661 original files and 161 directories were preserved. Each ZIP entry was verified against its original SHA-256 hash before the uncompressed staging folder was removed.

- Original file contents: 455,528,136 bytes (455.5 MB).
- ZIP: 145,978,182 bytes (146.0 MB).
- Reduction: about 309.5 MB (68.0%).
- `PAST_EXPERIMENTS_2026-10-25_MANIFEST.json` lists all original paths, hashes and metadata and records the verification.
- `PAST_EXPERIMENTS_2026-10-25_SHA256SUMS.txt` records the ZIP checksum.

The active thesis, WelchSatterthwaiteMI, DifferentialMI and PracticalMIExploration remain in place and unchanged. The existing Welch MI baseline archive was not moved or modified. All 275 active-project tests and the thesis delivery check passed after the old folders were moved. There were no active imports or runtime path dependencies on these folders; historical notes may still refer to their original names.

## Restore

Extract the ZIP into a separate location. It produces a folder named `Past experiments 2026-10-25`, containing the original project folders plus its own README and manifest. Move the projects needed back to the Simulations workspace root under their original names. Old projects may need their related historical projects restored together.

From this Archive directory, verify the ZIP with:

```sh
shasum -a 256 -c PAST_EXPERIMENTS_2026-10-25_SHA256SUMS.txt
```

The ZIP stays local and is excluded from Git because it contains historical generated results and exceeds GitHub's file limit. The manifest, checksum and this guide can be versioned. No commit was made.

## Projects

- `ChiSquaredExploration`
- `EffectiveDFCorrection`
- `EffectiveDFCorrection_Stage10_WeightedSparsityFormula`
- `EffectiveDFCorrection_Stage11_ExactMoments`
- `EffectiveDFCorrection_Stage12_MomentModel`
- `EffectiveDFCorrection_Stage13_JIDTValidation`
- `EffectiveDFCorrection_Stage14_NullComparison`
- `EffectiveDFCorrection_Stage15_LargeAlphabetScratch`
- `EffectiveDFCorrection_Stage2`
- `EffectiveDFCorrection_Stage3`
- `EffectiveDFCorrection_Stage4`
- `EffectiveDFCorrection_Stage5_TPCollapse`
- `EffectiveDFCorrection_Stage6_AlphabetScaling`
- `EffectiveDFCorrection_Stage7_ShapeScaling`
- `EffectiveDFCorrection_Stage8_RobustFit`
- `EffectiveDFCorrection_Stage9_RobustRegressions`
- `InfluenceDfMI`
- `JointEdgeworthMI`
- `PairedDifferentialMI`
- `Perplexity DoF`
- `ProfileDifferentialMI`
- `SaddlepointValidation`
- `Sparse CMI`
