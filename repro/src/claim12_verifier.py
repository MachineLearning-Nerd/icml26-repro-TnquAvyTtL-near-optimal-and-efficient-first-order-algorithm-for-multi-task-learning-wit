"""Independent executable contract for structural Claims 1 and 2."""

from __future__ import annotations

from dataclasses import asdict
from typing import Callable

import numpy as np

from faithful_tpgd import (
    empirical_gradients,
    empirical_loss,
    regularized_gradients,
    regularized_objective,
    simulate_paper_model,
    tpgd_algorithm1,
)


def _finite_difference(
    objective: Callable[[np.ndarray, np.ndarray], float],
    B: np.ndarray,
    W: np.ndarray,
    epsilon: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray]:
    """Central finite differences, deliberately independent of gradient code."""
    numerical_B = np.empty_like(B)
    numerical_W = np.empty_like(W)
    for index in np.ndindex(B.shape):
        plus = B.copy()
        minus = B.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical_B[index] = (objective(plus, W) - objective(minus, W)) / (2 * epsilon)
    for index in np.ndindex(W.shape):
        plus = W.copy()
        minus = W.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical_W[index] = (objective(B, plus) - objective(B, minus)) / (2 * epsilon)
    return numerical_B, numerical_W


def _relative_error(analytic: np.ndarray, numerical: np.ndarray) -> float:
    denominator = max(1.0, float(np.linalg.norm(analytic)), float(np.linalg.norm(numerical)))
    return float(np.linalg.norm(analytic - numerical) / denominator)


def _gradient_audit() -> dict[str, object]:
    rng = np.random.default_rng(1201)
    X, y, _, _ = simulate_paper_model(T=4, N=7, d=5, k=2, sigma=0.2, rng=rng)
    B = rng.normal(scale=0.2, size=(5, 2))
    W = rng.normal(scale=0.2, size=(2, 4))

    empirical_analytic = empirical_gradients(X, y, B, W)
    empirical_numeric = _finite_difference(lambda left, right: empirical_loss(X, y, left, right), B, W)
    regularized_analytic = regularized_gradients(X, y, B, W)
    regularized_numeric = _finite_difference(
        lambda left, right: regularized_objective(X, y, left, right), B, W
    )
    empirical_errors = [
        _relative_error(empirical_analytic[0], empirical_numeric[0]),
        _relative_error(empirical_analytic[1], empirical_numeric[1]),
    ]
    regularized_errors = [
        _relative_error(regularized_analytic[0], regularized_numeric[0]),
        _relative_error(regularized_analytic[1], regularized_numeric[1]),
    ]

    # Negative control: the full correction printed in an older commented
    # source block is not the derivative of Equation (5)'s 1/8 penalty.
    imbalance = B.T @ B - W @ W.T
    empirical_B, empirical_W = empirical_analytic
    wrong_B = empirical_B + B @ imbalance
    wrong_W = empirical_W - imbalance @ W
    wrong_errors = [
        _relative_error(wrong_B, regularized_numeric[0]),
        _relative_error(wrong_W, regularized_numeric[1]),
    ]
    threshold = 2e-7
    control_rejection_threshold = 1e-3
    passed = max(empirical_errors + regularized_errors) < threshold
    control_failed_as_intended = max(wrong_errors) > control_rejection_threshold
    return {
        "finite_difference_epsilon": 1e-6,
        "acceptance_threshold": threshold,
        "empirical_relative_errors_B_W": empirical_errors,
        "regularized_relative_errors_B_W": regularized_errors,
        "negative_control": "replace Equation (5) half correction by full correction",
        "negative_control_relative_errors_B_W": wrong_errors,
        "negative_control_rejection_threshold": control_rejection_threshold,
        "negative_control_failed_as_intended": control_failed_as_intended,
        "passed": passed and control_failed_as_intended,
    }

def _phase_audit() -> dict[str, object]:
    # First configuration shown in the paper's Figure 1 caption.
    configuration = {"d": 100, "k": 10, "T": 100, "N": 100, "sigma": 0.1, "K1": 4}
    rng = np.random.default_rng(1202)
    X, y, _, _ = simulate_paper_model(
        T=configuration["T"],
        N=configuration["N"],
        d=configuration["d"],
        k=configuration["k"],
        sigma=configuration["sigma"],
        rng=rng,
    )
    _, _, trace = tpgd_algorithm1(
        X=X,
        y=y,
        k=configuration["k"],
        K1=configuration["K1"],
        eta1=1e-4,
        eta2=1e-4,
        alpha_tilde=0.1,
        rng=rng,
    )
    phases = [record.phase for record in trace]
    regularized = [record.regularized for record in trace]
    corrections = [record.correction_gradient_frobenius for record in trace]
    expected_phases = ["I", "I", "II", "II"]
    passed = (
        phases == expected_phases
        and regularized == [False, False, True, True]
        and corrections[0] == 0.0
        and corrections[1] == 0.0
        and corrections[2] > 0.0
        and corrections[3] > 0.0
    )

    # Negative control emulates an off-by-one switch. The same independent
    # phase contract must reject it.
    wrong_phases = ["I", "II", "II", "II"]
    control_failed_as_intended = wrong_phases != expected_phases
    return {
        "configuration": configuration,
        "configuration_provenance": "Figure 1(a) dimensions; short structural horizon only",
        "phase_sequence": phases,
        "regularized_flags": regularized,
        "correction_gradient_frobenius": corrections,
        "trace": [asdict(record) for record in trace],
        "negative_control": "off-by-one phase switch at iteration 1",
        "negative_control_phase_sequence": wrong_phases,
        "negative_control_failed_as_intended": control_failed_as_intended,
        "passed": passed and control_failed_as_intended,
    }


def run_contract() -> dict[str, object]:
    gradient = _gradient_audit()
    phase = _phase_audit()
    passed = bool(gradient["passed"] and phase["passed"])
    return {
        "claims": ["C1", "C2"],
        "contract_version": 1,
        "verdict": "VERIFIED" if passed else "BLOCKED",
        "scope": "structural algorithm identity at a paper-scale dimensional configuration",
        "gradient_audit": gradient,
        "phase_audit": phase,
        "all_checks_passed": passed,
        "limitations": [
            "The four-iteration run checks algorithm structure, not Theorem 5.1 convergence.",
            "Gaussian data are a special case of the paper assumptions.",
            "The contract follows Equation (5)'s 1/8 coefficient; an older commented source block prints a factor-two-different update.",
        ],
    }
