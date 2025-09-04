from .fixtures import *

from qna_server.dto import CreateQuestion, Question
from qna_server.storage.sqla_implementation import QuestionsRepositorySQLA


async def test_creating_question(test_question: str, question_repo: QuestionsRepositorySQLA):
    new_question: Question = await question_repo.create_new_question(
        CreateQuestion(text=test_question)
    )

    assert new_question.text == test_question
