# Revenue Holdings CLI

**The `rh` command — one install, four developer CLI tools.**

[![PyPI](https://img.shields.io/pypi/v/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Four production-ready CLI tools for API contracts, SQL generation, infrastructure diffs, and config drift — in a single package. Install one meta-package and get immediate access to all tools via the unified `rh` command.

---

[🏠 Landing Page](https://coding-dev-tools.github.io/revenueholdings.dev/) · [💰 Pricing](https://coding-dev-tools.github.io/revenueholdings.dev/pricing.html) · [📝 Blog](https://coding-dev-tools.github.io/revenueholdings.dev/blog.html) · [🐛 Report a Bug](https://github.com/Coding-Dev-Tools/revenueholdings/issues)

---

## Why the Suite?

Instead of installing four separate tools and learning four different CLIs, `pip install revenueholdings[all]` gives you:

- **Single CLI** (`rh`) to invoke any tool — no context switching
- **Consistent flags, output formats, and help** across all tools
- **Shared license key** — one `REVENUEHOLDINGS_LICENSE_KEY` env var for everything
- **33% cheaper** than buying each tool individually ($39/mo suite vs $58/mo à la carte)

## Installation

```bash
# Install everything (recommended)
pip install revenueholdings[all]

# Or install individual tools
pip install revenueholdings[guard]    # API Contract Guardian
pip install revenueholdings[sql]      # json2sql
pip install revenueholdings[deploy]   # DeployDiff
pip install revenueholdings[drift]    # ConfigDrift
```

## Usage

```bash
rh --version           # Show version info
rh tools               # List all available tools
rh tools guard         # Show details about a specific tool
rh versions            # Show installed tool versions
```

Run any tool directly through `rh`:

```bash
# API Contract Guardian — detect OpenAPI breaking changes
rh guard check spec-v1.yaml spec-v2.yaml

# json2sql — convert JSON to SQL INSERT statements
rh sql convert data.json --dialect postgres

# DeployDiff — preview infrastructure changes with cost estimates
rh deploy preview plan.json

# ConfigDrift — catch config drift between environments
rh drift check dev.yaml prod.yaml
```

## Tools

| Command | Package | Description |
|---------|---------|-------------|
| `guard` | api-contract-guardian | Detect breaking API changes, generate migration guides, gate CI pipelines on contract violations |
| `sql` | json2sql | Convert JSON datasets to SQL with smart type inference across PostgreSQL, MySQL, and SQLite |
| `deploy` | deploydiff | Preview infra changes with cost estimates and automatic rollback commands for Terraform, CloudFormation, and Pulumi |
| `drift` | configdrift | Compare configs across environments, flag missing keys, deprecated values, and compliance violations |

## Pricing

Every tool has a generous free tier (50–1,500 checks/month per tool). Upgrade for CI/CD integration, unlimited usage, and team features.

| Tier | Price | Best For |
|------|-------|----------|
| **Free** | $0 | Hobbyists, OSS — CLI only, rate-limited |
| **Pro (per tool)** | $9–$19/mo | Professional devs needing CI/CD and unlimited usage |
| **Suite (all 4)** | **$39/mo** ($399/yr) | **Save 33%** vs buying individually — full toolkit, one license |
| **Team** | $79/mo | Up to 5 devs — dashboards, alerts, priority support |
| **Enterprise** | Custom | SSO/SAML, RBAC, SLA, on-prem |

> 🔹 One license covers all Revenue Holdings CLI tools. Annual billing saves ~17%.
> 🔹 Full pricing breakdown at [revenueholdings.dev/pricing](https://coding-dev-tools.github.io/revenueholdings.dev/pricing.html)

## Links

- [Landing Page](https://coding-dev-tools.github.io/revenueholdings.dev/)
- [Full Pricing](https://coding-dev-tools.github.io/revenueholdings.dev/pricing.html)
- [GitHub Organization](https://github.com/Coding-Dev-Tools)
- [Report an Issue](https://github.com/Coding-Dev-Tools/revenueholdings/issues)

## License

MIT — see [LICENSE](LICENSE) for details.

---

<sub>Built by [Revenue Holdings](https://coding-dev-tools.github.io/revenueholdings.dev/) — autonomous AI agents generating revenue 24/7.</sub>
