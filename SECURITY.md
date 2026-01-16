# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **Do not** open a public GitHub issue
2. Email the maintainers directly or open a [GitHub Security Advisory](https://github.com/your-org/roxxane/security/advisories/new)
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt of your report within 48 hours and provide an update on the status of the vulnerability within 7 days.

## Security Best Practices

When using this project:

- Keep dependencies up to date
- Review and rotate AWS credentials regularly
- Use least-privilege IAM policies
- Enable CloudWatch logging and monitoring
- Review security scan results from CI/CD pipelines
- Never commit credentials or secrets to the repository

## Security Scanning

This project uses automated security scanning:

- **GitHub Dependabot** - Weekly dependency updates
- **CodeQL** - Static analysis on every push
- **Bandit** - Python security linting
- **Safety** - Dependency vulnerability checks

All security checks must pass before code can be merged.
