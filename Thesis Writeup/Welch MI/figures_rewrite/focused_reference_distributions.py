#!/usr/bin/env python3
"""Plot standard normal and Student t densities at their printed dimensions."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, t


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "lines.linewidth": 1.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
    })

    x = np.linspace(-5, 5, 2001)
    fig, ax = plt.subplots(figsize=(118 / 25.4, 74 / 25.4))
    fig.subplots_adjust(left=.14, right=.98, bottom=.19, top=.74)
    ax.plot(x, norm.pdf(x), color="#252525", linewidth=1.6,
            label="Standard normal distribution")
    for degrees, color, style in (
        (3, "#194f78", "--"),
        (10, "#b76b28", "-."),
        (30, "#397f73", ":"),
    ):
        ax.plot(x, t.pdf(x, df=degrees), color=color, linestyle=style,
                label=rf"Student $t$ distribution, $\nu={degrees}$")

    ax.set_xlim(-5, 5)
    ax.set_ylim(0, .42)
    ax.set_xticks([-4, -2, 0, 2, 4])
    ax.set_yticks([0, .1, .2, .3, .4])
    ax.set_xlabel("Standardised statistic")
    ax.set_ylabel("Probability density")
    ax.grid(alpha=.15)
    fig.legend(loc="upper center", bbox_to_anchor=(.5, .97), ncol=2,
               frameon=False, columnspacing=1.0, handlelength=2.7)

    output = Path(__file__).resolve().with_suffix("")
    fig.savefig(output.with_suffix(".pdf"))
    fig.savefig(output.with_suffix(".png"), dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
