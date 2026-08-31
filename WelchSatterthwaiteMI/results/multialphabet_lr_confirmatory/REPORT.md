# Focused Multi-Alphabet LR Confirmation

This run re-evaluates six exact null configurations selected before the
confirmatory simulation. They include an ordinary control and screening
cases in which constrained LR appeared either better or worse than Wald.
All tests use $\alpha=0.05$.

| Shape | Regime | N | Purpose | Method | FPR | 95% interval | Valid rate |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| 3x3 | Balanced margins | 250 | ordinary control | Constrained LR | 0.0510 | [0.0422, 0.0615] | 1.0000 |
| 3x3 | Balanced margins | 250 | ordinary control | Expanded Welch | 0.0390 | [0.0314, 0.0484] | 1.0000 |
| 3x3 | Balanced margins | 250 | ordinary control | Normal Wald | 0.0475 | [0.0390, 0.0577] | 1.0000 |
| 3x3 | Ultra-skewed margins | 25 | screening LR loss | Constrained LR | 0.0100 | [0.0065, 0.0154] | 1.0000 |
| 3x3 | Ultra-skewed margins | 25 | screening LR loss | Expanded Welch | 0.0605 | [0.0442, 0.0822] | 0.3060 |
| 3x3 | Ultra-skewed margins | 25 | screening LR loss | Normal Wald | 0.0870 | [0.0742, 0.1016] | 0.8165 |
| 5x5 | Balanced margins | 50 | screening LR gain | Constrained LR | 0.0545 | [0.0454, 0.0653] | 1.0000 |
| 5x5 | Balanced margins | 50 | screening LR gain | Expanded Welch | 0.0635 | [0.0536, 0.0750] | 1.0000 |
| 5x5 | Balanced margins | 50 | screening LR gain | Normal Wald | 0.0810 | [0.0698, 0.0938] | 1.0000 |
| 5x5 | Ultra-skewed margins | 50 | screening LR loss | Constrained LR | 0.0210 | [0.0156, 0.0283] | 0.9995 |
| 5x5 | Ultra-skewed margins | 50 | screening LR loss | Expanded Welch | 0.0363 | [0.0279, 0.0470] | 0.7440 |
| 5x5 | Ultra-skewed margins | 50 | screening LR loss | Normal Wald | 0.0478 | [0.0392, 0.0582] | 0.9730 |
| 8x8 | Mildly skewed margins | 25 | largest screening LR gain | Constrained LR | 0.0461 | [0.0376, 0.0563] | 0.9660 |
| 8x8 | Mildly skewed margins | 25 | largest screening LR gain | Expanded Welch | 0.0835 | [0.0722, 0.0965] | 0.9995 |
| 8x8 | Mildly skewed margins | 25 | largest screening LR gain | Normal Wald | 0.0965 | [0.0843, 0.1102] | 1.0000 |
| 8x8 | Strongly skewed margins | 50 | screening LR gain | Constrained LR | 0.0506 | [0.0418, 0.0611] | 0.9985 |
| 8x8 | Strongly skewed margins | 50 | screening LR gain | Expanded Welch | 0.0658 | [0.0557, 0.0777] | 0.9795 |
| 8x8 | Strongly skewed margins | 50 | screening LR gain | Normal Wald | 0.0895 | [0.0778, 0.1028] | 1.0000 |

The intervals quantify simulation uncertainty only. They do not
represent variation over different population tables within a regime.
