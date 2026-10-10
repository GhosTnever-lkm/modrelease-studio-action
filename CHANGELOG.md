# Changelog

## 1.0.1 - 2026-10-10

- Add a version badge to the README alongside the CI badge.

## 1.0.0 - 2026-10-08

- Initial composite GitHub Action for running ModRelease Studio on checked-out mod folders and ZIPs.
- Emit escaped GitHub workflow annotations and a capped job-summary table without exposing scanner file contents or secret values.
- Upload JSON and Markdown reports even when findings block the scan.
- Add configurable scanner version, Python version, mod/config paths, artifact name, and warning threshold.
- Add standard-library regression tests for report parsing, workflow-command escaping, Markdown safety, severity mapping, missing reports, and output caps.
