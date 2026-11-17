"""Exact expected bias of plug-in MI for the thesis population tables (Slide 15).

Plug-in MI is H(X) + H(Y) - H(X, Y), a sum of per-cell terms -p_hat log p_hat.
Each cell count is Binomial(n, p), so the expected estimate is an exact sum,
with no simulation. The script splits the bias by cell group for the
different-skew 16x16 power setting on Slide 12 (P: margin 0.7, MI 0.02 nats;
Q: margin 0.8, MI 0.03 nats; n = 1,000 per population) and checks three
comparison designs.

Run: python3 bias_breakdown.py
"""
import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom


def population(k, rho, lam):
    """Thesis construction (Section 5.1): copy X into Y with probability lam."""
    a = np.full(k, (1 - rho) / (k - 1))
    a[0] = rho
    return lam * np.diag(a) + (1 - lam) * np.outer(a, a)


def mi(p):
    outer = np.outer(p.sum(1), p.sum(0))
    return float((p * np.log(p / outer)).sum())


def copying_probability(k, rho, target):
    return brentq(lambda lam: mi(population(k, rho, lam)) - target, 1e-9, 0.999)


def expected_h(p, n):
    """Exact E[-p_hat log p_hat] for a cell with count ~ Binomial(n, p)."""
    counts = np.arange(1, n + 1)
    x = counts / n
    return float((binom.pmf(counts, n, p) * (-x * np.log(x))).sum())


def cell_bias(p, n):
    return expected_h(p, n) + p * np.log(p)      # E[h(p_hat)] - h(p)


def bias_by_group(p, n):
    """Bias of plug-in MI, split into the margins and four groups of joint cells."""
    k = len(p)
    groups = {
        "common cell (1,1)": [(0, 0)],
        "first row or column": [(0, j) for j in range(1, k)] + [(i, 0) for i in range(1, k)],
        "rare diagonal": [(i, i) for i in range(1, k)],
        "rare pairings (off-diagonal)": [(i, j) for i in range(1, k) for j in range(1, k) if i != j],
    }
    parts = {"margins": 2 * sum(cell_bias(q, n) for q in p.sum(1))}
    for name, cells in groups.items():
        parts[name] = -sum(cell_bias(p[i, j], n) for i, j in cells)
    return parts


def expected_difference(k, n, p_design, q_design):
    """True and expected estimated MI difference I(P) - I(Q) under the plug-in estimator."""
    tables = [population(k, rho, copying_probability(k, rho, target)) for rho, target in (p_design, q_design)]
    true = mi(tables[0]) - mi(tables[1])
    bias = sum(bias_by_group(tables[0], n).values()) - sum(bias_by_group(tables[1], n).values())
    return true, bias, true + bias


k, n = 16, 1000
lam_p, lam_q = copying_probability(k, 0.7, 0.02), copying_probability(k, 0.8, 0.03)
P, Q = population(k, 0.7, lam_p), population(k, 0.8, lam_q)
print(f"Copying probability: P {lam_p:.3f}, Q {lam_q:.3f}")
print(f"Leading term (k - 1)^2 / (2n) = {(k - 1) ** 2 / (2 * n):.4f} nats per estimate")

bp, bq = bias_by_group(P, n), bias_by_group(Q, n)
print(f"\n{'Bias of plug-in MI':30s} {'P':>8s} {'Q':>8s} {'P - Q':>8s}")
for name in bp:
    print(f"{name:30s} {bp[name]:8.4f} {bq[name]:8.4f} {bp[name] - bq[name]:8.4f}")
print(f"{'total':30s} {sum(bp.values()):8.4f} {sum(bq.values()):8.4f} "
      f"{sum(bp.values()) - sum(bq.values()):8.4f}")

for name, table in (("P", P), ("Q", Q)):
    rare = table[1, 2]
    print(f"{name}: each rare pairing has probability {rare:.6f}, expected count {n * rare:.2f}, "
          f"empty with probability {(1 - rare) ** n:.2f}")

print("\nExpected estimated difference I(P) - I(Q), 16x16, n = 1,000")
designs = {
    "thesis: P 0.7 MI 0.02, Q 0.8 MI 0.03": ((0.7, 0.02), (0.8, 0.03)),
    "swapped: P 0.8 MI 0.02, Q 0.7 MI 0.03": ((0.8, 0.02), (0.7, 0.03)),
    "equal MI 0.02, different skew": ((0.7, 0.02), (0.8, 0.02)),
    "same skew 0.8, MI 0.02 vs 0.03": ((0.8, 0.02), (0.8, 0.03)),
}
for label, (pd, qd) in designs.items():
    true, bias, mean = expected_difference(k, n, pd, qd)
    print(f"  {label:40s} true {true:+.4f}  bias {bias:+.4f}  mean estimate {mean:+.4f}")

print("\nThesis design across sample sizes")
for size in (250, 1000, 2500, 10000):
    true, bias, mean = expected_difference(k, size, (0.7, 0.02), (0.8, 0.03))
    print(f"  n = {size:6d}: bias {bias:+.4f}, mean estimate {mean:+.4f}")


def second_order(p, n):
    """1/n^2 term of the large-sample bias expansion for plug-in MI, which assumes every cell is well sampled."""
    rows, cols = p.sum(1), p.sum(0)
    return (1 - (1 / rows).sum() - (1 / cols).sum() + (1 / p).sum()) / (12 * n ** 2)


print("\nBias beyond the leading term: exact against the 1/n^2 term (Slide 15)")
for name, table in (("P", P), ("Q", Q)):
    for size in (1000, 10000, 50000):
        beyond = sum(bias_by_group(table, size).values()) - (k - 1) ** 2 / (2 * size)
        print(f"  {name}, n = {size:6d}: exact {beyond:+.5f}, 1/n^2 term {second_order(table, size):+.5f}, "
              f"rarest cell expected {size * table.min():.2f} times")
