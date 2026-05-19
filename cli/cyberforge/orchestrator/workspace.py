"""Workspace creation and checks."""

from __future__ import annotations

from pathlib import Path

from cyberforge.orchestrator.scenario_loader import find_project_root

WORKSPACE_DIRNAME = ".cyberforge-workspace"
WORKSPACE_SUBDIRS = ("logs", "alerts", "evidence", "reports", "temp")


def workspace_path(project_root: Path | None = None) -> Path:
    """Return the workspace path for the current project."""
    root = project_root or find_project_root()
    return root / WORKSPACE_DIRNAME


def workspace_exists(project_root: Path | None = None) -> bool:
    """Return whether the workspace exists."""
    return workspace_path(project_root).is_dir()


def ensure_workspace(project_root: Path | None = None) -> tuple[Path, list[Path]]:
    """Create workspace folders if needed without overwriting user files."""
    path = workspace_path(project_root)
    created: list[Path] = []

    if path.exists() and not path.is_dir():
        raise RuntimeError(f"Workspace path exists and is not a directory: {path}")

    if not path.exists():
        path.mkdir(parents=True, exist_ok=False)
        created.append(path)

    for dirname in WORKSPACE_SUBDIRS:
        subdir = path / dirname
        if subdir.exists() and not subdir.is_dir():
            raise RuntimeError(f"Workspace entry exists and is not a directory: {subdir}")
        if not subdir.exists():
            subdir.mkdir(parents=False, exist_ok=False)
            created.append(subdir)

    return path, created
