"""Faithful implementation of Algorithm 1 and Equation (5) of arXiv 2605.00473.

Arrays follow the paper with one storage convention change: each task design
is stored as ``X[t, n, d]`` rather than as a ``d x N`` matrix. The empirical
objective is still the paper's sum over tasks, normalized by ``2N``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class StepRecord:
    iteration: int
    phase: str
    regularized: bool
    empirical_loss: float
    regularized_objective: float
    imbalance_frobenius: float
    correction_gradient_frobenius: float


def empirical_loss(X: FloatArray, y: FloatArray, B: FloatArray, W: FloatArray) -> float:
    """Equation (1): sum_t ||X_t B w_t - y_t||^2 / (2N)."""
    sample_count = X.shape[1]
    residual = np.einsum("tnd,dk,kt->tn", X, B, W, optimize=True) - y
    return float(np.sum(residual * residual) / (2.0 * sample_count))


def regularized_objective(
    X: FloatArray,
    y: FloatArray,
    B: FloatArray,
    W: FloatArray,
) -> float:
    """Equation (5): empirical loss plus ||B^T B - W W^T||_F^2 / 8."""
    imbalance = B.T @ B - W @ W.T
    return empirical_loss(X, y, B, W) + float(np.sum(imbalance * imbalance) / 8.0)


def empirical_gradients(
    X: FloatArray,
    y: FloatArray,
    B: FloatArray,
    W: FloatArray,
) -> tuple[FloatArray, FloatArray]:
    """Analytic gradients of Equation (1)."""
    sample_count = X.shape[1]
    residual = np.einsum("tnd,dk,kt->tn", X, B, W, optimize=True) - y
    design_residual = np.einsum("tnd,tn->td", X, residual, optimize=True)
    grad_B = np.einsum("td,kt->dk", design_residual, W, optimize=True) / sample_count
    grad_W = np.einsum("dk,td->kt", B, design_residual, optimize=True) / sample_count
    return grad_B, grad_W


def regularized_gradients(
    X: FloatArray,
    y: FloatArray,
    B: FloatArray,
    W: FloatArray,
) -> tuple[FloatArray, FloatArray]:
    """Analytic gradients of Equation (5), including its exact 1/8 penalty."""
    grad_B, grad_W = empirical_gradients(X, y, B, W)
    imbalance = B.T @ B - W @ W.T
    # d/dB (1/8)||B^T B-WW^T||_F^2 = (1/2)B(B^T B-WW^T)
    # d/dW (...) = -(1/2)(B^T B-WW^T)W.
    return grad_B + 0.5 * B @ imbalance, grad_W - 0.5 * imbalance @ W


def initialize(
    d: int,
    k: int,
    T: int,
    alpha_tilde: float,
    rng: np.random.Generator,
) -> tuple[FloatArray, FloatArray]:
    """Algorithm 1 Gaussian initialization, including the asymmetric W / 3."""
    B_tilde = rng.normal(size=(d, k)) / np.sqrt(d)
    W_tilde = rng.normal(size=(k, T)) / np.sqrt(d)
    return alpha_tilde * B_tilde, (alpha_tilde / 3.0) * W_tilde


def tpgd_algorithm1(
    X: FloatArray,
    y: FloatArray,
    k: int,
    K1: int,
    eta1: float,
    eta2: float,
    alpha_tilde: float,
    rng: np.random.Generator,
) -> tuple[FloatArray, FloatArray, list[StepRecord]]:
    """Run Algorithm 1 with the half-open phase ranges printed in the paper.

    ``K1`` must be even because Algorithm 1 switches at exactly ``K1/2``.
    Phase I uses Equation (1); Phase II uses Equation (5).
    """
    if K1 <= 0 or K1 % 2:
        raise ValueError("Algorithm 1 requires a positive even K1")
    if X.ndim != 3 or y.shape != X.shape[:2]:
        raise ValueError("X must have shape (T,N,d) and y shape (T,N)")
    T, _, d = X.shape
    B, W = initialize(d=d, k=k, T=T, alpha_tilde=alpha_tilde, rng=rng)
    records: list[StepRecord] = []

    for iteration in range(K1):
        regularized = iteration >= K1 // 2
        imbalance = B.T @ B - W @ W.T
        if regularized:
            grad_B, grad_W = regularized_gradients(X, y, B, W)
            correction_norm = float(
                np.sqrt(
                    np.sum((0.5 * B @ imbalance) ** 2)
                    + np.sum((0.5 * imbalance @ W) ** 2)
                )
            )
            step_size = eta2
            phase = "II"
        else:
            grad_B, grad_W = empirical_gradients(X, y, B, W)
            correction_norm = 0.0
            step_size = eta1
            phase = "I"
        B = B - step_size * grad_B
        W = W - step_size * grad_W
        new_imbalance = B.T @ B - W @ W.T
        records.append(
            StepRecord(
                iteration=iteration,
                phase=phase,
                regularized=regularized,
                empirical_loss=empirical_loss(X, y, B, W),
                regularized_objective=regularized_objective(X, y, B, W),
                imbalance_frobenius=float(np.linalg.norm(new_imbalance, ord="fro")),
                correction_gradient_frobenius=correction_norm,
            )
        )
    return B, W, records


def simulate_paper_model(
    T: int,
    N: int,
    d: int,
    k: int,
    sigma: float,
    rng: np.random.Generator,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Gaussian special case satisfying the paper's covariance assumptions."""
    raw_basis = rng.normal(size=(d, k))
    B_star, _ = np.linalg.qr(raw_basis, mode="reduced")
    W_star = rng.normal(size=(k, T))
    X = rng.normal(size=(T, N, d))
    signal = np.einsum("tnd,dk,kt->tn", X, B_star, W_star, optimize=True)
    y = signal + rng.normal(scale=sigma, size=(T, N))
    return X, y, B_star, W_star


def subspace_error(estimate: FloatArray, truth: FloatArray) -> float:
    """Normalized projector distance, invariant to factor scaling and rotation."""
    q_est, _ = np.linalg.qr(estimate, mode="reduced")
    q_truth, _ = np.linalg.qr(truth, mode="reduced")
    rank = truth.shape[1]
    difference = q_est @ q_est.T - q_truth @ q_truth.T
    return float(np.linalg.norm(difference, ord="fro") / np.sqrt(2.0 * rank))
