from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from pycommerce.config import get_settings

router = APIRouter()


class HealthCheck(BaseModel):
    title: str = Field(..., description="API title")
    description: str = Field(..., description="Brief description of the API")
    version: str = Field(..., description="API semver version number")
    status: str = Field(..., description="API current status")


@router.get(
    "/health-check",
    status_code=200,
    tags=["Health Check"],
    response_model=HealthCheck,
    summary="Performs API health check",
    description="Performs health check and returns information about the API",
)
def health_check():
    settings = get_settings()
    return {
        "title": settings.APP_TITLE,
        "description": settings.APP_DESCRIPTION,
        "version": settings.APP_VERSION,
        "status": "I'm ok!",
    }
