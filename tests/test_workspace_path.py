from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validate_workspace_path import main, resolve_workspace_path, sarif_path_prefix


class WorkspacePathTests(unittest.TestCase):
    def test_accepts_relative_and_absolute_paths_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            mod = workspace / "mod"
            mod.mkdir(parents=True)
            self.assertEqual(resolve_workspace_path("mod", workspace), mod.resolve())
            self.assertEqual(resolve_workspace_path(str(mod), workspace), mod.resolve())

    def test_sarif_prefix_is_checkout_relative_for_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            nested = workspace / "mods" / "release candidate"
            nested.mkdir(parents=True)
            self.assertEqual(sarif_path_prefix(".", workspace), "")
            self.assertEqual(sarif_path_prefix("mods/release candidate", workspace), "mods/release candidate")
            self.assertEqual(sarif_path_prefix(str(nested), workspace), "mods/release candidate")

    def test_sarif_prefix_is_empty_for_archive_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            archive = workspace / "mod.zip"
            archive.write_bytes(b"zip fixture")
            self.assertEqual(sarif_path_prefix("mod.zip", workspace), "")

    def test_validation_step_exports_prefix_for_action_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            (workspace / "mods" / "sample").mkdir(parents=True)
            output = Path(directory) / "github-output.txt"
            with patch.dict(os.environ, {
                "WORKSPACE": str(workspace),
                "MOD_PATH": "mods/sample",
                "CONFIG_FILE": "",
                "GITHUB_OUTPUT": str(output),
            }):
                self.assertEqual(main(), 0)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0].split("<<", maxsplit=1)[0], "sarif-path-prefix")
            self.assertEqual(lines[1], "mods/sample")
            self.assertEqual(lines[2], lines[0].split("<<", maxsplit=1)[1])

    def test_rejects_relative_and_absolute_paths_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            outside.mkdir()
            for value in ("../outside", str(outside)):
                with self.subTest(value=value), self.assertRaisesRegex(ValueError, "inside the workspace"):
                    resolve_workspace_path(value, workspace)

    def test_config_file_must_be_an_existing_file_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            config = workspace / "modrelease.toml"
            config.write_text("[scan]\n", encoding="utf-8")
            self.assertEqual(resolve_workspace_path(str(config), workspace, require_file=True), config.resolve())
            with self.assertRaisesRegex(ValueError, "path must be a file"):
                resolve_workspace_path(".", workspace, require_file=True)

    def test_rejects_symlink_escape_and_missing_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            outside.mkdir()
            (outside / "secret.txt").write_text("synthetic fixture only", encoding="utf-8")
            try:
                (workspace / "escape").symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    self.skipTest("symbolic links are unavailable for this Windows account")
                raise
            with self.assertRaisesRegex(ValueError, "inside the workspace"):
                resolve_workspace_path("escape/secret.txt", workspace)
            with self.assertRaises(FileNotFoundError):
                resolve_workspace_path("missing", workspace)


if __name__ == "__main__":
    unittest.main()
