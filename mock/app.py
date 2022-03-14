import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from mock.misc.config import environment
from mock.pedidosya.app import pedidosya

fastAPILogger = logger


def mount_sub_apps(app: FastAPI) -> None:
    app.mount("/pedidosya", pedidosya)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Platforms Fake API",
        description="Mock API",
    )
    mount_sub_apps(app)
    return app


if __name__ == "__main__":
    uvicorn.run(
        "mock.app:create_app",
        host="0.0.0.0",
        port=environment.PORT,
        log_level="info",
        reload=True,
    )
