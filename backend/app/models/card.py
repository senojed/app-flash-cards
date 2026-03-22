import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    lesson: Mapped["Lesson"] = relationship(back_populates="cards")
    fields: Mapped[list["CardField"]] = relationship(back_populates="card", cascade="all, delete-orphan")
    progress: Mapped[list["CardProgress"]] = relationship(back_populates="card", cascade="all, delete-orphan")


class CardField(Base):
    __tablename__ = "card_fields"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"))
    label: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text, default="")
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_tested: Mapped[bool] = mapped_column(Boolean, default=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    audio_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    card: Mapped["Card"] = relationship(back_populates="fields")
