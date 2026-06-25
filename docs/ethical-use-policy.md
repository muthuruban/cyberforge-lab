# Ethical Use Policy

CyberForge Lab is an educational platform for authorised, isolated cybersecurity learning only.

## Purpose

The project exists to support:

- secure development practice
- defensive analysis and reporting
- safe DevOps and automation learning
- scenario-based cyber range training in controlled environments

## Lab-Only Requirement

All usage must remain in isolated lab environments under your control or explicit written authorization.

## Prohibited Use

The following are not allowed:

- testing or scanning public systems
- targeting real organisations without authorization
- malware creation or distribution
- credential theft workflows
- persistence or covert-access automation
- repurposing scenarios for unauthorised activity

## Safe Operational Rules

- Use fictional data, fictional systems, and `.test` domains.
- Keep scenario internet exposure disabled by default.
- Keep containers and local networks isolated.
- Do not store secrets or production credentials in scenario files.

## AI and Credential Safety

- AI adapters must execute from the host or a dedicated trusted runner.
- AI credentials must never be copied into vulnerable containers, VM images, logs, or reports.
- AI should access only explicitly allowed workspace artifacts.

## Responsible Disclosure

If you discover a real vulnerability outside this educational lab:

1. Report privately to the rightful owner.
2. Provide clear, reproducible, defensive evidence.
3. Allow a reasonable remediation window before public disclosure.

## Contributor Responsibility

Contributors must preserve this policy when proposing code, scenarios, and documentation updates. Maintainers may reject or remove contributions that conflict with safe educational intent.
