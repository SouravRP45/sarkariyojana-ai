from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import logging
from contextlib import asynccontextmanager

from app.config import get_settings
from app.routers import schemes, chat
from app.services.data_loader import data_loader
from app.models import HealthResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB
    logger.info("Starting up SarkariYojana AI Backend...")
    data_loader.initialize_db()
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev. Restrict in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(schemes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        version=settings.APP_VERSION,
        schemes_loaded=len(data_loader.all_schemes)
    )

# Mount frontend static files
# In a real setup, make sure frontend path is correct relative to cwd
if os.path.exists(settings.FRONTEND_DIR):
    app.mount("/css", StaticFiles(directory=os.path.join(settings.FRONTEND_DIR, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(settings.FRONTEND_DIR, "js")), name="js")
    
    @app.get("/", response_class=HTMLResponse)
    async def serve_frontend():
        index_path = os.path.join(settings.FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Frontend not found at " + index_path
else:
    logger.warning(f"Frontend directory not found at {settings.FRONTEND_DIR}")
    @app.get("/")
    async def root():
        return {"message": "SarkariYojana AI API is running. Frontend not found."}
