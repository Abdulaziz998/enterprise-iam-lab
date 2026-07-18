# Architecture — Enterprise IAM Lifecycle Lab

This document describes the simplified architecture used for the lab. The flow is intentionally linear to help learners understand how HR-driven identity events are transformed into application access and audit records.

Flow diagram (conceptual):

HR
↓
IAM Engine
↓
RBAC Engine
↓
Application Access
↓
Audit Log

## Components

- HR
  - The authoritative source for employee records: join, move, leave events. In a real company this might be an HRIS (Human Resources Information System) such as Workday or BambooHR.
  - Beginner-friendly: HR tells the rest of the system who exists and what their job title/team is.

- IAM Engine
  - Responsible for provisioning and deprovisioning identities, creating accounts, and managing lifecycle events (Joiner/Mover/Leaver).
  - Beginner-friendly: The IAM Engine listens to HR changes and translates them into identity actions (create user, disable user, update attributes).

- RBAC Engine
  - Evaluates role memberships and assigns the specific permissions associated with roles. It enforces least-privilege by mapping HR attributes and business rules to roles.
  - Beginner-friendly: RBAC decides what each role can actually do in each application.

- Application Access
  - The set of target applications and services (ticketing, HR system, finance app, code repositories). Access is granted via the RBAC Engine’s decisions (group membership, SAML/SCIM, API tokens, etc.).
  - Beginner-friendly: This is where users actually gain access to tools they use daily.

- Audit Log
  - A centralized place to record all identity and access-related actions: who provisioned or changed access, when, and what the change was. Logs should be immutable or tamper-evident and stored according to retention policy.
  - Beginner-friendly: Audit logs create a trustworthy history for security teams and auditors.

## Notes

- In later sprints the IAM Engine could expose APIs to accept HR events (webhooks or message queues) and the RBAC Engine could be implemented as a policy engine or rule evaluator.
- Integration points (SCIM, SSO, SAML, API calls) are out of scope for Sprint 1 but are noted as future enhancements.
