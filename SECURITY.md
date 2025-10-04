# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in brain-trust, please email us at
security@brain-trust.dev. We take all reports seriously and will respond as
quickly as possible.

Please include:

- A clear description of the issue
- Steps to reproduce
- Affected versions/commit
- Any relevant logs or screenshots

Please do not create a public GitHub issue for security vulnerabilities.

## Supported Versions

We currently support the latest minor release series:

| Version | Supported    |
| ------- | ------------ |
| 0.1.x   | ✅ Supported |

## Security Best Practices

- Do not commit secrets or API keys to the repository
- Use environment variables for all sensitive configuration
- Keep dependencies up to date
- Use non-root users in containers
- Validate all inputs to tools

## Disclosure Policy

We follow a responsible disclosure policy. Once a fix is available, we will:

- Acknowledge the reporter (if desired)
- Publish a security advisory
- Release a patched version
- Update documentation as needed
