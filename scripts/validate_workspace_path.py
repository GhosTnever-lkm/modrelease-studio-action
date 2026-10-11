"""Validate that an Action input resolves inside the checked-out workspace."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def resolve_workspace_path(value: str, workspace: str | Path) -> Path:
    root = Path(workspace).resolve(strict=True)
    candidate = Path(value)
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("path must stay inside the workspace") from exc
    if not (resolved.is_file() or resolved.is_dir()):
        raise ValueError("path must be a file or directory")
    return resolved


def main() -> int:
    try:
        resolve_workspace_path(os.environ.get("MOD_PATH", "."), os.environ["WORKSPACE"])
    except (KeyError, OSError, ValueError):
        print("::error title=ModRelease Gate::mod-path must resolve to an existing file or directory inside the checked-out workspace.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
