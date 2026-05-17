# Revenue Holdings CLI

[![GitHub stars](https://img.shields.io/github/stars/Coding-Dev-Tools/revenueholdings?style=social)](https://github.com/Coding-Dev-Tools/revenueholdings/stargazers)

**The `rh` command — one install, ten developer CLI tools.**

[![PyPI](https://img.shields.io/pypi/v/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenueholdings)](https://pypi.org/project/revenueholdings/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Ten production-ready CLI tools for API contracts, SQL generation, infrastructure diffs, config drift, API mocking, key management, env syncing, schema conversion, MCP servers, and dead code removal — in a single package. Install one meta-package and get immediate access to all tools via the unified `rh` command.

---

[🏠 Landing Page](https://coding-dev-tools.github.io/revenueholdings.dev/) · [📝 Blog](https://coding-dev-tools.github.io/revenueholdings.dev/blog.html) · [🐛 Report a Bug](https://github.com/Coding-Dev-Tools/revenueholdings/issues)

---

## Why the Suite?

Instead of installing ten separate tools and learning ten different CLIs, `pip install revenueholdings[all]` gives you:

- **Single CLI** (`rh`) to invoke any tool — no context switching
- **Consistent flags, output formats, and help** across all tools
- **Shared configuration** — one install, all tools

## Installation

```bash
# Install everything (recommended)
pip install revenueholdings[all]

# Or install individual tools
pip install revenueholdings[guard]    # API Contract Guardian
pip install revenueholdings[sql]      # json2sql
pip install revenueholdings[deploy]   # DeployDiff
pip install revenueholdings[drift]    # ConfigDrift
pip install revenueholdings[ghost]    # APIGhost
pip install revenueholdings[auth]     # APIAuth
pip install revenueholdings[envault]  # Envault
pip install revenueholdings[schema]   # SchemaForge
pip install revenueholdings[mcp]      # click-to-mcp
pip install revenueholdings[deadcode] # DeadCode
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

# APIGhost — spawn mock API server from OpenAPI spec
rh ghost serve openapi.yaml

# APIAuth — generate API keys and JWTs
rh auth generate --type api-key

# Envault — sync .env files across environments
rh envault diff .env.dev .env.prod

# SchemaForge — convert between ORM formats
rh schema convert schema.prisma --to drizzle

# click-to-mcp — wrap CLI as MCP server
rh mcp wrap my-cli --transport http

# DeadCode — find unused exports in React/Next.js
rh deadcode scan src/
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

- [Landing Page](https://coding-dev-tools.github.io/revenueholdings.dev/)
- [GitHub Organization](https://github.com/Coding-Dev-Tools)
- [Report an Issue](https://github.com/Coding-Dev-Tools/revenueholdings/issues)

## License

MIT — see [LICENSE](LICENSE) for details.

---

<sub>Built by [Revenue Holdings](https://coding-dev-tools.github.io/revenueholdings.dev/) — autonomous AI agents generating revenue 24/7.</sub>