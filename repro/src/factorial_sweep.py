"""Independent d/k/T/N scaling and iteration first-hit sweep for faithful TPGD."""

from __future__ import annotations

import time

import numpy as np

from factorial_config import FACTORIAL_CONFIG
from faithful_tpgd import (
    empirical_gradients,
    initialize,
    regularized_gradients,
    simulate_paper_model,
)


def _error(B: np.ndarray, W: np.ndarray, truth: np.ndarray) -> float:
    return float(np.mean(np.sum((B @ W - truth) ** 2, axis=0)))


def _independent_error(B: np.ndarray, W: np.ndarray, truth: np.ndarray) -> float:
    total = 0.0
    for task in range(truth.shape[1]):
        residual = B @ W[:, task] - truth[:, task]
        total += float(residual @ residual)
    return total / truth.shape[1]


def _rip_delta(X: np.ndarray) -> float:
    """Exact worst-task delta in Definition 3.1 for the realized designs."""
    sample_count = X.shape[1]
    covariance = np.einsum("tnd,tne->tde", X, X, optimize=True) / sample_count
    eigenvalues = np.linalg.eigvalsh(covariance)
    return float(np.max(np.abs(eigenvalues - 1.0)))


def _run_one(dimensions: dict[str, int], seed: int, permuted_control: bool = False) -> dict[str, object]:
    config = FACTORIAL_CONFIG
    rng = np.random.default_rng(seed)
    X, y, B_star, W_star = simulate_paper_model(
        T=dimensions["T"],
        N=dimensions["N"],
        d=dimensions["d"],
        k=dimensions["k"],
        sigma=config["sigma"],
        rng=rng,
    )
    truth = B_star @ W_star
    if permuted_control:
        y = np.roll(y, shift=1, axis=0)
    singular_values = np.linalg.svd(truth, compute_uv=False)
    sigma_1 = float(singular_values[0])
    sigma_k = float(singular_values[dimensions["k"] - 1])
    condition_number = sigma_1 / sigma_k
    eta1 = config["phase1_step_multiplier"] / sigma_1
    eta2 = config["phase2_step_multiplier"] / sigma_1
    B, W = initialize(
        dimensions["d"],
        dimensions["k"],
        dimensions["T"],
        config["alpha_tilde"],
        rng,
    )
    initial_error = _error(B, W, truth)
    relative_target = initial_error * config["relative_first_hit_fraction"]
    relative_hit = None
    absolute_hit = None
    checkpoint_errors = {"0": initial_error}

    for iteration in range(config["K1"]):
        if iteration < config["K1"] // 2:
            grad_B, grad_W = empirical_gradients(X, y, B, W)
            step_size = eta1
        else:
            grad_B, grad_W = regularized_gradients(X, y, B, W)
            step_size = eta2
        B -= step_size * grad_B
        W -= step_size * grad_W
        completed = iteration + 1
        if completed % config["checkpoint_interval"] == 0:
            current = _error(B, W, truth)
            checkpoint_errors[str(completed)] = current
            if relative_hit is None and current <= relative_target:
                relative_hit = completed
            if absolute_hit is None and current <= config["absolute_first_hit_threshold"]:
                absolute_hit = completed

    final_error = _error(B, W, truth)
    independent = _independent_error(B, W, truth)
    theorem_scale = (
        config["sigma"] ** 2
        * dimensions["d"]
        * dimensions["k"]
        / (dimensions["N"] * dimensions["T"])
    )
    theorem_sample_expression = (
        config["sigma"] ** 2
        * (dimensions["d"] + dimensions["T"])
        * dimensions["k"]
        * condition_number**4
        / sigma_k**2
    )
    return {
        **dimensions,
        "seed": seed,
        "permuted_task_label_control": permuted_control,
        "sigma_1_M_star": sigma_1,
        "sigma_k_M_star": sigma_k,
        "condition_number": condition_number,
        "eta1": eta1,
        "eta2": eta2,
        "realized_worst_task_rip_delta": _rip_delta(X),
        "initial_parameter_error": initial_error,
        "final_parameter_error": final_error,
        "improvement_ratio": final_error / initial_error,
        "relative_first_hit_iteration": relative_hit,
        "absolute_first_hit_iteration": absolute_hit,
        "checkpoint_errors": checkpoint_errors,
        "independent_final_error": independent,
        "checker_absolute_difference": abs(final_error - independent),
        "sigma2_dk_over_NT": theorem_scale,
        "error_over_sigma2_dk_over_NT": final_error / theorem_scale,
        "theorem_sample_expression_without_hidden_constant": theorem_sample_expression,
        "N_over_theorem_sample_expression": dimensions["N"] / theorem_sample_expression,
    }


def _configurations() -> list[tuple[str, int, dict[str, int]]]:
    base = dict(FACTORIAL_CONFIG["base"])
    configurations = []
    for factor, values in FACTORIAL_CONFIG["values"].items():
        for value in values:
            current = dict(base)
            current[factor] = value
            configurations.append((factor, value, current))
    return configurations


def _slope(values: list[int], errors: list[float]) -> float:
    return float(np.polyfit(np.log(np.asarray(values)), np.log(np.asarray(errors)), 1)[0])


def _bootstrap_slope_interval(
    rows: list[dict[str, object]],
    factor: str,
    values: list[int],
    seed: int,
    repeats: int = 2000,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    grouped = {
        value: np.asarray(
            [
                float(row["final_parameter_error"])
                for row in rows
                if row["factor"] == factor and int(row["factor_value"]) == value
            ]
        )
        for value in values
    }
    boot = []
    for _ in range(repeats):
        means = [
            float(np.mean(rng.choice(grouped[value], size=len(grouped[value]), replace=True)))
            for value in values
        ]
        boot.append(_slope(values, means))
    return float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))


def run_factorial_sweep() -> dict[str, object]:
    started = time.perf_counter()
    rows = []
    for factor, value, dimensions in _configurations():
        for seed in FACTORIAL_CONFIG["seeds"]:
            row = _run_one(dimensions, seed)
            row["factor"] = factor
            row["factor_value"] = value
            rows.append(row)

    summaries = {}
    expected_slopes = {"d": 1.0, "k": 1.0, "T": -1.0, "N": -1.0}
    slope_tolerances = {
        "d": [-0.25, 2.25],
        "k": [-0.25, 2.25],
        "T": [-2.25, 0.25],
        "N": [-2.25, 0.25],
    }
    diagnostics_passed = True
    for factor, values in FACTORIAL_CONFIG["values"].items():
        means = []
        standard_errors = []
        medians_first_hit = []
        for value in values:
            subset = [
                row
                for row in rows
                if row["factor"] == factor and int(row["factor_value"]) == value
            ]
            errors = np.asarray([float(row["final_parameter_error"]) for row in subset])
            hits = [
                int(row["relative_first_hit_iteration"])
                for row in subset
                if row["relative_first_hit_iteration"] is not None
            ]
            means.append(float(np.mean(errors)))
            standard_errors.append(float(np.std(errors, ddof=1) / np.sqrt(len(errors))))
            medians_first_hit.append(float(np.median(hits)) if hits else None)
        slope = _slope(values, means)
        interval = _bootstrap_slope_interval(rows, factor, values, seed=5100 + len(summaries))
        lo, hi = slope_tolerances[factor]
        slope_diagnostic = lo <= slope <= hi
        all_hit = all(hit is not None for hit in medians_first_hit)
        diagnostics_passed = diagnostics_passed and slope_diagnostic and all_hit
        summaries[factor] = {
            "values": values,
            "mean_final_errors": means,
            "standard_errors": standard_errors,
            "log_log_slope": slope,
            "bootstrap_95pct_slope_interval": interval,
            "paper_rate_expected_slope": expected_slopes[factor],
            "broad_predeclared_diagnostic_interval": [lo, hi],
            "slope_diagnostic_passed": slope_diagnostic,
            "median_relative_first_hit_iterations": medians_first_hit,
            "all_seed_groups_hit_relative_target": all_hit,
        }

    control = _run_one(dict(FACTORIAL_CONFIG["base"]), seed=4199, permuted_control=True)
    unpermuted_base_errors = [
        float(row["final_parameter_error"])
        for row in rows
        if row["factor"] == "N" and int(row["factor_value"]) == FACTORIAL_CONFIG["base"]["N"]
    ]
    control_threshold = 10.0 * float(np.mean(unpermuted_base_errors))
    control_failed_as_intended = float(control["final_parameter_error"]) > control_threshold
    max_checker_difference = max(float(row["checker_absolute_difference"]) for row in rows)
    all_finite = all(np.isfinite(float(row["final_parameter_error"])) for row in rows)
    all_improved = all(float(row["improvement_ratio"]) < 0.2 for row in rows)
    diagnostics_passed = (
        diagnostics_passed
        and all_finite
        and all_improved
        and max_checker_difference < 1e-10
        and control_failed_as_intended
    )
    rip_deltas = [float(row["realized_worst_task_rip_delta"]) for row in rows]
    return {
        "artifact_status": "SCOPED_CORROBORATION",
        "claims": ["C3", "C4", "C5"],
        "configuration": FACTORIAL_CONFIG,
        "rows": rows,
        "summaries": summaries,
        "assumption_audit": {
            "definition": "max_t ||X_t^T X_t/N-I||_op",
            "minimum_realized_delta": min(rip_deltas),
            "maximum_realized_delta": max(rip_deltas),
            "all_realized_delta_below_one": max(rip_deltas) < 1.0,
            "warning": "A statistical trend is not theorem evidence when its realized design misses the theorem's delta requirement.",
        },
        "independent_checker_max_absolute_difference": max_checker_difference,
        "negative_control": {
            "name": "cyclically permuted task labels",
            "final_parameter_error": control["final_parameter_error"],
            "rejection_threshold": control_threshold,
            "failed_as_intended": control_failed_as_intended,
        },
        "all_runs_improved_at_least_five_fold": all_improved,
        "diagnostics_passed": diagnostics_passed,
        "runtime_seconds": time.perf_counter() - started,
        "verdict": "BLOCKED",
        "verdict_reason": "Finite scaling experiments cannot verify the universally quantified theorem, and the realized RIP constants are audited separately.",
    }
