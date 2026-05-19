from pathlib import Path

from cyberforge.orchestrator.scenario_loader import list_scenarios, load_scenario_by_id


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_load_scenario_yaml() -> None:
    loaded = load_scenario_by_id("nrg-staffhub-001", project_root=project_root())
    assert loaded.data["id"] == "nrg-staffhub-001"
    assert loaded.data["safety"]["lab_only"] is True


def test_list_scenarios_contains_staffhub() -> None:
    scenarios = list_scenarios(project_root=project_root())
    scenario_ids = {scenario["id"] for scenario in scenarios}
    assert "nrg-staffhub-001" in scenario_ids
