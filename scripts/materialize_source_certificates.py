"""Extract the accepted source certificates from an ORX run log.

The script reads the complete log on stdin, validates the expected marker
pairs, and writes only machine-readable evidence derived from those marked
JSON blocks.  It intentionally refuses partial or failed run logs.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch/artifacts/claims-3-5/source-certified"
EXPECTED_STATUS = (
    "theorem_certificate_status=PASS",
    "dimension_iteration_status=PASS",
    "historical_baseline_status=PASS",
)


def marked_json(log: str, name: str) -> dict:
    begin = f"{name}_JSON_BEGIN"
    end = f"{name}_JSON_END"
    start = log.find(begin)
    stop = log.find(end, start)
    if start < 0 or stop < 0:
        raise ValueError(f"missing complete {name} marker pair")
    return json.loads(log[start + len(begin) : stop].strip())


def main() -> int:
    log = sys.stdin.read()
    for status in EXPECTED_STATUS:
        if status not in log:
            raise ValueError(f"accepted status missing: {status}")

    theorem = marked_json(log, "THEOREM_CERTIFICATE")
    dimension = marked_json(log, "DIMENSION_ITERATION")
    if not theorem["all_certificates_passed"]:
        raise ValueError("theorem certificate did not pass")
    if not theorem["independent_checker"]["all_independent_checks_passed"]:
        raise ValueError("independent theorem checker did not pass")
    if not dimension["diagnostics_passed"]:
        raise ValueError("dimension sweep did not pass")
    if not dimension["negative_control"]["rejected_as_dimension_dependent"]:
        raise ValueError("dimension negative control was not rejected")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "theorem_certificate.json").write_text(
        json.dumps(theorem, indent=2, sort_keys=True) + "\n"
    )
    (OUT / "dimension_iteration_sweep.json").write_text(
        json.dumps(dimension, indent=2, sort_keys=True) + "\n"
    )
    (OUT / "independent_checker_output.json").write_text(
        json.dumps(theorem["independent_checker"], indent=2, sort_keys=True) + "\n"
    )
    controls = {
        "claim_3": theorem["claim_3"]["negative_control"],
        "claim_4_symbolic": theorem["claim_4"]["negative_control"],
        "claim_4_tpgd": dimension["negative_control"],
        "claim_5": theorem["claim_5"]["negative_control"],
    }
    (OUT / "negative_control_output.json").write_text(
        json.dumps(controls, indent=2, sort_keys=True) + "\n"
    )

    fields = [
        "d",
        "seed",
        "first_hit_iteration",
        "initial_relative_squared_error",
        "final_relative_squared_error",
        "eta1",
        "eta2",
        "exact_rip_delta",
        "condition_number",
    ]
    with (OUT / "dimension_iteration_rows.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(dimension["rows"])

    print(f"materialized={OUT}")
    print(f"dimension_rows={len(dimension['rows'])}")
    print(f"theorem_certificate_status=PASS")
    print(f"dimension_iteration_status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
