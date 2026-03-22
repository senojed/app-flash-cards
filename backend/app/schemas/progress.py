import uuid
from pydantic import BaseModel
from app.models.progress import ProgressDirection


class StudySessionRequest(BaseModel):
    lesson_ids: list[uuid.UUID]
    force: bool = False  # ignorovat due_date, vrátit všechny karty


class StudyCard(BaseModel):
    card_id: uuid.UUID
    direction: ProgressDirection
    front: str
    back: str
    front_image: str | None
    front_audio: str | None
    back_image: str | None
    back_audio: str | None


class RateRequest(BaseModel):
    card_id: uuid.UUID
    direction: ProgressDirection
    quality: int  # 0, 3, 4, 5
    previous_state: dict | None = None


class RateResponse(BaseModel):
    card_id: uuid.UUID
    direction: ProgressDirection
    new_interval: int
    new_ease_factor: float
    is_learned: bool
    previous_state: dict
