from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import time

import numpy as np

from .models import Stratum


DEFAULT_JIDT_JAR = Path(
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/"
    "jidt/infodynamics.jar"
)


@dataclass(frozen=True)
class JIDTConditionalResult:
    pvalue: float
    tie_corrected_pvalue: float
    g2: float
    mi_bits: float
    elapsed_seconds: float
    permutations: int
    shuffle_mode: str


def start_jidt_jvm(jar_path: str | Path = DEFAULT_JIDT_JAR) -> None:
    import jpype
    import jpype.imports  # noqa: F401

    path = Path(jar_path)
    if not path.exists():
        raise FileNotFoundError(f"JIDT jar not found: {path}")
    if not jpype.isJVMStarted():
        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            "-ea",
            f"-Djava.class.path={path}",
            convertStrings=True,
        )


def strata_to_observations(
    strata: Sequence[Stratum],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_values: list[int] = []
    y_values: list[int] = []
    z_values: list[int] = []
    for z_index, stratum in enumerate(strata):
        counts = (
            (0, 0, stratum.n - stratum.r - stratum.s + stratum.a_observed),
            (0, 1, stratum.s - stratum.a_observed),
            (1, 0, stratum.r - stratum.a_observed),
            (1, 1, stratum.a_observed),
        )
        for x_value, y_value, count in counts:
            if count:
                x_values.extend([x_value] * count)
                y_values.extend([y_value] * count)
                z_values.extend([z_index] * count)
    return (
        np.asarray(x_values, dtype=np.int32),
        np.asarray(y_values, dtype=np.int32),
        np.asarray(z_values, dtype=np.int32),
    )


def jidt_reconstructed_condition_indices(
    strata: Sequence[Stratum],
) -> tuple[np.ndarray, ...]:
    """Indices by Z in JIDT's internally reconstructed observation order."""

    groups: list[list[int]] = [[] for _ in strata]
    position = 0
    for x_value in range(2):
        for y_value in range(2):
            for z_index, stratum in enumerate(strata):
                if x_value == 1 and y_value == 1:
                    count = stratum.a_observed
                elif x_value == 1:
                    count = stratum.r - stratum.a_observed
                elif y_value == 1:
                    count = stratum.s - stratum.a_observed
                else:
                    count = (
                        stratum.n
                        - stratum.r
                        - stratum.s
                        + stratum.a_observed
                    )
                groups[z_index].extend(range(position, position + count))
                position += count
    return tuple(np.asarray(group, dtype=np.int32) for group in groups)


def blockwise_jidt_orderings(
    strata: Sequence[Stratum],
    permutations: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if permutations <= 0:
        raise ValueError("permutations must be positive")
    total_n = sum(stratum.n for stratum in strata)
    base = np.arange(total_n, dtype=np.int32)
    orderings = np.tile(base, (permutations, 1))
    for indices in jidt_reconstructed_condition_indices(strata):
        if indices.size > 1:
            random_keys = rng.random((permutations, indices.size))
            within_orders = np.argsort(random_keys, axis=1)
            orderings[:, indices] = indices[within_orders]
    return orderings


def jidt_conditional_significance(
    strata: Sequence[Stratum],
    *,
    permutations: int,
    shuffle_mode: str,
    rng: np.random.Generator | None = None,
    jar_path: str | Path = DEFAULT_JIDT_JAR,
) -> JIDTConditionalResult:
    if shuffle_mode not in {"blockwise", "default_global"}:
        raise ValueError("shuffle_mode must be 'blockwise' or 'default_global'")
    if permutations <= 0:
        raise ValueError("permutations must be positive")

    start_jidt_jvm(jar_path)
    from infodynamics.measures.discrete import (
        ConditionalMutualInformationCalculatorDiscrete,
    )
    from jpype.types import JArray, JInt

    x_values, y_values, z_values = strata_to_observations(strata)
    started = time.perf_counter()
    calculator = ConditionalMutualInformationCalculatorDiscrete(
        2,
        2,
        len(strata),
    )
    calculator.initialise()
    calculator.addObservations(
        JArray(JInt)(x_values),
        JArray(JInt)(y_values),
        JArray(JInt)(z_values),
    )
    mi_bits = float(calculator.computeAverageLocalOfObservations())
    if shuffle_mode == "blockwise":
        generator = rng if rng is not None else np.random.default_rng()
        orderings = blockwise_jidt_orderings(
            strata,
            permutations,
            generator,
        )
        distribution = calculator.computeSignificance(
            JArray(JInt, 2)(orderings)
        )
    else:
        distribution = calculator.computeSignificance(int(permutations))
    elapsed = time.perf_counter() - started
    g2 = 2.0 * x_values.size * mi_bits * np.log(2.0)
    surrogate_g2 = (
        np.asarray(distribution.distribution, dtype=np.float64)
        * 2.0
        * x_values.size
        * np.log(2.0)
    )
    tie_corrected_pvalue = float(
        np.mean(surrogate_g2 >= g2 - 1e-10)
    )
    return JIDTConditionalResult(
        pvalue=float(distribution.pValue),
        tie_corrected_pvalue=tie_corrected_pvalue,
        g2=float(g2),
        mi_bits=mi_bits,
        elapsed_seconds=elapsed,
        permutations=permutations,
        shuffle_mode=shuffle_mode,
    )
