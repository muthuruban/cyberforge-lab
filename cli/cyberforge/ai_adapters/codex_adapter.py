"""Codex CLI adapter placeholder."""

from __future__ import annotations

import re
import subprocess

from cyberforge.ai_adapters.base import BaseAIAdapter


class CodexAdapter(BaseAIAdapter):
    """Adapter placeholder for Codex CLI host integration."""

    provider_name = "Codex CLI"
    binary_name = "codex"

    _AUTHENTICATED_PATTERNS = (
        re.compile(r"\b(authenticated|logged in|login active|active session)\b", re.IGNORECASE),
    )
    _UNAUTHENTICATED_PATTERNS = (
        re.compile(
            r"\b(not authenticated|not logged in|login required|unauthenticated)\b",
            re.IGNORECASE,
        ),
    )

    def login_status(self) -> dict[str, str | bool]:
        """Check whether Codex appears authenticated without model execution."""
        if not self.is_installed():
            return {
                "checked": False,
                "authenticated": False,
                "auth_state": "not_checked",
                "message": "codex not found in PATH",
            }

        try:
            result = self.run_command(["codex", "login", "status"], timeout_seconds=10)
        except subprocess.TimeoutExpired:
            return {
                "checked": True,
                "authenticated": False,
                "auth_state": "unknown",
                "message": "codex login status timed out",
            }
        except OSError as exc:
            return {
                "checked": True,
                "authenticated": False,
                "auth_state": "unknown",
                "message": f"codex login status failed: {exc}",
            }

        output = "\n".join(
            part.strip() for part in (result.stdout, result.stderr) if part and part.strip()
        )
        normalized = output.lower()

        for pattern in self._UNAUTHENTICATED_PATTERNS:
            if pattern.search(normalized):
                return {
                    "checked": True,
                    "authenticated": False,
                    "auth_state": "unauthenticated",
                    "message": "Codex appears unauthenticated",
                }

        for pattern in self._AUTHENTICATED_PATTERNS:
            if pattern.search(normalized):
                return {
                    "checked": True,
                    "authenticated": True,
                    "auth_state": "authenticated",
                    "message": "Codex appears authenticated",
                }

        if result.returncode == 0:
            return {
                "checked": True,
                "authenticated": True,
                "auth_state": "authenticated",
                "message": "Codex login status completed (authentication appears available)",
            }

        return {
            "checked": True,
            "authenticated": False,
            "auth_state": "unknown",
            "message": "Codex authentication status could not be confirmed",
        }

    def status(self) -> dict[str, str | bool]:
        """Return codex installation and login-status summary."""
        base = super().status()
        login = self.login_status()
        base["auth_checked"] = login["checked"]
        base["authenticated"] = login["authenticated"]
        base["auth_state"] = login["auth_state"]
        base["auth_message"] = login["message"]
        return base

    # Future commands may include:
    # - cyberforge ai hint
    # - cyberforge ai soc-review
    # - cyberforge ai review-report
