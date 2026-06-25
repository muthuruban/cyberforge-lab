"""Scenario discovery and YAML loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class LoadedScenario:
    """Loaded scenario descriptor."""

    path: Path
    data: dict[str, Any]


def find_project_root(start: Path | None = None) -> Path:
    """Find the CyberForge project root by locating pyproject.toml and scenarios/."""
    probe = (start or Path.cwd()).resolve()
    for candidate in [probe, *probe.parents]:
        if (candidate / "pyproject.toml").is_file() and (candidate / "scenarios").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate project root with pyproject.toml and scenarios/")


def scenarios_root(project_root: Path | None = None) -> Path:
    """Return the scenarios directory."""
    return (project_root or find_project_root()) / "scenarios"


def discover_scenario_files(project_root: Path | None = None) -> list[Path]:
    """Return all scenario.yml files under the scenarios folder."""
    root = scenarios_root(project_root)
    return sorted(root.glob("*/*/scenario.yml"))


def load_scenario(scenario_file: Path) -> LoadedScenario:
    """Load a scenario YAML file into a dictionary."""
    if not scenario_file.is_file():
        raise FileNotFoundError(f"Scenario file does not exist: {scenario_file}")

    with scenario_file.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Scenario YAML must produce an object: {scenario_file}")

    return LoadedScenario(path=scenario_file, data=data)


def load_scenario_by_id(scenario_id: str, project_root: Path | None = None) -> LoadedScenario:
    """Load scenario metadata by scenario ID."""
    for scenario_file in discover_scenario_files(project_root):
        loaded = load_scenario(scenario_file)
        if loaded.data.get("id") == scenario_id:
            return loaded

    raise FileNotFoundError(f"Scenario ID '{scenario_id}' was not found")


def list_scenario_packs(project_root: Path | None = None) -> list[str]:
    """Return top-level scenario pack names."""
    root = scenarios_root(project_root)
    return sorted(path.name for path in root.iterdir() if path.is_dir())


def list_scenarios(project_root: Path | None = None) -> list[dict[str, Any]]:
    """Return discovered scenario summaries."""
    scenarios: list[dict[str, Any]] = []
    for scenario_file in discover_scenario_files(project_root):
        loaded = load_scenario(scenario_file)
        scenarios.append(
            {
                "id": loaded.data.get("id", "unknown"),
                "title": loaded.data.get("title", "untitled"),
                "path": loaded.path.parent,
            }
        )
    return scenarios
