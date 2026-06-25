import copy
from pathlib import Path

import pytest
from cyberforge.orchestrator.scenario_loader import load_scenario_by_id
from cyberforge.safety.validators import SafetyPolicyError, validate_safety_policy


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_valid_scenario() -> dict:
    loaded = load_scenario_by_id("nrg-staffhub-001", project_root=project_root())
    return loaded.data


def test_valid_safety_policy_passes() -> None:
    scenario = load_valid_scenario()
    validate_safety_policy(scenario)


def test_safety_policy_blocks_non_lab_domains() -> None:
    scenario = copy.deepcopy(load_valid_scenario())
    scenario["safety"]["allowed_domains"] = ["example.com"]
    with pytest.raises(SafetyPolicyError):
        validate_safety_policy(scenario)


def test_safety_policy_requires_lab_only_true() -> None:
    scenario = copy.deepcopy(load_valid_scenario())
    scenario["safety"]["lab_only"] = False
    with pytest.raises(SafetyPolicyError):
        validate_safety_policy(scenario)


def test_safety_policy_requires_internet_access_false() -> None:
    scenario = copy.deepcopy(load_valid_scenario())
    scenario["safety"]["internet_access"] = True
    with pytest.raises(SafetyPolicyError):
        validate_safety_policy(scenario)
