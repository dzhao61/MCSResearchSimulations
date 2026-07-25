from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .models import Stratum


def _binary_array(values: Sequence[int], name: str) -> np.ndarray:
    array = np.asarray(values)
    if array.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if not np.all(np.isin(array, (0, 1))):
        raise ValueError(f"{name} must contain only 0 and 1")
    return array.astype(np.int8, copy=False)


def build_binary_strata(
    x: Sequence[int],
    y: Sequence[int],
    z: Sequence[object],
) -> list[Stratum]:
    """Convert raw binary observations into fixed-margin stratum summaries."""

    x_array = _binary_array(x, "x")
    y_array = _binary_array(y, "y")
    z_array = np.asarray(z)
    if z_array.ndim != 1:
        raise ValueError("z must be one-dimensional")
    if not (x_array.size == y_array.size == z_array.size):
        raise ValueError("x, y, and z must have equal lengths")

    strata: list[Stratum] = []
    for label in np.unique(z_array):
        mask = z_array == label
        x_part = x_array[mask]
        y_part = y_array[mask]
        strata.append(
            Stratum(
                n=int(mask.sum()),
                r=int(x_part.sum()),
                s=int(y_part.sum()),
                a_observed=int(np.dot(x_part, y_part)),
                label=label.item() if hasattr(label, "item") else label,
            )
        )
    return strata

