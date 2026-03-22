from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User

async def get_current_user(
    remote_user: str | None = Header(default=None, alias="Remote-User"),
    remote_email: str | None = Header(default=None, alias="Remote-Email"),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(select(User).where(User.username == remote_user))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(username=remote_user, email=remote_email)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
