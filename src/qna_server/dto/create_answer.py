from pydantic import BaseModel, Field


class CreateAnswer(BaseModel):
    """
    Answer creation body model for transferring data.
    """
    text: str = Field(
        min_length=1,
        max_length=2048,
        pattern=r"^(\S.+){1,2048}",
        description="Answer text that must start from non-whitespace character",
        examples=["Answer to a question is 42"]
    )
    user_id: str = Field(
        min_length=1,
        max_length=320,
        pattern=r"^(\S.+){1,320}",
        description="User who writes a response",
        examples=["User 1", "user@example.com"]
    )
