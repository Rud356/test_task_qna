from datetime import datetime

from pydantic import BaseModel, Field


class Answer(BaseModel):
    """
    Answer model for specific question.
    """

    id: int = Field(
        description="ID of an answer"
    )
    question_id: int = Field(
        description="ID of a question specific answer is for"
    )
    user_id: str = Field(
        min_length=1,
        max_length=320,
        examples=["User 1", "user@example.com"]
    )
    text: str = Field(
        min_length=1,
        max_length=2048,
        description="Answer text",
        examples=["Answer to a question is 42"]
    )
    created_at: datetime = Field(
        description="When the answer was created"
    )
