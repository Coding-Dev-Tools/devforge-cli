# devforge-cli

## Purpose
DevForge CLI meta-package that installs all 11 developer tools in one command. Provides a unified `devforge` CLI entry point delegating to sub-tools: api-contract-guardian, json2sql, deploydiff, configdrift, apighost, apiauth, envault, schemaforge, click-to-mcp, and deadcode.

## Build & Test Commands
- Install: `pip install -e .[all]` or `pip install devforge`
- Install all tools: `pip install devforge[all]`
- Test: `pytest tests/` (or `python -m pytest tests/ -v --tb=short`)
- Lint: `ruff check .`
- Build: `pip install build twine && python -m build && twine check dist/*`
- CLI check: `devforge --help`

## Architecture
Key directories:
- `src/devforge/` — Main package (CLI dispatcher, version management)
- `tests/` — Test suite
- `.github/workflows/` — CI/CD pipelines

## Conventions
- Language: Python 3.10+
- Test framework: pytest
- Linting: ruff
- Build system: setuptools with src/ layout
- CLI entry point: `devforge.cli:app`
- Optional dependency groups: guard, sql, deploy, drift, ghost, auth, envault, schema, mcp, deadcode, all
- Default branch: main
