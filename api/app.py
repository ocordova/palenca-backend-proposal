import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .misc.env import is_production, is_staging, TORTOISE_ORM, Env
from .presentation.resources import health, indriver


def set_sentry() -> None:
    pass


def set_resources(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(indriver.router)


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
    set_sentry()
    return app


if __name__ == "__main__":
    uvicorn.run("api.app:create_app", host="0.0.0.0", port=Env.PORT, log_level="info")
