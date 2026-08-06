"""Welch-Satterthwaite inference for differential mutual information."""

from .welch import (
    CUSTOM_WELCH_MIN_SAMPLE_RATIO,
    WelchResult,
    differential_mi_pvalues,
    welch_satterthwaite_test,
)

__all__ = [
    "CUSTOM_WELCH_MIN_SAMPLE_RATIO",
    "WelchResult",
    "differential_mi_pvalues",
    "welch_satterthwaite_test",
]
