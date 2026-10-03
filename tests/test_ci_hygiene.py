"""CI hygiene regression tests.

Ensures workflow files follow security best practices:
- All GitHub Actions are SHA-pinned (no mutable tags like @v4)
- No silent-failure traps (|| true on validation steps)
"""

from __future__ import annotations

import pytest
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"

# Pattern: uses: OWNER/ACTION@REF
# SHA-pinned refs are exactly 40 hex chars.
# Mutable tags look like @v4, @v4.2.2, @main, @release/v1, etc.
USES_PATTERN = re.compile(r"uses:\s*([^@\s]+)@(\S+)")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

# Local/composite actions (e.g. ./.github/actions/foo) don't need SHA pins.
LOCAL_ACTION_PREFIX = "./"


class TestWorkflowHygiene:
    """Regression guards for CI workflow security and correctness."""

    @pytest.fixture
    def workflow_files(self) -> list[Path]:
        files = list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))
        if not files:
            pytest.skip("No workflow files found")
        return files

    def test_all_actions_sha_pinned(self, workflow_files: list[Path]) -> None:
        """Every remote action reference must use a 40-char SHA, not a mutable tag.

        Mutable tags like @v4 can be silently moved to point at different commits,
        creating a supply-chain attack vector. SHA pins lock the exact commit.
        """
        violations: list[str] = []
        for wf in workflow_files:
            for lineno, line in enumerate(wf.read_text(encoding="utf-8").splitlines(), 1):
                match = USES_PATTERN.search(line)
                if not match:
                    continue
                action, ref = match.group(1), match.group(2)
                # Strip inline comments (e.g. "# v4.2.2")
                ref = ref.split("#")[0].strip()
                if action.startswith(LOCAL_ACTION_PREFIX):
                    continue
                if not SHA_PATTERN.match(ref):
                    violations.append(f"{wf.name}:{lineno} {action}@{ref}")

        assert not violations, (
            f"Found {len(violations)} mutable action reference(s). "
            "Pin to a 40-char SHA instead:\n" + "\n".join(violations)
        )

    def test_no_silent_failure_on_validation_steps(self, workflow_files: list[Path]) -> None:
        """Validation/lint/test steps must not suppress failures with '|| true'.

        A step whose purpose is to fail the build on defects (linters, type
        checkers, security scanners) must not hide failures. This catches the
        'validation theater' trap where a real check is neutered.
        """
        validation_keywords = ("lint", "check", "test", "audit", "scan", "format", "typecheck")
        violations: list[str] = []
        for wf in workflow_files:
            lines = wf.read_text(encoding="utf-8").splitlines()
            for lineno, line in enumerate(lines, 1):
                stripped = line.strip()
                if "|| true" not in stripped:
                    continue
                # Check if this line or the step name above contains a validation keyword
                context = " ".join(lines[max(0, lineno - 5) : lineno]).lower()
                if any(kw in context for kw in validation_keywords):
                    violations.append(f"{wf.name}:{lineno} {stripped[:80]}")

        assert not violations, (
            f"Found {len(violations)} validation step(s) with '|| true' suppression. "
            "Remove the suppression so failures are visible:\n" + "\n".join(violations)
        )
