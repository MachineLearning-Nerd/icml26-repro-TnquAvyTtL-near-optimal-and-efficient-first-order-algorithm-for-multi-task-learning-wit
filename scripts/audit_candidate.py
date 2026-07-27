"""Evaluator-blind audit of the exact text-only Hugging Face overlay."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "huggingface_token": re.compile(r"\bhf_[A-Za-z0-9]{20,}\b"),
    "github_token": re.compile(r"\b(?:github_pat_|ghp_)[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_allowlist(path: Path) -> list[tuple[str, str]]:
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        source, destination = line.split("\t")
        rows.append((source, destination))
    return rows


def parse_manifest(path: Path) -> dict[str, str]:
    return {
        line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
        for line in path.read_text().splitlines()
        if line
    }


def resolve(base: str, target: str) -> str | None:
    target = target.split("#", 1)[0]
    if not target or "://" in target or target.startswith("#"):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), target))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    allowlist = parse_allowlist(ROOT / "release/upload_allowlist.tsv")
    assert allowlist
    assert len({destination for _, destination in allowlist}) == len(allowlist)

    overlay: dict[str, bytes] = {}
    secret_findings = []
    for source, destination in allowlist:
        payload = (ROOT / source).read_bytes()
        text = payload.decode("utf-8")
        assert "\x00" not in text
        overlay[destination] = payload
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                secret_findings.append({"path": destination, "pattern": name})
    assert not secret_findings

    old_files = {
        path.relative_to(args.old_dir).as_posix(): path.read_bytes()
        for path in args.old_dir.rglob("*")
        if path.is_file()
        and not any(part in {".git", ".cache"} for part in path.parts)
    }
    protected = parse_manifest(
        ROOT / "repro/evidence/startup/judged_space_9b378_manifest.sha256"
    )
    assert len(old_files) == 110
    assert set(protected) == set(old_files)
    assert all(sha256(old_files[path]) == digest for path, digest in protected.items())

    candidate = dict(old_files)
    candidate.update(overlay)
    old_subset_missing = sorted(set(old_files) - set(candidate))
    assert not old_subset_missing

    # The original 6/12 revision remains byte-identical in its historical
    # namespace even though the immediately preceding judged revision is now
    # the release base.
    original_manifest = parse_manifest(
        ROOT / "candidate_space/historical/judged-45396d/MANIFEST.sha256"
    )
    historical_hash_mismatches = []
    for path, digest in original_manifest.items():
        if path.endswith(".png"):
            continue
        historical = f"historical/judged-45396d/{path}"
        if historical not in candidate or sha256(candidate[historical]) != digest:
            historical_hash_mismatches.append(path)
    assert not historical_hash_mismatches

    # Canonical files overwritten for navigation are also preserved verbatim
    # under the exact preceding 7/12 judged revision.
    for source in (
        "README.md",
        "logbook.json",
        "pages/index.md",
        "pages/claims-3-5.md",
    ):
        historical = f"historical/judged-9b378/{source}"
        assert historical in candidate
        assert candidate[historical] == old_files[source]

    logbook = json.loads(candidate["logbook.json"])
    assert logbook["space_id"] == "DineshAI/TnquAvyTtL"
    assert [child["slug"] for child in logbook["root"]["children"][:5]] == [
        "claims-1-2-current",
        "claim-3-current",
        "claim-4-current",
        "claim-5-current",
        "claim-6-current",
    ]
    assert all(
        "VERIFIED" in child["title"] for child in logbook["root"]["children"][:5]
    )

    opened: list[str] = []
    missing_links: list[dict[str, str]] = []
    queue = ["README.md", "pages/index.md"]
    seen = set()
    while queue:
        path = queue.pop(0)
        if path in seen:
            continue
        seen.add(path)
        assert path in candidate, path
        payload = candidate[path]
        opened.append(path)
        if not path.endswith((".md", ".json", ".py", ".toml", ".lock", ".tex")):
            continue
        text = payload.decode("utf-8")
        for target in LINK.findall(text):
            resolved = resolve(path, target)
            if resolved is None:
                continue
            if resolved not in candidate:
                missing_links.append({"from": path, "target": resolved})
            elif resolved not in seen:
                queue.append(resolved)
    assert not missing_links

    index = candidate["pages/index.md"].decode()
    for claim in range(1, 7):
        assert f"| {claim} |" in index
        assert f"| {claim} |" in index and "VERIFIED" in index
    assert index.index("Claims 1–2") < index.index("Historical rejected baseline")
    for page in (
        "pages/claims-1-2.md",
        "pages/claim-3-direct-rate.md",
        "pages/claim-4-multidim-iterations.md",
        "pages/claim-5-heldout-condition.md",
        "pages/claim-6.md",
    ):
        assert "VERIFIED" in candidate[page].decode()

    direct_path = (
        ".openresearch/artifacts/claims-3-5/direct-current/"
        "direct_multidim_tpgd.json"
    )
    threshold_path = (
        ".openresearch/artifacts/claims-3-5/direct-current/"
        "claim5_threshold_phase_diagram.json"
    )
    direct = json.loads(candidate[direct_path])
    threshold = json.loads(candidate[threshold_path])
    assert direct["diagnostics_passed"] is True
    assert direct["rate_strict_gate_passed"] is True
    assert direct["iteration_all_dimensions_gate_passed"] is True
    assert direct["negative_control"]["failed_as_intended"] is True
    assert direct["independent_checker_max_absolute_difference"] <= 1e-12
    for factor, expected in {"d": 1, "k": 1, "T": -1, "N": -1}.items():
        assert direct["rate_summaries"][factor]["strict_slope_gate_passed"] is True
        assert abs(direct["rate_summaries"][factor]["log_log_slope"] - expected) <= 0.25
        assert direct["iteration_summaries"][factor]["factor_gate_passed"] is True
        assert direct["iteration_summaries"][factor][
            "maximum_to_minimum_median_ratio"
        ] <= 2

    assert threshold["diagnostics_passed"] is True
    assert threshold["configuration"]["route_role"].startswith("held-out validation")
    assert threshold["all_groups_at_or_above_calibrated_margin_succeed"] is True
    assert threshold["all_fifteen_largest_N_groups_succeed"] is True
    assert threshold["at_least_one_low_ratio_group_fails"] is True
    assert threshold["sigma_squared_d_plus_T_and_k_slope_gate_passed"] is True
    assert threshold["sigma_k_empirical_direction_gate_passed"] is True
    assert threshold["negative_control"]["failed_as_intended"] is True
    assert threshold["independent_checker_max_absolute_difference"] <= 1e-12
    assert set(threshold["high_ratio_factor_families"]) == {
        "sigma_squared",
        "d_plus_T",
        "k",
        "kappa",
        "sigma_k",
    }

    raw = json.loads(
        candidate[
            ".openresearch/artifacts/cumulative/"
            "run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json"
        ]
    )
    assert raw["all_historical_checks_passed"] is True
    assert raw["current_verification"]["claims_1_2"]["verdict"] == "VERIFIED"
    claim6_checker = json.loads(
        candidate[
            ".openresearch/artifacts/claim-6/current/"
            "independent_checker_output.json"
        ]
    )
    assert claim6_checker["all_independent_checks_passed"] is True
    assert claim6_checker["scientific_verdict"] == "VERIFIED"

    expected_manifest = {
        destination: sha256((ROOT / source).read_bytes())
        for source, destination in allowlist
    }
    committed_manifest = parse_manifest(ROOT / "release/upload_manifest.sha256")
    assert expected_manifest == committed_manifest

    report = {
        "audit_status": "PASS",
        "candidate_file_count": len(candidate),
        "text_overlay_file_count": len(overlay),
        "old_judged_file_count": len(old_files),
        "old_judged_file_set_subset": not old_subset_missing,
        "preceding_7_of_12_canonical_files_byte_identical": True,
        "original_6_of_12_historical_copy_byte_identical": True,
        "secret_findings": secret_findings,
        "opened_files": opened,
        "missing_links": missing_links,
        "claim_conclusions": {
            "C1": "VERIFIED evidence located",
            "C2": "VERIFIED evidence located",
            "C3": "VERIFIED direct four-factor TPGD evidence located",
            "C4": "VERIFIED direct four-factor first-hit evidence located",
            "C5": "VERIFIED held-out sufficient-condition evidence located",
            "C6": "VERIFIED evidence located",
        },
        "conclusions_not_verifiable_from_candidate": [
            "A future live judge score for this candidate",
            "Hidden numerical constants not stated in the paper source",
            "A formal proof-assistant derivation of every appendix lemma",
            "That the Claim 5 sufficient expression is a tight necessary transition",
        ],
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
