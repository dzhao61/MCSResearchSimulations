from __future__ import annotations

from dataclasses import dataclass

from .models import Stratum


@dataclass(frozen=True)
class ValidationConfiguration:
    name: str
    family: str
    strata: tuple[Stratum, ...]
    description: str

    @property
    def total_n(self) -> int:
        return sum(item.n for item in self.strata)


def _nondegenerate_count(n: int, probability: float) -> int:
    if n < 2:
        return 0
    return min(n - 1, max(1, int(round(n * probability))))


def homogeneous_configuration(
    *,
    k: int,
    n: int,
    p_x: float,
    p_y: float,
    label: str,
) -> ValidationConfiguration:
    r = _nondegenerate_count(n, p_x)
    s = _nondegenerate_count(n, p_y)
    expected_a = r * s / n
    lower = max(0, r + s - n)
    upper = min(r, s)
    observed_a = min(upper, max(lower, int(round(expected_a))))
    strata = tuple(Stratum(n, r, s, observed_a, z) for z in range(k))
    return ValidationConfiguration(
        name=f"homogeneous_k{k}_n{n}_{label}",
        family="homogeneous",
        strata=strata,
        description=(
            f"{k} equal strata of size {n}; p_x={p_x:.2f}, p_y={p_y:.2f}"
        ),
    )


def few_informative_configuration(
    *,
    k: int,
    informative: int,
) -> ValidationConfiguration:
    strata: list[Stratum] = []
    for z in range(k):
        if z < informative:
            strata.append(Stratum(5, 2, 2, 1, z))
        elif z % 2:
            strata.append(Stratum(3, 0, 1, 0, z))
        else:
            strata.append(Stratum(3, 1, 3, 1, z))
    return ValidationConfiguration(
        name=f"few_informative_k{k}_m{informative}",
        family="few_informative",
        strata=tuple(strata),
        description=f"{informative} informative strata among {k}",
    )


def dominant_stratum_configuration(k: int) -> ValidationConfiguration:
    strata = [Stratum(30, 15, 15, 8, 0)]
    for z in range(1, k):
        if z % 3 == 0:
            strata.append(Stratum(4, 1, 1, 0, z))
        elif z % 3 == 1:
            strata.append(Stratum(3, 0, 1, 0, z))
        else:
            strata.append(Stratum(3, 1, 3, 1, z))
    return ValidationConfiguration(
        name=f"dominant_stratum_k{k}",
        family="dominant_stratum",
        strata=tuple(strata),
        description="one large balanced stratum plus sparse/degenerate strata",
    )


def heterogeneous_configuration(k: int, variant: int) -> ValidationConfiguration:
    sizes = (3, 5, 10, 20, 30)
    margin_pairs = (
        (0.50, 0.50),
        (0.10, 0.50),
        (0.10, 0.10),
        (0.90, 0.10),
        (0.25, 0.75),
    )
    strata: list[Stratum] = []
    for z in range(k):
        n = sizes[(z + variant) % len(sizes)]
        p_x, p_y = margin_pairs[(2 * z + variant) % len(margin_pairs)]
        r = _nondegenerate_count(n, p_x)
        s = _nondegenerate_count(n, p_y)
        lower = max(0, r + s - n)
        upper = min(r, s)
        expected = r * s / n
        offset = (-1, 0, 1)[(z + variant) % 3]
        observed = min(upper, max(lower, int(round(expected)) + offset))
        strata.append(Stratum(n, r, s, observed, z))
    return ValidationConfiguration(
        name=f"heterogeneous_k{k}_v{variant}",
        family="heterogeneous",
        strata=tuple(strata),
        description="unequal sizes and asymmetric, mixed margins",
    )


def validation_configurations(profile: str) -> list[ValidationConfiguration]:
    if profile not in {"smoke", "full"}:
        raise ValueError("profile must be 'smoke' or 'full'")

    if profile == "smoke":
        k_values = (5, 20, 100)
        n_values = (3, 10, 30)
        margin_specs = (
            ("balanced", 0.50, 0.50),
            ("x_skew", 0.10, 0.50),
            ("both_skew", 0.10, 0.10),
            ("opposing_skew", 0.10, 0.90),
        )
    else:
        k_values = (5, 10, 20, 50, 100)
        n_values = (3, 5, 10, 20, 30)
        margin_specs = (
            ("balanced", 0.50, 0.50),
            ("x_skew", 0.10, 0.50),
            ("both_skew", 0.10, 0.10),
            ("opposing_skew", 0.10, 0.90),
            ("extreme_asymmetric", 0.05, 0.95),
        )

    homogeneous = [
        homogeneous_configuration(k=k, n=n, p_x=p_x, p_y=p_y, label=label)
        for k in k_values
        for n in n_values
        for label, p_x, p_y in margin_specs
    ]
    # Binary row/column relabelling and swapping X/Y leave G^2 unchanged.
    # Keep one representative of each conditional fixed-margin null so that
    # equivalent probability labels do not receive extra weight.
    configurations: list[ValidationConfiguration] = []
    seen_signatures: set[tuple[tuple[int, int, int], ...]] = set()
    for configuration in homogeneous:
        signature = tuple(
            (
                item.n,
                min(min(item.r, item.n - item.r), min(item.s, item.n - item.s)),
                max(min(item.r, item.n - item.r), min(item.s, item.n - item.s)),
            )
            for item in configuration.strata
        )
        if signature not in seen_signatures:
            seen_signatures.add(signature)
            configurations.append(configuration)

    adversarial_k = (20, 100) if profile == "smoke" else (10, 20, 50, 100)
    for k in adversarial_k:
        informative_values = (2, 5) if profile == "smoke" else (2, 3, 5, 10)
        for informative in informative_values:
            if informative <= k:
                configurations.append(
                    few_informative_configuration(k=k, informative=informative)
                )
        configurations.append(dominant_stratum_configuration(k))
        configurations.append(heterogeneous_configuration(k, variant=0))
        if profile == "full":
            configurations.append(heterogeneous_configuration(k, variant=1))

    return configurations
