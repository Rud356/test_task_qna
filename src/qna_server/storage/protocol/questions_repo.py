from abc import abstractmethod
from typing import Protocol, runtime_checkable

from qna_server.dto import CreateQuestion, Question
from qna_server.dto.questions_with_answers import QuestionWithAnswers


@runtime_checkable
class QuestionsRepository(Protocol):
    @abstractmethod
    async def create_new_question(
        self,
        question_content: CreateQuestion
    ) -> Question:
        """
        Creates new question in system.

        :param question_content: Content of a question.
        :return: Created question.
        """

    @abstractmethod
    async def get_all_questions(self) -> list[Question]:
        """
        Returns a list of all registered questions.

        :return: List of questions.
        """

    @abstractmethod
    async def fetch_specific_question(self, question_id: int) -> QuestionWithAnswers | None:
        """
        Fetches question by its ID.

        :param question_id: ID of a question.
        :return: Question if it was found or None.
        """

    @abstractmethod
    async def delete_question(self, question_id: int) -> bool:
        """
        Deletes question and related answers.

        :param question_id: Question ID of object to delete.
        :return: Flag signifying if question was deleted successfully.
        :raises NotFoundError: If question was not found by ID to be deleted.
        """
