# CyberForge Lab

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-D22128?logo=apache&logoColor=white)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Foundation-0A7E3F)](docs/roadmap.md)

CyberForge Lab is an open-source, non-commercial, local-first cybersecurity lab orchestrator for safe, isolated, scenario-driven learning.

## Project Snapshot

- **Project type**: educational cyber range workspace
- **Current scope**: Phase 0 and Phase 1 foundation
- **Primary provider**: Docker Compose
- **First scenario**: `nrg-staffhub-001` (Northbridge Retail Group)
- **Safety model**: lab-only, fictional-only, `.test` domains, no public targeting

## What CyberForge Lab Is

CyberForge Lab helps practitioners build practical skills in:

- Python engineering
- DevOps automation
- Docker-based orchestration
- secure software engineering
- blue-team style investigation and reporting
- AI-assisted workflows with host-side safety boundaries

## What CyberForge Lab Is Not

CyberForge Lab is not a public-target offensive hacking tool.

It must not be used for:

- unauthorised testing
- public system targeting
- malware development
- credential theft
- persistence or covert access techniques

## Ethical-Use Warning

All environments are fictional, isolated, and lab-only. Use only on systems you own or are explicitly authorised to test.

Read: [docs/ethical-use-policy.md](docs/ethical-use-policy.md)

## Quick Start

### 1) Prerequisites

- Python 3.11+
- Docker Desktop (or Docker Engine with Compose)

### 2) Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

### 3) Initialize workspace

```bash
cyberforge init
```

### 4) Health checks

```bash
cyberforge doctor
cyberforge status
cyberforge ai status
```

### 5) Start the first lab

```bash
cyberforge up --scenario nrg-staffhub-001
```

App URL: `http://127.0.0.1:8088`

### 6) Stop the lab

```bash
cyberforge down --scenario nrg-staffhub-001
```

## CLI Commands (Phase 1)

- `cyberforge init`
- `cyberforge doctor`
- `cyberforge status`
- `cyberforge up --scenario nrg-staffhub-001`
- `cyberforge down --scenario nrg-staffhub-001`
- `cyberforge ai status`
- `cyberforge report create --scenario nrg-staffhub-001`
- `cyberforge report status`
- `cyberforge report validate`

## Troubleshooting

### `ERR_CONNECTION_REFUSED` on `localhost:8088`

If this happens after `cyberforge down`, this is expected because the lab container is stopped.

To access the app again:

1. Run `cyberforge up --scenario nrg-staffhub-001`
2. Confirm runtime with `cyberforge status`
3. Open `http://127.0.0.1:8088`

If this happens while the lab is expected to be running:

1. Run `cyberforge status` and confirm the scenario is detected as running
2. Check container logs with `docker logs cyberforge-nrg-staffhub`
3. Run `cyberforge up --scenario nrg-staffhub-001` again (it now rebuilds before launch)

### Docker daemon unavailable

If `cyberforge doctor` reports daemon unavailable:

1. Start Docker Desktop
2. Wait until Docker is fully running
3. Run `cyberforge doctor` again

### Docker reports `No such container` during `up`

Sometimes Docker keeps stale local metadata after interrupted runs.

1. Run `cyberforge down --scenario nrg-staffhub-001`
2. Run `cyberforge up --scenario nrg-staffhub-001` again

## Architecture Summary

- Host-side Python orchestrator
- scenario packs with explicit safety metadata
- isolated victim app container with local-only exposure
- shared workspace for evidence and reports
- host-only AI adapter model (status only in Phase 1)

See [docs/architecture.md](docs/architecture.md) for full architecture and trust boundaries.

## First Scenario

- **ID**: `nrg-staffhub-001`
- **Title**: Suspicious Activity in the Northbridge StaffHub Portal
- **Organisation**: Northbridge Retail Group (fictional)
- **Focus**:
  - authentication weakness investigation
  - application log review
  - secure coding remediation planning
  - SOC-style reporting

## Skills Demonstrated

### Python Engineering

- modular Typer CLI command design
- YAML-based scenario loading and validation
- test-first safety checks and orchestration helpers

### DevOps and Automation

- Docker Compose lifecycle management
- deterministic local workspace bootstrapping
- GitHub Actions CI with Ruff + pytest

### Cybersecurity Lab Design

- safety-gated scenario startup
- `.test` domain boundary enforcement
- educational vulnerable app with defensive analysis framing

### Secure Software Engineering

- explicit ethical-use controls
- host-only AI credential posture
- no offensive automation or public targeting workflows

### AI-Assisted Development Readiness

- provider adapter placeholders for Codex CLI and Claude Code CLI
- future-ready command structure without runtime model execution in Phase 1

## Roadmap

Roadmap and milestones: [docs/roadmap.md](docs/roadmap.md)

## Open-Source and Non-Commercial Statement

CyberForge Lab is a non-commercial open-source educational project intended for portfolio and learning use.

## Contributing

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
