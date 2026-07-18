# Enterprise IAM Lifecycle Lab

A lightweight, educational portfolio project exploring Identity and Access Management (IAM) lifecycles and Role-Based Access Control (RBAC) in an enterprise context.

## Features

### ✅ Completed

- [x] Employee Identity Model (Python dataclasses)
- [x] Joiner Workflow (account provisioning)
- [x] Mover Workflow (role transitions)
- [x] Leaver Workflow (account termination)
- [x] RBAC Role Assignment
- [x] Automatic Username Generation
- [x] Audit Logging (event tracking)
- [x] Automated Testing (pytest)

### 🔄 Planned

- [ ] SQLite Database
- [ ] FastAPI REST API
- [ ] Microsoft Entra ID Integration
- [ ] Okta Integration
- [ ] Web Dashboard

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

## Technologies Used

- **Python 3.9+** – Core language for IAM logic and testing
- **pytest** – Automated testing framework
- **Git** – Version control
- **GitHub** – Source code hosting and collaboration
- **JSON** – Data serialization (roles, employees, audit logs)

## Project Structure

```
enterprise-iam-lab/
├── README.md                  # Project overview
├── CHANGELOG.md               # Detailed sprint history
├── LICENSE                    # MIT License
├── .gitignore                 # Git exclusions
├── requirements.txt           # Python dependencies
│
├── docs/
│   └── architecture.md        # System design and flow diagram
│
├── data/
│   ├── roles.json             # Role definitions (groups, apps, permissions)
│   ├── employees.json         # Employee records (Joiner/Mover/Leaver outcomes)
│   └── audit_log.json         # Audit events for compliance tracking
│
├── app/
│   ├── models.py              # Employee dataclass
│   ├── iam_service.py         # IAM business logic (create, update, terminate)
│   ├── audit.py               # Audit logging
│   └── demo.py                # Manual workflow demonstration
│
├── tests/
│   ├── test_models.py         # Employee model tests
│   ├── test_joiner.py         # Joiner workflow tests
│   ├── test_mover.py          # Mover workflow tests
│   ├── test_leaver.py         # Leaver workflow tests
│   └── test_audit.py          # Audit logging tests
│
└── screenshots/               # Demo images and diagrams (placeholder)
```

## Future Roadmap

### Near Term

- **SQLite Database Integration** – Replace JSON files with persistent relational storage
- **FastAPI REST API** – Expose Joiner/Mover/Leaver workflows via HTTP endpoints
- **Web Dashboard** – Simple UI for viewing employees, roles, and audit logs

### Medium Term

- **Microsoft Entra ID Integration** – Sync with Azure AD for real-world scenarios
- **Okta Integration** – Connect to Okta for cross-platform identity management
- **CI/CD Pipeline** – GitHub Actions for automated testing and deployment

### Long Term

- **Docker Containerization** – Package as container for local and cloud deployment
- **Policy Engine** – Advanced RBAC rules and conditional access
- **Data Retention & Compliance** – Audit log archival, GDPR/HIPAA audit trails

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip (Python package manager)

### Installation

```bash
git clone https://github.com/yourusername/enterprise-iam-lab.git
cd enterprise-iam-lab
python3 -m pip install -r requirements.txt
```

### Run Tests

```bash
python3 -m pytest -q
```

### Manual Demo

```bash
python3 app/demo.py
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
