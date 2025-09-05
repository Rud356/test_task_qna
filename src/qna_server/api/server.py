import uvicorn
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from starlette.middleware.cors import CORSMiddleware

from qna_server.api.endpoints import (
    api,
    answers_endpoints, # noqa: F401 user for assigning routes
    questions_endpoints, # noqa: F401 user for assigning routes
)
from qna_server.utils.config_schema import AppConfig
from qna_server.utils.providers import (
    AppConfigProvider,
    DatabaseSQLAReposProvider,
    RequestContextIdentifierProvider,
    UseCasesProvider,
)


def setup_app(config: AppConfig) -> FastAPI:
    """
    Prepares application for launching.

    :param config: Configuration of an app.
    :return: FastAPI Application.
    """
    app: FastAPI = FastAPI(
        title="Demo API of resource management",
        host=config.host,
        port=config.port
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_cors_domains,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    engine: AsyncEngine = create_async_engine(config.db_settings.connection_string)

    container: AsyncContainer = make_async_container(
        AppConfigProvider(config),
        DatabaseSQLAReposProvider(engine),
        RequestContextIdentifierProvider(),
        UseCasesProvider()
    )
    setup_dishka(container=container, app=app)
    app.include_router(api)

    return app


def main(config: AppConfig) -> None:
    """
    Main entry point.

    :param config: App configuration.
    :return: Nothing.
    """
    app: FastAPI = setup_app(config)

    uvicorn.run(
        app,
        host=config.host,
        port=config.port
    )
