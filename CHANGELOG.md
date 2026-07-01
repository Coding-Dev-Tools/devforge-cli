# Changelog

All notable changes to Revenue Holdings CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-06-30

### Added
- Python 3.13 to CI test matrix
- Formatting check step in CI workflow
- `format-check` Makefile target

### Changed
- Makefile lint/format targets scoped to `src/ tests/` instead of entire repo

## [0.2.0] - 2026-05-17

### Added
- Support for all 10 CLI tools (previously only 4)
- New tool subcommands: ghost, auth, envault, schema, mcp, deadcode
- CI/CD workflows for testing and PyPI publishing
- Comprehensive .gitignore

### Changed
- Updated tool registry to include all 10 tools
- Made revenueholdings-license an optional dependency
- Standardized pyproject.toml across all repos

## [0.1.0] - 2026-05-14

### Added
- Initial release with 4 tools: guard, sql, deploy, drift
- Unified `rh` CLI entry point
- Tool dispatching via subprocess