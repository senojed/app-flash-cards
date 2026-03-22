import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.language import Language
from app.models.lesson import Lesson
from app.models.card import Card
from app.models.progress import CardProgress
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonOut

router = APIRouter(prefix="/api/lessons", tags=["lessons"])


@router.get("", response_model=list[LessonOut])
async def list_lessons(language_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson)
        .join(Lesson.language)
        .where(Lesson.language_id == language_id, Language.user_id == user.id)
        .order_by(Lesson.order)
    )
    return result.scalars().all()


@router.post("", response_model=LessonOut, status_code=201)
async def create_lesson(data: LessonCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lang_result = await db.execute(select(Language).where(Language.id == data.language_id, Language.user_id == user.id))
    if not lang_result.scalar_one_or_none():
        raise HTTPException(404)
    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.patch("/{lesson_id}", response_model=LessonOut)
async def update_lesson(lesson_id: uuid.UUID, data: LessonUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).join(Lesson.language)
        .where(Lesson.id == lesson_id, Language.user_id == user.id)
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404)
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(lesson, k, v)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.delete("/{lesson_id}", status_code=204)
async def delete_lesson(lesson_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Lesson).join(Lesson.language)
        .where(Lesson.id == lesson_id, Language.user_id == user.id)
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404)
    await db.delete(lesson)
    await db.commit()


@router.delete("/{lesson_id}/progress", status_code=204)
async def reset_lesson_progress(lesson_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        sql_delete(CardProgress).where(
            CardProgress.user_id == user.id,
            CardProgress.card_id.in_(
                select(Card.id).where(Card.lesson_id == lesson_id)
            )
        )
    )
    await db.commit()
