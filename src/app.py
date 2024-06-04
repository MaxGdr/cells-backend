from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from routes import items

# from app.api.main import api_router
# from app.core.config import settings


app = FastAPI(
    title="MySuperAPI",
    openapi_url=f"/v1/openapi.json",
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
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(api_router, prefix="/v1")