"""Tests for devforge meta-package."""
from __future__ import annotations

from devforge import TOOLS, __version__
from devforge.cli import app, _is_tool_installed
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
    def test_install_all_uses_all_extra(self, mock_run):
        """'install all' must use the canonical devforge[all] extra, not a comma-joined list."""
        mock_run.return_value = mock.MagicMock(returncode=0, stdout="", stderr="")
        result = runner.invoke(app, ["install", "all"])
        assert result.exit_code == 0
        assert "Successfully" in result.stdout
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]  # positional arg: the command list
        # Must contain "devforge[all]", not "devforge[guard,sql,...]"
        pkg_arg = next((a for a in call_args if a.startswith("devforge[")), None)
        assert pkg_arg == "devforge[all]", f"Expected devforge[all], got {pkg_arg}"

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
        mock_run.return_value = mock.MagicMock(
            returncode=1, stdout="", stderr=""
        )
        result = runner.invoke(app, ["versions", "guard"])
        assert result.exit_code == 0
        assert "guard" in result.stdout
        assert "not installed" in result.stdout


class TestIsToolInstalled:
    def test_builtin_module_is_installed(self):
        """stdlib module should always be found."""
        assert _is_tool_installed("sys") is True

    def test_missing_module_is_not_installed(self):
        """Nonexistent module should return False."""
        assert _is_tool_installed("_devforge_no_such_pkg_xyz") is False


class TestDispatchCommands:
    def test_invalid_tool_subcommand(self):
        """Reject dispatch to an unknown tool subcommand."""
        result = runner.invoke(app, ["nonexistent"])
        assert result.exit_code != 0
        assert "No such command" in result.stdout or "No such command" in result.stderr

    @mock.patch("devforge.cli._is_tool_installed", return_value=False)
    def test_dispatch_not_installed_shows_install_hint(self, _mock):
        """When a tool is not installed, dispatch shows a clear install hint (not a silent exit)."""
        result = runner.invoke(app, ["guard"])
        assert result.exit_code == 1
        assert "not installed" in result.stdout
        assert "pip install devforge[guard]" in result.stdout

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    @mock.patch("devforge.cli.subprocess.run")
    def test_dispatch_installed_tool_runs(self, mock_run, _mock_installed):
        """When a tool is installed, dispatch calls the subprocess."""
        mock_run.return_value = mock.MagicMock(returncode=0)
        with mock.patch("devforge.cli.sys.exit"):
            runner.invoke(app, ["guard"])
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "api_contract_guardian" in cmd


class TestHelp:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tools" in result.stdout
        assert "versions" in result.stdout
        assert "guard" in result.stdout
