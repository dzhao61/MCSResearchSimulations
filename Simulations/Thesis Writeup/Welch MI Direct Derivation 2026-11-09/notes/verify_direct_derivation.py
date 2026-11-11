"""Check the direct centred-variance derivation independently of the estimator."""

from pathlib import Path
import json
import re
import sys

import numpy as np


def values(probability):
    row = probability.sum(axis=1, keepdims=True)
    column = probability.sum(axis=0, keepdims=True)
    pointwise = np.log(probability / (row * column))
    mi = np.sum(probability * pointwise)
    centred = pointwise - mi
    variance = np.sum(probability * centred**2)
    return row, column, pointwise, mi, centred, variance


def main():
    rng = np.random.default_rng(8092026)
    errors = {name: 0.0 for name in
              ("mean_cancellation", "weight_contribution", "score_contribution",
               "full_sensitivity", "finite_difference")}
    cases = 0
    for shape in ((2, 2), (2, 3), (3, 4), (4, 4)):
        for _ in range(12):
            p = rng.uniform(.5, 2., size=shape)
            p /= p.sum()
            row, column, ell, mi, centred, variance = values(p)
            row_mean = np.sum(p * ell, axis=1, keepdims=True) / row
            column_mean = np.sum(p * ell, axis=0, keepdims=True) / column
            final = centred**2 - variance + 2 * (ell - row_mean - column_mean + mi)
            errors["mean_cancellation"] = max(errors["mean_cancellation"],
                                               abs(np.sum(p * centred)))
            for cell in np.ndindex(shape):
                point = np.zeros_like(p)
                point[cell] = 1
                direction = point - p
                derivative = (direction / p
                              - direction.sum(axis=1, keepdims=True) / row
                              - direction.sum(axis=0, keepdims=True) / column)
                weights = np.sum(direction * centred**2)
                scores = np.sum(p * centred * derivative)
                expected_scores = (ell[cell] - row_mean[cell[0], 0]
                                   - column_mean[0, cell[1]] + mi)
                sensitivity = weights + 2 * scores
                errors["weight_contribution"] = max(
                    errors["weight_contribution"],
                    abs(weights - (centred[cell]**2 - variance)))
                errors["score_contribution"] = max(
                    errors["score_contribution"], abs(scores - expected_scores))
                errors["full_sensitivity"] = max(
                    errors["full_sensitivity"], abs(sensitivity - final[cell]))
                epsilon = 1e-6
                finite_difference = (values(p + epsilon * direction)[-1]
                                     - values(p - epsilon * direction)[-1]) / (2 * epsilon)
                errors["finite_difference"] = max(
                    errors["finite_difference"], abs(finite_difference - sensitivity))
                cases += 1
    assert all(value < 1e-12 for key, value in errors.items() if key != "finite_difference")
    assert errors["finite_difference"] < 1e-8

    root = Path(__file__).resolve().parents[1]
    original = root.parent / "Welch MI/chapters_rewrite/04_expanded_welch.tex"
    current = root / "chapters_rewrite/04_expanded_welch.tex"
    preserved = []
    if original.exists():
        def blocks(path):
            result = {}
            for match in re.finditer(r"\\begin\{(equation\*?|align\*?)\}.*?\\end\{\1\}",
                                     path.read_text(), re.S):
                for label in re.findall(r"\\label\{([^}]+)\}", match.group()):
                    result[label] = re.sub(r"\s+", "", match.group())
            return result
        before, after = blocks(original), blocks(current)
        for label in ("eq:g-final", "eq:population-component-df", "eq:g-hat",
                      "eq:tau-hat", "eq:nu-p-hat", "eq:ws-general",
                      "eq:expanded-df", "eq:expanded-p", "eq:worked-tables",
                      "eq:near-independent-moments", "eq:near-independent-df"):
            assert before[label] == after[label], label
            preserved.append(label)
    report = {"population_tables": 48, "cell_perturbations": cases,
              "maximum_absolute_errors": {key: float(value) for key, value in errors.items()},
              "preserved_core_equations": preserved, "all_pass": True}
    output = json.dumps(report, indent=2) + "\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(output)
    print(output)


if __name__ == "__main__":
    main()
