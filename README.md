# Enterprise IAM Platform

> Full-Stack Identity & Access Management (IAM) platform built with **FastAPI, React, SQLite, Docker, and GitHub Actions**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688)
![React](https://img.shields.io/badge/React-Vite-61DAFB)
![SQLite](https://img.shields.io/badge/SQLite-Persistence-003B57)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF)
![RBAC](https://img.shields.io/badge/RBAC-Implemented-success)
![IAM](https://img.shields.io/badge/Identity_Access_Management-Enterprise-blueviolet)
![Tests](https://img.shields.io/badge/Tests-100%2B-success)
![License](https://img.shields.io/badge/License-MIT-green)

Enterprise IAM is a production-style Identity & Access Management platform that automates employee lifecycle management through **Joiner, Mover, and Leaver (JML)** workflows. It demonstrates RBAC provisioning, authentication, audit logging, workforce analytics, persistent data storage, and enterprise-style administration using a modern React frontend and FastAPI backend.

---

# ✨ Features

- ✅ Authentication
- ✅ Joiner (Employee Onboarding)
- ✅ Mover (Role Changes)
- ✅ Leaver (Employee Termination)
- ✅ Role-Based Access Control (RBAC)
- ✅ Employee Directory
- ✅ Workforce Analytics Dashboard
- ✅ Audit Logging
- ✅ Global Employee Search
- ✅ CSV Export
- ✅ SQLite Persistent Storage
- ✅ Docker Deployment
- ✅ GitHub Actions CI/CD
- ✅ 100+ Automated Backend Tests

---

# 📸 Screenshots

### Login

> *(Insert login screenshot here)*

---

### Dashboard

> *(Insert dashboard screenshot here)*

---

### Employee Directory

> *(Insert employee directory screenshot here)*

---

### Joiner Workflow

> *(Insert create employee screenshot here)*

---

### Mover Workflow

> *(Insert change role screenshot here)*

---

### Audit Logs

> *(Insert audit logs screenshot here)*

---

# 🏗 Architecture

```
                    Browser
                        │
                        ▼
               React + Vite Frontend
                        │
                   REST API (HTTP)
                        ▼
                  FastAPI Backend
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     IAM Service     Audit Logs    SQLite
                        │
                        ▼
                  Employee Records
```

---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React, Vite |
| Backend | FastAPI |
| Database | SQLite |
| Authentication | Demo Authentication |
| Authorization | RBAC |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Testing | Pytest |
| API | REST |

---

# 📋 Project Overview

The platform simulates common enterprise IAM operations.

### Joiner

- Create employee identities
- Generate usernames
- Assign RBAC roles
- Provision groups
- Provision applications

### Mover

- Change employee role
- Remove previous permissions
- Assign new permissions
- Preserve identity information
- Record audit event

### Leaver

- Disable employee
- Remove group memberships
- Remove application access
- Update lifecycle status
- Preserve audit history

---

# 🌐 REST API

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/employees` | List employees |
| GET | `/employees/{employee_id}` | Employee details |
| POST | `/employees` | Create employee |
| POST | `/employees/{employee_id}/move` | Change employee role |
| POST | `/employees/{employee_id}/terminate` | Terminate employee |
| GET | `/roles` | List RBAC roles |
| GET | `/audit-logs` | View audit events |

Business logic lives in **app/iam_service.py** while API routing lives in **app/main.py**.

---

# 💻 Frontend

The React administration console includes:

- Executive Dashboard
- Employee Directory
- Employee Detail Drawer
- Joiner Workflow
- Mover Workflow
- Leaver Workflow
- Role Catalog
- Audit Logs
- Global Search
- CSV Export
- Responsive UI
- Toast Notifications

Configure the API:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

# 🚀 Running Locally

Install backend dependencies

```bash
python3 -m pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

Run React

```bash
cd frontend
npm install
npm run dev
```

Open

- Frontend → http://localhost:5173
- API Docs → http://localhost:8000/docs

---

# 🐳 Docker

Run both services

```bash
docker compose up --build
```

Services

- Frontend → http://localhost:3000
- Backend → http://localhost:8000

---

# ✅ Testing

Backend

```bash
python3 -m pytest -q
```

Current Status

- ✅ 100+ Backend Tests Passing
- ✅ Production Frontend Build Passing
- ✅ GitHub Actions CI/CD
- ✅ SQLite Persistence Verified

---

# ⚙️ CI/CD

GitHub Actions automatically executes on every Push and Pull Request.

Pipeline

- Install Python dependencies
- Execute backend test suite
- Install frontend dependencies
- Generate production React build

---

# 📁 Folder Structure

```
enterprise-iam-lab/
├── app/
├── frontend/
├── tests/
├── docs/
├── data/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🚧 Roadmap

- [x] Joiner Workflow
- [x] Mover Workflow
- [x] Leaver Workflow
- [x] RBAC Provisioning
- [x] Authentication
- [x] Workforce Analytics
- [x] Audit Logging
- [x] Global Search
- [x] CSV Export
- [ ] Microsoft Entra ID Integration
- [ ] Okta API Integration
- [ ] SCIM Provisioning
- [ ] Multi-Factor Authentication
- [ ] Access Review Campaigns
- [ ] Approval Workflows
- [ ] Live Cloud Deployment

---

# 👨‍💻 Author

**Abdulaziz Abdi**

- LinkedIn: https://linkedin.com/in/abdulaziz-abdi
- GitHub: https://github.com/Abdulaziz998

---

# 📄 License

This project is licensed under the MIT License.
