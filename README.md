# Instagram Reel Processor

A full-stack application for processing Instagram Reels with automatic transcription and text analysis.

## 🚀 Quick Start with Docker (Recommended)

```bash
# 1. Configure ports (optional)
cp .env.example .env
# Edit .env to customize FRONTEND_PORT, API_PORT, etc.

# 2. Start all services
docker-compose up -d --build

# 3. Access the application
# Web UI: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**That's it!** All services (Redis, API, Celery Worker, Frontend) are running.

📚 **Full Docker documentation**: [DOCKER.md](DOCKER.md)

## Alternative: Local Development Setup

See [QUICKSTART.md](QUICKSTART.md) for manual installation without Docker.

## Architecture

### Backend (Python + FastAPI + Celery)
- **API**: FastAPI REST API for task management
- **Processor**: Asynchronous processing pipeline using Celery
- **Database**: SQLite for task storage

### Frontend (Vue 3 + TypeScript)
- **Framework**: Vue 3 with Composition API and TypeScript
- **Build Tool**: Vite
- **Testing**: Vitest

## Features

### Core Features
- ✅ Add Instagram Reel URL for processing
- ✅ Asynchronous video download (yt-dlp)
- ✅ Audio extraction from video (ffmpeg)
- ✅ Speech-to-text transcription (OpenAI Whisper)
- ✅ Task status tracking (pending/processing/completed/failed/cancelled)
- ✅ Cancel running tasks
- ✅ View transcripts

### Bonus Features
- ✅ Language detection
- ✅ Topic extraction
- ✅ Real-time status updates (auto-refresh)
- ✅ Error handling and recovery

## Project Structure

```
reels-analyzer/
├── back/                      # Backend modules
│   ├── api/                   # FastAPI REST API
│   │   └── src/api/
│   │       ├── main.py        # FastAPI app
│   │       ├── routes.py      # API endpoints
│   │       ├── models.py      # Database models
│   │       ├── schemas.py     # Pydantic schemas
│   │       ├── database.py    # Database setup
│   │       └── config.py      # Configuration
│   ├── processor/             # Processing pipeline
│   │   └── src/processor/
│   │       ├── tasks.py       # Celery tasks
│   │       ├── downloader.py  # Video downloader
│   │       ├── audio_extractor.py  # Audio extraction
│   │       ├── transcriber.py # Speech-to-text
│   │       └── text_analyzer.py   # Language & topics
│   └── tests/                 # Backend tests
│       └── src/tests/
│           ├── test_api.py
│           └── test_processor.py
├── front/                     # Vue 3 frontend
│   └── src/
│       ├── components/        # Vue components
│       ├── views/             # Page views
│       ├── services/          # API client
│       └── __tests__/         # Frontend tests
├── pyproject.toml             # Python dependencies (uv)
└── README.md                  # This file
```

## Prerequisites

### For Docker Deployment (Recommended)
- Docker Engine 20.10+
- Docker Compose 2.0+

### For Local Development
- Python 3.11+
- Node.js 18+ (via nvm)
- pnpm
- Redis (for Celery)
- ffmpeg (for audio extraction)

### Install System Dependencies (Local Development Only)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y ffmpeg redis-server

# macOS
brew install ffmpeg redis
brew services start redis
```

## Quick Start

### Option 1: Docker (Recommended) 🐳

**Fastest way to get started:**

```bash
# 1. Clone the repository
git clone <repository-url>
cd reels-analyzer

# 2. Configure ports (optional)
cp .env.example .env
# Edit .env if you want to change default ports

# 3. Build and start all services
docker-compose up -d --build

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f
```

**Access the application:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Manage services:**
```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View specific service logs
docker-compose logs -f api
docker-compose logs -f celery-worker
```

📚 **Full Docker guide**: [DOCKER.md](DOCKER.md)

---

### Option 2: Local Development

For development without Docker, see [QUICKSTART.md](QUICKSTART.md).

### 1. Install uv (Python package manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup Backend (Local Development)

```bash
# Install Python dependencies
cd /path/to/reels-analyzer
uv sync

# Start Redis (if not already running)
redis-server

# Run database migrations (auto-creates tables)
# This happens automatically on first API start

# Start the API server
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# In a new terminal, start Celery worker
cd /path/to/reels-analyzer
uv run celery -A processor.tasks worker --loglevel=info
```

### 3. Setup Frontend (Local Development)

```bash
cd front
pnpm install
pnpm dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Running Tests

### Backend Tests

```bash
# Run all tests
uv run pytest back/tests/

# Run with coverage
uv run pytest back/tests/ --cov=api --cov=processor --cov-report=html
```

### Frontend Tests

```bash
cd front
pnpm test
```

## Processing Pipeline

1. **User submits Instagram Reel URL**
   - Frontend sends POST request to `/api/tasks`
   - Task created in database with status "pending"

2. **Celery worker picks up task**
   - Status updated to "processing"
   
3. **Download Video**
   - Uses yt-dlp to download the reel
   - Saved to temporary directory

4. **Extract Audio**
   - Uses ffmpeg to extract audio track
   - Converts to WAV format (16kHz, mono)

5. **Transcribe Audio**
   - Uses OpenAI Whisper (base model)
   - Generates text transcript

6. **Analyze Text** (Bonus)
   - Detects language using langdetect
   - Extracts key topics (keyword extraction)

7. **Complete Task**
   - Updates task status to "completed"
   - Stores transcript, language, and topics
   - Cleans up temporary files

## API Endpoints

- `POST /api/tasks` - Create a new processing task
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/{id}` - Get task details
- `PATCH /api/tasks/{id}/cancel` - Cancel a task
- `GET /api/tasks/{id}/transcript` - Get transcript
- `GET /health` - Health check

## Configuration

Backend configuration via environment variables (optional `.env` file):

```env
# API Settings
API_TITLE=Instagram Reel Processor
API_VERSION=1.0.0

# Database
DATABASE_URL=sqlite:///./reels.db

# Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Processing
TEMP_DIR=./temp

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: ORM for database operations
- **Celery**: Distributed task queue
- **Redis**: Message broker for Celery
- **yt-dlp**: Video download library
- **ffmpeg-python**: Audio extraction
- **OpenAI Whisper**: Speech-to-text
- **langdetect**: Language detection
- **pytest**: Testing framework

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **Axios**: HTTP client
- **Vitest**: Unit testing

## Troubleshooting

### Redis Connection Error
```bash
# Make sure Redis is running
redis-cli ping  # Should return PONG

# Start Redis if not running
redis-server
```

### Whisper Model Download
First time using Whisper will download the model (~150MB). This is automatic but may take a few minutes.

### FFmpeg Not Found
```bash
# Verify ffmpeg is installed
ffmpeg -version

# Install if missing (see Prerequisites)
```

### CORS Errors
Make sure the backend CORS settings include your frontend URL in `config.py`.

## License

MIT
