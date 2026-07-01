"""Tests for devforge meta-package."""

from __future__ import annotations

from devforge import TOOLS, __version__
from devforge.cli import app
from typer.testing import CliRunner
from unittest import mock

runner = CliRunner()


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "devforge" in result.stdout.lower()
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


class TestInstallCommand:
    @mock.patch("devforge.cli.subprocess.run")
    def test_install_specific_tool(self, mock_run):
        """Install a specific tool by name."""
        mock_run.return_value = mock.MagicMock(returncode=0, stdout="", stderr="")
        result = runner.invoke(app, ["install", "guard"])
        assert result.exit_code == 0
        assert "Successfully" in result.stdout
        mock_run.assert_called_once()

    @mock.patch("devforge.cli.subprocess.run")
    def test_install_all(self, mock_run):
        """Install all tools via the 'all' alias."""
        mock_run.return_value = mock.MagicMock(returncode=0, stdout="", stderr="")
        result = runner.invoke(app, ["install", "all"])
        assert result.exit_code == 0
        assert "Successfully" in result.stdout
        mock_run.assert_called_once()

    def test_install_unknown_tool(self):
        """Error on unknown tool name."""
        result = runner.invoke(app, ["install", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown" in result.stdout
        assert "Available:" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_install_failure(self, mock_run):
        """Handle pip install failure gracefully."""
        mock_run.return_value = mock.MagicMock(returncode=1, stdout="", stderr="Error message")
        result = runner.invoke(app, ["install", "guard"])
        assert result.exit_code == 1
        assert "failed" in result.stdout.lower()


class TestVersionsCommand:
    def test_versions_runs(self):
        """List all tool versions without error."""
        result = runner.invoke(app, ["versions"])
        assert result.exit_code == 0

    def test_versions_unknown_tool_fails(self):
        """Error on unknown tool name."""
        result = runner.invoke(app, ["versions", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_versions_specific_tool_not_installed(self, mock_run):
        """Show 'not installed' for a tool that isn't installed."""
        mock_run.return_value = mock.MagicMock(returncode=1, stdout="", stderr="")
        result = runner.invoke(app, ["versions", "guard"])
        assert result.exit_code == 0
        assert "guard" in result.stdout
        assert "not installed" in result.stdout


class TestDispatchCommands:
    def test_invalid_tool_subcommand(self):
        """Reject dispatch to an unknown tool subcommand."""
        result = runner.invoke(app, ["nonexistent"])
        # typer outputs error to stderr, not stdout
        assert result.exit_code != 0
        assert "No such command" in result.stdout or "No such command" in result.stderr


class TestHelp:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tools" in result.stdout
        assert "versions" in result.stdout
        assert "guard" in result.stdout
