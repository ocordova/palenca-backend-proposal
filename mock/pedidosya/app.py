from fastapi import FastAPI
from fastapi.logger import logger

from mock.pedidosya.misc.fastapi import catch_exceptions_middleware
from mock.pedidosya.presentation.resources import pedidosya_router

fastAPILogger = logger

pedidosya = app = FastAPI(
    title="PedidosYa API",
    description="Mock API",
)

app.include_router(pedidosya_router)

app.middleware("http")(catch_exceptions_middleware)
