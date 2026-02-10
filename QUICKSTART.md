# Quick Start Guide

## Prerequisites

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y ffmpeg redis-server

# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

```bash
cd /path/to/reels-analyzer

# Install all dependencies
uv sync
```

## Running the Application

### Terminal 1: Start Redis
```bash
redis-server
```

### Terminal 2: Start API Server
```bash
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3: Start Celery Worker
```bash
uv run celery -A processor.tasks worker --loglevel=info
```

### Terminal 4: Start Frontend
```bash
cd front
pnpm install
pnpm dev
```

## Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Testing

```bash
# Backend tests
uv run pytest back/tests/ -v

# Frontend tests
cd front && pnpm test
```

## Usage

1. Open http://localhost:5173 in your browser
2. Click "Add New Task"
3. Paste an Instagram Reel URL
4. Click "Add Task"
5. Watch the status change: pending → processing → completed
6. Click "View Transcript" when completed
7. View the transcript, detected language, and extracted topics

## Troubleshooting

**Redis not running:**
```bash
redis-cli ping  # Should return PONG
```

**Port already in use:**
```bash
# Change API port
uv run uvicorn api.main:app --reload --port 8001

# Change frontend port
cd front && pnpm dev --port 5174
```

**Tests failing:**
```bash
# Make sure you're in the root directory
cd /path/to/reels-analyzer
uv sync --all-packages
uv run pytest back/tests/ -v
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for architecture details
- Explore API docs at http://localhost:8000/docs
