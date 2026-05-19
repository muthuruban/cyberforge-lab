"""Implementation for `cyberforge init`."""

from rich.console import Console
from rich.panel import Panel

from cyberforge.orchestrator.workspace import ensure_workspace

console = Console()


def init_command() -> None:
    """Create the local CyberForge workspace if needed."""
    workspace_path, created_paths = ensure_workspace()

    if created_paths:
        created = "\n".join(f"- {path.name}" for path in created_paths)
        message = (
            f"Workspace ready at: [bold]{workspace_path}[/bold]\n"
            "Created folders:\n"
            f"{created}"
        )
    else:
        message = f"Workspace already present at: [bold]{workspace_path}[/bold]"

    console.print(Panel.fit(message, title="cyberforge init", border_style="green"))
