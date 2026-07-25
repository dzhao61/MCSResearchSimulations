from __future__ import annotations

import os
import shlex
import time
from dataclasses import dataclass

import numpy as np


DEFAULT_JIDT_JAR = (
    "/Users/danielzhao/MyMac/Masters Degree/CSYS5030/JIDT/jidt/infodynamics.jar"
)


def init_jvm(jar_path: str = DEFAULT_JIDT_JAR) -> None:
    import jpype
    import jpype.imports  # noqa: F401

    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JIDT jar not found: {jar_path}")
    if not jpype.isJVMStarted():
        extra_jvm_args = shlex.split(os.environ.get("JIDT_JVM_ARGS", ""))
        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            "-ea",
            *extra_jvm_args,
            "-Djava.class.path=" + jar_path,
            convertStrings=True,
        )


def table_to_observations(table: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    counts = np.asarray(table, dtype=np.int64)
    total = int(counts.sum())
    x = np.empty(total, dtype=np.int32)
    y = np.empty(total, dtype=np.int32)
    pos = 0
    for i in range(counts.shape[0]):
        for j in range(counts.shape[1]):
            cell = int(counts[i, j])
            if cell == 0:
                continue
            end = pos + cell
            x[pos:end] = i
            y[pos:end] = j
            pos = end
    return x, y


@dataclass(frozen=True)
class JIDTResult:
    pvalue: float
    g_statistic: float
    elapsed_s: float


def jidt_permutation_pvalue(
    table: np.ndarray,
    r_nominal: int,
    c_nominal: int,
    shuffles: int,
    jar_path: str = DEFAULT_JIDT_JAR,
) -> JIDTResult:
    init_jvm(jar_path)
    from infodynamics.measures.discrete import MutualInformationCalculatorDiscrete

    counts = np.asarray(table, dtype=np.int64)
    n = int(counts.sum())
    x, y = table_to_observations(counts)
    start = time.perf_counter()
    calc = MutualInformationCalculatorDiscrete(r_nominal, c_nominal, 0)
    calc.initialise()
    calc.addObservations(x.tolist(), y.tolist())
    mi_bits = float(calc.computeAverageLocalOfObservations())
    g_value = float(2.0 * n * mi_bits * np.log(2.0))
    dist = calc.computeSignificance(int(shuffles))
    return JIDTResult(
        pvalue=float(dist.pValue),
        g_statistic=g_value,
        elapsed_s=time.perf_counter() - start,
    )
