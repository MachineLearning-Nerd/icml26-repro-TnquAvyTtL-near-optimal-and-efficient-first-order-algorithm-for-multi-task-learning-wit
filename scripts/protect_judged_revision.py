"""Create a path-relative SHA-256 manifest for a downloaded judged Space."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.snapshot.resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in {".git", ".cache"} for part in path.parts):
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(root).as_posix()}")
    if not rows:
        raise ValueError("downloaded snapshot contains no files")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rows) + "\n")
    print(f"protected_files={len(rows)}")
    print(f"manifest={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
