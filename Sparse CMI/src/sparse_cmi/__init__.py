"""Finite-sample conditional tests for binary discrete CMI."""

from .api import test_sparse_cmi
from .models import CMIResult, Stratum
from .tables import build_binary_strata

__all__ = [
    "CMIResult",
    "Stratum",
    "build_binary_strata",
    "test_sparse_cmi",
]

