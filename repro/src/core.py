"""Historical small-scale utilities for the judged TPGD baseline.

This module reconstructs the code path described in the exact judged Space
revision.  It is intentionally retained as a historical toy control; stronger
claim contracts live only on descendant experiment branches.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def simulate_multitask(
    T: int,
    N: int,
    d: int,
    k: int,
    sigma: float,
    rng: np.random.Generator,
) -> tuple[list[FloatArray], list[FloatArray], FloatArray, FloatArray, FloatArray]:
    """Generate isotropic Gaussian linear tasks sharing a rank-k subspace."""
    raw = rng.normal(size=(d, k))
    B_star, _ = np.linalg.qr(raw, mode="reduced")
    W_star = rng.normal(scale=0.7, size=(k, T))
    theta_star = B_star @ W_star
    X: list[FloatArray] = []
    y: list[FloatArray] = []
    for task in range(T):
        design = rng.normal(size=(N, d))
        noise = rng.normal(scale=sigma, size=N)
        X.append(design)
        y.append(design @ theta_star[:, task] + noise)
    return X, y, B_star, W_star, theta_star


def per_task_ols(X: list[FloatArray], y: list[FloatArray]) -> FloatArray:
    """Fit each task independently and stack the d-dimensional predictors."""
    estimates = [np.linalg.lstsq(design, target, rcond=None)[0] for design, target in zip(X, y)]
    return np.column_stack(estimates)


def spectral_representation(theta_hat: FloatArray, k: int) -> tuple[FloatArray, FloatArray]:
    """Return the top-k left singular subspace and task coordinates."""
    left, _, _ = np.linalg.svd(theta_hat, full_matrices=False)
    basis = left[:, :k]
    return basis, basis.T @ theta_hat


def subspace_error(estimate: FloatArray, truth: FloatArray) -> float:
    """Normalized Frobenius distance between orthogonal projectors."""
    q_est, _ = np.linalg.qr(estimate, mode="reduced")
    q_truth, _ = np.linalg.qr(truth, mode="reduced")
    rank = truth.shape[1]
    return float(np.linalg.norm(q_est @ q_est.T - q_truth @ q_truth.T, ord="fro") / np.sqrt(2 * rank))


def avg_prediction_error(estimate: FloatArray, truth: FloatArray) -> float:
    """Average squared Euclidean parameter error across tasks."""
    return float(np.mean(np.sum((estimate - truth) ** 2, axis=0)))


def _loss(X: list[FloatArray], y: list[FloatArray], B: FloatArray, W: FloatArray) -> float:
    total = 0.0
    for task, (design, target) in enumerate(zip(X, y)):
        residual = design @ (B @ W[:, task]) - target
        total += float(residual @ residual)
    return total / (2.0 * sum(len(target) for target in y))


def tpgd(
    X: list[FloatArray],
    y: list[FloatArray],
    k: int,
    phase1_iters: int,
    phase2_iters: int,
    lr: float,
    lam: float,
    rng: np.random.Generator,
) -> tuple[FloatArray, FloatArray, int, list[float]]:
    """Run the historical two-phase first-order baseline.

    Phase I follows gradients of the empirical likelihood. Phase II adds the
    gradient of ``lam/8 * ||B.T B - W W.T||_F^2``. The normalization by the
    total sample count keeps this small baseline numerically stable.
    """
    d = X[0].shape[1]
    T = len(X)
    B = rng.normal(scale=0.25 / np.sqrt(d), size=(d, k))
    W = rng.normal(scale=0.25 / np.sqrt(d), size=(k, T))
    losses: list[float] = []
    total_samples = float(sum(len(target) for target in y))

    for iteration in range(phase1_iters + phase2_iters):
        grad_B = np.zeros_like(B)
        grad_W = np.zeros_like(W)
        for task, (design, target) in enumerate(zip(X, y)):
            residual = design @ (B @ W[:, task]) - target
            design_residual = design.T @ residual
            grad_B += np.outer(design_residual, W[:, task])
            grad_W[:, task] = B.T @ design_residual
        grad_B /= total_samples
        grad_W /= total_samples

        if iteration >= phase1_iters:
            imbalance = B.T @ B - W @ W.T
            grad_B += 0.5 * lam * B @ imbalance
            grad_W -= 0.5 * lam * imbalance @ W

        B = B - lr * grad_B
        W = W - lr * grad_W
        losses.append(_loss(X, y, B, W))

    return B, W, phase1_iters + phase2_iters, losses

