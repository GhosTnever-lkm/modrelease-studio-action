# Security

## Scope and handling

ModRelease Gate reads the checked-out mod path through ModRelease Studio. It does not execute mod files, alter the source tree, create pull-request comments through an API, or send files to an external service. The workflow uploads JSON and Markdown scan reports as a GitHub Actions artifact. These reports can contain file names, paths, sizes, and the build fingerprint; protect artifact access through repository permissions and retention settings.

The scanner intentionally does not include detected credential values in findings. The annotation formatter treats report paths and messages as untrusted: it escapes workflow-command delimiters and Markdown special characters before publishing them.

## Reporting a vulnerability

Please report security issues privately through GitHub's **Report a vulnerability** feature on this repository. Do not open a public issue containing credentials, private source, or an exploit against another repository.

Never put real credentials in tests, issues, workflow logs, or example reports. Use synthetic values only.
