# SOC Workshop Lab

This repository holds the setup and operating docs for a blue team workshop built around a single monitored website server, a central Wazuh dashboard, and seven analysts working in SOC roles.

## What this repo is for

- Building and resetting the lab
- Explaining the workshop flow
- Keeping red and blue team instructions separate
- Providing note templates for `vim`
- Documenting how the team uses `virt-manager`, Chrome, and Burp

## Lab model

- `1` target machine runs the website
- `1` Wazuh manager/dashboard machine receives alerts
- `7` analysts log into the same dashboard and split SOC duties

## Start here

1. Read [`docs/overview.md`](docs/overview.md)
2. Read [`docs/rules-of-engagement.md`](docs/rules-of-engagement.md)
3. Follow [`docs/setup/virt-manager.md`](docs/setup/virt-manager.md)
4. Follow [`docs/setup/rhel10.md`](docs/setup/rhel10.md)
5. Follow [`docs/setup/wazuh.md`](docs/setup/wazuh.md)
6. Use the templates in [`templates/`](templates/)

## Roles

- Tier 1 Analyst
- Tier 2 Analyst
- Tier 3 Analyst
- Incident Responder
- Threat Hunter
- Security Engineer
- Reporting and Threat Intel Analyst

## Repo layout

- `docs/` workshop and setup documentation
- `infra/` VM and reset helpers
- `templates/` notes and report templates
- `scripts/` small helper commands
- `evidence/` screenshots and exported findings

