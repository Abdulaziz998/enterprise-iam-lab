# Enterprise IAM Lifecycle Lab — Sprint 1

A lightweight, educational portfolio project exploring Identity and Access Management (IAM) lifecycles and Role-Based Access Control (RBAC) in an enterprise context.

## What is Identity and Access Management (IAM)?

Identity and Access Management (IAM) is the practice and set of systems that ensure the right people have the right access to the right resources at the right time. IAM covers provisioning and deprovisioning accounts, enforcing authentication and authorization policies, and maintaining an inventory of who can access what.

## Joiner, Mover, Leaver (JML)

- Joiner: When a new employee or contractor is onboarded. The JML process provisions accounts, assigns initial roles, and grants baseline access required to start work.
- Mover: When an existing person changes jobs, teams, or responsibilities. The Mover process updates access to reflect their new role and removes access no longer needed.
- Leaver: When a person exits the organisation. The Leaver process revokes access, archives accounts, and records the change for audits.

These three stages together ensure access continuously matches an individual’s employment status and role.

## What is Role-Based Access Control (RBAC)?

RBAC assigns permissions to roles rather than to individual users. Users are added to roles (or groups) and inherit the permissions of that role. This simplifies administration and helps enforce consistent access policies.

## Why Least Privilege Matters

Least privilege means granting users only the permissions they need to perform their tasks—and no more. Benefits:

- Reduces blast radius if an account is compromised
- Limits accidental misuse of powerful features
- Simplifies audits by narrowing required controls

Our sample roles follow least-privilege principles and avoid any unrestricted "administrator" role.

## Why Audit Logs Matter

Audit logs record who did what and when. They are essential for:

- Investigating incidents
- Proving compliance
- Tracking changes to sensitive access

Audit logs should be tamper-evident, retained according to policy, and easily searchable by security and compliance teams.

## Technologies (Sprint 1)

- Data format: `JSON` (for role definitions and simple config)
- Documentation: `Markdown` for README and architecture notes
- Test tooling: `pytest` (declared in `requirements.txt`)
- VCS: `git` (project intended for GitHub publication)

Future sprints may introduce Python apps, CI pipelines, and containerization (Docker), but Sprint 1 is documentation + data only.

## Future Roadmap (high level)

- Sprint 2: Implement a simple IAM Engine prototype (Python) to read `roles.json` and simulate Joiner flows
- Sprint 3: Add RBAC enforcement module and a demo web UI
- Sprint 4: Integrate audit logging backend and retention policies
- Sprint 5: Add end-to-end tests, CI, and deployment manifests

## Project Tree (Sprint 1)

- README.md
- LICENSE
- .gitignore
- requirements.txt
- docs/
  - architecture.md
- data/
  - roles.json
- app/ (placeholder for future code)
- tests/ (placeholder for future tests)
- screenshots/ (placeholder for demo images)

---

This sprint deliberately avoids writing application code. The artifacts here are designed to form a clear foundation for development in later sprints.
