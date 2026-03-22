from fastapi import FastAPI, Depends
from app.auth import get_current_user
from app.models.user import User
from app.routers import languages, lessons, cards, study, import_, translate, stats, wiktionary

app = FastAPI(title="FlashCards API")

app.include_router(languages.router)
app.include_router(lessons.router)
app.include_router(cards.router)
app.include_router(study.router)
app.include_router(import_.router)
app.include_router(translate.router)
app.include_router(stats.router)
app.include_router(wiktionary.router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/me")
async def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "email": user.email}
