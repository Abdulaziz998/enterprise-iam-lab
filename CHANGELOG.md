# Enterprise IAM Lifecycle Lab Changelog

This changelog documents the major milestones of the Enterprise IAM Lifecycle Lab.

Each sprint represents a functional enhancement to the simulated Identity and Access Management (IAM) platform. The goal is to progressively build an enterprise-style IAM solution using Python, automated testing, and modern software engineering practices.

## Sprint 1

- Created project foundation and public-facing documentation (`README.md`).
- Added legal and tooling files: `LICENSE` (MIT), `.gitignore`, and `requirements.txt`.
- Added architecture notes in `docs/architecture.md` and a professional project tree.
- Defined initial role metadata in `data/roles.json` following least-privilege principles.
- Added placeholder directories: `app/`, `tests/`, and `screenshots/` for future development.

## Sprint 2

- Implemented the employee identity data model using Python `dataclasses` in `app/models.py`.
- Added an initially empty employee store: `data/employees.json`.
- Added unit tests for the model in `tests/test_models.py` and verified model serialization (`to_dict` / `from_dict`).
- Ensured defaults: `status="active"`, empty `groups` and `applications`.

## Sprint 3

- Implemented the Joiner workflow in `app/iam_service.py` with `create_employee()`.
- `create_employee()` validates required fields, rejects duplicate IDs, assigns roles (groups/applications) from `data/roles.json`, generates unique usernames, and persists to `data/employees.json`.
- Added comprehensive tests in `tests/test_joiner.py` covering successful creation, validation failures, username generation and collision handling, and role assignment.
- Added `app/demo.py` to exercise the Joiner workflow manually.

## Sprint 4

- Implemented the Mover workflow (`update_employee_role`) in `app/iam_service.py` to change an employee's `job_title`, `groups`, and `applications` while preserving `employee_id`, `username`, `manager`, and `department`.
- Added tests in `tests/test_mover.py` covering successful moves, not-found handling, invalid roles, and verification that `username` and `employee_id` remain unchanged.
- All mover tests passed locally using `pytest`.

---

This changelog summarizes completed work through Sprint 4 and is intended to provide a concise historical record for future contributors and reviewers.
