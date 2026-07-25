"""Two-sample inference tools for discrete mutual information."""

from .distributions import (
    association_table,
    marginal_probabilities,
    mutual_information_probability,
    table_with_target_mi,
)
from .inference import (
    AnalyticWaldResult,
    InfluenceSaddlepointResult,
    analytic_wald_test,
    compare_tables,
    influence_saddlepoint_test,
)
from .statistics import (
    analytic_bias_corrected_mi,
    influence_variance,
    jackknife_mi,
    plugin_mi,
)

__all__ = [
    "association_table",
    "AnalyticWaldResult",
    "InfluenceSaddlepointResult",
    "analytic_bias_corrected_mi",
    "analytic_wald_test",
    "compare_tables",
    "influence_saddlepoint_test",
    "influence_variance",
    "jackknife_mi",
    "marginal_probabilities",
    "mutual_information_probability",
    "plugin_mi",
    "table_with_target_mi",
]
