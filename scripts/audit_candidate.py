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


def resolve(base: str, target: str) -> str | None:
    target = target.split("#", 1)[0]
    if not target or "://" in target or target.startswith("#"):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), target))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--old-dir",
        type=Path,
        default=Path("/tmp/tpgd_repro_audit/judged_api_45396d"),
    )
    args = parser.parse_args()
    allowlist = parse_allowlist(ROOT / "release/upload_allowlist.tsv")
    assert len(allowlist) == 73
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
    }
    candidate = dict(old_files)
    candidate.update(overlay)
    old_subset_missing = sorted(set(old_files) - set(candidate))
    assert not old_subset_missing

    manifest_lines = (
        ROOT / "candidate_space/historical/judged-45396d/MANIFEST.sha256"
    ).read_text().splitlines()
    old_manifest = {
        line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
        for line in manifest_lines
    }
    assert set(old_manifest) == set(old_files)
    assert all(sha256(old_files[path]) == digest for path, digest in old_manifest.items())

    # Every old text file also has an exact historical copy. Existing PNGs are
    # intentionally left untouched by the text-only overlay.
    historical_hash_mismatches = []
    for path, payload in old_files.items():
        if path.endswith(".png"):
            continue
        historical = f"historical/judged-45396d/{path}"
        if historical not in candidate or candidate[historical] != payload:
            historical_hash_mismatches.append(path)
    assert not historical_hash_mismatches

    logbook = json.loads(candidate["logbook.json"])
    assert logbook["space_id"] == "DineshAI/TnquAvyTtL"
    assert [child["slug"] for child in logbook["root"]["children"][:3]] == [
        "claims-1-2-current",
        "claims-3-5-current",
        "claim-6-current",
    ]

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
        if not path.endswith((".md", ".json", ".py", ".toml", ".lock")):
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
    assert index.index("Claims 1–2") < index.index("Historical rejected baseline")
    assert "VERIFIED" in candidate["pages/claims-1-2.md"].decode()
    assert "BLOCKED" in candidate["pages/claims-3-5.md"].decode()
    assert "BLOCKED" in candidate["pages/claim-6.md"].decode()

    raw_path = (
        ".openresearch/artifacts/cumulative/"
        "run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json"
    )
    assert sha256(candidate[raw_path]) == (
        "c531785bbfcf8103625e27de8863e36df5221cd5970f5eb2ec174adc3def85c5"
    )
    raw = json.loads(candidate[raw_path])
    assert raw["all_historical_checks_passed"] is True
    assert raw["current_verification"]["claims_1_2"]["verdict"] == "VERIFIED"
    assert raw["current_research"]["exact_rip"]["verdict"] == "BLOCKED"
    assert raw["current_research"]["transfer_decomposition"]["verdict"] == "BLOCKED"

    expected_manifest = {}
    for source, destination in allowlist:
        expected_manifest[destination] = sha256((ROOT / source).read_bytes())
    committed_manifest = {}
    for line in (ROOT / "release/upload_manifest.sha256").read_text().splitlines():
        digest, destination = line.split(maxsplit=1)
        committed_manifest[destination] = digest
    assert expected_manifest == committed_manifest

    report = {
        "audit_status": "PASS",
        "candidate_file_count": len(candidate),
        "text_overlay_file_count": len(overlay),
        "old_file_count": len(old_files),
        "old_file_set_subset": not old_subset_missing,
        "historical_text_byte_identical": True,
        "secret_findings": secret_findings,
        "opened_files": opened,
        "missing_links": missing_links,
        "claim_conclusions": {
            "C1": "VERIFIED evidence located",
            "C2": "VERIFIED evidence located",
            "C3": "BLOCKED evidence and limitation located",
            "C4": "BLOCKED evidence and limitation located",
            "C5": "BLOCKED evidence and limitation located",
            "C6": "BLOCKED evidence and limitation located",
        },
        "conclusions_not_verifiable_from_candidate": [
            "The universal mathematical validity of Theorems 5.1, 5.4, and Corollary 5.3",
            "Any live judge score for the unpublished candidate",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
