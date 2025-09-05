from dishka import FromDishka
from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from qna_server.dto import CreateQuestion, Question, QuestionDeletionConfirmation, QuestionWithAnswers
from qna_server.exceptions import NotFoundError
from qna_server.use_cases import QuestionsUseCases
from .api_router import api


@api.get(
    "/questions/",
    description="Fetches all questions in system",
    responses={
        HTTP_200_OK: {
            "description": "Fetched all questions successfully"
        },
    },
    tags=["Questions"]
)
async def get_all_questions(
    questions_use_cases: FromDishka[QuestionsUseCases]
) -> list[Question]:
    questions: list[Question] = await questions_use_cases.get_all_questions()
    return questions


@api.post(
    "/questions/",
    description="Creates new question in system",
    responses={
        HTTP_201_CREATED: {
            "description": "Question created successfully"
        },
    },
    status_code=HTTP_201_CREATED,
    tags=["Questions"]
)
async def create_new_question(
    body: CreateQuestion,
    questions_use_cases: FromDishka[QuestionsUseCases]
) -> Question:
    created_question: Question = await questions_use_cases.create_new_question(
        body
    )

    return created_question


@api.get(
    "/questions/{question_id}",
    description="Fetches question with specific ID",
    responses={
        HTTP_200_OK: {
            "description": "Question data fetched successfully"
        },
        HTTP_404_NOT_FOUND: {
            "description": "Question was not found by provided ID"
        }
    },
    tags=["Questions"]
)
async def get_specific_question(
    question_id: int,
    questions_use_cases: FromDishka[QuestionsUseCases]
) -> QuestionWithAnswers:
    try:
        question_data: QuestionWithAnswers = await questions_use_cases.fetch_specific_question(
            question_id
        )

    except NotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Question with ID={question_id} not found"
        )

    return question_data


@api.delete(
    "/questions/{question_id}",
    description="Deletes question and related answers",
    responses={
        HTTP_200_OK: {
            "description": "Question was deleted successfully"
        },
        HTTP_404_NOT_FOUND: {
            "description": "Question was not found by provided ID"
        }
    },
    tags=["Questions"]
)
async def delete_question(
    question_id: int,
    questions_use_cases: FromDishka[QuestionsUseCases]
) -> QuestionDeletionConfirmation:
    try:
        deleted: bool = await questions_use_cases.delete_question(question_id)

    except NotFoundError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Question with specified ID does not exist"
        )

    return QuestionDeletionConfirmation(
        question_id=question_id,
        deleted=deleted
    )
