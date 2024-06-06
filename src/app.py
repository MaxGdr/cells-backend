import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import items

from db.database import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"  # type: ignore


# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

app = FastAPI(
    title="MySuperAPI",
    openapi_url="/v1/openapi.json",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(api_router, prefix="/v1")

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
