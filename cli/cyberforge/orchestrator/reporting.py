"""Learner report workflow helpers."""

from __future__ import annotations

import re
from pathlib import Path

from cyberforge.orchestrator.scenario_loader import (
    LoadedScenario,
    find_project_root,
    load_scenario_by_id,
)
from cyberforge.orchestrator.workspace import ensure_workspace, workspace_path

REQUIRED_REPORT_SECTIONS = (
    "Executive summary",
    "Affected system",
    "Evidence reviewed",
    "Risk rating",
    "Technical finding",
    "Business impact",
    "Recommended remediation",
    "Lessons learned",
)


def reports_directory(project_root: Path | None = None) -> Path:
    """Return workspace report directory path."""
    root = project_root or find_project_root()
    return workspace_path(root) / "reports"


def report_path_for_scenario(scenario_id: str, project_root: Path | None = None) -> Path:
    """Return deterministic report path for a scenario."""
    return reports_directory(project_root) / f"{scenario_id}-report.md"


def _template_path(project_root: Path | None = None) -> Path:
    root = project_root or find_project_root()
    return root / "templates" / "finding-template.md"


def _load_template(project_root: Path | None = None) -> str:
    template_path = _template_path(project_root)
    if not template_path.is_file():
        raise FileNotFoundError(f"Report template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def _list_field(values: list[dict] | list[str], key: str | None = None) -> str:
    lines: list[str] = []
    for item in values:
        if isinstance(item, dict):
            if key and key in item:
                lines.append(f"- {item[key]}")
            elif "name" in item:
                lines.append(f"- {item['name']}")
        elif isinstance(item, str):
            lines.append(f"- {item}")
    return "\n".join(lines) if lines else "- none listed"


def build_report_content(loaded: LoadedScenario, template: str) -> str:
    """Build report markdown with scenario metadata and required sections."""
    data = loaded.data
    systems = data.get("systems", [])
    personas = data.get("personas", [])

    required_sections = "\n\n".join(
        f"## {section}\n\n- _Add your analysis here._" for section in REQUIRED_REPORT_SECTIONS
    )

    return f"""# CyberForge Learner Report

## Report Metadata

- Scenario ID: `{data.get("id", "unknown")}`
- Scenario Title: {data.get("title", "Untitled Scenario")}
- Organisation: {data.get("organisation", "Unknown")}
- Sector: {data.get("sector", "Unknown")}
- Generated Path: `{loaded.path}`

## Scenario Context

{data.get("description", "No description provided.")}

## Systems in Scope

{_list_field(systems, key="name")}

## Personas in Scope

{_list_field(personas, key="name")}

{required_sections}

## Template Baseline

The following baseline was sourced from `templates/finding-template.md`:

{template}
"""


def create_report(
    scenario_id: str,
    *,
    force: bool = False,
    project_root: Path | None = None,
) -> Path:
    """Create a scenario learner report in the workspace reports folder."""
    root = project_root or find_project_root()
    ensure_workspace(root)
    loaded = load_scenario_by_id(scenario_id, root)
    template = _load_template(root)
    report_path = report_path_for_scenario(scenario_id, root)

    if report_path.exists() and not force:
        raise FileExistsError(
            f"Report already exists: {report_path}. Use --force to overwrite."
        )

    content = build_report_content(loaded, template)
    report_path.write_text(content, encoding="utf-8")
    return report_path


def list_reports(project_root: Path | None = None) -> list[Path]:
    """Return all workspace report markdown files."""
    report_dir = reports_directory(project_root or find_project_root())
    if not report_dir.is_dir():
        return []
    return sorted(report_dir.glob("*.md"))


def validate_report(path: Path) -> list[str]:
    """Return missing required section names for a report file."""
    if not path.is_file():
        raise FileNotFoundError(f"Report file not found: {path}")

    content = path.read_text(encoding="utf-8")
    headings = {
        match.group(1).strip().lower()
        for match in re.finditer(r"^##\s+(.+?)\s*$", content, flags=re.MULTILINE)
    }

    return [section for section in REQUIRED_REPORT_SECTIONS if section.lower() not in headings]
