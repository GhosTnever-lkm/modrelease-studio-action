# Changelog

## 1.0.10 - 2026-10-11

- Pin the scanner and integration fixture to ModRelease Studio v0.3.8.
- Refresh quick-start to Action v1.0.10.

## 1.0.9 - 2026-10-11

- Pin the scanner and CI policy fixture to ModRelease Studio v0.3.7.
- Refresh the quick-start Action tag to v1.0.9.

## 1.0.8 - 2026-10-11

- Pin the default scanner and Action integration fixture to ModRelease Studio v0.3.6.
- Refresh the quick-start to v1.0.8.

## 1.0.7 - 2026-10-11

- Pin the default and integration fixture to ModRelease Studio v0.3.5.
- Refresh the Action quick-start to v1.0.7.

## 1.0.6 - 2026-10-11

- Document workspace-relative `config-file` use for ModRelease Studio v0.3.4 required-path policies.
- Add a CI integration run of the composite Action against a clean policy fixture.
- Correct the README scanner default and refresh quick-start to v1.0.6.

## 1.0.5 - 2026-10-11

- Update the default and quick-start scanner pin to ModRelease Studio v0.3.4.
- Refresh the example Action reference to v1.0.5.

## 1.0.4 - 2026-10-11

- Update the default and quick-start scanner pin to ModRelease Studio v0.3.2, including required-path policy support.
- Refresh the example Action reference to v1.0.4.

## 1.0.3 — 2026-10-11

- Add GitHub Funding metadata with verified Buy Me a Coffee and Gumroad links.
- Refresh the quick-start action tag.

## 1.0.2 - 2026-10-11

- Refresh the quick-start to use action v1.0.2 and ModRelease Studio v0.3.1.
- Update the action default scanner version to v0.3.1.

## 1.0.1 - 2026-10-10

- Add a version badge to the README alongside the CI badge.

## 1.0.0 - 2026-10-08

- Initial composite GitHub Action for running ModRelease Studio on checked-out mod folders and ZIPs.
- Emit escaped GitHub workflow annotations and a capped job-summary table without exposing scanner file contents or secret values.
- Upload JSON and Markdown reports even when findings block the scan.
- Add configurable scanner version, Python version, mod/config paths, artifact name, and warning threshold.
- Add standard-library regression tests for report parsing, workflow-command escaping, Markdown safety, severity mapping, missing reports, and output caps.
