# Multi-Alphabet Power Curves

These figures compare Normal Wald, Expanded Welch, and the usable constrained likelihood-ratio test over the same MI-difference range.

- Population MI: $I(P)=0.05$ nats.
- Comparison MI: $I(Q)=0.05+\Delta$ nats.
- Common effects: $\Delta\in\{0,0.005,0.01,0.02,0.035,0.05\}$ nats.
- Significance level: $\alpha=0.05$.
- Rows: balanced, mildly skewed, strongly skewed, and ultra-skewed margins.
- Columns: exact sample size per population.
- All panels and alphabet figures use the same axes.
- Replicates per point by alphabet: `{3: 1000, 4: 750, 5: 500, 8: 250}`.
- The $\Delta=0$ and $0.05$ endpoints are reused from `/Users/danielzhao/MyMac/Masters Degree/Research/Simulations/WelchSatterthwaiteMI/results/multialphabet_lr_screen/results.csv`.

## 3x3

![3x3 power curves](POWER_CURVES_3x3.png)

## 4x4

![4x4 power curves](POWER_CURVES_4x4.png)

## 5x5

![5x5 power curves](POWER_CURVES_5x5.png)

## 8x8

![8x8 power curves](POWER_CURVES_8x8.png)

## Overall numerical summary

| Method | Mean rejection rate | Median rejection rate | Minimum valid rate |
| --- | ---: | ---: | ---: |
| Constrained LR | 0.1027 | 0.0567 | 0.9520 |
| Expanded Welch | 0.1031 | 0.0600 | 0.2800 |
| Normal Wald | 0.1159 | 0.0750 | 0.7680 |

The averages are descriptive only. The individual panels are the primary result because calibration, power, and validity vary substantially by sample size and marginal regime.
