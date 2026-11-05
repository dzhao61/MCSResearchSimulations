"""Extract and validate the replanned presentation's data selections (evidence manifest version 2)."""
import math
import sys

import numpy as np
import pandas as pd

SRC, OUT = sys.argv[1], sys.argv[2]
R = f"{SRC}/WelchSatterthwaiteMI/results"
NS = [10, 20, 50, 100, 250, 500, 1000, 2500, 10000, 50000]


def close(a, b, tol=1e-12):
    return math.isclose(float(a), float(b), abs_tol=tol, rel_tol=0)


def sel(df, **kw):
    m = pd.Series(True, index=df.index)
    for k, v in kw.items():
        m &= df[k].apply(lambda x: close(x, v)) if isinstance(v, float) else (df[k] == v)
    return df[m].copy()


moments = pd.read_csv(f"{R}/approximation_redesign/moments.csv")
displays = pd.read_csv(f"{R}/approximation_redesign/displays.csv", keep_default_na=False)
null = pd.read_csv(f"{R}/balanced_null_2026-11-01/combined_rates.csv")
ndiag = pd.read_csv(f"{R}/balanced_null_2026-11-01/combined_diagnostics.csv")
power = pd.read_csv(f"{R}/mi_gap_power_2026-11-01/combined_rates.csv")
pdiag = pd.read_csv(f"{R}/mi_gap_power_2026-11-01/combined_diagnostics.csv")
app = pd.read_csv(f"{SRC}/PracticalMIExploration/thesis_application/full_data_results.csv")
null_ids = set(displays.loc[displays.study == "null", "configuration_id"])
assoc_ids = set(displays.loc[displays.study == "association", "configuration_id"])
null_all = null[null.denominator == "all"].copy()
power_all = power[power.denominator == "all"].copy()
for df, g in [(null_all, "common_mi"), (power_all, "gap")]:
    assert (df.replicates == 100000).all()
    assert df.groupby(["k", "profile", "n_p", g]).ngroups == 360
    w = df.pivot_table(index=["k", "profile", "n_p", g], columns="method", values="rejection_rate")
    assert (w.expanded_welch <= w.normal_wald).all()

# Slides 2 and 13: application
m = app[app.id == "shoppers_month"].iloc[0]
assert close(m.corrected_mi_p, 0.0043163111573871, 1e-12) and close(m.corrected_mi_q, 0.0178797492702181, 1e-12)
assert int(m.n_p) == 1694 and int(m.n_q) == 10551
assert close(m.wald_holm_p, 0.0001885602589484, 1e-12) and close(m.expanded_holm_p, 0.0014905078300573, 1e-12)
wk = app[app.id == "shoppers_weekend"].iloc[0]
assert not wk.wald_reject and not wk.expanded_reject
app.to_csv(f"{OUT}/slide02_13_B12_application_results.csv", index=False)

# Slide 7: P / 4x4 / different skew / MI 0.02, null display IDs
s7 = sel(moments, side="p", k=4, profile="different_skew", mi=0.02)
s7 = s7[s7.configuration_id.isin(null_ids)].sort_values("n")
assert len(s7) == 10 and list(s7.n) == NS
c = s7[s7.n == 1000].iloc[0]
for col, v in [("mean_ratio", 1.1904401416429922), ("variance_ratio", 0.970250354772405),
               ("plugin_variance_ratio", 1.080464909406677), ("nu_fo", 15.295500514108248), ("nu_mom", 21.031131016189576)]:
    assert close(c[col], v, 1e-9), col
s7[["configuration_id", "n", "mean_ratio", "mean_ratio_mcse", "variance_ratio", "variance_ratio_mcse",
    "plugin_variance_ratio", "plugin_variance_ratio_mcse", "nu_fo", "nu_mom"]].to_csv(f"{OUT}/slide07_variance_inputs_4x4.csv", index=False)

# Slide 8 / B5: near independence
s8 = sel(moments, side="p", k=4, profile="different_skew", n=1000)
s8 = s8[s8.configuration_id.isin(assoc_ids)].sort_values("mi")
assert len(s8) == 7 and (s8.df_valid_count == s8["count"]).all()
lo = s8.iloc[0]
for col, v in [("df_mean", 4.85978716999042), ("nu_mom", 9.124807968487897), ("nu_fo", 0.0964000042894677),
               ("a4_df_mean", 4.6), ("plugin_variance_ratio", 1.965405591167243)]:
    assert close(lo[col], v, 1e-9), col
s8[["configuration_id", "mi", "df_mean", "df_mean_mcse", "nu_mom", "nu_mom_mcse", "nu_fo", "a4_df_mean",
    "plugin_variance_ratio"]].to_csv(f"{OUT}/slide08_B5_near_independence_df.csv", index=False)

# Slide 9: uniform 4x4, n=20, three common MI values
s9 = sel(null_all, k=4, profile="uniform", n_p=20).sort_values(["common_mi", "method"])
assert len(s9) == 6 and (s9.valid_rate == 1.0).all()
exp9 = {(0.005, "normal_wald"): 7.606, (0.005, "expanded_welch"): 4.162, (0.02, "normal_wald"): 8.352,
        (0.02, "expanded_welch"): 4.897, (0.3, "normal_wald"): 15.861, (0.3, "expanded_welch"): 13.114}
for _, r in s9.iterrows():
    assert close(r.rejection_rate * 100, exp9[(round(r.common_mi, 3), r.method)], 0.0005), (r.common_mi, r.method)
s9.to_csv(f"{OUT}/slide09_null_uniform_4x4_n20.csv", index=False)

# Slide 10: 16x16, n=1,000, MI 0.02, same vs different skew
rows10 = []
for prof, wald, ew, vr, bsd in [("same_skew", 0.604, 0.525, 1.9286941072647668, -0.0027192541260095786),
                                ("different_skew", 26.011, 24.836, 1.9381042896284049, 2.0579206373676495)]:
    r = sel(null_all, k=16, profile=prof, n_p=1000, common_mi=0.02)
    got = dict(zip(r.method, r.rejection_rate * 100))
    assert close(got["normal_wald"], wald, 1e-9) and close(got["expanded_welch"], ew, 1e-9)
    assert (r.valid_rate == 1.0).all()
    d = sel(ndiag, k=16, profile=prof, n_p=1000, common_mi=0.02).iloc[0]
    assert close(d.estimated_observed_ratio, vr, 1e-12)
    assert close(d.difference_bias / np.sqrt(d.observed_variance), bsd, 1e-9)
    rows10.append(dict(profile=prof, normal_wald=got["normal_wald"], expanded_welch=got["expanded_welch"],
                       variance_ratio=d.estimated_observed_ratio, bias=d.difference_bias,
                       bias_over_sd=d.difference_bias / np.sqrt(d.observed_variance)))
pd.DataFrame(rows10).to_csv(f"{OUT}/slide10_bias_contrast.csv", index=False)

# Slide 11: uniform 4x4, gap 0.01 curve + snapshot at n=2,500
s11 = sel(power_all, k=4, profile="uniform", gap=0.01).sort_values(["method", "n_p"])
assert len(s11) == 20
snap = sel(power_all, k=4, profile="uniform", n_p=2500).sort_values(["gap", "method"])
assert len(snap) == 6 and (snap.valid_rate == 1.0).all()
exp11 = {(0.005, "normal_wald"): 11.604, (0.005, "expanded_welch"): 11.138, (0.01, "normal_wald"): 31.848,
         (0.01, "expanded_welch"): 31.14, (0.02, "normal_wald"): 79.24, (0.02, "expanded_welch"): 78.736}
for _, r in snap.iterrows():
    assert close(r.rejection_rate * 100, exp11[(round(r.gap, 3), r.method)], 0.0005), (r.gap, r.method)
s11.to_csv(f"{OUT}/slide11_power_uniform_4x4_gap001.csv", index=False)
snap.to_csv(f"{OUT}/slide11_snapshot_n2500.csv", index=False)

# Slide 12: 16x16 different skew, gap 0.01
s12 = sel(power_all, k=16, profile="different_skew", gap=0.01).sort_values(["method", "n_p"])
assert len(s12) == 20
d12 = sel(pdiag, k=16, profile="different_skew", n_p=1000, mi_p=0.02, mi_q=0.03).iloc[0]
assert close(d12.difference_bias, 0.0306714189759277, 1e-9)
assert int(d12.expanded_positive_rejections) == 9659 and int(d12.expanded_negative_rejections) == 3
ew = sel(s12, method="expanded_welch", n_p=1000).iloc[0]
assert int(ew.rejections) == 9662 and ew.valid_rate == 1.0
assert (sel(s12, n_p=1000).valid_rate == 1.0).all()
s12.to_csv(f"{OUT}/slide12_power_16x16_different_skew_gap001.csv", index=False)

# B4: six-panel ratios
b4 = sel(moments, profile="different_skew", mi=0.02)
b4 = b4[b4.configuration_id.isin(null_ids)]
assert len(b4) == 80
b4.to_csv(f"{OUT}/B4_approximation_ratios.csv", index=False)

# B6-B11 full grids
for prof in ["uniform", "same_skew", "different_skew"]:
    a = sel(null_all, profile=prof)
    b = sel(power_all, profile=prof)
    assert len(a) == 240 and len(b) == 240
    a.to_csv(f"{OUT}/B_null_{prof}.csv", index=False)
    b.to_csv(f"{OUT}/B_power_{prof}.csv", index=False)
u = sel(power_all, profile="uniform", gap=0.01, n_p=10000, method="expanded_welch")
pw = dict(zip(u.k, u.rejection_rate * 100))
assert close(pw[2], 89.44, 0.005) and close(pw[16], 71.12, 0.005), pw
ss = sel(power_all, profile="same_skew", k=16, n_p=50000, method="expanded_welch")
pss = dict(zip(ss.gap.round(3), ss.rejection_rate * 100))
assert close(pss[0.005], 79.87, 0.005) and pss[0.01] > 99.9 and pss[0.02] > 99.9
b8 = sel(null_all, profile="different_skew", k=16, n_p=1000, common_mi=0.005)
g8 = dict(zip(b8.method, b8.rejection_rate * 100))
assert close(g8["normal_wald"], 36.381, 1e-9) and close(g8["expanded_welch"], 34.382, 1e-9) and (b8.valid_rate == 1).all()
print("All version-2 manifest checks passed.")
