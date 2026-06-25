"""Base class for AI adapter status checks."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class BaseAIAdapter:
    """Base adapter used for installation and status checks only."""

    provider_name: str = "unknown"
    binary_name: str = ""

    # Future behavior:
    # - AI execution should run on host or dedicated AI runner.
    # - AI should read only workspace files selected by policy.
    # - AI credentials must never be placed in vulnerable containers or VMs.

    def is_installed(self) -> bool:
        """Return True if the adapter CLI binary is available."""
        return shutil.which(self.binary_name) is not None

    def run_command(
        self,
        args: list[str],
        cwd: Path | None = None,
        timeout_seconds: int = 10,
    ) -> subprocess.CompletedProcess[str]:
        """Run a local host command safely for status checks."""
        return subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )

    def status(self) -> dict[str, str | bool]:
        """Return structured adapter status."""
        installed = self.is_installed()
        return {
            "provider": self.provider_name,
            "installed": installed,
            "message": (
                f"{self.binary_name} detected in PATH"
                if installed
                else f"{self.binary_name} not found in PATH"
            ),
        }
