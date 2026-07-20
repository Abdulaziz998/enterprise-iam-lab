# Enterprise IAM Dashboard

A polished React dashboard for the Enterprise IAM Lifecycle Lab.

## Backend startup

```bash
python3 -m uvicorn app.main:app --reload
```

## Frontend startup

```bash
cd frontend
npm install
npm run dev
```

## Environment setup

```bash
cp .env.example .env
```

The frontend reads the backend URL from `VITE_API_BASE_URL`.
