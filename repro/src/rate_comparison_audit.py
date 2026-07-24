"""Primary-source-bound algebra audit for Claim 3's factor-k comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SOURCE_FACTS = {
    "tpgd_2605_00473": {
        "url": "https://arxiv.org/src/2605.00473",
        "sha256": "1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f",
        "anchor": "Main_Latex/main_result.tex, Corollary 5.3 and following paragraph",
        "training_rate_monomial": {"d": 1, "k": 1, "N": -1, "T": -1},
    },
    "tripuraneni_2021": {
        "url": "https://arxiv.org/pdf/2002.11684",
        "sha256": "4d2167b0f63ac72dc72deed79ed0041eefd38acc3bbbd7b4d9782967f02a46ac",
        "anchor": "Theorem 1, Eq. (2); formal statement Theorem 6",
        "source_notation": "d r^2 / n1, where n1 is total source-task samples",
        "training_rate_monomial_after_substitution": {
            "d": 1,
            "k": 2,
            "N": -1,
            "T": -1,
        },
    },
    "thekumparampil_2021": {
        "url": (
            "https://proceedings.neurips.cc/paper_files/paper/2021/file/"
            "99e7e6ce097324aceb45f98299ceb621-Paper.pdf"
        ),
        "sha256": "55cc2ba9bec7e478fc7c23744e5840da7826de032eb35b4859b986ec2424ec34",
        "anchor": "Theorem 1, Eq. (5), and Remark 2",
        "source_notation": "prediction term proportional to d r^2 / (m t)",
        "training_rate_monomial_after_substitution": {
            "d": 1,
            "k": 2,
            "N": -1,
            "T": -1,
        },
    },
}


def _canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _exponent_difference(numerator: dict[str, int], denominator: dict[str, int]):
    variables = sorted(set(numerator) | set(denominator))
    return {
        variable: numerator.get(variable, 0) - denominator.get(variable, 0)
        for variable in variables
        if numerator.get(variable, 0) != denominator.get(variable, 0)
    }


def run_rate_comparison_audit() -> dict[str, object]:
    proposed = SOURCE_FACTS["tpgd_2605_00473"]["training_rate_monomial"]
    prior_names = ("tripuraneni_2021", "thekumparampil_2021")
    comparisons = []
    for name in prior_names:
        prior = SOURCE_FACTS[name]["training_rate_monomial_after_substitution"]
        # prior / proposed must be k^1, with every other exponent cancelling.
        ratio = _exponent_difference(prior, proposed)
        comparisons.append(
            {
                "prior_source": name,
                "prior_over_tpgd_monomial": ratio,
                "factor_k_exact": ratio == {"k": 1},
            }
        )

    k_values = [2, 3, 5, 10, 20]
    numerical_cross_check = []
    for k in k_values:
        d, N, T = 37, 211, 53
        proposed_value = d * k / (N * T)
        prior_value = d * k * k / (N * T)
        numerical_cross_check.append(
            {
                "k": k,
                "prior_over_tpgd": prior_value / proposed_value,
                "equals_k": abs(prior_value / proposed_value - k) < 1e-12,
            }
        )

    # Negative control: if the cited rate were dk/(NT), the alleged factor-k
    # improvement would disappear. The checker must reject that alteration.
    invalid_prior = {"d": 1, "k": 1, "N": -1, "T": -1}
    invalid_ratio = _exponent_difference(invalid_prior, proposed)
    negative_control = {
        "mutation": "replace cited dk^2/(NT) with dk/(NT)",
        "mutated_ratio": invalid_ratio,
        "factor_k_exact": invalid_ratio == {"k": 1},
        "failed_as_intended": invalid_ratio != {"k": 1},
    }

    checker_passed = (
        all(item["factor_k_exact"] for item in comparisons)
        and all(item["equals_k"] for item in numerical_cross_check)
        and negative_control["failed_as_intended"]
    )
    return {
        "claim": "C3 factor-k comparison subclaim",
        "artifact_status": "VERIFIED_ALGEBRA_ONLY",
        "source_facts": SOURCE_FACTS,
        "source_fact_set_sha256": _canonical_hash(SOURCE_FACTS),
        "substitutions": {"r": "k", "n1": "N*T", "m": "N", "t": "T"},
        "comparisons": comparisons,
        "numerical_cross_check": numerical_cross_check,
        "negative_control": negative_control,
        "independent_checker_passed": checker_passed,
        "limitation": (
            "This checks the comparison arithmetic against two primary-source "
            "upper bounds. It does not prove Theorem 5.1/Corollary 5.3, remove "
            "hidden logarithms/constants, or establish a universal theorem."
        ),
        "claim_3_overall_verdict": "BLOCKED",
    }
