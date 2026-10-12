"""Normalize the ModRelease Studio version input to its published Git tag."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

_SEMVER = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")


def normalize_tool_version(value: str) -> str:
    """Return a validated scanner tag with the leading ``v`` GitHub uses."""
    version = value[1:] if value.startswith("v") else value
    if not _SEMVER.fullmatch(version):
        raise ValueError("tool-version must be an exact semantic version, with or without a leading v")
    return f"v{version}"


def main() -> int:
    try:
        version = normalize_tool_version(os.environ["TOOL_VERSION"])
        output = Path(os.environ["GITHUB_OUTPUT"])
        with output.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(f"normalized={version}\n")
    except (KeyError, OSError, ValueError) as exc:
        message = str(exc) if isinstance(exc, ValueError) else "required Action environment is unavailable"
        print(f"::error title=ModRelease Gate::{message}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
