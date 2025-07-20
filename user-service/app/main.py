from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.logger import configure_logging
from app.lifespan import lifespan
from app.api.router import v1_router


def get_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    Instrumentator().instrument(app).expose(app, should_gzip=True)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router, prefix=settings.API_V1_STR)
    return app


app: FastAPI = get_app()


@app.get("/")
async def root():
    """
    Root endpoint. Returns a simple welcome message.
    """
    return {"message": "Welcome"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
