import logging
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import models, login, predicts, users
from core.config import settings


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"  # type: ignore


# Add filter to the logger
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

app = FastAPI(
    title="Cells Backend",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
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

# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(predicts.router, prefix="/predict", tags=["predicts"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
