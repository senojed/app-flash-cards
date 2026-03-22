import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class LessonDirectionMode(str, enum.Enum):
    front_to_back = "front_to_back"
    back_to_front = "back_to_front"
    random = "random"
    inherit = "inherit"


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    language_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("languages.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    direction_mode: Mapped[LessonDirectionMode] = mapped_column(SAEnum(LessonDirectionMode), default=LessonDirectionMode.inherit)
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    language: Mapped["Language"] = relationship(back_populates="lessons")
    cards: Mapped[list["Card"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
