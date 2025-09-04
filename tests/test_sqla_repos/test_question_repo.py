from qna_server.exceptions import NotFoundError
from .fixtures import *

from qna_server.dto import CreateQuestion, Question, QuestionWithAnswers
from qna_server.storage.sqla_implementation import QuestionsRepositorySQLA


async def test_creating_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    new_question: Question = await question_repo.create_new_question(
        CreateQuestion(text=test_question)
    )

    assert new_question.text == test_question


async def test_fetching_specific_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    created_question: Question = await question_repo.create_new_question(
        CreateQuestion(text=test_question)
    )
    fetched_question_data: QuestionWithAnswers = await question_repo.fetch_specific_question(
        created_question.id
    )

    assert created_question == Question(**fetched_question_data.model_dump())


async def test_fetching_not_existing_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    assert await question_repo.fetch_specific_question(
        1<<31 - 1
    ) is None


async def test_fetching_all_questions(test_question: str, question_repo: QuestionsRepositorySQLA):
    created_questions: list[Question] = [
        await question_repo.create_new_question(
            CreateQuestion(text=test_question)
        ),
        await question_repo.create_new_question(
            CreateQuestion(text=test_question)
        ),
        await question_repo.create_new_question(
            CreateQuestion(text=test_question)
        ),
    ]

    fetched_questions: list[Question] = await question_repo.get_all_questions()

    assert all(
        (question_created in fetched_questions for question_created in created_questions)
    )


async def test_deleting_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    created_question: Question = await question_repo.create_new_question(
        CreateQuestion(text=test_question)
    )
    fetched_question_data: QuestionWithAnswers = await question_repo.fetch_specific_question(
        created_question.id
    )

    assert created_question == Question(**fetched_question_data.model_dump())

    assert await question_repo.delete_question(fetched_question_data.id)
    assert await question_repo.fetch_specific_question(
        created_question.id
    ) is None


async def test_deleting_non_existing_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    assert await question_repo.fetch_specific_question(
        1 << 31 - 1
    ) is None

    with pytest.raises(NotFoundError):
        await question_repo.delete_question(1 << 31 - 1)
