"""Evaluator-visible copy of the implementation used by evidence commit 9f27743."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StepRecord:
    iteration: int
    phase: str
    regularized: bool
    empirical_loss: float
    regularized_objective: float
    imbalance_frobenius: float
    correction_gradient_frobenius: float


def empirical_loss(X, y, B, W):
    """Equation (1): sum_t ||X_t B w_t - y_t||^2 / (2N)."""
    residual = np.einsum("tnd,dk,kt->tn", X, B, W, optimize=True) - y
    return float(np.sum(residual * residual) / (2.0 * X.shape[1]))


def regularized_objective(X, y, B, W):
    """Equation (5): empirical loss plus ||B^T B - W W^T||_F^2 / 8."""
    imbalance = B.T @ B - W @ W.T
    return empirical_loss(X, y, B, W) + float(np.sum(imbalance * imbalance) / 8.0)


def empirical_gradients(X, y, B, W):
    residual = np.einsum("tnd,dk,kt->tn", X, B, W, optimize=True) - y
    design_residual = np.einsum("tnd,tn->td", X, residual, optimize=True)
    grad_B = np.einsum("td,kt->dk", design_residual, W, optimize=True) / X.shape[1]
    grad_W = np.einsum("dk,td->kt", B, design_residual, optimize=True) / X.shape[1]
    return grad_B, grad_W


def regularized_gradients(X, y, B, W):
    """Exact derivative of Equation (5)'s displayed 1/8 penalty."""
    grad_B, grad_W = empirical_gradients(X, y, B, W)
    imbalance = B.T @ B - W @ W.T
    return grad_B + 0.5 * B @ imbalance, grad_W - 0.5 * imbalance @ W


def initialize(d, k, T, alpha_tilde, rng):
    B_tilde = rng.normal(size=(d, k)) / np.sqrt(d)
    W_tilde = rng.normal(size=(k, T)) / np.sqrt(d)
    return alpha_tilde * B_tilde, (alpha_tilde / 3.0) * W_tilde


def tpgd_algorithm1(X, y, k, K1, eta1, eta2, alpha_tilde, rng):
    if K1 <= 0 or K1 % 2:
        raise ValueError("Algorithm 1 requires a positive even K1")
    T, _, d = X.shape
    B, W = initialize(d, k, T, alpha_tilde, rng)
    records = []
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
            step_size, phase = eta2, "II"
        else:
            grad_B, grad_W = empirical_gradients(X, y, B, W)
            correction_norm = 0.0
            step_size, phase = eta1, "I"
        B -= step_size * grad_B
        W -= step_size * grad_W
        new_imbalance = B.T @ B - W @ W.T
        records.append(
            StepRecord(
                iteration,
                phase,
                regularized,
                empirical_loss(X, y, B, W),
                regularized_objective(X, y, B, W),
                float(np.linalg.norm(new_imbalance, ord="fro")),
                correction_norm,
            )
        )
    return B, W, records


def simulate_paper_model(T, N, d, k, sigma, rng):
    raw_basis = rng.normal(size=(d, k))
    B_star, _ = np.linalg.qr(raw_basis, mode="reduced")
    W_star = rng.normal(size=(k, T))
    X = rng.normal(size=(T, N, d))
    signal = np.einsum("tnd,dk,kt->tn", X, B_star, W_star, optimize=True)
    y = signal + rng.normal(scale=sigma, size=(T, N))
    return X, y
