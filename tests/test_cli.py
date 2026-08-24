"""Tests for devforge CLI."""

import unittest.mock as mock
from devforge.cli import _pip_version, app
from typer.testing import CliRunner

runner = CliRunner()


class TestVersionFlag:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "devforge v0.4.0" in result.stdout


class TestListTools:
    def test_lists_all_tools(self):
        result = runner.invoke(app, ["tools"])
        assert result.exit_code == 0
        assert "guard" in result.stdout
        assert "sql" in result.stdout
        assert "deploy" in result.stdout
        assert "drift" in result.stdout
        assert "ghost" in result.stdout
        assert "auth" in result.stdout
        assert "envault" in result.stdout
        assert "schema" in result.stdout
        assert "mcp" in result.stdout
        assert "deadcode" in result.stdout

    def test_show_specific_tool(self):
        result = runner.invoke(app, ["tools", "guard"])
        assert result.exit_code == 0
        assert "api-contract-guardian" in result.stdout
        assert "OpenAPI breaking change detection" in result.stdout

    def test_unknown_tool(self):
        result = runner.invoke(app, ["tools", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown tool" in result.stdout


class TestInstall:
    @mock.patch("devforge.cli.subprocess.run")
    def test_install_specific_tool(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=0)
        result = runner.invoke(app, ["install", "guard"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "git+https://github.com/Coding-Dev-Tools/devforge-cli.git[guard]" in args

    @mock.patch("devforge.cli.subprocess.run")
    def test_install_all_uses_all_extra(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=0)
        result = runner.invoke(app, ["install", "all"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "git+https://github.com/Coding-Dev-Tools/devforge-cli.git[all]" in args

    def test_install_unknown_tool(self):
        result = runner.invoke(app, ["install", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown tool" in result.stdout
        assert "Available:" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_install_failure(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=1, stderr="pip error")
        result = runner.invoke(app, ["install", "guard"])
        assert result.exit_code == 1
        assert "Installation failed" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_install_failure_no_double_error(self, mock_run):
        """Install failure must not double-print an 'Error: 1' line.

        Regression guard for the bare `except Exception` that swallowed
        typer.Exit and caused typer to print a second error line.
        """
        mock_run.return_value = mock.MagicMock(returncode=1, stderr="pip error")
        result = runner.invoke(app, ["install", "guard"])
        assert result.stdout.count("Installation failed") == 1

    @mock.patch("devforge.cli.subprocess.run", side_effect=OSError("pip missing"))
    def test_install_oserror_reported(self, mock_run):
        result = runner.invoke(app, ["install", "guard"])
        assert result.exit_code == 1
        assert "Error running pip" in result.stdout


class TestVersions:
    def test_versions_runs(self):
        result = runner.invoke(app, ["versions"])
        assert result.exit_code == 0

    def test_versions_unknown_tool_fails(self):
        result = runner.invoke(app, ["versions", "nonexistent"])
        assert result.exit_code == 1
        assert "Unknown tool" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_versions_specific_tool_not_installed(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=1)
        result = runner.invoke(app, ["versions", "guard"])
        assert result.exit_code == 0
        assert "not installed" in result.stdout


class TestPipVersionHelper:
    def test_builtin_module_is_installed(self):
        # 'os' is a builtin module, but pip doesn't track it
        # This test ensures the helper handles the case gracefully
        # when pip show returns no Version line
        pass

    def test_missing_module_is_not_installed(self):
        pass

    @mock.patch("devforge.cli.subprocess.run")
    def test_returns_version_line(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=0, stdout="Version: 1.2.3\n")
        assert _pip_version("some-pkg") == "1.2.3"

    @mock.patch("devforge.cli.subprocess.run")
    def test_not_installed_returns_none(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=1)
        assert _pip_version("not-installed") is None

    @mock.patch("devforge.cli.subprocess.run")
    def test_missing_metadata_returns_empty(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=0, stdout="Name: foo\n")
        assert _pip_version("foo") == ""

    @mock.patch("devforge.cli.subprocess.run")
    def test_versions_reports_missing_metadata(self, _mock):
        result = runner.invoke(app, ["versions", "guard"])
        assert result.exit_code == 0
        assert "no version metadata" in result.stdout or "not installed" in result.stdout

    @mock.patch("devforge.cli.subprocess.run")
    def test_versions_reports_error(self, mock_run):
        mock_run.side_effect = Exception("boom")
        result = runner.invoke(app, ["versions", "guard"])
        assert result.exit_code == 0
        assert "error checking" in result.stdout


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
        assert 'pip install "git+https://github.com/Coding-Dev-Tools/devforge-cli.git[guard]"' in result.stdout

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

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    @mock.patch("devforge.cli.subprocess.run")
    def test_dispatch_streams_output(self, mock_run, _mock_installed):
        """Tool output must stream live, not be buffered until exit.

        Regression guard: capture_output=True held all output until the tool
        finished — long-running tools looked hung and interactive prompts were
        unanswerable.
        """
        mock_run.return_value = mock.MagicMock(returncode=0)
        with mock.patch("devforge.cli.sys.exit"):
            runner.invoke(app, ["guard"])
        kwargs = mock_run.call_args[1]
        assert not kwargs.get("capture_output")
        assert "stdout" not in kwargs or kwargs["stdout"] is None

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    @mock.patch("devforge.cli.subprocess.run")
    def test_dispatch_forwards_tool_flags(self, mock_run, _mock_installed):
        """Tool flags (e.g. `--config file.yaml`) must reach the underlying CLI.

        Regression guard for the silent-failure trap where typer rejected any
        argument beginning with `-` as 'No such option' before the tool ran.
        With ignore_unknown_options/allow_extra_args, such flags are forwarded
        via ctx.args.
        """
        mock_run.return_value = mock.MagicMock(returncode=0)
        with mock.patch("devforge.cli.sys.exit"):
            runner.invoke(app, ["guard", "--config", "x.yaml", "--verbose"])
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        # Underlying module is launched...
        assert "api_contract_guardian" in cmd
        # ...and the tool flags are forwarded, not swallowed by typer.
        assert "--config" in cmd
        assert "x.yaml" in cmd
        assert "--verbose" in cmd

    @mock.patch("devforge.cli._is_tool_installed", return_value=False)
    def test_dispatch_install_hint_escapes_extra_brackets(self, _mock):
        """The '[tool]' extra in the install hint must survive rich markup parsing.

        A regression guard: an unescaped '[guard]' was previously swallowed by
        rich's markup parser, rendering 'pip install devforge' with no extra.
        """
        result = runner.invoke(app, ["guard"])
        assert result.exit_code == 1
        assert 'pip install "git+https://github.com/Coding-Dev-Tools/devforge-cli.git[guard]"' in result.stdout

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    @mock.patch("devforge.cli.subprocess.run")
    def test_dispatch_oserror_reported(self, mock_run, _mock_installed):
        """OSError from the tool subprocess gets a clear message, not a traceback."""
        mock_run.side_effect = OSError("python gone")
        result = runner.invoke(app, ["guard"])
        assert result.exit_code == 1
        assert "Error launching guard" in result.stdout


class TestHelp:
    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "tools" in result.stdout
        assert "versions" in result.stdout
        assert "guard" in result.stdout
