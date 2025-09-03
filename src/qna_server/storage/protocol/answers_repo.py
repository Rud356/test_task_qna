from abc import abstractmethod
from typing import Protocol, runtime_checkable

from qna_server.dto import Answer, CreateAnswer


@runtime_checkable
class AnswersRepository(Protocol):
    @abstractmethod
    async def create_answer(self, question_id: int, answer_content: CreateAnswer) -> Answer:
        """
        Creates new answer for a question.

        :param question_id: ID of a question that answer will be connected to.
        :param answer_content: Content of an answer.
        :return: Answer details after creating record.
        :raises DataIntegrityError: If question that answer is linked to does not exist.
        """

    @abstractmethod
    async def fetch_answer_by_id(self, answer_id: int) -> Answer | None:
        """
        Fetches an answer by the specified ID.

        :param answer_id: ID of an answer to fetch.
        :return: Answer information or None.
        """

    @abstractmethod
    async def delete_answer(self, answer_id: int) -> bool:
        """
        Delete an answer from database.

        :param answer_id: ID of an answer to be deleted.
        :return: Flag that signifies if answer was deleted.
        :raises NotFoundError: If answer was not found by ID to be deleted.
        """
