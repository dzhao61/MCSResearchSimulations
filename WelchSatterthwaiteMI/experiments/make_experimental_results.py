"""Build the single study document from the two recorded experiments."""
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT = ROOT / 'docs/experiments/EXPERIMENTAL_RESULTS.md'


def extract(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def write_combined(document=DOCUMENT, primary=None, followup=None):
    from make_final_experiment_landscape import _write_document
    from run_design_followup import report

    if primary is None:
        primary = pd.read_csv(ROOT/'results/detection_breakdown_sweep/cell_results.csv')
    if followup is None:
        followup = pd.read_csv(ROOT/'results/design_followup/cell_results.csv')
    with TemporaryDirectory(prefix='mi-report-') as temporary:
        first, second = Path(temporary)/'primary.md', Path(temporary)/'followup.md'
        _write_document(primary, first)
        report(followup, second)
        original, additions = first.read_text(), second.read_text()

    main = extract(original, '### 4.1 Equal sample sizes and the primary dependence arrangement',
                   '### 4.2 Unequal sample sizes')
    main = re.sub(r'#### 4\.1\.(\d+)', r'#### 2.1.\1', main)
    interactions = extract(original, '### 4.3 Other arrangements of dependence', '## 5. Briefing sequence')
    interactions = re.sub(r'#### 4\.3\.(\d+)', r'#### 2.2.\1', interactions)
    blocks = re.split(r'(?=^## \d+\.)', additions, flags=re.M)[1:]
    groups = {3: [], 4: [], 5: [], 6: []}
    for block in blocks:
        title, body = block.split('\n', 1)
        if 'Different margins:' in title:
            section = 3
        elif 'Baseline MI sensitivity:' in title:
            section = 4
        elif 'Reversed sample allocation:' in title:
            section = 5
        elif 'Large-sample null calibration:' in title:
            section = 6
        else:
            raise ValueError(f'Unknown experiment subsection: {title}')
        title = re.sub(r'^## \d+\. ', '', title)
        groups[section].append((title, body.strip()))
    assert [len(groups[s]) for s in groups] == [4, 12, 24, 8]

    introduction = r'''# Experimental Results: Normal Wald and Expanded Welch

This document brings together the original experiment and the subsequent
design follow-up. Each panel represents one fixed regime; results are not
averaged across population definitions, table sizes, or sample sizes. The
follow-up was specified after reviewing the original results. Both protocols
and datasets remain available in the reproducibility section.

## Contents

- [1. How to read the figures and metrics](#1-how-to-read-the-figures-and-metrics)
- [2. Main landscape](#2-main-landscape)
- [3. Different margins](#3-different-margins)
- [4. Baseline MI sensitivity](#4-baseline-mi-sensitivity)
- [5. Unequal sample sizes: both allocations](#5-unequal-sample-sizes-both-allocations)
- [6. Large-sample convergence](#6-large-sample-convergence)
- [7. Protocols and reproducibility](#7-protocols-and-reproducibility)

## 1. How to read the figures and metrics

The test compares $H_0:I(P)=I(Q)$ with $H_1:I(P)\ne I(Q)$ for two independent
multinomial samples. Every plotted point uses 10,000 simulated table pairs,
evaluated by both methods at significance level $\alpha=0.05$.

| Quantity | Meaning |
| --- | --- |
| Rejection rate | Fraction of all simulated pairs for which the method rejects; invalid results count as non-rejections |
| False-positive rate | Rejection rate at zero MI difference; the target is 0.05 |
| Power | Rejection rate at a positive MI difference |
| Valid rate | Fraction of pairs for which the method returns a valid statistic and p-value |
| Conditional rejection rate | Fraction rejected among valid results only |
| Shaded band | Pointwise 95% Wilson interval for Monte Carlo uncertainty in the rejection rate |
| Hollow marker | Valid rate below 0.90; exact validity is reported in the detailed tables |

Blue circles represent Normal Wald and magenta squares represent Expanded
Welch. Read the zero-difference point before comparing power: a method that
already rejects too often under the null can have misleadingly high power.
Expanded Welch uses the same statistic with a heavier-tailed reference, so
it can only reduce rejection relative to Wald. Its value depends on whether
that reduction improves calibration at an acceptable cost in power and validity.

The effect axis is $e$, where the absolute MI difference is $eM$ nats. $M$ is
the smaller of the largest MI values successfully constructed on the original
numerical probe grids. It is a demonstrated numerical range, not a theoretical
maximum. Equal $e$ values in different regimes can therefore represent different
absolute MI differences.

The baseline parameter $b$ sets $I(P)=bM$, while $I(Q)=(b+e)M$. Most regimes
use $b=0.2$; Section 4 varies it explicitly. All power graphs share an $e$ axis
from 0 to 0.6 and a rejection-rate axis from 0 to 1. Section 6 instead plots
sample size on a logarithmic horizontal axis because it examines null convergence.

Balanced margins are uniform. Mild, strong, and ultra margins have one
dominant category with probability 0.70, 0.90, and 0.95, respectively; the
remaining marginal probabilities are equal. There is no minimum expected-count
filter. A minimum expected count is the smallest $n_Pp_{ij}$ or $n_Qq_{ij}$,
using the true joint probabilities rather than a fitted independence model.

Each figure is followed by its specifications. Original-landscape figures
link to exact point-by-point tables; the other sections place those tables
inside expandable details beneath each figure.

## 2. Main landscape

These are the original equal-sample comparisons across table sizes, skewness,
sample sizes, and dependence arrangements. The balanced primary different-shape
nulls are column relabellings of $P$. They are useful invariance controls,
but do not establish performance for different MI-estimator distributions.
Section 3 explicitly compares different margins.

### 2.1 Equal sample sizes and the primary dependence arrangement
'''
    pieces = [introduction.strip(), main,
              '### 2.2 Other arrangements of dependence', interactions]
    headings = {
        3: ('Different margins', 'P has uniform margins and Q has a dominant marginal probability of 0.70. These populations cannot be made identical by relabelling categories. The original dependence arrangements are tuned to the stated MI values.'),
        4: ('Baseline MI sensitivity', 'These comparisons vary b over {0.02, 0.2, 0.6} while holding margins, dependence arrangements, M, and sample sizes fixed. At each e, the absolute MI difference eM therefore stays fixed across baseline levels.'),
        5: ('Unequal sample sizes: both allocations', 'Each figure shows both sample allocations for the same population pairs. The first row gives Q the larger sample; the second gives P the larger sample. The populations are not swapped. The first row reuses the original results; the second contains the follow-up simulations. These figures include all configurations from the original unequal-sample overviews.'),
        6: ('Large-sample convergence', 'These null comparisons use the same populations at nP=nQ in {1000, 2500, 10000, 50000}. The n=1000 points come from the original experiment. The larger samples are diagnostic controls beyond the main study range; the question is whether false-positive rates approach 0.05.'),
    }
    for section, (heading, description) in headings.items():
        pieces.extend([f'## {section}. {heading}', description])
        for index, (title, body) in enumerate(groups[section], 1):
            pieces.extend([f'### {section}.{index} {title}', body])
    pieces.append('''## 7. Protocols and reproducibility

The original run contains 5,672 configurations and 56.72 million simulated
table pairs. The subsequent additions contain 528 new configurations and
5.28 million pairs. Reused points in the combined figures are not new simulations.
Simple Welch and secondary significance levels remain in the datasets.

| Resource | Original experiment | Follow-up |
| --- | --- | --- |
| Protocol | [Original protocol](../../experiments/FINAL_PROTOCOL.json) | [Follow-up protocol](../../experiments/DESIGN_FOLLOWUP_PROTOCOL.json) |
| Results | [All exact results](../../results/detection_breakdown_sweep/cell_results.csv) | [All exact results](../../results/design_followup/cell_results.csv) |
| Populations | [Population definitions](../../results/detection_breakdown_sweep/population_definitions.csv) | [Population definitions](../../results/design_followup/population_definitions.csv) |
| Paired comparisons | [Paired results](../../results/detection_breakdown_sweep/paired_method_results.csv) | [Paired results](../../results/design_followup/paired_method_results.csv) |
| Verification | [Original checks](../../results/detection_breakdown_sweep/verification_checks.json) | [Follow-up checks](../../results/design_followup/verification.json) |

The landscape includes the original power grid and matching null points.
The finer original null-only sample-size grid, including n=2, 3 and 4, remains
in the original results. The two earlier standalone documents are archived in
[the original landscape](archive/FINAL_EXPERIMENT_LANDSCAPE.md) and
[the follow-up report](archive/DESIGN_FOLLOWUP.md).

Regenerate this document from the saved results with
`python experiments/make_experimental_results.py` from the project directory.
The [combined report generator](../../experiments/make_experimental_results.py)
uses the original and follow-up reporting functions. It does not rerun sampling.
''')
    text = '\n\n'.join(pieces) + '\n'
    assert len(re.findall(r'^!\[', text, re.M)) == 68
    document.parent.mkdir(parents=True, exist_ok=True)
    document.write_text(text)
    return document


if __name__ == '__main__':
    print(f'Wrote {write_combined()}')
