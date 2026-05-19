# Contributing to CyberForge Lab

Thanks for contributing.

## Principles

- Keep everything lab-only and defensive.
- Preserve fictional scenario boundaries.
- Prefer readable, tested code over complexity.
- Do not include secrets, real credentials, or real company data.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Quality Gates

```bash
ruff check .
pytest
```

## Pull Requests

- Describe what changed and why.
- Add or update tests for behavior changes.
- Keep commits focused and reviewable.
- Confirm safety policy and ethical-use boundaries are intact.
