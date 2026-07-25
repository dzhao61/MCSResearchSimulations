from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy.stats import chi2

from .approximations import (
    cornish_fisher_critical_value,
    edgeworth_pvalue,
    normal_pvalue,
)
from .exact_convolution import (
    StateSpaceTooLarge,
    exact_conditional_distribution,
)
from .models import CMIResult, Stratum
from .moments import aggregate_moments
from .statistic import observed_cmi_nats, observed_g2


def test_sparse_cmi(
    strata: Sequence[Stratum],
    alpha: float = 0.05,
    *,
    exact_max_states: int | None = None,
) -> CMIResult:
    """Calculate finite-sample approximations for binary conditional MI."""

    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    strata_list = list(strata)
    moments = aggregate_moments(strata_list)
    observed = observed_g2(strata_list)

    if moments.variance > 0:
        z_score = (observed - moments.mean) / np.sqrt(moments.variance)
    else:
        z_score = 0.0

    nominal_df = len(strata_list)
    informative_df = moments.informative_strata
    p_nominal = float(chi2.sf(observed, nominal_df)) if nominal_df else 1.0
    p_informative = (
        float(chi2.sf(observed, informative_df)) if informative_df else 1.0
    )

    p_exact: float | None = None
    exact_states: int | None = None
    if exact_max_states is not None:
        try:
            exact = exact_conditional_distribution(
                strata_list,
                max_states=exact_max_states,
            )
            p_exact = exact.upper_tail(observed)
            exact_states = int(exact.values.size)
        except StateSpaceTooLarge:
            pass

    return CMIResult(
        g2_observed=observed,
        cmi_nats=observed_cmi_nats(strata_list),
        mean=moments.mean,
        variance=moments.variance,
        third_cumulant=moments.third_cumulant,
        fourth_cumulant=moments.fourth_cumulant,
        skewness=moments.skewness,
        z_score=float(z_score),
        p_normal=float(normal_pvalue(observed, moments.mean, moments.variance)),
        p_edgeworth=float(
            edgeworth_pvalue(
                observed,
                moments.mean,
                moments.variance,
                moments.skewness,
            )
        ),
        cf_critical_value=cornish_fisher_critical_value(
            alpha,
            moments.mean,
            moments.variance,
            moments.skewness,
        ),
        p_chi2_nominal=p_nominal,
        p_chi2_informative=p_informative,
        p_exact=p_exact,
        informative_strata=informative_df,
        total_strata=nominal_df,
        lyapunov_ratio=moments.lyapunov_ratio,
        max_variance_share=moments.max_variance_share,
        exact_state_count=exact_states,
    )

