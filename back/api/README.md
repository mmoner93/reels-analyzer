# Backend API Module

FastAPI REST API for managing Instagram Reel processing tasks.

## Structure

```
api/
└── src/api/
    ├── main.py         # FastAPI application
    ├── routes.py       # API endpoints
    ├── models.py       # SQLAlchemy models
    ├── schemas.py      # Pydantic schemas
    ├── database.py     # Database configuration
    └── config.py       # Settings
```

## Running the API

```bash
# From repository root
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Create Task
```http
POST /api/tasks
Content-Type: application/json

{
  "url": "https://www.instagram.com/reel/..."
}
```

### List Tasks
```http
GET /api/tasks
```

### Get Task
```http
GET /api/tasks/{task_id}
```

### Cancel Task
```http
PATCH /api/tasks/{task_id}/cancel
```

### Get Transcript
```http
GET /api/tasks/{task_id}/transcript
```

## Testing

```bash
# Run API tests
uv run pytest back/tests/src/tests/test_api.py -v
```
