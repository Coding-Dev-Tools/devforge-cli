"""Tests for revenueholdings meta-package."""
from __future__ import annotations

from revenueholdings import TOOLS, __version__
from revenueholdings.cli import app
from typer.testing import CliRunner

runner = CliRunner()


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "revenueholdings" in result.stdout.lower() or "rh" in result.stdout.lower()
        assert __version__ in result.stdout


class TestToolsCommand:
    def test_lists_all_tools(self):
        result = runner.invoke(app, ["tools"])
        assert result.exit_code == 0
        for cmd in TOOLS:
            assert cmd in result.stdout

    def test_show_specific_tool(self):
        result = runner.invoke(app, ["tools", "guard"])
        assert result.exit_code == 0
        assert "guard" in result.stdout
        assert "api-contract-guardian" in result.stdout

    def test_unknown_tool(self):
        result = runner.invoke(app, ["tools", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown" in result.stdout


class TestVersionsCommand:
    def test_versions_runs(self):
        result = runner.invoke(app, ["versions"])
        # Should succeed even if tools aren't installed
        assert result.exit_code == 0


class TestHelp:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tools" in result.stdout
        assert "versions" in result.stdout
        assert "guard" in result.stdout
