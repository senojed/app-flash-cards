import uuid
import random
from datetime import date, timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.card import Card, CardField
from app.models.lesson import Lesson, LessonDirectionMode
from app.models.language import DirectionMode
from app.models.progress import CardProgress, ProgressDirection
from app.schemas.progress import StudySessionRequest, StudyCard, RateRequest, RateResponse
from app.services.sm2 import sm2_update, is_learned as sm2_is_learned
from app.config import settings

router = APIRouter(prefix="/api/study", tags=["study"])


def resolve_direction(lesson: Lesson) -> DirectionMode:
    if lesson.direction_mode == LessonDirectionMode.inherit:
        return lesson.language.direction_mode
    return DirectionMode(lesson.direction_mode.value)


@router.post("/cards", response_model=list[StudyCard])
async def get_study_cards(
    req: StudySessionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cards_to_study = []
    for lesson_id in req.lesson_ids:
        result = await db.execute(
            select(Card)
            .where(Card.lesson_id == lesson_id)
            .options(
                joinedload(Card.fields),
                joinedload(Card.lesson).joinedload(Lesson.language),
            )
        )
        cards = result.unique().scalars().all()
        for card in cards:
            lesson = card.lesson
            direction = resolve_direction(lesson)

            if direction == DirectionMode.random:
                directions = [random.choice([ProgressDirection.front_to_back, ProgressDirection.back_to_front])]
            elif direction == DirectionMode.front_to_back:
                directions = [ProgressDirection.front_to_back]
            else:
                directions = [ProgressDirection.back_to_front]

            for d in directions:
                prog_result = await db.execute(
                    select(CardProgress).where(
                        CardProgress.card_id == card.id,
                        CardProgress.user_id == user.id,
                        CardProgress.direction == d,
                    )
                )
                prog = prog_result.scalar_one_or_none()
                if prog and prog.due_date > date.today():
                    continue

                front_field = next(f for f in card.fields if f.label == "front")
                back_field = next(f for f in card.fields if f.label == "back")

                if d == ProgressDirection.front_to_back:
                    front_content, back_content = front_field.content, back_field.content
                    fi, fa = front_field.image_path, front_field.audio_path
                    bi, ba = back_field.image_path, back_field.audio_path
                else:
                    front_content, back_content = back_field.content, front_field.content
                    fi, fa = back_field.image_path, back_field.audio_path
                    bi, ba = front_field.image_path, front_field.audio_path

                cards_to_study.append(StudyCard(
                    card_id=card.id,
                    direction=d,
                    front=front_content,
                    back=back_content,
                    front_image=fi,
                    front_audio=fa,
                    back_image=bi,
                    back_audio=ba,
                ))

    random.shuffle(cards_to_study)
    return cards_to_study


@router.post("/rate", response_model=RateResponse)
async def rate_card(
    req: RateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    prog_result = await db.execute(
        select(CardProgress).where(
            CardProgress.card_id == req.card_id,
            CardProgress.user_id == user.id,
            CardProgress.direction == req.direction,
        )
    )
    prog = prog_result.scalar_one_or_none()

    previous_state = {
        "card_id": str(req.card_id),
        "direction": req.direction.value,
        "interval": prog.interval if prog else 1,
        "ease_factor": prog.ease_factor if prog else 2.5,
        "repetitions": prog.repetitions if prog else 0,
        "is_learned": prog.is_learned if prog else False,
        "is_new": prog is None,
    }

    result = sm2_update(
        interval=prog.interval if prog else 1,
        ease_factor=prog.ease_factor if prog else 2.5,
        repetitions=prog.repetitions if prog else 0,
        quality=req.quality,
    )
    learned = sm2_is_learned(result["interval"], settings.sm2_learned_threshold_days)

    if prog is None:
        prog = CardProgress(
            card_id=req.card_id,
            user_id=user.id,
            direction=req.direction,
        )
        db.add(prog)

    prog.interval = result["interval"]
    prog.ease_factor = result["ease_factor"]
    prog.repetitions = result["repetitions"]
    prog.due_date = date.today() + timedelta(days=result["interval"])
    prog.last_reviewed = datetime.utcnow()
    prog.is_learned = learned
    await db.commit()

    return RateResponse(
        card_id=req.card_id,
        direction=req.direction,
        new_interval=result["interval"],
        new_ease_factor=result["ease_factor"],
        is_learned=learned,
        previous_state=previous_state,
    )


@router.post("/undo", status_code=204)
async def undo_rating(
    previous_state: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not previous_state:
        return
    prog_result = await db.execute(
        select(CardProgress).where(
            CardProgress.card_id == uuid.UUID(previous_state["card_id"]),
            CardProgress.user_id == user.id,
            CardProgress.direction == ProgressDirection(previous_state["direction"]),
        )
    )
    prog = prog_result.scalar_one_or_none()
    if prog:
        if previous_state.get("is_new"):
            await db.delete(prog)
        else:
            prog.interval = previous_state["interval"]
            prog.ease_factor = previous_state["ease_factor"]
            prog.repetitions = previous_state["repetitions"]
            prog.is_learned = previous_state["is_learned"]
        await db.commit()
