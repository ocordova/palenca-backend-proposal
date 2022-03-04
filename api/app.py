import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


from .misc.config import TORTOISE_ORM, environment
from .misc.fastapi import catch_exceptions_middleware
from .presentation.resources import health_router, indriver_router


def set_sentry() -> None:
    pass


def set_resources(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(indriver_router)


def set_database(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url="postgres://postgres:@host.docker.internal:5432/palenca_neue",
        modules={"models": ["api.data.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def create_app() -> FastAPI:
    app = FastAPI(title="Palenca API", description="API of Core service")
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
