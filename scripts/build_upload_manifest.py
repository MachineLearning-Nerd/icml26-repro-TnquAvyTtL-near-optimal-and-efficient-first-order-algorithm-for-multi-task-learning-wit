"""Build the exact SHA-256 manifest for the text-only HF upload allowlist."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "release/upload_allowlist.tsv"
MANIFEST = ROOT / "release/upload_manifest.sha256"


def main() -> int:
    rows = []
    destinations = set()
    for line in ALLOWLIST.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        source, destination = line.split("\t")
        if destination in destinations:
            raise ValueError(f"duplicate upload destination: {destination}")
        destinations.add(destination)
        payload = (ROOT / source).read_bytes()
        payload.decode("utf-8")
        rows.append(f"{hashlib.sha256(payload).hexdigest()}  {destination}")
    MANIFEST.write_text("\n".join(rows) + "\n")
    print(f"text_upload_files={len(rows)}")
    print(f"manifest={MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
