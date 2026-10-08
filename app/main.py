import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.endpoints import api_router
from app.config import get_settings
from app.schemas import HealthStatusResponse
from app.services.detector import detector_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()
BASE_DIR = Path(__file__).resolve().parent.parent


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown events."""
    logger.info(f"Initializing {settings.APP_NAME} v{settings.APP_VERSION}")
    try:
        detector_service.load_model()
        logger.info("Detector service successfully initialized.")
    except Exception as exc:
        logger.warning(
            f"Could not load detector model during startup: {exc}. "
            f"API will start but detection requests will return 503 until model is available."
        )

    yield

    logger.info("Shutting down application and releasing resources...")
    detector_service.unload()
    logger.info("Shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="High-performance AI text detection API powered by fine-tuned DistilRoBERTa token classification.",
    lifespan=lifespan,
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular API routers
app.include_router(api_router)


@app.get("/", summary="Serve Web Interface", include_in_schema=False)
def serve_frontend():
    """Serves the single-page application frontend."""
    html_path = BASE_DIR / "frontend" / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="frontend/index.html not found.")
    return FileResponse(html_path)


@app.get(
    "/health",
    response_model=HealthStatusResponse,
    tags=["System"],
    summary="Health check endpoint",
)
def health_check() -> HealthStatusResponse:
    """Returns application status, version, and model initialization state."""
    return HealthStatusResponse(
        status="healthy" if detector_service.is_loaded else "degraded",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        device=detector_service.device,
        model_loaded=detector_service.is_loaded,
    )