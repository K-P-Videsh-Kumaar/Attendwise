# AttendWise API

FastAPI backend for student-managed attendance planning. It deliberately does not represent an official college record.

## Run

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Interactive API docs: `http://127.0.0.1:8000/docs`.

## Test

```bash
pytest
```

Set `ATTENDWISE_JWT_SECRET` to a strong secret before deployment and set `ATTENDWISE_CORS_ORIGINS` to the deployed frontend origin.
