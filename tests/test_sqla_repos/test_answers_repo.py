from qna_server.exceptions import DataIntegrityError, NotFoundError
from .fixtures import *

from qna_server.dto import Answer, CreateAnswer, CreateQuestion, Question, QuestionWithAnswers
from qna_server.storage.sqla_implementation import QuestionsRepositorySQLA

@pytest.fixture(scope="function")
async def question(
    test_question: str,
    question_repo: QuestionsRepositorySQLA
) -> Question:
    return await question_repo.create_new_question(
        CreateQuestion(text=test_question)
    )


@pytest.fixture(scope="function")
async def answer_data(
    question: Question,
    test_answer: str,
    response_author: str,
    answers_repo: AnswerRepositorySQLA
) -> Answer:
    created_answer: Answer = await answers_repo.create_answer(
        question.id,
        CreateAnswer(
            text=test_answer,
            user_id=response_author
        )
    )
    return created_answer


async def test_creating_answer(
    question: Question,
    test_answer: str,
    response_author: str,
    answers_repo: AnswerRepositorySQLA
):
    created_answer: Answer = await answers_repo.create_answer(
        question.id,
        CreateAnswer(
            text=test_answer,
            user_id=response_author
        )
    )
    assert created_answer.question_id == question.id
    assert created_answer.user_id == response_author
    assert f"Answer is: {created_answer.text}" == question.text


async def test_creating_answer_to_non_existing_question(
    test_answer: str,
    response_author: str,
    answers_repo: AnswerRepositorySQLA
):
    with pytest.raises(DataIntegrityError):
        await answers_repo.create_answer(
            1<<31 - 1,
            CreateAnswer(
                text=test_answer,
                user_id=response_author
            )
        )


async def test_fetching_answer_by_id(
    answer_data: Answer,
    answers_repo: AnswerRepositorySQLA
):
    assert answer_data == await answers_repo.fetch_answer_by_id(answer_data.id)


async def test_deleting_answer(
    answer_data: Answer,
    answers_repo: AnswerRepositorySQLA
):
    assert answer_data == await answers_repo.fetch_answer_by_id(answer_data.id)
    assert await answers_repo.delete_answer(answer_data.id)
    assert await answers_repo.fetch_answer_by_id(answer_data.id) is None


async def test_deleting_non_existing_answer(
    answers_repo: AnswerRepositorySQLA
):
    with pytest.raises(NotFoundError):
        await answers_repo.delete_answer(1<<31 - 1)


async def test_deleting_question_and_answers(
    answer_data: Answer,
    answers_repo: AnswerRepositorySQLA,
    question_repo: QuestionsRepositorySQLA
):
    assert answer_data == await answers_repo.fetch_answer_by_id(answer_data.id)
    assert await question_repo.delete_question(answer_data.question_id)

    assert await question_repo.fetch_specific_question(answer_data.question_id) is None
    assert await answers_repo.fetch_answer_by_id(answer_data.id) is None


async def test_deleting_question_and_multiple_answers(
    answer_data: Answer,
    answers_repo: AnswerRepositorySQLA,
    question_repo: QuestionsRepositorySQLA
):
    created_answer: Answer = await answers_repo.create_answer(
        answer_data.question_id,
        CreateAnswer(
            text="Demo answer 123",
            user_id="42"
        )
    )
    answers_listed: list[Answer] = (await question_repo.fetch_specific_question(answer_data.question_id)).answers

    assert answer_data in answers_listed
    assert created_answer in answers_listed

    assert answer_data == await answers_repo.fetch_answer_by_id(answer_data.id)
    assert await question_repo.delete_question(answer_data.question_id)

    assert await question_repo.fetch_specific_question(answer_data.question_id) is None
    assert await answers_repo.fetch_answer_by_id(answer_data.id) is None
    assert await answers_repo.fetch_answer_by_id(created_answer.id) is None
