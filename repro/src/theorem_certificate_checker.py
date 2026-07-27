"""Independent checks over the serialized Claim 3–5 theorem certificate."""

from __future__ import annotations


def check_theorem_certificate(certificate):
    source = certificate["source"]
    source_passed = all(source["anchors_found"].values())

    claim3 = certificate["claim_3"]
    rate_errors = [
        abs(row["prior_to_proposed_ratio"] - row["k"])
        for row in claim3["rate_grid"]
    ]
    c3 = (
        source_passed
        and len(rate_errors) == 24
        and max(rate_errors) < 1e-12
        and claim3["negative_control"]["rejected"]
    )

    claim4 = certificate["claim_4"]
    grouped = {}
    for row in claim4["iteration_grid"]:
        grouped.setdefault(str(row["kappa"]), []).append(row["total_K1_for_target"])
    independent_spreads = {
        kappa: max(values) - min(values) for kappa, values in grouped.items()
    }
    c4 = (
        source_passed
        and len(claim4["iteration_grid"]) == 64
        and all(spread == 0 for spread in independent_spreads.values())
        and claim4["negative_control"]["rejected"]
    )

    claim5 = certificate["claim_5"]
    sample_errors = []
    for row in claim5["sample_condition_grid"]:
        reconstructed = (
            row["sigma_squared"]
            * (row["d"] + row["T"])
            * row["k"]
            * row["kappa"] ** 4
            / row["sigma_k"] ** 2
        )
        sample_errors.append(
            abs(reconstructed - row["threshold_without_constants_or_logs"])
        )
    c5 = (
        source_passed
        and len(sample_errors) == 24
        and max(sample_errors) < 1e-12
        and claim5["negative_control"]["rejected"]
    )
    return {
        "source_anchors_passed": source_passed,
        "claim_3_independent_check": c3,
        "claim_4_independent_check": c4,
        "claim_5_independent_check": c5,
        "claim_3_max_identity_error": max(rate_errors),
        "claim_4_spreads_by_kappa": independent_spreads,
        "claim_5_max_reconstruction_error": max(sample_errors),
        "all_independent_checks_passed": c3 and c4 and c5,
    }
