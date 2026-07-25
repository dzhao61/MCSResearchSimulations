"""Two-sample inference tools for discrete mutual information."""

from .distributions import (
    association_table,
    marginal_probabilities,
    mutual_information_probability,
    table_with_target_mi,
)
from .inference import compare_tables
from .statistics import (
    analytic_bias_corrected_mi,
    influence_variance,
    jackknife_mi,
    plugin_mi,
)

__all__ = [
    "association_table",
    "analytic_bias_corrected_mi",
    "compare_tables",
    "influence_variance",
    "jackknife_mi",
    "marginal_probabilities",
    "mutual_information_probability",
    "plugin_mi",
    "table_with_target_mi",
]
