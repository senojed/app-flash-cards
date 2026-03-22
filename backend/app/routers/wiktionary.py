from fastapi import APIRouter
import httpx
import re

router = APIRouter(prefix="/api/wiktionary", tags=["wiktionary"])


@router.get("/gender")
async def get_gender(word: str):
    """Vrátí člen (der/die/das) pro německé podstatné jméno, nebo None."""
    clean = word.lower().strip().split()[-1]

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://en.wiktionary.org/w/api.php",
                params={
                    "action": "parse",
                    "page": clean,
                    "prop": "wikitext",
                    "format": "json",
                    "section": 0,
                },
            )
            if resp.status_code != 200:
                return {"article": None}

            wikitext = resp.json().get("parse", {}).get("wikitext", {}).get("*", "")

            if "==German==" not in wikitext:
                return {"article": None}

            # |g=m, |g=f, |g=n
            gender_match = re.search(r"\|g=([mfn])", wikitext)
            if gender_match:
                g = gender_match.group(1)
                article = {"m": "der", "f": "die", "n": "das"}.get(g)
                return {"article": article}

        return {"article": None}
    except Exception:
        return {"article": None}
