# Target Server Setup

This server is the machine being monitored by the SOC team and used by the Red Team during the workshop.

## Purpose

- Host the workshop website
- Run the Wazuh agent
- Generate the activity that the Blue Team must detect and investigate

## Recommended base

- OS: RHEL 10
- Web server: Nginx
- Hostname: `school-web`
- Network: lab-only interface on the same virtual network as the Wazuh server

## Build order

1. Create the VM in `virt-manager`
2. Install RHEL 10
3. Update the system
4. Install Nginx
5. Deploy the workshop website
6. Install and enroll the Wazuh agent
7. Confirm the dashboard sees the host
8. Take a clean snapshot

## Training weaknesses

The server is designed to contain seven training weaknesses across common web and system misconfiguration categories:

- weak credentials
- directory listing
- file upload weakness
- broken access control
- SQL injection
- command injection
- outdated or misconfigured service

## Notes

- Keep the target isolated from real systems
- Do not reuse production credentials or data
- Keep a clean snapshot for resets

