"""Docker Compose orchestration helpers."""

from __future__ import annotations

import json
import locale
import shutil
import subprocess
import time
from pathlib import Path


class DockerComposeError(RuntimeError):
    """Raised when a Docker Compose operation fails."""


STARTUP_WAIT_SECONDS = 20
STARTUP_POLL_INTERVAL_SECONDS = 1


def _decode_output(raw: bytes | str | None) -> str:
    """Decode subprocess output safely across platforms."""
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw

    preferred = locale.getpreferredencoding(False) or "utf-8"
    for encoding in ("utf-8", preferred, "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw.decode("utf-8", errors="replace")


def _run_command(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run command and return decoded text output without locale decode crashes."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=False,
            check=False,
        )
    except FileNotFoundError as exc:
        raise DockerComposeError(f"required command was not found: {command[0]}") from exc

    return subprocess.CompletedProcess(
        args=result.args,
        returncode=result.returncode,
        stdout=_decode_output(result.stdout),
        stderr=_decode_output(result.stderr),
    )


def _run_compose(args: list[str], scenario_dir: Path) -> subprocess.CompletedProcess[str]:
    return _run_command(["docker", "compose", *args], cwd=scenario_dir)


def _running_services(scenario_dir: Path) -> list[str]:
    """Return running service names for a compose project."""
    # Prefer JSON for accurate state parsing.
    json_result = _run_compose(["ps", "--format", "json"], scenario_dir)
    if json_result.returncode == 0 and json_result.stdout.strip():
        try:
            rows = json.loads(json_result.stdout)
            running = []
            for row in rows:
                if not isinstance(row, dict):
                    continue
                state = str(row.get("State", "")).lower()
                if state == "running":
                    service = str(row.get("Service", "")).strip()
                    if service:
                        running.append(service)
            if running:
                return sorted(set(running))
        except json.JSONDecodeError:
            pass

    # Fallback for Compose variants without JSON output support.
    result = _run_compose(["ps", "--status", "running", "--services"], scenario_dir)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _summarize_compose_state(scenario_dir: Path) -> str:
    """Return a short compose ps snapshot for troubleshooting."""
    result = _run_compose(["ps", "--all"], scenario_dir)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown compose state"
        return f"unable to inspect compose state: {detail}"
    return result.stdout.strip() or "no compose services listed"


def docker_available() -> tuple[bool, str]:
    """Return whether Docker CLI and daemon appear available."""
    if not shutil.which("docker"):
        return False, "docker binary was not found in PATH"

    version = _run_command(["docker", "--version"])
    if version.returncode != 0:
        detail = version.stderr.strip() or "unable to execute docker --version"
        return False, detail
    cli_version = version.stdout.strip() or "unknown docker version"

    daemon = _run_command(["docker", "info", "--format", "{{.ServerVersion}}"])
    if daemon.returncode != 0:
        detail = daemon.stderr.strip() or "docker daemon is not reachable"
        return False, f"{cli_version}; daemon unavailable: {detail}"

    daemon_version = daemon.stdout.strip() or "unknown"
    return True, f"{cli_version}; daemon={daemon_version}"


def docker_compose_available() -> tuple[bool, str]:
    """Return whether Docker Compose CLI appears available."""
    if not shutil.which("docker"):
        return False, "docker binary was not found in PATH"

    result = _run_command(["docker", "compose", "version"])
    if result.returncode != 0:
        detail = result.stderr.strip() or "unable to execute docker compose version"
        return False, detail
    return True, result.stdout.strip()


def run_compose_up(scenario_dir: Path) -> None:
    """Run `docker compose up -d` in a scenario directory."""
    result = _run_compose(["up", "--build", "-d"], scenario_dir)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise DockerComposeError(f"docker compose up failed: {detail}")

    attempts = max(1, int(STARTUP_WAIT_SECONDS / STARTUP_POLL_INTERVAL_SECONDS))
    running_services: list[str] = []
    for _ in range(attempts):
        running_services = _running_services(scenario_dir)
        if running_services:
            break
        time.sleep(STARTUP_POLL_INTERVAL_SECONDS)

    if not running_services:
        state = _summarize_compose_state(scenario_dir)
        raise DockerComposeError(
            "docker compose up reported success but no running services were detected. "
            f"Compose state:\n{state}"
        )


def run_compose_down(scenario_dir: Path) -> None:
    """Run `docker compose down --remove-orphans` in a scenario directory."""
    result = _run_compose(["down", "--remove-orphans"], scenario_dir)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise DockerComposeError(f"docker compose down failed: {detail}")


def is_scenario_running(scenario_dir: Path) -> bool:
    """Best-effort runtime detection for a scenario."""
    docker_ok, _ = docker_available()
    compose_ok, _ = docker_compose_available()
    if not (docker_ok and compose_ok):
        return False

    try:
        services = _running_services(scenario_dir)
    except DockerComposeError:
        return False
    return bool(services)
