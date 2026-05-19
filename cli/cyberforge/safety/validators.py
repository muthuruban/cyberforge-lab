"""Scenario safety validators."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from cyberforge.safety.policy import is_allowed_domain

_REQUIRED_SAFETY_KEYS = {"lab_only", "allowed_domains", "allowed_targets", "internet_access"}
_KEY_PATTERNS = [
    re.compile(r"OPENAI_API_KEY", re.IGNORECASE),
    re.compile(r"ANTHROPIC_API_KEY", re.IGNORECASE),
    re.compile(r"AZURE_OPENAI_API_KEY", re.IGNORECASE),
]
_TEXT_EXTENSIONS = {
    ".env",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".cfg",
    ".conf",
    ".ini",
    ".md",
    ".py",
}


class SafetyPolicyError(ValueError):
    """Raised when a scenario safety policy fails validation."""


def validate_safety_policy(scenario: dict[str, Any]) -> None:
    """Validate required safety controls for scenario startup."""
    safety = scenario.get("safety")
    if not isinstance(safety, dict):
        raise SafetyPolicyError("Scenario is missing a valid 'safety' section")

    missing = _REQUIRED_SAFETY_KEYS - set(safety.keys())
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise SafetyPolicyError(f"Scenario safety section is missing keys: {missing_text}")

    if safety.get("lab_only") is not True:
        raise SafetyPolicyError("Scenario startup blocked: safety.lab_only must be true")

    if safety.get("internet_access") is not False:
        raise SafetyPolicyError(
            "Scenario startup blocked: safety.internet_access must be false in Phase 1"
        )

    allowed_domains = safety.get("allowed_domains")
    if not isinstance(allowed_domains, list) or not allowed_domains:
        raise SafetyPolicyError("safety.allowed_domains must be a non-empty list")

    invalid_domains = [value for value in allowed_domains if not is_allowed_domain(str(value))]
    if invalid_domains:
        invalid_text = ", ".join(invalid_domains)
        raise SafetyPolicyError(
            "Scenario startup blocked: invalid safety.allowed_domains entries: "
            f"{invalid_text}. Use only .test, localhost, or internal Docker service names."
        )

    allowed_targets = safety.get("allowed_targets")
    if not isinstance(allowed_targets, list) or not allowed_targets:
        raise SafetyPolicyError("safety.allowed_targets must be a non-empty list")


def find_ai_credential_exposure(scenarios_root: Path) -> list[str]:
    """Detect likely AI credential material in scenario folders."""
    exposures: list[str] = []
    if not scenarios_root.exists():
        return exposures

    for file_path in scenarios_root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.stat().st_size > 1_000_000:
            continue
        if file_path.suffix.lower() not in _TEXT_EXTENSIONS and file_path.name != ".env":
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        if any(pattern.search(content) for pattern in _KEY_PATTERNS):
            exposures.append(str(file_path))

    return exposures
