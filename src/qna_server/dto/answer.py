from datetime import datetime

from pydantic import BaseModel, Field


class Answer(BaseModel):
    """
    Answer model for specific question.
    """

    answer_id: int = Field(
        alias="id",
        description="ID of an answer"
    )
    question_id: int = Field(
        description="ID of a question specific answer is for"
    )
    text: str = Field(
        min_length=1,
        max_length=2048,
        description="Answer text"
    )
    created_at: datetime = Field(
        description="When the answer was created"
    )
