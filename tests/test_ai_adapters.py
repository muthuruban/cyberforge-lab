import subprocess

from cyberforge.ai_adapters.claude_adapter import ClaudeAdapter
from cyberforge.ai_adapters.codex_adapter import CodexAdapter


def test_codex_status_when_not_installed(monkeypatch) -> None:
    monkeypatch.setattr(CodexAdapter, "is_installed", lambda self: False)
    status = CodexAdapter().status()
    assert status["installed"] is False
    assert status["auth_checked"] is False
    assert status["authenticated"] is False
    assert status["auth_state"] == "not_checked"


def test_codex_status_authenticated(monkeypatch) -> None:
    monkeypatch.setattr(CodexAdapter, "is_installed", lambda self: True)
    monkeypatch.setattr(
        CodexAdapter,
        "run_command",
        lambda self, args, cwd=None, timeout_seconds=10: subprocess.CompletedProcess(
            args,
            0,
            "You are logged in.",
            "",
        ),
    )
    status = CodexAdapter().status()
    assert status["installed"] is True
    assert status["auth_checked"] is True
    assert status["authenticated"] is True
    assert status["auth_state"] == "authenticated"


def test_codex_status_unauthenticated(monkeypatch) -> None:
    monkeypatch.setattr(CodexAdapter, "is_installed", lambda self: True)
    monkeypatch.setattr(
        CodexAdapter,
        "run_command",
        lambda self, args, cwd=None, timeout_seconds=10: subprocess.CompletedProcess(
            args,
            1,
            "",
            "Not logged in",
        ),
    )
    status = CodexAdapter().status()
    assert status["auth_checked"] is True
    assert status["authenticated"] is False
    assert status["auth_state"] == "unauthenticated"


def test_codex_status_timeout(monkeypatch) -> None:
    monkeypatch.setattr(CodexAdapter, "is_installed", lambda self: True)

    def raise_timeout(self, args, cwd=None, timeout_seconds=10):
        raise subprocess.TimeoutExpired(cmd=args, timeout=timeout_seconds)

    monkeypatch.setattr(CodexAdapter, "run_command", raise_timeout)
    status = CodexAdapter().status()
    assert status["auth_checked"] is True
    assert status["authenticated"] is False
    assert status["auth_state"] == "unknown"
    assert "timed out" in str(status["auth_message"]).lower()


def test_claude_status_uses_command_discovery(monkeypatch) -> None:
    monkeypatch.setattr("cyberforge.ai_adapters.base.shutil.which", lambda _: "/usr/bin/claude")
    status = ClaudeAdapter().status()
    assert status["installed"] is True
