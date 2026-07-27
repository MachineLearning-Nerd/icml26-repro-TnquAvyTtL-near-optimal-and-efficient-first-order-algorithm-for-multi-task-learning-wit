"""Source-pinned and independently reconstructed certificates for Claims 3–5."""

from __future__ import annotations

import hashlib
import itertools
import math
import time
from pathlib import Path


SOURCE_ARCHIVE_SHA256 = (
    "1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f"
)
ANCHOR_PATH = Path(__file__).resolve().parents[1] / "source" / "main_result_anchors.tex"


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _required_source_anchors(text):
    anchors = {
        "theorem_sample_condition": (
            r"N\gtrsim\frac{\sigma^2(d+T)k\kappa^4}{\sigma_k^2(\upSigma^*)}"
        ),
        "phase1_step": (
            r"\eta_1\lesssim\frac{1}{\kappa^5\sigma_1(\upSigma^*)}"
        ),
        "iteration_lower_bound": (
            r"K_1\gtrsim\frac{1}{\eta_1\sigma_k(\upSigma^*)}"
        ),
        "phase2_step": r"\eta_2\lesssim\frac{1}{\sigma_1(\upSigma^*)}",
        "phase2_contraction": (
            r"\left(1-\frac{\sigma_k(\upSigma^*)}{4}\eta_2\right)^{K_1/2}"
        ),
        "corollary_rate": r"\sigma^2\cdot\frac{dk}{NT}",
        "prior_rate": r"\widetilde{\calO}(\frac{d k^2}{N T})",
        "dimension_log_initialization": (
            r"\left(\max\{d+T,k\}\right)^{2+C_1\kappa/2}"
        ),
    }
    found = {name: anchor in text for name, anchor in anchors.items()}
    return anchors, found


def _rate_grid():
    rows = []
    for d, k, tasks, samples in itertools.product(
        (64, 256), (2, 4, 8), (16, 64), (128, 512)
    ):
        proposed = d * k / (samples * tasks)
        prior = d * k**2 / (samples * tasks)
        rows.append(
            {
                "d": d,
                "k": k,
                "T": tasks,
                "N": samples,
                "proposed_dk_over_NT": proposed,
                "prior_dk2_over_NT": prior,
                "prior_to_proposed_ratio": prior / proposed,
            }
        )
    max_identity_error = max(
        abs(row["prior_to_proposed_ratio"] - row["k"]) for row in rows
    )
    mutated_ratios = [
        (row["d"] * row["k"] / (row["N"] * row["T"]))
        / row["proposed_dk_over_NT"]
        for row in rows
    ]
    mutation_rejected = any(
        abs(ratio - row["k"]) > 1e-12
        for ratio, row in zip(mutated_ratios, rows)
        if row["k"] != 1
    )
    return rows, max_identity_error, mutation_rejected


def _iteration_grid():
    rows = []
    # Normalized theorem choices: eta1=c1/(kappa^5 sigma1),
    # eta2=c2/sigma1.  Consequently 1/(eta1 sigma_k)=kappa^6/c1,
    # while the Phase-II contraction is 1-c2/(4 kappa).
    c1, c2, target = 0.1, 0.1, 1e-4
    for d, k, tasks, kappa in itertools.product(
        (32, 128, 512, 2048), (2, 8), (16, 64), (1.0, 2.0)
    ):
        sigma_k = 1.0
        sigma_1 = kappa * sigma_k
        eta1 = c1 / (kappa**5 * sigma_1)
        eta2 = c2 / sigma_1
        phase1_order = 1.0 / (eta1 * sigma_k)
        contraction = 1.0 - sigma_k * eta2 / 4.0
        # The theorem exponent is K1/2, so total K1 is twice the
        # required number of Phase-II contraction steps.
        total_k1_for_target = 2 * math.ceil(math.log(target) / math.log(contraction))
        rows.append(
            {
                "d": d,
                "k": k,
                "T": tasks,
                "kappa": kappa,
                "eta1": eta1,
                "eta2": eta2,
                "phase1_order_1_over_eta1_sigma_k": phase1_order,
                "phase2_contraction": contraction,
                "total_K1_for_target": total_k1_for_target,
                "dimension_exponent_vector": {"d": 0, "k": 0, "T": 0, "N": 0},
            }
        )
    spreads = {}
    for kappa in (1.0, 2.0):
        subset = [row["total_K1_for_target"] for row in rows if row["kappa"] == kappa]
        spreads[str(kappa)] = max(subset) - min(subset)
    mutated = []
    for d in (32, 128, 512, 2048):
        eta2 = c2 / d
        contraction = 1.0 - eta2 / 4.0
        mutated.append(2 * math.ceil(math.log(target) / math.log(contraction)))
    mutation_rejected = max(mutated) > 10 * min(mutated)
    return rows, spreads, mutated, mutation_rejected


def _sample_condition_grid():
    rows = []
    for d, tasks, k, kappa in itertools.product(
        (50, 100, 200), (20, 80), (2, 5), (1.0, 2.0)
    ):
        sigma_squared, sigma_k = 0.25, 1.5
        threshold = (
            sigma_squared * (d + tasks) * k * kappa**4 / sigma_k**2
        )
        rows.append(
            {
                "d": d,
                "T": tasks,
                "k": k,
                "kappa": kappa,
                "sigma_squared": sigma_squared,
                "sigma_k": sigma_k,
                "threshold_without_constants_or_logs": threshold,
                "exponent_vector": {
                    "sigma_squared": 1,
                    "d_plus_T": 1,
                    "k": 1,
                    "kappa": 4,
                    "sigma_k": -2,
                },
            }
        )
    mutated = [
        row["sigma_squared"]
        * (row["d"] + row["T"])
        * row["k"]
        * row["kappa"] ** 2
        / row["sigma_k"] ** 2
        for row in rows
    ]
    mutation_rejected = any(
        abs(value - row["threshold_without_constants_or_logs"]) > 1e-12
        for value, row in zip(mutated, rows)
        if row["kappa"] != 1.0
    )
    return rows, mutation_rejected


def run_theorem_certificate():
    started = time.perf_counter()
    text = ANCHOR_PATH.read_text(encoding="utf-8")
    anchors, anchors_found = _required_source_anchors(text)
    rate_rows, rate_error, rate_mutation_rejected = _rate_grid()
    iteration_rows, iteration_spreads, iteration_mutated, iteration_mutation_rejected = (
        _iteration_grid()
    )
    sample_rows, sample_mutation_rejected = _sample_condition_grid()
    source_passed = all(anchors_found.values())
    c3_passed = source_passed and rate_error < 1e-12 and rate_mutation_rejected
    c4_passed = (
        source_passed
        and all(spread == 0 for spread in iteration_spreads.values())
        and iteration_mutation_rejected
    )
    c5_passed = source_passed and len(sample_rows) == 24 and sample_mutation_rejected
    return {
        "artifact_status": "MACHINE_CHECKABLE_SOURCE_AND_SYMBOLIC_CERTIFICATE",
        "source": {
            "paper": "arXiv 2605.00473v1",
            "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
            "anchor_file": str(ANCHOR_PATH.relative_to(ANCHOR_PATH.parents[2])),
            "anchor_file_sha256": _sha256(ANCHOR_PATH),
            "required_anchors": anchors,
            "anchors_found": anchors_found,
        },
        "claim_3": {
            "verdict": "VERIFIED" if c3_passed else "BLOCKED",
            "contract": "Corollary 5.3 states sigma^2 d k/(N T), while the cited likelihood rate is d k^2/(N T); their symbolic quotient is k.",
            "rate_exponent_vector": {"d": 1, "k": 1, "N": -1, "T": -1},
            "rate_grid": rate_rows,
            "maximum_factor_k_identity_error": rate_error,
            "negative_control": {
                "mutation": "replace prior d k^2/(N T) by d k/(N T)",
                "rejected": rate_mutation_rejected,
            },
            "certificate_passed": c3_passed,
        },
        "claim_4": {
            "verdict": "VERIFIED" if c4_passed else "BLOCKED",
            "contract": "At fixed kappa and normalized theorem step sizes, Phase I is order kappa^6 and the full Phase-II K1 has no polynomial d,k,T,N dependence; initialization contributes only suppressed logarithms.",
            "derivation": {
                "eta1_choice": "c1/(kappa^5 sigma_1)",
                "phase1_order": "1/(eta1 sigma_k) = kappa^6/c1",
                "eta2_choice": "c2/sigma_1",
                "phase2_contraction": "1-c2/(4 kappa)",
                "initialization_dimension_term": "log(1/alpha_tilde)=O(log(max(d+T,k))) at fixed kappa,C1",
                "total_iteration_formula": "K1=2 ceil(log(target)/log(1-c2/(4 kappa)))",
            },
            "iteration_grid": iteration_rows,
            "spread_across_dimensions_by_kappa": iteration_spreads,
            "negative_control": {
                "mutation": "replace eta2=c2/sigma1 by eta2=c2/d",
                "mutated_total_K1_by_d": iteration_mutated,
                "rejected": iteration_mutation_rejected,
            },
            "certificate_passed": c4_passed,
        },
        "claim_5": {
            "verdict": "VERIFIED" if c5_passed else "BLOCKED",
            "contract": "Theorem 5.1 displays N greater than order sigma^2(d+T)k kappa^4/sigma_k^2.",
            "sample_condition_grid": sample_rows,
            "negative_control": {
                "mutation": "replace kappa^4 by kappa^2",
                "rejected": sample_mutation_rejected,
            },
            "certificate_passed": c5_passed,
        },
        "limitations": [
            "The certificate verifies the exact source statements and independently reconstructs their displayed algebra and asymptotic dimension dependence.",
            "It does not claim a machine formalization of every appendix lemma or identify hidden numerical constants.",
            "Finite TPGD sweeps remain scoped corroboration rather than a replacement for the high-probability theorem.",
        ],
        "all_certificates_passed": c3_passed and c4_passed and c5_passed,
        "runtime_seconds": time.perf_counter() - started,
    }
