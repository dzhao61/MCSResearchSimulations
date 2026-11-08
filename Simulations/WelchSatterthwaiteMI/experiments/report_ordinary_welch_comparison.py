"""Check a small ordinary-Welch benchmark using saved null repetitions."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import norm, t
import redesign_study as study


def comparison_rows():
    configurations = pd.read_csv(study.OUTPUT / 'configurations.csv')
    displays = pd.read_csv(study.OUTPUT / 'displays.csv', keep_default_na=False)
    ids = set(displays.loc[displays.study.eq('null'), 'configuration_id'])
    configurations = configurations[configurations.configuration_id.isin(ids)]
    rows = []
    for k, profile, n in ((4, 'uniform', 20), (4, 'uniform', 50),
                           (16, 'different_skew', 1000)):
        selected = configurations[(configurations.k == k) &
                                  (configurations.profile == profile) &
                                  (configurations.n_p == n) &
                                  (configurations.n_q == n)]
        assert len(selected) == 1
        c = selected.iloc[0]
        assert np.isclose(c.mi_p, .02) and np.isclose(c.mi_q, .02)
        r = study.load_records(study.OUTPUT, 'evaluation', c.configuration_id)
        statistic = r['statistic']
        valid = r['base_valid'].astype(bool)
        assert len(statistic) == 100000
        a = r['influence_variance_p'] / n
        b = r['influence_variance_q'] / n
        df = (a + b)**2 / (a*a/(n-1) + b*b/(n-1))
        # Independent algebraic expression for equal sample sizes.
        np.testing.assert_allclose(df, (n-1)*(a+b)**2/(a*a+b*b))
        ordinary = valid & np.isfinite(df) & (df > 0) & (2*t.sf(np.abs(statistic), df) <= .05)
        np.testing.assert_array_equal(ordinary, valid & (np.abs(statistic) >= t.ppf(.975, df)))
        wald = valid & (r['normal_p_value'] <= .05)
        np.testing.assert_array_equal(wald, valid & (np.abs(statistic) >= norm.ppf(.975)))
        expanded_valid = r['expanded_valid'].astype(bool)
        expanded = expanded_valid & (r['expanded_welch_p_value'] <= .05)
        assert not np.any(ordinary & ~wald)
        rows.append(dict(k=k, profile=profile, n=n, common_mi=.02,
                         repetitions=len(statistic), wald_valid=int(valid.sum()),
                         expanded_valid=int(expanded_valid.sum()), configuration_id=c.configuration_id,
                         wald_rejections=int(wald.sum()),
                         ordinary_rejections=int(ordinary.sum()),
                         expanded_rejections=int(expanded.sum())))
    return rows


if __name__ == '__main__':
    rows = comparison_rows()
    output = study.ROOT / 'results/ordinary_welch_comparison/verification.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps(rows, indent=2))
