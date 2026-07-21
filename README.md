# Enterprise IAM Platform

Enterprise IAM is a production-style identity administration lab for Joiner, Mover, and Leaver workflows. It combines a FastAPI backend, SQLite-backed employee persistence, audit logging, RBAC role definitions, and a React administration console.

## Project Overview

The platform models common IAM operations:

- Create employees and assign access from role definitions.
- Move employees between roles while preserving identity fields.
- Terminate employees by removing access and updating status.
- Review employee records, role coverage, and audit events.

The project is designed for portfolio-quality engineering practice: tested backend workflows, a polished frontend console, Dockerized services, and CI checks.

## Architecture

```
React + Vite frontend  --->  FastAPI backend  --->  IAM service
       |                         |                    |
       |                         |                    +-- RBAC roles JSON
       |                         |                    +-- audit log JSON
       |                         |
       |                         +-- SQLite employee database
       |
       +-- Nginx production container
```

## Backend

The backend is a FastAPI service exposing existing IAM endpoints:

- `GET /employees`
- `GET /employees/{employee_id}`
- `POST /employees`
- `POST /employees/{employee_id}/move`
- `POST /employees/{employee_id}/terminate`
- `GET /roles`
- `GET /audit-logs`

Business logic lives in `app/iam_service.py`; API routing lives in `app/main.py`.

## Frontend

The frontend is a React + Vite administration console in `frontend/`. It provides:

- Dashboard KPIs and operational panels.
- Employee directory and detail drawer.
- Create Employee, Change Role, and Terminate Employee workflows.
- Role catalog and audit log views.
- Toast notifications and production-style loading/error states.

Set the API URL with:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

See `frontend/.env.example`.

## Running Locally

Install backend dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

## Docker

Build and run both services:

```bash
docker compose up --build
```

Services:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

The frontend production build is served by Nginx. The Vite API base URL is injected at build time through `VITE_API_BASE_URL`.

## Running Tests

Backend tests:

```bash
python3 -m pytest -q
```

Frontend production build:

```bash
cd frontend
npm install
npm run build
```

## CI/CD

GitHub Actions runs on `push` and `pull_request`.

Pipeline jobs:

- Backend: install Python dependencies and run `python3 -m pytest -q`.
- Frontend: install Node dependencies and run `npm run build`.

## Folder Structure

```
enterprise-iam-lab/
├── app/                      # FastAPI routes and IAM business logic
├── data/                     # Roles, employees, audit data
├── docs/                     # Architecture notes
├── frontend/                 # React + Vite admin console
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .env.example
├── tests/                    # Pytest backend test suite
├── Dockerfile                # Backend container
├── docker-compose.yml        # Backend + frontend services
├── requirements.txt
└── README.md
```

## Screenshots

Placeholder for dashboard, employee drawer, role catalog, and audit log screenshots.

## Future Roadmap

- Add seeded demo data reset workflow.
- Add API-level authentication and admin roles.
- Add deployment manifests for cloud environments.
- Add structured audit export and retention controls.
- Integrate with Microsoft Entra ID or Okta sandbox tenants.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
