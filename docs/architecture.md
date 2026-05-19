# Architecture

## Overview

CyberForge Lab uses a host-orchestrated architecture for isolated, educational cybersecurity scenarios. The host controls lifecycle, safety checks, and evidence workflow. Scenario systems remain intentionally constrained and local-first.

## ASCII Architecture Diagram

```text
+--------------------------------------------------------------------------------------------------+
|                                      Host Machine (Trusted Zone)                                |
|                                                                                                  |
|  +-------------------------+          +-----------------------------------------+                |
|  | cyberforge CLI (Typer)  |--------->| Safety Layer                            |                |
|  | init/doctor/status/up   |          | - lab_only enforcement                  |                |
|  | down/ai status          |          | - allowed_domains validation            |                |
|  +-----------+-------------+          | - internet_access policy                |                |
|              |                        +--------------------+--------------------+                |
|              |                                             |                                     |
|              v                                             v                                     |
|  +-------------------------+          +-----------------------------------------+                |
|  | Workspace               |          | Scenario Loader                         |                |
|  | .cyberforge-workspace/  |<-------->| scenarios/*/*/scenario.yml             |                |
|  | logs alerts evidence    |          | metadata + safety + lab profile         |                |
|  | reports temp            |          +--------------------+--------------------+                |
|  +-------------------------+                               |                                     |
|                                                             v                                     |
|                                           +-----------------------------------+                  |
|                                           | Docker Compose Orchestrator       |                  |
|                                           | up/down/status checks             |                  |
|                                           +----------------+------------------+                  |
+------------------------------------------------------------|-------------------------------------+
                                                             |
                                                             v
+--------------------------------------------------------------------------------------------------+
|                          Local Docker Lab Network (Isolated Learning Zone)                      |
|                                                                                                  |
|  +---------------------------------------+        +-----------------------------------------+    |
|  | staffhub service                      |        | mounted scenario logs                   |    |
|  | container: cyberforge-nrg-staffhub    |------->| scenarios/.../logs/staffhub.log        |    |
|  | FastAPI + SQLite                      |        +-----------------------------------------+    |
|  | port: 127.0.0.1:8088 -> 8000          |                                                      |
|  +---------------------------------------+                                                      |
|                                                                                                  |
|  Future (not active in Phase 1):                                                                 |
|  - nrg-soc-01 (log correlation)                                                                  |
|  - attacker simulation profile in controlled boundary                                            |
+--------------------------------------------------------------------------------------------------+

AI Boundary (Phase 1):
- Codex/Claude adapters are host-side status checks only.
- No model execution inside containers.
- No AI credentials in scenario folders, images, logs, or vulnerable systems.
```

## Component Roles

### Host Orchestrator

The `cyberforge` CLI coordinates:

- workspace setup (`init`)
- environment checks (`doctor`)
- scenario discovery (`status`)
- lifecycle operations (`up`, `down`)
- AI adapter availability checks (`ai status`)

### Safety Layer

Startup is blocked when safety metadata is non-compliant:

- `lab_only` must be true
- `allowed_domains` must stay within `.test`, `localhost`, or internal service names
- `internet_access` must be false in Phase 1

### Shared Workspace

`.cyberforge-workspace` separates operational artifacts from source code:

- `logs/`
- `alerts/`
- `evidence/`
- `reports/`
- `temp/`

### Victim App

The first scenario uses a business-style FastAPI app (`StaffHub Portal`) designed for defensive review and secure coding remediation exercises.

## Trust Boundaries

### Trusted Zone

- host CLI runtime
- scenario metadata
- workspace artifacts
- CI/test tooling

### Untrusted-by-Design Zone

- intentionally weak training app container(s)
- any data generated by vulnerable services

## Why AI Credentials Must Never Be in Vulnerable Lab Systems

Placing AI credentials inside intentionally weak systems breaks the project safety model and teaches poor operational practice.

Rules:

- keep credentials in host-managed secret stores only
- never bake credentials into Docker images
- never commit credentials into scenario repositories
- never write credentials into logs, reports, or seeded data
