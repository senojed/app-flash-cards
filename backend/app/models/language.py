import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class DirectionMode(str, enum.Enum):
    front_to_back = "front_to_back"
    back_to_front = "back_to_front"
    random = "random"


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    emoji: Mapped[str] = mapped_column(String(10), default="🌐")
    direction_mode: Mapped[DirectionMode] = mapped_column(SAEnum(DirectionMode), default=DirectionMode.front_to_back)
    target_lang: Mapped[str] = mapped_column(String(10), default="cs")
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="language", cascade="all, delete-orphan")
