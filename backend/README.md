# StratumWeb Backend API

Professional FastAPI backend with async SQLAlchemy, email notifications,
and SQLite/PostgreSQL support.

## Setup

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deployment (Render)

1. Create a Web Service
2. Root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env vars from `.env.example`
