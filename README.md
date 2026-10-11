# ModRelease Gate

**Run ModRelease Studio in GitHub Actions for every mod pull request.** Get workflow annotations for blocking and advisory findings, a Markdown job summary, and downloadable JSON/Markdown reports.

[![CI](https://github.com/GhosTnever-lkm/modrelease-studio-action/actions/workflows/ci.yml/badge.svg)](https://github.com/GhosTnever-lkm/modrelease-studio-action/actions/workflows/ci.yml) · [![Version](https://img.shields.io/github/v/release/GhosTnever-lkm/modrelease-studio-action?sort=semver)](https://github.com/GhosTnever-lkm/modrelease-studio-action/releases/latest) · [MIT License](LICENSE)

ModRelease Gate is a small composite action around the existing [ModRelease Studio](https://github.com/GhosTnever-lkm/modrelease-studio) scanner. It does not comment on pull requests through the API, modify the checked-out mod, or upload source files. It uploads only the generated reports as a workflow artifact.

## Quick start

Add this workflow to the mod repository as `.github/workflows/modrelease.yml`:

```yaml
name: Mod release preflight

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  preflight:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: GhosTnever-lkm/modrelease-studio-action@v1.0.10
        with:
          mod-path: .
          tool-version: v0.3.8
```

The consumer workflow must check out its mod repository first. The action installs the scanner from its exact tagged GitHub source; it never runs `pip install .` in the consumer project.

### Use a project-specific release policy

Create a `modrelease.toml` file in the checked-out mod repository and pass its workspace-relative path with `config-file`. ModRelease Studio v0.3.8 supports required path globs and ERROR/WARNING/INFO severity; an ERROR-level missing path fails the scan. The action CI exercises this integration using [`examples/policy-project`](examples/policy-project).

```yaml
- uses: GhosTnever-lkm/modrelease-studio-action@v1.0.10
  with:
    mod-path: .
    config-file: modrelease.toml
    tool-version: v0.3.8
```

Example policy:

```toml
[scan]
required_paths = ["descriptor.mod", "README.md"]
required_paths_severity = "ERROR"
```

## Inputs

| Input | Default | Purpose |
|---|---|---|
| `mod-path` | `.` | Mod folder or ZIP path relative to the checked-out workspace. |
| `config-file` | empty | Optional TOML configuration path relative to the checked-out workspace. |
| `tool-version` | `v0.3.8` | Exact scanner tag, such as `v0.3.8`. |
| `python-version` | `3.12` | Python runtime. |
| `artifact-name` | `modrelease-report` | Name of the uploaded reports artifact. |
| `fail-on-warning` | `false` | Also fail the workflow when advisory warnings exist. Errors always fail the scan. |

The `tool-version` input accepts a strict `major.minor.patch` tag, with an optional leading `v`. The action pins its helper actions to major releases. GitHub-hosted runners are recommended; self-hosted runners need support for the Node runtime used by the referenced Actions.

## What the workflow receives

- **Annotations:** up to 50 findings per run, mapped to GitHub error, warning, and notice annotations.
- **Job summary:** finding counts and a compact Markdown table.
- **Artifact:** `modrelease-report.md` and `modrelease-report.json`, available even when the scan reports blocking findings.
- **Outputs:** runner paths to the JSON and Markdown reports (`steps.<id>.outputs.json-report` and `markdown-report`).

Annotation fields are escaped using GitHub's workflow-command encoding, and untrusted file paths are escaped in Markdown. The scanner's messages do not include detected credential values. The workflow artifact includes the scanner's file manifest and paths; artifact access follows the mod repository's Actions permissions and retention policy.

## Development

The action and its annotation formatter use only Python's standard library.

```console
python -m unittest discover -s tests -v
```

The fixture in `examples/findings.sample.json` contains placeholder paths and generic messages only; it does not contain real credentials or game files.

## ☕ Support

ModRelease Gate is free and open source. Support the author through [Buy Me a Coffee](https://buymeacoffee.com/azizazimov8), [Boosty](https://boosty.to/azizazimov), or [GitHub Sponsors](https://github.com/sponsors/GhosTnever-lkm).

## License

MIT. See [LICENSE](LICENSE).
