from fastapi import APIRouter

# Router Initialization
health_router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])

# Healthcheck Endpoint
@health_router.get("/")
async def healthcheck():
    return {"status": "ok", "message": "API is operational"}
