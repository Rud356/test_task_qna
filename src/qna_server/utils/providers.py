from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from qna_server.storage.protocol import AnswersRepository, QuestionsRepository, TransactionManager
from qna_server.storage.sqla_implementation import (
    AnswerRepositorySQLA,
    QuestionsRepositorySQLA,
    TransactionManagerSQLA,
)
from qna_server.types import ContextID, generate_context_id
from qna_server.use_cases.answers_use_cases import AnswersUseCases
from qna_server.use_cases.questions_use_cases import QuestionsUseCases
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


class RequestContextIdentifierProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_request_id(self) -> ContextID:
        return generate_context_id()


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
    def _get_transaction_manager(self) -> TransactionManagerSQLA:
        return TransactionManagerSQLA(self.session_maker)

    @provide(scope=Scope.REQUEST)
    def get_questions_repository(
        self,
        transaction: TransactionManagerSQLA,
        context_id: ContextID
    ) -> QuestionsRepository:
        return QuestionsRepositorySQLA(transaction, context_id)

    @provide(scope=Scope.REQUEST)
    def get_answers_repository(
        self,
        transaction: TransactionManagerSQLA,
        context_id: ContextID
    ) -> AnswersRepository:
        return AnswerRepositorySQLA(transaction, context_id)


class UseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_questions_use_cases(
        self,
        questions_repo: QuestionsRepository,
        context_id: ContextID
    ) -> QuestionsUseCases:
        return QuestionsUseCases(questions_repo, context_id)

    @provide(scope=Scope.REQUEST)
    def get_answers_use_cases(
        self,
        answers_repo: AnswersRepository,
        context_id: ContextID
    ) -> AnswersUseCases:
        return AnswersUseCases(answers_repo, context_id)
