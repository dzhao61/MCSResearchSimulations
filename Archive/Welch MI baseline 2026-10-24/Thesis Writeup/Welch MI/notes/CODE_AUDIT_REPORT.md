# Audit report: Welch-MI thesis experiment code

**Status:** Audit only. No files were modified. Nothing was rebuilt or repackaged.
**Audited:** 20 September 2026, against the working tree as of 18:53.
**Auditor note:** `chapters_rewrite/*.tex` and `figures_rewrite/audit_evidence.py`
were being edited live during this audit (18:48–18:53). Every finding below was
re-verified against the post-edit state.

---

## 0. Orientation for a fresh agent

Workspace root: `/Users/danielzhao/MyMac/Masters Degree/Research/Simulations`

| Component | Path |
| --- | --- |
| Manuscript | `Thesis Writeup/Welch MI/` (`main.tex`, `chapters_rewrite/`, `appendices_rewrite/`) |
| Estimator library | `WelchSatterthwaiteMI/src/welch_differential_mi/welch.py` |
| Shared statistics | `DifferentialMI/src/differential_mi/statistics.py` |
| Population constructors | `DifferentialMI/src/differential_mi/distributions.py` |
| Confirmatory harness | `WelchSatterthwaiteMI/experiments/thesis_redesign_core.py`, `run_thesis_redesign.py` |
| Frozen protocol | `WelchSatterthwaiteMI/experiments/THESIS_REDESIGN_PROTOCOL.json` |
| Frozen results | `WelchSatterthwaiteMI/results/thesis_redesign/` |
| Mechanism study | `WelchSatterthwaiteMI/experiments/run_thesis_mechanism_check.py` + `report_thesis_mechanism_check.py` |
| Figures / evidence audit | `Thesis Writeup/Welch MI/figures_rewrite/make_figures.py`, `audit_evidence.py` |

Python interpreter: `./.venv/bin/python` (numpy 2.4.4, scipy 1.17.1, pandas
3.0.3, matplotlib 3.10.9 — exactly the versions recorded in `run_metadata.json`).
`pytest` is **not** installed and is not needed; the tests are `unittest`-based.
Set `MPLBACKEND=Agg` for any script that imports matplotlib.

The method: a two-sample Wald test on the bias-corrected plug-in MI difference,
with the normal reference replaced by a Student reference whose degrees of
freedom come from a Satterthwaite argument applied to the *variance estimator*
itself ("Expanded Welch"). Chapter 4 derives it; `welch.py` implements it.

---

## 1. Bottom line

**The science and the implementation are sound. No defect found changes any
number in the thesis.** The Chapter 4 derivation matches the code line-for-line,
and the novel part reproduces under independent numerical checks. What remains
is one latent bug in a report generator (currently masked by a filter), some
provenance/packaging hygiene, and one optional scientific addition.

All three verification gates pass as of this audit:

```
100 unittest tests                      -> OK
figures_rewrite/audit_evidence.py       -> PASS
deliverables/SHA256SUMS.txt             -> all 3 OK
```

---

## 2. What was verified, and how

These are not code reads — each was independently reproduced.

### 2.1 The influence function is correct

`_variance_influence_component_df` in
`WelchSatterthwaiteMI/src/welch_differential_mi/welch.py:110-178` computes the
influence function of `V(P) = Var_P[pmi]`. I compared it against a
central-difference derivative of `influence_variance` along the contamination
path `P_eps = (1-eps)P + eps*delta_(x,y)`:

| shape | Var(IF) analytic | Var(IF) numeric | rel. error |
| --- | --- | --- | --- |
| 2x2 | 0.1637275169 | 0.1637275169 | 4.0e-11 |
| 3x3 | 0.1224459515 | 0.1224459514 | 3.3e-10 |
| 3x5 | 0.4492393419 | 0.4492393418 | 2.5e-10 |
| 5x5 | 0.3393006033 | 0.3393006030 | 8.5e-10 |

The algebra also reconciles exactly with the boxed `eq:g-final` / `eq:g-hat` of
`chapters_rewrite/04_expanded_welch.tex`, and with `population_moments` in
`run_thesis_mechanism_check.py:20-28` (which drops the `-2*I*(pmi-I)` term by
expanding the square — algebraically identical, not a discrepancy).

### 2.2 The Satterthwaite degrees of freedom are correct

`nu = 2*n*V^2/tau^2` vs. a Monte Carlo estimate of `2*sigma^4/Var(sigmahat^2)`
over 60,000 replicates:

| n | analytic nu | Monte Carlo nu |
| --- | --- | --- |
| 500 | 37.0 | 35.8 |
| 5,000 | 369.9 | 366.1 |
| 50,000 | 3699.2 | 3686.0 |

The residual gap shrinks with n, as a first-order approximation should.

### 2.3 The delta-method variance is correct

MC `n*Var(MI_hat)` vs. population `sigma^2 = 0.096897`: 0.1068 (n=200),
0.0993 (n=2000), 0.0966 (n=20000). Converges as expected.

### 2.4 The manuscript's formulas map onto the code

| Manuscript | Code |
| --- | --- |
| `eq:g-hat` | `variance_influence` block, `welch.py:148-159` |
| `eq:tau-hat` | `influence_variance` (centred), `welch.py:160-168` |
| `eq:nu-p-hat` | `numerator = 2.0*sample_size*variance**2`, `welch.py:171-177` |
| `eq:expanded-df` | `_combine_df(component_p, component_q, expanded_df_p, expanded_df_q)` |

The Miller–Madow bias correction sign is correct: plug-in MI is biased *upward*
by `d/(2n)`, and `differential_mi_pvalues` subtracts it (`welch.py:196-201`).

### 2.5 The frozen run reproduces

- `build_manifests` rebuilds **bit-identically**: 4001 display slots, 3111
  configurations, 534 population pairs; zero mismatches in `pair_id`, `n_p`,
  `n_q`, `replicates`, `simulation_seed`; achieved MI agrees to 1e-16.
- I re-simulated **22 configurations** (2 per section, all 11 design sections,
  20,000 replicates each) from the recorded seeds. Every `rejections`,
  `valid_replicates`, `common_valid_replicates`, `common_valid_rejections`,
  `both_reject`, `neither_rejects`, `only_method_a_rejects` and
  `only_method_b_rejects` matched `cell_results.csv` and
  `paired_method_results.csv` **exactly**.
- This also explains the suspiciously short 65.5 s recorded runtime: 22 configs
  re-simulate in 1.4 s single-threaded, so 3111 configs across 4 workers in
  ~65 s is consistent. Not a red flag.

### 2.6 Manuscript numbers match the data

I independently recomputed the values the audit script does **not** cover and
all matched: the Wilson intervals in `tab:null-paired-examples`; every cell of
`tab:null-band-summary` including the new "validity below 90%" column
(4/5/8/12/8/12); the runtime ratio range (min 1.7232, median 1.7535, max
1.7882 against the stated "about 1.72–1.79"); and the per-shape ratios.

The post-edit Chapter 6 claims also verify: Expanded Welch rejects 0 of the 12
`n=5` main nulls; uniform 3x3/5x5/8x8 at `n=5` have validity 0.953/0.991/0.916
(all > 0.9); 15 vs 9 closeness split over the 24 `n∈{10,20}` regimes; all
`n=2` configurations have exactly zero validity.

Mechanism-study claims verify too: max |Hutcheson − Simple Welch| = 0.01235 in a
5x5 `n=5` configuration (as stated); kurtosis-only is less conservative than
Expanded Welch (mean rate 0.0466 vs 0.0350, higher in 653/809 configurations);
169 null pilots, 338 component rows, 4854 ablation rows all as claimed.

### 2.7 Numerical robustness

Zero cells, empty rows and empty columns are handled safely. Logs are masked via
`np.log(..., where=...)` and every sum is probability-weighted, so empty cells
contribute exactly zero and no NaN leaks into `tau^2`. The `n<=1` case is
explicitly guarded in `thesis_redesign_core.py:691-698` before `_validate_pair`
would raise. At `n=2` the influence variance is provably 0, so all replicates
are correctly marked invalid.

The nested-rejection invariant (Expanded Welch rejects only where Wald does)
is mathematically guaranteed by the shared statistic plus a heavier-tailed
reference, and is asserted in `verify_results` — it holds across all 3111
configurations.

---

## 3. Findings

### Finding 1 — Latent bug: `local_moment_df` uses `n_p` for both populations

**File:** `WelchSatterthwaiteMI/experiments/report_thesis_mechanism_check.py`
**Severity:** Latent. No published number is affected.

```python
c["local_moment_df"] = (
    (c.n_p * c.v + interaction_df) ** 2
    / (2 * c.n_p * c.v + interaction_df)
)
```

`c` has one row per population per configuration (`population` is `"p"` or
`"q"`). The `population == "q"` rows should use `n_q`, not `n_p`.

This is currently harmless because the table is filtered to
`diag.n_p.eq(diag.n_q)`, so all four published rows of `tab:component-check`
have `n_p == n_q`. But 12 of 338 rows in `component_diagnostics.csv` have
`n_p != n_q`, so the column would be wrong for any wider selection.

The same expression is duplicated in the `representative["local_moment_df"]`
block of `figures_rewrite/audit_evidence.py`, so the audit cannot catch it.

**Suggested fix:** `n = c.n_p.where(c.population.eq("p"), c.n_q)`, then use `n`
in both numerator and denominator; mirror it in `audit_evidence.py`. Published
values will not change — verify by confirming the four rows of
`tab:component-check` are unchanged and only the 12 `n_p != n_q` rows differ.

Note `run_thesis_mechanism_check.py` itself is **correct** here — it uses
`n = c[f"n_{side}"]` for `population_first_order_df`. Only the report generator
has the bug.

### Finding 2 — Shipped supplement contradicts its own hash record

**Severity:** Provenance/presentation. Already documented internally; the
underlying claim is accurate.

`results/thesis_redesign/run_metadata.json` records
`run_thesis_redesign.py = 42c0ef36f46c88e7828a628ee68fbeb18dbde5d978291d849dc4847c2b857908`,
but the script shipped beside it inside
`Daniel_Zhao_Welch_MI_Experiment_Supplement.zip` hashes to
`5de63a0d2f38d1ca42729a53d66200ce1a25a8034390ed6b8f4d21e453aafed7`.

The metadata also has **no `output_sha256` block**, so `cell_results.csv`,
`paired_method_results.csv` and the manifests carry no recorded checksum —
even though the current code would write one.

Related symptom: shipped `preflight_summary.json` says `figure_count: 106`
(99 primary + 7 companion) while `run_metadata.json` says `99`, because the
former was regenerated by a later preflight pass under newer code.

**This is already documented** in `SUBMISSION_CHECK.md` ("The orchestration
runner has two later, non-statistical additions … Its simulation path is
unchanged"). I verified that claim by diffing `1c6a52a..HEAD`: the only changes
are the `primary_figure_count`/`companion_calibration_zooms` keys, the
`report_thesis_redesign.py` input hash, and the new `output_sha256` block.
**The simulation path is byte-identical.** All other recorded input hashes
(protocol, `thesis_redesign_core.py`, `welch.py`, `statistics.py`,
`distributions.py`) still match exactly, as does the reporter hash in
`report_metadata.json`.

**Critical constraint for whoever fixes this:** do **not** re-run
`run_thesis_redesign.py --full` to refresh the metadata. `--full` re-executes
`runtime_experiment`, which would change every timing number quoted in
Chapter 6 and `tab:runtime-by-shape`. The checkpoints are also deliberately
excluded from the supplement, so a reader cannot re-aggregate.

**Suggested fix (documentation only):** add a provenance note to
`WelchSatterthwaiteMI/EXPERIMENT_SUPPLEMENT_README.md` and one sentence to
`appendices_rewrite/E_reproducibility.tex` naming both hashes, stating that the
runner gained only metadata fields after the run, and that `figure_count` in
`run_metadata.json` predates the primary/companion split now recorded in
`report_metadata.json`. Appendix E already hedges the git revision; this extends
that hedge to the one file it applies to.

### Finding 3 — Manuscript numbers are hand-duplicated in the audit script

**Severity:** Structural / process risk.

`figures_rewrite/audit_evidence.py` asserts hardcoded constants that restate the
Chapter 6 prose. Nothing structurally prevents a prose edit from leaving an
assertion behind.

This risk is not hypothetical — it materialised during this audit. The claim
"Among the 36 main null regimes with n=5,10,20, Expanded Welch is closer in 26
and Wald in 10" was replaced by "Among the 24 main null regimes with n=10 or
20 … 15 and Wald in 9", and `audit_evidence.py` had to be updated by hand to
match. It *was* updated correctly (both now pass), but only because the author
remembered.

**Suggested fix:** extend the mechanism that already exists and works.
`evidence_macros()` in `figures_rewrite/make_figures.py` already generates
`evidence_values.tex` for three configurations. Promote the recurring inline
counts and rates — the early/late closeness counts, the `n=1000` ranges, the
baseline/pattern/imbalance/construction null rates — to generated macros and
cite the macros from the `.tex`, so prose and CSVs cannot diverge.

### Finding 4 — Minor code warts

None affect results.

- `run_thesis_redesign.py:359-362` — on preflight failure `build_manifests`
  returns the failures frame in its third slot, so `populations` holds failures
  and `save_preflight` writes them into `population_definitions.csv` before the
  run aborts; `build_manifests` is then called a **second time** purely to
  recover `failures`. Unpack once and branch.
- `run_thesis_mechanism_check.py:117` uses `.lt(.05)` (strict) with a hardcoded
  alpha, while `thesis_redesign_core.py:712` uses `p_value <= alpha` read from
  the protocol. No numerical impact (exact ties have probability ~0), but the
  two should agree.
- `welch.py:303-307` — `unbiased_p` is masked by `valid` (= `simple_valid`)
  rather than its own validity mask. Unused by the thesis
  (`include_unbiased_sensitivity=False` throughout).
- `make_figures.py:112` hardcodes `"denominator": 20000` in the figure manifest
  rather than reading `protocol["replicates"]`.

### Finding 5 — Rebuild and repackage before submitting

**Severity:** Housekeeping. Expected mid-revision.

`main.pdf` (18:11:28) and the deliverable archives (18:12:19–18:12:21) predate
the current `.tex` edits (18:48:06–18:53:18). The shipped source zip therefore
contains the superseded Chapter 6 text — I confirmed nine `.tex` files differ
between `Daniel_Zhao_Welch_MI_Thesis_Source.zip` and the working tree.

Checksums in `SHA256SUMS.txt` are internally consistent and the packaged PDF is
byte-identical to `main.pdf` — the archives are simply a revision behind.

The last build was clean: 0 overfull boxes, 0 LaTeX errors, 0 undefined
references/citations, 8 underfull boxes (cosmetic), 109 pages.

### Finding 6 — Optional scientific addition: imbalance null inflation

**Severity:** Not a defect. A strengthening opportunity.

Chapter 6 already names the bias corrections `d/(2n_P)` and `d/(2n_Q)` as the
mechanism behind the direction effect. But the deterministic offset
`d/(2n_P) − d/(2n_Q)` scales with `d = (r-1)(c-1)` and dwarfs the MI differences
under test. For 8x8 at `(n_P,n_Q) = (500,50)` the offset is **0.441 nats**
against differences of at most 0.02 nats.

Null rejection rises monotonically with that offset, and both methods inherit it
because they share the numerator:

| 8x8 uniform, null | (50,50) | (50,250) | (50,500) |
| --- | --- | --- | --- |
| offset (nats) | 0.000 | 0.392 | 0.441 |
| Normal Wald | 0.0703 | 0.1273 | 0.1425 |
| Expanded Welch | 0.0592 | 0.1003 | 0.1113 |

(Validity is 1.000 throughout, so this is not a sparsity artefact.)

The displayed imbalance figures are 3x3 only, so the largest failures live in the
atlas but are never quoted. Adding one sentence with these numbers to the
imbalance section of Chapter 6 would strengthen the "no general improvement"
conclusion and pre-empt an obvious examiner question. The `observed_support_wald`
arm already present in the mechanism study is the natural follow-up reference.

---

## 4. Verification commands

From the workspace root, with `export MPLBACKEND=Agg`:

```bash
# Full test suite — expect "Ran 100 tests ... OK"
cd WelchSatterthwaiteMI/tests && ../../.venv/bin/python -m unittest discover -s . -p "test_*.py"

# Source-linked evidence audit — expect "PASS: ..."
cd "Thesis Writeup/Welch MI" && ../../.venv/bin/python figures_rewrite/audit_evidence.py

# Deliverable checksums — expect three "OK" lines
cd "Thesis Writeup/Welch MI/deliverables" && shasum -a 256 -c SHA256SUMS.txt
```

If Finding 1 is fixed, regenerate the mechanism tables before re-running the
evidence audit:

```bash
cd WelchSatterthwaiteMI/experiments && ../../.venv/bin/python report_thesis_mechanism_check.py
```

If evidence macros change (Finding 3), regenerate figures and macros:

```bash
cd "Thesis Writeup/Welch MI" && ../../.venv/bin/python figures_rewrite/make_figures.py
```

Rebuild and repackage only once the text has settled (Finding 5):

```bash
cd "Thesis Writeup/Welch MI"
/Library/TeX/texbin/latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
../../.venv/bin/python package_deliverables.py
cd deliverables && shasum -a 256 -c SHA256SUMS.txt
```

**Do not** run `run_thesis_redesign.py --full` (see Finding 2).

---

## 5. Suggested priority

| # | Finding | Priority | Touches |
| --- | --- | --- | --- |
| 1 | `local_moment_df` n_p/n_q | Fix — cheap, real, no output change | 2 Python files |
| 2 | Provenance note | Fix — examiner-facing | 1 markdown + 1 `.tex` sentence |
| 5 | Rebuild/repackage | Must do before submission | build artifacts |
| 6 | Imbalance null text | Optional — strengthens the argument | 1 `.tex` paragraph |
| 3 | Macro-ify prose numbers | Optional — process hardening | `make_figures.py` + `06_results.tex` |
| 4 | Minor warts | Optional — tidy when convenient | 3 Python files |
