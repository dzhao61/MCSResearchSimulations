"""Finite-sample conditional tests for binary discrete CMI."""

from .api import test_sparse_cmi
from .exact_convolution import (
    ConvolutionComplexity,
    estimate_convolution_complexity,
)
from .models import CMIResult, Stratum
from .routing import DeterministicTestResult, deterministic_pvalue
from .saddlepoint import FactorizedConditionalCGF, SaddlepointResult
from .tables import build_binary_strata

__all__ = [
    "CMIResult",
    "ConvolutionComplexity",
    "DeterministicTestResult",
    "FactorizedConditionalCGF",
    "SaddlepointResult",
    "Stratum",
    "build_binary_strata",
    "deterministic_pvalue",
    "estimate_convolution_complexity",
    "test_sparse_cmi",
]
