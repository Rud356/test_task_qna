import logging
from typing import Optional, Sequence

from sqlalchemy import Result, Select, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import StaleDataError

from qna_server.dto import Answer, CreateQuestion, Question
from qna_server.dto.questions_with_answers import QuestionWithAnswers
from qna_server.exceptions import NotFoundError
from qna_server.storage.protocol import QuestionsRepository
from qna_server.storage.sqla_implementation.tables import QuestionTable
from qna_server.storage.sqla_implementation.transaction_manager_sqla import TransactionManagerSQLA
from qna_server.types import ContextID, LoggingContext, generate_context_id


class QuestionsRepositorySQLA(QuestionsRepository):
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
        self.logging_ctx = LoggingContext(context_id=self.context_id)

    async def create_new_question(self, question_content: CreateQuestion) -> Question:
        async with self.transaction as tr:
            self.logger.debug(
                "Creating new question",
                extra=self.logging_ctx
            )
            new_question: QuestionTable = QuestionTable(
                text=question_content.text
            )
            tr.add(new_question)
            await tr.commit()

        self.logger.debug(
            "Question was successfully created",
            extra=self.logging_ctx
        )
        return Question(
            id=new_question.id,
            text=new_question.text,
            created_at=new_question.created_at
        )

    async def get_all_questions(self) -> list[Question]:
        async with self.transaction as tr:
            self.logger.info(
                "Fetching questions",
                extra=self.logging_ctx
            )

            query: Select[tuple[QuestionTable]] = (
                select(QuestionTable)
                .order_by(QuestionTable.created_at)
            )
            results: Result[tuple[QuestionTable]] = await tr.execute(query)
            fetched_questions: Sequence[QuestionTable] = results.scalars().all()

        questions_list: list[Question] = []
        for question in fetched_questions:
            self.logger.debug(
                f"Processing question with ID={question.id}",
                extra=self.logging_ctx
            )

            current_question: Question = Question(id=question.id, text=question.text, created_at=question.created_at)
            questions_list.append(current_question)

            self.logger.debug(
                f"Processed {current_question}",
                extra=self.logging_ctx
            )

        self.logger.info(
            f"Fetched {len(questions_list)} questions",
            extra=self.logging_ctx
        )
        return questions_list

    async def fetch_specific_question(self, question_id: int) -> QuestionWithAnswers | None:
        self.logger.info(
        f"Fetching question with ID={question_id}",
            extra=self.logging_ctx
        )
        async with self.transaction as tr:
            query: Select[tuple[QuestionTable]] = (
                select(QuestionTable).options(
                    selectinload(QuestionTable.answers)
                ).where(QuestionTable.id == question_id)
            )
            question: QuestionTable | None = (
                await tr.execute(query)
            ).scalar_one_or_none()

        if question is not None:
            answers_list = []

            for answer in question.answers:
                answers_list.append(
                    Answer(
                        id=answer.id,
                        question_id=answer.question_id,
                        user_id=answer.user_id,
                        text=answer.text,
                        created_at=answer.created_at
                    )
                )

            self.logger.info(
                f"Fetching question with ID={question_id} completed successfully",
                extra=self.logging_ctx
            )
            return QuestionWithAnswers(
                id=question.id,
                text=question.text,
                created_at=question.created_at,
                answers=answers_list
            )

        else:
            self.logger.info(
                f"Question with ID={question_id} not found",
                extra=self.logging_ctx
            )
            return None

    async def delete_question(self, question_id: int) -> bool:
        async with self.transaction as tr:
            self.logger.debug(
                f"Deleting question with ID={question_id}",
                extra=self.logging_ctx
            )

            try:
                query: Select[tuple[QuestionTable]] = (
                    select(QuestionTable)
                    .options(
                        selectinload(QuestionTable.answers)
                    )
                    .where(QuestionTable.id == question_id)
                )
                question: QuestionTable = (
                    await tr.execute(query)
                ).scalar_one()
                await tr.delete(question)
                await tr.commit()

            except NoResultFound as err:
                self.logger.warning(
                    f"Question for deletion was not found with ID={question_id}",
                    extra=self.logging_ctx
                )
                raise NotFoundError(f"Question with ID={question_id} not found") from err

            except (IntegrityError, StaleDataError):
                self.logger.exception(
                    "Unexpected exception caught related to data integrity when deleting",
                    extra=self.logging_ctx
                )
                raise

        return True
