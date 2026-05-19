"""Entry point for the CyberForge CLI."""

import typer

app = typer.Typer(
    help="CyberForge Lab: local-first, safety-first cybersecurity lab orchestrator.",
    no_args_is_help=True,
)


if __name__ == "__main__":
    app()
