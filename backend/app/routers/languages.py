import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from sqlalchemy.orm import joinedload
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.language import Language, DirectionMode
from app.models.lesson import Lesson, LessonDirectionMode
from app.models.card import Card
from app.models.progress import CardProgress, ProgressDirection
from app.schemas.language import LanguageCreate, LanguageUpdate, LanguageOut, LanguageDashboard, LessonSummary

router = APIRouter(prefix="/api/languages", tags=["languages"])


@router.get("/dashboard", response_model=list[LanguageDashboard])
async def dashboard(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Language)
        .where(Language.user_id == user.id)
        .options(joinedload(Language.lessons).joinedload(Lesson.cards).joinedload(Card.progress))
        .order_by(Language.order)
    )
    languages = result.unique().scalars().all()

    output = []
    for lang in languages:
        lessons_out = []
        lang_total = lang_learned = 0
        for lesson in sorted(lang.lessons, key=lambda l: l.order):
            total = len(lesson.cards)
            learned = sum(1 for card in lesson.cards if _is_card_learned(card, lesson, lang, user.id))
            lang_total += total
            lang_learned += learned
            lessons_out.append(LessonSummary(
                id=lesson.id, name=lesson.name, direction_mode=lesson.direction_mode,
                order=lesson.order, total_cards=total, learned_cards=learned,
            ))
        output.append(LanguageDashboard(
            id=lang.id, name=lang.name, emoji=lang.emoji, direction_mode=lang.direction_mode,
            source_lang=lang.source_lang, target_lang=lang.target_lang, order=lang.order,
            total_cards=lang_total, learned_cards=lang_learned, lessons=lessons_out,
        ))
    return output


def _is_card_learned(card, lesson, lang, user_id) -> bool:
    effective = lesson.direction_mode if lesson.direction_mode != LessonDirectionMode.inherit else LessonDirectionMode(lang.direction_mode.value)
    progress = {p.direction: p for p in card.progress if p.user_id == user_id}
    if effective == LessonDirectionMode.front_to_back:
        p = progress.get(ProgressDirection.front_to_back)
        return p is not None and p.is_learned
    elif effective == LessonDirectionMode.back_to_front:
        p = progress.get(ProgressDirection.back_to_front)
        return p is not None and p.is_learned
    else:
        pf = progress.get(ProgressDirection.front_to_back)
        pb = progress.get(ProgressDirection.back_to_front)
        return pf is not None and pf.is_learned and pb is not None and pb.is_learned


@router.get("", response_model=list[LanguageOut])
async def list_languages(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).where(Language.user_id == user.id).order_by(Language.order))
    return result.scalars().all()


@router.post("", response_model=LanguageOut, status_code=201)
async def create_language(data: LanguageCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    lang = Language(**data.model_dump(), user_id=user.id)
    db.add(lang)
    await db.commit()
    await db.refresh(lang)
    return lang


@router.patch("/{lang_id}", response_model=LanguageOut)
async def update_language(lang_id: uuid.UUID, data: LanguageUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).where(Language.id == lang_id, Language.user_id == user.id))
    lang = result.scalar_one_or_none()
    if not lang:
        raise HTTPException(404)
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(lang, k, v)
    await db.commit()
    await db.refresh(lang)
    return lang


@router.delete("/{lang_id}", status_code=204)
async def delete_language(lang_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Language).where(Language.id == lang_id, Language.user_id == user.id))
    lang = result.scalar_one_or_none()
    if not lang:
        raise HTTPException(404)
    await db.delete(lang)
    await db.commit()


@router.delete("/{lang_id}/progress", status_code=204)
async def reset_language_progress(lang_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(
        sql_delete(CardProgress).where(
            CardProgress.user_id == user.id,
            CardProgress.card_id.in_(
                select(Card.id).join(Card.lesson).join(Lesson.language)
                .where(Language.id == lang_id, Language.user_id == user.id)
            )
        )
    )
    await db.commit()
