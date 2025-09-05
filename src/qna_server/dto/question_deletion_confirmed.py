from pydantic import BaseModel


class QuestionDeletionConfirmation(BaseModel):
    question_id: int
    deleted: bool
