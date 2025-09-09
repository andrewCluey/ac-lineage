from fastapi import APIRouter
from api.routes.entities import router as entities_router

api_router = APIRouter(prefix="/api")
api_router.include_router(entities_router, prefix="/entities", tags=["entities"])


