"""Welch-Satterthwaite inference for differential mutual information."""

from .welch import (
    WelchResult,
    differential_mi_pvalues,
    welch_satterthwaite_test,
)

__all__ = [
    "WelchResult",
    "differential_mi_pvalues",
    "welch_satterthwaite_test",
]
