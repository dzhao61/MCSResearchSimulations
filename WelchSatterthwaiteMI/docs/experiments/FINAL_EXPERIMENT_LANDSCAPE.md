# Final Experiment Landscape: Normal Wald versus Expanded Welch

## 1. Purpose

This document presents the complete primary comparison of Normal Wald and
Expanded Welch. Every panel represents one fixed experimental regime. No
result is averaged across table shape, skewness, sample size, population
construction, MI difference, sample-size ratio, or arrangement of dependence.

The test is

$$
H_0:I(P)=I(Q)
\qquad\text{against}\qquad
H_1:I(P)\ne I(Q).
$$

## 2. How to read the figures

The blue circular line is Normal Wald and the magenta square line is Expanded
Welch. The horizontal axis is the scaled MI difference $e$. The zero-difference
point gives the false-positive rate; positive differences give power. The dotted
horizontal line marks the target rejection rate of 0.05 under the null.

Every figure uses the same horizontal range of 0 to 0.60 and the same vertical
range of 0 to 1. A filled marker means that at least 90% of replicates returned
a valid statistic and $p$-value. A hollow marker means that the valid rate was
below 90%.

## 3. Population definitions

A table's shape is its number of rows and columns. Skewness controls its
margins: balanced margins are uniform, while mild, strong, and ultra margins
have dominant probabilities 0.70, 0.90, and 0.95, respectively. There is no
minimum expected-count requirement and no lower sample-size floor beyond the
sample sizes stated in each subsection.

The primary dependence arrangement places higher probability near matching
ordered categories. The additional dependence experiments use the two
arrangements defined explicitly in each subsection table. All observed tables
are independent multinomial samples from fixed population tables $P$ and $Q$.

$M$ is the smaller of the maximum MI values attainable by the fixed $P$ and
$Q$ constructions. Every regime sets $I(P)=0.2M$ and
$I(Q)=(0.2+e)M$. Therefore, the absolute MI difference is
$\lvert I(Q)-I(P)\rvert=eM$ nats. Scaling by $M$ places regimes with
different attainable MI ranges on the same horizontal axis.

## 4. Calibration and power across regimes

Each figure combines calibration and power. Reading a curve from left to right
shows the method's false-positive rate at zero difference and how often it
detects progressively larger MI differences.

### 4.1 Equal sample sizes and the primary dependence arrangement

#### 4.1.1 Shape 2x2: same distribution shape

![2x2 rejection curves for same distribution shape](figures/final_experiment_landscape/power_2x2_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $2\times2$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.6931$, $I(P)pprox0.1386$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.1328$, $I(P)pprox0.02657$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.2 Shape 2x2: different distribution shapes

![2x2 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_2x2_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $2\times2$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.6931$, $I(P)pprox0.1386$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.1328$, $I(P)pprox0.02657$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.3 Shape 2x3: same distribution shape

![2x3 rejection curves for same distribution shape](figures/final_experiment_landscape/power_2x3_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $2\times3$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.4621$, $I(P)pprox0.09242$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.1328$, $I(P)pprox0.02657$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.4 Shape 2x3: different distribution shapes

![2x3 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_2x3_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $2\times3$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.4621$, $I(P)pprox0.09242$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.1328$, $I(P)pprox0.02657$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.5 Shape 3x3: same distribution shape

![3x3 rejection curves for same distribution shape](figures/final_experiment_landscape/power_3x3_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times3$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.095$, $I(P)pprox0.2189$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.4279$, $I(P)pprox0.08558$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.1922$, $I(P)pprox0.03844$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.113$, $I(P)pprox0.0226$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.6 Shape 3x3: different distribution shapes

![3x3 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_3x3_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times3$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.095$, $I(P)pprox0.2189$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.4279$, $I(P)pprox0.08558$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.1922$, $I(P)pprox0.03844$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.113$, $I(P)pprox0.0226$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.7 Shape 3x5: same distribution shape

![3x5 rejection curves for same distribution shape](figures/final_experiment_landscape/power_3x5_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times5$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.844$, $I(P)pprox0.1688$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.4415$, $I(P)pprox0.0883$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.1968$, $I(P)pprox0.03936$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1153$, $I(P)pprox0.02306$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.8 Shape 3x5: different distribution shapes

![3x5 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_3x5_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times5$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox0.844$, $I(P)pprox0.1688$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.4415$, $I(P)pprox0.0883$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.1968$, $I(P)pprox0.03936$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1153$, $I(P)pprox0.02306$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.9 Shape 4x4: same distribution shape

![4x4 rejection curves for same distribution shape](figures/final_experiment_landscape/power_4x4_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $4\times4$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.376$, $I(P)pprox0.2753$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.603$, $I(P)pprox0.1206$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.2754$, $I(P)pprox0.05508$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1609$, $I(P)pprox0.03219$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.10 Shape 4x4: different distribution shapes

![4x4 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_4x4_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $4\times4$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.376$, $I(P)pprox0.2753$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.603$, $I(P)pprox0.1206$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.2754$, $I(P)pprox0.05508$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1609$, $I(P)pprox0.03219$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.11 Shape 4x8: same distribution shape

![4x8 rejection curves for same distribution shape](figures/final_experiment_landscape/power_4x8_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $4\times8$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.374$, $I(P)pprox0.2749$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.5988$, $I(P)pprox0.1198$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.2742$, $I(P)pprox0.05484$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1604$, $I(P)pprox0.03209$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.12 Shape 4x8: different distribution shapes

![4x8 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_4x8_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $4\times8$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.374$, $I(P)pprox0.2749$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.5988$, $I(P)pprox0.1198$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.2742$, $I(P)pprox0.05484$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1604$, $I(P)pprox0.03209$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.13 Shape 5x5: same distribution shape

![5x5 rejection curves for same distribution shape](figures/final_experiment_landscape/power_5x5_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $5\times5$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.467$, $I(P)pprox0.2934$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.7482$, $I(P)pprox0.1496$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.336$, $I(P)pprox0.06721$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1945$, $I(P)pprox0.0389$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.14 Shape 5x5: different distribution shapes

![5x5 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_5x5_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $5\times5$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox1.467$, $I(P)pprox0.2934$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.7482$, $I(P)pprox0.1496$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.336$, $I(P)pprox0.06721$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.1945$, $I(P)pprox0.0389$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.15 Shape 8x8: same distribution shape

![8x8 rejection curves for same distribution shape](figures/final_experiment_landscape/power_8x8_identical_distribution.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $8\times8$ |
| Population construction | Same distribution shape: $P$ and $Q$ use the same margins and dependence arrangement; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox2.021$, $I(P)pprox0.4043$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.9088$, $I(P)pprox0.1818$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.4029$, $I(P)pprox0.08058$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.2309$, $I(P)pprox0.04618$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.1.16 Shape 8x8: different distribution shapes

![8x8 rejection curves for different distribution shapes](figures/final_experiment_landscape/power_8x8_equal_mi_different_shape.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $8\times8$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250, 500, 1000\}$ |
| Vertical graph regime specifications (rows) | {balanced (uniform margins), mild (dominant marginal probability 0.70), strong (0.90), ultra (0.95)} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250), (500,500), (1000,1000)\}$ |
| MI settings by vertical regime | balanced: $Mpprox2.021$, $I(P)pprox0.4043$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>mild: $Mpprox0.9088$, $I(P)pprox0.1818$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>strong: $Mpprox0.4029$, $I(P)pprox0.08058$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$<br>ultra: $Mpprox0.2309$, $I(P)pprox0.04618$, $e$ values $\{0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

### 4.2 Unequal sample sizes

#### 4.2.1 Shape 2x2

![2x2 rejection curves under unequal sample sizes](figures/final_experiment_landscape/imbalance_2x2.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $2\times2$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=5, 10, 20, 50, 100\}$ |
| Vertical graph regime specifications (rows) | $\{\text{strong}, n_Q:n_P=2:1;\ \text{strong}, 5:1;\ \text{strong}, 10:1;\ \text{ultra}, 2:1;\ \text{ultra}, 5:1;\ \text{ultra}, 10:1\}$ |
| Resulting sample sizes | ratio 2:1: $\{(5,10),(10,20),(20,40),(50,100),(100,200)\}$; ratio 5:1: $\{(5,25),(10,50),(20,100),(50,250),(100,500)\}$; ratio 10:1: $\{(5,50),(10,100),(20,200),(50,500),(100,1000)\}$, where each pair is $(n_P,n_Q)$ |
| MI settings by vertical regime | strong, $n_Q:n_P=2:1$: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=5:1$: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=10:1$: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=2:1$: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=5:1$: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=10:1$: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.1, 0.4\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.2.2 Shape 3x3

![3x3 rejection curves under unequal sample sizes](figures/final_experiment_landscape/imbalance_3x3.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times3$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=5, 10, 20, 50, 100\}$ |
| Vertical graph regime specifications (rows) | $\{\text{strong}, n_Q:n_P=2:1;\ \text{strong}, 5:1;\ \text{strong}, 10:1;\ \text{ultra}, 2:1;\ \text{ultra}, 5:1;\ \text{ultra}, 10:1\}$ |
| Resulting sample sizes | ratio 2:1: $\{(5,10),(10,20),(20,40),(50,100),(100,200)\}$; ratio 5:1: $\{(5,25),(10,50),(20,100),(50,250),(100,500)\}$; ratio 10:1: $\{(5,50),(10,100),(20,200),(50,500),(100,1000)\}$, where each pair is $(n_P,n_Q)$ |
| MI settings by vertical regime | strong, $n_Q:n_P=2:1$: $Mpprox0.1922$, $I(P)pprox0.03844$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=5:1$: $Mpprox0.1922$, $I(P)pprox0.03844$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=10:1$: $Mpprox0.1922$, $I(P)pprox0.03844$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=2:1$: $Mpprox0.113$, $I(P)pprox0.0226$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=5:1$: $Mpprox0.113$, $I(P)pprox0.0226$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=10:1$: $Mpprox0.113$, $I(P)pprox0.0226$, $e$ values $\{0, 0.1, 0.4\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.2.3 Shape 5x5

![5x5 rejection curves under unequal sample sizes](figures/final_experiment_landscape/imbalance_5x5.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $5\times5$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=5, 10, 20, 50, 100\}$ |
| Vertical graph regime specifications (rows) | $\{\text{strong}, n_Q:n_P=2:1;\ \text{strong}, 5:1;\ \text{strong}, 10:1;\ \text{ultra}, 2:1;\ \text{ultra}, 5:1;\ \text{ultra}, 10:1\}$ |
| Resulting sample sizes | ratio 2:1: $\{(5,10),(10,20),(20,40),(50,100),(100,200)\}$; ratio 5:1: $\{(5,25),(10,50),(20,100),(50,250),(100,500)\}$; ratio 10:1: $\{(5,50),(10,100),(20,200),(50,500),(100,1000)\}$, where each pair is $(n_P,n_Q)$ |
| MI settings by vertical regime | strong, $n_Q:n_P=2:1$: $Mpprox0.336$, $I(P)pprox0.06721$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=5:1$: $Mpprox0.336$, $I(P)pprox0.06721$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=10:1$: $Mpprox0.336$, $I(P)pprox0.06721$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=2:1$: $Mpprox0.1945$, $I(P)pprox0.0389$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=5:1$: $Mpprox0.1945$, $I(P)pprox0.0389$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=10:1$: $Mpprox0.1945$, $I(P)pprox0.0389$, $e$ values $\{0, 0.1, 0.4\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.2.4 Shape 8x8

![8x8 rejection curves under unequal sample sizes](figures/final_experiment_landscape/imbalance_8x8.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $8\times8$ |
| Population construction | Different distribution shapes: the largest row and column probabilities are moved in $Q$, and its dependence arrangement is reversed; $I(Q)$ is increased according to the listed scaled MI settings |
| Horizontal graph regime specifications (columns) | $\{n_P=5, 10, 20, 50, 100\}$ |
| Vertical graph regime specifications (rows) | $\{\text{strong}, n_Q:n_P=2:1;\ \text{strong}, 5:1;\ \text{strong}, 10:1;\ \text{ultra}, 2:1;\ \text{ultra}, 5:1;\ \text{ultra}, 10:1\}$ |
| Resulting sample sizes | ratio 2:1: $\{(5,10),(10,20),(20,40),(50,100),(100,200)\}$; ratio 5:1: $\{(5,25),(10,50),(20,100),(50,250),(100,500)\}$; ratio 10:1: $\{(5,50),(10,100),(20,200),(50,500),(100,1000)\}$, where each pair is $(n_P,n_Q)$ |
| MI settings by vertical regime | strong, $n_Q:n_P=2:1$: $Mpprox0.4029$, $I(P)pprox0.08058$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=5:1$: $Mpprox0.4029$, $I(P)pprox0.08058$, $e$ values $\{0, 0.1, 0.4\}$<br>strong, $n_Q:n_P=10:1$: $Mpprox0.4029$, $I(P)pprox0.08058$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=2:1$: $Mpprox0.2309$, $I(P)pprox0.04618$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=5:1$: $Mpprox0.2309$, $I(P)pprox0.04618$, $e$ values $\{0, 0.1, 0.4\}$<br>ultra, $n_Q:n_P=10:1$: $Mpprox0.2309$, $I(P)pprox0.04618$, $e$ values $\{0, 0.1, 0.4\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

### 4.3 Other arrangements of dependence

#### 4.3.1 Shape 3x3

![3x3 rejection curves for other arrangements of dependence](figures/final_experiment_landscape/interaction_3x3.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times3$ |
| Population construction | Different distribution shapes. Alternating/repeating compares an alternating high-low arrangement in $P$ with a repeating shifted-diagonal arrangement in $Q$. Fixed irregular compares two irregular arrangements generated once from fixed seeds and then held constant. |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250\}$ |
| Vertical graph regime specifications (rows) | {balanced, alternating/repeating; balanced, fixed irregular; strong, alternating/repeating; strong, fixed irregular; ultra, alternating/repeating; ultra, fixed irregular} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250)\}$ |
| MI settings by vertical regime | balanced, alternating/repeating: $Mpprox0.6337$, $I(P)pprox0.1267$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>balanced, fixed irregular: $Mpprox0.7167$, $I(P)pprox0.1433$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, alternating/repeating: $Mpprox0.1942$, $I(P)pprox0.03884$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, fixed irregular: $Mpprox0.1933$, $I(P)pprox0.03866$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, alternating/repeating: $Mpprox0.1123$, $I(P)pprox0.02247$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, fixed irregular: $Mpprox0.1135$, $I(P)pprox0.02271$, $e$ values $\{0, 0.1, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.3.2 Shape 3x5

![3x5 rejection curves for other arrangements of dependence](figures/final_experiment_landscape/interaction_3x5.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $3\times5$ |
| Population construction | Different distribution shapes. Alternating/repeating compares an alternating high-low arrangement in $P$ with a repeating shifted-diagonal arrangement in $Q$. Fixed irregular compares two irregular arrangements generated once from fixed seeds and then held constant. |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250\}$ |
| Vertical graph regime specifications (rows) | {balanced, alternating/repeating; balanced, fixed irregular; strong, alternating/repeating; strong, fixed irregular; ultra, alternating/repeating; ultra, fixed irregular} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250)\}$ |
| MI settings by vertical regime | balanced, alternating/repeating: $Mpprox0.4563$, $I(P)pprox0.09126$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>balanced, fixed irregular: $Mpprox0.8438$, $I(P)pprox0.1688$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, alternating/repeating: $Mpprox0.08851$, $I(P)pprox0.0177$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, fixed irregular: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, alternating/repeating: $Mpprox0.05135$, $I(P)pprox0.01027$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, fixed irregular: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.1, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.3.3 Shape 5x5

![5x5 rejection curves for other arrangements of dependence](figures/final_experiment_landscape/interaction_5x5.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $5\times5$ |
| Population construction | Different distribution shapes. Alternating/repeating compares an alternating high-low arrangement in $P$ with a repeating shifted-diagonal arrangement in $Q$. Fixed irregular compares two irregular arrangements generated once from fixed seeds and then held constant. |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250\}$ |
| Vertical graph regime specifications (rows) | {balanced, alternating/repeating; balanced, fixed irregular; strong, alternating/repeating; strong, fixed irregular; ultra, alternating/repeating; ultra, fixed irregular} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250)\}$ |
| MI settings by vertical regime | balanced, alternating/repeating: $Mpprox0.6701$, $I(P)pprox0.134$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>balanced, fixed irregular: $Mpprox1.023$, $I(P)pprox0.2046$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, alternating/repeating: $Mpprox0.1972$, $I(P)pprox0.03944$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, fixed irregular: $Mpprox0.01113$, $I(P)pprox0.002227$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, alternating/repeating: $Mpprox0.116$, $I(P)pprox0.02319$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, fixed irregular: $Mpprox0.002633$, $I(P)pprox0.0005266$, $e$ values $\{0, 0.1, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

#### 4.3.4 Shape 8x8

![8x8 rejection curves for other arrangements of dependence](figures/final_experiment_landscape/interaction_8x8.png)

| Figure specification | Exact setting |
| --- | --- |
| Table shape | $8\times8$ |
| Population construction | Different distribution shapes. Alternating/repeating compares an alternating high-low arrangement in $P$ with a repeating shifted-diagonal arrangement in $Q$. Fixed irregular compares two irregular arrangements generated once from fixed seeds and then held constant. |
| Horizontal graph regime specifications (columns) | $\{n_P=n_Q=5, 10, 20, 50, 100, 250\}$ |
| Vertical graph regime specifications (rows) | {balanced, alternating/repeating; balanced, fixed irregular; strong, alternating/repeating; strong, fixed irregular; ultra, alternating/repeating; ultra, fixed irregular} |
| Resulting sample sizes | $\{(n_P,n_Q)=(5,5), (10,10), (20,20), (50,50), (100,100), (250,250)\}$ |
| MI settings by vertical regime | balanced, alternating/repeating: $Mpprox0.6931$, $I(P)pprox0.1386$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>balanced, fixed irregular: $Mpprox1.25$, $I(P)pprox0.2499$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, alternating/repeating: $Mpprox0.2176$, $I(P)pprox0.04353$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>strong, fixed irregular: $Mpprox0.2279$, $I(P)pprox0.04558$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, alternating/repeating: $Mpprox0.1287$, $I(P)pprox0.02575$, $e$ values $\{0, 0.1, 0.4, 0.6\}$<br>ultra, fixed irregular: $Mpprox0.1233$, $I(P)pprox0.02466$, $e$ values $\{0, 0.1, 0.4, 0.6\}$ |
| Horizontal axis within each graph | Scaled MI difference $e$, from 0 to 0.60; the corresponding absolute difference is $eM$ nats |
| Vertical axis within each graph | Unconditional rejection rate from 0 to 1; an invalid result counts as a non-rejection |
| Methods | {Normal Wald, Expanded Welch} |
| Test and significance level | Two-sided test of $H_0:I(P)=I(Q)$ at $\alpha=0.05$ |
| Reference line | Rejection rate 0.05 |
| Validity notation | Filled marker: valid rate at least 0.90; hollow marker: valid rate below 0.90 |
| Replicates | 10,000 independently simulated table pairs per plotted point |

## 5. Briefing sequence

1. Read the zero-difference point to assess false-positive control.
2. Check whether the marker is hollow before interpreting a low rejection rate.
3. Follow both curves to the right to compare power at the same scaled MI
   differences $e$.
4. Compare panels horizontally to change sample size while holding the row
   regime fixed.
5. Compare panels vertically to change skewness, imbalance, or dependence
   arrangement while holding the column regime fixed.

## 6. Reproducibility

The figures and this document are generated by
[`../../experiments/make_final_experiment_landscape.py`](../../experiments/make_final_experiment_landscape.py)
from
[`../../results/detection_breakdown_sweep/cell_results.csv`](../../results/detection_breakdown_sweep/cell_results.csv).
The generator verifies the frozen configuration counts and rejects duplicate
or incomplete curves rather than averaging them.
