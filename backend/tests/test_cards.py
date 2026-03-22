import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

HEADERS = {"Remote-User": "testuser"}


async def _create_language_and_lesson(ac):
    lang_resp = await ac.post("/api/languages", json={"name": "Angličtina"}, headers=HEADERS)
    lang_id = lang_resp.json()["id"]
    lesson_resp = await ac.post("/api/lessons", json={"language_id": lang_id, "name": "Lekce 1"}, headers=HEADERS)
    lesson_id = lesson_resp.json()["id"]
    return lang_id, lesson_id


@pytest.mark.asyncio
async def test_create_card_requires_front_and_back():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        _, lesson_id = await _create_language_and_lesson(ac)
        resp = await ac.post("/api/cards", json={
            "lesson_id": lesson_id,
            "fields": [{"label": "front", "content": "Hello"}]
        }, headers=HEADERS)
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_card_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        _, lesson_id = await _create_language_and_lesson(ac)
        resp = await ac.post("/api/cards", json={
            "lesson_id": lesson_id,
            "fields": [
                {"label": "front", "content": "Hello"},
                {"label": "back", "content": "Ahoj"},
            ]
        }, headers=HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["fields"]) == 2


@pytest.mark.asyncio
async def test_list_cards():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        _, lesson_id = await _create_language_and_lesson(ac)
        await ac.post("/api/cards", json={
            "lesson_id": lesson_id,
            "fields": [{"label": "front", "content": "Cat"}, {"label": "back", "content": "Kočka"}]
        }, headers=HEADERS)
        resp = await ac.get(f"/api/cards?lesson_id={lesson_id}", headers=HEADERS)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
