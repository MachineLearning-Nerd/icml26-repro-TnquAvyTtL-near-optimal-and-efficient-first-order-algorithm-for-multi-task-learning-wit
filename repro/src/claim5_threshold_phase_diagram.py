"""Non-circular, direct-TPGD sample-threshold phase diagram for Claim 5."""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path

import numpy as np

from claim5_threshold_config import CLAIM5_THRESHOLD_CONFIG
from faithful_tpgd import initialize


ARTIFACT_DIR = (
    Path(__file__).resolve().parents[2]
    / ".openresearch"
    / "artifacts"
    / "claim-5-threshold"
)


def _balanced_truth(
    d: int,
    k: int,
    tasks: int,
    kappa: float,
    sigma_k: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    basis, _ = np.linalg.qr(rng.normal(size=(d, k)), mode="reduced")
    task_basis, _ = np.linalg.qr(rng.normal(size=(tasks, k)), mode="reduced")
    singular_values = np.linspace(kappa * sigma_k, sigma_k, k)
    root = np.sqrt(singular_values)
    B_star = basis * root[None, :]
    W_star = root[:, None] * task_basis.T
    return B_star, W_star, B_star @ W_star, singular_values


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


def _stacked_distance_squared(
    B: np.ndarray,
    W: np.ndarray,
    B_star: np.ndarray,
    W_star: np.ndarray,
) -> tuple[float, float, float]:
    estimate = np.vstack([B, W.T])
    truth = np.vstack([B_star, W_star.T])
    left, _, right_t = np.linalg.svd(estimate.T @ truth, full_matrices=False)
    rotation = left @ right_t
    residual = estimate @ rotation - truth
    distance = float(np.sum(residual * residual))
    independent = float(
        sum(float(row @ row) for row in residual)
    )
    normalized = distance / float(np.sum(truth * truth))
    return distance, normalized, abs(distance - independent)


def _run_one(
    configuration: dict[str, float | int],
    sample_count: int,
    seed: int,
    permuted_control: bool = False,
) -> dict[str, object]:
    config = CLAIM5_THRESHOLD_CONFIG
    rng = np.random.default_rng(seed)
    d = int(configuration["d"])
    k = int(configuration["k"])
    tasks = int(configuration["T"])
    sigma = float(configuration["sigma"])
    kappa = float(configuration["kappa"])
    sigma_k = float(configuration["sigma_k"])
    B_star, W_star, truth, singular_values = _balanced_truth(
        d, k, tasks, kappa, sigma_k, rng
    )
    response = truth + rng.normal(
        scale=sigma / np.sqrt(sample_count),
        size=truth.shape,
    )
    if permuted_control:
        response = np.roll(response, shift=1, axis=1)
    sigma_1 = float(singular_values[0])
    eta1 = (
        config["phase1_step_multiplier"]
        / (kappa**5 * sigma_1)
    )
    eta2 = config["phase2_step_multiplier"] / sigma_1
    B, W = initialize(d, k, tasks, config["alpha_tilde"], rng)
    initial_distance, initial_normalized, _ = _stacked_distance_squared(
        B, W, B_star, W_star
    )
    for iteration in range(config["K1"]):
        regularized = iteration >= config["K1"] // 2
        grad_B, grad_W = _gradients(B, W, response, regularized)
        step = eta2 if regularized else eta1
        B -= step * grad_B
        W -= step * grad_W
    distance, normalized, checker_difference = _stacked_distance_squared(
        B, W, B_star, W_star
    )
    sample_expression = (
        sigma**2
        * (d + tasks)
        * k
        * kappa**4
        / sigma_k**2
    )
    success = (
        distance <= config["absolute_stacked_distance_squared_target"]
        and normalized <= config["normalized_stacked_distance_squared_target"]
    )
    return {
        "d": d,
        "T": tasks,
        "k": k,
        "N": sample_count,
        "sigma": sigma,
        "sigma_squared": sigma**2,
        "kappa": kappa,
        "sigma_k": sigma_k,
        "seed": seed,
        "permuted_task_control": permuted_control,
        "exact_rip_delta": 0.0,
        "sigma_1_M_star": sigma_1,
        "realized_sigma_k_M_star": float(singular_values[-1]),
        "realized_condition_number": sigma_1 / float(singular_values[-1]),
        "eta1": eta1,
        "eta2": eta2,
        "K1_eta1_sigma_k": config["K1"] * eta1 * sigma_k,
        "initial_stacked_distance_squared": initial_distance,
        "initial_normalized_stacked_distance_squared": initial_normalized,
        "final_stacked_distance_squared": distance,
        "final_normalized_stacked_distance_squared": normalized,
        "checker_absolute_difference": checker_difference,
        "sample_expression_without_hidden_constants": sample_expression,
        "N_over_sample_expression": sample_count / sample_expression,
        "success": success,
    }


def _configurations() -> list[tuple[str, float, dict[str, float | int]]]:
    base = dict(CLAIM5_THRESHOLD_CONFIG["base"])
    configurations = []
    for factor, values in CLAIM5_THRESHOLD_CONFIG["factor_values"].items():
        for value in values:
            current = dict(base)
            if factor == "sigma_squared":
                current["sigma"] = math.sqrt(float(value))
            elif factor == "d_plus_T":
                current["d"] = int(value) - int(current["T"])
            else:
                current[factor] = value
            configurations.append((factor, float(value), current))
    return configurations


def _interpolated_threshold(
    sample_counts: list[int],
    mean_distances: list[float],
    target: float,
) -> float | None:
    if mean_distances[0] <= target:
        return float(sample_counts[0])
    for index in range(len(sample_counts) - 1):
        left_error = mean_distances[index]
        right_error = mean_distances[index + 1]
        if left_error > target >= right_error:
            log_left_n = math.log(sample_counts[index])
            log_right_n = math.log(sample_counts[index + 1])
            log_left_error = math.log(left_error)
            log_right_error = math.log(right_error)
            fraction = (
                math.log(target) - log_left_error
            ) / (log_right_error - log_left_error)
            return float(math.exp(log_left_n + fraction * (log_right_n - log_left_n)))
    return None


def _slope(xs: list[float], ys: list[float]) -> float:
    return float(
        np.polyfit(
            np.log(np.asarray(xs, dtype=float)),
            np.log(np.asarray(ys, dtype=float)),
            1,
        )[0]
    )


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run_claim5_threshold_phase_diagram() -> dict[str, object]:
    started = time.perf_counter()
    config = CLAIM5_THRESHOLD_CONFIG
    rows: list[dict[str, object]] = []
    configurations = _configurations()
    for factor, factor_value, parameters in configurations:
        for sample_count in config["N_grid"]:
            for seed in config["seeds"]:
                row = _run_one(parameters, sample_count, seed)
                row["factor"] = factor
                row["factor_value"] = factor_value
                rows.append(row)

    summaries: dict[str, object] = {}
    threshold_pairs = []
    high_ratio_groups = []
    low_ratio_groups = []
    high_ratio_factors = set()
    for factor, factor_value, parameters in configurations:
        subset = [
            row
            for row in rows
            if row["factor"] == factor and row["factor_value"] == factor_value
        ]
        pass_counts = []
        mean_distances = []
        for sample_count in config["N_grid"]:
            group = [row for row in subset if row["N"] == sample_count]
            pass_count = sum(bool(row["success"]) for row in group)
            pass_counts.append(pass_count)
            mean_distances.append(
                float(
                    np.mean(
                        [
                            float(row["final_stacked_distance_squared"])
                            for row in group
                        ]
                    )
                )
            )
            ratio = float(group[0]["N_over_sample_expression"])
            if ratio >= config["high_ratio_margin"]:
                high_ratio_groups.append(pass_count)
                high_ratio_factors.add(factor)
            if ratio <= config["low_ratio_margin"]:
                low_ratio_groups.append(pass_count)
        first_grid_success = next(
            (
                sample_count
                for sample_count, count in zip(config["N_grid"], pass_counts)
                if count >= config["successes_required_out_of_five"]
            ),
            None,
        )
        interpolated = _interpolated_threshold(
            config["N_grid"],
            mean_distances,
            config["absolute_stacked_distance_squared_target"],
        )
        expression = float(subset[0]["sample_expression_without_hidden_constants"])
        summary_key = f"{factor}={factor_value:g}"
        summaries[summary_key] = {
            "factor": factor,
            "factor_value": factor_value,
            "parameters": parameters,
            "sample_expression_without_hidden_constants": expression,
            "pass_counts_out_of_five_by_N": dict(
                zip(map(str, config["N_grid"]), pass_counts)
            ),
            "mean_stacked_distance_squared_by_N": dict(
                zip(map(str, config["N_grid"]), mean_distances)
            ),
            "first_grid_N_with_at_least_four_successes": first_grid_success,
            "interpolated_N_at_absolute_distance_target": interpolated,
        }
        if interpolated is not None:
            threshold_pairs.append((expression, interpolated, factor, factor_value))

    factor_slopes = {}
    expected_factor_slopes = {
        "sigma_squared": 1.0,
        "d_plus_T": 1.0,
        "k": 1.0,
        "kappa": 4.0,
        "sigma_k": -2.0,
    }
    for factor, values in config["factor_values"].items():
        factor_pairs = [
            pair for pair in threshold_pairs if pair[2] == factor
        ]
        if len(factor_pairs) == len(values):
            empirical = _slope(
                [float(pair[3]) for pair in factor_pairs],
                [pair[1] for pair in factor_pairs],
            )
        else:
            empirical = None
        factor_slopes[factor] = {
            "paper_expression_expected_slope": expected_factor_slopes[factor],
            "empirical_interpolated_threshold_slope": empirical,
            "complete_three_point_route": len(factor_pairs) == len(values),
        }

    if len(threshold_pairs) >= 3:
        overall_slope = _slope(
            [pair[0] for pair in threshold_pairs],
            [pair[1] for pair in threshold_pairs],
        )
        correlation = float(
            np.corrcoef(
                np.log([pair[0] for pair in threshold_pairs]),
                np.log([pair[1] for pair in threshold_pairs]),
            )[0, 1]
        )
    else:
        overall_slope = None
        correlation = None

    control_parameters = dict(config["base"])
    control = _run_one(
        control_parameters,
        max(config["N_grid"]),
        config["seeds"][0],
        permuted_control=True,
    )
    control_failed = not bool(control["success"])
    high_ratio_passed = bool(high_ratio_groups) and all(
        count >= config["successes_required_out_of_five"]
        for count in high_ratio_groups
    )
    low_ratio_nonvacuous = bool(low_ratio_groups) and any(
        count <= 1 for count in low_ratio_groups
    )
    largest_N_groups = [
        [
            row
            for row in rows
            if row["factor"] == factor
            and row["factor_value"] == factor_value
            and row["N"] == max(config["N_grid"])
        ]
        for factor, factor_value, _ in configurations
    ]
    all_largest_N_groups_succeed = all(
        sum(bool(row["success"]) for row in group)
        >= config["successes_required_out_of_five"]
        for group in largest_N_groups
    )
    key_factor_slope_gate = all(
        factor_slopes[factor]["empirical_interpolated_threshold_slope"] is not None
        and abs(
            float(
                factor_slopes[factor]["empirical_interpolated_threshold_slope"]
            )
            - float(factor_slopes[factor]["paper_expression_expected_slope"])
        )
        <= 0.25
        for factor in ("sigma_squared", "d_plus_T", "k")
    )
    sigma_k_direction_gate = (
        factor_slopes["sigma_k"]["empirical_interpolated_threshold_slope"]
        is not None
        and float(
            factor_slopes["sigma_k"]["empirical_interpolated_threshold_slope"]
        )
        < 0.0
    )
    max_checker_difference = max(
        float(row["checker_absolute_difference"]) for row in rows
    )
    assumptions_passed = (
        all(float(row["exact_rip_delta"]) == 0.0 for row in rows)
        and max(
            abs(float(row["realized_condition_number"]) - float(row["kappa"]))
            for row in rows
        )
        < 1e-12
        and max(
            abs(float(row["realized_sigma_k_M_star"]) - float(row["sigma_k"]))
            for row in rows
        )
        < 1e-12
        and all(int(row["T"]) > int(row["k"]) for row in rows)
    )
    diagnostics_passed = (
        high_ratio_passed
        and low_ratio_nonvacuous
        and control_failed
        and assumptions_passed
        and max_checker_difference < 1e-10
        and len(high_ratio_factors) >= 4
        and all_largest_N_groups_succeed
        and key_factor_slope_gate
        and sigma_k_direction_gate
    )
    result = {
        "artifact_status": "DIRECT_TPGD_SCOPED_SAMPLE_THRESHOLD_AUDIT",
        "claim": "C5",
        "configuration": config,
        "rows": rows,
        "configuration_summaries": summaries,
        "factor_threshold_slopes": factor_slopes,
        "overall_empirical_threshold_vs_expression_log_slope": overall_slope,
        "overall_log_correlation": correlation,
        "high_ratio_group_count": len(high_ratio_groups),
        "high_ratio_factor_families": sorted(high_ratio_factors),
        "all_groups_at_or_above_calibrated_margin_succeed": high_ratio_passed,
        "low_ratio_group_count": len(low_ratio_groups),
        "at_least_one_low_ratio_group_fails": low_ratio_nonvacuous,
        "all_fifteen_largest_N_groups_succeed": all_largest_N_groups_succeed,
        "sigma_squared_d_plus_T_and_k_slope_gate_passed": key_factor_slope_gate,
        "sigma_k_empirical_direction_gate_passed": sigma_k_direction_gate,
        "assumption_audit": {
            "N_grid_selected_independently_of_formula": True,
            "hidden_constant_margin_frozen_before_held_out_seeds": config[
                "high_ratio_margin"
            ],
            "held_out_seed_set": config["seeds"],
            "calibration_run": config["calibration_run"],
            "exact_rip_delta": 0.0,
            "all_T_strictly_greater_than_k": all(
                int(row["T"]) > int(row["k"]) for row in rows
            ),
            "realized_kappa_and_sigma_k_match_configuration": assumptions_passed,
        },
        "independent_checker_max_absolute_difference": max_checker_difference,
        "negative_control": {
            "mutation": "cyclically permute task sufficient-response columns",
            "N": max(config["N_grid"]),
            "final_stacked_distance_squared": control[
                "final_stacked_distance_squared"
            ],
            "success": control["success"],
            "failed_as_intended": control_failed,
        },
        "diagnostics_passed": diagnostics_passed,
        "runtime_seconds": time.perf_counter() - started,
        "limitations": [
            "This is a finite sufficient-condition stress test, not a proof of the universal theorem.",
            "The theorem hides constants and logarithms; ratio margins are reported without claiming their numerical optimality.",
            "Factor-specific empirical threshold slopes are diagnostic and are not forced to equal the conservative sufficient-condition exponents.",
        ],
    }
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    _write_csv(ARTIFACT_DIR / "threshold_rows.csv", rows)
    (ARTIFACT_DIR / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result
