"""Make thesis figures and evidence macros from the frozen experiment outputs."""

from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def find_workspace_root() -> Path:
    """Locate the experiment tree in the workspace or extracted archives."""
    override = os.environ.get("WELCH_MI_WORKSPACE_ROOT")
    candidates = ([Path(override).expanduser().resolve()] if override else [])
    candidates.extend((HERE, *HERE.parents))
    for candidate in candidates:
        if (candidate / "WelchSatterthwaiteMI" / "results" / "thesis_redesign").is_dir():
            return candidate
    raise FileNotFoundError(
        "Could not locate WelchSatterthwaiteMI/results/thesis_redesign. "
        "Extract the experiment supplement beside the thesis source or set "
        "WELCH_MI_WORKSPACE_ROOT."
    )


PROJECT = find_workspace_root() / "WelchSatterthwaiteMI"
RESULTS = PROJECT / "results" / "thesis_redesign"
DISPLAY = pd.read_csv(RESULTS / "display_manifest.csv")
CELLS = pd.read_csv(RESULTS / "cell_results.csv")
VALUES = CELLS[
    [
        "configuration_id",
        "method",
        "unconditional_rejection_rate",
        "valid_rate",
    ]
]
DATA = DISPLAY.merge(VALUES, on="configuration_id", validate="many_to_many")
assert len(DATA) == 2 * len(DISPLAY)

COLORS = {"normal_wald": "#184a70", "expanded_welch": "#b03c78"}
LABELS = {"normal_wald": "Normal Wald", "expanded_welch": "Expanded Welch"}
MARKERS = {"normal_wald": "o", "expanded_welch": "s"}
STYLES = {"normal_wald": "-", "expanded_welch": "--"}
RECORDS: list[dict] = []


def subset(section: str, **filters: object) -> pd.DataFrame:
    rows = DATA.loc[DATA.section.eq(section)].copy()
    for key, value in filters.items():
        if isinstance(value, (tuple, list, set)):
            rows = rows.loc[rows[key].isin(value)]
        elif isinstance(value, float):
            rows = rows.loc[np.isclose(rows[key].astype(float), value)]
        else:
            rows = rows.loc[rows[key].eq(value)]
    if rows.empty:
        raise ValueError(f"Empty figure panel: {section} {filters}")
    return rows


def draw(ax, rows: pd.DataFrame, *, ylim=(0, 1), x_kind="difference") -> None:
    for method in ("normal_wald", "expanded_welch"):
        current = rows.loc[rows.method.eq(method)].sort_values("x_value")
        x = current.x_value.to_numpy(dtype=float)
        y = current.unconditional_rejection_rate.to_numpy(dtype=float)
        ax.plot(
            x, y, label=LABELS[method], color=COLORS[method],
            linestyle=STYLES[method], marker=MARKERS[method],
            linewidth=1.8, markersize=4.5,
        )
        invalid = current.loc[current.valid_rate.lt(0.9)]
        if not invalid.empty:
            ax.scatter(
                invalid.x_value, invalid.unconditional_rejection_rate,
                marker=MARKERS[method], s=42, facecolors="white",
                edgecolors=COLORS[method], linewidths=1.1, zorder=4,
            )
    ax.axhline(0.05, color="#777777", linestyle=":", linewidth=1)
    ax.set_ylim(*ylim)
    if x_kind == "difference":
        ax.set_xlim(0, float(rows.x_value.max()) * 1.015)
    else:
        ax.set_xscale("log")
        ax.set_xticks([1000, 2500, 10000, 50000])
        ax.set_xticklabels(["1k", "2.5k", "10k", "50k"])
    ax.grid(alpha=0.18)
    ax.tick_params(labelsize=9)


def save(name: str, fig, rows: pd.DataFrame, description: str) -> None:
    fig.savefig(HERE / f"{name}.pdf", bbox_inches="tight", metadata={"Creator": "make_figures.py"})
    plt.close(fig)
    RECORDS.append(
        {
            "file": f"figures_rewrite/{name}.pdf",
            "description": description,
            "source_files": ["display_manifest.csv", "cell_results.csv"],
            "sections": sorted(rows.section.unique().tolist()),
            "configuration_ids": sorted(rows.configuration_id.unique().tolist()),
            "rate_column": "unconditional_rejection_rate",
            "denominator": 20000,
        }
    )


def grid(name: str, panels: list[tuple[str, pd.DataFrame]], *, zoom: float | None = 0.15) -> None:
    columns = len(panels)
    rows_count = 2 if zoom is not None else 1
    fig, axes = plt.subplots(rows_count, columns, figsize=(3.55 * columns, 2.95 * rows_count), squeeze=False)
    all_rows = []
    for j, (title, rows) in enumerate(panels):
        all_rows.append(rows)
        draw(axes[0, j], rows)
        axes[0, j].set_title(title, fontsize=11)
        if zoom is not None:
            draw(axes[1, j], rows, ylim=(0, zoom))
            axes[1, j].set_xlabel("True |MI difference| (nats)", fontsize=10)
        else:
            axes[0, j].set_xlabel("True |MI difference| (nats)", fontsize=10)
    axes[0, 0].set_ylabel("Rejection rate", fontsize=10)
    if zoom is not None:
        axes[1, 0].set_ylabel("Rejection rate (zoom)", fontsize=10)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", ncol=2, fontsize=10,
        frameon=False, bbox_to_anchor=(0.5, 0.99),
    )
    top = 0.80 if columns == 1 else 0.88
    fig.subplots_adjust(top=top, wspace=0.28, hspace=0.35)
    save(name, fig, pd.concat(all_rows), "Panels: " + ", ".join(title for title, _ in panels))


def main_landscape() -> None:
    profiles = ["uniform", "same_skew", "different_skew"]
    samples = [10, 100, 1000]
    for shape in ("2x2", "3x3", "5x5", "8x8"):
        for profile in profiles:
            panels = [
                (f"nP = nQ = {n}", subset("main", shape=shape, profile=profile, n_p=n, n_q=n))
                for n in samples
            ]
            grid(f"main_{shape}_{profile}", panels)


def focused() -> None:
    grid(
        "baseline_3x3_different_skew",
        [(f"I0 = {value:g}", subset("baseline", shape="3x3", profile="different_skew", baseline_mi=value, n_p=100))
         for value in (0.0001, 0.001, 0.02)],
    )
    grid(
        "patterns_5x5_different_skew",
        [(f"Changed cells: {pattern}", subset("patterns", shape="5x5", profile="different_skew", pattern=pattern, n_p=100))
         for pattern in ("first", "rare", "spread")],
    )
    # Keep the unequal-sample comparison symmetric in sample allocation and MI direction.
    pairs = [(50, 250), (250, 50)]
    for direction in ("q_higher", "p_higher"):
        grid(
            f"imbalance_3x3_{direction}",
            [(f"nP={n_p}, nQ={n_q}", subset("imbalance", shape="3x3", profile="different_skew", n_p=n_p, n_q=n_q, mi_direction=direction))
             for n_p, n_q in pairs],
        )
    grid(
        "broad_2x2_uniform",
        [("nP=nQ=100", subset("broad_effect", shape="2x2", profile="uniform", n_p=100))],
        zoom=None,
    )
    grid(
        "rectangular_different_skew",
        [(shape, subset("rectangular", shape=shape, profile="different_skew", n_p=100))
         for shape in ("2x3", "3x5")],
    )
    grid(
        "construction_5x5_different_skew",
        [(constructor, subset("construction", shape="5x5", profile="different_skew", baseline_mi=0.02, n_p=100, constructor=constructor))
         for constructor in ("additive", "loglinear")],
    )
    grid(
        "extreme_3x3",
        [(f"P {p:g}, Q {q:g}", subset("extreme", shape="3x3", dominant_p=p, dominant_q=q, n_p=100))
         for p, q in ((0.9, 0.95), (0.99, 0.995), (0.999, 0.9995))],
    )
    grid(
        "independence_2x2",
        [(profile.replace("_", " "), subset("independence", shape="2x2", profile=profile, n_p=100))
         for profile in ("uniform", "same_skew", "different_skew")],
    )


def convergence() -> None:
    panels = []
    for shape in ("2x2", "8x8"):
        for baseline in (0.0001, 0.02):
            panels.append((shape, baseline, subset("convergence", shape=shape, profile="different_skew", baseline_mi=baseline, pattern="first")))
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.5))
    for ax, (shape, baseline, rows) in zip(axes.flat, panels):
        draw(ax, rows, ylim=(0, 0.1), x_kind="sample")
        ax.set_title(f"{shape}, I(P)=I(Q)={baseline:g}", fontsize=11)
        ax.set_xlabel("nP = nQ", fontsize=10)
    axes[0, 0].set_ylabel("Null rejection rate", fontsize=10)
    axes[1, 0].set_ylabel("Null rejection rate", fontsize=10)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, fontsize=10, frameon=False)
    fig.subplots_adjust(top=0.89, hspace=0.42, wspace=0.28)
    save("convergence", fig, pd.concat([panel[2] for panel in panels]), "Different-skew null, first block, both baseline MI values")


def evidence_macros() -> None:
    identifiers = {
        "EightUniformTwenty": "config_313a5e5c05280f9e",
        "TwoUniformThousand": "config_700945d218841f2e",
        "EightSparseFiveAlternative": "config_e9b5baebbe3f5535",
    }
    lines = ["% Generated from results/thesis_redesign/cell_results.csv; do not edit values by hand."]
    for name, identifier in identifiers.items():
        match = CELLS.loc[CELLS.configuration_id.eq(identifier)]
        if set(match.method) != set(LABELS):
            raise ValueError(f"Missing method rows for {identifier}")
        for method, stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = match.loc[match.method.eq(method)].iloc[0]
            lines.append(f"\\newcommand{{\\{name}{stem}Rate}}{{{row.unconditional_rejection_rate:.5f}}}")
            lines.append(f"\\newcommand{{\\{name}{stem}Valid}}{{{row.valid_rate:.5f}}}")
    (HERE / "evidence_values.tex").write_text("\n".join(lines) + "\n")


def main() -> None:
    HERE.mkdir(exist_ok=True)
    main_landscape()
    focused()
    convergence()
    evidence_macros()
    (HERE / "figure_manifest.json").write_text(json.dumps(RECORDS, indent=2) + "\n")
    print(f"Generated {len(RECORDS)} PDF figures from {len(DISPLAY)} display points.")


if __name__ == "__main__":
    main()
