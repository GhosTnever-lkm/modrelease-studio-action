from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_workspace_path import resolve_workspace_path


class WorkspacePathTests(unittest.TestCase):
    def test_accepts_relative_and_absolute_paths_inside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            mod = workspace / "mod"
            mod.mkdir(parents=True)
            self.assertEqual(resolve_workspace_path("mod", workspace), mod.resolve())
            self.assertEqual(resolve_workspace_path(str(mod), workspace), mod.resolve())

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

    def test_rejects_symlink_escape_and_missing_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            outside = root / "outside"
            workspace.mkdir()
            outside.mkdir()
            (outside / "secret.txt").write_text("synthetic fixture only", encoding="utf-8")
            (workspace / "escape").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "inside the workspace"):
                resolve_workspace_path("escape/secret.txt", workspace)
            with self.assertRaises(FileNotFoundError):
                resolve_workspace_path("missing", workspace)


if __name__ == "__main__":
    unittest.main()
