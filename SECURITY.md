# Security Policy

## Supported Versions

Versions that are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| >= 1.0.0 | :white_check_mark: |
| < 1.0.0  | :x:                |

## Reporting a Vulnerability

We appreciate your help in keeping our project secure. If you discover a security vulnerability, please report it responsibly by following these steps:

- Email us directly at imhoteptech@outlook.com.
- Include a detailed description of the vulnerability in your email. This should include steps to reproduce the issue, any relevant code/CLI snippets, and the potential impact of the vulnerability.
- We will acknowledge receipt of your report within 1-3 business days. We will then work to investigate the issue and provide you with an update within 2 more days maximum.
- If the vulnerability is confirmed, we will prioritize a fix and aim to release a security patch within 5 business days for supported versions. We may also choose to disclose the vulnerability publicly after a fix is available.
- We will not disclose your identity without your permission, unless required by law.

## CLI & Execution Security

- `dj-scaffold` runs commands locally to bootstrap projects. Always verify that you are running `dj-scaffold` inside trusted workspace directories.
- We perform regular dependency audits to avoid supply chain vulnerabilities in third-party packages (like `typer`, `questionary`, etc.).
