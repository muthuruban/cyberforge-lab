"""Implementation for `cyberforge up`."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel

from cyberforge.orchestrator.docker_compose import DockerComposeError, run_compose_up
from cyberforge.orchestrator.scenario_loader import load_scenario_by_id
from cyberforge.safety.policy import ETHICAL_USE_MESSAGE
from cyberforge.safety.validators import SafetyPolicyError, validate_safety_policy

console = Console()


def up_command(
    scenario: str = typer.Option(
        ...,
        "--scenario",
        help="Scenario ID to launch, for example: nrg-staffhub-001",
    )
) -> None:
    """Validate and launch a scenario with Docker Compose."""
    try:
        loaded = load_scenario_by_id(scenario)
        validate_safety_policy(loaded.data)
        run_compose_up(loaded.path.parent)
    except (FileNotFoundError, SafetyPolicyError, DockerComposeError) as exc:
        console.print(f"[red]Failed to start scenario:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    access_url = loaded.data.get("lab", {}).get("access_url", "http://127.0.0.1:8088")
    console.print(
        Panel.fit(
            f"Scenario [bold]{scenario}[/bold] is running.\nAccess URL: [bold]{access_url}[/bold]",
            title="cyberforge up",
            border_style="green",
        )
    )
    console.print(Panel.fit(ETHICAL_USE_MESSAGE, title="Lab-Only Warning", border_style="yellow"))
