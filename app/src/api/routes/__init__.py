from fastapi import APIRouter
from api.routes import model, health

router = APIRouter()
router.include_router(model.router, tags=["Model"])
router.include_router(health.router, tags=["Health"])
