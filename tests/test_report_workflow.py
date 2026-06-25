from pathlib import Path

import pytest
from cyberforge.orchestrator.reporting import (
    REQUIRED_REPORT_SECTIONS,
    create_report,
    list_reports,
    report_path_for_scenario,
    reports_directory,
    validate_report,
)


def bootstrap_project_root(tmp_path: Path) -> Path:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='tmp'\n", encoding="utf-8")
    scenario_dir = tmp_path / "scenarios" / "northbridge-retail-group" / "nrg-staffhub-001"
    scenario_dir.mkdir(parents=True)
    (scenario_dir / "scenario.yml").write_text(
        "\n".join(
            [
                "id: nrg-staffhub-001",
                "title: Suspicious Activity in StaffHub",
                "organisation: Northbridge Retail Group",
                "sector: Retail and e-commerce",
                "description: Learner investigates suspicious authentication activity.",
                "systems:",
                "  - name: StaffHub Portal",
                "personas:",
                "  - name: Maya Patel",
            ]
        ),
        encoding="utf-8",
    )

    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    (template_dir / "finding-template.md").write_text(
        "# Security Finding Template\n\n## Title\n\n## Summary\n",
        encoding="utf-8",
    )
    return tmp_path


def test_report_create_generates_workspace_markdown(tmp_path: Path) -> None:
    root = bootstrap_project_root(tmp_path)
    report_path = create_report("nrg-staffhub-001", project_root=root)

    assert report_path.exists()
    assert report_path.parent == reports_directory(root)
    content = report_path.read_text(encoding="utf-8")
    assert "Scenario ID: `nrg-staffhub-001`" in content
    for section in REQUIRED_REPORT_SECTIONS:
        assert f"## {section}" in content


def test_report_create_blocks_overwrite_without_force(tmp_path: Path) -> None:
    root = bootstrap_project_root(tmp_path)
    create_report("nrg-staffhub-001", project_root=root)

    with pytest.raises(FileExistsError):
        create_report("nrg-staffhub-001", project_root=root)


def test_report_create_overwrites_with_force(tmp_path: Path) -> None:
    root = bootstrap_project_root(tmp_path)
    report = create_report("nrg-staffhub-001", project_root=root)
    report.write_text("custom content", encoding="utf-8")

    forced_report = create_report("nrg-staffhub-001", project_root=root, force=True)
    assert forced_report == report_path_for_scenario("nrg-staffhub-001", root)
    assert "custom content" not in forced_report.read_text(encoding="utf-8")


def test_report_validate_detects_missing_sections(tmp_path: Path) -> None:
    root = bootstrap_project_root(tmp_path)
    report = create_report("nrg-staffhub-001", project_root=root)
    content = report.read_text(encoding="utf-8")
    content = content.replace("## Lessons learned", "## Lessons retired")
    report.write_text(content, encoding="utf-8")

    missing = validate_report(report)
    assert "Lessons learned" in missing


def test_list_reports_returns_workspace_reports(tmp_path: Path) -> None:
    root = bootstrap_project_root(tmp_path)
    create_report("nrg-staffhub-001", project_root=root)
    reports = list_reports(root)
    assert len(reports) == 1
    assert reports[0].name == "nrg-staffhub-001-report.md"
