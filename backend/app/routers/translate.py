from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.config import settings

router = APIRouter(prefix="/api/translate", tags=["translate"])


class TranslateRequest(BaseModel):
    text: str
    target_lang: str
    source_lang: str = "auto"


@router.post("")
async def translate(req: TranslateRequest):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.post(
                f"{settings.libretranslate_url}/translate",
                json={"q": req.text, "source": req.source_lang, "target": req.target_lang},
            )
            resp.raise_for_status()
            return {"translation": resp.json()["translatedText"]}
        except (httpx.RequestError, httpx.HTTPStatusError):
            raise HTTPException(503, "Translation service unavailable")
