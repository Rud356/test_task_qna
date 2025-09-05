from dishka import FromDishka
from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from qna_server.dto import Answer, AnswerDeletionConfirmation, CreateAnswer
from qna_server.exceptions import DataIntegrityError, NotFoundError
from qna_server.use_cases import AnswersUseCases
from .api_router import api


@api.post(
    "/questions/{question_id}/answers/",
    description="Adds new answer to a question",
    responses={
        HTTP_201_CREATED: {
            "description": "Successfully created new answer to a question"
        },
        HTTP_404_NOT_FOUND: {
            "description": "Question was not found by provided ID, "
                           "creating answer is impossible"
        }
    },
    status_code=201,
    tags=["Answers"]
)
async def create_answer(
    question_id: int,
    body: CreateAnswer,
    answers_use_case: FromDishka[AnswersUseCases]
) -> Answer:
    try:
        return await answers_use_case.create_answer(
            question_id,
            body
        )

    except DataIntegrityError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Question not found to which answer is related"
        )


@api.get(
    "/answers/{answer_id}",
    description="Fetches information about specified answer to a question",
    responses={
        HTTP_200_OK: {
            "description": "Answer was found and fetched"
        },
        HTTP_404_NOT_FOUND: {
            "description": "Answer was not found by specified ID"
        }
    },
    tags=["Answers"]
)
async def fetch_answer_details(
    answer_id: int,
    answers_use_case: FromDishka[AnswersUseCases]
) -> Answer:
    answer_data: Answer | None = await answers_use_case.fetch_answer_by_id(answer_id)

    if answer_data is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Answer was not found by ID"
        )

    return answer_data


@api.delete(
    "/answers/{answer_id}",
    description="Deletes answer from system",
    responses={
        HTTP_200_OK: {
            "description": "Answer was deleted"
        },
        HTTP_404_NOT_FOUND: {
            "description": "Answer was not found by specified ID"
        }
    },
    tags=["Answers"]
)
async def delete_answer(
    answer_id: int,
    answers_use_case: FromDishka[AnswersUseCases]
) -> AnswerDeletionConfirmation:
    try:
        has_been_deleted: bool = await answers_use_case.delete_answer(
            answer_id
        )

    except NotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Answer was not found in system"
        )

    return AnswerDeletionConfirmation(
        answer_id=answer_id,
        deleted=has_been_deleted
    )
