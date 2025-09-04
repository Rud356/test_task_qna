from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from qna_server.storage.protocol import AnswersRepository, QuestionsRepository
from qna_server.storage.sqla_implementation import (
    AnswerRepositorySQLA,
    QuestionsRepositorySQLA,
    TransactionManagerSQLA,
)
from qna_server.utils.config_schema import AppConfig


class AppConfigProvider(Provider):
    """
    Provides application configuration
    """

    def __init__(self, app_config: AppConfig):
        super().__init__()
        self.app_config: AppConfig = app_config

    @provide(scope=Scope.REQUEST)
    def get_app_config(self) -> AppConfig:
        return self.app_config


class DatabaseSQLAReposProvider(Provider):
    def __init__(self, engine: AsyncEngine):
        super().__init__()
        self.engine: AsyncEngine = engine
        self.session_maker: async_sessionmaker[
            AsyncSession
        ] = async_sessionmaker(
            self.engine,
            expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    def get_transaction_manager(self) -> TransactionManagerSQLA:
        return TransactionManagerSQLA(self.session_maker)

    @provide(scope=Scope.REQUEST)
    def get_questions_repository(self, transaction: TransactionManagerSQLA) -> QuestionsRepository:
        return QuestionsRepositorySQLA(transaction)

    @provide(scope=Scope.REQUEST)
    def get_answers_repository(self, transaction: TransactionManagerSQLA) -> AnswersRepository:
        return AnswerRepositorySQLA(transaction)
