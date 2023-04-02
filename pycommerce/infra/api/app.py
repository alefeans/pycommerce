from toolz import pipe
from fastapi import FastAPI
from pycommerce.config import Settings
from pycommerce.infra.api.routers import v1
from pycommerce.infra.api.routers import root


def create_instance(settings: Settings) -> FastAPI:
    return FastAPI(
        debug=settings.APP_DEBUG,
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )


def register_events(app: FastAPI) -> FastAPI:
    return app


def register_middlewares(app: FastAPI) -> FastAPI:
    return app


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    app.include_router(v1.router, prefix="/api/v1")
    return app


def create_app(settings: Settings) -> FastAPI:
    app: FastAPI = pipe(
        settings,
        create_instance,
        register_events,
        register_middlewares,
        register_routers,
    )
    return app
