"""Implementation for `cyberforge down`."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel

from cyberforge.orchestrator.docker_compose import DockerComposeError, run_compose_down
from cyberforge.orchestrator.scenario_loader import load_scenario_by_id

console = Console()


def down_command(
    scenario: str = typer.Option(
        ...,
        "--scenario",
        help="Scenario ID to stop, for example: nrg-staffhub-001",
    )
) -> None:
    """Stop a running scenario with safe defaults."""
    try:
        loaded = load_scenario_by_id(scenario)
        run_compose_down(loaded.path.parent)
    except (FileNotFoundError, DockerComposeError) as exc:
        console.print(f"[red]Failed to stop scenario:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel.fit(
            "Scenario stopped.\n"
            "The lab URL will refuse connections until you run `cyberforge up` again.\n"
            "Reports and evidence directories were not deleted.",
            title="cyberforge down",
            border_style="green",
        )
    )
