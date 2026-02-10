# Docker Deployment Guide

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Configure Ports

Copy the example environment file and customize ports:

```bash
cp .env.example .env
```

Edit `.env` to set your preferred ports:

```bash
# .env
FRONTEND_PORT=3000    # Web UI port
API_PORT=8000         # Backend API port
REDIS_PORT=6379       # Redis port (optional, for debugging)
```

### 2. Build and Start Services

```bash
# Build images and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f celery-worker
```

### 3. Access the Application

- **Web UI**: http://localhost:3000 (or your FRONTEND_PORT)
- **API**: http://localhost:8000 (or your API_PORT)
- **API Docs**: http://localhost:8000/docs

## Services

The docker-compose setup includes 4 services:

### 1. Redis
- **Image**: redis:7-alpine
- **Purpose**: Message broker for Celery
- **Port**: 6379 (configurable)
- **Data**: Persisted in `reels-redis-data` volume

### 2. API (FastAPI)
- **Image**: Built from Dockerfile.backend
- **Purpose**: REST API server
- **Port**: 8000 (configurable)
- **Depends on**: Redis
- **Volumes**: 
  - `./temp` - Temporary files for processing
  - `api_data` - SQLite database

### 3. Celery Worker
- **Image**: Built from Dockerfile.backend
- **Purpose**: Async task processing
- **Depends on**: Redis, API
- **Volumes**: Same as API (shared storage)

### 4. Frontend (Vue + Nginx)
- **Image**: Built from Dockerfile.frontend
- **Purpose**: Web UI
- **Port**: 80 → mapped to FRONTEND_PORT (default 3000)
- **Depends on**: API

## Network

All services run on a custom bridge network: `reels-analyzer-network`

This provides:
- Service discovery by name
- Isolation from other Docker networks
- Internal DNS resolution

## Management Commands

### Start Services
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### View Status
```bash
# List running services
docker-compose ps

# View resource usage
docker stats
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f celery-worker
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 api
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
docker-compose restart celery-worker
```

### Rebuild Images
```bash
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build api

# Rebuild and start
docker-compose up -d --build
```

## Health Checks

All services include health checks:

```bash
# Check service health
docker-compose ps

# Manually check API health
curl http://localhost:8000/health

# Manually check frontend health
curl http://localhost:3000/health

# Check Redis health
docker exec reels-redis redis-cli ping
```

## Volumes

### Named Volumes
- `reels-redis-data` - Redis persistence
- `reels-api-data` - SQLite database

### Bind Mounts
- `./temp` - Temporary processing files (shared between API and worker)

### Backup Database
```bash
# Backup SQLite database
docker cp reels-api:/app/data/reels.db ./backup-reels.db

# Restore database
docker cp ./backup-reels.db reels-api:/app/data/reels.db
docker-compose restart api celery-worker
```

## Troubleshooting

### Port Conflicts
If ports are already in use, change them in `.env`:

```bash
FRONTEND_PORT=3001
API_PORT=8001
REDIS_PORT=6380
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### View Service Logs
```bash
# API errors
docker-compose logs --tail=50 api

# Celery worker issues
docker-compose logs --tail=50 celery-worker

# Redis connection issues
docker-compose logs redis
```

### Celery Not Processing Tasks
```bash
# Check worker status
docker-compose logs celery-worker

# Restart worker
docker-compose restart celery-worker

# Check Redis connection
docker exec reels-redis redis-cli ping
```

### Database Issues
```bash
# Access SQLite database
docker exec -it reels-api sqlite3 /app/data/reels.db

# Run SQL query
sqlite> SELECT * FROM tasks;
sqlite> .quit
```

### Frontend Not Connecting to API
1. Check API is running: `docker-compose ps`
2. Check API health: `curl http://localhost:8000/health`
3. Check nginx config: `docker exec reels-frontend cat /etc/nginx/conf.d/default.conf`
4. View frontend logs: `docker-compose logs frontend`

### Clean Start
```bash
# Stop and remove everything
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## Production Considerations

### Security
1. **Don't expose Redis port** in production:
   ```yaml
   # Remove from redis service:
   # ports:
   #   - "${REDIS_PORT:-6379}:6379"
   ```

2. **Use environment variables** for sensitive data
3. **Enable HTTPS** with reverse proxy (nginx/traefik)
4. **Limit resource usage**:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

### Performance
1. **Increase Celery concurrency**:
   ```yaml
   command: uv run celery -A processor.tasks worker --loglevel=info --concurrency=4
   ```

2. **Use PostgreSQL** instead of SQLite:
   ```yaml
   environment:
     - DATABASE_URL=postgresql://user:pass@postgres:5432/reels
   ```

3. **Scale workers**:
   ```bash
   docker-compose up -d --scale celery-worker=3
   ```

### Monitoring
Add monitoring services:
```yaml
  prometheus:
    image: prom/prometheus
    # ... config

  grafana:
    image: grafana/grafana
    # ... config
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| FRONTEND_PORT | 3000 | Web UI access port |
| API_PORT | 8000 | Backend API port |
| REDIS_PORT | 6379 | Redis port |
| NODE_ENV | production | Node environment |
| PYTHONUNBUFFERED | 1 | Python output buffering |
| LOG_LEVEL | info | Logging level |

## Advanced Usage

### Custom Network
The compose file creates a custom network: `reels-analyzer-network`

To connect external services:
```bash
docker network connect reels-analyzer-network <container-name>
```

### Access Services from Other Containers
Services can communicate using service names:
- `http://api:8000`
- `redis://redis:6379`
- `http://frontend:80`

### Development with Docker
Mount source code for live reloading:
```yaml
api:
  volumes:
    - ./back:/app/back
  command: uv run uvicorn api.main:app --reload --host 0.0.0.0
```

## Updating

### Update Application Code
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update Dependencies
```bash
# Update Python deps
docker-compose build --no-cache api celery-worker

# Update Node deps
docker-compose build --no-cache frontend
```

## Cleanup

### Remove Unused Resources
```bash
# Remove stopped containers
docker-compose rm

# Remove unused volumes
docker volume prune

# Remove unused images
docker image prune
```

### Complete Cleanup
```bash
# Stop and remove everything
docker-compose down -v --rmi all

# Clean Docker system
docker system prune -a --volumes
```
