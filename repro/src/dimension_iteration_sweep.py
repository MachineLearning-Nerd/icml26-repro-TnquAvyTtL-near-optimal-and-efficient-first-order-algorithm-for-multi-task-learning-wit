"""Direct TPGD dimension sweep under fixed condition number and exact RIP."""

from __future__ import annotations

import time

import numpy as np

from dimension_iteration_config import DIMENSION_ITERATION_CONFIG
from faithful_tpgd import initialize


def _unit_spectrum_truth(d: int, k: int, tasks: int, rng: np.random.Generator):
    basis, _ = np.linalg.qr(rng.normal(size=(d, k)), mode="reduced")
    task_columns, _ = np.linalg.qr(rng.normal(size=(tasks, k)), mode="reduced")
    weights = task_columns.T
    truth = basis @ weights
    return truth


def _gradients(B, W, truth, regularized):
    residual = B @ W - truth
    grad_B = residual @ W.T
    grad_W = B.T @ residual
    if regularized:
        imbalance = B.T @ B - W @ W.T
        grad_B = grad_B + 0.5 * B @ imbalance
        grad_W = grad_W - 0.5 * imbalance @ W
    return grad_B, grad_W


def _relative_squared_error(B, W, truth):
    return float(
        np.linalg.norm(B @ W - truth, ord="fro") ** 2
        / np.linalg.norm(truth, ord="fro") ** 2
    )


def _run_one(d, seed, dimension_dependent_steps=False):
    config = DIMENSION_ITERATION_CONFIG
    rng = np.random.default_rng(seed)
    truth = _unit_spectrum_truth(d, config["k"], config["T"], rng)
    singular_values = np.linalg.svd(truth, compute_uv=False)
    sigma_1 = float(singular_values[0])
    sigma_k = float(singular_values[config["k"] - 1])
    eta_scale = 32.0 / d if dimension_dependent_steps else 1.0
    eta1 = config["eta1_times_sigma1"] * eta_scale / sigma_1
    eta2 = config["eta2_times_sigma1"] * eta_scale / sigma_1
    B, W = initialize(d, config["k"], config["T"], config["alpha_tilde"], rng)
    first_hit = None
    initial_error = _relative_squared_error(B, W, truth)
    for iteration in range(config["K1"]):
        regularized = iteration >= config["K1"] // 2
        grad_B, grad_W = _gradients(B, W, truth, regularized)
        step = eta2 if regularized else eta1
        B -= step * grad_B
        W -= step * grad_W
        error = _relative_squared_error(B, W, truth)
        if first_hit is None and error <= config["relative_squared_error_target"]:
            first_hit = iteration + 1
    return {
        "d": d,
        "k": config["k"],
        "T": config["T"],
        "seed": seed,
        "exact_rip_delta": 0.0,
        "sigma_1_M_star": sigma_1,
        "sigma_k_M_star": sigma_k,
        "condition_number": sigma_1 / sigma_k,
        "eta1": eta1,
        "eta2": eta2,
        "dimension_dependent_step_control": dimension_dependent_steps,
        "initial_relative_squared_error": initial_error,
        "final_relative_squared_error": _relative_squared_error(B, W, truth),
        "first_hit_iteration": first_hit,
    }


def run_dimension_iteration_sweep():
    started = time.perf_counter()
    config = DIMENSION_ITERATION_CONFIG
    rows = [
        _run_one(d, seed)
        for d in config["d_values"]
        for seed in config["seeds"]
    ]
    medians = {}
    for d in config["d_values"]:
        hits = [row["first_hit_iteration"] for row in rows if row["d"] == d]
        medians[str(d)] = float(np.median(hits)) if all(hits) else None
    finite_medians = [value for value in medians.values() if value is not None]
    median_ratio = (
        max(finite_medians) / min(finite_medians)
        if len(finite_medians) == len(config["d_values"])
        else None
    )
    slope = (
        float(
            np.polyfit(
                np.log(np.asarray(config["d_values"], dtype=float)),
                np.log(np.asarray(finite_medians, dtype=float)),
                1,
            )[0]
        )
        if len(finite_medians) == len(config["d_values"])
        else None
    )

    control_rows = [
        _run_one(d, config["seeds"][0], dimension_dependent_steps=True)
        for d in config["d_values"]
    ]
    control_hits = [row["first_hit_iteration"] for row in control_rows]
    control_rejected = (
        any(hit is None for hit in control_hits)
        or max(control_hits) / min(control_hits) > config["maximum_median_iteration_ratio"]
    )
    passed = (
        median_ratio is not None
        and median_ratio <= config["maximum_median_iteration_ratio"]
        and slope is not None
        and abs(slope) <= config["maximum_absolute_loglog_slope"]
        and control_rejected
        and max(abs(row["condition_number"] - 1.0) for row in rows) < 1e-12
    )
    return {
        "artifact_status": "DIRECT_TPGD_SCOPED_CORROBORATION",
        "claim": "C4",
        "configuration": config,
        "rows": rows,
        "median_first_hit_by_d": medians,
        "maximum_to_minimum_median_iteration_ratio": median_ratio,
        "loglog_median_iteration_vs_d_slope": slope,
        "negative_control": {
            "mutation": "replace constant normalized step sizes by step sizes proportional to 1/d",
            "rows": control_rows,
            "rejected_as_dimension_dependent": control_rejected,
        },
        "diagnostics_passed": passed,
        "runtime_seconds": time.perf_counter() - started,
    }
