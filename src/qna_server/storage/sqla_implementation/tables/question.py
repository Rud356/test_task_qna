from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .answer import AnswerTable
from .base import BaseTable


class QuestionTable(BaseTable):
    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True
    )
    text: Mapped[str] = mapped_column(
        String(2048)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    answers: Mapped[list[AnswerTable]] = relationship(
        lazy="raise",
        cascade="all, delete-orphan"
    )
    __tablename__ = "question"
