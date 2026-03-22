import uuid
from datetime import datetime, date
from sqlalchemy import Integer, DateTime, Date, Boolean, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class ProgressDirection(str, enum.Enum):
    front_to_back = "front_to_back"
    back_to_front = "back_to_front"


class CardProgress(Base):
    __tablename__ = "card_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    direction: Mapped[ProgressDirection] = mapped_column(SAEnum(ProgressDirection))
    interval: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    due_date: Mapped[date] = mapped_column(Date, default=date.today)
    last_reviewed: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_learned: Mapped[bool] = mapped_column(Boolean, default=False)

    card: Mapped["Card"] = relationship(back_populates="progress")
