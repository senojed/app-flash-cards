import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.language import Language
from app.models.lesson import Lesson
from app.models.card import Card, CardField
from app.schemas.card import CardCreate, CardUpdate, CardOut

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.get("", response_model=list[CardOut])
async def list_cards(lesson_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Card)
        .join(Card.lesson).join(Lesson.language)
        .where(Card.lesson_id == lesson_id, Language.user_id == user.id)
        .options(joinedload(Card.fields))
    )
    return result.unique().scalars().all()


@router.post("", response_model=CardOut, status_code=201)
async def create_card(data: CardCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lesson_result = await db.execute(
        select(Lesson).join(Lesson.language)
        .where(Lesson.id == data.lesson_id, Language.user_id == user.id)
    )
    if not lesson_result.scalar_one_or_none():
        raise HTTPException(404)

    card = Card(lesson_id=data.lesson_id)
    db.add(card)
    await db.flush()

    for i, field in enumerate(data.fields):
        db.add(CardField(card_id=card.id, label=field.label, content=field.content, order=i))

    await db.commit()
    result = await db.execute(
        select(Card).where(Card.id == card.id).options(joinedload(Card.fields))
    )
    return result.unique().scalar_one()


@router.patch("/{card_id}", response_model=CardOut)
async def update_card(card_id: uuid.UUID, data: CardUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Card).join(Card.lesson).join(Lesson.language)
        .where(Card.id == card_id, Language.user_id == user.id)
        .options(joinedload(Card.fields))
    )
    card = result.unique().scalar_one_or_none()
    if not card:
        raise HTTPException(404)

    for field_update in data.fields:
        field = next((f for f in card.fields if f.label == field_update.label), None)
        if field:
            field.content = field_update.content

    await db.commit()
    result = await db.execute(
        select(Card).where(Card.id == card.id).options(joinedload(Card.fields))
    )
    return result.unique().scalar_one()


@router.delete("/{card_id}", status_code=204)
async def delete_card(card_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Card).join(Card.lesson).join(Lesson.language)
        .where(Card.id == card_id, Language.user_id == user.id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(404)
    from app.services.media import delete_media
    delete_media(card_id)
    await db.delete(card)
    await db.commit()


@router.post("/{card_id}/media/{label}", status_code=200)
async def upload_media(
    card_id: uuid.UUID,
    label: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Card).join(Card.lesson).join(Lesson.language)
        .where(Card.id == card_id, Language.user_id == user.id)
    )
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(404)

    from app.services.media import save_media
    path = await save_media(card_id, label, file)

    field_result = await db.execute(
        select(CardField).where(CardField.card_id == card_id, CardField.label == label)
    )
    field = field_result.scalar_one_or_none()
    if not field:
        raise HTTPException(404, f"Field '{label}' not found")

    ext = path.split(".")[-1].lower()
    if ext in ("mp3", "ogg"):
        field.audio_path = path
    else:
        field.image_path = path

    await db.commit()
    return {"path": path}
