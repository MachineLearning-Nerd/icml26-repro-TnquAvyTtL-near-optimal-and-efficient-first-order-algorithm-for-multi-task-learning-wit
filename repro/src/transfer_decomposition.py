"""Direct Algorithm 2 experiment for Theorem 5.4's two risk components."""

from __future__ import annotations

import time

import numpy as np

from exact_rip_sweep import (
    _balanced_truth,
    _exact_rip_gradients,
    _regularized_exact_rip_gradients,
)
from faithful_tpgd import initialize
from transfer_config import TRANSFER_CONFIG


def _learn_representation(sample_count, seed):
    config = TRANSFER_CONFIG
    rng = np.random.default_rng(seed)
    B_star, W_star, truth = _balanced_truth(
        config["d"], config["k"], config["T"], rng
    )
    sufficient = truth + rng.normal(
        scale=config["sigma"] / np.sqrt(sample_count), size=truth.shape
    )
    singular_values = np.linalg.svd(truth, compute_uv=False)
    sigma_1 = float(singular_values[0])
    B, W = initialize(
        config["d"], config["k"], config["T"], config["alpha_tilde"], rng
    )
    eta1 = config["phase1_step_multiplier"] / sigma_1
    eta2 = config["phase2_step_multiplier"] / sigma_1
    for iteration in range(config["K1"]):
        if iteration < config["K1"] // 2:
            grad_B, grad_W = _exact_rip_gradients(B, W, sufficient)
            step = eta1
        else:
            grad_B, grad_W = _regularized_exact_rip_gradients(B, W, sufficient)
            step = eta2
        B -= step * grad_B
        W -= step * grad_W
    return B, B_star, W_star, singular_values, rng


def _algorithm2(B_hat, theta, sigma, K2, eta0, h, rng):
    if K2 - h <= 1:
        raise ValueError("K2-h must exceed one")
    decay_length = int(np.floor((K2 - h) / np.log(K2 - h)))
    if decay_length < 1:
        raise ValueError("Algorithm 2 decay length must be positive")
    weight = np.zeros(B_hat.shape[1])
    step = eta0
    step_halvings = 0
    for tau in range(K2 - 1):
        one_based = tau + 1
        if one_based > h and (one_based - h) % decay_length == 0:
            step /= 2.0
            step_halvings += 1
        x = rng.normal(size=B_hat.shape[0])
        y = float(x @ theta + rng.normal(scale=sigma))
        residual = float(x @ (B_hat @ weight) - y)
        weight -= step * residual * (B_hat.T @ x)
    return weight, decay_length, step_halvings


def _risk_decomposition(B_hat, theta, weight):
    q, _ = np.linalg.qr(B_hat, mode="reduced")
    projection = q @ (q.T @ theta)
    optimal_weight = np.linalg.lstsq(B_hat, theta, rcond=None)[0]
    representation = 0.5 * float(np.linalg.norm(projection - theta) ** 2)
    optimization = 0.5 * float(np.linalg.norm(B_hat @ (weight - optimal_weight)) ** 2)
    total = 0.5 * float(np.linalg.norm(B_hat @ weight - theta) ** 2)
    return {
        "total_excess_risk": total,
        "representation_approximation_component": representation,
        "task_optimization_component": optimization,
        "decomposition_absolute_error": abs(total - representation - optimization),
        "optimal_weight": optimal_weight,
        "projection": projection,
    }


def _run_one(upstream_N, K2, seed):
    config = TRANSFER_CONFIG
    B_hat, B_star, W_star, singular_values, upstream_rng = _learn_representation(
        upstream_N, seed
    )
    target_rng = np.random.default_rng(seed + 100_000 + 17 * K2 + upstream_N)
    target_weight = target_rng.normal(size=config["k"])
    target_weight /= np.linalg.norm(target_weight)
    theta = B_star @ target_weight
    gram = B_hat.T @ B_hat
    trace = float(np.trace(gram))
    minimum_eigenvalue = float(np.min(np.linalg.eigvalsh(gram)))
    alpha = 3.0
    eta0 = config["eta0_fraction_of_alpha_trace_bound"] / (alpha * trace)
    required_K2_without_hidden_constant = max(
        alpha / (config["sigma"] ** 2 * eta0),
        1.0 / (2.0 * eta0 * minimum_eigenvalue),
    )
    weight, decay_length, halvings = _algorithm2(
        B_hat,
        theta,
        config["sigma"],
        K2,
        eta0,
        config["target_h"],
        target_rng,
    )
    decomposition = _risk_decomposition(B_hat, theta, weight)
    sigma_k = float(singular_values[config["k"] - 1])
    trace_sigma = float(np.sum(singular_values[: config["k"]]))
    # H=I, B*=orthonormal: beta1=beta2=1 and the bracket in Theorem 5.4 is 4.
    representation_bound_term = (
        config["sigma"] ** 2
        * np.linalg.norm(target_weight) ** 2
        * 4.0
        * trace_sigma
        * config["d"]
        / (sigma_k**2 * upstream_N)
    )
    optimization_bound_term = config["sigma"] ** 2 * config["k"] / K2
    return {
        "upstream_N": upstream_N,
        "K2": K2,
        "seed": seed,
        "h": config["target_h"],
        "eta0": eta0,
        "eta0_alpha_trace": eta0 * alpha * trace,
        "algorithm2_decay_length": decay_length,
        "algorithm2_step_halvings": halvings,
        "required_K2_expression_without_hidden_constant": required_K2_without_hidden_constant,
        "K2_meets_unit_constant_expression": K2 >= required_K2_without_hidden_constant,
        "total_excess_risk": decomposition["total_excess_risk"],
        "representation_approximation_component": decomposition[
            "representation_approximation_component"
        ],
        "task_optimization_component": decomposition["task_optimization_component"],
        "decomposition_absolute_error": decomposition["decomposition_absolute_error"],
        "theorem_representation_term_without_hidden_constant": representation_bound_term,
        "theorem_optimization_term_without_hidden_constant": optimization_bound_term,
        "total_over_sum_of_printed_terms": decomposition["total_excess_risk"]
        / (representation_bound_term + optimization_bound_term),
    }


def _slope(values, means):
    return float(np.polyfit(np.log(np.asarray(values)), np.log(np.asarray(means)), 1)[0])


def _bootstrap_interval(rows, field, selector_field, selector_value, values, seed):
    rng = np.random.default_rng(seed)
    grouped = {
        value: np.asarray(
            [
                row[field]
                for row in rows
                if row[selector_field] == selector_value
                and row["upstream_N" if selector_field == "K2" else "K2"] == value
            ]
        )
        for value in values
    }
    slopes = []
    for _ in range(2000):
        means = [
            float(np.mean(rng.choice(grouped[value], len(grouped[value]), replace=True)))
            for value in values
        ]
        slopes.append(_slope(values, means))
    return [float(np.quantile(slopes, 0.025)), float(np.quantile(slopes, 0.975))]


def run_transfer_decomposition():
    started = time.perf_counter()
    config = TRANSFER_CONFIG
    rows = []
    for upstream_N in config["upstream_N_values"]:
        for K2 in config["K2_values"]:
            for seed in config["seeds"]:
                rows.append(_run_one(upstream_N, K2, seed))

    # Representation scaling uses the longest target run; optimization scaling
    # uses the largest upstream N, avoiding cross-factor mixing.
    representation_means = []
    for upstream_N in config["upstream_N_values"]:
        subset = [
            row
            for row in rows
            if row["upstream_N"] == upstream_N and row["K2"] == max(config["K2_values"])
        ]
        representation_means.append(
            float(np.mean([row["representation_approximation_component"] for row in subset]))
        )
    optimization_means = []
    for K2 in config["K2_values"]:
        subset = [
            row
            for row in rows
            if row["K2"] == K2 and row["upstream_N"] == max(config["upstream_N_values"])
        ]
        optimization_means.append(
            float(np.mean([row["task_optimization_component"] for row in subset]))
        )
    representation_slope = _slope(config["upstream_N_values"], representation_means)
    optimization_slope = _slope(config["K2_values"], optimization_means)
    representation_interval = _bootstrap_interval(
        rows,
        "representation_approximation_component",
        "K2",
        max(config["K2_values"]),
        config["upstream_N_values"],
        9101,
    )
    optimization_interval = _bootstrap_interval(
        rows,
        "task_optimization_component",
        "upstream_N",
        max(config["upstream_N_values"]),
        config["K2_values"],
        9102,
    )

    # Invalid decomposition control: using zero rather than the orthogonal
    # projection as the anchor leaves a nonzero cross term.
    control_rng = np.random.default_rng(8999)
    B_hat, B_star, _, _, _ = _learn_representation(400, 8999)
    target = B_star @ (np.ones(config["k"]) / np.sqrt(config["k"]))
    arbitrary_weight = control_rng.normal(size=config["k"])
    direct = 0.5 * np.linalg.norm(B_hat @ arbitrary_weight - target) ** 2
    invalid_sum = (
        0.5 * np.linalg.norm(target) ** 2
        + 0.5 * np.linalg.norm(B_hat @ arbitrary_weight) ** 2
    )
    control_gap = float(abs(direct - invalid_sum))
    control_failed_as_intended = control_gap > 1e-4

    max_identity_error = max(row["decomposition_absolute_error"] for row in rows)
    moment_certificate = {
        "H": "I",
        "alpha": 3.0,
        "identity": "E[xx^T M xx^T]=2M+tr(M)I for x~N(0,I)",
        "psd_bound": "2M+tr(M)I <= 3 tr(M)I for every PSD M",
    }
    all_finite = all(np.isfinite(row["total_excess_risk"]) for row in rows)
    diagnostics = (
        all_finite
        and max_identity_error < 1e-10
        and -2.0 <= representation_slope <= 0.25
        and -2.0 <= optimization_slope <= 0.25
        and control_failed_as_intended
    )
    return {
        "artifact_status": "ASSUMPTION_SATISFYING_SCOPED_CORROBORATION",
        "claim": "C6",
        "configuration": config,
        "rows": rows,
        "representation_scaling": {
            "upstream_N_values": config["upstream_N_values"],
            "mean_components_at_K2_max": representation_means,
            "log_log_slope": representation_slope,
            "bootstrap_95pct_slope_interval": representation_interval,
        },
        "optimization_scaling": {
            "K2_values": config["K2_values"],
            "mean_components_at_upstream_N_max": optimization_means,
            "log_log_slope": optimization_slope,
            "bootstrap_95pct_slope_interval": optimization_interval,
        },
        "moment_assumption_certificate": moment_certificate,
        "maximum_exact_decomposition_error": max_identity_error,
        "negative_control": {
            "name": "use zero instead of orthogonal projection anchor",
            "identity_gap": control_gap,
            "rejection_threshold": 1e-4,
            "failed_as_intended": control_failed_as_intended,
        },
        "algorithm_source_ambiguity": {
            "h_not_specified_by_theorem": True,
            "selected_h": config["target_h"],
            "off_by_one": "Algorithm 2 halves before the K2'-th sampled update, while prose says the initial step remains constant through K2'+h iterations.",
        },
        "diagnostics_passed": diagnostics,
        "runtime_seconds": time.perf_counter() - started,
        "verdict": "BLOCKED",
        "verdict_reason": "Direct decomposition and scaling are reproducible, but Algorithm 2 leaves h unspecified and finite trials cannot certify the universal bound."
    }
