from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.annotate import MAX_ANNOTATIONS, _annotation, _validate_report, escape_data, escape_markdown, escape_property, publish

class EscapeTests(unittest.TestCase):
    def test_workflow_data_escapes_percent_and_line_breaks(self):
        self.assertEqual(escape_data("bad%\n::error"), "bad%25%0A::error")

    def test_workflow_properties_escape_reserved_delimiters(self):
        self.assertEqual(escape_property("dir/a,b:c%\nnext"), "dir/a%2Cb%3Ac%25%0Anext")

    def test_markdown_escapes_untrusted_filename_markup(self):
        self.assertEqual(escape_markdown("[x](url)|`code`"), r"\[x\]\(url\)\|\`code\`")

    def test_severity_maps_to_supported_workflow_commands(self):
        for severity, expected in (("ERROR", "::error"), ("WARNING", "::warning"), ("INFO", "::notice")):
            with self.subTest(severity=severity):
                item = {"severity": severity, "code": "RULE", "path": "mod/file.txt", "message": "Check this."}
                self.assertTrue(_annotation(item).startswith(expected))

    def test_invalid_severity_falls_back_to_notice(self):
        item = {"severity": "UNKNOWN", "code": "RULE", "path": "file", "message": "Review."}
        self.assertTrue(_annotation(item).startswith("::notice"))

    def test_untrusted_values_cannot_create_a_second_workflow_command(self):
        item = {"severity": "ERROR", "code": "RULE", "path": "bad::error file=other\n::warning", "message": "value%\n::add-mask::secret"}
        line = _annotation(item)
        self.assertEqual(len(line.splitlines()), 1)
        self.assertIn("%0A", line)
        self.assertIn("%3A%3A", line)
        self.assertIn("::add-mask::secret", line)

class ReportTests(unittest.TestCase):
    def test_json_validation_and_severity_counts(self):
        report = {"findings": [{"severity": "ERROR", "code": "A"}, {"severity": "WARNING", "code": "B"}, {"severity": "INFO", "code": "C"}]}
        findings, errors, warnings, infos = _validate_report(report)
        self.assertEqual((len(findings), errors, warnings, infos), (3, 1, 1, 1))

    def test_invalid_report_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            _validate_report({"findings": ["not an object"]})

    def test_many_findings_are_capped_in_output_and_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.json"
            summary_path = Path(directory) / "summary.md"
            payload = {"findings": [{"severity": "WARNING", "code": f"RULE_{i}", "path": f"file-{i}.txt", "message": "Review."} for i in range(MAX_ANNOTATIONS + 3)]}
            report_path.write_text(json.dumps(payload), encoding="utf-8")
            with patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": str(summary_path)}):
                with patch("builtins.print") as output:
                    result = publish(report_path)
            self.assertEqual(result, 0)
            self.assertEqual(output.call_count, MAX_ANNOTATIONS)
            self.assertIn("Additional findings omitted", summary_path.read_text(encoding="utf-8"))

    def test_missing_report_returns_error_without_echoing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            summary_path = Path(directory) / "summary.md"
            with patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": str(summary_path)}):
                with patch("builtins.print") as output:
                    result = publish(Path(directory) / "missing.json")
            self.assertEqual(result, 2)
            self.assertIn("missing or invalid", summary_path.read_text(encoding="utf-8"))

    def test_malformed_json_is_reported_without_echoing_source(self):
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.json"
            report_path.write_text('{"secret": "do-not-echo"', encoding="utf-8")
            with patch("builtins.print") as output:
                result = publish(report_path)
            self.assertEqual(result, 2)
            self.assertNotIn("do-not-echo", " ".join(str(call) for call in output.call_args_list))

    def test_fail_on_warning_is_opt_in(self):
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "report.json"
            report_path.write_text(json.dumps({"findings": [{"severity": "WARNING", "code": "RULE", "message": "Advisory."}]}), encoding="utf-8")
            with patch("builtins.print"):
                self.assertEqual(publish(report_path, fail_on_warning=False), 0)
                self.assertEqual(publish(report_path, fail_on_warning=True), 1)

if __name__ == "__main__":
    unittest.main()
