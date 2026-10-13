from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True
    )
    seen: dict[str, str] = {}
    collisions: list[tuple[str, str]] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        path = raw_path.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        key = path.casefold()
        previous = seen.get(key)
        if previous is not None and previous != path:
            collisions.append((previous, path))
        else:
            seen[key] = path
    if collisions:
        for left, right in collisions:
            print(f"Case-insensitive checkout collision: {left} <-> {right}", file=sys.stderr)
        return 1
    print("Tracked paths are unique on case-insensitive filesystems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
