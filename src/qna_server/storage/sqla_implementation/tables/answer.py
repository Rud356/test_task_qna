from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTable


class AnswerTable(BaseTable):
    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("question.id")
    )
    user_id: Mapped[str] = mapped_column(String(320))
    text: Mapped[str] = mapped_column(
        String(2048)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __tablename__ = "answer"
