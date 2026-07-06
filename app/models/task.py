from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    datum: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    task: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    done: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="tasks"
    )