"""Implementation for `cyberforge doctor`."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.table import Table

from cyberforge.ai_adapters.claude_adapter import ClaudeAdapter
from cyberforge.ai_adapters.codex_adapter import CodexAdapter
from cyberforge.orchestrator.docker_compose import docker_available, docker_compose_available
from cyberforge.orchestrator.scenario_loader import scenarios_root
from cyberforge.orchestrator.workspace import workspace_exists
from cyberforge.safety.validators import find_ai_credential_exposure

console = Console()


@dataclass(slots=True)
class CheckResult:
    """Represents an environment check result."""

    name: str
    status: str
    detail: str


def _python_check() -> CheckResult:
    major, minor = sys.version_info[:2]
    version = platform.python_version()
    if (major, minor) >= (3, 11):
        return CheckResult("Python version", "PASS", f"{version} (supported)")
    return CheckResult("Python version", "FAIL", f"{version} (requires 3.11+)")


def doctor_command() -> None:
    """Run local environment and safety checks."""
    checks: list[CheckResult] = []
    checks.append(_python_check())

    docker_ok, docker_detail = docker_available()
    checks.append(
        CheckResult(
            "Docker availability",
            "PASS" if docker_ok else "FAIL",
            docker_detail,
        )
    )

    compose_ok, compose_detail = docker_compose_available()
    checks.append(
        CheckResult(
            "Docker Compose availability",
            "PASS" if compose_ok else "FAIL",
            compose_detail,
        )
    )

    scenario_dir = scenarios_root()
    checks.append(
        CheckResult(
            "Scenario directory",
            "PASS" if scenario_dir.is_dir() else "FAIL",
            str(scenario_dir),
        )
    )

    ws_exists = workspace_exists()
    workspace_detail = (
        "Workspace found"
        if ws_exists
        else "Missing .cyberforge-workspace (run `cyberforge init`)"
    )
    checks.append(CheckResult("Workspace", "PASS" if ws_exists else "WARN", workspace_detail))

    codex_status = CodexAdapter().status()
    checks.append(
        CheckResult(
            "Codex CLI",
            "PASS" if codex_status["installed"] else "WARN",
            codex_status["message"],
        )
    )

    claude_status = ClaudeAdapter().status()
    checks.append(
        CheckResult(
            "Claude Code CLI",
            "PASS" if claude_status["installed"] else "WARN",
            claude_status["message"],
        )
    )

    exposures = find_ai_credential_exposure(scenario_dir)
    checks.append(
        CheckResult(
            "AI credential scan (scenario folders)",
            "PASS" if not exposures else "FAIL",
            "No likely AI credential material found"
            if not exposures
            else f"Potential credential material found: {', '.join(exposures)}",
        )
    )

    table = Table(title="CyberForge Doctor Results")
    table.add_column("Check", style="bold")
    table.add_column("Status")
    table.add_column("Detail")

    status_style = {"PASS": "green", "WARN": "yellow", "FAIL": "red"}
    for result in checks:
        styled_status = (
            f"[{status_style[result.status]}]{result.status}[/{status_style[result.status]}]"
        )
        table.add_row(result.name, styled_status, result.detail)

    console.print(table)

    failed = any(result.status == "FAIL" for result in checks)
    if failed:
        raise typer.Exit(code=1)
