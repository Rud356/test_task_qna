import logging
from typing import Optional

from qna_server.dto import CreateQuestion, Question, QuestionWithAnswers
from qna_server.exceptions import NotFoundError
from qna_server.storage.protocol import QuestionsRepository
from qna_server.custom_types import ContextID, LoggingContext, generate_context_id


class QuestionsUseCases:
    def __init__(
        self,
        question_repo: QuestionsRepository,
        context_id: Optional[ContextID] = None
    ):
        if context_id:
            self.context_id: ContextID = context_id

        else:
            self.context_id = generate_context_id()

        self.question_repo: QuestionsRepository = question_repo
        self.logger: logging.Logger = logging.getLogger("qna_logger")
        self.logging_ctx = LoggingContext(context_id=self.context_id)

    async def create_new_question(self, question_content: CreateQuestion) -> Question:
        """
        Creates a new question in database.

        :param question_content: Content of a question.
        :return: Question information.
        """
        self.logger.info(
            "Creating new question",
            extra=self.logging_ctx
        )

        new_question: Question = await self.question_repo.create_new_question(question_content)

        self.logger.info(
            f"New question successfully created with ID={new_question.id}",
            extra=self.logging_ctx
        )
        return new_question

    async def get_all_questions(self) -> list[Question]:
        """
        Fetches all questions information.

        :return: List of all questions.
        """
        self.logger.info(
            "Fetching all questions in database",
            extra=self.logging_ctx
        )
        return await self.question_repo.get_all_questions()

    async def fetch_specific_question(self, question_id: int) -> QuestionWithAnswers:
        """
        Fetch specific question by ID.

        :param question_id: ID of a question.
        :return: Question information with all answers related to it.
        :raise NotFoundError: If question was not found by specified ID.
        """
        self.logger.info(
            f"Fetching question by ID={question_id}",
            extra=self.logging_ctx
        )
        fetched_question_data: QuestionWithAnswers | None = await self.question_repo.fetch_specific_question(
            question_id
        )

        if fetched_question_data is None:
            self.logger.warning(
                f"Question with ID={question_id} not found",
                extra=self.logging_ctx
            )
            raise NotFoundError(f"Question with ID={question_id} not found")

        return fetched_question_data

    async def delete_question(self, question_id: int) -> bool:
        """
        Delete question and all related answers.

        :param question_id: ID of a question to be deleted.
        :return: Flag representing that question was deleted.
        :raise NotFoundError: Question was not found in database.
        """
        self.logger.info(
            f"Deleting question by ID={question_id}",
            extra=self.logging_ctx
        )

        return await self.question_repo.delete_question(question_id)
