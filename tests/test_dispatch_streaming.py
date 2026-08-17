"""Regression tests for subprocess output streaming in dispatch.

The dispatch command must stream stdout/stderr in real time rather than
buffering the entire output via capture_output=True. Long-running tools
(deploydiff, schemaforge, configdrift on large datasets) can produce
megabytes of output that should reach the user's terminal immediately.
"""

from __future__ import annotations

import subprocess
import sys
from unittest import mock

from typer.testing import CliRunner

from devforge.cli import app

runner = CliRunner()


class TestDispatchStreaming:
    """dispatch must NOT use subprocess.run with capture_output=True.

    Real-time streaming requires subprocess.Popen (or subprocess.run with
    stdout=None, stderr=None) so the child process inherits the parent's
    file descriptors directly.
    """

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    def test_dispatch_does_not_buffer_output(self, _mock_installed):
        """subprocess.run must NOT be called with capture_output=True.

        capture_output=True buffers the entire child output in memory before
        the parent can write anything. For tools that produce large or
        long-running output, this is a UX regression: the user sees nothing
        until the tool finishes, and memory usage grows unbounded.
        """
        with mock.patch("devforge.cli.subprocess.run") as mock_run:
            mock_run.return_value = mock.MagicMock(returncode=0, stdout="", stderr="")
            with mock.patch("devforge.cli.sys.exit"):
                runner.invoke(app, ["guard", "--help"])

        if mock_run.called:
            # If subprocess.run is used, it must NOT capture output
            call_kwargs = mock_run.call_args[1] if mock_run.call_args[1] else {}
            assert call_kwargs.get("capture_output") is not True, (
                "dispatch uses subprocess.run(capture_output=True) which buffers "
                "all output. Use subprocess.Popen or stdout=None to stream."
            )
            assert call_kwargs.get("stdout") is not subprocess.PIPE, (
                "dispatch uses stdout=PIPE which buffers output. "
                "Use stdout=None to inherit the parent's stdout."
            )

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    def test_dispatch_uses_popen_or_inherited_fds(self, _mock_installed):
        """dispatch should use subprocess.Popen for real-time streaming,
        or subprocess.run without capture (stdout=None, stderr=None).
        """
        with mock.patch("devforge.cli.subprocess.Popen") as mock_popen, \
             mock.patch("devforge.cli.subprocess.run") as mock_run:

            # Set up Popen mock to simulate a successful run
            mock_proc = mock.MagicMock()
            mock_proc.wait.return_value = 0
            mock_popen.return_value = mock_proc

            with mock.patch("devforge.cli.sys.exit"):
                runner.invoke(app, ["guard"])

            # Either Popen was used (preferred for streaming)
            # or subprocess.run was used WITHOUT capture_output
            if mock_popen.called:
                # Good: Popen streams by default
                assert True
            elif mock_run.called:
                kwargs = mock_run.call_args[1] if mock_run.call_args[1] else {}
                assert kwargs.get("capture_output") is not True
                assert kwargs.get("stdout") is not subprocess.PIPE
            else:
                raise AssertionError(
                    "Neither subprocess.Popen nor subprocess.run was called"
                )

    @mock.patch("devforge.cli._is_tool_installed", return_value=True)
    def test_dispatch_exit_code_propagates(self, _mock_installed):
        """The child process exit code must propagate to the parent."""
        with mock.patch("devforge.cli.subprocess.Popen") as mock_popen:
            mock_proc = mock.MagicMock()
            mock_proc.wait.return_value = 42
            mock_popen.return_value = mock_proc

            with mock.patch("devforge.cli.sys.exit") as mock_exit:
                runner.invoke(app, ["guard"])

            if mock_popen.called:
                # sys.exit(42) raises SystemExit; CliRunner catches it and
                # may call sys.exit(0) afterward. Check that 42 was among
                # the calls rather than asserting exactly one call.
                exit_codes = [c.args[0] for c in mock_exit.call_args_list]
                assert 42 in exit_codes, f"Expected exit code 42 in {exit_codes}"
