from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.normalize_tool_version import main, normalize_tool_version


class ToolVersionTests(unittest.TestCase):
    def test_adds_published_tag_prefix_when_input_omits_v(self) -> None:
        self.assertEqual(normalize_tool_version("0.3.69"), "v0.3.69")

    def test_keeps_published_tag_prefix_when_input_includes_v(self) -> None:
        self.assertEqual(normalize_tool_version("v0.3.69"), "v0.3.69")

    def test_rejects_non_semver_tags(self) -> None:
        for value in ("", "01.0.0", "v01.0.0", "0.3", "0.3.69-rc.1", " 0.3.69"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_tool_version(value)

    def test_writes_normalized_tag_to_github_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "github-output.txt"
            with patch.dict(os.environ, {"TOOL_VERSION": "0.3.69", "GITHUB_OUTPUT": str(output)}):
                self.assertEqual(main(), 0)
            self.assertEqual(output.read_text(encoding="utf-8"), "normalized=v0.3.69\n")

    def test_reports_invalid_input_without_writing_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "github-output.txt"
            with patch.dict(os.environ, {"TOOL_VERSION": "v01.0.0", "GITHUB_OUTPUT": str(output)}):
                self.assertEqual(main(), 2)
            self.assertFalse(output.exists())

    def test_default_scanner_version_matches_action_docs_and_ci(self) -> None:
        root = Path(__file__).resolve().parents[1]
        action = (root / "action.yml").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        workflow = (root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        release = (root / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("default: v0.3.85", action)
        self.assertNotIn("v0.3.83", action)
        self.assertIn("tool-version: v0.3.85", readme)
        self.assertNotIn("v0.3.83", readme)
        self.assertIn("@v1.0.67", readme)
        self.assertNotIn("@v1.0.66", readme)
        self.assertIn('modrelease 0.3.85', workflow)
        self.assertIn('tags: ["v*"]', release)
        self.assertIn("contents: write", release)
        self.assertIn('gh release create "$GITHUB_REF_NAME"', release)

    def test_action_installs_normalized_version_output(self) -> None:
        root = Path(__file__).resolve().parents[1]
        action = (root / "action.yml").read_text(encoding="utf-8")
        self.assertIn("id: validate-version", action)
        self.assertIn("${{ steps.validate-version.outputs.normalized }}", action)
        self.assertNotIn("${{ inputs.tool-version }}\"\n      run: python -m pip install", action)


if __name__ == "__main__":
    unittest.main()
