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
PROTOCOL = json.loads((RESULTS / "protocol.json").read_text())
REPLICATES = int(PROTOCOL["replicates"])
DISPLAY = pd.read_csv(RESULTS / "display_manifest.csv")
CELLS = pd.read_csv(RESULTS / "cell_results.csv")
RUNTIME = pd.read_csv(RESULTS / "runtime_summary.csv")
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
            "denominator": REPLICATES,
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
                (fr"$n_P=n_Q={n}$", subset("main", shape=shape, profile=profile, n_p=n, n_q=n))
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
            [(fr"$n_P={n_p},\ n_Q={n_q}$", subset("imbalance", shape="3x3", profile="different_skew", n_p=n_p, n_q=n_q, mi_direction=direction))
             for n_p, n_q in pairs],
        )
    grid(
        "broad_2x2_uniform",
        [(r"$n_P=n_Q=100$", subset("broad_effect", shape="2x2", profile="uniform", n_p=100))],
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
        ax.set_xlabel(r"$n_P=n_Q$", fontsize=10)
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

    def add(name: str, value: float | int, digits: int | None = None) -> None:
        rendered = str(int(value)) if digits is None else f"{float(value):.{digits}f}"
        lines.append(f"\\newcommand{{\\{name}}}{{{rendered}}}")

    def one_row(section: str, method: str, **filters: object) -> pd.Series:
        rows = subset(section, **filters)
        rows = rows.loc[rows.method.eq(method)].drop_duplicates("configuration_id")
        if len(rows) != 1:
            raise ValueError(f"Expected one evidence row: {section} {method} {filters}")
        return rows.iloc[0]

    main_null = DATA.loc[DATA.section.eq("main") & DATA.mi_difference.eq(0)].drop_duplicates(
        ["configuration_id", "method"]
    )
    main_meta = main_null[["configuration_id", "n_p"]].drop_duplicates().set_index("configuration_id")
    main_pivot = main_null.pivot(
        index="configuration_id", columns="method", values="unconditional_rejection_rate"
    ).join(main_meta)
    smallest = main_pivot.loc[main_pivot.n_p.eq(5)]
    early = main_pivot.loc[main_pivot.n_p.isin([10, 20])]
    late = main_pivot.loc[main_pivot.n_p.isin([500, 1000])]
    add("MainFiveNullCount", len(smallest))
    add("MainTenTwentyNullCount", len(early))
    add("MainTenTwentyExpandedCloserCount", int(
        ((early.expanded_welch - .05).abs() < (early.normal_wald - .05).abs()).sum()
    ))
    add("MainTenTwentyWaldCloserCount", int(
        ((early.normal_wald - .05).abs() < (early.expanded_welch - .05).abs()).sum()
    ))
    add("MainLateNullCount", len(late))
    add("MainLateWaldCloserCount", int(
        ((late.normal_wald - .05).abs() < (late.expanded_welch - .05).abs()).sum()
    ))
    main_thousand = main_null.loc[main_null.n_p.eq(1000)]
    for method, stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
        values = main_thousand.loc[main_thousand.method.eq(method), "unconditional_rejection_rate"]
        add(f"MainThousand{stem}MinRate", values.min(), 4)
        add(f"MainThousand{stem}MaxRate", values.max(), 4)

    for baseline, stem in ((0.0001, "Tiny"), (0.001, "Small"), (0.02, "Regular")):
        for method, method_stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = one_row(
                "baseline", method, shape="3x3", profile="different_skew",
                baseline_mi=baseline, n_p=100, n_q=100, mi_difference=0.0,
            )
            add(f"Baseline{stem}{method_stem}Rate", row.unconditional_rejection_rate, 4)

    for pattern, stem in (("first", "First"), ("rare", "Rare"), ("spread", "Spread")):
        for method, method_stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = one_row(
                "patterns", method, shape="5x5", profile="different_skew",
                pattern=pattern, baseline_mi=0.0001, n_p=100, n_q=100,
                mi_difference=0.0,
            )
            add(f"Pattern{stem}{method_stem}Rate", row.unconditional_rejection_rate, 4)

    for direction, stem in (("q_higher", "QHigher"), ("p_higher", "PHigher")):
        for method, method_stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = one_row(
                "imbalance", method, shape="3x3", profile="different_skew",
                n_p=50, n_q=250, mi_direction=direction, mi_difference=0.02,
            )
            add(f"Imbalance{stem}{method_stem}Rate", row.unconditional_rejection_rate, 4)

    for constructor, stem in (("additive", "Additive"), ("loglinear", "Loglinear")):
        for method, method_stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = one_row(
                "construction", method, shape="5x5", profile="different_skew",
                constructor=constructor, baseline_mi=0.02, n_p=100, n_q=100,
                mi_difference=0.0,
            )
            add(f"Construction{stem}{method_stem}Rate", row.unconditional_rejection_rate, 4)

    for n_q, stem in ((50, "EqualSmall"), (500, "QFiveHundred")):
        for method, method_stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            row = one_row(
                "imbalance", method, shape="8x8", profile="uniform",
                n_p=50, n_q=n_q, mi_difference=0.0,
            )
            add(f"ImbalanceEight{stem}{method_stem}Rate", row.unconditional_rejection_rate, 4)
    add("ImbalanceEightCorrectionOffset", abs(49 / (2 * 50) - 49 / (2 * 500)), 3)

    for method, stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
        regular = RUNTIME.loc[
            RUNTIME["shape"].eq("3x3") & RUNTIME.profile.eq("different_skew")
            & RUNTIME.n_p.eq(100) & RUNTIME.n_q.eq(100)
            & RUNTIME.mi_difference.eq(0) & RUNTIME.method.eq(method)
        ]
        if len(regular) != 1:
            raise ValueError(f"Expected one runtime row for {method}")
        add(f"RuntimeRegular{stem}Median", regular.iloc[0].median_microseconds, 3)
    (HERE / "evidence_values.tex").write_text("\n".join(lines) + "\n")


def null_band_table() -> None:
    rows = []
    main_null = DATA.loc[DATA.section.eq("main") & DATA.mi_difference.eq(0)].drop_duplicates(
        ["configuration_id", "method"]
    )
    for profile, profile_label in (
        ("uniform", "Uniform"),
        ("same_skew", "Same skew"),
        ("different_skew", "Different skew"),
    ):
        for method, method_label in (
            ("normal_wald", "Normal Wald"),
            ("expanded_welch", "Expanded Welch"),
        ):
            group = main_null.loc[
                main_null.profile.eq(profile) & main_null.method.eq(method)
            ]
            rate = group.unconditional_rejection_rate
            rows.append(
                f"{profile_label} & {method_label} & {int((rate < .025).sum())} & "
                f"{int(rate.between(.025, .075).sum())} & {int((rate > .075).sum())} & "
                f"{int((group.valid_rate < .9).sum())} \\\\"
            )
    content = "\n".join([
        r"\begin{table}[htbp]",
        r"\centering",
        r"\small",
        r"\caption{Location, separately for each method, of the 108 main-grid null configurations relative to the descriptive rejection-rate interval 0.025--0.075. Each profile contains 36 configurations. The final column separately counts configurations with validity below 90\%; it overlaps the three rate-location columns. In particular, all four $n=2$ configurations per profile have zero validity for both methods. Uniform and same-skew are strong nulls; different-skew is the equal-MI weak null. Exact rates and validity are in Appendix~\ref{app:mechanism}.}",
        r"\label{tab:null-band-summary}",
        r"\begin{tabular}{@{}llrrrr@{}}",
        r"\toprule",
        r"Margins & Method & Below & Inside & Above & Validity below 90\%\\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])
    (HERE / "null_band_summary.tex").write_text(content + "\n")


def main() -> None:
    HERE.mkdir(exist_ok=True)
    main_landscape()
    focused()
    convergence()
    evidence_macros()
    null_band_table()
    (HERE / "figure_manifest.json").write_text(json.dumps(RECORDS, indent=2) + "\n")
    print(f"Generated {len(RECORDS)} PDF figures from {len(DISPLAY)} display points.")


if __name__ == "__main__":
    main()
