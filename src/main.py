from fastapi import FastAPI
from routers import router
from connections.keycloak_connection import idp
from .core.config import PROJECT_VERSION
from .core.exception_handlers import exception_handlers
from .core.middlewares import middlewares
from .core.http_responses import error_responses

app = FastAPI(
    title = "API de Autenticação e Autorização com Keycloak",
    version = PROJECT_VERSION or "unknown",
    responses=error_responses,
    exception_handlers=exception_handlers,
    middleware=middlewares
)

app.include_router(router)

idp.add_swagger_config(app)
