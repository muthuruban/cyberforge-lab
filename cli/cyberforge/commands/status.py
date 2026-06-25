"""Implementation for `cyberforge status`."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from cyberforge.orchestrator.docker_compose import docker_available, is_scenario_running
from cyberforge.orchestrator.scenario_loader import list_scenario_packs, list_scenarios
from cyberforge.orchestrator.workspace import workspace_exists, workspace_path

console = Console()


def status_command() -> None:
    """Show current CyberForge workspace and scenario status."""
    packs = list_scenario_packs()
    scenarios = list_scenarios()
    docker_ok, docker_detail = docker_available()

    summary = Table(title="CyberForge Status")
    summary.add_column("Item", style="bold")
    summary.add_column("Value")
    summary.add_row("Workspace path", str(workspace_path()))
    summary.add_row("Workspace exists", "yes" if workspace_exists() else "no")
    summary.add_row("Docker", "available" if docker_ok else f"unavailable ({docker_detail})")
    summary.add_row("Scenario packs", ", ".join(packs) if packs else "none")
    scenario_ids = ", ".join(scenario["id"] for scenario in scenarios) if scenarios else "none"
    summary.add_row("Available scenarios", scenario_ids)
    console.print(summary)

    running = []
    if docker_ok:
        for scenario in scenarios:
            scenario_path = scenario["path"]
            if is_scenario_running(scenario_path):
                running.append(scenario["id"])

    running_table = Table(title="Lab Runtime")
    running_table.add_column("Runtime Signal", style="bold")
    running_table.add_column("Status")
    running_table.add_row(
        "Detected running labs",
        ", ".join(running) if running else "none detected",
    )
    console.print(running_table)
