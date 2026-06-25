"""Safety policy constants and helpers."""

from __future__ import annotations

import re

ETHICAL_USE_MESSAGE = (
    "Lab-only environment. Do not target public systems. "
    "Do not perform unauthorised testing. Use only fictional, isolated scenarios."
)

_DOCKER_SERVICE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def is_allowed_domain(value: str) -> bool:
    """Validate allowed domain entries for Phase 1."""
    domain = value.strip().lower()
    if domain == "localhost":
        return True
    if domain.endswith(".test"):
        return True
    if _DOCKER_SERVICE_PATTERN.fullmatch(domain):
        return True
    return False
