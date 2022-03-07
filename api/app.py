import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from tortoise.contrib.fastapi import register_tortoise

from .misc.config import TORTOISE_ORM, environment
from .misc.http import HTTPClient
from .misc.fastapi import catch_exceptions_middleware
from .presentation.resources import health_router, pedidosya_router


fastAPILogger = logger


async def on_start_up() -> None:
    fastAPILogger.info("on_start_up")
    HTTPClient.get_aiohttp_client()


async def on_shutdown() -> None:
    fastAPILogger.info("on_shutdown")
    await HTTPClient.close_aiohttp_client()


def set_sentry() -> None:
    pass


def set_resources(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(pedidosya_router)


def set_database(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=environment.POSTGRES_URI,
        modules={"models": ["api.data.postgres_models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="Palenca API",
        description="API of Core service",
        on_start_up=[on_start_up],
        on_shutdown=[on_shutdown],
    )
    set_resources(app)
    set_database(app)
    register_error_handler(app)
    set_sentry()
    return app


def register_error_handler(app: FastAPI):
    app.middleware("http")(catch_exceptions_middleware)


if __name__ == "__main__":
    uvicorn.run(
        "api.app:create_app",
        host="0.0.0.0",
        port=environment.PORT,
        log_level="info",
        reload=True,
    )
