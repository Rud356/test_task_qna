from pydantic import BaseModel, Field


class CreateQuestion(BaseModel):
    """
    Questions creation body model for transferring data.
    """
    text: str = Field(
        min_length=1,
        max_length=2048,
        pattern=r"^(\S.+){1,2048}",
        description="Questions text that must start from non-whitespace character"
    )
