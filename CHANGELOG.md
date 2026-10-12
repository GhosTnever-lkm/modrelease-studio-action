# Changelog

## 1.0.51 - 2026-10-12

- Pin ModRelease Studio v0.3.65 in the default input, integration CI, and usage examples.

## 1.0.49 - 2026-10-12

- Pin the default scanner and integration CI to ModRelease Studio v0.3.63, including the corrected modpack and CI-gate guidance.

## 1.0.48 - 2026-10-12

- Correct the scanner version assertions in integration CI and republish the v0.3.62 default as a green release.

## 1.0.47 - 2026-10-12

- Pin the default scanner to ModRelease Studio v0.3.62, including fine-grained GitHub token detection; refresh examples and CI integration scans.

## 1.0.46 - 2026-10-12

- Reject scanner version tags with leading zeroes so tool-version validation matches SemVer.
- Add an integration check for invalid scanner version input.

## 1.0.45 - 2026-10-12

- Pin the default scanner to ModRelease Studio v0.3.62; update the examples and integration CI to assert the current scanner release.

## 1.0.44 - 2026-10-12

- Pin the default scanner to ModRelease Studio v0.3.60, including its synchronized release metadata and installation examples.
- Refresh CI integration tests and examples to exercise the current scanner release.

## 1.0.43 - 2026-10-12

- Export ModRelease Studio's SARIF 2.1.0 report as an Action output and downloadable artifact, including on blocking findings.
- Prefix SARIF locations with the checked-out folder path so findings point to repository files; ZIP scans keep archive-relative locations.
- Document optional GitHub Code Scanning upload and its workflow-level permission requirement.
- Add unit and end-to-end CI coverage for output readiness, blocking findings, and nested checkout paths.

## 1.0.42 - 2026-10-12

- Pin the default scanner to ModRelease Studio v0.3.58, including SARIF 2.1.0 export.
- Refresh the current usage example and CI integration checks to use the latest scanner and Action release.

## 1.0.41 - 2026-10-11

- Pin the default scanner to ModRelease Studio v0.3.57, which prunes a directory and emits `READ_METADATA` if junction-status metadata cannot be checked.
- Refresh examples and user-facing installation guidance.
- Verify in CI that inaccessible junction metadata is pruned, reported as `READ_METADATA`, and follows advisory/strict warning policy.

## 1.0.40 - 2026-10-11

- Exercise the scanner's `JUNCTION` warning through the real report formatter: advisory mode passes and `fail-on-warning` blocks.
- Keep the default scanner on v0.3.56.

## 1.0.39 - 2026-10-11

- Upgrade the default ModRelease Studio scanner to v0.3.56, which avoids traversing Windows directory junctions and reports skipped junctions.
- Assert the installed default scanner version in CI.

## 1.0.38 - 2026-10-11

- Upgrade to ModRelease Studio v0.3.53; keep secret scanning active for every path shipped inside ZIP archives.
- Add CI coverage for a synthetic secret under `.git` inside a ZIP.


## 1.0.37 - 2026-10-11

- Correct the traversal integration fixture boundary: the OS-junk file is an indexed entry alongside the sample mod file.
- Preserve a tight entry limit while asserting ignored folders do not consume it.



## 1.0.35 - 2026-10-11

- Upgrade the default scanner to v0.3.50 for generated-folder exclusions and OS-junk warnings.
- Verify the installed scanner traversal policy in CI.


## 1.0.34 - 2026-10-11

- Add a scanner-derived `LARGE_TEXT_FILE` policy check: advisory mode passes, `fail-on-warning` blocks.


## 1.0.33 - 2026-10-11

- Upgrade the default scanner to v0.3.46, surfacing `LARGE_TEXT_FILE` when an indexed text file grows past the bounded read limit.
- Add a CI integration check for the installed scanner warning.


## 1.0.32 - 2026-10-11

- Advance the default scanner pin to v0.3.44 so uploaded JSON/Markdown artifacts visibly escape bidi and Unicode line separators.
- Add an end-to-end workflow regression that verifies the artifact Markdown is safe and JSON preserves the decoded finding path.

## 1.0.31 - 2026-10-11

- Escape bidi controls and Unicode line/paragraph separators visibly in workflow annotations and Markdown summaries to prevent deceptive output.
- Extend tests to cover bidi, C1, ANSI, U+2028, and U+2029 values; keep the scanner pin at v0.3.25 because scanning behavior is unchanged.

## 1.0.30 - 2026-10-11

- Assert the exact installed ModRelease Studio version after default and explicit Action invocations.
- Keep the scanner pin at v0.3.25; this release changes CI verification only.

## 1.0.29 - 2026-10-11

- Advance the default scanner to v0.3.25 so the Action uses symlink-safe indexed reads.
- Refresh action examples and end-to-end fixtures; the successful policy fixture now exercises the action default.


## 1.0.28 - 2026-10-11

- Pin the default scanner to v0.3.16, which omits local parent directories from shared reports.
- Refresh action usage examples to v1.0.28.

## 1.0.27 - 2026-10-11

- Clarify workspace containment requirements for `mod-path` and `config-file` inputs.
- Refresh the README quick-start tag to v1.0.27.

## 1.0.26 - 2026-10-11

- Add an end-to-end CI fixture proving that a `mod-path` outside the checkout is rejected.
- Refresh the README quick-start tag to v1.0.26.

## 1.0.25 - 2026-10-11

- Add an end-to-end CI fixture proving that a workspace config symlink pointing outside the checkout is rejected.
- Refresh the README quick-start tag to v1.0.25.

## 1.0.24 - 2026-10-11

- Add an expected-failure composite Action fixture for a config file outside the checkout.
- Refresh the README quick-start tag to v1.0.24.

## 1.0.23 - 2026-10-11

- Apply workspace confinement to `config-file` as well as `mod-path`; require config files to exist as regular files.
- Extend unit coverage for valid config files and directory rejection.
- Refresh the README quick-start tag to v1.0.23.

## 1.0.22 - 2026-10-11

- Reject absolute, parent-traversal, and symlink-resolved `mod-path` values outside the checked-out workspace.
- Add unit coverage for valid paths, outside paths, and symlink escapes.
- Refresh the README quick-start tag to v1.0.22.

## 1.0.21 - 2026-10-11

- Add an end-to-end expected-failure fixture for the `fail-on-warning` Action input.
- Refresh the README quick-start tag to v1.0.21.

## 1.0.20 - 2026-10-11

- Add an expected-failure composite Action fixture for an out-of-range `max_file_bytes` policy.
- Refresh the README quick-start tag to v1.0.20.

## 1.0.19 - 2026-10-11

- Exercise a synthetic Windows reserved-name ZIP through the composite Action and assert that it blocks release.
- Refresh the README quick-start tag to v1.0.19.

## 1.0.18 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.15.
- Refresh the README quick-start tag to v1.0.18.

## 1.0.17 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.14.
- Refresh the README quick-start tag to v1.0.17.

## 1.0.16 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.13.
- Refresh the README quick-start tag to v1.0.16.

## 1.0.15 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.12.
- Refresh the README quick-start tag to v1.0.15.

## 1.0.14 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.11.
- Refresh the README quick-start tag to v1.0.14.

## 1.0.13 - 2026-10-11

- Pin the default scanner and CI integration fixtures to ModRelease Studio v0.3.10.
- Refresh the README quick-start tag to v1.0.13.

## 1.0.12 - 2026-10-11

- Pin the default scanner and clean/collision CI fixtures to ModRelease Studio v0.3.9.
- Refresh the README quick-start tag to v1.0.12.

## 1.0.11 - 2026-10-11

- Exercise a synthetic case-only path collision through the composite Action and assert that it blocks the run.
- Refresh the quick-start tag to v1.0.11.

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
