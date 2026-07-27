"""Materialize accepted direct-TPGD evidence from immutable ORX run logs.

The two inputs must be complete enough to contain the marked JSON blocks.
This script validates the preregistered gates before writing reviewer-facing
JSON and CSV.  It refuses calibration runs and partial/failed logs.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch/artifacts/claims-3-5/direct-current"


def marked_json(log: str, marker: str) -> dict:
    begin = f"{marker}_JSON_BEGIN"
    end = f"{marker}_JSON_END"
    start = log.find(begin)
    stop = log.find(end, start)
    if start < 0 or stop < 0:
        raise ValueError(f"missing complete marker pair: {marker}")
    return json.loads(log[start + len(begin) : stop].strip())


def write_json(name: str, payload: object) -> None:
    (OUT / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_csv(name: str, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {name}")
    fields = sorted({key for row in rows for key in row})
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def validate_claims_3_4(result: dict, log: str) -> None:
    if "direct_multidim_tpgd_status=PASS" not in log:
        raise ValueError("Claims 3-4 accepted status is absent")
    if not result["diagnostics_passed"]:
        raise ValueError("Claims 3-4 diagnostics failed")
    if not result["rate_strict_gate_passed"]:
        raise ValueError("Claim 3 strict four-factor gate failed")
    if not result["iteration_all_dimensions_gate_passed"]:
        raise ValueError("Claim 4 four-factor iteration gate failed")
    if not result["assumption_audit"]["all_machine_checkable_assumptions_passed"]:
        raise ValueError("Claims 3-4 assumptions failed")
    if not result["negative_control"]["failed_as_intended"]:
        raise ValueError("Claims 3-4 negative control did not fail")
    if result["independent_checker_max_absolute_difference"] > 1e-12:
        raise ValueError("Claims 3-4 independent checker disagrees")
    for factor, expected in {"d": 1, "k": 1, "T": -1, "N": -1}.items():
        summary = result["rate_summaries"][factor]
        if summary["paper_expected_slope"] != expected:
            raise ValueError(f"unexpected registered slope for {factor}")
        if not summary["strict_slope_gate_passed"]:
            raise ValueError(f"strict rate gate failed for {factor}")
        if not result["iteration_summaries"][factor]["factor_gate_passed"]:
            raise ValueError(f"iteration gate failed for {factor}")


def validate_claim_5(result: dict, log: str) -> None:
    if "claim5_threshold_phase_diagram_status=PASS" not in log:
        raise ValueError("Claim 5 accepted status is absent")
    if result["configuration"]["route_role"] != (
        "held-out validation after an immutable calibration run"
    ):
        raise ValueError("Claim 5 evidence is not the held-out route")
    required = (
        "diagnostics_passed",
        "all_fifteen_largest_N_groups_succeed",
        "all_groups_at_or_above_calibrated_margin_succeed",
        "at_least_one_low_ratio_group_fails",
        "sigma_squared_d_plus_T_and_k_slope_gate_passed",
        "sigma_k_empirical_direction_gate_passed",
    )
    if not all(result[key] for key in required):
        raise ValueError("Claim 5 preregistered diagnostics failed")
    if set(result["high_ratio_factor_families"]) != {
        "sigma_squared",
        "d_plus_T",
        "k",
        "kappa",
        "sigma_k",
    }:
        raise ValueError("Claim 5 factor-family coverage is incomplete")
    if not result["negative_control"]["failed_as_intended"]:
        raise ValueError("Claim 5 negative control did not fail")
    if result["independent_checker_max_absolute_difference"] > 1e-12:
        raise ValueError("Claim 5 independent checker disagrees")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims-3-4-log", type=Path, required=True)
    parser.add_argument("--claim-5-log", type=Path, required=True)
    args = parser.parse_args()

    log34 = args.claims_3_4_log.read_text()
    log5 = args.claim_5_log.read_text()
    result34 = marked_json(log34, "DIRECT_MULTIDIM_TPGD")
    result5 = marked_json(log5, "CLAIM5_THRESHOLD_PHASE_DIAGRAM")
    validate_claims_3_4(result34, log34)
    validate_claim_5(result5, log5)

    OUT.mkdir(parents=True, exist_ok=True)
    write_json("direct_multidim_tpgd.json", result34)
    write_json("claim5_threshold_phase_diagram.json", result5)
    write_csv("claim3_rate_rows.csv", result34["rate_rows"])
    write_csv("claim4_iteration_rows.csv", result34["iteration_rows"])
    write_csv("claim5_phase_diagram_rows.csv", result5["rows"])
    write_json(
        "independent_checker_output.json",
        {
            "claims_3_4_max_absolute_difference": result34[
                "independent_checker_max_absolute_difference"
            ],
            "claim_5_max_absolute_difference": result5[
                "independent_checker_max_absolute_difference"
            ],
            "tolerance": 1e-12,
            "all_independent_checks_passed": True,
        },
    )
    write_json(
        "negative_control_output.json",
        {
            "claims_3_4": result34["negative_control"],
            "claim_5": result5["negative_control"],
            "all_controls_failed_as_intended": True,
        },
    )
    write_json(
        "run_metadata.json",
        {
            "fixed_command": "uv run python repro/src/verify.py",
            "environment": [".python-version", "pyproject.toml", "uv.lock"],
            "claims_3_4": {
                "git_sha": "1aa33107943e838d5d09f80baa614383c5b828cc",
                "orx_run_id": "44fb4f8f-3ee0-4739-bdfd-46f6ab195f4f",
                "orx_wall_time": "3m59s",
                "module_runtime_seconds": result34["runtime_seconds"],
                "estimated_cores": 8,
                "actual_container_logical_cpus": 64,
                "process_affinity_cpus": 64,
                "numerical_thread_limit": 8,
                "backend": "hf",
                "flavor": "cpu-upgrade",
                "seeds": result34["configuration"]["seeds"],
            },
            "claim_5_calibration": {
                "git_sha": "5bc1702b3480dffedf676a0e052d0d9ea5a9ac53",
                "orx_run_id": "200bd469-e6d7-484b-9571-d9503ef82f35",
                "orx_wall_time": "4m40s",
                "scientific_gate": "FAILED; used only to freeze C=10",
            },
            "claim_5_held_out": {
                "git_sha": "963ddf47b5e0e5ee0f59dbd14552e414b2931f26",
                "orx_run_id": "5aaa91cb-c2aa-47f3-b1e4-d9342b475db0",
                "orx_wall_time": "4m14s",
                "module_runtime_seconds": result5["runtime_seconds"],
                "estimated_cores": 8,
                "actual_container_logical_cpus": 64,
                "process_affinity_cpus": 64,
                "numerical_thread_limit": 8,
                "backend": "hf",
                "flavor": "cpu-upgrade",
                "seeds": result5["configuration"]["seeds"],
            },
            "cost": "The HF interface exposed no monetary cost; none is invented.",
        },
    )

    print(f"materialized={OUT}")
    print(f"claim3_rate_rows={len(result34['rate_rows'])}")
    print(f"claim4_iteration_rows={len(result34['iteration_rows'])}")
    print(f"claim5_phase_diagram_rows={len(result5['rows'])}")
    print("direct_current_evidence_status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
