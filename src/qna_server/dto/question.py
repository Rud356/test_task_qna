from datetime import datetime

from pydantic import BaseModel, Field


class Question(BaseModel):
    """
    Questions model for transferring data.
    """

    id: int = Field(
        description="ID of a question"
    )
    text: str = Field(
        min_length=1,
        max_length=2048,
        description="Questions text"
    )
    created_at: datetime = Field(
        description="When the question was created"
    )
