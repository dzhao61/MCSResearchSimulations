"""Compare estimates and predictions with their corresponding benchmarks."""
from __future__ import annotations
import numpy as np

MEAN_LABEL = r'\mathbb{E}(\widehat V)/V'
VAR_POP_LABEL = r'\frac{\tau^2/n}{\mathrm{Var}(\widehat V)}'
VAR_SAMPLE_LABEL = r'\frac{\mathbb{E}(\widehat{\tau}^{\,2})/n}{\mathrm{Var}(\widehat V)}'
DF_POP_LABEL = r'\nu/\nu_{\mathrm{mom}}'
DF_SAMPLE_LABEL = r'\mathbb{E}(\widehat\nu)/\nu_{\mathrm{mom}}'
RATIO_ORIENTATION = 'quantity assessed / corresponding benchmark'
VAR_AXIS_LABEL = 'Variance prediction\n/ $\\mathrm{Var}(\\widehat V)$'
DF_AXIS_LABEL = 'Degrees of freedom\n/ $\\nu_{\\mathrm{mom}}$'


def ratio_interval(values, mcse):
    """Keep the point estimate and its Monte Carlo interval on the same scale."""
    values = np.asarray(values, dtype=float)
    half_width = 1.96 * np.asarray(mcse, dtype=float)
    return values, values-half_width, values+half_width


def mean_df_over_moment_target(data):
    """Require a genuinely unconditional mean in the plotted comparison."""
    complete = np.asarray(data.df_valid_count == data['count'])
    target = np.asarray(data.nu_mom, dtype=float)
    mean = np.asarray(data.df_mean, dtype=float)
    valid = complete & np.isfinite(target) & (target > 0) & np.isfinite(mean) & (mean > 0)
    values = np.full(mean.shape, np.nan)
    np.divide(mean, target, out=values, where=valid)
    return values


def comparison_curves(data, kind):
    """Return benchmark-normalised curves, interval endpoints and sample curve.

    Both variance predictions share the observed sampling variance as their
    denominator; both df approximations share the sampling-moment target.
    These are the saved CSV definitions, used without inversion or rounding.
    """
    field = {'mean':'mean_ratio', 'variance':'variance_ratio', 'df':'df_ratio'}[kind]
    point, low, high = ratio_interval(data[field], data[field+'_mcse'])
    sample = (None if kind=='mean' else np.asarray(data.plugin_variance_ratio, dtype=float)
              if kind=='variance' else mean_df_over_moment_target(data))
    return point, low, high, sample


def plain_log_tick(value, _position=None):
    """Write 1 instead of 10^0 while retaining logarithmic coordinates."""
    return f'{value:g}'
