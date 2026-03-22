import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

HEADERS = {"Remote-User": "testuser"}


@pytest.mark.asyncio
async def test_dashboard_returns_hierarchy():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        lang_resp = await ac.post("/api/languages", json={"name": "Angličtina", "emoji": "🇬🇧"}, headers=HEADERS)
        lang_id = lang_resp.json()["id"]

        lesson_resp = await ac.post("/api/lessons", json={"language_id": lang_id, "name": "Lekce 1"}, headers=HEADERS)
        lesson_id = lesson_resp.json()["id"]

        await ac.post("/api/cards", json={
            "lesson_id": lesson_id,
            "fields": [{"label": "front", "content": "Hello"}, {"label": "back", "content": "Ahoj"}]
        }, headers=HEADERS)

        resp = await ac.get("/api/languages/dashboard", headers=HEADERS)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    lang_data = data[0]
    assert lang_data["name"] == "Angličtina"
    assert lang_data["total_cards"] == 1
    assert lang_data["learned_cards"] == 0
    assert len(lang_data["lessons"]) == 1
    assert lang_data["lessons"][0]["total_cards"] == 1
