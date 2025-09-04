import secrets
from pathlib import Path
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio  # noqa: enables async mode
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from qna_server.storage.sqla_implementation import (
    AnswerRepositorySQLA,
    QuestionsRepositorySQLA,
    TransactionManagerSQLA,
)
from qna_server.utils.config_schema import AppConfig, load_config


@pytest.fixture(scope="module")
def config() -> AppConfig:
    return load_config(Path(__file__).parent.parent / "test_config.toml")


@pytest.fixture()
async def engine(config: AppConfig) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(
        config.db_settings.connection_string,
        echo=False
    )

    return engine


@pytest.fixture()
async def session_maker(engine) -> async_sessionmaker[AsyncSession]:
    session_maker: async_sessionmaker[
        AsyncSession
    ] = async_sessionmaker(
        engine,
        expire_on_commit=False
    )

    return session_maker


@pytest.fixture()
async def session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="function")
def transaction(session_maker: async_sessionmaker[AsyncSession]) -> TransactionManagerSQLA:
    return TransactionManagerSQLA(session_maker)


@pytest.fixture(scope="function")
def question_repo(transaction: TransactionManagerSQLA) -> QuestionsRepositorySQLA:
    return QuestionsRepositorySQLA(transaction)


@pytest.fixture(scope="function")
def answers_repo(transaction: TransactionManagerSQLA) -> AnswerRepositorySQLA:
    return AnswerRepositorySQLA(transaction)


@pytest.fixture(scope='function')
def response_author() -> str:
    return f"demo_email_{secrets.token_urlsafe(16)}@example.com"


@pytest.fixture(scope='function')
def test_answer() -> str:
    return secrets.token_urlsafe(16)


@pytest.fixture(scope='function')
def test_question(test_answer: str) -> str:
    return f"Answer is: {test_answer}"
