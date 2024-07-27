from fastapi import APIRouter

from app.api.routers import health, organizations, users

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(organizations.router)
