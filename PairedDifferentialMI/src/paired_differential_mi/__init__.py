"""Paired differential mutual-information feasibility implementation."""

from .core import paired_bootstrap_t, paired_mi_tests
from .distributions import PairedScenario, pilot_scenarios

__all__ = [
    "PairedScenario",
    "paired_bootstrap_t",
    "paired_mi_tests",
    "pilot_scenarios",
]
