# Roadmap

This roadmap is intentionally phased to show clear growth from local-first foundations to larger cyber range capabilities while preserving safety and educational boundaries.

## Phase Milestones

| Phase | Focus | Key Milestones | Exit Criteria |
|---|---|---|---|
| Phase 0 | Repository foundation | Governance docs, project structure, CLI skeleton, scenario schema baseline | Repo is contributor-ready and safety baseline is documented |
| Phase 1 | First working local lab | `nrg-staffhub-001`, Docker Compose orchestration, logging, report templates, AI status adapters | Scenario can be launched/stopped safely and validated via tests/CI |
| Phase 2 | AI-assisted learning workflows | Host-side AI tutor hints, report reviewer, SOC-log review assistant patterns | AI features remain host-scoped with strict credential isolation |
| Phase 3 | Blue-team depth | Controlled integration profile for Wazuh/Suricata and richer telemetry flows | Defensive monitoring scenarios are reproducible and documented |
| Phase 4 | VM profile | Vagrant/VirtualBox lab profile with parity to Docker scenario concepts | VM lifecycle controls and safety parity checks are in place |
| Phase 5 | Cloud-ready extension | Azure lab profile concepts with Terraform and monitoring-aligned architecture | Cloud profile remains educational, isolated, and policy-aligned |

## Current Status

Current active milestone: **Phase 1 foundation**.

Delivered:

- CLI lifecycle commands for local scenarios
- safety validation for lab boundaries
- first fictional enterprise scenario and vulnerable training app
- markdown reporting workflow
- CI quality gates with Ruff and pytest

## Quality Gates by Phase

- Safety policy checks must pass before scenario startup.
- Tests and lint checks must pass in CI for merge readiness.
- New scenario proposals must preserve fictional-only and authorised-use constraints.
