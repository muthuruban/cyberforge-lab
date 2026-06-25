"""Implementation for `cyberforge ai` commands."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cyberforge.ai_adapters.claude_adapter import ClaudeAdapter
from cyberforge.ai_adapters.codex_adapter import CodexAdapter

ai_app = typer.Typer(help="AI adapter commands for host-side integration.", no_args_is_help=True)
console = Console()


@ai_app.command("status")
def ai_status_command() -> None:
    """Show host-only AI adapter status checks (no model calls)."""
    adapters = [CodexAdapter(), ClaudeAdapter()]

    table = Table(title="AI Adapter Status")
    table.add_column("Provider", style="bold")
    table.add_column("Installed")
    table.add_column("Authentication")
    table.add_column("Detail")

    for adapter in adapters:
        status = adapter.status()
        installed = "yes" if status["installed"] else "no"
        install_color = "green" if status["installed"] else "yellow"

        auth_display = "not checked"
        auth_color = "yellow"
        if adapter.provider_name == "Codex CLI":
            auth_state = str(status.get("auth_state", "unknown"))
            if auth_state == "authenticated":
                auth_display = "appears authenticated"
                auth_color = "green"
            elif auth_state == "unauthenticated":
                auth_display = "appears unauthenticated"
                auth_color = "yellow"
            elif auth_state == "unknown":
                auth_display = "unable to confirm"
                auth_color = "yellow"

        detail = str(status.get("auth_message", status["message"]))
        table.add_row(
            str(status["provider"]),
            f"[{install_color}]{installed}[/{install_color}]",
            f"[{auth_color}]{auth_display}[/{auth_color}]",
            detail,
        )

    console.print(table)
    console.print(
        Panel.fit(
            "AI support is host-side only in this phase.\n"
            "Only CLI installation/authentication status checks are executed.\n"
            "No AI model calls are executed.\n"
            "Credentials must never be placed inside vulnerable containers or scenario files.",
            title="AI Safety Note",
            border_style="yellow",
        )
    )
