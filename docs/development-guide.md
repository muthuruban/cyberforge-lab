# Development Guide

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run CLI

```bash
cyberforge --help
cyberforge init
cyberforge doctor
```

## Run Quality Checks

```bash
ruff check .
pytest
```

## Run Scenario

```bash
cyberforge up --scenario nrg-staffhub-001
cyberforge down --scenario nrg-staffhub-001
```

## Engineering Notes

- Keep modules small and testable.
- Add docstrings to non-trivial functions.
- Handle command failures with explicit messages.
- Keep safety checks strict by default.
