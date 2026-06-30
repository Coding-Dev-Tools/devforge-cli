# DevForge CLI

[![GitHub stars](https://img.shields.io/github/stars/Coding-Dev-Tools/devforge?style=social)](https://github.com/Coding-Dev-Tools/devforge/stargazers)

**The `devforge` command — one install, ten developer CLI tools.**

[![PyPI](https://img.shields.io/pypi/v/devforge)](https://pypi.org/project/devforge/)
[![Python Versions](https://img.shields.io/pypi/pyversions/devforge)](https://pypi.org/project/devforge/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Ten production-ready CLI tools for API contracts, SQL generation, infrastructure diffs, config drift, API mocking, key management, env syncing, schema conversion, MCP servers, and dead code removal — in a single package. Install one meta-package and get immediate access to all tools via the unified `devforge` command.

---

[🏠 Landing Page](https://coding-dev-tools.github.io/devforge/) · [📝 Blog](https://coding-dev-tools.github.io/devforge/blog.html) · [🐛 Report a Bug](https://github.com/Coding-Dev-Tools/devforge/issues)

---

## Why the Suite?

Instead of installing ten separate tools and learning ten different CLIs, `pip install devforge[all]` gives you:

- **Single CLI** (`devforge`) to invoke any tool — no context switching
- **Consistent flags, output formats, and help** across all tools
- **Shared configuration** — one install, all tools

## Installation

```bash
# Install everything (recommended)
pip install devforge[all]

# Or install individual tools
pip install devforge[guard]    # API Contract Guardian
pip install devforge[sql]      # json2sql
pip install devforge[deploy]   # DeployDiff
pip install devforge[drift]    # ConfigDrift
pip install devforge[ghost]    # APIGhost
pip install devforge[auth]     # APIAuth
pip install devforge[envault]  # Envault
pip install devforge[schema]   # SchemaForge
pip install devforge[mcp]      # click-to-mcp
pip install devforge[deadcode] # DeadCode
```

## Usage

```bash
devforge --version           # Show version info
devforge tools               # List all available tools
devforge tools guard         # Show details about a specific tool
devforge versions            # Show installed tool versions
```

Run any tool directly through `devforge`:

```bash
# API Contract Guardian — detect OpenAPI breaking changes
devforge guard check spec-v1.yaml spec-v2.yaml

# json2sql — convert JSON to SQL INSERT statements
devforge sql convert data.json --dialect postgres

# DeployDiff — preview infrastructure changes with cost estimates
devforge deploy preview plan.json

# ConfigDrift — catch config drift between environments
devforge drift check dev.yaml prod.yaml

# APIGhost — spawn mock API server from OpenAPI spec
devforge ghost serve openapi.yaml

# APIAuth — generate API keys and JWTs
devforge auth generate --type api-key

# Envault — sync .env files across environments
devforge envault diff .env.dev .env.prod

# SchemaForge — convert between ORM formats
devforge schema convert schema.prisma --to drizzle

# click-to-mcp — wrap CLI as MCP server
devforge mcp wrap my-cli --transport http

# DeadCode — find unused exports in React/Next.js
devforge deadcode scan src/
```

## Tools

| Command | Package | Description |
|---------|---------|-------------|
| `guard` | api-contract-guardian | Detect breaking API changes, generate migration guides, gate CI pipelines on contract violations |
| `sql` | json2sql | Convert JSON datasets to SQL with smart type inference across PostgreSQL, MySQL, and SQLite |
| `deploy` | deploydiff | Preview infra changes with cost estimates and automatic rollback commands for Terraform, CloudFormation, and Pulumi |
| `drift` | configdrift | Compare configs across environments, flag missing keys, deprecated values, and compliance violations |
| `ghost` | apighost | Mock API server from OpenAPI specs with VCR cassette recording and realistic fake data |
| `auth` | apiauth | API key and JWT lifecycle management with AES-256-GCM encrypted local store |
| `envault` | envault | Env variable syncing, diffing, and secret rotation with Vault/AWS SSM/Doppler/1Password support |
| `schema` | schemaforge | Bidirectional ORM schema converter — 11 formats with zero-loss roundtripping |
| `mcp` | click-to-mcp | Auto-wrap any Click/typer CLI as an MCP server — zero code changes |
| `deadcode` | deadcode | Detect unused exports, dead routes, orphaned CSS in TypeScript/React/Next.js projects |

## Links

- [Landing Page](https://coding-dev-tools.github.io/devforge/)
- [GitHub Organization](https://github.com/Coding-Dev-Tools)
- [Report an Issue](https://github.com/Coding-Dev-Tools/devforge/issues)

## License

MIT — see [LICENSE](LICENSE) for details.

## Test

```bash
pytest -q
```
