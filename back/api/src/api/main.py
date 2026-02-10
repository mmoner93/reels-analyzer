from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.database import init_db
from api.routes import router

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix=settings.api_prefix)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {
        "message": "Instagram Reel Processor API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
