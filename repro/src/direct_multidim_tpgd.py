"""Direct multidimensional TPGD checks for Claims 3 and 4.

This uses the paper's two-phase updates under an explicit exact-RIP design.
The sufficient statistic is mathematically identical to running Algorithm 1 on
X_t^T X_t / N = I, which is independently checked by exact_rip_sweep.py.
Unlike the historical proxy, every reported rate and first-hit number comes
from the TPGD iterates themselves.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import numpy as np

from direct_multidim_config import DIRECT_MULTIDIM_CONFIG
from faithful_tpgd import initialize


ARTIFACT_DIR = (
    Path(__file__).resolve().parents[2]
    / ".openresearch"
    / "artifacts"
    / "claims-3-4-direct"
)


def _unit_spectrum_truth(
    d: int,
    k: int,
    tasks: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return balanced factors whose nonzero singular values are exactly one."""
    basis, _ = np.linalg.qr(rng.normal(size=(d, k)), mode="reduced")
    task_basis, _ = np.linalg.qr(rng.normal(size=(tasks, k)), mode="reduced")
    weights = task_basis.T
    return basis, weights, basis @ weights


def _gradients(
    B: np.ndarray,
    W: np.ndarray,
    response: np.ndarray,
    regularized: bool,
) -> tuple[np.ndarray, np.ndarray]:
    residual = B @ W - response
    grad_B = residual @ W.T
    grad_W = B.T @ residual
    if regularized:
        imbalance = B.T @ B - W @ W.T
        grad_B = grad_B + 0.5 * B @ imbalance
        grad_W = grad_W - 0.5 * imbalance @ W
    return grad_B, grad_W


def _mean_parameter_error(B: np.ndarray, W: np.ndarray, truth: np.ndarray) -> float:
    return float(np.mean(np.sum((B @ W - truth) ** 2, axis=0)))


def _independent_parameter_error(
    B: np.ndarray,
    W: np.ndarray,
    truth: np.ndarray,
) -> float:
    total = 0.0
    for task in range(truth.shape[1]):
        residual = B @ W[:, task] - truth[:, task]
        total += float(residual @ residual)
    return total / truth.shape[1]


def _relative_squared_error(
    B: np.ndarray,
    W: np.ndarray,
    truth: np.ndarray,
) -> float:
    return float(
        np.linalg.norm(B @ W - truth, ord="fro") ** 2
        / np.linalg.norm(truth, ord="fro") ** 2
    )


def _run_one(
    dimensions: dict[str, int],
    seed: int,
    route: str,
    permuted_control: bool = False,
) -> dict[str, object]:
    config = DIRECT_MULTIDIM_CONFIG[route]
    rng = np.random.default_rng(seed)
    B_star, W_star, truth = _unit_spectrum_truth(
        dimensions["d"], dimensions["k"], dimensions["T"], rng
    )
    response = truth + rng.normal(
        scale=config["sigma"] / np.sqrt(dimensions["N"]),
        size=truth.shape,
    )
    if permuted_control:
        response = np.roll(response, shift=1, axis=1)

    singular_values = np.linalg.svd(truth, compute_uv=False)
    sigma_1 = float(singular_values[0])
    sigma_k = float(singular_values[dimensions["k"] - 1])
    eta1 = config["phase1_step_multiplier"] / sigma_1
    eta2 = config["phase2_step_multiplier"] / sigma_1
    B, W = initialize(
        dimensions["d"],
        dimensions["k"],
        dimensions["T"],
        config["alpha_tilde"],
        rng,
    )
    initial_error = _mean_parameter_error(B, W, truth)
    initial_relative_error = _relative_squared_error(B, W, truth)
    rate_target = initial_error * DIRECT_MULTIDIM_CONFIG["rate"][
        "relative_first_hit_fraction"
    ]
    iteration_target = DIRECT_MULTIDIM_CONFIG["iteration"][
        "relative_squared_error_target"
    ]
    first_hit = None

    for iteration in range(config["K1"]):
        regularized = iteration >= config["K1"] // 2
        grad_B, grad_W = _gradients(B, W, response, regularized)
        step = eta2 if regularized else eta1
        B -= step * grad_B
        W -= step * grad_W
        if first_hit is None:
            if route == "rate":
                hit = _mean_parameter_error(B, W, truth) <= rate_target
            else:
                hit = _relative_squared_error(B, W, truth) <= iteration_target
            if hit:
                first_hit = iteration + 1

    final_error = _mean_parameter_error(B, W, truth)
    independent_error = _independent_parameter_error(B, W, truth)
    expected_scale = (
        config["sigma"] ** 2
        * dimensions["d"]
        * dimensions["k"]
        / (dimensions["N"] * dimensions["T"])
    )
    sample_expression = (
        config["sigma"] ** 2
        * (dimensions["d"] + dimensions["T"])
        * dimensions["k"]
        / sigma_k**2
    )
    return {
        **dimensions,
        "route": route,
        "seed": seed,
        "permuted_task_control": permuted_control,
        "exact_rip_delta": 0.0,
        "sigma": config["sigma"],
        "sigma_1_M_star": sigma_1,
        "sigma_k_M_star": sigma_k,
        "condition_number": sigma_1 / sigma_k,
        "eta1": eta1,
        "eta2": eta2,
        "initial_parameter_error": initial_error,
        "initial_relative_squared_error": initial_relative_error,
        "final_parameter_error": final_error,
        "final_relative_squared_error": _relative_squared_error(B, W, truth),
        "first_hit_iteration": first_hit,
        "independent_final_error": independent_error,
        "checker_absolute_difference": abs(final_error - independent_error),
        "sigma2_dk_over_NT": expected_scale,
        "error_over_sigma2_dk_over_NT": final_error / expected_scale,
        "sample_expression_without_hidden_constant": sample_expression,
        "N_over_sample_expression": dimensions["N"] / sample_expression,
        "truth_factor_balance_residual": float(
            np.linalg.norm(B_star.T @ B_star - W_star @ W_star.T, ord="fro")
        ),
    }


def _slope(values: list[int], means: list[float]) -> float:
    return float(
        np.polyfit(
            np.log(np.asarray(values, dtype=float)),
            np.log(np.asarray(means, dtype=float)),
            1,
        )[0]
    )


def _bootstrap_slope_interval(
    rows: list[dict[str, object]],
    factor: str,
    values: list[int],
    seed: int,
    repeats: int = 2000,
) -> list[float]:
    rng = np.random.default_rng(seed)
    groups = {
        value: np.asarray(
            [
                float(row["final_parameter_error"])
                for row in rows
                if row["factor"] == factor and row["factor_value"] == value
            ]
        )
        for value in values
    }
    slopes = []
    for _ in range(repeats):
        means = [
            float(
                np.mean(
                    rng.choice(groups[value], size=len(groups[value]), replace=True)
                )
            )
            for value in values
        ]
        slopes.append(_slope(values, means))
    return [
        float(np.quantile(slopes, 0.025)),
        float(np.quantile(slopes, 0.975)),
    ]


def _factor_rows(route: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    config = DIRECT_MULTIDIM_CONFIG
    for factor, values in config["factor_values"].items():
        for value in values:
            dimensions = dict(config["base"])
            dimensions[factor] = value
            for seed in config["seeds"]:
                row = _run_one(dimensions, seed, route)
                row["factor"] = factor
                row["factor_value"] = value
                rows.append(row)
    return rows


def _rate_summary(rows: list[dict[str, object]]) -> tuple[dict[str, object], bool]:
    expected = {"d": 1.0, "k": 1.0, "T": -1.0, "N": -1.0}
    tolerance = DIRECT_MULTIDIM_CONFIG["rate"]["maximum_slope_deviation"]
    summaries: dict[str, object] = {}
    passed = True
    for index, (factor, values) in enumerate(
        DIRECT_MULTIDIM_CONFIG["factor_values"].items()
    ):
        means = []
        standard_errors = []
        for value in values:
            errors = np.asarray(
                [
                    float(row["final_parameter_error"])
                    for row in rows
                    if row["factor"] == factor and row["factor_value"] == value
                ]
            )
            means.append(float(np.mean(errors)))
            standard_errors.append(
                float(np.std(errors, ddof=1) / np.sqrt(len(errors)))
            )
        slope = _slope(values, means)
        interval = _bootstrap_slope_interval(rows, factor, values, 8400 + index)
        target = expected[factor]
        slope_passed = (
            abs(slope - target) <= tolerance
            and interval[0] <= target + tolerance
            and interval[1] >= target - tolerance
        )
        summaries[factor] = {
            "values": values,
            "mean_final_errors": means,
            "standard_errors": standard_errors,
            "log_log_slope": slope,
            "bootstrap_95pct_slope_interval": interval,
            "paper_expected_slope": target,
            "maximum_allowed_deviation": tolerance,
            "strict_slope_gate_passed": slope_passed,
        }
        passed = passed and slope_passed
    return summaries, passed


def _iteration_summary(
    rows: list[dict[str, object]],
) -> tuple[dict[str, object], bool]:
    config = DIRECT_MULTIDIM_CONFIG["iteration"]
    summaries: dict[str, object] = {}
    passed = True
    for factor, values in DIRECT_MULTIDIM_CONFIG["factor_values"].items():
        medians = []
        first_hit_counts = []
        for value in values:
            subset = [
                row
                for row in rows
                if row["factor"] == factor and row["factor_value"] == value
            ]
            hits = [
                int(row["first_hit_iteration"])
                for row in subset
                if row["first_hit_iteration"] is not None
            ]
            first_hit_counts.append(len(hits))
            medians.append(float(np.median(hits)) if len(hits) == len(subset) else None)
        if any(value is None for value in medians):
            slope = None
            ratio = None
            factor_passed = False
        else:
            finite_medians = [float(value) for value in medians if value is not None]
            slope = _slope(values, finite_medians)
            ratio = max(finite_medians) / min(finite_medians)
            factor_passed = (
                abs(slope) <= config["maximum_absolute_loglog_slope"]
                and ratio <= config["maximum_median_ratio"]
            )
        summaries[factor] = {
            "values": values,
            "median_first_hit_iterations": medians,
            "successful_seeds_out_of_six": first_hit_counts,
            "log_log_median_iteration_slope": slope,
            "maximum_to_minimum_median_ratio": ratio,
            "factor_gate_passed": factor_passed,
        }
        passed = passed and factor_passed
    return summaries, passed


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_direct_multidim_tpgd() -> dict[str, object]:
    started = time.perf_counter()
    rate_rows = _factor_rows("rate")
    iteration_rows = _factor_rows("iteration")
    rate_summaries, rate_passed = _rate_summary(rate_rows)
    iteration_summaries, iteration_passed = _iteration_summary(iteration_rows)

    base = dict(DIRECT_MULTIDIM_CONFIG["base"])
    control = _run_one(base, DIRECT_MULTIDIM_CONFIG["seeds"][0], "rate", True)
    clean_base = [
        float(row["final_parameter_error"])
        for row in rate_rows
        if row["factor"] == "N" and row["factor_value"] == base["N"]
    ]
    control_threshold = 10.0 * float(np.mean(clean_base))
    control_failed = float(control["final_parameter_error"]) > control_threshold
    all_rows = rate_rows + iteration_rows
    max_checker_difference = max(
        float(row["checker_absolute_difference"]) for row in all_rows
    )
    max_balance_residual = max(
        float(row["truth_factor_balance_residual"]) for row in all_rows
    )
    all_assumptions_passed = (
        all(float(row["exact_rip_delta"]) == 0.0 for row in all_rows)
        and max(abs(float(row["condition_number"]) - 1.0) for row in all_rows)
        < 1e-12
        and max_balance_residual < 1e-12
        and min(
            float(row["N_over_sample_expression"])
            for row in rate_rows
        )
        >= 1.0
    )
    diagnostics_passed = (
        rate_passed
        and iteration_passed
        and control_failed
        and max_checker_difference < 1e-10
        and all_assumptions_passed
    )
    result = {
        "artifact_status": "DIRECT_TPGD_SCOPED_CORROBORATION",
        "claims": ["C3", "C4"],
        "configuration": DIRECT_MULTIDIM_CONFIG,
        "rate_rows": rate_rows,
        "rate_summaries": rate_summaries,
        "rate_strict_gate_passed": rate_passed,
        "iteration_rows": iteration_rows,
        "iteration_summaries": iteration_summaries,
        "iteration_all_dimensions_gate_passed": iteration_passed,
        "assumption_audit": {
            "exact_rip_delta": 0.0,
            "maximum_condition_number_error": max(
                abs(float(row["condition_number"]) - 1.0) for row in all_rows
            ),
            "maximum_truth_balance_residual": max_balance_residual,
            "minimum_N_over_sample_expression_without_hidden_constant": min(
                float(row["N_over_sample_expression"]) for row in rate_rows
            ),
            "all_machine_checkable_assumptions_passed": all_assumptions_passed,
            "scope": "Gaussian-noise exact-RIP special case with T>k in every cell",
        },
        "independent_checker_max_absolute_difference": max_checker_difference,
        "negative_control": {
            "mutation": "cyclically permute task sufficient-response columns",
            "final_parameter_error": control["final_parameter_error"],
            "rejection_threshold": control_threshold,
            "failed_as_intended": control_failed,
        },
        "diagnostics_passed": diagnostics_passed,
        "runtime_seconds": time.perf_counter() - started,
        "limitations": [
            "Finite experiments corroborate rather than prove universal high-probability theorems.",
            "The rate sweep uses d/T >= 2 and base d/T=32 to isolate the leading dk/(NT) term.",
            "Hidden constants in the theorem's alpha initialization bound remain unavailable.",
        ],
    }
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    _write_csv(ARTIFACT_DIR / "rate_rows.csv", rate_rows)
    _write_csv(ARTIFACT_DIR / "iteration_rows.csv", iteration_rows)
    (ARTIFACT_DIR / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result
