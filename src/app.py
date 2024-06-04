from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from routes import items

from db.database import session_manager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if session_manager._engine is not None:
        # Close the DB connection
        await session_manager.close()

app = FastAPI(
    title="MySuperAPI",
    openapi_url=f"/v1/openapi.json",
    lifespan=lifespan,
)

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

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)