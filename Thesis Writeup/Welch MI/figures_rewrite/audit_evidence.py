"""Check manuscript headline values against the frozen simulation records."""

from __future__ import annotations

import json
import hashlib
import os
import re
import sys
from pathlib import Path

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


WORKSPACE = find_workspace_root()
RESULTS = WORKSPACE / "WelchSatterthwaiteMI" / "results" / "thesis_redesign"
MECHANISM = WORKSPACE / "WelchSatterthwaiteMI" / "results" / "thesis_mechanism_check"
EXPERIMENTS = WORKSPACE / "WelchSatterthwaiteMI" / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from thesis_redesign_core import build_manifests  # noqa: E402

DISPLAY = pd.read_csv(RESULTS / "display_manifest.csv")
CONFIGURATIONS = pd.read_csv(RESULTS / "configuration_manifest.csv")
POPULATIONS = pd.read_csv(RESULTS / "population_definitions.csv")
CELLS = pd.read_csv(RESULTS / "cell_results.csv")
RUNTIME = pd.read_csv(RESULTS / "runtime_summary.csv")
PAIRED = pd.read_csv(RESULTS / "paired_method_results.csv")


def equal(actual: float, expected: float, *, tolerance: float = 5e-6) -> None:
    assert np.isclose(actual, expected, atol=tolerance, rtol=0), (actual, expected)


def result(configuration_id: str, method: str, column: str) -> float:
    rows = CELLS.loc[
        CELLS.configuration_id.eq(configuration_id) & CELLS.method.eq(method)
    ]
    assert len(rows) == 1, (configuration_id, method, len(rows))
    return float(rows.iloc[0][column])


def display_subset(section: str, **filters: object) -> pd.DataFrame:
    """Select the display rows that a manuscript figure is required to use."""
    rows = DISPLAY.loc[DISPLAY.section.eq(section)].copy()
    for column, value in filters.items():
        if isinstance(value, (tuple, list, set)):
            rows = rows.loc[rows[column].isin(value)]
        elif isinstance(value, float):
            rows = rows.loc[np.isclose(rows[column].astype(float), value)]
        else:
            rows = rows.loc[rows[column].eq(value)]
    assert not rows.empty, (section, filters)
    return rows


def expected_figure_sources() -> dict[str, pd.DataFrame]:
    """Reconstruct all thesis figure selections independently of the plotter."""
    expected: dict[str, pd.DataFrame] = {}
    for shape in ("2x2", "3x3", "5x5", "8x8"):
        for profile in ("uniform", "same_skew", "different_skew"):
            expected[f"figures_rewrite/main_{shape}_{profile}.pdf"] = display_subset(
                "main", shape=shape, profile=profile,
                n_p=(10, 100, 1000), n_q=(10, 100, 1000),
            )
    expected["figures_rewrite/baseline_3x3_different_skew.pdf"] = display_subset(
        "baseline", shape="3x3", profile="different_skew",
        baseline_mi=(0.0001, 0.001, 0.02), n_p=100, n_q=100,
    )
    expected["figures_rewrite/patterns_5x5_different_skew.pdf"] = display_subset(
        "patterns", shape="5x5", profile="different_skew",
        pattern=("first", "rare", "spread"), baseline_mi=0.0001,
        n_p=100, n_q=100,
    )
    for direction in ("q_higher", "p_higher"):
        expected[f"figures_rewrite/imbalance_3x3_{direction}.pdf"] = display_subset(
            "imbalance", shape="3x3", profile="different_skew",
            n_p=(50, 250), n_q=(50, 250), mi_direction=direction,
        ).loc[lambda frame: frame.n_p.ne(frame.n_q)]
    expected["figures_rewrite/broad_2x2_uniform.pdf"] = display_subset(
        "broad_effect", shape="2x2", profile="uniform", n_p=100, n_q=100,
    )
    expected["figures_rewrite/rectangular_different_skew.pdf"] = display_subset(
        "rectangular", shape=("2x3", "3x5"), profile="different_skew",
        n_p=100, n_q=100,
    )
    expected["figures_rewrite/construction_5x5_different_skew.pdf"] = display_subset(
        "construction", shape="5x5", profile="different_skew",
        baseline_mi=0.02, constructor=("additive", "loglinear"),
        n_p=100, n_q=100,
    )
    expected["figures_rewrite/extreme_3x3.pdf"] = display_subset(
        "extreme", shape="3x3", dominant_p=(0.9, 0.99, 0.999),
        dominant_q=(0.95, 0.995, 0.9995), n_p=100, n_q=100,
    )
    expected["figures_rewrite/independence_2x2.pdf"] = display_subset(
        "independence", shape="2x2",
        profile=("uniform", "same_skew", "different_skew"), n_p=100, n_q=100,
    )
    expected["figures_rewrite/convergence.pdf"] = display_subset(
        "convergence", shape=("2x2", "8x8"), profile="different_skew",
        baseline_mi=(0.0001, 0.02), pattern="first",
    )
    return expected


def selected_results(section: str, **filters: object) -> pd.DataFrame:
    selected = display_subset(section, **filters)
    return selected.merge(
        CELLS[[
            "configuration_id", "method", "unconditional_rejection_rate",
            "valid_rate", "wilson_95_low", "wilson_95_high",
        ]],
        on="configuration_id", validate="many_to_many",
    ).drop_duplicates(["configuration_id", "method"])


def claim_value(rows: pd.DataFrame, method: str, column: str = "unconditional_rejection_rate") -> float:
    match = rows.loc[rows.method.eq(method), column]
    assert len(match) == 1, (method, column, len(match))
    return float(match.iloc[0])


def main() -> None:
    protocol_path = EXPERIMENTS / "THESIS_REDESIGN_PROTOCOL.json"
    protocol = json.loads(protocol_path.read_text())
    saved_protocol = json.loads((RESULTS / "protocol.json").read_text())
    metadata = json.loads((RESULTS / "run_metadata.json").read_text())
    assert protocol == saved_protocol
    protocol_hash = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    assert protocol_hash == metadata["protocol_sha256"]
    assert metadata["status"] == "complete" and metadata["profile"] == "full"
    assert protocol["status"] == "frozen_for_confirmatory_run"
    assert protocol["replicates"] == 20000 and protocol["alpha"] == 0.05

    expected_display, expected_configurations, expected_populations, _ = build_manifests(protocol)
    pd.testing.assert_frame_equal(
        expected_display.reset_index(drop=True), DISPLAY.reset_index(drop=True),
        check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-14,
    )
    pd.testing.assert_frame_equal(
        expected_configurations.reset_index(drop=True), CONFIGURATIONS.reset_index(drop=True),
        check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-14,
    )
    pd.testing.assert_frame_equal(
        expected_populations.reset_index(drop=True), POPULATIONS.reset_index(drop=True),
        check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-14,
    )

    section_counts = DISPLAY.groupby("section").agg(
        display_slots=("display_id", "size"),
        unique_configurations=("configuration_id", "nunique"),
    )
    expected_section_counts = {
        "main": (648, 648), "baseline": (648, 648),
        "patterns": (144, 144), "imbalance": (1152, 1056),
        "broad_effect": (162, 162), "rectangular": (108, 108),
        "construction": (432, 432), "extreme": (315, 315),
        "rare_stress": (140, 140), "independence": (144, 144),
        "convergence": (108, 108),
    }
    for section, expected in expected_section_counts.items():
        actual = tuple(int(value) for value in section_counts.loc[section])
        assert actual == expected, (section, actual, expected)

    assert json.loads((RESULTS / "verification.json").read_text())["all_pass"]
    assert json.loads((RESULTS / "report_verification.json").read_text())["all_pass"]
    assert DISPLAY.configuration_id.nunique() == 3111
    assert len(DISPLAY) == 4001
    assert len(CONFIGURATIONS) == metadata["unique_configurations"] == 3111
    assert len(POPULATIONS) == metadata["population_pairs"] == 534
    assert metadata["table_pairs"] == len(CONFIGURATIONS) * protocol["replicates"]
    assert CONFIGURATIONS.replicates.eq(protocol["replicates"]).all()
    minimum_expected = np.minimum(
        CONFIGURATIONS.merge(
            POPULATIONS[["pair_id", "minimum_probability_p", "minimum_probability_q"]],
            on="pair_id", validate="many_to_one",
        ).eval("n_p * minimum_probability_p"),
        CONFIGURATIONS.merge(
            POPULATIONS[["pair_id", "minimum_probability_p", "minimum_probability_q"]],
            on="pair_id", validate="many_to_one",
        ).eval("n_q * minimum_probability_q"),
    )
    assert float(minimum_expected.min()) < 1e-8
    assert set(CONFIGURATIONS["shape"]) == {"2x2", "2x3", "3x3", "3x5", "5x5", "8x8"}
    assert float(CONFIGURATIONS["dominant_q"].max()) == 0.9995
    assert len(CELLS) == 2 * DISPLAY.configuration_id.nunique()
    assert len(PAIRED) == DISPLAY.configuration_id.nunique()
    assert PAIRED.method_a.eq("expanded_welch").all()
    assert PAIRED.method_b.eq("normal_wald").all()
    assert PAIRED.only_method_a_rejects.eq(0).all()
    assert (
        PAIRED.both_reject + PAIRED.neither_rejects
        + PAIRED.only_method_a_rejects + PAIRED.only_method_b_rejects
        == PAIRED.replicates
    ).all()

    anchors = {
        "config_313a5e5c05280f9e": (0.06870, 0.05695, 1, 1),
        "config_700945d218841f2e": (0.04450, 0.03865, 1, 1),
        "config_e9b5baebbe3f5535": (0.30865, 0, 0.83840, 0.31415),
    }
    for configuration_id, (wald_rate, expanded_rate, wald_valid, expanded_valid) in anchors.items():
        for method, rate, valid in (
            ("normal_wald", wald_rate, wald_valid),
            ("expanded_welch", expanded_rate, expanded_valid),
        ):
            equal(result(configuration_id, method, "unconditional_rejection_rate"), rate)
            equal(result(configuration_id, method, "valid_rate"), valid)

    paired_examples = {
        "config_313a5e5c05280f9e": (0.01175, 0.010257, 0.013243),
        "config_700945d218841f2e": (0.00585, 0.004793, 0.006907),
    }
    for configuration_id, (gap, low, high) in paired_examples.items():
        row = PAIRED.loc[PAIRED.configuration_id.eq(configuration_id)].iloc[0]
        assert row.method_a == "expanded_welch" and row.method_b == "normal_wald"
        equal(-row.rejection_rate_difference_a_minus_b, gap)
        equal(-row.paired_95_high, low)
        equal(-row.paired_95_low, high)

    display_results = DISPLAY.merge(
        CELLS[["configuration_id", "method", "unconditional_rejection_rate", "valid_rate"]],
        on="configuration_id",
        validate="many_to_many",
    )
    null_main = display_results.loc[
        display_results.section.eq("main") & display_results.mi_difference.eq(0)
    ]
    paired = null_main.pivot(index="configuration_id", columns="method", values="unconditional_rejection_rate")
    specs = DISPLAY.loc[
        DISPLAY.section.eq("main") & DISPLAY.mi_difference.eq(0),
        ["configuration_id", "n_p", "shape", "profile"],
    ].drop_duplicates().set_index("configuration_id")
    paired = paired.join(specs, validate="one_to_one")
    smallest = paired.loc[paired.n_p.eq(5)]
    early = paired.loc[paired.n_p.isin([10, 20])]
    late = paired.loc[paired.n_p.isin([500, 1000])]
    assert len(smallest) == 12 and len(early) == 24 and len(late) == 24
    assert smallest.expanded_welch.eq(0).all()
    early_expanded_closer = (
        (early.expanded_welch - .05).abs() < (early.normal_wald - .05).abs()
    ).sum()
    early_wald_closer = (
        (early.normal_wald - .05).abs() < (early.expanded_welch - .05).abs()
    ).sum()
    late_wald_closer = (
        (late.normal_wald - .05).abs() < (late.expanded_welch - .05).abs()
    ).sum()
    assert early_expanded_closer == 15 and early_wald_closer == 9
    assert late_wald_closer == 24

    smallest_expanded = null_main.loc[
        null_main.n_p.eq(5) & null_main.method.eq("expanded_welch")
    ]
    equal(smallest_expanded.valid_rate.min(), 0.20820)
    equal(smallest_expanded.valid_rate.max(), 0.99085)
    uniform_larger_shapes = smallest_expanded.loc[
        smallest_expanded.profile.eq("uniform")
        & smallest_expanded["shape"].isin(["3x3", "5x5", "8x8"])
    ]
    assert len(uniform_larger_shapes) == 3
    assert uniform_larger_shapes.valid_rate.gt(.9).all()

    expected_null_summary = {
        ("uniform", "normal_wald"): (10, 18, 8, 4),
        ("uniform", "expanded_welch"): (19, 16, 1, 5),
        ("same_skew", "normal_wald"): (14, 15, 7, 8),
        ("same_skew", "expanded_welch"): (25, 11, 0, 12),
        ("different_skew", "normal_wald"): (9, 16, 11, 8),
        ("different_skew", "expanded_welch"): (19, 13, 4, 12),
    }
    for (profile, method), expected in expected_null_summary.items():
        rows = null_main.loc[
            null_main.profile.eq(profile) & null_main.method.eq(method)
        ]
        observed = (
            int((rows.unconditional_rejection_rate < .025).sum()),
            int(rows.unconditional_rejection_rate.between(.025, .075).sum()),
            int((rows.unconditional_rejection_rate > .075).sum()),
            int((rows.valid_rate < .9).sum()),
        )
        assert observed == expected

    main_thousand = null_main.loc[null_main.n_p.eq(1000)]
    for method, expected_range in {
        "normal_wald": (0.02280, 0.04530),
        "expanded_welch": (0.02115, 0.03925),
    }.items():
        values = main_thousand.loc[
            main_thousand.method.eq(method), "unconditional_rejection_rate"
        ]
        equal(values.min(), expected_range[0])
        equal(values.max(), expected_range[1])

    for baseline, expected_rates in {
        0.0001: (0.01930, 0.00170),
        0.001: (0.01455, 0.00160),
        0.02: (0.01710, 0.00830),
    }.items():
        rows = selected_results(
            "baseline", shape="3x3", profile="different_skew",
            baseline_mi=baseline, n_p=100, n_q=100, mi_difference=0.0,
        )
        equal(claim_value(rows, "normal_wald"), expected_rates[0])
        equal(claim_value(rows, "expanded_welch"), expected_rates[1])
        assert rows.valid_rate.eq(1).all()

    for pattern, expected_rates in {
        "first": (0.01685, 0.00390),
        "rare": (0.01700, 0.00440),
        "spread": (0.01605, 0.00410),
    }.items():
        rows = selected_results(
            "patterns", shape="5x5", profile="different_skew",
            pattern=pattern, baseline_mi=0.0001, n_p=100, n_q=100,
            mi_difference=0.0,
        )
        equal(claim_value(rows, "normal_wald"), expected_rates[0])
        equal(claim_value(rows, "expanded_welch"), expected_rates[1])

    for direction, expected_rates in {
        "q_higher": (0.09940, 0.02470),
        "p_higher": (0.04950, 0.02325),
    }.items():
        rows = selected_results(
            "imbalance", shape="3x3", profile="different_skew",
            n_p=50, n_q=250, mi_direction=direction, mi_difference=0.02,
        )
        equal(claim_value(rows, "normal_wald"), expected_rates[0])
        equal(claim_value(rows, "expanded_welch"), expected_rates[1])
        assert rows.valid_rate.eq(1).all()

    for constructor, expected_rates in {
        "additive": (0.02500, 0.01360),
        "loglinear": (0.01815, 0.01190),
    }.items():
        rows = selected_results(
            "construction", shape="5x5", profile="different_skew",
            constructor=constructor, baseline_mi=0.02, n_p=100, n_q=100,
            mi_difference=0.0,
        )
        equal(claim_value(rows, "normal_wald"), expected_rates[0])
        equal(claim_value(rows, "expanded_welch"), expected_rates[1])
        assert rows.valid_rate.eq(1).all()

    extreme = selected_results(
        "extreme", shape="3x3", dominant_p=0.999, dominant_q=0.9995,
        n_p=100, n_q=100, mi_difference=0.0,
    )
    equal(claim_value(extreme, "normal_wald", "valid_rate"), 0.01180)
    equal(claim_value(extreme, "expanded_welch", "valid_rate"), 0.00005)
    assert extreme.unconditional_rejection_rate.eq(0).all()
    less_extreme = selected_results(
        "extreme", shape="3x3", dominant_p=0.9, dominant_q=0.95,
        n_p=100, n_q=100, mi_difference=0.0,
    )
    equal(claim_value(less_extreme, "normal_wald"), 0.07005)
    equal(claim_value(less_extreme, "expanded_welch"), 0.00875)

    independence = selected_results(
        "independence", shape="2x2", profile="uniform",
        n_p=100, n_q=100, mi_difference=0.0,
    )
    equal(claim_value(independence, "normal_wald"), 0.00025)
    equal(claim_value(independence, "expanded_welch"), 0.00010)

    converged = display_results.loc[
        display_results.section.eq("convergence")
        & display_results.pattern.eq("first")
        & display_results.n_p.eq(50000)
        & display_results.mi_difference.eq(0)
    ]
    for baseline, expected in {
        0.02: {"normal_wald": (0.04700, 0.05265), "expanded_welch": (0.04655, 0.05255)},
        0.0001: {"normal_wald": (0.00890, 0.02795), "expanded_welch": (0.00755, 0.01380)},
    }.items():
        subset = converged.loc[np.isclose(converged.baseline_mi, baseline)]
        assert subset.configuration_id.nunique() == 12
        for method, (low, high) in expected.items():
            values = subset.loc[subset.method.eq(method), "unconditional_rejection_rate"]
            equal(values.min(), low)
            equal(values.max(), high)

    timing = RUNTIME.drop_duplicates(
        ["shape", "profile", "n_p", "n_q", "baseline_mi", "mi_difference"]
    )
    assert len(timing) == 60
    assert 1.72 < timing.expanded_to_wald_ratio.median() < 1.79
    for shape, (wald_time, wald_q1, wald_q3, expanded_time, expanded_q1, expanded_q3) in {
        "2x2": (85.833, 85.53075, 86.333, 150.041, 149.417, 151.3015),
        "3x3": (85.083, 84.58375, 85.59425, 149.979, 148.9065, 150.917),
        "3x5": (85.208, 84.875, 85.458, 150.125, 149.541, 150.8855),
        "5x5": (85.292, 85.083, 85.66625, 149.208, 148.48975, 150.0935),
        "8x8": (88.041, 87.08375, 88.93775, 153.4375, 152.375, 154.8435),
    }.items():
        rows = RUNTIME.loc[
            RUNTIME["shape"].eq(shape) & RUNTIME.profile.eq("different_skew")
            & RUNTIME.n_p.eq(100) & RUNTIME.n_q.eq(100)
            & RUNTIME.mi_difference.eq(0)
        ]
        assert len(rows) == 2
        for method, expected in {
            "normal_wald": (wald_time, wald_q1, wald_q3),
            "expanded_welch": (expanded_time, expanded_q1, expanded_q3),
        }.items():
            row = rows.loc[rows.method.eq(method)].iloc[0]
            for column, value in zip(
                ("median_microseconds", "q1_microseconds", "q3_microseconds"), expected
            ):
                equal(float(row[column]), value)

    figures = json.loads((HERE / "figure_manifest.json").read_text())
    expected_figures = expected_figure_sources()
    assert len(figures) == len(expected_figures) == 22
    assert len({figure["file"] for figure in figures}) == 22
    for figure in figures:
        assert figure["file"] in expected_figures, figure["file"]
        expected_rows = expected_figures[figure["file"]]
        expected_ids = sorted(expected_rows.configuration_id.unique().tolist())
        assert figure["configuration_ids"] == expected_ids, figure["file"]
        assert figure["sections"] == sorted(expected_rows.section.unique().tolist())
        assert figure["source_files"] == ["display_manifest.csv", "cell_results.csv"]
        assert figure["rate_column"] == "unconditional_rejection_rate"
        assert figure["denominator"] == int(protocol["replicates"])
        pdf = HERE / Path(figure["file"]).name
        assert pdf.is_file() and pdf.stat().st_size > 5000
        assert pdf.read_bytes()[:5] == b"%PDF-"

        plotted = CELLS.loc[CELLS.configuration_id.isin(expected_ids)]
        assert len(plotted) == 2 * len(expected_ids)
        assert plotted.replicates.eq(int(protocol["replicates"])).all()
        assert plotted.method.groupby(plotted.configuration_id).nunique().eq(2).all()
        assert plotted.unconditional_rejection_rate.between(0, 1).all()
        assert plotted.valid_rate.between(0, 1).all()

    macro_text = (HERE / "evidence_values.tex").read_text()
    assert macro_text.startswith(
        "% Generated from results/thesis_redesign/cell_results.csv; do not edit values by hand.\n"
    )
    macros = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", macro_text))

    def macro(name: str, value: float | int, digits: int | None = None) -> None:
        expected = str(int(value)) if digits is None else f"{float(value):.{digits}f}"
        assert macros[name] == expected, (name, macros.get(name), expected)

    for name, configuration_id in {
        "EightUniformTwenty": "config_313a5e5c05280f9e",
        "TwoUniformThousand": "config_700945d218841f2e",
        "EightSparseFiveAlternative": "config_e9b5baebbe3f5535",
    }.items():
        for method, stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
            macro(
                f"{name}{stem}Rate",
                result(configuration_id, method, "unconditional_rejection_rate"),
                5,
            )
            macro(
                f"{name}{stem}Valid",
                result(configuration_id, method, "valid_rate"),
                5,
            )
    macro("MainFiveNullCount", len(smallest))
    macro("MainTenTwentyNullCount", len(early))
    macro("MainTenTwentyExpandedCloserCount", early_expanded_closer)
    macro("MainTenTwentyWaldCloserCount", early_wald_closer)
    macro("MainLateNullCount", len(late))
    macro("MainLateWaldCloserCount", late_wald_closer)
    for method, stem in (("normal_wald", "Wald"), ("expanded_welch", "Expanded")):
        values = main_thousand.loc[
            main_thousand.method.eq(method), "unconditional_rejection_rate"
        ]
        macro(f"MainThousand{stem}MinRate", values.min(), 4)
        macro(f"MainThousand{stem}MaxRate", values.max(), 4)

    for baseline, stem in ((0.0001, "Tiny"), (0.001, "Small"), (0.02, "Regular")):
        rows = selected_results(
            "baseline", shape="3x3", profile="different_skew",
            baseline_mi=baseline, n_p=100, n_q=100, mi_difference=0.0,
        )
        macro(f"Baseline{stem}WaldRate", claim_value(rows, "normal_wald"), 4)
        macro(f"Baseline{stem}ExpandedRate", claim_value(rows, "expanded_welch"), 4)
    for pattern, stem in (("first", "First"), ("rare", "Rare"), ("spread", "Spread")):
        rows = selected_results(
            "patterns", shape="5x5", profile="different_skew", pattern=pattern,
            baseline_mi=0.0001, n_p=100, n_q=100, mi_difference=0.0,
        )
        macro(f"Pattern{stem}WaldRate", claim_value(rows, "normal_wald"), 4)
        macro(f"Pattern{stem}ExpandedRate", claim_value(rows, "expanded_welch"), 4)
    for direction, stem in (("q_higher", "QHigher"), ("p_higher", "PHigher")):
        rows = selected_results(
            "imbalance", shape="3x3", profile="different_skew", n_p=50, n_q=250,
            mi_direction=direction, mi_difference=0.02,
        )
        macro(f"Imbalance{stem}WaldRate", claim_value(rows, "normal_wald"), 4)
        macro(f"Imbalance{stem}ExpandedRate", claim_value(rows, "expanded_welch"), 4)
    for constructor, stem in (("additive", "Additive"), ("loglinear", "Loglinear")):
        rows = selected_results(
            "construction", shape="5x5", profile="different_skew",
            constructor=constructor, baseline_mi=0.02, n_p=100, n_q=100,
            mi_difference=0.0,
        )
        macro(f"Construction{stem}WaldRate", claim_value(rows, "normal_wald"), 4)
        macro(f"Construction{stem}ExpandedRate", claim_value(rows, "expanded_welch"), 4)
    for n_q, stem in ((50, "EqualSmall"), (500, "QFiveHundred")):
        rows = selected_results(
            "imbalance", shape="8x8", profile="uniform", n_p=50, n_q=n_q,
            mi_difference=0.0,
        )
        macro(f"ImbalanceEight{stem}WaldRate", claim_value(rows, "normal_wald"), 4)
        macro(f"ImbalanceEight{stem}ExpandedRate", claim_value(rows, "expanded_welch"), 4)
        assert rows.valid_rate.eq(1).all()
    macro("ImbalanceEightCorrectionOffset", abs(49 / (2 * 50) - 49 / (2 * 500)), 3)
    manuscript = (HERE.parent / "chapters_rewrite/06_results.tex").read_text()
    used_generated = set(re.findall(r"\\([A-Z][A-Za-z0-9]+(?:Rate|Valid|Count|Median|Offset))", manuscript))
    assert used_generated <= macros.keys(), sorted(used_generated - macros.keys())

    null_band = (HERE / "null_band_summary.tex").read_text()
    for profile, method, expected in (
        ("Uniform", "Normal Wald", (10, 18, 8, 4)),
        ("Uniform", "Expanded Welch", (19, 16, 1, 5)),
        ("Same skew", "Normal Wald", (14, 15, 7, 8)),
        ("Same skew", "Expanded Welch", (25, 11, 0, 12)),
        ("Different skew", "Normal Wald", (9, 16, 11, 8)),
        ("Different skew", "Expanded Welch", (19, 13, 4, 12)),
    ):
        assert f"{profile} & {method} & {' & '.join(map(str, expected))} \\\\" in null_band

    mechanism_rates = pd.read_csv(MECHANISM / "ablation_rates.csv")
    mechanism_diagnostics = pd.read_csv(MECHANISM / "denominator_diagnostics.csv")
    mechanism_components = pd.read_csv(MECHANISM / "component_diagnostics.csv")
    mechanism_metadata = json.loads((MECHANISM / "metadata.json").read_text())
    assert mechanism_metadata["configurations"] == 809
    expected_mechanism_methods = {
        "normal_wald",
        "hutcheson_welch",
        "simple_welch",
        "kurtosis_welch",
        "expanded_welch",
        "observed_support_wald",
    }
    assert len(mechanism_rates) == 809 * len(expected_mechanism_methods)
    assert set(mechanism_rates.method) == expected_mechanism_methods
    assert mechanism_rates.groupby("configuration_id").method.nunique().eq(6).all()
    assert mechanism_diagnostics.configuration_id.nunique() == 169
    assert len(mechanism_components) == 2 * 169
    mechanism_anchor = mechanism_diagnostics.loc[
        mechanism_diagnostics.configuration_id.eq("config_f67e74127a56dc37")
    ].iloc[0]
    equal(mechanism_anchor.normal_wald_rate, 0.01660)
    equal(mechanism_anchor.independent_mc_sd_rate, 0.05510)
    equal(mechanism_anchor.population_first_order_sd_rate, 0.09760)
    equal(mechanism_anchor.mean_se2_over_empirical_var, 1.169852, tolerance=5e-7)
    equal(mechanism_anchor.empirical_var_over_first_order, 1.424926, tolerance=5e-7)
    representative = mechanism_components.loc[
        mechanism_components.configuration_id.isin([
            "config_f67e74127a56dc37",
            "config_1b6b2afc5ccb1291",
        ])
    ].copy()
    assert len(representative) == 4
    interaction_df = 4
    representative_sample_size = representative.n_p.where(
        representative.population.eq("p"), representative.n_q
    )
    representative["local_moment_df"] = (
        (representative_sample_size * representative.v + interaction_df) ** 2
        / (2 * representative_sample_size * representative.v + interaction_df)
    )
    expected_local = {
        (100, "p"): 5.54624,
        (100, "q"): 5.76934,
        (1000, "p"): 25.41624,
        (1000, "q"): 27.86032,
    }
    for row in representative.itertuples():
        equal(row.local_moment_df, expected_local[(row.n_p, row.population)], tolerance=5e-5)
    unequal_components = mechanism_components.loc[
        mechanism_components.n_p.ne(mechanism_components.n_q)
    ].copy()
    unequal_sample_size = unequal_components.n_p.where(
        unequal_components.population.eq("p"), unequal_components.n_q
    )
    unequal_shape = unequal_components["shape"].str.extract(r"(\d+)x(\d+)").astype(int)
    unequal_d = (unequal_shape[0] - 1) * (unequal_shape[1] - 1)
    unequal_components["local_moment_df"] = (
        (unequal_sample_size * unequal_components.v + unequal_d) ** 2
        / (2 * unequal_sample_size * unequal_components.v + unequal_d)
    )
    assert len(unequal_components) == 12
    assert unequal_components.local_moment_df.notna().all()
    assert (HERE / "mechanism_ablation.pdf").read_bytes()[:5] == b"%PDF-"
    null_table = (HERE / "main_null_table.tex").read_text()
    shape_prefixes = ("2x2 &", "3x3 &", "5x5 &", "8x8 &")
    assert sum(line.startswith(shape_prefixes) for line in null_table.splitlines()) == 108

    print("PASS: protocol reconstruction, family counts, manuscript claims, 22 confirmatory figures, supplementary mechanism diagnostics, nested rejections, convergence and runtime")


if __name__ == "__main__":
    main()
