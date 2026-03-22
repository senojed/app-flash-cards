import uuid
from pydantic import BaseModel, model_validator


class CardFieldIn(BaseModel):
    label: str
    content: str


class CardCreate(BaseModel):
    lesson_id: uuid.UUID
    fields: list[CardFieldIn]

    @model_validator(mode="after")
    def validate_fields(self):
        labels = {f.label for f in self.fields}
        if labels != {"front", "back"}:
            raise ValueError("Card must have exactly 'front' and 'back' fields")
        return self


class CardFieldUpdate(BaseModel):
    label: str
    content: str


class CardUpdate(BaseModel):
    fields: list[CardFieldUpdate]


class CardFieldOut(BaseModel):
    id: uuid.UUID
    label: str
    content: str
    order: int
    image_path: str | None
    audio_path: str | None

    model_config = {"from_attributes": True}


class CardOut(BaseModel):
    id: uuid.UUID
    lesson_id: uuid.UUID
    fields: list[CardFieldOut]

    model_config = {"from_attributes": True}
