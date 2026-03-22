from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.progress import CardProgress

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
async def get_stats(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    today = date.today()

    result = await db.execute(
        select(func.date(CardProgress.last_reviewed))
        .where(CardProgress.user_id == user.id, CardProgress.last_reviewed.isnot(None))
        .distinct()
        .order_by(func.date(CardProgress.last_reviewed).desc())
    )
    review_dates = [row[0] for row in result.all()]
    streak = _calculate_streak(review_dates, today)

    today_result = await db.execute(
        select(func.count()).where(
            CardProgress.user_id == user.id,
            func.date(CardProgress.last_reviewed) == today,
        )
    )
    reviews_today = today_result.scalar() or 0

    learned_result = await db.execute(
        select(func.count()).where(CardProgress.user_id == user.id, CardProgress.is_learned == True)
    )
    total_learned = learned_result.scalar() or 0

    reviews_per_day = await _reviews_per_day(db, user.id, today, days=7)
    accuracy_7days = await _accuracy_per_day(db, user.id, today, days=7)

    total_result = await db.execute(
        select(func.count()).where(CardProgress.user_id == user.id)
    )
    total_cards = total_result.scalar() or 0

    return {
        "streak_days": streak,
        "total_reviews_today": reviews_today,
        "total_learned": total_learned,
        "total_cards": total_cards,
        "reviews_per_day": reviews_per_day,
        "accuracy_7days": accuracy_7days,
    }


def _calculate_streak(dates: list, today: date) -> int:
    if not dates:
        return 0
    streak = 0
    current = today
    for d in dates:
        if isinstance(d, str):
            from datetime import datetime
            d = datetime.strptime(d, "%Y-%m-%d").date()
        if d == current or d == current - timedelta(days=1):
            streak += 1
            current = d
        else:
            break
    return streak


async def _accuracy_per_day(db, user_id, today: date, days: int) -> list[float]:
    """Accuracy = avg ease_factor normalized (1.3=0%, 4.0=100%) for cards reviewed each day."""
    results = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        result = await db.execute(
            select(func.avg(CardProgress.ease_factor)).where(
                CardProgress.user_id == user_id,
                func.date(CardProgress.last_reviewed) == day,
            )
        )
        avg_ef = result.scalar()
        if avg_ef is None:
            results.append(0.0)
        else:
            # normalize: ease_factor range 1.3–4.0 → 0–1
            normalized = max(0.0, min(1.0, (avg_ef - 1.3) / (4.0 - 1.3)))
            results.append(round(normalized, 3))
    return results


async def _reviews_per_day(db, user_id, today: date, days: int) -> list[dict]:
    results = []
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        result = await db.execute(
            select(func.count()).where(
                CardProgress.user_id == user_id,
                func.date(CardProgress.last_reviewed) == day,
            )
        )
        count = result.scalar() or 0
        results.append({"date": day.isoformat(), "count": count})
    return results
