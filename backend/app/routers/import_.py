import csv
import io
import json
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.card import Card, CardField
from app.models.lesson import Lesson
from app.models.language import Language

router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("")
async def import_cards(
    lesson_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    lesson_result = await db.execute(
        select(Lesson).join(Lesson.language).where(
            Lesson.id == lesson_id,
            Language.user_id == user.id,
        )
    )
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404)

    content = await file.read()

    if file.filename.endswith(".csv"):
        rows = _parse_csv(content)
    elif file.filename.endswith(".json"):
        rows = _parse_json(content)
    else:
        raise HTTPException(400, "Unsupported format. Use CSV or JSON.")

    existing_result = await db.execute(
        select(CardField.content).join(CardField.card).where(
            Card.lesson_id == lesson_id,
            CardField.label == "front",
        )
    )
    existing_fronts = {row[0].strip() for row in existing_result.all()}

    imported = 0
    skipped = 0
    for row in rows:
        front = row.get("front", "").strip()
        back = row.get("back", "").strip()
        if not front or not back:
            continue
        if front in existing_fronts:
            skipped += 1
            continue
        card = Card(lesson_id=lesson_id)
        db.add(card)
        await db.flush()
        db.add(CardField(card_id=card.id, label="front", content=front, order=0))
        db.add(CardField(card_id=card.id, label="back", content=back, order=1))
        existing_fronts.add(front)
        imported += 1

    await db.commit()
    return {"imported": imported, "skipped": skipped}


def _parse_csv(content: bytes) -> list[dict]:
    text = content.decode("utf-8-sig").strip()
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def _parse_json(content: bytes) -> list[dict]:
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(400, f"Invalid JSON: {e}")
