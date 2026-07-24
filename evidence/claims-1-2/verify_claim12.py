"""Standalone evaluator-visible verifier; exits nonzero on evidence failure."""

from __future__ import annotations

import json
import os

for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[variable] = "1"

import numpy as np

from faithful_tpgd import (
    empirical_gradients,
    empirical_loss,
    regularized_gradients,
    regularized_objective,
    simulate_paper_model,
    tpgd_algorithm1,
)


def finite_difference(objective, B, W, epsilon=1e-6):
    numerical_B = np.empty_like(B)
    numerical_W = np.empty_like(W)
    for index in np.ndindex(B.shape):
        plus, minus = B.copy(), B.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical_B[index] = (objective(plus, W) - objective(minus, W)) / (2 * epsilon)
    for index in np.ndindex(W.shape):
        plus, minus = W.copy(), W.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical_W[index] = (objective(B, plus) - objective(B, minus)) / (2 * epsilon)
    return numerical_B, numerical_W


def relative_error(analytic, numerical):
    denominator = max(1.0, float(np.linalg.norm(analytic)), float(np.linalg.norm(numerical)))
    return float(np.linalg.norm(analytic - numerical) / denominator)


def verify():
    rng = np.random.default_rng(1201)
    X, y = simulate_paper_model(4, 7, 5, 2, 0.2, rng)
    B = rng.normal(scale=0.2, size=(5, 2))
    W = rng.normal(scale=0.2, size=(2, 4))
    empirical = empirical_gradients(X, y, B, W)
    empirical_fd = finite_difference(lambda left, right: empirical_loss(X, y, left, right), B, W)
    regularized = regularized_gradients(X, y, B, W)
    regularized_fd = finite_difference(
        lambda left, right: regularized_objective(X, y, left, right), B, W
    )
    empirical_errors = [relative_error(a, n) for a, n in zip(empirical, empirical_fd)]
    regularized_errors = [relative_error(a, n) for a, n in zip(regularized, regularized_fd)]

    imbalance = B.T @ B - W @ W.T
    wrong = (empirical[0] + B @ imbalance, empirical[1] - imbalance @ W)
    wrong_errors = [relative_error(a, n) for a, n in zip(wrong, regularized_fd)]

    rng = np.random.default_rng(1202)
    X, y = simulate_paper_model(100, 100, 100, 10, 0.1, rng)
    _, _, trace = tpgd_algorithm1(X, y, 10, 4, 1e-4, 1e-4, 0.1, rng)
    phases = [record.phase for record in trace]
    corrections = [record.correction_gradient_frobenius for record in trace]

    threshold = 2e-7
    passed = (
        max(empirical_errors + regularized_errors) < threshold
        and phases == ["I", "I", "II", "II"]
        and corrections[:2] == [0.0, 0.0]
        and min(corrections[2:]) > 0.0
        and max(wrong_errors) > 1e-3
        and ["I", "II", "II", "II"] != phases
    )
    return {
        "passed": passed,
        "phase_sequence": phases,
        "correction_gradient_frobenius": corrections,
        "empirical_relative_errors_B_W": empirical_errors,
        "regularized_relative_errors_B_W": regularized_errors,
        "factor_two_control_relative_errors_B_W": wrong_errors,
        "off_by_one_control_failed_as_intended": ["I", "II", "II", "II"] != phases,
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
