from fastapi import FastAPI, Depends
from app.auth import get_current_user
from app.models.user import User
from app.routers import languages

app = FastAPI(title="FlashCards API")

app.include_router(languages.router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/me")
async def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}
