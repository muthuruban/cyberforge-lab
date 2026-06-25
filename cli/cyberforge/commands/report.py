"""Implementation for `cyberforge report` commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cyberforge.orchestrator.reporting import (
    create_report,
    list_reports,
    reports_directory,
    validate_report,
)

report_app = typer.Typer(help="Learner report workflow commands.", no_args_is_help=True)
console = Console()


@report_app.command("create")
def report_create_command(
    scenario: str = typer.Option(
        ...,
        "--scenario",
        help="Scenario ID to create report for, for example: nrg-staffhub-001",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite existing report file for the selected scenario.",
    ),
) -> None:
    """Create a workspace learner report from templates and scenario metadata."""
    try:
        report_path = create_report(scenario, force=force)
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError) as exc:
        console.print(f"[red]Failed to create report:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel.fit(
            f"Report created: [bold]{report_path}[/bold]",
            title="cyberforge report create",
            border_style="green",
        )
    )


def _status_row(report_path: Path) -> tuple[str, str, str]:
    missing = validate_report(report_path)
    if missing:
        return (
            report_path.name,
            "[yellow]needs updates[/yellow]",
            ", ".join(missing),
        )
    return (report_path.name, "[green]ready[/green]", "all required sections present")


@report_app.command("status")
def report_status_command() -> None:
    """Show report files and required-section completeness."""
    report_dir = reports_directory()
    reports = list_reports()

    summary = Table(title="Learner Report Status")
    summary.add_column("Item", style="bold")
    summary.add_column("Value")
    summary.add_row("Reports directory", str(report_dir))
    summary.add_row("Report count", str(len(reports)))
    console.print(summary)

    table = Table(title="Reports")
    table.add_column("File", style="bold")
    table.add_column("Validation")
    table.add_column("Detail")

    if not reports:
        table.add_row(
            "-",
            "[yellow]none[/yellow]",
            "No reports found. Run `cyberforge report create`.",
        )
    else:
        for report in reports:
            file_name, validation, detail = _status_row(report)
            table.add_row(file_name, validation, detail)

    console.print(table)


@report_app.command("validate")
def report_validate_command() -> None:
    """Validate required learner report sections in workspace reports."""
    reports = list_reports()
    if not reports:
        console.print(
            "[red]No reports found to validate.[/red] "
            "Run `cyberforge report create` first."
        )
        raise typer.Exit(code=1)

    table = Table(title="Report Validation")
    table.add_column("File", style="bold")
    table.add_column("Result")
    table.add_column("Missing Sections")

    has_errors = False
    for report in reports:
        missing = validate_report(report)
        if missing:
            has_errors = True
            table.add_row(report.name, "[red]invalid[/red]", ", ".join(missing))
        else:
            table.add_row(report.name, "[green]valid[/green]", "-")

    console.print(table)
    if has_errors:
        raise typer.Exit(code=1)

    console.print(Panel.fit("All reports passed validation.", border_style="green"))
