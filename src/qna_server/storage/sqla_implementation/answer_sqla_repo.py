import logging
from typing import Optional

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm.exc import StaleDataError

from qna_server.dto import Answer, CreateAnswer
from qna_server.exceptions import DataIntegrityError, NotFoundError
from qna_server.storage.protocol import AnswersRepository
from qna_server.types import ContextID, LoggingContext, generate_context_id
from .tables import AnswerTable
from .transaction_manager_sqla import TransactionManagerSQLA


class AnswerRepositorySQLA(AnswersRepository):
    def __init__(
        self,
        transaction: TransactionManagerSQLA,
        context_id: Optional[ContextID] = None
    ):
        self.transaction: TransactionManagerSQLA = transaction
        if context_id:
            self.context_id: ContextID = context_id

        else:
            self.context_id = generate_context_id()

        self.logger: logging.Logger = logging.getLogger("qna_logger")

    async def create_answer(
        self, question_id: int, answer_content: CreateAnswer
    ) -> Answer:
        logging_ctx: LoggingContext = LoggingContext(context_id=self.context_id)
        self.logger.debug(
            f"Started creating the answer for question with ID={question_id}",
            extra=logging_ctx
        )

        async with self.transaction as tr:
            self.logger.debug(
                f"Creating object with provided data: {answer_content=}",
                extra=logging_ctx
            )

            new_answer = AnswerTable(
                question_id=question_id,
                user_id=answer_content.user_id,
                text=answer_content.text
            )

            try:
                self.logger.debug(
                    f"Successfully created the answer for question with ID={question_id}",
                    extra=logging_ctx
                )
                await tr.commit()

            except IntegrityError as err:
                self.logger.exception(
                    "Failed to create an answer to a question in database",
                    extra=logging_ctx
                )
                raise DataIntegrityError("Question does not exist to be linked to") from err

        self.logger.debug(
            f"Successfully created the answer for question with ID={question_id}",
            extra=logging_ctx
        )

        return Answer(
            id=new_answer.id,
            question_id=new_answer.question_id,
            user_id=new_answer.user_id,
            text=new_answer.text,
            created_at=new_answer.created_at
        )

    async def fetch_answer_by_id(self, answer_id: int) -> Answer | None:
        logging_ctx: LoggingContext = LoggingContext(context_id=self.context_id)

        async with self.transaction as tr:
            self.logger.debug(
                f"Fetching information for answer with id={answer_id}",
                extra=logging_ctx
            )
            answer_data: AnswerTable | None = await tr.get(AnswerTable, answer_id)

        if answer_data is not None:
            self.logger.debug(
                f"Successfully found answer with id={answer_data}",
                extra=logging_ctx
            )

            return Answer(
                id=answer_data.id,
                question_id=answer_data.question_id,
                user_id=answer_data.user_id,
                text=answer_data.text,
                created_at=answer_data.created_at
            )

        else:
            self.logger.debug(
                f"Answer with id={answer_data} not found",
                extra=logging_ctx
            )
            return None

    async def delete_answer(self, answer_id: int) -> bool:
        logging_ctx: LoggingContext = LoggingContext(context_id=self.context_id)

        async with self.transaction as tr:
            self.logger.debug(
                f"Fetching information for answer with id={answer_id} to be deleted",
                extra=logging_ctx
            )

            try:
                answer_data: AnswerTable = await tr.get_one(AnswerTable, answer_id)

            except NoResultFound as err:
                self.logger.exception("No answer with provided ID found", extra=logging_ctx)
                raise NotFoundError("Answer not found in database") from err

            try:
                await tr.delete(answer_data)
                await tr.commit()

            except StaleDataError as err:
                self.logger.exception("Exception while deleting data from DB", extra=logging_ctx)
                raise NotFoundError("Data was deleted before it could be found") from err

        return True
