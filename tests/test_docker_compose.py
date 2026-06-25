import subprocess
from pathlib import Path

import pytest
from cyberforge.orchestrator.docker_compose import (
    DockerComposeError,
    _run_command,
    docker_available,
    is_scenario_running,
    run_compose_up,
)


def test_run_command_decodes_undecodable_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args, **kwargs) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(args[0], 0, b"ok\x81", b"")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = _run_command(["docker", "--version"])
    assert result.returncode == 0
    assert "ok" in result.stdout


def test_run_compose_up_fails_when_no_services_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("cyberforge.orchestrator.docker_compose.STARTUP_WAIT_SECONDS", 2)
    monkeypatch.setattr("cyberforge.orchestrator.docker_compose.STARTUP_POLL_INTERVAL_SECONDS", 1)
    monkeypatch.setattr("cyberforge.orchestrator.docker_compose.time.sleep", lambda _: None)

    def fake_run(command, **kwargs) -> subprocess.CompletedProcess[bytes]:
        if command[:3] == ["docker", "compose", "up"]:
            return subprocess.CompletedProcess(command, 0, b"", b"")
        if command[:3] == ["docker", "compose", "ps"] and "--format" in command:
            payload = b'[{"Service":"staffhub","State":"restarting"}]'
            return subprocess.CompletedProcess(command, 0, payload, b"")
        if command[:3] == ["docker", "compose", "ps"] and "--all" in command:
            return subprocess.CompletedProcess(
                command,
                0,
                b"NAME STATUS\ncyberforge-nrg-staffhub exited",
                b"",
            )
        return subprocess.CompletedProcess(command, 1, b"", b"unexpected call")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(DockerComposeError, match="no running services"):
        run_compose_up(Path("."))


def test_is_scenario_running_detects_active_services(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("cyberforge.orchestrator.docker_compose.shutil.which", lambda _: "docker")

    def fake_run(command, **kwargs) -> subprocess.CompletedProcess[bytes]:
        if command == ["docker", "--version"]:
            return subprocess.CompletedProcess(command, 0, b"Docker version 29", b"")
        if command == ["docker", "info", "--format", "{{.ServerVersion}}"]:
            return subprocess.CompletedProcess(command, 0, b"29.4.0", b"")
        if command == ["docker", "compose", "version"]:
            return subprocess.CompletedProcess(command, 0, b"Docker Compose version v2", b"")
        if command == ["docker", "compose", "ps", "--format", "json"]:
            payload = b'[{"Service":"staffhub","State":"running"}]'
            return subprocess.CompletedProcess(command, 0, payload, b"")
        return subprocess.CompletedProcess(command, 1, b"", b"unexpected call")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert is_scenario_running(Path(".")) is True


def test_docker_available_fails_gracefully_when_binary_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("cyberforge.orchestrator.docker_compose.shutil.which", lambda _: None)
    ok, detail = docker_available()
    assert ok is False
    assert "not found" in detail
