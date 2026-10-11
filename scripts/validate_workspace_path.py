"""Validate that an Action input resolves inside the checked-out workspace."""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path


def resolve_workspace_path(value: str, workspace: str | Path, *, require_file: bool = False) -> Path:
    root = Path(workspace).resolve(strict=True)
    candidate = Path(value)
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("path must stay inside the workspace") from exc
    if require_file and not resolved.is_file():
        raise ValueError("path must be a file")
    if not (resolved.is_file() or resolved.is_dir()):
        raise ValueError("path must be a file or directory")
    return resolved


def sarif_path_prefix(value: str, workspace: str | Path) -> str:
    """Return a checkout-relative prefix for a scanned directory, or empty for ZIP/file scans."""
    root = Path(workspace).resolve(strict=True)
    resolved = resolve_workspace_path(value, root)
    if not resolved.is_dir():
        return ""
    relative = resolved.relative_to(root).as_posix()
    return "" if relative == "." else relative


def _write_output(name: str, value: str) -> None:
    destination = os.environ.get("GITHUB_OUTPUT")
    if not destination:
        return
    delimiter = "ghadelimiter_" + uuid.uuid4().hex
    while delimiter in value:
        delimiter = "ghadelimiter_" + uuid.uuid4().hex
    with Path(destination).open("a", encoding="utf-8", newline="") as output:
        output.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main() -> int:
    try:
        workspace = os.environ["WORKSPACE"]
        mod_path = os.environ.get("MOD_PATH", ".")
        resolve_workspace_path(mod_path, workspace)
        config_file = os.environ.get("CONFIG_FILE", "")
        if config_file:
            resolve_workspace_path(config_file, workspace, require_file=True)
        _write_output("sarif-path-prefix", sarif_path_prefix(mod_path, workspace))
    except (KeyError, OSError, ValueError):
        print("::error title=ModRelease Gate::mod-path and config-file must resolve inside the checked-out workspace; config-file must be an existing file.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
