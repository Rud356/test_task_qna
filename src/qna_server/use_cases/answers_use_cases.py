import logging
from typing import Optional

from qna_server.dto import Answer, CreateAnswer
from qna_server.storage.protocol import AnswersRepository
from qna_server.custom_types import ContextID, LoggingContext, generate_context_id


class AnswersUseCases:
    def __init__(
        self,
        answers_repo: AnswersRepository,
        context_id: Optional[ContextID] = None
    ):
        if context_id:
            self.context_id: ContextID = context_id

        else:
            self.context_id = generate_context_id()

        self.answers_repo: AnswersRepository = answers_repo
        self.logger: logging.Logger = logging.getLogger("qna_logger")
        self.logging_ctx = LoggingContext(context_id=self.context_id)

    async def create_answer(self, question_id: int, answer_content: CreateAnswer) -> Answer:
        """
        Creates new answer for a question.

        :param question_id: ID of a question that answer will be connected to.
        :param answer_content: Content of an answer.
        :return: Answer details after creating record.
        :raises DataIntegrityError: If question that answer is linked to does not exist.
        """

        self.logger.info(
            f"Creating new answer with {answer_content=}",
            extra=self.logging_ctx
        )
        return await self.answers_repo.create_answer(question_id, answer_content)

    async def fetch_answer_by_id(self, answer_id: int) -> Answer | None:
        """
        Fetches an answer by the specified ID.

        :param answer_id: ID of an answer to fetch.
        :return: Answer information or None.
        """
        self.logger.info(
            f"Fetching answer with {answer_id=}",
            extra=self.logging_ctx
        )
        return await self.answers_repo.fetch_answer_by_id(answer_id)

    async def delete_answer(self, answer_id: int) -> bool:
        """
        Delete an answer from database.

        :param answer_id: ID of an answer to be deleted.
        :return: Flag that signifies if answer was deleted.
        :raises NotFoundError: If answer was not found by ID to be deleted.
        """
        self.logger.info(
            f"Deleting answer with {answer_id=}",
            extra=self.logging_ctx
        )
        return await self.answers_repo.delete_answer(answer_id)
