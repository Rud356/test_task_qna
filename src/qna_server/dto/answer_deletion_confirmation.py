from pydantic import BaseModel


class AnswerDeletionConfirmation(BaseModel):
    answer_id: int
    deleted: bool
