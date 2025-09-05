from pydantic import Field

from .answer import Answer
from .question import Question


class QuestionWithAnswers(Question):
    answers: list[Answer] = Field(
        description="Answers to specified question",
        examples=["Answer to a question is 42"]
    )
