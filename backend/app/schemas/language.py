import uuid
from pydantic import BaseModel
from app.models.language import DirectionMode
from app.models.lesson import LessonDirectionMode


class LanguageCreate(BaseModel):
    name: str
    emoji: str = "🌐"
    direction_mode: DirectionMode = DirectionMode.front_to_back
    source_lang: str = "en"
    target_lang: str = "cs"
    order: int = 0


class LanguageUpdate(BaseModel):
    name: str | None = None
    emoji: str | None = None
    direction_mode: DirectionMode | None = None
    source_lang: str | None = None
    target_lang: str | None = None
    order: int | None = None


class LanguageOut(BaseModel):
    id: uuid.UUID
    name: str
    emoji: str
    direction_mode: DirectionMode
    source_lang: str
    target_lang: str
    order: int
    total_cards: int = 0
    learned_cards: int = 0

    model_config = {"from_attributes": True}


class LessonSummary(BaseModel):
    id: uuid.UUID
    name: str
    direction_mode: LessonDirectionMode
    order: int
    total_cards: int
    learned_cards: int

    model_config = {"from_attributes": True}


class LanguageDashboard(BaseModel):
    id: uuid.UUID
    name: str
    emoji: str
    direction_mode: DirectionMode
    source_lang: str
    target_lang: str
    order: int
    total_cards: int
    learned_cards: int
    lessons: list[LessonSummary]

    model_config = {"from_attributes": True}
