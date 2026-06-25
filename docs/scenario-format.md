# Scenario Format

Each scenario must include `scenario.yml` with required metadata and safety constraints.

## Required Fields

- `id`
- `title`
- `organisation`
- `sector`
- `description`
- `systems`
- `personas`
- `learning_objectives`
- `safety`
- `ai`
- `scoring`
- `report_requirements`

## Safety Requirements

`safety` must include:

- `lab_only: true`
- `allowed_domains`
- `allowed_targets`
- `internet_access`

For initial scenarios:

- `internet_access` must be `false`
- domains should be `.test`, `localhost`, or internal Docker service names

## Example

```yaml
id: nrg-staffhub-001
title: Suspicious Activity in the Northbridge StaffHub Portal
safety:
  lab_only: true
  internet_access: false
  allowed_domains:
    - staffhub.northbridge.test
    - db.northbridge.test
    - localhost
  allowed_targets:
    - staffhub
    - nrg-web-01
```
