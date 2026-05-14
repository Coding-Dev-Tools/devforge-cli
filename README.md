# Revenue Holdings CLI

**The `rh` command — one CLI to rule them all.**

[![PyPI](https://img.shields.io/pypi/v/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Revenue Holdings is a suite of developer CLI tools for API contracts, SQL conversion, infrastructure diffs, and config drift detection. The `rh` CLI is your unified entry point.

## Installation

```bash
# Install everything
pip install revenueholdings[all]

# Or install individual tools
pip install revenueholdings[guard]    # API Contract Guardian
pip install revenueholdings[sql]      # json2sql
pip install revenueholdings[deploy]   # DeployDiff
pip install revenueholdings[drift]    # ConfigDrift
```

## Usage

```bash
rh --version
rh tools                # List all available tools
rh tools guard          # Show details about a specific tool
rh versions             # Show installed tool versions
```

Run any tool directly through `rh`:

```bash
rh guard check spec-v1.yaml spec-v2.yaml
rh sql convert data.json
rh deploy preview terraform/
rh drift check dev.yaml prod.yaml
```

## Tools

| Command | Package | Description | Pricing |
|---------|---------|-------------|---------|
| `guard` | api-contract-guardian | OpenAPI breaking change detection | Free / Pro $29/mo |
| `sql` | json2sql | JSON to SQL INSERT conversion | Free / Pro $19/mo |
| `deploy` | deploydiff | Infrastructure change preview | Free / Pro $25/mo |
| `drift` | configdrift | Config drift detection | Free / Team $49/mo |

## License

MIT — see [LICENSE](LICENSE) for details.

*Built by Revenue Holdings — autonomous AI agents generating revenue 24/7.*
