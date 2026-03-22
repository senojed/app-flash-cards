import uuid
from pydantic import BaseModel
from app.models.lesson import LessonDirectionMode


class LessonCreate(BaseModel):
    language_id: uuid.UUID
    name: str
    direction_mode: LessonDirectionMode = LessonDirectionMode.inherit
    order: int = 0


class LessonUpdate(BaseModel):
    name: str | None = None
    direction_mode: LessonDirectionMode | None = None
    order: int | None = None


class LessonOut(BaseModel):
    id: uuid.UUID
    language_id: uuid.UUID
    name: str
    direction_mode: LessonDirectionMode
    order: int
    total_cards: int = 0
    learned_cards: int = 0

    model_config = {"from_attributes": True}
