"""Run six pre-specified public-data comparisons without changing the thesis."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import platform
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.stats import norm, t

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
sys.path.insert(0, str(WORKSPACE / "DifferentialMI/src"))
sys.path.insert(0, str(WORKSPACE / "WelchSatterthwaiteMI/src"))
from welch_differential_mi.welch import differential_mi_pvalues

SEED = 20261010
ALPHA = 0.05
SAMPLE_SIZES = (50, 100, 200, 500, 1000, 2000, 5000)
ADULT_COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income",
]
EDUCATION = [
    "Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th",
    "12th", "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors",
    "Masters", "Prof-school", "Doctorate",
]
OCCUPATION = [
    "Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial",
    "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical",
    "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv",
    "Armed-Forces",
]
SPECIFICATIONS = [
    ("adult_education", "Adult", "education", "sex", "Female", "Male", "income_above_50k", EDUCATION),
    ("adult_occupation", "Adult", "occupation", "sex", "Female", "Male", "income_above_50k", OCCUPATION),
    ("shoppers_month", "Online Shoppers", "Month", "VisitorType", "New_Visitor", "Returning_Visitor", "Revenue", None),
    ("shoppers_weekend", "Online Shoppers", "Weekend", "VisitorType", "New_Visitor", "Returning_Visitor", "Revenue", [False, True]),
    ("students_studytime", "Student Performance", "studytime", "school", "GP", "MS", "grade_at_least_10", [1, 2, 3, 4]),
    ("students_maternal_education", "Student Performance", "Medu", "school", "GP", "MS", "grade_at_least_10", [0, 1, 2, 3, 4]),
]
SOURCES = {
    "Adult": {
        "archive": "adult.zip", "url": "https://archive.ics.uci.edu/static/public/2/adult.zip",
        "citation": "Becker and Kohavi (1996), doi:10.24432/C5XW20",
        "page": "https://archive.ics.uci.edu/dataset/2/adult",
    },
    "Online Shoppers": {
        "archive": "online_shoppers.zip",
        "url": "https://archive.ics.uci.edu/static/public/468/online%2Bshoppers%2Bpurchasing%2Bintention%2Bdataset.zip",
        "citation": "Sakar and Kastro (2018), doi:10.24432/C5F88Q",
        "page": "https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset",
    },
    "Student Performance": {
        "archive": "student_performance.zip",
        "url": "https://archive.ics.uci.edu/static/public/320/student%2Bperformance.zip",
        "citation": "Cortez (2008), doi:10.24432/C5TG7T",
        "page": "https://archive.ics.uci.edu/dataset/320/student+performance",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv_bytes(data: bytes, **kwargs) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(data), **kwargs)


def load_datasets(raw: Path) -> dict[str, pd.DataFrame]:
    with zipfile.ZipFile(raw / "adult.zip") as archive:
        frames = [read_csv_bytes(archive.read(name), names=ADULT_COLUMNS,
                                 header=None, skipinitialspace=True, comment="|")
                  for name in ("adult.data", "adult.test")]
    adult = pd.concat(frames, ignore_index=True)
    for name in adult.select_dtypes(include=["object", "str"]).columns:
        adult[name] = adult[name].str.strip()
    adult["income"] = adult["income"].str.rstrip(".")
    if not adult.income.isin(["<=50K", ">50K"]).all():
        raise ValueError("Unexpected Adult income labels.")
    adult["income_above_50k"] = adult.income.eq(">50K")
    with zipfile.ZipFile(raw / "online_shoppers.zip") as archive:
        shoppers = read_csv_bytes(archive.read("online_shoppers_intention.csv"))
    for name in ("Revenue", "Weekend"):
        if shoppers[name].dtype != bool:
            raise ValueError(f"Unexpected shopper {name} coding.")
    with zipfile.ZipFile(raw / "student_performance.zip") as archive:
        with zipfile.ZipFile(io.BytesIO(archive.read("student.zip"))) as nested:
            students = read_csv_bytes(nested.read("student-por.csv"), sep=";")
    if not students.G3.between(0, 20).all():
        raise ValueError("Unexpected student final grades.")
    students["grade_at_least_10"] = students.G3.ge(10)
    expected = {"Adult": 48842, "Online Shoppers": 12330, "Student Performance": 649}
    frames = {"Adult": adult, "Online Shoppers": shoppers, "Student Performance": students}
    for name, frame in frames.items():
        if len(frame) != expected[name]:
            raise ValueError(f"Unexpected {name} row count: {len(frame)}")
    return frames


def count_table(frame: pd.DataFrame, x: str, y: str, levels: list) -> np.ndarray:
    if frame[[x, y]].isna().any().any() or not frame[x].isin(levels).all():
        raise ValueError("Missing values or categories outside the common alphabet.")
    codes = pd.Categorical(frame[x], categories=levels).codes
    outcome = frame[y].to_numpy(dtype=np.int64)
    if not np.isin(outcome, [0, 1]).all():
        raise ValueError("Outcome must be binary.")
    return np.bincount(codes * 2 + outcome, minlength=len(levels) * 2).reshape(-1, 2)


def comparisons(frames: dict[str, pd.DataFrame]) -> list[dict]:
    result = []
    for identifier, dataset, x, group, p_name, q_name, y, declared in SPECIFICATIONS:
        frame = frames[dataset]
        selected = frame[frame[group].isin([p_name, q_name])].copy()
        missing = selected[x].isna() | selected[x].eq("?")
        excluded_missing = int(missing.sum())
        selected = selected.loc[~missing]
        levels = declared if declared is not None else sorted(selected[x].unique().tolist())
        p_rows = selected.loc[selected[group].eq(p_name)]
        q_rows = selected.loc[selected[group].eq(q_name)]
        assert p_rows.index.intersection(q_rows.index).empty
        p_table = count_table(p_rows, x, y, levels)
        q_table = count_table(q_rows, x, y, levels)
        result.append({
            "id": identifier, "dataset": dataset, "predictor": x, "outcome": y,
            "group_variable": group, "group_p": p_name, "group_q": q_name,
            "levels": levels, "table_p": p_table, "table_q": q_table,
            "source_rows": len(frame), "excluded_group_rows": len(frame) - int(frame[group].isin([p_name, q_name]).sum()),
            "excluded_missing_predictor": excluded_missing,
            "identical_source_rows": int(frame.duplicated().sum()),
        })
    return result


def method_values(p: np.ndarray, q: np.ndarray) -> dict[str, np.ndarray]:
    return differential_mi_pvalues(p, q, include_simple=False,
                                  include_expanded=True, include_unbiased_sensitivity=False)


def independent_component(table: np.ndarray) -> tuple[float, float, float]:
    counts = np.asarray(table, dtype=float)
    n = counts.sum()
    prob = counts / n
    row, column = prob.sum(axis=1), prob.sum(axis=0)
    score = np.zeros_like(prob)
    for i, j in np.ndindex(prob.shape):
        if prob[i, j] > 0:
            score[i, j] = np.log(prob[i, j] / (row[i] * column[j]))
    mean = float(np.sum(prob * score))
    variance = float(np.sum(prob * (score - mean)**2))
    row_mean = np.zeros_like(row)
    col_mean = np.zeros_like(column)
    for i in range(len(row)):
        if row[i] > 0:
            row_mean[i] = np.sum(prob[i] * score[i]) / row[i]
    for j in range(len(column)):
        if column[j] > 0:
            col_mean[j] = np.sum(prob[:, j] * score[:, j]) / column[j]
    sensitivity = np.zeros_like(prob)
    for i, j in np.ndindex(prob.shape):
        sensitivity[i, j] = (
            (score[i, j] - mean)**2 - variance
            + 2 * (score[i, j] - row_mean[i] - col_mean[j] + mean)
        )
    centered_sensitivity = sensitivity - np.sum(prob * sensitivity)
    tau = float(np.sum(prob * centered_sensitivity**2))
    return mean, variance, tau


def independent_values(p: np.ndarray, q: np.ndarray) -> dict[str, float]:
    mi_p, v_p, tau_p = independent_component(p)
    mi_q, v_q, tau_q = independent_component(q)
    n_p, n_q = p.sum(), q.sum()
    bias_df = (p.shape[0] - 1) * (p.shape[1] - 1)
    delta = mi_p - mi_q - bias_df / (2 * n_p) + bias_df / (2 * n_q)
    se = np.sqrt(v_p / n_p + v_q / n_q)
    statistic = delta / se if se > 0 else np.nan
    df_p = 2 * n_p * v_p**2 / tau_p if tau_p > 0 else np.nan
    df_q = 2 * n_q * v_q**2 / tau_q if tau_q > 0 else np.nan
    df = ((v_p / n_p + v_q / n_q)**2 /
          ((v_p / n_p)**2 / df_p + (v_q / n_q)**2 / df_q))
    return {
        "delta_corrected": delta, "influence_variance_p": v_p,
        "influence_variance_q": v_q, "standard_error": se, "statistic": statistic,
        "variance_influence_variance_p": tau_p, "variance_influence_variance_q": tau_q,
        "expanded_component_degrees_of_freedom_p": df_p,
        "expanded_component_degrees_of_freedom_q": df_q,
        "expanded_welch_degrees_of_freedom": df,
        "normal_p_value": float(2 * norm.sf(abs(statistic))),
        "expanded_welch_p_value": float(2 * t.sf(abs(statistic), df)),
    }


def holm(p_values: list[float]) -> np.ndarray:
    values = np.asarray(p_values, dtype=float)
    usable = np.where(np.isfinite(values), values, 1.0)
    order = np.argsort(usable, kind="stable")
    corrected = np.minimum(1.0, np.maximum.accumulate(usable[order] * (len(values) - np.arange(len(values)))))
    result = np.empty_like(values)
    result[order] = corrected
    return np.where(np.isfinite(values), result, np.nan)


def wilson(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return np.nan, np.nan
    z = norm.ppf(0.975)
    fraction = successes / total
    denominator = 1 + z*z / total
    centre = (fraction + z*z / (2 * total)) / denominator
    half = z * np.sqrt(fraction*(1-fraction)/total + z*z/(4*total*total)) / denominator
    return float(centre-half), float(centre+half)


def rng_for(identifier: str, size: int, group: str) -> np.random.Generator:
    key = f"{SEED}|{identifier}|{size}|{group}".encode()
    entropy = int.from_bytes(hashlib.sha256(key).digest()[:16], "little")
    return np.random.Generator(np.random.PCG64(entropy))


def full_result(item: dict) -> dict:
    p, q = item["table_p"], item["table_q"]
    values = method_values(p, q)
    independent = independent_values(p, q)
    for name, expected in independent.items():
        np.testing.assert_allclose(values[name], expected, rtol=1e-10, atol=1e-12, equal_nan=True)
    n_p, n_q = int(p.sum()), int(q.sum())
    correction = (p.shape[0]-1) / 2
    mi_p, _, _ = independent_component(p)
    mi_q, _, _ = independent_component(q)
    result = {key: item[key] for key in (
        "id", "dataset", "predictor", "outcome", "group_variable", "group_p", "group_q",
        "source_rows", "excluded_group_rows", "excluded_missing_predictor", "identical_source_rows")}
    result.update({
        "rows": p.shape[0], "columns": 2, "n_p": n_p, "n_q": n_q,
        "plugin_mi_p": mi_p, "plugin_mi_q": mi_q,
        "corrected_mi_p": mi_p - correction/n_p,
        "corrected_mi_q": mi_q - correction/n_q,
        "empty_cells_p": int((p==0).sum()), "empty_cells_q": int((q==0).sum()),
        "empty_rows_p": int((p.sum(axis=1)==0).sum()), "empty_rows_q": int((q.sum(axis=1)==0).sum()),
        "positive_outcome_fraction_p": float(p[:, 1].sum()/n_p),
        "positive_outcome_fraction_q": float(q[:, 1].sum()/n_q),
    })
    for key in independent:
        result[key] = float(values[key])
    result["wald_valid"] = bool(values["base_valid"])
    result["expanded_valid"] = bool(values["expanded_valid"])
    result["wald_reject"] = result["wald_valid"] and result["normal_p_value"] < ALPHA
    result["expanded_reject"] = result["expanded_valid"] and result["expanded_welch_p_value"] < ALPHA
    for method, critical in (("wald", norm.ppf(.975)),
                             ("expanded", t.ppf(.975, result["expanded_welch_degrees_of_freedom"]))):
        result[f"{method}_ci_low"] = result["delta_corrected"] - critical * result["standard_error"]
        result[f"{method}_ci_high"] = result["delta_corrected"] + critical * result["standard_error"]
    return result


def subsample_result(identifier: str, size: int, p: np.ndarray, q: np.ndarray,
                     values: dict[str, np.ndarray]) -> dict:
    repetitions = len(p)
    valid_w, valid_e = values["base_valid"], values["expanded_valid"]
    reject_w = valid_w & (values["normal_p_value"] < ALPHA)
    reject_e = valid_e & (values["expanded_welch_p_value"] < ALPHA)
    if np.any(reject_e & ~reject_w):
        raise AssertionError("Expanded Welch rejected where Normal Wald did not.")
    both = valid_w & valid_e
    result = {"id": identifier, "n_each": size, "repetitions": repetitions,
              "wald_only_both_valid": int((both & reject_w & ~reject_e).sum()),
              "wald_reject_expanded_invalid": int((reject_w & ~valid_e).sum()),
              "expanded_only": int((reject_e & ~reject_w).sum()),
              "both_valid": int(both.sum()),
              "mean_delta": float(np.mean(values["delta_corrected"])),
              "sd_delta": float(np.std(values["delta_corrected"], ddof=1)),
              "median_expanded_df": float(np.median(values["expanded_welch_degrees_of_freedom"][valid_e])) if valid_e.any() else np.nan,
              "support_loss_fraction_p": float(np.mean((p.sum(axis=2)==0).any(axis=1))),
              "support_loss_fraction_q": float(np.mean((q.sum(axis=2)==0).any(axis=1))),
              "mean_empty_cells_p": float(np.mean((p==0).sum(axis=(1, 2)))),
              "mean_empty_cells_q": float(np.mean((q==0).sum(axis=(1, 2)))),
              }
    for name, valid, reject in (("wald", valid_w, reject_w), ("expanded", valid_e, reject_e)):
        count = int(reject.sum())
        valid_count = int(valid.sum())
        result[f"{name}_rejections"] = count
        result[f"{name}_valid"] = valid_count
        result[f"{name}_valid_fraction"] = valid_count/repetitions
        result[f"{name}_reject_fraction"] = count/repetitions
        result[f"{name}_reject_valid_only"] = count/valid_count if valid_count else np.nan
        result[f"{name}_reject_low"], result[f"{name}_reject_high"] = wilson(count, repetitions)
    return result


def serializable(value):
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if isinstance(value, np.ndarray):
        return serializable(value.tolist())
    if isinstance(value, np.generic):
        return serializable(value.item())
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def plot_results(full: pd.DataFrame, subsets: pd.DataFrame, output: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False})
    figure, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True, layout="constrained")
    primary = ("adult_education", "shoppers_month", "students_studytime")
    titles = ("Adult: education / income", "Shoppers: month / purchase", "Students: study time / grade >=10")
    for ax, identifier, title in zip(axes, primary, titles):
        rows = subsets.loc[subsets.id.eq(identifier)].sort_values("n_each")
        for method, color, marker, label in (("wald", "#164b67", "o", "Normal Wald"),
                                            ("expanded", "#ad3f68", "s", "Expanded Welch")):
            ax.plot(rows.n_each, rows[f"{method}_reject_fraction"], color=color, marker=marker, label=label)
            ax.fill_between(rows.n_each, rows[f"{method}_reject_low"], rows[f"{method}_reject_high"], color=color, alpha=.12)
        ax.set_xscale("log")
        ax.set_xticks(rows.n_each, [str(n) for n in rows.n_each], rotation=35)
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.set_xlabel("Subset size per group")
        ax.set_title(title, fontsize=10)
        ax.set_ylim(0, 1)
        ax.grid(axis="y", alpha=.2)
    axes[0].set_ylabel("Fraction of subsets rejecting equal MI")
    handles, labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside upper center", ncol=2, frameon=False)
    figure.savefig(output / "decision_stability.png", dpi=180)
    plt.close(figure)
    figure, ax = plt.subplots(figsize=(8, 4.8), layout="constrained")
    labels = [f"{row.dataset}: {row.predictor}" for row in full.itertuples()]
    for offset, method, color, marker, label in ((-.12, "wald", "#164b67", "o", "Normal Wald"),
                                               (.12, "expanded", "#ad3f68", "s", "Expanded Welch")):
        centres = full.delta_corrected.to_numpy()
        intervals = np.stack([centres-full[f"{method}_ci_low"], full[f"{method}_ci_high"]-centres])
        ax.errorbar(centres, np.arange(len(full))+offset, xerr=intervals,
                    fmt=marker, color=color, capsize=3, label=label)
    ax.set_yticks(np.arange(len(full)), labels)
    ax.invert_yaxis()
    ax.axvline(0, color="0.4", ls=":", lw=1)
    ax.set_xlabel("Corrected MI difference P - Q (nats); approximate 95% interval")
    handles, labels = ax.get_legend_handles_labels()
    figure.legend(handles, labels, frameon=False, ncol=2, loc="outside upper center")
    figure.savefig(output / "full_data_intervals.png", dpi=180)
    plt.close(figure)


def report_text(full: pd.DataFrame, subsets: pd.DataFrame, repetitions: int) -> str:
    lines = ["# Exploratory application: Normal Wald versus Expanded Welch", "",
             "Six comparisons were specified before method p-values were calculated.",
             "P/Q labels and preparation are in PROTOCOL.md. Differences are P minus Q in nats.",
             "The thesis, methods, prior simulations and working drafts are unchanged.", "",
             "## Full-data comparisons", "",
             "| Comparison | P / Q sample sizes | Corrected MI P / Q | Difference | Wald p | Expanded p | Expanded df | Empty cells P / Q |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in full.itertuples():
        lines.append(f"| {row.dataset}: {row.predictor} | {row.n_p} / {row.n_q} | {row.corrected_mi_p:.5f} / {row.corrected_mi_q:.5f} | {row.delta_corrected:.5f} | {row.normal_p_value:.4g} | {row.expanded_welch_p_value:.4g} | {row.expanded_welch_degrees_of_freedom:.1f} | {row.empty_cells_p} / {row.empty_cells_q} |")
    lines += ["", "Both methods use the same effect estimate and standard error. Intervals are",
              "pointwise approximations, not multiple-comparison-adjusted intervals.", "",
              "| Comparison | Raw 5% decisions Wald / Expanded | Holm-adjusted p Wald / Expanded | Holm 5% decisions Wald / Expanded |",
              "| --- | --- | --- | --- |"]
    for row in full.itertuples():
        decisions = f"{'reject' if row.wald_reject else 'retain'} / {'reject' if row.expanded_reject else 'retain'}"
        adjusted = f"{row.wald_holm_p:.4g} / {row.expanded_holm_p:.4g}"
        adjusted_decisions = f"{'reject' if row.wald_holm_p < ALPHA else 'retain'} / {'reject' if row.expanded_holm_p < ALPHA else 'retain'}"
        lines.append(f"| {row.dataset}: {row.predictor} | {decisions} | {adjusted} | {adjusted_decisions} |")
    lines += ["", "Here 'retain' means do not reject equal MI, not proof of equality.", "",
              "## Subset decision stability", "",
              f"Each size uses {repetitions} uniform subsets without replacement per group.",
              "The two methods see the same subset pairs. Frequencies are unconditional:",
              "invalid calculations remain in the denominator and are reported separately.", "",
              "| Comparison | n each | Rejection % Wald / Expanded | Valid % Wald / Expanded | Wald-only decisions with both valid | Wald reject / Expanded invalid | Median Expanded df |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for row in subsets.itertuples():
        lines.append(f"| {row.id} | {row.n_each} | {100*row.wald_reject_fraction:.2f} / {100*row.expanded_reject_fraction:.2f} | {100*row.wald_valid_fraction:.2f} / {100*row.expanded_valid_fraction:.2f} | {row.wald_only_both_valid} | {row.wald_reject_expanded_invalid} | {row.median_expanded_df:.2f} |")
    lines += ["", "## Reading the evidence", "",
              "These are practical demonstrations, not calibration benchmarks: true population",
              "MI is unknown. A larger p-value, fewer rejections or a disagreement does not show",
              "that Expanded Welch is more accurate. Overlapping subsets of the same data do",
              "not establish power, false-positive rates or independent replication.", "",
              "Full-data and subset analyses answer different questions; subsets deliberately",
              "balance group sample sizes while the full-data analyses retain natural imbalance.",
              "Holm adjustment applies to the six full-data comparisons separately for each method.",
              "Subset frequencies are descriptive stability measures, not a search for significant",
              "sample sizes or an additional family of scientific discoveries.", "",
              "Adult is an unweighted survey-derived benchmark. Its survey design and unidentified",
              "duplicate profiles prevent national-population or fully verified independent-person",
              "inference. The two-school data may have within-class dependence. Shoppers has",
              "different users per session by source documentation, but common seasonal effects",
              "are possible. Neither method adjusts for these sampling-design issues.", "",
              "Empty cells and missing category margins can weaken the fixed-support first-order",
              "approximations. All raw tables and diagnostics are retained; no smoothing is used.",
              "MI also depends on predictor and outcome frequencies, so a group contrast is not",
              "by itself a causal effect or a difference in a classifier's predictive accuracy.", "",
              "## Sources", ""]
    for name, info in SOURCES.items():
        lines.append(f"- [{name}]({info['page']}): {info['citation']}; CC BY 4.0.")
    return "\n".join(lines) + "\n"


def run(output: Path, repetitions: int) -> None:
    if repetitions < 2:
        raise ValueError("At least two repetitions are required.")
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Use a new output directory; existing results are not overwritten.")
    output.mkdir(parents=True, exist_ok=True)
    record_dir = output / "records"
    record_dir.mkdir()
    items = comparisons(load_datasets(HERE / "raw"))
    full_rows, subset_rows, metadata, checksums = [], [], [], {}
    for item in items:
        full_rows.append(full_result(item))
        metadata.append(serializable(item))
        p, q = item["table_p"], item["table_q"]
        for size in SAMPLE_SIZES:
            if size > min(p.sum(), q.sum()):
                continue
            sample_p = rng_for(item["id"], size, "P").multivariate_hypergeometric(p.ravel(), size, size=repetitions).reshape(repetitions, *p.shape)
            sample_q = rng_for(item["id"], size, "Q").multivariate_hypergeometric(q.ravel(), size, size=repetitions).reshape(repetitions, *q.shape)
            values = method_values(sample_p, sample_q)
            row = subsample_result(item["id"], size, sample_p, sample_q, values)
            subset_rows.append(row)
            path = record_dir / f"{item['id']}_n{size}.npz"
            fields = {key: value for key, value in values.items() if not key.startswith("unbiased") and not key.startswith("welch_") and key not in ("valid", "simple_valid")}
            np.savez_compressed(path, table_p=sample_p, table_q=sample_q, **fields)
            checksums[str(path.relative_to(output))] = sha256(path)
        print(f"Completed {item['id']}: n={p.sum()}/{q.sum()}, table {p.shape}.", flush=True)
    full = pd.DataFrame(full_rows)
    full["wald_holm_p"] = holm(full.normal_p_value.tolist())
    full["expanded_holm_p"] = holm(full.expanded_welch_p_value.tolist())
    subsets = pd.DataFrame(subset_rows)
    full.to_csv(output / "full_data_results.csv", index=False)
    subsets.to_csv(output / "subsample_results.csv", index=False)
    (output / "count_tables.json").write_text(json.dumps(metadata, indent=2, allow_nan=False)+"\n")
    (output / "record_checksums.json").write_text(json.dumps(checksums, indent=2)+"\n")
    identity = {
        "master_seed": SEED, "repetitions_per_subset_size": repetitions,
        "sample_sizes": SAMPLE_SIZES, "alpha": ALPHA,
        "subsample_settings": len(subsets), "sampled_table_pairs": len(subsets)*repetitions,
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "scipy": scipy.__version__, "pandas": pd.__version__},
        "sources": {name: {**info, "sha256": sha256(HERE / "raw" / info["archive"])} for name, info in SOURCES.items()},
        "protocol_sha256": sha256(HERE / "PROTOCOL.md"), "runner_sha256": sha256(Path(__file__)),
        "method_sha256": sha256(WORKSPACE / "WelchSatterthwaiteMI/src/welch_differential_mi/welch.py"),
        "statistics_sha256": sha256(WORKSPACE / "DifferentialMI/src/differential_mi/statistics.py"),
        "interpretation": "Exploratory practical application and conditional subset stability; population MI unknown.",
    }
    (output / "study_identity.json").write_text(json.dumps(identity, indent=2)+"\n")
    (output / "RESULTS.md").write_text(report_text(full, subsets, repetitions))
    plot_results(full, subsets, output)
    print(full[["id", "n_p", "n_q", "delta_corrected", "normal_p_value", "expanded_welch_p_value", "expanded_welch_degrees_of_freedom"]].to_string(index=False))


def verify(output: Path) -> None:
    items = comparisons(load_datasets(HERE / "raw"))
    full = pd.read_csv(output / "full_data_results.csv")
    subsets = pd.read_csv(output / "subsample_results.csv")
    identity = json.loads((output / "study_identity.json").read_text())
    checksums = json.loads((output / "record_checksums.json").read_text())
    for name, info in identity["sources"].items():
        assert sha256(HERE / "raw" / info["archive"]) == info["sha256"], name
    assert sha256(Path(__file__)) == identity["runner_sha256"]
    assert sha256(HERE / "PROTOCOL.md") == identity["protocol_sha256"]
    assert sha256(WORKSPACE / "WelchSatterthwaiteMI/src/welch_differential_mi/welch.py") == identity["method_sha256"]
    assert sha256(WORKSPACE / "DifferentialMI/src/differential_mi/statistics.py") == identity["statistics_sha256"]
    assert len(full) == len(items) == 6
    assert len(subsets) == identity["subsample_settings"] == len(checksums)
    for item in items:
        expected = full_result(item)
        saved = full.loc[full.id.eq(item["id"])].iloc[0]
        for key, value in expected.items():
            if isinstance(value, (float, int)) and not isinstance(value, bool):
                np.testing.assert_allclose(saved[key], value, rtol=1e-10, atol=1e-12, equal_nan=True)
            else:
                assert saved[key] == value, key
        for _, row in subsets.loc[subsets.id.eq(item["id"])].iterrows():
            size = int(row.n_each)
            relative = f"records/{item['id']}_n{size}.npz"
            path = output / relative
            assert sha256(path) == checksums[relative]
            with np.load(path) as record:
                p, q = record["table_p"], record["table_q"]
                for group, sampled, original in (("P", p, item["table_p"]), ("Q", q, item["table_q"])):
                    assert np.all(sampled.sum(axis=(1, 2)) == size)
                    assert np.all((sampled >= 0) & (sampled <= original))
                    regenerated = rng_for(item["id"], size, group).multivariate_hypergeometric(original.ravel(), size, size=len(sampled)).reshape(sampled.shape)
                    np.testing.assert_array_equal(sampled, regenerated)
                values = method_values(p, q)
                for key in record.files:
                    if key not in ("table_p", "table_q"):
                        np.testing.assert_allclose(record[key], values[key], rtol=1e-12, atol=1e-12, equal_nan=True)
                for index in np.linspace(0, len(p)-1, 5, dtype=int):
                    independent = independent_values(p[index], q[index])
                    for key, value in independent.items():
                        actual = values[key][index]
                        if np.isfinite(actual):
                            np.testing.assert_allclose(actual, value, rtol=1e-9, atol=1e-11, equal_nan=True)
                expected_row = subsample_result(item["id"], size, p, q, values)
                for key, value in expected_row.items():
                    if key == "id":
                        assert row[key] == value
                    else:
                        np.testing.assert_allclose(row[key], value, rtol=1e-10, atol=1e-12, equal_nan=True)
    np.testing.assert_allclose(full.wald_holm_p, holm(full.normal_p_value.tolist()), rtol=1e-10, atol=1e-12)
    np.testing.assert_allclose(full.expanded_holm_p, holm(full.expanded_welch_p_value.tolist()), rtol=1e-10, atol=1e-12)
    summary = {"all_pass": True, "full_comparisons": len(full),
               "subset_settings": len(subsets), "sampled_table_pairs": identity["sampled_table_pairs"],
               "independently_recomputed_pairs": 6+5*len(subsets),
               "checks": ["raw archive hashes", "fixed comparisons and category alphabets",
                          "full-data independent MI/variance/sensitivity/df/p-value algebra",
                          "raw subset record checksums", "all sample totals and finite-population bounds",
                          "all deterministic subset inputs regenerated", "all saved method outputs recomputed",
                          "independent subset formula checkpoints", "all summaries and Holm corrections"]}
    (output / "verification.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["run", "verify"])
    parser.add_argument("--output", type=Path, default=HERE / "results")
    parser.add_argument("--repetitions", type=int, default=5000)
    args = parser.parse_args()
    if args.mode == "run":
        run(args.output, args.repetitions)
    else:
        verify(args.output)
