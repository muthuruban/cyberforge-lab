# AI Integration (Phase 1 Safe Foundation)

## Current Scope

AI execution is intentionally disabled in Phase 1.

The only supported AI command is:

- `cyberforge ai status`

This command performs host-side status checks only:

- check whether `codex` CLI is installed
- if installed, run `codex login status` to infer whether authentication appears available
- check whether `claude` CLI is installed using command discovery only

## Explicit Non-Goals in Phase 1

- no model invocation
- no prompt sending
- no autonomous AI actions
- no AI-driven lab interaction

## Safety and Credential Rules

- AI status checks run from the host environment only.
- Status checks do not copy or store credentials.
- AI credentials must never be placed in:
  - vulnerable containers
  - vulnerable VMs
  - scenario folders
  - Docker images
  - logs or reports

## Filesystem Boundary

CyberForge AI status checks do not scan user documents. They only execute local CLI status commands and return command-level health signals.

## Future Direction (Later Phases)

Future AI features may include:

- `cyberforge ai hint`
- `cyberforge ai soc-review`
- `cyberforge ai review-report`

Any future execution remains subject to host-side trust boundaries and strict credential isolation controls.
