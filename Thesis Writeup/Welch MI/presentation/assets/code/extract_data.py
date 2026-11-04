"""Extract and validate the presentation data slices named in the evidence manifest."""
import math
import sys
import pandas as pd

SRC = sys.argv[1]  # .../Simulations
OUT = sys.argv[2]
R = f"{SRC}/WelchSatterthwaiteMI/results"
NS = [10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000]


def close(a, b, tol=1e-12):
    return math.isclose(a, b, abs_tol=tol, rel_tol=0)


def sel(df, **kw):
    mask = pd.Series(True, index=df.index)
    for k, v in kw.items():
        if isinstance(v, float):
            mask &= df[k].apply(lambda x: close(float(x), v))
        else:
            mask &= df[k] == v
    return df[mask].copy()


moments = pd.read_csv(f"{R}/approximation_redesign/moments.csv")
displays = pd.read_csv(f"{R}/approximation_redesign/displays.csv", keep_default_na=False)
null = pd.read_csv(f"{R}/balanced_null_2026-11-01/combined_rates.csv")
power = pd.read_csv(f"{R}/mi_gap_power_2026-11-01/combined_rates.csv")
pdiag = pd.read_csv(f"{R}/mi_gap_power_2026-11-01/combined_diagnostics.csv")
app = pd.read_csv(f"{SRC}/PracticalMIExploration/thesis_application/full_data_results.csv")

# Slide 8: P, 16x16, different skew, MI 0.02, null display IDs
ids_null = set(displays.loc[displays.study == "null", "configuration_id"])
s8 = sel(moments, side="p", k=16, profile="different_skew", mi=0.02)
s8 = s8[s8.configuration_id.isin(ids_null)].sort_values("n")
assert len(s8) == 10 and list(s8.n) == NS, s8.n.tolist()
r50 = s8[s8.n == 50].iloc[0]
assert close(r50.mean_ratio, 12.709119363203984, 1e-9)
assert close(r50.variance_ratio, 0.1862837474058447, 1e-9)
assert close(r50.plugin_variance_ratio, 0.5526659456140404, 1e-9)
s8[["configuration_id", "n", "mean_ratio", "mean_ratio_mcse", "variance_ratio", "variance_ratio_mcse",
    "plugin_variance_ratio", "plugin_variance_ratio_mcse"]].to_csv(f"{OUT}/slide08_variance_inputs.csv", index=False)

# Slide 9: P, 4x4, different skew, n=1000, association display IDs
ids_assoc = set(displays.loc[displays.study == "association", "configuration_id"])
s9 = sel(moments, side="p", k=4, profile="different_skew", n=1000)
s9 = s9[s9.configuration_id.isin(ids_assoc)].sort_values("mi")
assert len(s9) == 7, len(s9)
assert (s9.df_valid_count == s9["count"]).all()
lo = s9.iloc[0]
assert close(lo.mi, 0.0001, 1e-9)
assert close(lo.df_mean, 4.85978716999042, 1e-9)
assert close(lo.nu_mom, 9.124807968487897, 1e-9)
assert close(lo.nu_fo, 0.0964000042894677, 1e-9)
assert close(lo.a4_df_mean, 4.6, 1e-9)
assert close(lo.plugin_variance_ratio, 1.965405591167243, 1e-9)
s9[["configuration_id", "mi", "df_mean", "df_mean_mcse", "nu_mom", "nu_mom_mcse", "nu_fo",
    "a4_df_mean", "a4_df_mom", "plugin_variance_ratio"]].to_csv(f"{OUT}/slide09_near_independence_df.csv", index=False)

# Null and power: primary denominator
null_all = null[null.denominator == "all"].copy()
power_all = power[power.denominator == "all"].copy()
for df, g in [(null_all, "common_mi"), (power_all, "gap")]:
    assert (df.replicates == 100000).all()
    settings = df.groupby(["k", "profile", "n_p", g]).ngroups
    assert settings == 360, settings
    wide = df.pivot_table(index=["k", "profile", "n_p", g], columns="method", values="rejection_rate")
    assert (wide.expanded_welch <= wide.normal_wald).all()

# Slide 10 rows
s10 = []
for k, prof, n, wald, ew, cid in [(4, "uniform", 20, 8.352, 4.897, "setting_c1d939c2103eb6d7"),
                                   (16, "same_skew", 1000, 0.604, 0.525, "setting_1363c7043554941c"),
                                   (16, "different_skew", 1000, 26.011, 24.836, "setting_9bdd689bf556c0d0")]:
    rows = sel(null_all, k=k, profile=prof, n_p=n, common_mi=0.02)
    assert len(rows) == 2 and set(rows.configuration_id) == {cid}
    got = dict(zip(rows.method, rows.rejection_rate * 100))
    assert close(got["normal_wald"], wald, 1e-9) and close(got["expanded_welch"], ew, 1e-9), got
    assert (rows.valid_rate == 1.0).all()
    s10.append(rows)
pd.concat(s10).to_csv(f"{OUT}/slide10_illustrative_null_rows.csv", index=False)

# Slide 11
s11 = sel(null_all, k=16, profile="different_skew").sort_values(["common_mi", "method", "n_p"])
assert len(s11) == 60
h = sel(s11, common_mi=0.005, n_p=1000)
got = dict(zip(h.method, h.rejection_rate * 100))
assert close(got["normal_wald"], 36.381, 1e-9) and close(got["expanded_welch"], 34.382, 1e-9)
assert (h.valid_rate == 1.0).all()
s11.to_csv(f"{OUT}/slide11_null_16x16_different_skew.csv", index=False)

# Slide 12
s12 = sel(power_all, k=4, profile="uniform").sort_values(["gap", "method", "n_p"])
assert len(s12) == 60
s12.to_csv(f"{OUT}/slide12_power_4x4_uniform.csv", index=False)

# Slide 13
s13 = sel(power_all, k=16, profile="different_skew", gap=0.01).sort_values(["method", "n_p"])
assert len(s13) == 20
d13 = sel(pdiag, k=16, profile="different_skew", n_p=1000, mi_p=0.02, mi_q=0.03)
assert len(d13) == 1
d = d13.iloc[0]
assert close(d.difference_bias, 0.0306714189759277, 1e-9)
assert int(d.expanded_positive_rejections) == 9659 and int(d.expanded_negative_rejections) == 3
ew1000 = sel(s13, method="expanded_welch", n_p=1000).iloc[0]
assert int(ew1000.rejections) == 9662 and ew1000.valid_rate == 1.0
s13.to_csv(f"{OUT}/slide13_power_16x16_different_skew_gap001.csv", index=False)
d13.to_csv(f"{OUT}/slide13_direction_diagnostics_n1000.csv", index=False)

# Slide 14
m = app[app.id == "shoppers_month"].iloc[0]
assert close(m.corrected_mi_p, 0.0043163111573871, 1e-9) and close(m.corrected_mi_q, 0.0178797492702181, 1e-9)
assert close(m.delta_corrected, -0.013563438112832, 1e-9)
assert close(m.expanded_holm_p, 0.0014905078300573, 1e-9) and close(m.wald_holm_p, 0.0001885602589484, 1e-9)
assert int(m.n_p) == 1694 and int(m.n_q) == 10551
app.to_csv(f"{OUT}/slide14_B10_application_results.csv", index=False)

# Backups B6-B8 (null) and B9 (power, same skew)
for prof in ["uniform", "same_skew", "different_skew"]:
    b = sel(null_all, profile=prof)
    assert len(b) == 240
    b.to_csv(f"{OUT}/backup_null_{prof}.csv", index=False)
b9 = sel(power_all, profile="same_skew")
assert len(b9) == 240
x = sel(b9, k=16, n_p=50000, method="expanded_welch")
pw = dict(zip(x.gap.round(3), x.rejection_rate * 100))
assert close(pw[0.005], 79.87, 0.005) and pw[0.01] > 99.9 and pw[0.02] > 99.9, pw
b9.to_csv(f"{OUT}/backup_power_same_skew.csv", index=False)

print("All manifest checks passed.")
print("Slide 13 EW rejection at n=1000:", ew1000.rejection_rate * 100, "%; mean delta", -0.01 + d.difference_bias)
print("B9 16x16 n=50000 EW power:", pw)
print("Application month df:", m.expanded_component_degrees_of_freedom_p, m.expanded_component_degrees_of_freedom_q, m.expanded_welch_degrees_of_freedom)
